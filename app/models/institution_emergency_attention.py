from app.extensions import db


class InstitutionEmergencyAttention(db.Model):
    __tablename__ = "institution_emergency_attentions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    institution_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "institutions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    emergency_attention_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "emergency_attentions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    institution = db.relationship(
        "Institution",
        back_populates="institution_emergency_attentions"
    )

    emergency_attention = db.relationship(
        "EmergencyAttention",
        back_populates="institution_emergency_attentions"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "institution_id",
            "emergency_attention_id",
            name="uq_institution_emergency_attention"
        ),
    )