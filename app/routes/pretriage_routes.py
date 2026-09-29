from flask import Blueprint
from app.controllers.pretriage_controller import (
    iniciar_pretriage_nn_controller
)

pretriage_bp = Blueprint("pretriage"," __name__")


@pretriage_bp.route("/pretriage", methods=["POST"])
def emergency_access():
    return iniciar_pretriage_nn_controller()