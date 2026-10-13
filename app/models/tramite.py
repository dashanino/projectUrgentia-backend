
from app.extensions import db


class Tramite(db.Model):
    __tablename__ = "tramites"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    eps_tramites = db.relationship(
        "EPSTramite",
        back_populates="tramite"
    )
