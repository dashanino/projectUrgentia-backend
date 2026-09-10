from datetime import datetime, timezone

from app.extensions import db


class UserNN(db.Model):
    __tablename__ = "usersNN"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nn_code = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    
   