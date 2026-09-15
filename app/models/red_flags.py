from app.extensions import db


class RedFlag(db.Model):
    __tablename__ = "red_flags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    population_id = db.Column(
        db.Integer,
        db.ForeignKey("populations.id"),
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    population = db.relationship(
        "Population",
        backref="red_flags"
    )