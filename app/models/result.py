from datetime import datetime, timezone
from app.extensions import db


class Result(db.Model):
    __tablename__ = "resultados"

    id = db.Column(db.Integer, primary_key=True)

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False,
        unique=True
    )

    nivel_triage = db.Column(
        db.String(20),
        nullable=False
    )

    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=True
    )

    id_institucion_recomendada = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id"),
        nullable=True
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    recomendacion = db.Column(
        db.Text,
        nullable=True
    )

    fecha_resultado = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    pretriage = db.relationship(
        "Pretriage",
        back_populates="resultado"
    )

    servicio = db.relationship(
        "Service"
    )

    institucion_recomendada = db.relationship(
        "Institution"
    )