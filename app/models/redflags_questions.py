from app.extensions import db


class RedFlagQuestion(db.Model):
    __tablename__ = "red_flag_questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    red_flag_id = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    question = db.Column(
        db.String(255),
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    red_flag = db.relationship(
        "RedFlag",
        backref="questions"
    )