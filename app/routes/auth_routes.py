from flask import Blueprint
from app.controllers.auth_controller import login_controller, register_controller

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['GET'])
def login_route():
    return login_controller()


@auth_bp.route('/auth/register', methods=['POST'])
def register_route():
    return register_controller()

