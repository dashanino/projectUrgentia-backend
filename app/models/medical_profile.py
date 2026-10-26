from datetime import datetime, timezone
from app.extensions import db


class MedicalProfile(db.Model):
    __tablename__ = 'medical_profiles'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, unique=True)
    medications = db.Column(db.JSON, nullable=False, default=list)
    allergies = db.Column(db.JSON, nullable=False, default=list)
    hospitalizations = db.Column(db.JSON, nullable=False, default=list)
    surgeries = db.Column(db.JSON, nullable=False, default=list)
    photo_filename = db.Column(db.String(80), nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
