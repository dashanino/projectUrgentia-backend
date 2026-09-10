from sqlalchemy import select
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db
from app.models.user import User


def register_user(full_name, email, password, identification):
    existing_user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_user:
        raise ValueError("Email already registered")

    existing_user = db.session.execute(
            select(User).where(User.identification == identification)
        ).scalar_one_or_none()
    
    if existing_user:
        raise ValueError("Identification already registered")

    user = User(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password),
        identification = identification
    )

    db.session.add(user)
    db.session.commit()

    return user


def validate_credentials(email, password):
    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return None

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return None

    if not user.is_active:
        return None
