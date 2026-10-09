from app.extensions import db


class InstitutionEPS(db.Model):
    __tablename__ = "institution_eps"

    id = db.Column(db.Integer, primary_key=True)

    institution_id = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False
    )

    eps_id = db.Column(
        db.Integer,
        db.ForeignKey("eps.id", ondelete="CASCADE"),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    institution = db.relationship(
        "Institution",
        back_populates="institution_eps"
    )

    eps = db.relationship(
        "EPS",
        back_populates="institution_eps"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "institution_id",
            "eps_id",
            name="uq_institution_eps"
        ),
    )