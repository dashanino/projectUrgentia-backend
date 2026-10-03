from flask import request, jsonify
from app.services.auth_service import login_service, register_service


def register_controller():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "document_type",
        "document_number",
        "first_names",
        "last_names",
        "email",
        "phone",
        "password",
    ]
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    try:
        user = register_service(
            document_type=data["document_type"],
            document_number=data["document_number"],
            first_names=data["first_names"],
            last_names=data["last_names"],
            email=data["email"],
            phone=data["phone"],
            password=data["password"],
        )
    except ValueError as e:
        status = 500 if "not configured" in str(e) else 409
        return jsonify({"error": str(e)}), status

    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_names": user.first_names,
        "last_names": user.last_names,
    }), 201 

def login_controller():
    data = request.get_json(silent=True)

    if not data or not data.get("document_number") or not data.get("password"):
        return jsonify({"error": "document number and password are required"}), 400

    try:
         user = login_service(data["document_number"], data["password"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    return jsonify({
        
        "user": {
            "id": user.id,
            "document_number": user.document_number,
            "first_names": user.first_names,
        }
    }), 200