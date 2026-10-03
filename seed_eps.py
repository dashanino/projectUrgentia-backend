from app import create_app
from app.extensions import db
from app.models.eps import EPS
 
 
app = create_app()
 
 
Eps = [
    {'name': 'SURA' },
    {'name': 'Sanitas'},
    {'name': 'Nueva EPS'},
    {'name': 'Salud Total'},
    {'name': 'Coosalud'},
    {'name': 'Emssanar'},
    {'name': 'Compensar'},
    {'name': 'Famisanar'}
]
 
 
with app.app_context():
    for item in Eps:
        eps = EPS.query.filter_by(
            name=item['name']
        ).first()
 
        if eps:
            continue
 
        db.session.add(
            EPS(
                name=item['name'],
                is_active=True
            )
        )
 
    db.session.commit()
