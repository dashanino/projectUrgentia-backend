from datetime import datetime, timezone
from app.extensions import db


class LostItem(db.Model):
    __tablename__ = "lost_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_type = db.Column(
        db.String(100),
        nullable=False
    )

    campus_location = db.Column(
        db.String(150),
        nullable=False
    )

    found_location_description = db.Column(
        db.String(250),
        nullable=False
    )

    item_description = db.Column(
        db.Text,
        nullable=False
    )

    delivered_by_name = db.Column(
        db.String(150),
        nullable=False
    )

    delivered_by_area = db.Column(
        db.String(150),
        nullable=True
    )

    photo_path = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="RECEIVED"
    )

    storage_location = db.Column(
        db.String(100),
        nullable=False
    )


    received_at = db.Column(
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
