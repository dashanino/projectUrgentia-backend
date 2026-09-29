from datetime import datetime, timezone
from app.extensions import db


class Pretriage(db.Model):
    __tablename__ = "pretriages"

    id = db.Column(db.Integer, primary_key=True)

    id_user = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    id_poblacion = db.Column(
        db.Integer,
        db.ForeignKey("poblaciones.id"),
        nullable=True
    )

    id_eps = db.Column(
        db.Integer,
        db.ForeignKey("eps.id"),
        nullable=True 
        )
    

    estado = db.Column(
        db.String(20),
        nullable=False,
        default="iniciado"  # iniciado, incompleto, finalizado
    )

    fecha_inicio = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    fecha_actualizacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    fecha_finalizacion = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

        # Relaciones
    user = db.relationship(
        "User",
        back_populates="pretriages"
    )

    eps = db.relationship(
        "EPS",
        back_populates="pretriages"
    )

    poblacion = db.relationship(
        "Poblacion",
        back_populates="pretriages"
    )

    respuestas = db.relationship(
        "RespuestaPretriage",
        back_populates="pretriage"
    )

    resultado = db.relationship(
        "Result",
        back_populates="pretriage",
        uselist=False
    )
    antecedentes_asociados = db.relationship(
        "PretriageAntecedente",
        back_populates="pretriage"
    )