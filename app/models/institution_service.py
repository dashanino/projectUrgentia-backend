from app.extensions import db


class InstitutionService(db.Model):
    __tablename__ = "institution_services"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    institution_id = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    institution = db.relationship(
        "Institution",
        back_populates="institution_services"
    )

    service = db.relationship(
        "Service",
        back_populates="institution_services"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "institution_id",
            "service_id",
            name="uq_institution_service"
        ),
    )