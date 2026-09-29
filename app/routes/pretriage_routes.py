from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers.pretriage_controller import (
    iniciar_pretriage_nn_controller,
    guardar_antecedentes_nn_controller
)

pretriage_bp = Blueprint("pretriage", __name__)


# Iniciar el acceso de emergencias
@pretriage_bp.route("/pretriage", methods=["POST"])
def emergency_access():
    return iniciar_pretriage_nn_controller()


# Guardar los antecedentes del usuario NN
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/antecedentes",
    methods=["POST"]
)
@jwt_required()
def save_emergency_antecedents(id_pretriage):
    return guardar_antecedentes_nn_controller(id_pretriage)