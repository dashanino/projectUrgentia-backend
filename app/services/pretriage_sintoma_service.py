from app.extensions import db
from app.models.pretriage import Pretriage
from app.models.pretriage_sintoma import PretriageSintoma
from app.models.sintoma import Sintoma
from app.models.pretriage_red_flag import PretriageRedFlag
from app.models.pregunta_ia import PreguntaIA

from app.services.pretriage_access_service import (
    validar_evaluacion_inicial
)


def guardar_sintomas_pretriage(
    id_pretriage,
    id_user,
    ids_sintomas
):

    # 1. Buscar el pretriage
    pretriage = db.session.get(
        Pretriage,
        id_pretriage
    )

    if pretriage is None:
        raise ValueError(
            "El pretriage no existe"
        )

    # 2. Verificar que pertenezca al usuario
    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para modificar este pretriage"
        )

    # 3. Verificar que esté iniciado
    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage no está iniciado"
        )

    # 4. Verificar evaluación inicial y ausencia
    # de alerta de alta prioridad
    validar_evaluacion_inicial(id_pretriage)

    # 5. No permitir modificar síntomas después
    # de comenzar las preguntas de IA
    pregunta_existente = (
        db.session.query(PreguntaIA.id)
        .filter(
            PreguntaIA.id_pretriage == id_pretriage
        )
        .first()
    )

    if pregunta_existente is not None:
        raise PermissionError(
            "Ya comenzaron las preguntas de IA. "
            "No se pueden modificar los síntomas "
            "de este pretriage."
        )

    # 6. Validar lista de síntomas
    if not isinstance(ids_sintomas, list):
        raise ValueError(
            "Los síntomas deben enviarse como lista"
        )

    if any(
        type(id_sintoma) is not int
        for id_sintoma in ids_sintomas
    ):
        raise ValueError(
            "Los IDs de síntomas deben ser números enteros"
        )

    if len(ids_sintomas) != len(set(ids_sintomas)):
        raise ValueError(
            "Hay síntomas duplicados"
        )

    # 7. Obtener banderas seleccionadas
    banderas = {
        fila.id_bandera
        for fila in db.session.query(
            PretriageRedFlag.id_bandera
        )
        .filter_by(
            id_pretriage=id_pretriage
        )
        .all()
    }

    # 8. Consultar síntomas solicitados
    sintomas = (
        db.session.query(Sintoma)
        .filter(
            Sintoma.id.in_(ids_sintomas)
        )
        .all()
    ) if ids_sintomas else []

    if len(sintomas) != len(ids_sintomas):
        raise ValueError(
            "Uno o más síntomas no existen"
        )

    # 9. Validar que correspondan a las banderas
    if any(
        sintoma.id_bandera not in banderas
        for sintoma in sintomas
    ):
        raise ValueError(
            "Hay síntomas que no corresponden "
            "a las banderas seleccionadas"
        )

    try:
        # 10. Eliminar selección anterior
        db.session.query(PretriageSintoma).filter_by(
            id_pretriage=id_pretriage
        ).delete(synchronize_session=False)

        # 11. Guardar nuevos síntomas
        for sintoma in sintomas:
            db.session.add(
                PretriageSintoma(
                    id_pretriage=id_pretriage,
                    id_sintoma=sintoma.id
                )
            )
        # 12. Registrar que el paciente completó la etapa
        pretriage.sintomas_completados = True

        # 13. Confirmar cambios
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "id_pretriage": id_pretriage,
        "ids_sintomas": ids_sintomas,
        "cantidad": len(ids_sintomas)
    }
