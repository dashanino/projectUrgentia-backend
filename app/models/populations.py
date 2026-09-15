from app.extensions import db

class Population(db.Model):
    __tablename__ = "populations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
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