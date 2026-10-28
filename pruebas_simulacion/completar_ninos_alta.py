import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-002": {
        "edad": 4,
        "sexo": "Masculino",
        "banderas_ids": [5],
        "motivo_consulta": "Dificultad respiratoria grave.",
        "historia_clinica": (
            "Niño de 4 años con dificultad respiratoria intensa "
            "desde hace 30 minutos. Presenta respiración rápida, "
            "hundimiento de las costillas y dificultad para hablar "
            "o llorar con normalidad. Su cuidadora refiere que "
            "los síntomas están empeorando."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene cuatro años y respira con mucha dificultad.",
            "2": "Comenzó hace media hora.",
            "3": "Respira muy rápido y se le hunden las costillas.",
            "4": "Le cuesta hablar y llorar.",
            "5": "Está empeorando."
        }
    },
    "URG-003": {
        "edad": 8,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal intenso.",
        "historia_clinica": (
            "Niña de 8 años con dolor abdominal intenso de "
            "intensidad 9/10 desde hace tres horas. El dolor "
            "se localiza principalmente en la parte inferior "
            "derecha del abdomen. Presenta vómitos repetidos "
            "y dolor importante al caminar. Su cuidadora "
            "refiere empeoramiento progresivo."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene ocho años y le duele mucho el abdomen.",
            "2": "Comenzó hace tres horas.",
            "3": "El dolor es de 9 sobre 10.",
            "4": "Le duele más abajo a la derecha y ha vomitado varias veces.",
            "5": "Le duele al caminar y está empeorando."
        }
    },
    "URG-004": {
        "edad": 6,
        "sexo": "Masculino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre alta con confusión y somnolencia.",
        "historia_clinica": (
            "Niño de 6 años con temperatura de 40,0 °C "
            "desde hace cuatro horas. Su cuidadora refiere "
            "somnolencia marcada, dificultad para mantenerlo "
            "despierto y respuestas confusas. No se dispone "
            "de otros signos vitales."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene seis años y fiebre muy alta.",
            "2": "La temperatura llegó a 40 grados.",
            "3": "Empezó hace cuatro horas.",
            "4": "Está muy dormido y cuesta despertarlo.",
            "5": "Cuando responde, parece confundido."
        }
    },
    "URG-005": {
        "edad": 11,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Cefalea súbita intensa con vómitos.",
        "historia_clinica": (
            "Niña de 11 años con dolor de cabeza súbito "
            "de intensidad 10/10 desde hace 40 minutos. "
            "Presenta vómitos repetidos y dificultad para "
            "mantenerse de pie debido al malestar. "
            "Su cuidadora refiere que nunca había presentado "
            "un dolor de cabeza de esta intensidad."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene once años y le empezó un dolor de cabeza muy fuerte.",
            "2": "Comenzó de repente hace cuarenta minutos.",
            "3": "Dice que es de 10 sobre 10.",
            "4": "Ha vomitado varias veces.",
            "5": "Le cuesta mantenerse de pie."
        }
    },
    "URG-006": {
        "edad": 2,
        "sexo": "Masculino",
        "banderas_ids": [5],
        "motivo_consulta": "Dificultad respiratoria con labios azulados.",
        "historia_clinica": (
            "Niño de 2 años con dificultad respiratoria intensa "
            "desde hace 20 minutos. Su cuidadora observa "
            "coloración azulada alrededor de los labios, "
            "respiración rápida y disminución de la actividad. "
            "Los síntomas persisten."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene dos años y está respirando muy mal.",
            "2": "Empezó hace veinte minutos.",
            "3": "Tiene los labios azulados.",
            "4": "Respira muy rápido.",
            "5": "Está menos activo de lo normal."
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

        if caso["prioridad_objetivo"] != "alta":
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