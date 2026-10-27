from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.pretriage_agent_controller import (
    PretriageAgentController
)


pretriage_agent_bp = Blueprint(
    "pretriage_agent",
    __name__
)

controller = PretriageAgentController()


# 1. Evaluar el pre-triage mediante IA
@pretriage_agent_bp.route(
    "/pretriage-agent/evaluate",
    methods=["POST"]
)
@jwt_required()
def evaluate():
    return controller.evaluate()


# 2. Generar preguntas mediante IA
@pretriage_agent_bp.route(
    "/pretriage-agent/pregunta",
    methods=["POST"]
)
@jwt_required()
def generar_pregunta():
    return controller.generar_pregunta()


# 3. Guardar las respuestas del paciente
@pretriage_agent_bp.route(
    "/pretriage-agent/respuesta",
    methods=["POST"]
)
@jwt_required()
def guardar_respuesta():
    return controller.guardar_respuesta()

@pretriage_agent_bp.route(
    "/pretriage-agent/respuestas",
    methods=["POST"]
)
@jwt_required()
def guardar_respuestas():
    return controller.guardar_respuestas()


# 4. Clasificar el tipo de atención
@pretriage_agent_bp.route(
    "/pretriage-agent/tipo-atencion",
    methods=["POST"]
)
@jwt_required()
def clasificar_tipo_atencion():
    return controller.clasificar_tipo_atencion()