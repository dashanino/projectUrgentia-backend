from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.pretriage_agent_controller import (
    PretriageAgentController
)
from app.controllers.bulk_pretriage_controller import BulkPretriageController


pretriage_agent_bp = Blueprint(
    "pretriage_agent",
    __name__
)

controller = PretriageAgentController()
bulk_controller = BulkPretriageController()


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


# 5. Evaluación de un relato libre para administrador
@pretriage_agent_bp.route(
    "/pretriage-agent/admin/evaluate-free-text",
    methods=["POST"]
)
@jwt_required()
def evaluate_admin_free_text():
    return controller.evaluate_admin_free_text()


# 6. Iniciar evaluación masiva de casos desde Excel para administrador
@pretriage_agent_bp.route(
    "/pretriage-agent/admin/evaluate-excel",
    methods=["POST"]
)
@jwt_required()
def evaluate_admin_excel():
    return bulk_controller.evaluate_excel()


# 7. Consultar avance de una evaluación masiva
@pretriage_agent_bp.route(
    "/pretriage-agent/admin/evaluate-excel/<job_id>/progress",
    methods=["GET"]
)
@jwt_required()
def evaluate_admin_excel_progress(job_id):
    return bulk_controller.get_progress(job_id)


# 8. Descargar el Excel cuando termine la evaluación masiva
@pretriage_agent_bp.route(
    "/pretriage-agent/admin/evaluate-excel/<job_id>/result",
    methods=["GET"]
)
@jwt_required()
def evaluate_admin_excel_result(job_id):
    return bulk_controller.download_result(job_id)
