from app import create_app
from app.extensions import db
from app.models.role import Role
 
 
app = create_app()
 
 
ROLES = [
    {'name': 'admin', 'description': 'Administrador.'},
    {'name': 'teacher', 'description': 'Docente.'},
    {'name': 'student', 'description': 'Estudiante.'},
    {'name': 'doctor', 'description': 'Doctor.'}
]
 
 
with app.app_context():
    for item in ROLES:
        role = Role.query.filter_by(
            name=item['name']
        ).first()
 
        if role:
            continue
 
        db.session.add(
            Role(
                name=item['name'],
                description=item['description'],
                is_active=True
            )
        )
 
    db.session.commit()
