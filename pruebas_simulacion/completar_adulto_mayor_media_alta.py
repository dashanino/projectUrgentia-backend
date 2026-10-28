import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-047": {
        "edad": 73,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal progresivo en la parte inferior derecha.",
        "historia_clinica": (
            "Hombre de 73 años con dolor abdominal de 7/10 desde "
            "hace diez horas. Inicialmente era difuso y ahora se "
            "localiza en la parte inferior derecha. Presenta náuseas "
            "y pérdida de apetito. El dolor empeora al caminar. "
            "Está consciente y orientado."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor abdominal desde hace diez horas.",
            "2": "El dolor ha aumentado progresivamente.",
            "3": "Ahora me duele principalmente abajo a la derecha.",
            "4": "Tengo náuseas y poco apetito.",
            "5": "Me duele más al caminar, pero estoy consciente."
        }
    },
    "URG-048": {
        "edad": 81,
        "sexo": "Femenino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre alta y debilidad desde hace dos días.",
        "historia_clinica": (
            "Mujer de 81 años con temperatura máxima de 39,1 °C "
            "desde hace dos días, escalofríos, debilidad y "
            "disminución de la ingesta de líquidos. "
            "Está orientada y puede conversar normalmente. "
            "Niega dificultad respiratoria y dolor torácico."
        ),
        "respuestas_ia": {
            "1": "Tengo fiebre alta desde hace dos días.",
            "2": "La temperatura más alta fue 39,1 grados.",
            "3": "Tengo escalofríos y mucha debilidad.",
            "4": "Estoy tomando menos líquidos de lo normal.",
            "5": "Estoy orientada y no tengo dificultad para respirar."
        }
    },
    "URG-049": {
        "edad": 69,
        "sexo": "Femenino",
        "banderas_ids": [7],
        "motivo_consulta": "Caída con dolor intenso de cadera.",
        "historia_clinica": (
            "Mujer de 69 años que sufrió una caída desde su propia "
            "altura hace una hora. Presenta dolor intenso en "
            "la cadera derecha, intensidad 8/10, e incapacidad "
            "para ponerse de pie o caminar. Niega golpe en la "
            "cabeza y pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Me caí hace una hora y me duele mucho la cadera.",
            "2": "Fue una caída desde mi propia altura.",
            "3": "El dolor es de 8 sobre 10.",
            "4": "No puedo ponerme de pie ni caminar.",
            "5": "No me golpeé la cabeza ni perdí el conocimiento."
        }
    },
    "URG-050": {
        "edad": 77,
        "sexo": "Masculino",
        "banderas_ids": [3],
        "motivo_consulta": "Presión en el pecho durante el esfuerzo.",
        "historia_clinica": (
            "Hombre de 77 años con episodios recientes de dolor "
            "opresivo en el centro del pecho al caminar. "
            "Cada episodio dura aproximadamente ocho minutos "
            "y mejora con el reposo. El último episodio ocurrió "
            "hace dos horas. Actualmente está sin dolor."
        ),
        "respuestas_ia": {
            "1": "Me ha dado presión en el pecho cuando camino.",
            "2": "Cada episodio dura unos ocho minutos.",
            "3": "Me mejora cuando descanso.",
            "4": "El último episodio fue hace dos horas.",
            "5": "Ahora no tengo dolor ni dificultad para respirar."
        }
    },
    "URG-051": {
        "edad": 85,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza intenso y persistente.",
        "historia_clinica": (
            "Mujer de 85 años con cefalea de intensidad 8/10 "
            "que comenzó gradualmente hace seis horas. "
            "Refiere náuseas, pero no ha vomitado. "
            "Está orientada y niega pérdida del conocimiento, "
            "debilidad de extremidades y confusión."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor de cabeza muy fuerte.",
            "2": "Comenzó poco a poco hace seis horas.",
            "3": "Es de intensidad 8 sobre 10.",
            "4": "Tengo náuseas, pero no he vomitado.",
            "5": "Estoy orientada y no tengo debilidad ni confusión."
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