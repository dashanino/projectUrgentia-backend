from flask import jsonify, request

from app.services.user_service import create_user_service

def create_user():

    data = request.get_json()

    user = create_user_service(
        document_type=data.get("document_type"),
        document_number=data.get("document_number"),
        first_names=data.get("first_names"),
        last_names=data.get("last_names"),
        email=data.get("email"),
        phone=data.get("phone"),
        password=data.get("password"),
        
    )

    return jsonify({
        "id": user.id,
        "email": user.email
    }), 201



def list_all():
    pass