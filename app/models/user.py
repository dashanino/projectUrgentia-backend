from datetime import datetime, timezone

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    id_role = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=True
    )

    document_type = db.Column(
        db.String(20),
        nullable=True
    )

    document_number = db.Column(
        db.String(50),
        nullable=True,
        unique=True
    )

    first_names = db.Column(
        db.String(100),
        nullable=True
    )

    last_names = db.Column(
        db.String(100),
        nullable=True
    )

    email = db.Column(
        db.String(200),
        nullable=True,
        unique=True
    )

    phone = db.Column(
        db.String(15),
        nullable=True,
        unique=True

    )

    password_hash = db.Column(
        db.String(255),
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