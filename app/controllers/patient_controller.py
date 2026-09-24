from flask import request, jsonify
from datetime import datetime
from app.services.patient_service import (
    create_patient,
    get_patient_by_id,
    get_patient_by_user_id,
    update_patient,
)


def create_patient_controller():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if not data.get("user_id"):
        return jsonify({"error": "Field 'user_id' is required"}), 400

    try:
        patient = create_patient(
            user_id=data["user_id"],
            id_eps=data.get("id_eps"),
            birth_date=data.get("birth_date"),
            sex=data.get("sex"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify(patient_to_dict(patient)), 201


def get_patient_controller(patient_id):
    patient = get_patient_by_id(patient_id)

    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient_to_dict(patient)), 200


def get_patient_by_user_controller(user_id):
    patient = get_patient_by_user_id(user_id)

    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient_to_dict(patient)), 200


def update_patient_controller(patient_id):
    
    data = request.get_json(silent=True)
    

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        birth_date_str = data.get("birth_date")
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date() if birth_date_str else None
        patient = update_patient(
            patient_id=patient_id,
            id_eps=data.get("id_eps"),
            birth_date=data.get("birth_date"),
            sex=data.get("sex"),
        )
    except ValueError as e:
        status = 404 if "not found" in str(e).lower() and "EPS" not in str(e) else 400
        return jsonify({"error": str(e)}), status
    

    return jsonify(patient_to_dict(patient)), 200


def patient_to_dict(patient):
    return {
        "id": patient.id,
        "user_id": patient.user_id,
        "id_eps": patient.id_eps,
        "birth_date": patient.birth_date.isoformat() if patient.birth_date else None,
        "sex": patient.sex,
    }