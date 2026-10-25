from app import create_app
from app.extensions import db
from app.models.institution import Institution
from app.models.emergency_attention import EmergencyAttention
from app.models.institution_emergency_attention import InstitutionEmergencyAttention

def seed_institution_emergency_attentions():

    general = EmergencyAttention.query.filter_by(
    name="Urgencias Generales"
    ).first()

    pediatrica = EmergencyAttention.query.filter_by(
    name="Urgencias Pediátricas"
    ).first()

    ginecoobstetrica = EmergencyAttention.query.filter_by(
    name="Urgencias Ginecoobstétricas"
    ).first()

    trauma = EmergencyAttention.query.filter_by(
    name="Urgencias de Trauma"
    ).first()

    neurologica = EmergencyAttention.query.filter_by(
    name="Urgencias Neurológicas"
    ).first()

    cardiovascular = EmergencyAttention.query.filter_by(
    name="Urgencias Cardiovasculares"
    ).first()

    categorias = {
        "Urgencias Generales": general,
        "Urgencias Pediátricas": pediatrica,
        "Urgencias Ginecoobstétricas": ginecoobstetrica,
        "Urgencias de Trauma": trauma,
        "Urgencias Neurológicas": neurologica,
        "Urgencias Cardiovasculares": cardiovascular,
    }

    categorias_faltantes = [nombre for nombre, obj in categorias.items() if obj is None]
    if categorias_faltantes:
        raise ValueError(
            "Faltan categorías en emergency_attentions: "
            + ", ".join(categorias_faltantes)
        )

    # Estas relaciones describen capacidades declaradas para el prototipo.
    # Deben confirmarse con la institución/especialista antes de usarlas
    # para orientar pacientes reales.
    relaciones = {
        "Hospital General de Medellín Luz Castro de Gutiérrez ESE": [
            general, pediatrica, ginecoobstetrica,
            trauma, neurologica, cardiovascular,
        ],
        "Hospital Pablo Tobón Uribe": [
            general, pediatrica, ginecoobstetrica,
            trauma, neurologica, cardiovascular,
        ],
        "Fundación Hospitalaria San Vicente de Paúl": [
            general, pediatrica, trauma, neurologica, cardiovascular,
        ],
        "Hospital Alma Máter de Antioquia": [
            general, trauma, neurologica, cardiovascular,
        ],
        "ESE Hospital La María": [
            general, trauma,
        ],
        "Clínica Las Américas": [
            general, pediatrica, trauma, neurologica, cardiovascular,
        ],
        "Clínica CES": [
            general, neurologica, cardiovascular,
        ],
        "Clínica Universitaria Bolivariana": [
            general, pediatrica, ginecoobstetrica,
            neurologica, cardiovascular,
        ],
        "Clínica Las Vegas": [
            general, trauma, neurologica, cardiovascular,
        ],
        "Clínica Medellín Occidente": [
            general, trauma, neurologica, cardiovascular,
        ],
        "Clínica Medellín Poblado": [
            general, trauma, neurologica, cardiovascular,
        ],
        "Clínica El Rosario Sede Centro": [
            general, neurologica, cardiovascular,
        ],
        "Clínica El Rosario Sede El Tesoro": [
            general, pediatrica,
        ],
        "Clínica del Prado Ciudad del Río": [
            ginecoobstetrica,
        ],
        "Nueva Clínica Sagrado Corazón": [
            general, ginecoobstetrica,
        ],
        "Clínica Cardio VID": [
            general, cardiovascular,
        ],
        "Fundación Instituto Neurológico de Colombia": [
            neurologica,
        ],
        "Hospital Manuel Uribe Ángel": [
            general, pediatrica, ginecoobstetrica,
            trauma, neurologica, cardiovascular,
        ],
        "ESE Hospital Marco Fidel Suárez": [
            general, pediatrica, ginecoobstetrica, trauma,
        ],
        "ESE Hospital San Rafael de Itagüí": [
            general, pediatrica, ginecoobstetrica,
        ],
        "Hospital Venancio Díaz": [
            general, ginecoobstetrica,
        ],
        "ESE Hospital San Vicente de Paúl de Caldas": [
            general, pediatrica, ginecoobstetrica,
        ],
        "Corporación Hospital Infantil Concejo de Medellín": [
            pediatrica,
        ],
        "Fundación Clínica del Norte": [
            general, trauma, neurologica, cardiovascular,
        ],
        # En el catálogo existen dos registros/sedes de Clínica Antioquia.
        "Clínica Antioquia": [
            general, trauma,
        ],
        "Clínica Antioquia Sur": [
            general, trauma,
        ],
    }

    total_creadas = 0
    total_existentes = 0
    instituciones_no_encontradas = []

    for institution_name, attentions in relaciones.items():
        institution = Institution.query.filter_by(
            name=institution_name
        ).first()

        if institution is None:
            instituciones_no_encontradas.append(institution_name)
            print(f"⚠️ Institución no encontrada: {institution_name}")
            continue

        for attention in attentions:
            existe = InstitutionEmergencyAttention.query.filter_by(
                institution_id=institution.id,
                emergency_attention_id=attention.id,
            ).first()

            if existe:
                # Reactiva una relación previa si estaba desactivada.
                if not existe.is_active:
                    existe.is_active = True
                    total_creadas += 1
                else:
                    total_existentes += 1
                continue

            db.session.add(
                InstitutionEmergencyAttention(
                    institution_id=institution.id,
                    emergency_attention_id=attention.id,
                    is_active=True,
                )
            )
            total_creadas += 1

    db.session.commit()

    print("--------------------------------------------------")
    print("✅ Seed de categorías de urgencias completado")
    print(f"➕ Relaciones creadas/reactivadas: {total_creadas}")
    print(f"↩️ Relaciones que ya existían: {total_existentes}")
    print(f"⚠️ Instituciones no encontradas: {len(instituciones_no_encontradas)}")
    print("--------------------------------------------------")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_institution_emergency_attentions()