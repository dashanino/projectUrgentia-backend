from app.extensions import db


class Institution(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    level = db.Column(
        db.Integer,
        nullable=True
    )

    municipality = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.String(250),
        nullable=True
    )

    latitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    longitude = db.Column(
        db.Numeric(10, 7),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    institution_services = db.relationship(
        "InstitutionService",
        back_populates="institution",
        cascade="all, delete-orphan"
    )

    institution_eps = db.relationship(
        "InstitutionEPS",
        back_populates="institution",
        cascade="all, delete-orphan"
    )