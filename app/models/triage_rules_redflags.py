from app.extensions import db


class TriageRuleRedFlag(db.Model):
    __tablename__ = "triage_rule_red_flags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    triage_rule_id = db.Column(
        db.Integer,
        db.ForeignKey("triage_rules.id"),
        nullable=False
    )

    red_flag_id = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    triage_rule = db.relationship(
        "TriageRule",
        backref="required_red_flags"
    )

    red_flag = db.relationship(
        "RedFlag",
        backref="triage_rules"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "triage_rule_id",
            "red_flag_id",
            name="uq_triage_rule_red_flag"
        ),
    )