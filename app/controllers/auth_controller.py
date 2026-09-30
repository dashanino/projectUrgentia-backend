from flask import request, jsonify
from app.services.auth_service import login


def login_controller():
    data = request.get_json(silent=True)

    if not data or not data.get("document_number") or not data.get("password"):
        return jsonify({"error": "document number and password are required"}), 400

    try:
         user = login(data["document_number"], data["password"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    return jsonify({
        
        "user": {
            "id": user.id,
            "document_number": user.document_number,
            "first_names": user.first_names,
        }
    }), 200