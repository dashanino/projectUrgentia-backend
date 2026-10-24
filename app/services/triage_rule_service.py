
from datetime import datetime, timezone

from app.extensions import db

from app.models.pretriage import Pretriage
from app.models.pretriage_antecedente import PretriageAntecedente
from app.models.pretriage_red_flag import PretriageRedFlag
from app.models.triage_rule import TriageRule
from app.models.triage_rule_antecedente import TriageRuleAntecedente
from app.models.red_flag import RedFlag


def evaluar_reglas_triage(id_pretriage, id_user):

    # 1. Buscar y validar el pretriage
    pretriage = db.session.get(Pretriage, id_pretriage)

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para consultar este pretriage"
        )

    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage ya no se encuentra iniciado"
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

    # 3. Obtener banderas rojas seleccionadas
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

    # 4. Evaluar reglas de alta prioridad
    for id_bandera in ids_banderas:

        reglas = (
            db.session.query(TriageRule)
            .filter(
                TriageRule.id_poblacion == pretriage.id_poblacion,
                TriageRule.id_bandera == id_bandera,
                TriageRule.alta_prioridad.is_(True)
            )
            .all()
        )

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

            # Los antecedentes requeridos por la regla
            # deben estar presentes en el paciente.
            # Se permiten antecedentes adicionales.
            if not ids_antecedentes_regla.issubset(
                ids_antecedentes
            ):
                continue

            bandera = db.session.get(
                RedFlag,
                regla.id_bandera
            )

            # 5. Registrar alerta en PostgreSQL
            pretriage.reglas_evaluadas = True
            pretriage.alerta_reglas = True
            pretriage.fecha_evaluacion_reglas = (
                datetime.now(timezone.utc)
            )

            db.session.commit()

            return {
                "id_pretriage": id_pretriage,
                "alta_prioridad": True,
                "accion": "alerta",
                "regla_activadora": regla.id,
                "bandera_activadora": {
                    "id_bandera": id_bandera,
                    "name": bandera.name if bandera else None
                }
            }

    # 6. Ninguna regla de alta prioridad se activó
    pretriage.reglas_evaluadas = True
    pretriage.alerta_reglas = False
    pretriage.fecha_evaluacion_reglas = (
        datetime.now(timezone.utc)
    )

    db.session.commit()

    return {
        "id_pretriage": id_pretriage,
        "alta_prioridad": False,
        "accion": "continuar_ia"
    }
