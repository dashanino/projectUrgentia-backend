from app.extensions import db


class PreTriageAntecedent(db.Model):
    __tablename__ = "pretriage_antecedents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pretriage_id = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )

    antecedent_id = db.Column(
        db.Integer,
        db.ForeignKey("antecedents.id"),
        nullable=False
    )

    pretriage = db.relationship(
        "PreTriage",
        backref="selected_antecedents"
    )

    antecedent = db.relationship(
        "Antecedent",
        backref="pretriage_selections"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "pretriage_id",
            "antecedent_id",
            name="uq_pretriage_antecedent"
        ),
    )