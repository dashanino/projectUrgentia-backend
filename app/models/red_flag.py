from datetime import datetime, timezone
from app.extensions import db


class RedFlag(db.Model):
    __tablename__ = "red_flags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

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

    
    submenu = db.relationship("SubmenuRedFlag", back_populates="red_flag")
    poblaciones_asociadas = db.relationship("PoblacionRedFlag", back_populates="red_flag")
    pretriages_asociados = db.relationship("PretriageRedFlag", back_populates="red_flag")

