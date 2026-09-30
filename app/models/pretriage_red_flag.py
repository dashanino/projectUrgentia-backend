from datetime import datetime, timezone
from app.extensions import db


class PretriageRedFlag(db.Model):
    __tablename__ = "pretriage_red_flags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )

    id_bandera = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    pretriage = db.relationship(
        "Pretriage",
        back_populates="banderas_seleccionadas"
    )

    red_flag = db.relationship(
        "RedFlag",
        back_populates="pretriages_asociados"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "id_pretriage",
            "id_bandera",
            name="uq_pretriage_red_flag"
        ),
    )