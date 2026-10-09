from app import create_app
from app.extensions import db
from app.models.service import Service


app = create_app()

services = [
    "Psiquiatría",
    "Medicina Interna",
    "Pediatría",
    "Ortopedia",
    "Ortopedia - Módulo de Hombro",
    "Ortopedia - Módulo de Rodilla",
    "Ortopedia - Módulo de Cadera",
    "Microcirugía",
    "Cirugía Reconstructiva Ortopédica",

    "UCI Adultos",
    "Unidad de Diálisis",
    "UCE Adulto",
    "UCI Pediátrica",
    "UCI Neonatal",
    "UCE Pediátrica",

    "Cardiología",
    "UCI Cardiovascular",
    "Cirugía Vascular",
    "Cirugía Cardiovascular",
    "Terapia ECMO (Oxigenación por Membrana Extracorpórea)",
    "Terapia Endovascular (Trombectomía Mecánica)",
    "Cirugía Vascular y Angiológica",
    "Hemodinamia",
    "Cardiología Pediátrica",

    "Ginecología",
    "Ginecoobstetricia",
    "Neonatología",

    "Fibrobroncoscopia",
    "Neumología",
    "Cirugía de Tórax",

    "Neurología",
    "Neuropediatría",
    "Neurocirugía",
    "Neurointervencionismo",

    "Cirugía General",
    "Cirugía Hepatobiliar",
    "Hepatología",
    "Gastroenterología",
    "CPRE (Colangiografía Retrógrada Endoscópica)",
    "Coloproctología",

    "Cirugía Pediátrica",

    "Cirugía Plástica",
    "Maxilofacial",
    "Cirugía de Cabeza y Cuello",

    "Oftalmología",
    "Hematología",
    "Hematooncología",
    "Oncología",
    "Cirugía Oncológica",
    "Ginecología Oncológica",
    "Ortopedia Oncológica",

    "Nefrología Pediátrica",

    "Urología",
    "Toxicología",
    "Infectología",
    "Dolor Paliativo",

    "Radiología Intervencionista",
    "Medicina Nuclear",
]


with app.app_context():

    for item in services:

        service = Service.query.filter_by(
            name=item
        ).first()

        if service:
            continue

        db.session.add(
            Service(
                name=item,
                is_active=True
            )
        )

    db.session.commit()

    print("Services seeded successfully.")