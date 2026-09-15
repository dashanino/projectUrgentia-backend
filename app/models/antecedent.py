from app.extensions import db


class Antecedent(db.Model):
    __tablename__ = "antecedents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
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