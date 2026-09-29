from datetime import datetime, timezone
from app.extensions import db


class RedFlag(db.Model):
    __tablename__ = "red_flags"

    id = db.Column(db.Integer, primary_key=True)

    id_poblacion = db.Column(
        db.Integer,
        db.ForeignKey("poblaciones.id"),
        nullable=False
    )

    name = db.Column(db.String(150), nullable=False)
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

    poblacion = db.relationship("Poblacion", back_populates="red_flags")
    submenu = db.relationship("SubmenuRedFlag", back_populates="red_flag")