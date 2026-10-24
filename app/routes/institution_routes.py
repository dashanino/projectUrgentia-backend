from flask import Blueprint
from app.controllers.institution_controller import instituciones_cercanas_controller


institution_bp = Blueprint('institution', __name__)
@institution_bp.route("institution/nearby", methods=["GET"])
def obtener_instituciones_cercanas():
    return instituciones_cercanas_controller()