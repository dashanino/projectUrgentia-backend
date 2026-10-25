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

    relaciones = {

        "Hospital General de Medellín Luz Castro de Gutiérrez ESE": [
            general,
            pediatrica,
            ginecoobstetrica,
            trauma,
            neurologica,
            cardiovascular,
        ],

        "Hospital Pablo Tobón Uribe": [
            general,
            pediatrica,
            trauma,
            neurologica,
            cardiovascular,
        ],

        "Fundación Hospitalaria San Vicente de Paúl": [
            general,
            trauma,
            neurologica,
            cardiovascular,
        ],

        "Hospital Alma Máter de Antioquia": [
            general,
            trauma,
            cardiovascular,
        ],

        "Clínica Las Américas": [
            general,
            pediatrica,
            trauma,
            neurologica,
            cardiovascular,
        ],

        "Clínica CES": [
            general,
            neurologica,
            cardiovascular,
        ],

        "Clínica Universitaria Bolivariana": [
            general,
            ginecoobstetrica,
            cardiovascular,
        ],

        "Clínica El Rosario Sede Centro": [
            general,
            neurologica,
            cardiovascular,
        ],

        "Clínica Cardio VID": [
            general,
            cardiovascular,
        ],

        "Fundación Instituto Neurológico de Colombia": [
            neurologica,
        ],

        "Hospital Manuel Uribe Ángel": [
            general,
            pediatrica,
            ginecoobstetrica,
            trauma,
            neurologica,
            cardiovascular,
        ],

        "ESE Hospital Marco Fidel Suárez": [
            general,
            pediatrica,
            ginecoobstetrica,
            trauma,
        ],

        "ESE Hospital San Rafael de Itagüí": [
            general,
            pediatrica,
            ginecoobstetrica,
        ],

        "Hospital Venancio Díaz": [
            general,
            ginecoobstetrica,
        ],

        "ESE Hospital San Vicente de Paúl de Caldas": [
            general,
            pediatrica,
            ginecoobstetrica,
        ],

        "Corporación Hospital Infantil Concejo de Medellín": [
            pediatrica,
        ],

        "Fundación Clínica del Norte": [
            general,
            trauma,
            neurologica,
            cardiovascular,
        ],
    }

    total = 0

    for institution_name, attentions in relaciones.items():

        institution = Institution.query.filter_by(
            name=institution_name
        ).first()

        if not institution:
            print(f"⚠️ Institución no encontrada: {institution_name}")
            continue

        for attention in attentions:

            if not attention:
                print(
                    f"⚠️ Tipo de atención no encontrado "
                    f"para {institution_name}"
                )
                continue

            existe = InstitutionEmergencyAttention.query.filter_by(
                institution_id=institution.id,
                emergency_attention_id=attention.id
            ).first()

            if existe:
                continue

            relation = InstitutionEmergencyAttention(
                institution_id=institution.id,
                emergency_attention_id=attention.id,
                is_active=True
            )

            db.session.add(relation)
            total += 1

    db.session.commit()

    print(f"✅ Seed completado. Relaciones creadas: {total}")


if __name__ == "__main__":

    app = create_app()

    with app.app_context():
        seed_institution_emergency_attentions()