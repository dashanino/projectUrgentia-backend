from flask import Blueprint

from app.controllers.pretriage_agent_controller import PretriageAgentController


pretriage_agent_bp = Blueprint("pretriage_agent",__name__)

controller = PretriageAgentController()


@pretriage_agent_bp.route("/pretriage-agent/evaluate", methods=["POST"])
def evaluate():

    return controller.evaluate()