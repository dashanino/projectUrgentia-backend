from flask import Blueprint
from app.controllers.sintoma_controller import sintoma_redflag_controller

sintoma_bp = Blueprint('sintoma', __name__)


@sintoma_bp.route('sintomas/<int:id_bandera>', methods=['GET'])
def obtener_sintomas_por_red_flag(id_bandera):
    return sintoma_redflag_controller(id_bandera)
