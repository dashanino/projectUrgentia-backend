from flask import Blueprint
from app.controllers.user_controller import create_user

user_bp = Blueprint("users", __name__)


user_bp.route("/users", methods=["POST"])(create_user)


# POST /api/users
# GET /api/users