from datetime import datetime, timezone
from app.extensions import db


class TriageRule(db.Model):
    __tablename__ = "triage_rules"

    id = db.Column(db.Integer, primary_key=True)

    id_poblacion = db.Column(
        db.Integer,
        db.ForeignKey("poblaciones.id"),
        nullable=False
    )

    id_bandera = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    alta_prioridad = db.Column(
        db.Boolean,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    antecedentes = db.relationship(
        "TriageRuleAntecedente",
        back_populates="triage_rule",
        cascade="all, delete-orphan"
    )