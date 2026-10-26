from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.sintoma_controller import sintoma_redflag_controller
from app.controllers.pretriage_sintoma_controller import (
    guardar_sintomas_pretriage_controller
)

sintoma_bp = Blueprint("sintoma", __name__)


# Consultar síntomas asociados a una bandera roja
@sintoma_bp.route(
    "/sintomas/<int:id_bandera>",
    methods=["GET"]
)
def obtener_sintomas_por_red_flag(id_bandera):
    return sintoma_redflag_controller(id_bandera)


# Guardar síntomas seleccionados por el paciente
@sintoma_bp.route(
    "/pretriage/<int:id_pretriage>/sintomas",
    methods=["POST"]
)
@jwt_required()
def guardar_sintomas(id_pretriage):
    return guardar_sintomas_pretriage_controller(id_pretriage)