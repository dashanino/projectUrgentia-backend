from types import SimpleNamespace
import pytest

from app.services import pretriage_safety_service as safety


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def crear_pretriage(
    id_user=10,
    estado="iniciado",
    alerta_reglas=False,
    estado_seguridad_ia="pendiente"
):
    return SimpleNamespace(
        id=1,
        id_user=id_user,
        estado=estado,
        alerta_reglas=alerta_reglas,
        estado_seguridad_ia=estado_seguridad_ia
    )


def preparar_db(mocker, pretriage):
    mocker.patch.object(
        safety.db.session,
        "get",
        return_value=pretriage
    )


# =========================================================
# PRUEBAS DE ACCESO Y ESTADO DEL PRETRIAGE
# =========================================================

def test_no_permite_acceso_a_otro_usuario(mocker):
    preparar_db(
        mocker,
        crear_pretriage(id_user=10)
    )

    with pytest.raises(PermissionError):
        safety.revisar_seguridad_ia(
            id_pretriage=1,
            id_user=99
        )


def test_alerta_inicial_interrumpe_revision(mocker):
    preparar_db(
        mocker,
        crear_pretriage(alerta_reglas=True)
    )

    resultado = safety.revisar_seguridad_ia(
        id_pretriage=1,
        id_user=10
    )

    assert resultado["accion"] == "alerta"


def test_alerta_ia_bloquea_revision(mocker):
    preparar_db(
        mocker,
        crear_pretriage(
            estado_seguridad_ia="alerta"
        )
    )

    resultado = safety.revisar_seguridad_ia(
        id_pretriage=1,
        id_user=10
    )

    assert resultado["accion"] == "alerta"


def test_pretriage_inexistente(mocker):
    preparar_db(mocker, None)

    with pytest.raises(
        ValueError,
        match="no existe"
    ):
        safety.revisar_seguridad_ia(1, 10)


def test_pretriage_no_iniciado(mocker):
    preparar_db(
        mocker,
        crear_pretriage(estado="finalizado")
    )

    with pytest.raises(
        ValueError,
        match="no está iniciado"
    ):
        safety.revisar_seguridad_ia(1, 10)


# =========================================================
# PRUEBAS DE RESPUESTAS Y SEGURIDAD
# =========================================================

def test_sin_respuestas_no_autoriza_continuar(mocker):
    preparar_db(
        mocker,
        crear_pretriage()
    )

    consulta = mocker.MagicMock()
    consulta.filter_by.return_value = consulta
    consulta.order_by.return_value = consulta
    consulta.all.return_value = []

    mocker.patch.object(
        safety.db.session,
        "query",
        return_value=consulta
    )

    resultado = safety.revisar_seguridad_ia(1, 10)

    assert resultado["accion"] == "sin_respuestas"


def test_respuesta_registrada_sigue_pendiente(mocker):
    pretriage = crear_pretriage()

    preparar_db(
        mocker,
        pretriage
    )

    consulta = mocker.MagicMock()
    consulta.filter_by.return_value = consulta
    consulta.order_by.return_value = consulta
    consulta.all.return_value = [
        SimpleNamespace(
            respuesta="Respuesta simulada"
        )
    ]

    mocker.patch.object(
        safety.db.session,
        "query",
        return_value=consulta
    )

    commit = mocker.patch.object(
        safety.db.session,
        "commit"
    )

    resultado = safety.revisar_seguridad_ia(1, 10)

    assert (
        resultado["accion"]
        == "informacion_insuficiente"
    )

    assert (
        resultado["estado_seguridad_ia"]
        == "pendiente"
    )

    assert pretriage.estado_seguridad_ia == "pendiente"

    commit.assert_not_called()


# =========================================================
# PRUEBAS DE GENERACIÓN DE PREGUNTAS
# =========================================================

