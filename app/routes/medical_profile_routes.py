from pathlib import Path
from uuid import uuid4
from flask import current_app, send_file

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.antecedente import Antecedente
from app.models.patient_antecedente import PatientAntecedente
from app.models.medical_profile import MedicalProfile

medical_profile_bp = Blueprint('medical_profile', __name__)


def current_patient():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    patient = db.session.execute(select(Patient).where(Patient.user_id == user_id)).scalar_one_or_none()
    return user, patient


def serialize(user, patient, profile):
    antecedentes = db.session.execute(
        select(Antecedente.id, Antecedente.name)
        .join(PatientAntecedente, PatientAntecedente.id_antecedente == Antecedente.id)
        .where(PatientAntecedente.id_paciente == patient.id)
        .order_by(Antecedente.name)
    ).all()
    return {
        'first_names': user.first_names, 'last_names': user.last_names,
        'document_number': user.document_number, 'email': user.email,
        'sex': patient.sex,
        'birth_date': patient.birth_date.isoformat() if patient.birth_date else None,
        'eps': patient.eps.name if patient.eps else None,
        'antecedentes': [{'id': row.id, 'name': row.name} for row in antecedentes],
        'medications': profile.medications if profile else [],
        'allergies': profile.allergies if profile else [],
        'hospitalizations': profile.hospitalizations if profile else [],
        'surgeries': profile.surgeries if profile else [],
        'weight_kg': profile.weight_kg if profile else None,
        'height_cm': profile.height_cm if profile else None,
    }


@medical_profile_bp.get('/medical-profile/antecedentes')
@jwt_required()
def catalogo_antecedentes():
    rows = db.session.execute(select(Antecedente).where(Antecedente.is_active.is_(True)).order_by(Antecedente.name)).scalars().all()
    return jsonify([{'id': a.id, 'name': a.name} for a in rows]), 200


@medical_profile_bp.get('/medical-profile/me')
@jwt_required()
def get_medical_profile():
    user, patient = current_patient()
    if user is None or patient is None:
        return jsonify({'error': 'Perfil de paciente no encontrado'}), 404
    profile = db.session.execute(select(MedicalProfile).where(MedicalProfile.patient_id == patient.id)).scalar_one_or_none()
    return jsonify(serialize(user, patient, profile)), 200


@medical_profile_bp.put('/medical-profile/me')
@jwt_required()
def put_medical_profile():
    user, patient = current_patient()
    if user is None or patient is None:
        return jsonify({'error': 'Perfil de paciente no encontrado'}), 404
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Se requiere un objeto JSON'}), 400

    allowed_lists = ('medications', 'allergies', 'hospitalizations', 'surgeries')
    for key in allowed_lists:
        if key in data and (not isinstance(data[key], list) or len(data[key]) > 30 or
                            any(not isinstance(v, str) or not v.strip() or len(v) > 200 for v in data[key])):
            return jsonify({'error': f'{key} debe ser una lista de textos (máximo 30, 200 caracteres cada uno)'}), 400

    for key, maximum in (('weight_kg', 500), ('height_cm', 260)):
        if key in data and data[key] is not None:
            if isinstance(data[key], bool) or not isinstance(data[key], (int, float)) or not (0 < data[key] <= maximum):
                return jsonify({'error': f'{key} debe ser un número positivo válido'}), 400

    ids = data.get('antecedente_ids')
    if ids is not None:
        if not isinstance(ids, list) or len(ids) > 200 or any(type(v) is not int or v <= 0 for v in ids) or len(set(ids)) != len(ids):
            return jsonify({'error': 'antecedente_ids debe contener identificadores únicos válidos'}), 400
        valid = set(db.session.execute(select(Antecedente.id).where(Antecedente.id.in_(ids), Antecedente.is_active.is_(True))).scalars().all())
        if set(ids) != valid:
            return jsonify({'error': 'Hay antecedentes inexistentes o inactivos'}), 400

    profile = db.session.execute(select(MedicalProfile).where(MedicalProfile.patient_id == patient.id)).scalar_one_or_none()
    if profile is None:
        profile = MedicalProfile(patient_id=patient.id)
        db.session.add(profile)
    for key in allowed_lists:
        if key in data:
            setattr(profile, key, [v.strip() for v in data[key]])
    for key in ('weight_kg', 'height_cm'):
        if key in data:
            setattr(profile, key, data[key])

    if ids is not None:
        existing = db.session.execute(select(PatientAntecedente).where(PatientAntecedente.id_paciente == patient.id)).scalars().all()
        for item in existing:
            db.session.delete(item)
        db.session.flush()
        for antecedente_id in ids:
            db.session.add(PatientAntecedente(id_paciente=patient.id, id_antecedente=antecedente_id))

    db.session.commit()
    return jsonify(serialize(user, patient, profile)), 200


