from flask import Blueprint
from app.controllers.role_controller import create_role_controller, get_all_roles_controller

role_bp = Blueprint('role', __name__)

role_bp.route('/role/generate', methods=['POST'])
def create_role_route():
    return create_role_controller()

role_bp.route('/role/get_all', methods=['GET'])
def get_all_roles_route():
    return get_all_roles_controller()


