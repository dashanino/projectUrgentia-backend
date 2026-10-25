from app import create_app
from app.extensions import db
from app.models.emergency_attention import EmergencyAttention
 
 
app = create_app()
 
 
Emergency_attention = [
    {'name': 'Urgencias Generales' },
    {'name': 'Urgencias Pedriátricas' },
    {'name': 'Urgencias Ginecoobstétricas' },
    {'name': 'Urgencias de Trauma' },
    {'name': 'Urgencias Neurológicas' },
    {'name': 'Urgencias Cardiovasculares' },
]
 
 
with app.app_context():
    for item in Emergency_attention:
        eps = EmergencyAttention.query.filter_by(
            name=item['name']
        ).first()
 
        if eps:
            continue
 
        db.session.add(
            EmergencyAttention(
                name=item['name'],
                is_active=True
            )
        )
 
    db.session.commit()
