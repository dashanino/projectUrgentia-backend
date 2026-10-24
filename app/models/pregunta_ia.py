
from datetime import datetime, timezone
from app.extensions import db


class PreguntaIA(db.Model):
    __tablename__ = "preguntas_ia"

    id = db.Column(db.Integer, primary_key=True)

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False,
        index=True
    )

    pregunta = db.Column(db.Text, nullable=False)

    respuesta = db.Column(db.Text, nullable=True)

    orden = db.Column(db.Integer, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    answered_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_pretriage",
            "orden",
            name="uq_preguntas_ia_pretriage_orden"
        ),
    )