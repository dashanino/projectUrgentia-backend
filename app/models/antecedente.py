from datetime import datetime, timezone
from app.extensions import db


class Antecedente(db.Model):
    __tablename__ = "antecedentes"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False, unique=True)
    
    description = db.Column(db.Text, nullable=True)

    is_active = db.Column(
            db.Boolean,
            nullable=False,
            default=True
        )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    pacientes = db.relationship(
        "PacienteAntecedente",
        back_populates="antecedente"
    )