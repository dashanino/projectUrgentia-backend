from app import create_app
from app.extensions import db
from app.models.institution import Institution

app = create_app()

institutions = [

    # =========================================================
    # MEDELLÍN
    # =========================================================

    {
        "name": "Hospital General de Medellín Luz Castro de Gutiérrez ESE",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 48 #32-102",
        "latitude": 6.23429,
        "longitude": -75.57265
    },

    {
        "name": "Hospital Pablo Tobón Uribe",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 78B #69-240",
        "latitude": 6.27732,
        "longitude": -75.57971
    },

    {
        "name": "Fundación Hospitalaria San Vicente de Paúl",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 64 #51D-154",
        "latitude": 6.26170,
        "longitude": -75.56581
    },

    {
        "name": "Hospital Alma Máter de Antioquia",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 69 #51C-24",
        "latitude": 6.26666,
        "longitude": -75.56480
    },

    {
        "name": "ESE Hospital La María",
        "type": "ESE",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 92EE #67-61",
        "latitude": 6.28644,
        "longitude": -75.57443
    },

    {
        "name": "Clínica Las Américas",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Diagonal 75B #2A-80",
        "latitude": 6.21402,
        "longitude": -75.59492
    },

    {
        "name": "Clínica CES",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 58 #50C-2",
        "latitude": 6.25757,
        "longitude": -75.56542
    },

    {
        "name": "Clínica Universitaria Bolivariana",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 72A #78B-50",
        "latitude": 6.27684,
        "longitude": -75.58218
    },

    {
        "name": "Clínica Las Vegas",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 2 Sur #46-55",
        "latitude": 6.20323,
        "longitude": -75.57643
    },

    {
        "name": "Clínica Medellín Occidente",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 65B #30-95",
        "latitude": 6.23261,
        "longitude": -75.58443
    },

    {
        "name": "Clínica Medellín Poblado",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 7 #39-290",
        "latitude": 6.20681,
        "longitude": -75.57124
    },

    {
        "name": "Clínica El Rosario Sede Centro",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 41 #62-5",
        "latitude": 6.25497,
        "longitude": -75.55657
    },

    {
        "name": "Clínica El Rosario Sede El Tesoro",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 20 #2 Sur-185",
        "latitude": 6.19386,
        "longitude": -75.55750
    },

    {
        "name": "Sociedad Médica Antioqueña S.A. SOMA",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 51 #45-93",
        "latitude": 6.24864,
        "longitude": -75.56439
    },

    {
        "name": "Clínica Cardio VID",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 78B #75-21",
        "latitude": 6.27939,
        "longitude": -75.58469
    },

    {
        "name": "Fundación Instituto Neurológico de Colombia",
        "type": "IPS_ESPECIALIZADA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 55 #46-36",
        "latitude": 6.250438,
        "longitude": -75.564547
    },

    {
        "name": "Instituto de Cancerología",
        "type": "IPS_ESPECIALIZADA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Carrera 70 #1-135, Torre 5",
        "latitude": 6.213693,
        "longitude": -75.594122
    },

    {
        "name": "Fundación Colombiana de Cancerología Clínica Vida",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Avenida 33 #63A-18",
        "latitude": 6.239867,
        "longitude": -75.579021
    },

    {
        "name": "Clínica Vida Sede Hospitalaria",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Avenida 80 #18A-140",
        "latitude": 6.224680,
        "longitude": -75.598940
    },

    {
        "name": "Clínica del Prado Ciudad del Río",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 19A #44-25",
        "latitude": 6.22241,
        "longitude": -75.57488
    },

    {
        "name": "Corporación Hospital Infantil Concejo de Medellín",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 72A #48A-70",
        "latitude": 6.267812,
        "longitude": -75.559423
    },

    {
        "name": "Nueva Clínica Sagrado Corazón",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Medellín",
        "address": "Calle 49 #35-61",
        "latitude": 6.241521,
        "longitude": -75.551834
    },

    {
        "name": "Clínica Oftalmológica Laureles S.A. (CLODEL)",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Transversal 74 #C1-23",
        "latitude": 6.244321,
        "longitude": -75.590123
    },

    {
        "name": "Clínica de Oftalmología Sandiego S.A.",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 43 #29-25",
        "latitude": 6.22890,
        "longitude": -75.56924
    },

    {
        "name": "Visión Integrados S.A.S.",
        "type": "IPS_ESPECIALIZADA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Avenida 33 #66B-23",
        "latitude": 6.236125,
        "longitude": -75.591211
    },

    {
        "name": "Clínica Oftalmológica de Antioquia S.A. (CLOFAN)",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 48 #19A-40",
        "latitude": 6.216512,
        "longitude": -75.578434
    },


    # =========================================================
    # ENVIGADO
    # =========================================================

    {
        "name": "Hospital Manuel Uribe Ángel",
        "type": "HOSPITAL",
        "level": 3,
        "municipality": "Envigado",
        "address": "Diagonal 31 #36A Sur-80",
        "latitude": 6.16682,
        "longitude": -75.58006
    },

    {
        "name": "Centro Oncológico de Antioquia",
        "type": "CLINICA_ESPECIALIZADA",
        "level": 3,
        "municipality": "Envigado",
        "address": "Carrera 48 #46A Sur-107",
        "latitude": 6.166841,
        "longitude": -75.602534
    },


    # =========================================================
    # BELLO
    # =========================================================

    {
        "name": "Clínica del Norte",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Bello",
        "address": "Avenida 38 Diagonal 59-50",
        "latitude": 6.34292,
        "longitude": -75.54592
    },

    {
        "name": "Especialidades Médicas Metropolitanas S.A. (EMMSA)",
        "type": "IPS_ESPECIALIZADA",
        "level": 3,
        "municipality": "Bello",
        "address": "Avenida 34 #51-03",
        "latitude": 6.339241,
        "longitude": -75.557412
    },

    {
        "name": "Clínica Antioquia",
        "type": "CLINICA",
        "level": 2,
        "municipality": "Bello",
        "address": "Carrera 48 #47-16",
        "latitude": 6.33222,
        "longitude": -75.55811
    },

    {
        "name": "ESE Hospital Marco Fidel Suárez",
        "type": "ESE",
        "level": 2,
        "municipality": "Bello",
        "address": "Calle 44 #49B-90",
        "latitude": 6.334125,
        "longitude": -75.560124
    },

    {
        "name": "ESE Hospital Marco Fidel Suárez Sede 02 Niquía",
        "type": "ESE",
        "level": 2,
        "municipality": "Bello",
        "address": "Avenida 42 #52-06",
        "latitude": 6.342114,
        "longitude": -75.552147
    },


    # =========================================================
    # ITAGÜÍ
    # =========================================================

    {
        "name": "Clínica Antioquia Sur",
        "type": "CLINICA",
        "level": 3,
        "municipality": "Itagüí",
        "address": "Calle 45 #48-51",
        "latitude": 6.174102,
        "longitude": -75.610521
    },

    {
        "name": "AngioSur S.A.S.",
        "type": "IPS_ESPECIALIZADA",
        "level": 3,
        "municipality": "Itagüí",
        "address": "Calle 47 #48-63",
        "latitude": 6.171542,
        "longitude": -75.609214
    },

    {
        "name": "ESE Hospital San Rafael de Itagüí",
        "type": "ESE",
        "level": 2,
        "municipality": "Itagüí",
        "address": "Carrera 51A #45-51",
        "latitude": 6.174365,
        "longitude": -75.614812
    },
    # =========================================================
     # SABANETA
     # =========================================================

    {


        "name": "Hospital Venancio Díaz",
        "type": "HOSPITAL",
        "level": 2,
        "municipality": "Sabaneta",
        "address": "Calle 77 Sur #46-43",
        "latitude": 6.148122,
        "longitude": -75.621743
    },
        # =========================================================
        # LA ESTRELLA
        # =========================================================
    {
        "name": "Hospital La Estrella",
        "type": "HOSPITAL",
        "level": 1,
        "municipality": "La Estrella",
        "address": "Calle 83A Sur #60-45",
        "latitude": 6.155452,
        "longitude": -75.644155
    },
        # =========================================================
        # CALDAS
        # =========================================================
    {
        "name": "ESE Hospital San Vicente de Paúl de Caldas",
        "type": "ESE",
        "level": 2,
        "municipality": "Caldas",
        "address": "Carrera 48 #135 Sur-41",
        "latitude": 6.091142,
        "longitude": -75.636125
    },
        # =========================================================
        # UNIDADES HOSPITALARIAS DE MEDELLÍN
        # =========================================================
    {
        "name": "Unidad Hospitalaria Santa Cruz Víctor Cárdenas Jaramillo",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 51A #100-80",
        "latitude": 6.292415,
        "longitude": -75.553142
    },
    {
        "name": "Unidad Hospitalaria Doce de Octubre Luis Carlos Galán Sarmiento",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Calle 108 #78-10",
        "latitude": 6.298102,
        "longitude": -75.578451
    },
    {
        "name": "Unidad Hospitalaria Buenos Aires Braulio Henao Mejía",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 31 #49-23",
        "latitude": 6.241124,
        "longitude": -75.549215
    },
    {
        "name": "Unidad Hospitalaria de Manrique Hermenegildo de Fex",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Calle 66E #42-51",
        "latitude": 6.265532,
        "longitude": -75.554012
    },
    {
        "name": "Unidad Hospitalaria San Antonio de Prado Diego Echavarría Misas",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 79 #40 Sur-45",
        "latitude": 6.183412,
        "longitude": -75.657142
    },
    {
        "name": "Unidad Hospitalaria de Belén Héctor Abad Gómez",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Calle 28 #77-124",
        "latitude": 6.228145,
        "longitude": -75.603124
    },
    {
        "name": "Unidad Hospitalaria de Castilla Jaime Tobón Arbeláez",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 65 #98-115",
        "latitude": 6.297412,
        "longitude": -75.571452
    },
    {
        "name": "Unidad Hospitalaria Nuevo Occidente",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Carrera 102C #63B-65",
        "latitude": 6.275102,
        "longitude": -75.619241
    },
    {
        "name": "Unidad Hospitalaria San Cristóbal Leonardo Betancur Taborda",
        "type": "UNIDAD_HOSPITALARIA",
        "level": 2,
        "municipality": "Medellín",
        "address": "Calle 63 #133-19",
        "latitude": 6.279412,
        "longitude": -75.634105
    },
]


with app.app_context():
    added_count = 0
    skipped_count = 0

    for item in institutions:

        institution = Institution.query.filter_by(
            name=item["name"]
        ).first()

        if institution:
            skipped_count += 1
            continue

        db.session.add(
            Institution(
                name=item["name"],
                type=item["type"],
                level=item["level"],
                municipality=item["municipality"],
                address=item["address"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                is_active=True
            )
        )
    
    added_count += 1
    db.session.commit()

    db.session.commit()

    print("--------------------------------------------------")
    print(f"✅ Proceso terminado con éxito.")
    print(f"📊 Total agregadas ahora: {added_count}")
    print(f"⏩ Omitidas (ya existían en la BD): {skipped_count}")
    print("--------------------------------------------------")
