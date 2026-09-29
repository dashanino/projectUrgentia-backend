from datetime import datetime, timezone
from app.extensions import db


class PretriageAntecedente(db.Model):
    __tablename__ = "pretriage_antecedentes"

    id = db.Column(db.Integer, primary_key=True)

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )

    id_antecedente = db.Column(
        db.Integer,
        db.ForeignKey("antecedentes.id"),
        nullable=False
    )

    fecha_registro = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    pretriage = db.relationship(
        "Pretriage",
        back_populates="antecedentes_asociados"
    )

    antecedente = db.relationship(
        "Antecedente",
        back_populates="pretriages_asociados"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_pretriage",
            "id_antecedente",
            name="uq_pretriage_antecedente"
        ),
    )