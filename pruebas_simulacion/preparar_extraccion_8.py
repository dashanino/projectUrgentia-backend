import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

IDS = {
    "URG-004", "URG-005", "URG-007", "URG-008",
    "URG-010", "URG-011", "URG-012", "URG-013",
}

fichas = json.loads(
    (BASE / "fichas_clinicas_100.json").read_text(encoding="utf-8")
)

salida = []

for ficha in fichas:
    if ficha["id_caso"] not in IDS:
        continue

    salida.append({
        "id_caso": ficha["id_caso"],
        "historia_clinica": ficha["historia_clinica"],
        "datos_confirmados": [],
        "datos_negados": [],
        "datos_desconocidos": [],
        "estado_revision": "pendiente",
    })

ruta = BASE / "extraccion_clinica_8.json"

if ruta.exists():
    raise FileExistsError(
        "La extracción ya existe. No se sobrescribirá."
    )

ruta.write_text(
    json.dumps(salida, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)

print("Archivo creado:", ruta)
print("Casos preparados:", len(salida))
print("Estado: pendientes de extracción y revisión.")
print("No se modificaron las fichas originales.")
