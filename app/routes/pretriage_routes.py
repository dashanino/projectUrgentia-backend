from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.pretriage_controller import (
    iniciar_pretriage_nn_controller,
    guardar_antecedentes_nn_controller,
    guardar_poblacion_nn_controller,
    obtener_banderas_rojas_controller,
    guardar_banderas_rojas_nn_controller
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
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/poblacion",
    methods=["POST"]
)
def guardar_poblacion(id_pretriage):
    return guardar_poblacion_nn_controller(id_pretriage)
# Consultar las banderas rojas de la población seleccionada
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/banderas-rojas",
    methods=["GET"]
)
def consultar_banderas_rojas(id_pretriage):
    return obtener_banderas_rojas_controller(id_pretriage)
# Guardar las banderas rojas seleccionadas
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/banderas-rojas",
    methods=["POST"]
)
def guardar_banderas_rojas(id_pretriage):
    return guardar_banderas_rojas_nn_controller(id_pretriage)