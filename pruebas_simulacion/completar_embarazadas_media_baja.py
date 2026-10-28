import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-072": {
        "edad": 26,
        "sexo": "Femenino",
        "semanas_gestacion": 22,
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve e intermitente.",
        "historia_clinica": (
            "Gestante de 26 años con 22 semanas de embarazo. "
            "Presenta molestia abdominal difusa de intensidad 3/10 "
            "desde hace cuatro horas, intermitente y sin empeoramiento. "
            "Niega sangrado vaginal, pérdida de líquido, fiebre "
            "y dolor intenso. No refiere contracciones regulares."
        ),
        "respuestas_ia": {
            "1": "Tengo 22 semanas de embarazo y una molestia leve en el abdomen.",
            "2": "Empezó hace cuatro horas y va y viene.",
            "3": "Es de 3 sobre 10 y no ha empeorado.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre ni contracciones regulares."
        }
    },
    "URG-073": {
        "edad": 30,
        "sexo": "Femenino",
        "semanas_gestacion": 25,
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza moderado durante el embarazo.",
        "historia_clinica": (
            "Gestante de 30 años con 25 semanas de embarazo. "
            "Presenta cefalea bilateral de intensidad 4/10 "
            "desde hace tres horas, de inicio gradual. "
            "Niega visión borrosa, zumbidos, dolor epigástrico "
            "y pérdida del conocimiento. No dispone de una "
            "medición reciente de presión arterial."
        ),
        "respuestas_ia": {
            "1": "Tengo 25 semanas de embarazo y dolor de cabeza.",
            "2": "Empezó poco a poco hace tres horas.",
            "3": "Es de intensidad 4 sobre 10.",
            "4": "No tengo visión borrosa ni zumbidos.",
            "5": "No sé cómo está mi presión arterial."
        }
    },
    "URG-074": {
        "edad": 23,
        "sexo": "Femenino",
        "semanas_gestacion": 20,
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal leve que mejora con reposo.",
        "historia_clinica": (
            "Gestante de 23 años con 20 semanas de embarazo. "
            "Presenta molestia abdominal baja de intensidad 2/10 "
            "después de caminar durante un periodo prolongado. "
            "Ha mejorado con reposo. Niega sangrado vaginal, "
            "pérdida de líquido, fiebre y contracciones regulares."
        ),
        "respuestas_ia": {
            "1": "Tengo 20 semanas de embarazo y una molestia leve abajo del abdomen.",
            "2": "Comenzó después de caminar bastante.",
            "3": "Es de 2 sobre 10 y mejora cuando descanso.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre ni contracciones regulares."
        }
    },
    "URG-075": {
        "edad": 33,
        "sexo": "Femenino",
        "semanas_gestacion": 27,
        "banderas_ids": [2],
        "motivo_consulta": "Cefalea gradual con presión arterial normal reportada.",
        "historia_clinica": (
            "Gestante de 33 años con 27 semanas de embarazo. "
            "Presenta cefalea de intensidad 4/10 desde hace "
            "cuatro horas, de inicio gradual. Refiere una "
            "medición reciente de presión arterial de 115/75 mmHg. "
            "Niega visión borrosa, zumbidos, dolor epigástrico, "
            "convulsiones y pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo 27 semanas de embarazo y me duele la cabeza.",
            "2": "Comenzó poco a poco hace cuatro horas.",
            "3": "Es de 4 sobre 10.",
            "4": "Me tomaron la presión y estaba en 115 sobre 75.",
            "5": "No tengo visión borrosa ni dolor en la boca del estómago."
        }
    },
    "URG-076": {
        "edad": 28,
        "sexo": "Femenino",
        "semanas_gestacion": 24,
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal moderado y estable.",
        "historia_clinica": (
            "Gestante de 28 años con 24 semanas de embarazo. "
            "Presenta dolor abdominal difuso de intensidad 4/10 "
            "desde hace cinco horas, intermitente y estable. "
            "Niega sangrado vaginal, pérdida de líquido, fiebre "
            "y contracciones regulares. No presenta vómitos."
        ),
        "respuestas_ia": {
            "1": "Tengo 24 semanas de embarazo y dolor abdominal moderado.",
            "2": "Empezó hace cinco horas.",
            "3": "Es de 4 sobre 10, va y viene y no ha aumentado.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre, vómitos ni contracciones regulares."
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

        if caso["prioridad_objetivo"] != "media_baja":
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