from flask_jwt_extended import get_jwt, get_jwt_identity
from app.extensions import db
from app.models.pretriage import Pretriage


def validar_acceso_pretriage(id_pretriage):

    # 1. Validar el tipo de acceso
    claims = get_jwt()

    if claims.get("tipo_acceso") != "emergencia":
        raise PermissionError(
            "Este endpoint requiere acceso de emergencia"
        )

    # 2. Validar identidad y pretriage del token
    try:
        id_user = int(get_jwt_identity())
        id_pretriage_token = int(
            claims.get("id_pretriage")
        )
    except (TypeError, ValueError):
        raise PermissionError(
            "El token no contiene un acceso válido"
        )

    if id_pretriage_token != id_pretriage:
        raise PermissionError(
            "El pretriage no corresponde al token"
        )

    # 3. Consultar el pretriage
    pretriage = db.session.get(
        Pretriage,
        id_pretriage
    )

    if pretriage is None:
        raise ValueError(
            "El pretriage no existe"
        )

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para consultar este pretriage"
        )

    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage no está iniciado"
        )

    return id_user


def validar_evaluacion_inicial(
    id_pretriage,
    requerir_sintomas=False
):

    # 1. Consultar el pretriage
    pretriage = db.session.get(
        Pretriage,
        id_pretriage
    )

    if pretriage is None:
        raise ValueError(
            "El pretriage no existe"
        )

    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage no se encuentra iniciado"
        )

    # 2. Verificar evaluación de reglas
    if pretriage.reglas_evaluadas is not True:
        raise ValueError(
            "Primero debes completar la evaluación inicial de triage"
        )

    # 3. Bloquear si existe una alerta
    if pretriage.alerta_reglas is True:
        raise PermissionError(
            "Se detectó una alerta de alta prioridad. "
            "No se permite continuar con las preguntas de IA. "
            "Se requiere valoración médica urgente."
        )

    # 4. Validar consistencia de la evaluación
    if pretriage.alerta_reglas is not False:
        raise ValueError(
            "El resultado de la evaluación inicial no es válido"
        )

    # 5. Exigir síntomas completados solo cuando
    # la operación lo requiera
    if (
        requerir_sintomas
        and pretriage.sintomas_completados is not True
    ):
        raise ValueError(
            "Primero debes completar la selección de síntomas "
            "antes de continuar con la inteligencia artificial."
        )

    return pretriage
