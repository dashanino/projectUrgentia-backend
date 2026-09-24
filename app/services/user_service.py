from app.extensions import db
from sqlalchemy import select, or_#select reemplaza query.filter
from werkzeug.security import generate_password_hash #crea el hash SEGURIDAD

from app.models.user import User


def create_user(
    document_type,
    document_number,
    first_names,
    last_names,
    email,
    phone,
    password
):
    # Una sola query trae cualquier usuario que choque en email, documento o teléfono
    existing_users = db.session.execute(
        select(User).where( #ASEGURA QUE SEAN UNIQUEEEEEEEEEEE
            or_(
                User.email == email,
                User.document_number == document_number,
                User.phone == phone
            )
        )
    ).scalars().all()

    # Si hay coincidencias, se determina cuál campo específico causó el conflicto
    for user in existing_users:
        if user.email == email:
            raise ValueError("Email already registered")
        if user.document_number == document_number:
            raise ValueError("Document already registered")
        if user.phone == phone:
            raise ValueError("Phone already registered")

    user = User(
        document_type=document_type,
        document_number=document_number,
        first_names=first_names,
        last_names=last_names,
        email=email,
        phone=phone,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(user_id):

    return db.session.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()


def get_user_by_email(email):

    return db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()


def update_user(
    user_id,
    first_names=None,
    last_names=None,
    email=None,
    phone=None
):
    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User not found")

    if first_names is not None:
        user.first_names = first_names

    if last_names is not None:
        user.last_names = last_names

    if email is not None:
        user.email = email

    if phone is not None:
        user.phone = phone

    db.session.commit()

    return user


def deactivate_user(user_id):

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User not found")

    user.is_active = False

    db.session.commit()

    return user

def activate_user(user_id):

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User not found")

    user.is_active = True

    db.session.commit()

    return user