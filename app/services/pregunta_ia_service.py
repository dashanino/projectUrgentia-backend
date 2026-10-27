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

def guardar_respuestas_ia(
    id_pretriage,
    respuestas,
    id_user
):
    pretriage = db.session.get(
        Pretriage,
        id_pretriage
    )

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para modificar este pretriage"
        )

    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage no está iniciado"
        )

    if (
        pretriage.alerta_reglas is True
        or pretriage.estado_seguridad_ia == "alerta"
    ):
        raise ValueError(
            "El cuestionario está bloqueado por una alerta de seguridad"
        )

    if not isinstance(respuestas, list) or not respuestas:
        raise ValueError(
            "Debes enviar una lista de respuestas"
        )

    ids_preguntas = []

    respuestas_validas = []

    for item in respuestas:

        if not isinstance(item, dict):
            raise ValueError(
                "Cada respuesta debe tener id_pregunta y respuesta"
            )

        try:
            id_pregunta = int(
                item.get("id_pregunta")
            )
        except (TypeError, ValueError):
            raise ValueError(
                "El id de pregunta no es válido"
            )

        respuesta = item.get("respuesta")

        if (
            not isinstance(respuesta, str)
            or not respuesta.strip()
        ):
            raise ValueError(
                "Todas las preguntas deben tener una respuesta"
            )

        respuesta = respuesta.strip()

        if len(respuesta) > 2000:
            raise ValueError(
                "Una respuesta supera los 2000 caracteres"
            )

        ids_preguntas.append(id_pregunta)

        respuestas_validas.append(
            (
                id_pregunta,
                respuesta
            )
        )

    # No permitir IDs repetidos
    if len(ids_preguntas) != len(set(ids_preguntas)):
        raise ValueError(
            "No se puede responder una pregunta más de una vez"
        )

    preguntas = (
        db.session.query(PreguntaIA)
        .filter(
            PreguntaIA.id_pretriage == id_pretriage,
            PreguntaIA.id.in_(ids_preguntas)
        )
        .all()
    )

    preguntas_por_id = {
        pregunta.id: pregunta
        for pregunta in preguntas
    }

    if len(preguntas_por_id) != len(ids_preguntas):
        raise ValueError(
            "Una o más preguntas no pertenecen a este pretriage"
        )

    for id_pregunta in ids_preguntas:

        pregunta = preguntas_por_id[id_pregunta]

        if pregunta.respuesta is not None:
            raise ValueError(
                "Una o más preguntas ya fueron respondidas"
            )

    ahora = datetime.now(timezone.utc)

    for id_pregunta, respuesta in respuestas_validas:

        pregunta = preguntas_por_id[id_pregunta]

        pregunta.respuesta = respuesta
        pregunta.answered_at = ahora

    # IMPORTANTE:
    # la seguridad se revisará una sola vez
    # después de guardar TODO el bloque.

    pretriage.estado_seguridad_ia = "pendiente"

    db.session.flush()

    return {
        "id_pretriage": id_pretriage,
        "respuestas_guardadas": len(respuestas_validas),
        "accion": "revision_seguridad_pendiente"
    }