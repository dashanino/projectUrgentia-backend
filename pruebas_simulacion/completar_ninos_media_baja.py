import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-012": {
        "edad": 8,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal leve y estable.",
        "historia_clinica": (
            "Niño de 8 años con dolor abdominal alrededor del ombligo "
            "de intensidad 4/10 desde hace cuatro horas. "
            "El dolor es intermitente y no ha aumentado. "
            "Niega fiebre, vómitos y diarrea. "
            "Puede caminar, comer y beber normalmente."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene ocho años y le duele el abdomen.",
            "2": "Comenzó hace cuatro horas.",
            "3": "El dolor es de 4 sobre 10 y va y viene.",
            "4": "No tiene fiebre, vómitos ni diarrea.",
            "5": "Puede caminar, comer y beber normalmente."
        }
    },
    "URG-013": {
        "edad": 10,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Cefalea moderada de inicio gradual.",
        "historia_clinica": (
            "Niña de 10 años con dolor de cabeza bilateral "
            "de intensidad 5/10 desde hace cinco horas. "
            "El dolor comenzó gradualmente y no ha empeorado. "
            "Niega fiebre, vómitos, confusión, alteraciones "
            "visuales y debilidad. Está activa y orientada."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene diez años y le duele la cabeza.",
            "2": "Comenzó poco a poco hace cinco horas.",
            "3": "Es de 5 sobre 10 y no ha empeorado.",
            "4": "No tiene fiebre, vómitos ni cambios en la visión.",
            "5": "Está activa y responde normalmente."
        }
    },
    "URG-014": {
        "edad": 6,
        "sexo": "Masculino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre leve con congestión nasal.",
        "historia_clinica": (
            "Niño de 6 años con temperatura máxima de 38,2 °C "
            "desde hace un día, congestión nasal y dolor leve "
            "de garganta. Está activo, juega normalmente "
            "y tolera alimentos y líquidos. "
            "Niega dificultad respiratoria, vómitos y somnolencia."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene seis años y fiebre desde ayer.",
            "2": "La temperatura máxima fue de 38,2 grados.",
            "3": "Tiene congestión nasal y un poco de dolor de garganta.",
            "4": "Está activo y juega normalmente.",
            "5": "Come y bebe bien, y no tiene dificultad para respirar."
        }
    },
    "URG-015": {
        "edad": 11,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal intermitente.",
        "historia_clinica": (
            "Niña de 11 años con dolor abdominal difuso "
            "de intensidad 4/10 desde hace seis horas. "
            "El dolor aparece por momentos y no ha empeorado. "
            "Niega fiebre, vómitos, diarrea y sangrado. "
            "Puede caminar normalmente y tolera líquidos."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene once años y le duele el abdomen.",
            "2": "El dolor empezó hace seis horas.",
            "3": "Es de 4 sobre 10 y aparece por momentos.",
            "4": "No tiene fiebre, vómitos ni diarrea.",
            "5": "Puede caminar y beber líquidos normalmente."
        }
    },
    "URG-016": {
        "edad": 7,
        "sexo": "Masculino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza recurrente sin cambios.",
        "historia_clinica": (
            "Niño de 7 años con cefalea de intensidad 4/10 "
            "desde hace tres horas. Su cuidadora refiere "
            "episodios similares durante los últimos meses, "
            "sin cambios en las características del dolor. "
            "Niega fiebre, vómitos, alteraciones visuales, "
            "confusión y debilidad. Está activo."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene siete años y le duele la cabeza.",
            "2": "Comenzó hace tres horas.",
            "3": "Es de 4 sobre 10.",
            "4": "Ha tenido dolores parecidos antes.",
            "5": "No tiene fiebre, vómitos ni cambios en la visión."
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