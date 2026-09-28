from datetime import datetime, timezone
from app.extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    id_eps = db.Column(
        db.Integer,
        db.ForeignKey("eps.id"),
        nullable=True
    )

    birth_date = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(20), nullable=True)

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

    # Relaciones
    user = db.relationship("User", back_populates="patient")
    eps = db.relationship("EPS", back_populates="patients")

    antecedentes_asociados = db.relationship(
        "PacienteAntecedente",
        back_populates="paciente"
    )

    # cirugias = db.relationship("Cirugia", back_populates="paciente")
    # medicamentos = db.relationship("Medicamento", back_populates="paciente")
    # alergias = db.relationship("Alergia", back_populates="paciente")
    # hospitalizaciones = db.relationship("Hospitalizacion", back_populates="paciente")
    # habitos = db.relationship("Habito", back_populates="paciente", uselist=False)