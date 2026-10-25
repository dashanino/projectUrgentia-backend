from app.extensions import db


class EmergencyAttention(db.Model):
    __tablename__ = "emergency_attentions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    institution_emergency_attentions = db.relationship(
        "InstitutionEmergencyAttention",
        back_populates="emergency_attention",
        cascade="all, delete-orphan"
    )