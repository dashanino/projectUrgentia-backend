from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import login_service, register_service


def register_controller():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "document_number",
        "first_names",
        "last_names",
        "email",
        "phone",
        "password",
        "birth_date",
        "sex",
        "id_eps",
    ]

    missing = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing:
        print("FALTAN:", missing)
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    try:
        result = register_service(
            document_number=data["document_number"],
            first_names=data["first_names"],
            last_names=data["last_names"],
            email=data["email"],
            phone=data["phone"],
            password=data["password"],
            birth_date=data["birth_date"],
            sex=data["sex"],
            id_eps=data["id_eps"],
        )

    

    except ValueError as e:
        status = 500 if "not configured" in str(e) else 409

        return jsonify({
            "error": str(e)
        }), status

    return jsonify(result), 201

def login_controller():
    data = request.get_json(silent=True)
    print("DATA RECIBIDA:", data)

    if not data or not data.get("document_number") or not data.get("password"):
        return jsonify({"error": "document number and password are required"}), 400

    try:
        user = login_service(
            data["document_number"],
            data["password"]
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    access_token = create_access_token(
    identity=str(user.id)
)

    return jsonify({
        "message": "Login exitoso",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "document_number": user.document_number,
            "first_names": user.first_names,
            "last_names": user.last_names,
            "email": user.email,
            "id_role": user.id_role
        }
    }), 200