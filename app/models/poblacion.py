from datetime import datetime, timezone
from app.extensions import db


class Poblacion(db.Model):
    __tablename__ = "poblaciones"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

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

    banderas_asociadas = db.relationship( "PoblacionRedFlag", back_populates="poblacion")
    pretriages = db.relationship( "Pretriage", back_populates="poblacion")