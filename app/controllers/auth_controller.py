from flask import jsonify, request

from app.services.auth_service import (
    register_user,
    validate_credentials,
)


def register():
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    identification = data.get("identification")

    if not full_name or not email or not password or not identification:
        return jsonify({
            "message": "full_name, email, password and identification are required"
        }), 400

    try:
        user = register_user(
            full_name=full_name,
            email=email,
            password=password,
            identification=identification
        )

        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "identification": user.identification
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 409


def login_without_token():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "email and password are required"
        }), 400

    user = validate_credentials(
        email=email,
        password=password
    )

    if user is None:
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        }
    }), 200
