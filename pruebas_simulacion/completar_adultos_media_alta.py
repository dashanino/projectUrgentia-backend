import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-027": {
        "edad": 29,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal progresivo en la parte inferior derecha.",
        "historia_clinica": (
            "Hombre de 29 años con dolor abdominal iniciado hace 12 horas "
            "alrededor del ombligo, que posteriormente se desplazó hacia "
            "la parte inferior derecha. Intensidad 7/10, empeora al caminar "
            "y se acompaña de náuseas y pérdida de apetito. Sin desmayo."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor abdominal desde hace unas 12 horas.",
            "2": "Ha empeorado progresivamente.",
            "3": "Empezó alrededor del ombligo y ahora está abajo a la derecha.",
            "4": "Me duele más cuando camino y tengo náuseas.",
            "5": "He perdido el apetito, pero no me he desmayado."
        }
    },
    "URG-028": {
        "edad": 46,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre alta persistente desde hace dos días.",
        "historia_clinica": (
            "Mujer de 46 años con fiebre reportada de 39,2 °C durante "
            "dos días, escalofríos, dolores musculares y debilidad. "
            "Está consciente, orientada, puede beber líquidos y "
            "no presenta dificultad respiratoria."
        ),
        "respuestas_ia": {
            "1": "Tengo fiebre alta desde hace dos días.",
            "2": "Me he medido 39,2 grados.",
            "3": "Tengo escalofríos, dolor muscular y mucha debilidad.",
            "4": "Puedo beber agua y estoy consciente.",
            "5": "No tengo dificultad para respirar."
        }
    },
    "URG-029": {
        "edad": 52,
        "sexo": "Masculino",
        "banderas_ids": [3],
        "motivo_consulta": "Dolor opresivo en el pecho al realizar esfuerzo.",
        "historia_clinica": (
            "Hombre de 52 años con episodios recientes de presión "
            "en el centro del pecho al subir escaleras. Cada episodio "
            "dura aproximadamente diez minutos y mejora con el reposo. "
            "El último episodio ocurrió hace una hora. "
            "Actualmente no tiene dolor ni dificultad respiratoria."
        ),
        "respuestas_ia": {
            "1": "He sentido presión en el pecho cuando subo escaleras.",
            "2": "Los episodios duran unos diez minutos.",
            "3": "Me mejora cuando descanso.",
            "4": "El último episodio fue hace una hora.",
            "5": "Ahora no tengo dolor ni dificultad para respirar."
        }
    },
    "URG-030": {
        "edad": 34,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza intenso y persistente.",
        "historia_clinica": (
            "Mujer de 34 años con cefalea de intensidad 8/10 "
            "que aumentó gradualmente durante las últimas seis horas. "
            "Presenta náuseas y sensibilidad a la luz. "
            "Niega pérdida de conocimiento, confusión, "
            "debilidad de extremidades y fiebre."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor de cabeza muy fuerte.",
            "2": "Empezó hace seis horas y aumentó poco a poco.",
            "3": "Es de intensidad 8 sobre 10.",
            "4": "Tengo náuseas y la luz me molesta.",
            "5": "No tengo fiebre, confusión ni debilidad en brazos o piernas."
        }
    },
    "URG-031": {
        "edad": 40,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal acompañado de vómitos repetidos.",
        "historia_clinica": (
            "Hombre de 40 años con dolor abdominal de intensidad "
            "7/10 desde hace ocho horas, acompañado de cinco "
            "episodios de vómito. Durante las últimas cuatro horas "
            "ha tenido dificultad para retener líquidos. "
            "Está consciente y no refiere sangre en el vómito."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor abdominal y he vomitado varias veces.",
            "2": "El dolor empezó hace ocho horas.",
            "3": "Es de intensidad 7 sobre 10.",
            "4": "He vomitado cinco veces.",
            "5": "Me cuesta mantener líquidos, pero estoy consciente."
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