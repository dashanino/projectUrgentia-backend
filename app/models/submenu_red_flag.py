from datetime import datetime, timezone
from app.extensions import db


class SubmenuRedFlag(db.Model):
    __tablename__ = "submenu_red_flags"

    id = db.Column(db.Integer, primary_key=True)

    id_bandera = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    pregunta = db.Column(db.Text, nullable=False)
    tipo_respuesta = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Integer, nullable=False, default=0)
    nivel_riesgo = db.Column(db.String(20), nullable=True)  # bajo, medio, alto
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

    red_flag = db.relationship("RedFlag", back_populates="submenu")
    respuestas = db.relationship("RespuestaPretriage", back_populates="submenu")