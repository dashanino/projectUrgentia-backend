from app.extensions import db


class TriageRuleAntecedent(db.Model):
    __tablename__ = "triage_rule_antecedents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    triage_rule_id = db.Column(
        db.Integer,
        db.ForeignKey("triage_rules.id"),
        nullable=False
    )

    antecedent_id = db.Column(
        db.Integer,
        db.ForeignKey("antecedents.id"),
        nullable=False
    )

    triage_rule = db.relationship(
        "TriageRule",
        backref="required_antecedents"
    )

    antecedent = db.relationship(
        "Antecedent",
        backref="triage_rules"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "triage_rule_id",
            "antecedent_id",
            name="uq_triage_rule_antecedent"
        ),
    )