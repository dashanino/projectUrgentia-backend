import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"

# Datos extraídos de las cinco historias clínicas revisadas.
# No se agregan diagnósticos ni signos vitales no documentados.

EXTRACCIONES = {
    "URG-002": {
        "datos_clinicos": {
            "inicio": "Hace 30 minutos",
            "duracion": "30 minutos",
            "evolucion": "Empeoramiento progresivo",
            "sintomas_asociados": [
                "Dificultad respiratoria intensa",
                "Respiración rápida",
                "Hundimiento de las costillas",
                "Dificultad para hablar o llorar normalmente"
            ],
            "signos_alarma": [
                "Dificultad respiratoria intensa",
                "Hundimiento de las costillas",
                "Dificultad para hablar o llorar normalmente"
            ],
            "fuente_informacion": "Cuidadora"
        },
        "datos_especificos_poblacion": {
            "cuidador": "Cuidadora, relación no especificada",
            "signos_respiratorios": [
                "Respiración rápida",
                "Hundimiento de las costillas",
                "Dificultad para hablar o llorar normalmente"
            ]
        }
    },

    "URG-022": {
        "datos_clinicos": {
            "inicio": "Hace 30 minutos",
            "duracion": "30 minutos",
            "intensidad_dolor": "9/10",
            "localizacion": "Pecho, irradiado al brazo izquierdo",
            "sintomas_asociados": [
                "Dolor torácico opresivo",
                "Sudoración fría",
                "Náuseas",
                "Dificultad respiratoria"
            ],
            "sintomas_negados": [
                "Pérdida del conocimiento"
            ],
            "signos_alarma": [
                "Dolor torácico opresivo intenso",
                "Dificultad respiratoria"
            ]
        },
        "datos_especificos_poblacion": {
            "dolor_toracico": {
                "tipo": "Opresivo",
                "inicio": "En reposo",
                "irradiacion": "Brazo izquierdo"
            }
        }
    },

    "URG-042": {
        "datos_clinicos": {
            "inicio": "Hace 25 minutos",
            "duracion": "25 minutos",
            "intensidad_dolor": "9/10",
            "localizacion": "Pecho, irradiado al brazo izquierdo",
            "sintomas_asociados": [
                "Dolor torácico opresivo",
                "Sudoración fría",
                "Náuseas",
                "Dificultad respiratoria en reposo"
            ],
            "signos_alarma": [
                "Dolor torácico opresivo intenso",
                "Dificultad respiratoria en reposo"
            ]
        },
        "datos_especificos_poblacion": {
            "dolor_toracico": {
                "tipo": "Opresivo",
                "irradiacion": "Brazo izquierdo"
            },
            "estado_conciencia": "Consciente"
        }
    },

    "URG-062": {
        "datos_clinicos": {
            "inicio": "Hace 20 minutos",
            "duracion": "20 minutos",
            "sintomas_asociados": [
                "Sangrado vaginal abundante",
                "Dolor abdominal",
                "Mareo"
            ],
            "sintomas_negados": [
                "Pérdida del conocimiento"
            ],
            "signos_alarma": [
                "Sangrado vaginal abundante durante el embarazo"
            ]
        },
        "datos_especificos_poblacion": {
            "semanas_gestacion": 32,
            "sangrado_vaginal": "Abundante, color rojo"
        }
    },

    "URG-082": {
        "datos_clinicos": {
            "inicio": "Hace 20 minutos",
            "duracion": "20 minutos",
            "intensidad_dolor": "9/10",
            "localizacion": "Pecho",
            "evolucion": "Empeoramiento progresivo",
            "sintomas_asociados": [
                "Dificultad respiratoria intensa",
                "Dolor torácico",
                "Respiración rápida",
                "Dificultad para completar frases"
            ],
            "signos_alarma": [
                "Dificultad respiratoria intensa",
                "Dificultad para completar frases"
            ]
        },
        "datos_especificos_poblacion": {
            "mecanismo_trauma": "Colisión de motocicleta",
            "tiempo_desde_accidente": "20 minutos"
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    fichas = json.load(archivo)

actualizadas = []

for ficha in fichas:
    id_caso = ficha["id_caso"]

    if id_caso not in EXTRACCIONES:
        continue

    extraccion = EXTRACCIONES[id_caso]

    ficha["datos_clinicos"].update(
        extraccion["datos_clinicos"]
    )

    ficha["datos_especificos_poblacion"].update(
        extraccion["datos_especificos_poblacion"]
    )

    ficha["estado_extraccion"] = "extraido_pendiente_revision"

    actualizadas.append(id_caso)

if len(actualizadas) != 5:
    raise ValueError(
        f"Se esperaban 5 casos, se encontraron {len(actualizadas)}"
    )

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(fichas, archivo, ensure_ascii=False, indent=2)

print("\n=== EXTRACCIÓN POR POBLACIÓN ===")

for id_caso in actualizadas:
    print(f"{id_caso}: extracción registrada")

print("\nTotal de fichas:", len(fichas))

print(
    "Fichas con extracción:",
    sum(
        ficha["estado_extraccion"] != "pendiente"
        for ficha in fichas
    )
)

print("\nExtracción completada correctamente.")