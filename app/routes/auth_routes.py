from flask import Blueprint
from app.controllers.auth_controller import login_controller

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['GET'])
def login_route():
    return login_controller()


