import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-032": {
        "edad": 35,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal moderado desde esta mañana.",
        "historia_clinica": (
            "Hombre de 35 años con dolor alrededor del ombligo desde "
            "hace seis horas, intensidad 4/10, intermitente y estable. "
            "Niega fiebre, vómitos, náuseas, diarrea, distensión, "
            "síntomas urinarios y desplazamiento del dolor. "
            "Tolera alimentos y líquidos y puede caminar normalmente."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor alrededor del ombligo desde esta mañana, de 4 sobre 10.",
            "2": "El dolor va y viene y no ha aumentado.",
            "3": "No se ha desplazado hacia otra parte del abdomen.",
            "4": "No tengo diarrea, estreñimiento ni distensión.",
            "5": "No tengo síntomas urinarios.",
            "6": "Puedo comer y beber normalmente y no tengo náuseas.",
            "7": "No empeora al caminar ni tengo el abdomen duro.",
            "8": "No he tenido cirugías abdominales ni golpes recientes."
        }
    },
    "URG-033": {
        "edad": 27,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza moderado desde hace varias horas.",
        "historia_clinica": (
            "Mujer de 27 años con cefalea bilateral de intensidad "
            "5/10, iniciada gradualmente hace ocho horas. "
            "Refiere sensación de presión en la cabeza. "
            "Está orientada y niega fiebre, vómitos, alteraciones "
            "visuales, debilidad y pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor de cabeza desde hace ocho horas.",
            "2": "Empezó poco a poco.",
            "3": "Es una presión en ambos lados de la cabeza, de 5 sobre 10.",
            "4": "No tengo vómitos, fiebre ni problemas de visión.",
            "5": "Estoy consciente y no tengo debilidad."
        }
    },
    "URG-034": {
        "edad": 43,
        "sexo": "Masculino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre moderada y malestar general.",
        "historia_clinica": (
            "Hombre de 43 años con temperatura máxima reportada "
            "de 38,2 °C desde hace 24 horas, congestión nasal, "
            "dolor de garganta leve y cansancio. "
            "Puede comer, beber y realizar actividades básicas. "
            "Niega dificultad respiratoria, confusión y dolor torácico."
        ),
        "respuestas_ia": {
            "1": "Tengo fiebre y congestión nasal desde ayer.",
            "2": "La temperatura más alta fue 38,2 grados.",
            "3": "Tengo dolor leve de garganta y cansancio.",
            "4": "Puedo comer y beber normalmente.",
            "5": "No me falta el aire ni tengo dolor en el pecho."
        }
    },
    "URG-035": {
        "edad": 31,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal tipo cólico de intensidad moderada.",
        "historia_clinica": (
            "Mujer de 31 años con dolor abdominal tipo cólico "
            "de intensidad 4/10 desde hace cinco horas. "
            "Es intermitente, no ha empeorado y no se localiza "
            "en un punto específico. Niega fiebre, vómitos, "
            "sangrado y síntomas urinarios. "
            "No se ha documentado posibilidad de embarazo."
        ),
        "respuestas_ia": {
            "1": "Tengo cólicos abdominales desde hace cinco horas.",
            "2": "El dolor va y viene y no ha empeorado.",
            "3": "Es de 4 sobre 10 y no está en un punto específico.",
            "4": "No tengo fiebre, vómitos ni sangrado.",
            "5": "No tengo molestias al orinar.",
            "6": "Puedo tomar líquidos y comer.",
            "7": "No tengo el abdomen duro ni dolor intenso al moverme.",
            "8": "No he tenido golpes recientes en el abdomen."
        }
    },
    "URG-036": {
        "edad": 48,
        "sexo": "Masculino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza recurrente similar a episodios anteriores.",
        "historia_clinica": (
            "Hombre de 48 años con cefalea de intensidad 5/10 "
            "desde hace cuatro horas, de inicio gradual y "
            "características similares a episodios previos. "
            "Está orientado, puede caminar normalmente y niega "
            "fiebre, vómitos, confusión, alteraciones visuales "
            "y pérdida de fuerza."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor de cabeza desde hace cuatro horas.",
            "2": "Empezó gradualmente.",
            "3": "Es de 5 sobre 10 y parecido a otros dolores que he tenido.",
            "4": "No tengo vómitos, fiebre ni cambios en la visión.",
            "5": "Puedo caminar normalmente y no tengo debilidad."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 2:
            raise ValueError(f"Población incorrecta: {id_caso}")

        if caso["prioridad_objetivo"] != "media_baja":
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