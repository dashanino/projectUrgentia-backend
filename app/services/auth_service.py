from sqlalchemy import select
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
    
)

from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.services.user_service import create_user
from app.models.role import Role


def register_service(
    document_number,
    first_names,
    last_names,
    email,
    phone,
    password,
    birth_date,
    sex,
    id_eps
):

    # Buscar el rol patient
    patient_role = db.session.execute(
        select(Role).where(Role.name == "patient")
    ).scalar_one_or_none()

    if patient_role is None:
        raise ValueError("Patient role not configured")

    # Crear User
    user = User(
        id_role=patient_role.id,
        document_type="CC",
        document_number=document_number,
        first_names=first_names,
        last_names=last_names,
        email=email,
        phone=phone
    )

    user.set_password(password)

    db.session.add(user)

    # Flush para obtener user.id
    db.session.flush()

    # Crear Patient relacionado con ese User
    patient = Patient(
        user_id=user.id,
        id_eps=id_eps,
        birth_date=birth_date,
        sex=sex
    )

    db.session.add(patient)

    db.session.commit()

    return {
        "message": "Usuario registrado correctamente",
        "user": {
            "id": user.id,
            "document_number": user.document_number,
            "first_names": user.first_names,
            "last_names": user.last_names,
            "email": user.email
        },
        "patient": {
            "id": patient.id,
            "user_id": patient.user_id,
            "id_eps": patient.id_eps,
            "sex": patient.sex,
            "birth_date": patient.birth_date.isoformat()
                if patient.birth_date else None
            
        }
    }


def login_service(document_number,password):
    user = (
        User.query.filter_by(
            document_number=document_number
        ).first()
    )
    if not user:
        return {"message": "documento inválido"}

    if not user.check_password(password):
        return {"message": "Contraseña inválida"}

    return user
            
