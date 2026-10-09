from app.extensions import db


class Service(db.Model):
    __tablename__ = "services"

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

    institution_services = db.relationship(
        "InstitutionService",
        back_populates="service",
        cascade="all, delete-orphan"
    )