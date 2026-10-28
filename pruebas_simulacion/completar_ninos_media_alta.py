import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-007": {
        "edad": 9,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal progresivo.",
        "historia_clinica": (
            "Niño de 9 años con dolor abdominal de intensidad 7/10 "
            "desde hace ocho horas. Comenzó alrededor del ombligo "
            "y posteriormente se localizó en la parte inferior "
            "derecha del abdomen. Presenta náuseas, disminución "
            "del apetito y dolor al caminar. Niega sangrado."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene nueve años y le duele el abdomen.",
            "2": "El dolor empezó hace ocho horas.",
            "3": "Es de 7 sobre 10.",
            "4": "Primero le dolía alrededor del ombligo y ahora abajo a la derecha.",
            "5": "Tiene náuseas, no quiere comer y le duele al caminar."
        }
    },
    "URG-008": {
        "edad": 5,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre alta persistente.",
        "historia_clinica": (
            "Niña de 5 años con fiebre de hasta 39,5 °C "
            "desde hace dos días. Presenta cansancio, "
            "disminución del apetito y menor consumo de líquidos. "
            "Está despierta, responde adecuadamente y no "
            "presenta dificultad respiratoria. La cuidadora "
            "refiere que ha orinado menos de lo habitual."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene cinco años y fiebre desde hace dos días.",
            "2": "La temperatura máxima ha sido de 39,5 grados.",
            "3": "Está cansada y come poco.",
            "4": "Está tomando menos líquidos y orinando menos.",
            "5": "Está despierta y responde normalmente."
        }
    },
    "URG-009": {
        "edad": 10,
        "sexo": "Masculino",
        "banderas_ids": [5],
        "motivo_consulta": "Dificultad respiratoria moderada.",
        "historia_clinica": (
            "Niño de 10 años con dificultad respiratoria "
            "desde hace tres horas, acompañada de tos. "
            "Respira más rápido de lo habitual y refiere "
            "sensación de falta de aire al caminar. "
            "Puede hablar en frases completas. "
            "Niega coloración azulada de los labios."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene diez años y le cuesta respirar.",
            "2": "Comenzó hace tres horas.",
            "3": "Respira rápido y tiene tos.",
            "4": "Se cansa cuando camina.",
            "5": "Puede hablar normalmente y no tiene los labios azulados."
        }
    },
    "URG-010": {
        "edad": 7,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Cefalea intensa acompañada de vómitos.",
        "historia_clinica": (
            "Niña de 7 años con cefalea de intensidad 8/10 "
            "desde hace cuatro horas. El dolor comenzó "
            "gradualmente y se acompaña de dos episodios "
            "de vómito y sensibilidad a la luz. "
            "Está orientada y no presenta pérdida "
            "del conocimiento. No se ha documentado "
            "si tiene rigidez de cuello."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene siete años y un dolor de cabeza fuerte.",
            "2": "Empezó poco a poco hace cuatro horas.",
            "3": "Dice que es de 8 sobre 10.",
            "4": "Ha vomitado dos veces y le molesta la luz.",
            "5": "Está despierta y responde normalmente."
        }
    },
    "URG-011": {
        "edad": 3,
        "sexo": "Masculino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre y vómitos con menor ingesta de líquidos.",
        "historia_clinica": (
            "Niño de 3 años con fiebre de hasta 39,0 °C "
            "desde hace 24 horas y cuatro episodios de vómito. "
            "Su cuidadora refiere menor consumo de líquidos "
            "y disminución de la cantidad de orina. "
            "Está despierto y responde a estímulos, "
            "pero se encuentra más decaído de lo habitual."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene tres años y fiebre desde ayer.",
            "2": "La temperatura máxima fue de 39 grados.",
            "3": "Ha vomitado cuatro veces.",
            "4": "Está tomando menos líquidos y orinando menos.",
            "5": "Está despierto, pero más decaído de lo normal."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 1:
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