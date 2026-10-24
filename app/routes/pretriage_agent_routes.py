from flask import Blueprint

from app.controllers.pretriage_agent_controller import PretriageAgentController


pretriage_agent_bp = Blueprint("pretriage_agent",__name__)

controller = PretriageAgentController()


@pretriage_agent_bp.route("/pretriage-agent/evaluate", methods=["POST"])
def evaluate():

    return controller.evaluate()
@pretriage_agent_bp.route("/pretriage-agent/pregunta", methods=["POST"])
def generar_pregunta():
    return controller.generar_pregunta()
@pretriage_agent_bp.route(
    "/pretriage-agent/respuesta",
    methods=["POST"]
)
def guardar_respuesta():
    return controller.guardar_respuesta()