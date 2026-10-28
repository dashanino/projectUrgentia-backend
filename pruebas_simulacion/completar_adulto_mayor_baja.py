import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-057": {
        "edad": 67,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza leve similar a episodios anteriores.",
        "historia_clinica": (
            "Mujer de 67 años con cefalea leve de intensidad 2/10, "
            "iniciada gradualmente hace tres horas. Refiere episodios "
            "similares desde hace varios años, sin cambios recientes "
            "en las características del dolor. Niega fiebre, vómitos, "
            "confusión, alteraciones visuales y debilidad."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor de cabeza leve desde hace tres horas.",
            "2": "Empezó poco a poco.",
            "3": "Es de 2 sobre 10, igual a otros dolores que he tenido.",
            "4": "No tengo fiebre, vómitos ni cambios en la visión.",
            "5": "Estoy orientada y no tengo debilidad."
        }
    },
    "URG-058": {
        "edad": 74,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve después de comer.",
        "historia_clinica": (
            "Hombre de 74 años con molestia abdominal difusa "
            "de intensidad 2/10 después de una comida abundante. "
            "Comenzó hace tres horas y ha disminuido progresivamente. "
            "Niega fiebre, vómitos, sangrado, distensión y dificultad "
            "para expulsar gases. Tolera líquidos."
        ),
        "respuestas_ia": {
            "1": "Tengo una molestia leve en el abdomen después de comer.",
            "2": "Comenzó hace tres horas y está mejorando.",
            "3": "Es de intensidad 2 sobre 10.",
            "4": "No tengo fiebre, vómitos ni sangrado.",
            "5": "Puedo beber líquidos y expulsar gases.",
            "6": "No tengo náuseas.",
            "7": "No tengo el abdomen duro ni dolor al caminar.",
            "8": "No he tenido golpes ni cirugías abdominales."
        }
    },
    "URG-059": {
        "edad": 69,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre baja y congestión nasal desde ayer.",
        "historia_clinica": (
            "Mujer de 69 años con temperatura máxima reportada "
            "de 38,0 °C desde hace un día, congestión nasal "
            "y estornudos. Está orientada, se alimenta normalmente "
            "y niega dificultad respiratoria, dolor torácico "
            "y confusión."
        ),
        "respuestas_ia": {
            "1": "Tengo congestión nasal y algo de fiebre desde ayer.",
            "2": "La temperatura máxima fue de 38 grados.",
            "3": "Tengo estornudos y congestión.",
            "4": "Puedo comer y beber normalmente.",
            "5": "No tengo dificultad para respirar ni confusión."
        }
    },
    "URG-060": {
        "edad": 78,
        "sexo": "Masculino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza leve que mejora con descanso.",
        "historia_clinica": (
            "Hombre de 78 años con cefalea de intensidad 3/10 "
            "desde hace cuatro horas. El dolor comenzó gradualmente "
            "y ha mejorado después de descansar. Refiere episodios "
            "similares anteriormente. Niega fiebre, vómitos, "
            "confusión, alteraciones visuales y pérdida de fuerza."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor de cabeza leve desde hace cuatro horas.",
            "2": "Comenzó poco a poco.",
            "3": "Es de 3 sobre 10 y ha mejorado con el descanso.",
            "4": "No tengo vómitos, fiebre ni cambios en la visión.",
            "5": "No estoy confundido y no tengo debilidad."
        }
    },
    "URG-061": {
        "edad": 72,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal leve e intermitente.",
        "historia_clinica": (
            "Mujer de 72 años con molestia abdominal difusa "
            "de intensidad 2/10 desde hace cinco horas. "
            "Es intermitente y ha disminuido. Niega fiebre, "
            "vómitos, sangrado, distensión, síntomas urinarios "
            "y dificultad para evacuar. Tolera alimentos y líquidos."
        ),
        "respuestas_ia": {
            "1": "Tengo una molestia leve en el abdomen desde hace cinco horas.",
            "2": "Va y viene y ha disminuido.",
            "3": "Es de intensidad 2 sobre 10.",
            "4": "No tengo fiebre, vómitos ni sangrado.",
            "5": "Puedo comer, beber y evacuar normalmente.",
            "6": "No tengo náuseas.",
            "7": "No tengo el abdomen duro ni dolor al moverme.",
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
        if caso["poblacion_id"] != 3:
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