def test_no_generar_pregunta_durante_revision(mocker):
    from app.services.pretriage_agent_service import (
        PretriageAgentService
    )

    agente = object.__new__(
        PretriageAgentService
    )

    mocker.patch.object(
        agente,
        "obtener_contexto_clinico",
        return_value={}
    )

    pretriage = crear_pretriage(
        estado_seguridad_ia="en_revision"
    )

    mocker.patch(
        "app.services.pretriage_agent_service.db.session.get",
        return_value=pretriage
    )

    with pytest.raises(
        ValueError,
        match="comprobación de seguridad"
    ):
        agente.generate_additional_questions(1)


def test_no_generar_pregunta_con_alerta(mocker):
    from app.services.pretriage_agent_service import (
        PretriageAgentService
    )

    agente = object.__new__(
        PretriageAgentService
    )

    pretriage = crear_pretriage(
        estado_seguridad_ia="alerta"
    )

    mocker.patch(
        "app.services.pretriage_agent_service.db.session.get",
        return_value=pretriage
    )

    with pytest.raises(
        ValueError,
        match="alerta de seguridad"
    ):
        agente.generate_additional_questions(1)


# =========================================================
# PRUEBAS DE EVALUACIÓN FINAL
# =========================================================

def test_no_evaluar_con_revision_pendiente(mocker):
    from app.services.pretriage_agent_service import (
        PretriageAgentService
    )

    agente = object.__new__(
        PretriageAgentService
    )

    mocker.patch.object(
        agente,
        "obtener_contexto_clinico",
        return_value={}
    )

    mocker.patch(
        "app.services.pretriage_agent_service.db.session.get",
        return_value=crear_pretriage(
            estado_seguridad_ia="pendiente"
        )
    )

    with pytest.raises(
        ValueError,
        match="comprobación de seguridad"
    ):
        agente.evaluate(1)


def test_no_evaluar_con_alerta(mocker):
    from app.services.pretriage_agent_service import (
        PretriageAgentService
    )

    agente = object.__new__(
        PretriageAgentService
    )

    mocker.patch(
        "app.services.pretriage_agent_service.db.session.get",
        return_value=crear_pretriage(
            estado_seguridad_ia="alerta"
        )
    )

    with pytest.raises(
        ValueError,
        match="alerta de seguridad"
    ):
        agente.evaluate(1)


# =========================================================
# PRUEBAS DE DETECCIÓN DE EXPRESIONES DE ALERTA
# =========================================================

@pytest.mark.parametrize(
    "respuesta,categoria",
    [
        (
            "No puedo respirar",
            "dificultad_respiratoria"
        ),
        (
            "Me cuesta respirar",
            "dificultad_respiratoria"
        ),
        (
            "Tengo dolor fuerte en el pecho",
            "dolor_toracico"
        ),
        (
            "Perdí el conocimiento",
            "perdida_conciencia"
        ),
        (
            "Tengo sangrado abundante",
            "sangrado_importante"
        ),
    ]
)
def test_detecta_expresiones_de_alerta(
    respuesta,
    categoria
):
    assert categoria in safety.detectar_alertas_texto(
        respuesta
    )


# =========================================================
# PRUEBA DE BLOQUEO POR ALERTA DETECTADA
# =========================================================

def test_alerta_detectada_bloquea_pretriage(mocker):
    pretriage = crear_pretriage()

    preparar_db(
        mocker,
        pretriage
    )

    consulta = mocker.MagicMock()
    consulta.filter_by.return_value = consulta
    consulta.order_by.return_value = consulta
    consulta.all.return_value = [
        SimpleNamespace(
            respuesta="No puedo respirar"
        )
    ]

    mocker.patch.object(
        safety.db.session,
        "query",
        return_value=consulta
    )

    commit = mocker.patch.object(
        safety.db.session,
        "commit"
    )

    resultado = safety.revisar_seguridad_ia(1, 10)

    assert resultado["accion"] == "alerta"

    assert pretriage.estado_seguridad_ia == "alerta"

    assert (
        "dificultad_respiratoria"
        in resultado["categorias_detectadas"]
    )

    commit.assert_not_called()