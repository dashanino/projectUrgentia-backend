from datetime import datetime, timezone
from app.extensions import db
from app.models.pretriage import Pretriage
from app.models.pregunta_ia import PreguntaIA


def guardar_respuesta_ia(
    id_pretriage,
    id_pregunta,
    respuesta,
    id_user
):
    pretriage = db.session.get(Pretriage, id_pretriage)

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para modificar este pretriage"
        )

    if pretriage.estado != "iniciado":
        raise ValueError("El pretriage no está iniciado")

    pregunta = db.session.get(PreguntaIA, id_pregunta)

    if pregunta is None:
        raise ValueError("La pregunta no existe")

    if pregunta.id_pretriage != id_pretriage:
        raise PermissionError(
            "La pregunta no corresponde a este pretriage"
        )

    if pregunta.respuesta is not None:
        raise ValueError("Esta pregunta ya fue respondida")

    if not isinstance(respuesta, str) or not respuesta.strip():
        raise ValueError("La respuesta no puede estar vacía")

    if len(respuesta) > 2000:
        raise ValueError("La respuesta es demasiado larga")

    # Primero verificar que no exista una alerta activa.
    if pretriage.alerta_reglas is True or pretriage.estado_seguridad_ia == "alerta":
        raise ValueError(
            "El cuestionario está bloqueado por una alerta de seguridad"
        )

    # Solo guardar la respuesta si no existe un bloqueo.
    pregunta.respuesta = respuesta.strip()
    pregunta.answered_at = datetime.now(timezone.utc)

    pretriage.estado_seguridad_ia = "pendiente"

    # La transacción se confirmará después de revisar la seguridad.
    db.session.flush()

    return {
        "id_pretriage": id_pretriage,
        "id_pregunta": pregunta.id,
        "respuesta_guardada": True,
        "accion": "revision_seguridad_pendiente"
    }