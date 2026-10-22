
from app.extensions import db
from datetime import datetime, timezone


class Sintoma(db.Model):
    __tablename__ = "sintomas"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    id_bandera = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)

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

