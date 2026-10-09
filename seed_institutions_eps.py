from app import create_app
from app.extensions import db
from app.models.institution import Institution
from app.models.eps import EPS
from app.models.institution_eps import InstitutionEPS


app = create_app()


institution_eps = [

    # ============================================================
    # SURA
    # ============================================================

    ("Hospital General de Medellín Luz Castro de Gutiérrez ESE", "SURA"),
    ("Hospital Pablo Tobón Uribe", "SURA"),
    ("Fundación Hospitalaria San Vicente de Paúl", "SURA"),
    ("ESE Hospital La María", "SURA"),
    ("Clínica Las Américas", "SURA"),
    ("Clínica CES", "SURA"),
    ("Clínica Las Vegas", "SURA"),
    ("Clínica del Prado Ciudad del Río", "SURA"),
    ("Sociedad Médica Antioqueña S.A. SOMA", "SURA"),
    ("Clínica Universitaria Bolivariana", "SURA"),
    ("Fundación Instituto Neurológico de Colombia", "SURA"),
    ("Instituto de Cancerología", "SURA"),
    ("Fundación Colombiana de Cancerología Clínica Vida", "SURA"),
    ("Corporación Hospital Infantil Concejo de Medellín", "SURA"),
    ("Hospital Alma Máter de Antioquia", "SURA"),
    ("Hospital Manuel Uribe Ángel", "SURA"),
    ("Fundación Clínica del Norte", "SURA"),
    ("Hospital Venancio Díaz", "SURA"),

    # ============================================================
    # SANITAS
    # ============================================================

    ("Hospital Pablo Tobón Uribe", "Sanitas"),
    ("Hospital Alma Máter de Antioquia", "Sanitas"),
    ("Clínica del Prado Ciudad del Río", "Sanitas"),
    ("Sociedad Médica Antioqueña S.A. SOMA", "Sanitas"),
    ("Hospital Manuel Uribe Ángel", "Sanitas"),
    ("Fundación Clínica del Norte", "Sanitas"),
    ("Centro Oncológico de Antioquia", "Sanitas"),
    ("Clínica Las Vegas", "Sanitas"),
    ("ESE Hospital Marco Fidel Suárez", "Sanitas"),
    ("ESE Hospital San Rafael de Itagüí", "Sanitas"),

    # ============================================================
    # NUEVA EPS
    # ============================================================

    ("Fundación Clínica del Norte", "Nueva EPS"),
    ("ESE Hospital Marco Fidel Suárez", "Nueva EPS"),
    ("Clínica Antioquia", "Nueva EPS"),
    ("Hospital Alma Máter de Antioquia", "Nueva EPS"),
    ("Fundación Hospitalaria San Vicente de Paúl", "Nueva EPS"),
    ("Hospital Manuel Uribe Ángel", "Nueva EPS"),
    ("Clínica Medellín Occidente", "Nueva EPS"),
    ("Clínica Las Vegas", "Nueva EPS"),
    ("Clínica Universitaria Bolivariana", "Nueva EPS"),
    ("Hospital Pablo Tobón Uribe", "Nueva EPS"),
    ("ESE Hospital San Rafael de Itagüí", "Nueva EPS"),

    # ============================================================
    # SALUD TOTAL
    # ============================================================

    ("Hospital Alma Máter de Antioquia", "Salud Total"),
    ("Hospital Pablo Tobón Uribe", "Salud Total"),
    ("Clínica del Prado Ciudad del Río", "Salud Total"),
    ("Hospital Manuel Uribe Ángel", "Salud Total"),
    ("ESE Hospital Marco Fidel Suárez", "Salud Total"),
    ("Clínica CES", "Salud Total"),
    ("Sociedad Médica Antioqueña S.A. SOMA", "Salud Total"),
    ("Clínica Universitaria Bolivariana", "Salud Total"),

    # ============================================================
    # SAVIA SALUD
    # ============================================================

    ("Hospital General de Medellín Luz Castro de Gutiérrez ESE", "Savia Salud"),
    ("Hospital Pablo Tobón Uribe", "Savia Salud"),
    ("Fundación Hospitalaria San Vicente de Paúl", "Savia Salud"),
    ("ESE Hospital La María", "Savia Salud"),
    ("Clínica CES", "Savia Salud"),
    ("Clínica del Prado Ciudad del Río", "Savia Salud"),
    ("Sociedad Médica Antioqueña S.A. SOMA", "Savia Salud"),
    ("Clínica Cardio VID", "Savia Salud"),
    ("Fundación Instituto Neurológico de Colombia", "Savia Salud"),
    ("Hospital Alma Máter de Antioquia", "Savia Salud"),
    ("Corporación Hospital Infantil Concejo de Medellín", "Savia Salud"),
    ("Hospital Manuel Uribe Ángel", "Savia Salud"),
    ("Especialidades Médicas Metropolitanas S.A. (EMMSA)", "Savia Salud"),
    ("ESE Hospital Marco Fidel Suárez", "Savia Salud"),
    ("ESE Hospital San Rafael de Itagüí", "Savia Salud"),
    ("Visión Integrados S.A.S.", "Savia Salud"),

    # ============================================================
    # COOSALUD
    # ============================================================

    ("Hospital General de Medellín Luz Castro de Gutiérrez ESE", "Coosalud"),
    ("Hospital Pablo Tobón Uribe", "Coosalud"),
    ("Fundación Hospitalaria San Vicente de Paúl", "Coosalud"),
    ("ESE Hospital La María", "Coosalud"),
    ("Clínica CES", "Coosalud"),
    ("Clínica del Prado Ciudad del Río", "Coosalud"),
    ("Sociedad Médica Antioqueña S.A. SOMA", "Coosalud"),
    ("Fundación Instituto Neurológico de Colombia", "Coosalud"),
    ("Corporación Hospital Infantil Concejo de Medellín", "Coosalud"),
    ("Nueva Clínica Sagrado Corazón", "Coosalud"),
    ("Hospital Manuel Uribe Ángel", "Coosalud"),
    ("ESE Hospital Marco Fidel Suárez", "Coosalud"),
    ("ESE Hospital San Rafael de Itagüí", "Coosalud"),

    # ============================================================
    # FAMISANAR
    # ============================================================

    ("Hospital General de Medellín Luz Castro de Gutiérrez ESE", "Famisanar"),
    ("Hospital Pablo Tobón Uribe", "Famisanar"),
    ("Clínica Medellín Poblado", "Famisanar"),
    ("ESE Hospital San Rafael de Itagüí", "Famisanar"),
    ("Clínica Universitaria Bolivariana", "Famisanar"),

    # ============================================================
    # COMPENSAR
    # ============================================================

    ("Hospital Pablo Tobón Uribe", "Compensar"),

    # ============================================================
    # EMSSANAR
    # ============================================================

    # No agrego relaciones por ahora.
    # No encontré evidencia actual suficientemente fuerte
    # para una conexión vigente con las 48 instituciones.
]


with app.app_context():

    for institution_name, eps_name in institution_eps:

        institution = Institution.query.filter_by(
            name=institution_name
        ).first()

        if not institution:
            print(f"⚠️ Institución no encontrada: {institution_name}")
            continue

        eps = EPS.query.filter_by(
            name=eps_name
        ).first()

        if not eps:
            print(f"⚠️ EPS no encontrada: {eps_name}")
            continue

        exists = InstitutionEPS.query.filter_by(
            institution_id=institution.id,
            eps_id=eps.id
        ).first()

        if exists:
            print(
                f"↪️ Ya existe: {institution_name} - {eps_name}"
            )
            continue

        relation = InstitutionEPS(
            institution_id=institution.id,
            eps_id=eps.id
        )

        db.session.add(relation)

        print(
            f"✅ Agregada: {institution_name} - {eps_name}"
        )

    db.session.commit()

    print("\n========================================")
    print("Seed institution_eps completado")
    print("========================================")