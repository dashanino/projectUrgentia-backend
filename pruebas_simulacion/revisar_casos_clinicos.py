import json
from pathlib import Path

RUTA = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS_REVISAR = [
    "URG-029",
    "URG-035",
    "URG-039",
    "URG-041",
    "URG-050",
    "URG-053",
    "URG-055",
    "URG-071",
    "URG-089",
    "URG-095",
    "URG-101",
]

with RUTA.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

por_id = {caso["id_caso"]: caso for caso in casos}

print("\n=== REVISIÓN CLÍNICA PRELIMINAR ===")

for codigo in CASOS_REVISAR:
    caso = por_id.get(codigo)

    if caso is None:
        print(f"\nERROR: No se encontró {codigo}")
        continue

    print(f"\n{'=' * 55}")
    print("CASO:", codigo)
    print("POBLACIÓN:", caso["poblacion"])
    print("PRIORIDAD OBJETIVO:", caso["prioridad_objetivo"])
    print("EDAD:", caso["edad"])
    print("BANDERAS:", caso["banderas_ids"])
    print("MOTIVO:", caso["motivo_consulta"])
    print("HISTORIA:", caso["historia_clinica"])

print(f"\nCasos solicitados para revisión: {len(CASOS_REVISAR)}")