from app.extensions import db


class TriageRuleAntecedente(db.Model):
    __tablename__ = "triage_rule_antecedentes"

    id = db.Column(db.Integer, primary_key=True)

    id_regla = db.Column(
        db.Integer,
        db.ForeignKey("triage_rules.id", ondelete="CASCADE"),
        nullable=False
    )

    id_antecedente = db.Column(
        db.Integer,
        db.ForeignKey("antecedentes.id"),
        nullable=False
    )

    triage_rule = db.relationship(
        "TriageRule",
        back_populates="antecedentes"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_regla",
            "id_antecedente",
            name="uq_triage_rule_antecedente"
        ),
    )