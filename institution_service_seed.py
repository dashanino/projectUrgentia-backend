from app import create_app
from app.extensions import db
from app.models.institution import Institution
from app.models.service import Service
from app.models.institution_service import InstitutionService


service_institutions = {
    'CPRE (Colangiografía Retrógrada Endoscópica)': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Cardiología': [
        'AngioSur S.A.S.',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica del Norte',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cardiología Pediátrica': [
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía Cardiovascular': [
        'Clínica CES',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía General': [
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'ESE Hospital Marco Fidel Suárez',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Cirugía Hepatobiliar': [
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía Oncológica': [
        'Centro Oncológico de Antioquia',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Clínica Vida Sede Hospitalaria',
        'Fundación Colombiana de Cancerología Clínica Vida',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Instituto de Cancerología',
    ],

    'Cirugía Pediátrica': [
        'Clínica Antioquia',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Prado Ciudad del Río',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Cirugía Plástica': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Cirugía Reconstructiva Ortopédica': [
        'Clínica El Rosario Sede Centro',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía Vascular': [
        'AngioSur S.A.S.',
        'Clínica Antioquia',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Cirugía Vascular y Angiológica': [
        'Clínica Antioquia',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Hospital Alma Máter de Antioquia',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía de Cabeza y Cuello': [
        'Clínica Las Américas',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Cirugía de Tórax': [
        'Clínica CES',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Coloproctología': [
        'Clínica Las Américas',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Dermatología': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Dolor Paliativo': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Fibrobroncoscopia': [
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Gastroenterología': [
        'Clínica CES',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica del Norte',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ginecología': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Prado Ciudad del Río',
        'ESE Hospital San Vicente de Paúl de Caldas',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ginecología Oncológica': [
        'Centro Oncológico de Antioquia',
        'Clínica Las Américas',
        'Clínica Vida Sede Hospitalaria',
        'Fundación Colombiana de Cancerología Clínica Vida',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Instituto de Cancerología',
    ],

    'Ginecoobstetricia': [
        'Clínica Antioquia',
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Universitaria Bolivariana',
        'Clínica del Prado Ciudad del Río',
        'ESE Hospital Marco Fidel Suárez',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Hematología': [
        'Centro Oncológico de Antioquia',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Fundación Colombiana de Cancerología Clínica Vida',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Instituto de Cancerología',
        'Nueva Clínica Sagrado Corazón',
    ],

    'Hematooncología': [
        'Centro Oncológico de Antioquia',
        'Clínica El Rosario Sede Centro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica Vida Sede Hospitalaria',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Hemodinamia': [
        'AngioSur S.A.S.',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Hepatología': [
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Infectología': [
        'Clínica Cardio VID',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Maxilofacial': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Medicina Interna': [
        'Clínica Antioquia',
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'ESE Hospital Marco Fidel Suárez',
        'ESE Hospital San Rafael de Itagüí',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Medicina Nuclear': [
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Microcirugía': [
        'Clínica El Rosario Sede Centro',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Nefrología': [
        'AngioSur S.A.S.',
        'Clínica CES',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'ESE Hospital San Rafael de Itagüí',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Nefrología Pediátrica': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Universitaria Bolivariana',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Pablo Tobón Uribe',
    ],

    'Neonatología': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica del Prado Ciudad del Río',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Neumología': [
        'Clínica CES',
        'Clínica Cardio VID',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Neurocirugía': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Fundación Instituto Neurológico de Colombia',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Neurointervencionismo': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Fundación Instituto Neurológico de Colombia',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Neurología': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Fundación Instituto Neurológico de Colombia',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Neuropediatría': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Fundación Instituto Neurológico de Colombia',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Oftalmología': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Oncología': [
        'Centro Oncológico de Antioquia',
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Fundación Colombiana de Cancerología Clínica Vida',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Instituto de Cancerología',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ortopedia': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'Corporación Hospital Infantil Concejo de Medellín',
        'ESE Hospital La María',
        'ESE Hospital San Vicente de Paúl de Caldas',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ortopedia - Módulo de Cadera': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ortopedia - Módulo de Hombro': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Pablo Tobón Uribe',
    ],

    'Ortopedia - Módulo de Rodilla': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Norte',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Ortopedia Oncológica': [
        'Centro Oncológico de Antioquia',
        'Clínica Las Américas',
        'Fundación Colombiana de Cancerología Clínica Vida',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital Pablo Tobón Uribe',
    ],

    'Otorrinolaringología': [
        'Clínica CES',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'Pediatría': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Corporación Hospital Infantil Concejo de Medellín',
        'ESE Hospital Marco Fidel Suárez Sede 02 Niquía',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Psiquiatría': [
        'Clínica Universitaria Bolivariana',
    ],

    'Radiología Intervencionista': [
        'Clínica CES',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'Reumatología': [
        'Clínica CES',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Pablo Tobón Uribe',
    ],

    'Terapia ECMO (Oxigenación por Membrana Extracorpórea)': [
        'Clínica Cardio VID',
        'Clínica Las Américas',
        'Hospital Pablo Tobón Uribe',
    ],

    'Terapia Endovascular (Trombectomía Mecánica)': [
        'AngioSur S.A.S.',
        'Clínica Cardio VID',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
    ],

    'Toxicología': [
        'Clínica CES',
        'Clínica Las Américas',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'UCE Adulto': [
        'Clínica Antioquia',
        'Clínica CES',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Medellín Occidente',
        'Clínica Universitaria Bolivariana',
        'Clínica del Prado Ciudad del Río',
        'ESE Hospital La María',
        'ESE Hospital Marco Fidel Suárez',
        'ESE Hospital San Rafael de Itagüí',
        'Fundación Instituto Neurológico de Colombia',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'UCI Adultos': [
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica del Norte',
        'ESE Hospital La María',
        'ESE Hospital Marco Fidel Suárez',
        'ESE Hospital San Rafael de Itagüí',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Nueva Clínica Sagrado Corazón',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'UCI Cardiovascular': [
        'AngioSur S.A.S.',
        'Clínica Cardio VID',
        'Clínica El Rosario Sede Centro',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Medellín Occidente',
        'Clínica del Norte',
        'Especialidades Médicas Metropolitanas S.A. (EMMSA)',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
    ],

    'UCI Neonatal': [
        'Clínica Cardio VID',
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Clínica Universitaria Bolivariana',
        'Clínica del Prado Ciudad del Río',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

    'UCI Pediátrica': [
        'Clínica El Rosario Sede El Tesoro',
        'Clínica Las Américas',
        'Corporación Hospital Infantil Concejo de Medellín',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Unidad de Diálisis': [
        'Clínica Las Américas',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Pablo Tobón Uribe',
    ],

    'Urología': [
        'Clínica CES',
        'Clínica El Rosario Sede Centro',
        'Clínica Las Américas',
        'Clínica Las Vegas',
        'Clínica Universitaria Bolivariana',
        'ESE Hospital La María',
        'Fundación Hospitalaria San Vicente de Paúl',
        'Hospital Alma Máter de Antioquia',
        'Hospital General de Medellín Luz Castro de Gutiérrez ESE',
        'Hospital Manuel Uribe Ángel',
        'Hospital Pablo Tobón Uribe',
        'Sociedad Médica Antioqueña S.A. SOMA',
    ],

}


app = create_app()

with app.app_context():
    created = 0
    skipped_services = set()
    skipped_institutions = set()

    for service_name, institution_names in service_institutions.items():
        service = Service.query.filter_by(name=service_name).first()
        if not service:
            skipped_services.add(service_name)
            continue

        for institution_name in institution_names:
            institution = Institution.query.filter_by(name=institution_name).first()
            if not institution:
                skipped_institutions.add(institution_name)
                continue

            exists = InstitutionService.query.filter_by(
                institution_id=institution.id,
                service_id=service.id,
            ).first()

            if exists:
                continue

            db.session.add(InstitutionService(
                institution_id=institution.id,
                service_id=service.id,
            ))
            created += 1

    db.session.commit()

    print(f"Institution-service relationships created: {created}")
    if skipped_services:
        print("Services not found in DB:")
        for name in sorted(skipped_services):
            print(f"  - {name}")
    if skipped_institutions:
        print("Institutions not found in DB:")
        for name in sorted(skipped_institutions):
            print(f"  - {name}")
