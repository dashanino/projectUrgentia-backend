from flask import Blueprint
from app.controllers.patient_controller import (
    create_patient_controller,
    get_patient_controller,
    get_patient_by_user_controller,
    update_patient_controller,
)

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patients', methods=['POST'])
def create_patient_route():
    return create_patient_controller()


@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient_route(patient_id):
    return get_patient_controller(patient_id)


@patient_bp.route('/patients/user/<int:user_id>', methods=['GET'])
def get_patient_by_user_route(user_id):
    return get_patient_by_user_controller(user_id)


@patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient_route(patient_id):
    return update_patient_controller(patient_id)