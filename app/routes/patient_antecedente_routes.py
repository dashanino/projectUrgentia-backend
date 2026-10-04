from flask import Blueprint
from app.controllers.patient_antecedente_controller import get_antecedentes_by_patient_controller, set_antecedentes_for_patient_controller

patient_antecedente_bp = Blueprint('patient_antecedente', __name__)

@patient_antecedente_bp.route('/patient_antecedente/<int:user_id>', methods=['GET'])
def get_antecedentes():
    return get_antecedentes_by_patient_controller

@patient_antecedente_bp.route('/patient_antecedente/<int:user_id>', methods=['PUT'])
def set_antecedentes():
    return set_antecedentes_for_patient_controller()