# Las fotos se guardan fuera de la carpeta pública y solo se consultan con JWT.
def _photo_folder():
    folder = Path(current_app.instance_path) / 'profile_photos'
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _photo_type(content):
    if content.startswith(b'\xff\xd8\xff') and content.endswith(b'\xff\xd9'):
        return 'jpg', 'image/jpeg'
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png', 'image/png'
    if content[:4] == b'RIFF' and content[8:12] == b'WEBP':
        return 'webp', 'image/webp'
    return None


@medical_profile_bp.get('/medical-profile/me/photo')
@jwt_required()
def get_profile_photo():
    user, patient = current_patient()
    if user is None or patient is None:
        return jsonify({'error': 'Perfil de paciente no encontrado'}), 404
    profile = db.session.execute(select(MedicalProfile).where(MedicalProfile.patient_id == patient.id)).scalar_one_or_none()
    if not profile or not profile.photo_filename:
        return jsonify({'error': 'Sin foto de perfil'}), 404
    path = _photo_folder() / profile.photo_filename
    if not path.is_file():
        return jsonify({'error': 'Foto no encontrada'}), 404
    mime = {'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}.get(path.suffix.lstrip('.'))
    if not mime:
        return jsonify({'error': 'Formato no admitido'}), 404
    return send_file(path, mimetype=mime, max_age=0)


@medical_profile_bp.post('/medical-profile/me/photo')
@jwt_required()
def upload_profile_photo():
    user, patient = current_patient()
    if user is None or patient is None:
        return jsonify({'error': 'Perfil de paciente no encontrado'}), 404
    photo = request.files.get('photo')
    if not photo:
        return jsonify({'error': 'Selecciona una foto'}), 400
    content = photo.stream.read(3 * 1024 * 1024 + 1)
    if not content or len(content) > 3 * 1024 * 1024:
        return jsonify({'error': 'La foto debe pesar máximo 3 MB'}), 400
    kind = _photo_type(content)
    if not kind:
        return jsonify({'error': 'Solo se aceptan imágenes JPG, PNG o WEBP'}), 400
    ext, _ = kind
    folder = _photo_folder()
    filename = f'{uuid4().hex}.{ext}'
    destination = folder / filename
    profile = db.session.execute(select(MedicalProfile).where(MedicalProfile.patient_id == patient.id)).scalar_one_or_none()
    if profile is None:
        profile = MedicalProfile(patient_id=patient.id)
        db.session.add(profile)
    previous = profile.photo_filename
    try:
        destination.write_bytes(content)
        profile.photo_filename = filename
        db.session.commit()
    except Exception:
        db.session.rollback()
        destination.unlink(missing_ok=True)
        current_app.logger.exception('Error al guardar la foto de perfil')
        return jsonify({'error': 'No se pudo guardar la foto'}), 500
    if previous:
        (folder / previous).unlink(missing_ok=True)
    return jsonify({'message': 'Foto actualizada'}), 200


@medical_profile_bp.delete('/medical-profile/me/photo')
@jwt_required()
def delete_profile_photo():
    user, patient = current_patient()

    if user is None or patient is None:
        return jsonify({'error': 'Perfil de paciente no encontrado'}), 404

    profile = db.session.execute(
        select(MedicalProfile).where(
            MedicalProfile.patient_id == patient.id
        )
    ).scalar_one_or_none()

    if profile is None or not profile.photo_filename:
        return jsonify({'message': 'No hay foto de perfil'}), 200

    previous = profile.photo_filename

    try:
        profile.photo_filename = None
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Error al eliminar foto')
        return jsonify({'error': 'No se pudo eliminar la foto'}), 500

    try:
        (_photo_folder() / previous).unlink(missing_ok=True)
    except OSError:
        current_app.logger.exception('No se pudo borrar el archivo de foto')

    return jsonify({
        'message': 'Foto eliminada correctamente',
        'photo_url': None
    }), 200
