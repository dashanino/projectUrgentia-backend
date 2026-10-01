from flask import Blueprint
from app.controllers.poblacion_controller import create_poblacion_controller, get_all_poblaciones_controller

poblacion_bp = Blueprint('poblacion', __name__)

poblacion_bp.route('/poblacion/generate', methods=['POST'])
def create_poblacion_route():
    return create_poblacion_controller()

poblacion_bp.route('/poblacion/get_all', methods=['GET'])
def get_all_poblaciones_route():
    return get_all_poblaciones_controller()
