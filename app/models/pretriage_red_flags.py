from app.extensions import db


class PreTriageRedFlag(db.Model):
    __tablename__ = "pretriage_red_flags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pretriage_id = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )

    red_flag_id = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    pretriage = db.relationship(
        "PreTriage",
        backref="selected_red_flags"
    )

    red_flag = db.relationship(
        "RedFlag",
        backref="pretriage_selections"
    )
    #porque evita, por ejemplo, que en el mismo pretriaje se guarde dos veces la misma bandera:
    __table_args__ = (
        db.UniqueConstraint(
            "pretriage_id",
            "red_flag_id",
            name="uq_pretriage_red_flag"
        ),
    )