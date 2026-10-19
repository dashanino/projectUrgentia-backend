
from datetime import datetime, timezone
from app.extensions import db


class EPSTramite(db.Model):
    __tablename__ = "eps_tramites"

    id = db.Column(db.Integer, primary_key=True)

    eps_id = db.Column(
        db.Integer,
        db.ForeignKey("eps.id"),
        nullable=False
    )

    tramite_id = db.Column(
        db.Integer,
        db.ForeignKey("tramites.id"),
        nullable=False
    )

    requisitos = db.Column(
        db.JSON,
        nullable=True
    )

    pasos = db.Column(
        db.JSON,
        nullable=True
    )

    url_oficial = db.Column(
        db.Text,
        nullable=True
    )

    fecha_verificacion = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    eps = db.relationship("EPS")

    tramite = db.relationship(
        "Tramite",
        back_populates="eps_tramites"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "eps_id",
            "tramite_id",
            name="uq_eps_tramite"
        ),
    )
