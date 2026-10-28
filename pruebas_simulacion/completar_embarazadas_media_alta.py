import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-067": {
        "edad": 27,
        "sexo": "Femenino",
        "semanas_gestacion": 33,
        "banderas_ids": [11],
        "motivo_consulta": "Contracciones regulares antes de las 37 semanas.",
        "historia_clinica": (
            "Gestante de 27 años con 33 semanas de embarazo. "
            "Presenta contracciones dolorosas cada diez minutos "
            "desde hace dos horas, con presión pélvica. "
            "Niega sangrado vaginal y pérdida de líquido. "
            "Percibe movimientos fetales."
        ),
        "respuestas_ia": {
            "1": "Tengo 33 semanas de embarazo y estoy teniendo contracciones.",
            "2": "Comenzaron hace dos horas.",
            "3": "Las contracciones vienen cada diez minutos.",
            "4": "Siento presión en la pelvis, pero no tengo sangrado.",
            "5": "No he perdido líquido y siento mover a mi bebé."
        }
    },
    "URG-068": {
        "edad": 32,
        "sexo": "Femenino",
        "semanas_gestacion": 30,
        "banderas_ids": [12],
        "motivo_consulta": "Presión arterial elevada y dolor de cabeza persistente.",
        "historia_clinica": (
            "Gestante de 32 años con 30 semanas de embarazo. "
            "Refiere cefalea persistente de intensidad 6/10 "
            "desde hace cuatro horas y presión arterial "
            "reportada de 150/95 mmHg. Niega alteraciones "
            "visuales, convulsiones y pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo 30 semanas de embarazo y me duele la cabeza.",
            "2": "El dolor lleva cuatro horas.",
            "3": "Es de 6 sobre 10.",
            "4": "Me tomaron la presión y estaba en 150 sobre 95.",
            "5": "No tengo visión borrosa ni me he desmayado."
        }
    },
    "URG-069": {
        "edad": 24,
        "sexo": "Femenino",
        "semanas_gestacion": 28,
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal persistente durante el embarazo.",
        "historia_clinica": (
            "Gestante de 24 años con 28 semanas de embarazo. "
            "Presenta dolor abdominal de intensidad 6/10 "
            "desde hace cinco horas, localizado en la parte "
            "inferior del abdomen. Niega sangrado vaginal, "
            "pérdida de líquido y fiebre. Percibe movimientos "
            "fetales habituales. No se ha determinado si "
            "presenta actividad uterina."
        ),
        "respuestas_ia": {
            "1": "Tengo 28 semanas de embarazo y me duele la parte baja del abdomen.",
            "2": "El dolor empezó hace cinco horas.",
            "3": "Es de intensidad 6 sobre 10.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "Siento mover a mi bebé normalmente."
        }
    },
    "URG-070": {
        "edad": 35,
        "sexo": "Femenino",
        "semanas_gestacion": 36,
        "banderas_ids": [13, 14],
        "motivo_consulta": "Visión borrosa y zumbidos en los oídos.",
        "historia_clinica": (
            "Gestante de 35 años con 36 semanas de embarazo. "
            "Presenta visión borrosa y zumbidos en los oídos "
            "desde hace una hora. Refiere cefalea de intensidad "
            "5/10. No dispone de una medición reciente de "
            "presión arterial. Niega pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo 36 semanas de embarazo y estoy viendo borroso.",
            "2": "Empezó hace aproximadamente una hora.",
            "3": "También escucho zumbidos en los oídos.",
            "4": "Tengo dolor de cabeza de 5 sobre 10.",
            "5": "No sé cómo está mi presión arterial."
        }
    },
    "URG-071": {
        "edad": 29,
        "sexo": "Femenino",
        "semanas_gestacion": 34,
        "banderas_ids": [4],
        "motivo_consulta": "Dolor persistente en la parte superior del abdomen.",
        "historia_clinica": (
            "Gestante de 29 años con 34 semanas de embarazo. "
            "Presenta dolor epigástrico persistente de intensidad "
            "7/10 desde hace tres horas, acompañado de náuseas. "
            "Niega sangrado vaginal y pérdida de líquido. "
            "No dispone de una medición reciente de presión arterial."
        ),
        "respuestas_ia": {
            "1": "Tengo 34 semanas de embarazo y me duele la parte alta del abdomen.",
            "2": "El dolor comenzó hace tres horas.",
            "3": "Es constante y de intensidad 7 sobre 10.",
            "4": "Tengo náuseas, pero no estoy sangrando.",
            "5": "No sé cómo está mi presión arterial."
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

        if caso["prioridad_objetivo"] != "media_alta":
            raise ValueError(f"Prioridad incorrecta: {id_caso}")

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