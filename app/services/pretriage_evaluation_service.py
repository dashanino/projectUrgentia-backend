from app.models.pretriage import Pretriage
from app.extensions import db
from app.models.pregunta_ia import PreguntaIA

def invalidar_evaluacion_reglas(pretriage: Pretriage):
    """
    Invalida la evaluación inicial cuando cambian
    los datos clínicos del paciente.

    Los cambios se guardan con el commit del
    servicio que llamó a esta función.
    """

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    if pretriage.estado != "iniciado":
        raise ValueError(
            "No se puede modificar un pretriage que no está iniciado"
        )

    # No permitir modificar los datos si existe
    # una alerta de alta prioridad registrada.
    if pretriage.alerta_reglas is True:
        raise PermissionError(
            "Este pretriage tiene una alerta activa. "
            "No se permite modificar los datos clínicos "
            "para continuar con la IA."
        )
    validar_preguntas_no_iniciadas(pretriage.id)
    pretriage.reglas_evaluadas = False
    pretriage.alerta_reglas = None
    pretriage.fecha_evaluacion_reglas = None

def validar_preguntas_no_iniciadas(id_pretriage):

    pregunta_existente = (
        db.session.query(PreguntaIA.id)
        .filter(
            PreguntaIA.id_pretriage == id_pretriage
        )
        .first()
    )

    if pregunta_existente is not None:
        raise PermissionError(
            "Ya comenzó la evaluación con inteligencia artificial. "
            "No se pueden modificar los datos clínicos de este pretriage."
        )