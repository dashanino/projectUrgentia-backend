from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.patient import Patient
from app.extensions import db
from app.controllers.patient_antecedente_controller import (
    get_antecedentes_by_patient_controller,
    set_antecedentes_for_patient_controller,
)

patient_antecedente_bp = Blueprint('patient_antecedente', __name__)


def authorized_patient(user_id):
    if str(get_jwt_identity()) != str(user_id):
        return None
    return Patient.query.filter_by(user_id=user_id).first()


@patient_antecedente_bp.route('/patient_antecedente/<int:user_id>', methods=['GET'])
@jwt_required()
def get_antecedentes(user_id):
    if str(get_jwt_identity()) != str(user_id):
        return jsonify({'error': 'Acceso denegado'}), 403
    patient = authorized_patient(user_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    return get_antecedentes_by_patient_controller(patient.id)


@patient_antecedente_bp.route('/patient_antecedente/<int:user_id>', methods=['PUT'])
@jwt_required()
def set_antecedentes(user_id):
    if str(get_jwt_identity()) != str(user_id):
        return jsonify({'error': 'Acceso denegado'}), 403
    patient = authorized_patient(user_id)
    if not patient:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    return set_antecedentes_for_patient_controller(patient.id)