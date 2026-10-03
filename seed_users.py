from getpass import getpass

from sqlalchemy import func, or_
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User


# Datos de ejemplo: reemplazar antes de ejecutar.
# Roles disponibles: admin, patient, doctor, usernn.
USERS = [
    {
        'document_type': 'CC',
        'document_number': '1111',
        'first_names': 'Administrador',
        'last_names': 'Ejemplo',
        'email': 'admin@urgentia.com',
        'phone': '3000000001',
        'role': 'admin',
        'is_active': True,
    },
    {
        'document_type': 'CC',
        'document_number': '2222',
        'first_names': 'Paciente',
        'last_names': 'Ejemplo',
        'email': 'patient@urgentia.com',
        'phone': '3000000003',
        'role': 'patient',
        'is_active': True,
    },
    {
        'role': 'usernn',
        'is_active': True,
    },
    {
        'document_type': 'CC',
        'document_number': '3333',
        'first_names': 'Doctor',
        'last_names': 'Ejemplo',
        'email': 'doctor@urgentia.com',
        'phone': '3000000002',
        'role': 'doctor',
        'is_active': True,
    },
]


def seed_users():
    app = create_app()

    with app.app_context():
        created = 0
        skipped = 0

        try:
            for item in USERS:
                role_name = item.get('role')
                is_active = item.get('is_active', True)

                if not isinstance(is_active, bool):
                    raise ValueError(f"is_active debe ser True o False para el rol '{role_name}'.")

                role = db.session.execute(
                    db.select(Role).where(Role.name == role_name)
                ).scalar_one_or_none()

                if role is None:
                    raise ValueError(
                        f"El rol '{role_name}' no existe. Ejecuta el seed de roles primero."
                    )
                if not role.is_active:
                    raise ValueError(f"El rol '{role_name}' está inactivo.")

                # --- Caso especial: usuario NN, sin datos personales ---
                if role_name == 'usernn':
                    user = User(
                        id_role=role.id,
                        is_active=is_active,
                    )
                    db.session.add(user)
                    db.session.flush()
                    created += 1
                    print("Usuario NN creado.")
                    continue

                # --- Resto de roles (admin, patient, doctor): requieren datos completos ---
                values = {}
                for field in ('document_type', 'document_number', 'first_names', 'last_names', 'email', 'phone'):
                    value = item.get(field)
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f"El campo '{field}' es obligatorio y debe ser texto para el rol '{role_name}'.")
                    values[field] = value.strip()
                    if len(values[field]) > 150:
                        raise ValueError(f"El campo '{field}' excede el límite de caracteres.")

                email = values['email'].lower()
                document_number = values['document_number']
                phone = values['phone']

                existing = db.session.execute(
                    db.select(User).where(
                        or_(
                            User.document_number == document_number,
                            User.phone == phone,
                            func.lower(User.email) == email,
                        )
                    )
                ).scalar_one_or_none()

                if existing:
                    print(f"Omitido: {email}; documento, teléfono o correo ya registrado.")
                    skipped += 1
                    continue

                password = item.get('password')
                if password is None:
                    password = getpass(f"Contraseña para {email}: ")
                    confirmation = getpass('Confirma la contraseña: ')
                    if password != confirmation:
                        raise ValueError(f"Las contraseñas no coinciden para {email}.")
                if not isinstance(password, str) or not password.strip():
                    raise ValueError(f"La contraseña no puede estar vacía para {email}.")

                user = User(
                    document_type=values['document_type'],
                    document_number=document_number,
                    first_names=values['first_names'],
                    last_names=values['last_names'],
                    email=email,
                    phone=phone,
                    id_role=role.id,
                    is_active=is_active,
                    password_hash=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.flush()
                created += 1

            db.session.commit()
            print(f"Proceso finalizado. Creados: {created}. Omitidos: {skipped}.")
        except Exception:
            db.session.rollback()
            print('Proceso cancelado: no se guardaron nuevos usuarios en esta ejecución.')
            raise


if __name__ == '__main__':
    seed_users()