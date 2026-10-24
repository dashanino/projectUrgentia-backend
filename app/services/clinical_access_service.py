from flask_jwt_extended import get_jwt, get_jwt_identity

from app.extensions import db
from app.models.user import User


def validar_acceso_clinico():
    claims = get_jwt()

    # Un token de emergencia no permite realizar
    # operaciones reservadas a profesionales.
    if claims.get("tipo_acceso") == "emergencia":
        raise PermissionError(
            "El acceso de emergencia no permite revisión clínica"
        )

    try:
        id_user = int(get_jwt_identity())
    except (TypeError, ValueError):
        raise PermissionError(
            "El token no contiene una identidad válida"
        )

    usuario = db.session.get(User, id_user)

    if usuario is None or not usuario.is_active:
        raise PermissionError(
            "El usuario no existe o está inactivo"
        )

    if (
        usuario.role is None
        or not usuario.role.is_active
        or usuario.role.name != "doctor"
    ):
        raise PermissionError(
            "No tienes autorización para realizar revisiones clínicas"
        )

    return usuario