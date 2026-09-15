from app.extensions import db


class TriageRule(db.Model):
    __tablename__ = "triage_rules"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    population_id = db.Column(
        db.Integer,
        db.ForeignKey("populations.id"),
        nullable=False
    )

    high_priority = db.Column(
        db.Boolean,
        nullable=False
    )

    population = db.relationship(
        "Population",
        backref="triage_rules"
    )