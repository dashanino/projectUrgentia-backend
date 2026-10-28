import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-037": {
        "edad": 24,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza leve después de estudiar.",
        "historia_clinica": (
            "Mujer de 24 años con cefalea leve de intensidad 2/10, "
            "iniciada gradualmente después de varias horas de estudio. "
            "No presenta fiebre, vómitos, confusión, alteraciones "
            "visuales ni debilidad. Puede realizar sus actividades."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor de cabeza leve desde hace dos horas.",
            "2": "Empezó poco a poco después de estudiar.",
            "3": "Es de intensidad 2 sobre 10.",
            "4": "No tengo fiebre, vómitos ni cambios en la visión.",
            "5": "Puedo hacer mis actividades normalmente."
        }
    },
    "URG-038": {
        "edad": 30,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal leve que aparece ocasionalmente.",
        "historia_clinica": (
            "Hombre de 30 años con molestia abdominal difusa "
            "de intensidad 2/10 desde hace tres horas. "
            "El dolor es intermitente y ha disminuido. "
            "Niega fiebre, vómitos, diarrea, distensión abdominal "
            "y síntomas urinarios. Tolera alimentos y líquidos."
        ),
        "respuestas_ia": {
            "1": "Tengo una molestia leve en el abdomen.",
            "2": "Empezó hace tres horas y ha disminuido.",
            "3": "Es de intensidad 2 sobre 10 y no está localizada.",
            "4": "No tengo fiebre, vómitos ni diarrea.",
            "5": "Puedo comer y beber normalmente.",
            "6": "No tengo náuseas.",
            "7": "No tengo el abdomen duro ni dolor al caminar.",
            "8": "No he tenido golpes ni cirugías abdominales."
        }
    },
    "URG-039": {
        "edad": 41,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Temperatura ligeramente elevada y congestión nasal.",
        "historia_clinica": (
            "Mujer de 41 años con temperatura máxima reportada "
            "de 37,8 °C, congestión nasal y estornudos desde ayer. "
            "No presenta dificultad respiratoria, dolor torácico, "
            "confusión ni deshidratación. Se alimenta normalmente."
        ),
        "respuestas_ia": {
            "1": "Tengo congestión nasal y algo de temperatura desde ayer.",
            "2": "La temperatura máxima fue de 37,8 grados.",
            "3": "Tengo estornudos y congestión.",
            "4": "Puedo comer y beber normalmente.",
            "5": "No tengo dificultad para respirar ni dolor de pecho."
        }
    },
    "URG-040": {
        "edad": 26,
        "sexo": "Masculino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza leve que mejora con el descanso.",
        "historia_clinica": (
            "Hombre de 26 años con cefalea de intensidad 3/10 "
            "desde hace cuatro horas, de inicio gradual. "
            "El dolor ha disminuido después de descansar. "
            "Niega fiebre, vómitos, confusión, alteraciones "
            "visuales y pérdida de fuerza."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor de cabeza leve desde hace cuatro horas.",
            "2": "Empezó poco a poco.",
            "3": "Es de 3 sobre 10 y ha mejorado con el descanso.",
            "4": "No tengo vómitos, fiebre ni problemas de visión.",
            "5": "No tengo confusión ni debilidad."
        }
    },
    "URG-041": {
        "edad": 36,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve después de comer.",
        "historia_clinica": (
            "Mujer de 36 años con molestia abdominal leve "
            "de intensidad 2/10 después de una comida abundante. "
            "Comenzó hace dos horas y está mejorando. "
            "Niega vómitos, fiebre, sangrado y síntomas urinarios. "
            "No se ha documentado posibilidad de embarazo."
        ),
        "respuestas_ia": {
            "1": "Tengo una molestia leve en el abdomen después de comer.",
            "2": "Empezó hace dos horas y está mejorando.",
            "3": "Es de intensidad 2 sobre 10.",
            "4": "No tengo fiebre, vómitos ni sangrado.",
            "5": "No tengo molestias al orinar.",
            "6": "Puedo beber líquidos normalmente.",
            "7": "No tengo el abdomen duro ni dolor intenso al moverme.",
            "8": "No he tenido golpes recientes."
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

        if caso["prioridad_objetivo"] != "baja":
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