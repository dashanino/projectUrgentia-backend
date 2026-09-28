from datetime import datetime, timezone
from app.extensions import db


class PatientAntecedente(db.Model):
    __tablename__ = "patient_antecedentes"

    id = db.Column(db.Integer, primary_key=True)

    id_paciente = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    id_antecedente = db.Column(
        db.Integer,
        db.ForeignKey("antecedentes.id"),
        nullable=False
    )

    fecha_registro = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    paciente = db.relationship("Patient", backref="antecedentes_asociados")
    antecedente = db.relationship("Antecedente", back_populates="pacientes")

    __table_args__ = (
        db.UniqueConstraint("id_paciente", "id_antecedente", name="uq_paciente_antecedente"),
    )