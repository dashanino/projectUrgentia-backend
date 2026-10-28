import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_FICHAS = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO_CASOS.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

fichas = []

for caso in casos:
    ficha = {
        "id_caso": caso["id_caso"],
        "poblacion": caso["poblacion"],
        "edad": caso["edad"],
        "sexo": caso["sexo"],
        "motivo_consulta": caso["motivo_consulta"],
        "historia_clinica": caso["historia_clinica"],

        "datos_clinicos": {
            "inicio": None,
            "duracion": None,
            "intensidad_dolor": None,
            "localizacion": None,
            "evolucion": None,
            "sintomas_asociados": [],
            "sintomas_negados": [],
            "antecedentes": []
        },

        "datos_desconocidos": caso.get(
            "datos_clinicos_desconocidos", []
        ),

        "estado_extraccion": "pendiente"
    }

    fichas.append(ficha)

if len(fichas) != 100:
    raise ValueError(
        f"Se esperaban 100 fichas y se encontraron {len(fichas)}"
    )

with ARCHIVO_FICHAS.open("w", encoding="utf-8") as archivo:
    json.dump(fichas, archivo, ensure_ascii=False, indent=2)

print("\n=== FICHAS CLÍNICAS URGENTIA ===")
print("Fichas creadas:", len(fichas))
print("Archivo:", ARCHIVO_FICHAS.name)
print("Estado inicial: pendiente de extracción")
print("Historias originales conservadas:", len(fichas))