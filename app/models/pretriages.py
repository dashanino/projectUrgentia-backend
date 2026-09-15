from datetime import datetime, timezone
from app.extensions import db


class PreTriage(db.Model):
    __tablename__ = "pretriages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=True
    )

    user_nn_id = db.Column(
        db.Integer,
        db.ForeignKey("usersNN.id"),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="started"
    )

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    population_id = db.Column(
        db.Integer,
        db.ForeignKey("populations.id"),
        nullable=True
    )
    population = db.relationship(
        "Population",
        backref="pretriages"
    )

    patient = db.relationship(
        "Patient",
        backref="pretriages"
    )

    user_nn = db.relationship(
        "UserNN",
        backref="pretriages"
    )
    #proteger directamente en PostgreSQL/SQLAlchemy con una restricción:
    #Paciente registrado: patient_id ≠ NULL/ user_nn_id = NULL O Paciente NN: patient_id = NULL user_nn_id ≠ NULL
    __table_args__ = (
        db.CheckConstraint(
            """
            (patient_id IS NOT NULL AND user_nn_id IS NULL)
            OR
            (patient_id IS NULL AND user_nn_id IS NOT NULL)
            """,
            name="check_pretriage_owner"
        ),
    )