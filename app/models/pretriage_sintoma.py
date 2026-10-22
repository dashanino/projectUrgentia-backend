from app.extensions import db
from datetime import datetime, timezone


class PretriageSintoma(db.Model):
    __tablename__ = "pretriage_sintomas"

    id = db.Column(
            db.Integer,
            primary_key = True
        )

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )
    id_sintoma = db.Column(
        db.Integer,
        db.ForeignKey("sintomas.id"),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )