from flask import request, jsonify
from app.services.patient_antecedente_service import (
    get_antecedentes_by_patient,
    set_antecedentes_for_patient,
)


def get_antecedentes_by_patient_controller(patient_id):
    registros = get_antecedentes_by_patient(patient_id)
    return jsonify([
        {
            "id_antecedente": r.id_antecedente,
            "name": r.antecedente.name
        }
        for r in registros
    ]), 200


def set_antecedentes_for_patient_controller(patient_id):
    data = request.get_json(silent=True)

    if data is None or "antecedente_ids" not in data:
        return jsonify({
            "error": "Field 'antecedente_ids' is required (puede ser una lista vacía)"
        }), 400

    antecedente_ids = data["antecedente_ids"]

    if not isinstance(antecedente_ids, list):
        return jsonify({"error": "'antecedente_ids' must be a list"}), 400

    try:
        registros = set_antecedentes_for_patient(patient_id, antecedente_ids)
    except ValueError as e:
        status = 404 if "Patient not found" in str(e) else 400
        return jsonify({"error": str(e)}), status

    return jsonify([
        {
            "id_antecedente": r.id_antecedente,
            "name": r.antecedente.name
        }
        for r in registros
    ]), 200