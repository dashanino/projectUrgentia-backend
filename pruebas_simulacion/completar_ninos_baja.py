import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-017": {
        "edad": 9,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza muy leve después de estudiar.",
        "historia_clinica": (
            "Niña de 9 años con cefalea bilateral de intensidad "
            "2/10 desde hace dos horas, después de realizar "
            "actividades escolares. El dolor comenzó gradualmente "
            "y está mejorando con descanso. Niega fiebre, vómitos, "
            "confusión, alteraciones visuales y debilidad. "
            "Está activa y se comporta normalmente."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene nueve años y le duele un poco la cabeza.",
            "2": "Empezó hace dos horas después de estudiar.",
            "3": "Es de 2 sobre 10.",
            "4": "Está mejorando con el descanso.",
            "5": "No tiene fiebre, vómitos ni cambios en la visión."
        }
    },
    "URG-018": {
        "edad": 6,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve después de comer.",
        "historia_clinica": (
            "Niño de 6 años con molestia abdominal difusa "
            "de intensidad 2/10 después de una comida abundante. "
            "Comenzó hace una hora y está disminuyendo. "
            "Niega fiebre, vómitos, diarrea y dolor al caminar. "
            "Está activo y tolera líquidos."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene seis años y le molesta un poco el abdomen.",
            "2": "Comenzó hace una hora después de comer.",
            "3": "Es de 2 sobre 10 y está mejorando.",
            "4": "No tiene fiebre, vómitos ni diarrea.",
            "5": "Está jugando y puede beber líquidos normalmente."
        }
    },
    "URG-019": {
        "edad": 10,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre leve con congestión nasal.",
        "historia_clinica": (
            "Niña de 10 años con temperatura máxima de 38,0 °C "
            "desde hace doce horas, acompañada de congestión nasal "
            "y estornudos. Está activa, come y bebe normalmente. "
            "Niega dificultad respiratoria, vómitos, somnolencia "
            "y dolor torácico."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene diez años y algo de fiebre.",
            "2": "La temperatura máxima fue de 38 grados.",
            "3": "Empezó hace doce horas.",
            "4": "Tiene congestión nasal y estornudos.",
            "5": "Está activa, come bien y respira normalmente."
        }
    },
    "URG-020": {
        "edad": 8,
        "sexo": "Masculino",
        "banderas_ids": [2],
        "motivo_consulta": "Cefalea leve que mejora con descanso.",
        "historia_clinica": (
            "Niño de 8 años con dolor de cabeza de intensidad "
            "2/10 desde hace tres horas. El dolor comenzó "
            "gradualmente y ha mejorado después de descansar. "
            "Niega fiebre, vómitos, alteraciones visuales, "
            "confusión y debilidad. Mantiene su actividad habitual."
        ),
        "respuestas_ia": {
            "1": "Mi hijo tiene ocho años y le duele un poco la cabeza.",
            "2": "Comenzó poco a poco hace tres horas.",
            "3": "Es de 2 sobre 10.",
            "4": "Ha mejorado con el descanso.",
            "5": "No tiene fiebre, vómitos ni problemas de visión."
        }
    },
    "URG-021": {
        "edad": 11,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve y transitoria.",
        "historia_clinica": (
            "Niña de 11 años con molestia abdominal alrededor "
            "del ombligo de intensidad 2/10 desde hace dos horas. "
            "La molestia es intermitente y ha disminuido. "
            "Niega fiebre, vómitos, diarrea y dolor al caminar. "
            "Está activa y tolera alimentos y líquidos."
        ),
        "respuestas_ia": {
            "1": "Mi hija tiene once años y una molestia leve en el abdomen.",
            "2": "Comenzó hace dos horas.",
            "3": "Es de 2 sobre 10 y está mejorando.",
            "4": "No tiene fiebre, vómitos ni diarrea.",
            "5": "Puede caminar, comer y beber normalmente."
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