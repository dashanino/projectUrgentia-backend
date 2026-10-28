import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-062": {
        "edad": 28,
        "sexo": "Femenino",
        "semanas_gestacion": 32,
        "banderas_ids": [8],
        "motivo_consulta": "Sangrado vaginal abundante durante el embarazo.",
        "historia_clinica": (
            "Gestante de 28 años, con 32 semanas de embarazo. "
            "Presenta sangrado vaginal abundante de color rojo "
            "desde hace 20 minutos, acompañado de dolor abdominal "
            "y sensación de mareo. No ha perdido el conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo 32 semanas de embarazo y estoy sangrando mucho.",
            "2": "El sangrado comenzó hace 20 minutos.",
            "3": "Es sangre roja y la cantidad es abundante.",
            "4": "También tengo dolor abdominal y mareo.",
            "5": "No me he desmayado."
        }
    },
    "URG-063": {
        "edad": 34,
        "sexo": "Femenino",
        "semanas_gestacion": 35,
        "banderas_ids": [9],
        "motivo_consulta": "Dificultad respiratoria intensa y tos con sangre.",
        "historia_clinica": (
            "Gestante de 34 años con 35 semanas de embarazo. "
            "Presenta dificultad respiratoria intensa de inicio "
            "súbito hace 30 minutos, acompañada de dolor torácico "
            "y tos con sangre. Le cuesta completar frases."
        ),
        "respuestas_ia": {
            "1": "Estoy embarazada de 35 semanas y me cuesta mucho respirar.",
            "2": "Comenzó de repente hace media hora.",
            "3": "También tengo dolor en el pecho.",
            "4": "He tosido sangre.",
            "5": "Me cuesta hablar sin detenerme a respirar."
        }
    },
    "URG-064": {
        "edad": 25,
        "sexo": "Femenino",
        "semanas_gestacion": 38,
        "banderas_ids": [10],
        "motivo_consulta": "No percibe movimientos fetales.",
        "historia_clinica": (
            "Gestante de 25 años con 38 semanas de embarazo. "
            "Refiere ausencia de movimientos fetales durante "
            "las últimas ocho horas, a pesar de que anteriormente "
            "los percibía regularmente. Niega sangrado vaginal "
            "y pérdida de líquido."
        ),
        "respuestas_ia": {
            "1": "Tengo 38 semanas de embarazo y no siento mover a mi bebé.",
            "2": "Hace unas ocho horas que no siento movimientos.",
            "3": "Antes lo sentía moverse normalmente.",
            "4": "No tengo sangrado vaginal.",
            "5": "No he tenido pérdida de líquido."
        }
    },
    "URG-065": {
        "edad": 31,
        "sexo": "Femenino",
        "semanas_gestacion": 34,
        "banderas_ids": [12, 13],
        "motivo_consulta": "Presión arterial elevada, cefalea intensa y visión borrosa.",
        "historia_clinica": (
            "Gestante de 31 años con 34 semanas de embarazo. "
            "Presenta dolor de cabeza intenso de 9/10, "
            "visión borrosa y presión arterial reportada "
            "de 170/110 mmHg. Los síntomas comenzaron "
            "hace aproximadamente una hora."
        ),
        "respuestas_ia": {
            "1": "Tengo 34 semanas de embarazo y me duele mucho la cabeza.",
            "2": "El dolor empezó hace una hora.",
            "3": "Es de 9 sobre 10 y veo borroso.",
            "4": "Me tomaron la presión y estaba en 170 sobre 110.",
            "5": "No he perdido el conocimiento."
        }
    },
    "URG-066": {
        "edad": 29,
        "sexo": "Femenino",
        "semanas_gestacion": 30,
        "banderas_ids": [8, 11],
        "motivo_consulta": "Contracciones frecuentes y sangrado vaginal.",
        "historia_clinica": (
            "Gestante de 29 años con 30 semanas de embarazo. "
            "Presenta contracciones dolorosas cada cuatro minutos "
            "desde hace una hora, acompañadas de sangrado vaginal "
            "moderado. Refiere presión intensa en la pelvis."
        ),
        "respuestas_ia": {
            "1": "Tengo 30 semanas de embarazo y estoy teniendo contracciones.",
            "2": "Las contracciones vienen cada cuatro minutos.",
            "3": "Comenzaron hace una hora.",
            "4": "También tengo sangrado vaginal.",
            "5": "Siento mucha presión en la pelvis."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 4:
            raise ValueError(f"Población incorrecta: {id_caso}")

        if caso["prioridad_objetivo"] != "alta":
            raise ValueError(f"Prioridad objetivo incorrecta: {id_caso}")

        caso.update(CASOS[id_caso])
        caso["antecedentes_ids"] = []
        caso["sintomas_ids"] = []
        caso["prioridad_esperada"] = None
        caso["estado_validacion"] = "pendiente_revision_clinica"

        actualizados.append(id_caso)

if len(actualizados) != 5:
    raise ValueError(
        f"Se esperaban 5 casos y se actualizaron {len(actualizados)}"
    )

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("Casos actualizados:")
for id_caso in actualizados:
    print(f"  {id_caso}")

print(f"\nTotal de casos: {len(casos)}")
print(
    "Casos con historia clínica:",
    sum(bool(c.get("historia_clinica")) for c in casos)
)