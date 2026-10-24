import re
from app.extensions import db
from app.models.pretriage import Pretriage
from app.models.pregunta_ia import PreguntaIA


# Expresiones de ejemplo para pruebas del prototipo.
# No constituyen un protocolo clínico validado.
EXPRESIONES_ALERTA = {
    "dificultad_respiratoria": [
        r"\bno puedo respirar\b",
        r"\bme cuesta respirar\b",
        r"\bme estoy ahogando\b",
    ],
    "dolor_toracico": [
        r"\bdolor (?:fuerte |intenso )?en el pecho\b",
        r"\bpresion en el pecho\b",
    ],
    "perdida_conciencia": [
        r"\bperdi el conocimiento\b",
        r"\bme desmaye\b",
    ],
    "sangrado_importante": [
        r"\bno puedo detener el sangrado\b",
        r"\bsangrado abundante\b",
    ],
}


def normalizar_texto(texto):
    import unicodedata

    texto = unicodedata.normalize("NFKD", texto.lower())

    return "".join(
        caracter for caracter in texto
        if not unicodedata.combining(caracter)
    )


def detectar_alertas_texto(respuesta):
    """
    Detector preliminar basado en expresiones explícitas.

    Una coincidencia genera una alerta conservadora.
    La ausencia de coincidencias NO descarta emergencias.
    """
    texto = normalizar_texto(respuesta)
    alertas = []

    for categoria, patrones in EXPRESIONES_ALERTA.items():
        if any(re.search(patron, texto) for patron in patrones):
            alertas.append(categoria)

    return alertas


def revisar_seguridad_ia(id_pretriage, id_user):
    pretriage = db.session.get(Pretriage, id_pretriage)

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para revisar este pretriage"
        )

    if pretriage.estado != "iniciado":
        raise ValueError("El pretriage no está iniciado")

    if pretriage.alerta_reglas is True:
        return {
            "accion": "alerta",
            "mensaje": "Se requiere valoración médica urgente."
        }

    if pretriage.estado_seguridad_ia == "alerta":
        return {
            "accion": "alerta",
            "mensaje": "Existe una alerta de seguridad activa."
        }

    preguntas = (
        db.session.query(PreguntaIA)
        .filter_by(id_pretriage=id_pretriage)
        .order_by(PreguntaIA.orden)
        .all()
    )

    respondidas = [
        pregunta for pregunta in preguntas
        if pregunta.respuesta is not None
    ]

    if not respondidas:
        return {
            "accion": "sin_respuestas",
            "mensaje": "Todavía no existen respuestas para revisar."
        }

    alertas_detectadas = set()

    for pregunta in respondidas:
        alertas_detectadas.update(
            detectar_alertas_texto(pregunta.respuesta)
        )

    if alertas_detectadas:
        pretriage.estado_seguridad_ia = "alerta"
        

        return {
            "accion": "alerta",
            "estado_seguridad_ia": "alerta",
            "categorias_detectadas": sorted(alertas_detectadas),
            "mensaje": (
                "Se identificó una posible señal de alarma. "
                "Interrumpa el cuestionario y solicite "
                "valoración médica inmediata."
            )
        }

    # Sin coincidencias NO significa que sea seguro continuar.
    pretriage.estado_seguridad_ia = "pendiente"
    

    return {
        "accion": "revision_clinica",
        "estado_seguridad_ia": "pendiente",
        "respuestas_registradas": len(respondidas),
        "mensaje": (
            "No se identificaron coincidencias con las "
            "expresiones configuradas. Esto no descarta "
            "una emergencia. Se requiere revisión clínica."
        )
    }
