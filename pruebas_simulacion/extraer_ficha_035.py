import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    fichas = json.load(archivo)

encontrado = False

for ficha in fichas:
    if ficha["id_caso"] == "URG-035":

        ficha["datos_clinicos"] = {
            "inicio": "Hace cinco horas",
            "duracion": "Cinco horas",
            "intensidad_dolor": "4/10",
            "localizacion": "Abdomen, sin localización específica",
            "evolucion": "Intermitente, sin empeoramiento",
            "sintomas_asociados": [
                "Dolor abdominal tipo cólico"
            ],
            "sintomas_negados": [
                "Fiebre",
                "Vómitos",
                "Sangrado",
                "Síntomas urinarios"
            ],
            "antecedentes": []
        }

        ficha["datos_desconocidos"] = [
            "posibilidad_embarazo"
        ]

        ficha["estado_extraccion"] = "extraido_pendiente_revision"

        encontrado = True
        print(json.dumps(ficha, ensure_ascii=False, indent=2))
        break

if not encontrado:
    raise ValueError("No se encontró URG-035")

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(fichas, archivo, ensure_ascii=False, indent=2)

print("\nURG-035: extracción registrada correctamente.")
print("Fichas totales:", len(fichas))
print(
    "Fichas con extracción:",
    sum(
        f["estado_extraccion"] != "pendiente"
        for f in fichas
    )
)