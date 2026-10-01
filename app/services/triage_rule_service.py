from app.extensions import db

from app.models.pretriage import Pretriage
from app.models.pretriage_antecedente import PretriageAntecedente
from app.models.pretriage_red_flag import PretriageRedFlag

from app.models.triage_rule import TriageRule
from app.models.triage_rule_antecedente import TriageRuleAntecedente

from app.models.red_flag import RedFlag


def evaluar_reglas_triaje(id_pretriage, id_user):

    # 1. Buscar el pretriaje
    pretriage = db.session.get(Pretriage, id_pretriage)

    if pretriage is None:
        raise ValueError("El pretriaje no existe")

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para consultar este pretriaje"
        )

    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriaje ya no se encuentra iniciado"
        )

    if pretriage.id_poblacion is None:
        raise ValueError(
            "Primero debes seleccionar una población"
        )

    # 2. Obtener antecedentes seleccionados
    antecedentes_pretriage = (
        db.session.query(PretriageAntecedente.id_antecedente)
        .filter(
            PretriageAntecedente.id_pretriage == id_pretriage
        )
        .all()
    )

    ids_antecedentes = {
        fila.id_antecedente
        for fila in antecedentes_pretriage
    }

    # 3. Obtener banderas seleccionadas
    banderas_pretriage = (
        db.session.query(PretriageRedFlag.id_bandera)
        .filter(
            PretriageRedFlag.id_pretriage == id_pretriage
        )
        .all()
    )

    ids_banderas = {
        fila.id_bandera
        for fila in banderas_pretriage
    }

    if not ids_banderas:
        raise ValueError(
            "Debes seleccionar al menos una bandera roja"
        )

    # 4. Buscar reglas candidatas:
    # misma población + cualquiera de las banderas seleccionadas
    reglas = (
        db.session.query(TriageRule)
        .filter(
            TriageRule.id_poblacion == pretriage.id_poblacion,
            TriageRule.id_bandera.in_(ids_banderas)
        )
        .all()
    )

    # 5. Revisar las reglas
    #
    # IMPORTANTE:
    # los antecedentes deben coincidir EXACTAMENTE.
    for regla in reglas:

        antecedentes_regla = (
            db.session.query(
                TriageRuleAntecedente.id_antecedente
            )
            .filter(
                TriageRuleAntecedente.id_regla == regla.id
            )
            .all()
        )

        ids_antecedentes_regla = {
            fila.id_antecedente
            for fila in antecedentes_regla
        }

        # Esta regla no corresponde al usuario
        if ids_antecedentes_regla != ids_antecedentes:
            continue

        # Encontramos una coincidencia exacta
        if regla.alta_prioridad:

            bandera = db.session.get(
                RedFlag,
                regla.id_bandera
            )

            return {
                "id_pretriage": id_pretriage,
                "alta_prioridad": True,
                "accion": "alerta",
                "bandera_activadora": {
                    "id_bandera": bandera.id,
                    "name": bandera.name
                }
            }

    # 6. Llegamos aquí solamente si ninguna regla exacta dio Sí
    return {
        "id_pretriage": id_pretriage,
        "alta_prioridad": False,
        "accion": "continuar_ia"
    }