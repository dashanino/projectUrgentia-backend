import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-077": {
        "edad": 24,
        "sexo": "Femenino",
        "semanas_gestacion": 18,
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve después de caminar.",
        "historia_clinica": (
            "Gestante de 24 años con 18 semanas de embarazo. "
            "Presenta molestia abdominal baja de intensidad 2/10 "
            "después de caminar durante una hora. La molestia "
            "ha disminuido con reposo. Niega sangrado vaginal, "
            "pérdida de líquido, fiebre y contracciones regulares."
        ),
        "respuestas_ia": {
            "1": "Tengo 18 semanas de embarazo y una molestia leve en el abdomen.",
            "2": "Comenzó después de caminar.",
            "3": "Es de 2 sobre 10 y mejora cuando descanso.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre ni contracciones."
        }
    },
    "URG-078": {
        "edad": 29,
        "sexo": "Femenino",
        "semanas_gestacion": 16,
        "banderas_ids": [],
        "motivo_consulta": "Cefalea leve similar a episodios habituales.",
        "historia_clinica": (
            "Gestante de 29 años con 16 semanas de embarazo. "
            "Presenta cefalea bilateral de intensidad 2/10 "
            "desde hace dos horas, similar a episodios previos "
            "y con mejoría después de descansar. "
            "Niega visión borrosa, zumbidos, vómitos y confusión. "
            "No dispone de medición reciente de presión arterial."
        ),
        "respuestas_ia": {
            "1": "Tengo 16 semanas de embarazo y un dolor de cabeza leve.",
            "2": "Empezó hace dos horas.",
            "3": "Es de 2 sobre 10 y se parece a otros dolores que he tenido.",
            "4": "Ha mejorado con el descanso.",
            "5": "No tengo visión borrosa ni zumbidos.",
            "6": "No sé cómo está mi presión arterial."
        }
    },
    "URG-079": {
        "edad": 26,
        "sexo": "Femenino",
        "semanas_gestacion": 21,
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve después de comer.",
        "historia_clinica": (
            "Gestante de 26 años con 21 semanas de embarazo. "
            "Presenta molestia abdominal difusa de intensidad "
            "2/10 después de una comida abundante. "
            "Ha disminuido progresivamente durante las últimas "
            "dos horas. Niega sangrado vaginal, pérdida de líquido, "
            "fiebre, vómitos y contracciones regulares."
        ),
        "respuestas_ia": {
            "1": "Tengo 21 semanas de embarazo y una molestia leve en el abdomen.",
            "2": "Comenzó después de comer.",
            "3": "Es de 2 sobre 10 y está mejorando.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre, vómitos ni contracciones."
        }
    },
    "URG-080": {
        "edad": 32,
        "sexo": "Femenino",
        "semanas_gestacion": 19,
        "banderas_ids": [],
        "motivo_consulta": "Cefalea leve de inicio gradual.",
        "historia_clinica": (
            "Gestante de 32 años con 19 semanas de embarazo. "
            "Presenta cefalea de intensidad 3/10 desde hace "
            "tres horas, de inicio gradual. Niega visión borrosa, "
            "zumbidos, dolor epigástrico, vómitos y confusión. "
            "No dispone de medición reciente de presión arterial."
        ),
        "respuestas_ia": {
            "1": "Tengo 19 semanas de embarazo y dolor de cabeza leve.",
            "2": "Comenzó poco a poco hace tres horas.",
            "3": "Es de 3 sobre 10.",
            "4": "No tengo visión borrosa ni zumbidos.",
            "5": "No tengo vómitos ni confusión.",
            "6": "No sé cómo está mi presión arterial."
        }
    },
    "URG-081": {
        "edad": 27,
        "sexo": "Femenino",
        "semanas_gestacion": 23,
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve y transitoria.",
        "historia_clinica": (
            "Gestante de 27 años con 23 semanas de embarazo. "
            "Presenta molestia abdominal baja de intensidad "
            "2/10, intermitente, desde hace tres horas. "
            "Ha disminuido con reposo. Niega sangrado vaginal, "
            "pérdida de líquido, fiebre y contracciones regulares."
        ),
        "respuestas_ia": {
            "1": "Tengo 23 semanas de embarazo y una molestia leve abajo del abdomen.",
            "2": "Comenzó hace tres horas.",
            "3": "Es de 2 sobre 10 y está mejorando.",
            "4": "No tengo sangrado ni pérdida de líquido.",
            "5": "No tengo fiebre ni contracciones."
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

        if caso["prioridad_objetivo"] != "baja":
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