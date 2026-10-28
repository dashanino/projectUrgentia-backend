import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "casos_estudio_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

poblaciones_revisadas = set()

print("\n=== HISTORIAS CLÍNICAS POR POBLACIÓN ===")

for caso in casos:
    poblacion = caso["poblacion"]

    if poblacion in poblaciones_revisadas:
        continue

    poblaciones_revisadas.add(poblacion)

    print("\n" + "=" * 60)
    print("Caso:", caso["id_caso"])
    print("Población:", poblacion)
    print("Edad:", caso["edad"])
    print("Sexo:", caso["sexo"])
    print("Motivo:", caso["motivo_consulta"])
    print("Historia clínica:", caso["historia_clinica"])
    print(
        "Datos desconocidos:",
        caso.get("datos_clinicos_desconocidos", [])
    )

print("\nPoblaciones encontradas:", len(poblaciones_revisadas))