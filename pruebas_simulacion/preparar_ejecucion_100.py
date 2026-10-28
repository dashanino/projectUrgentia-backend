import json
import csv
from pathlib import Path
from collections import Counter

CARPETA = Path(__file__).resolve().parent

ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_FICHAS = CARPETA / "fichas_clinicas_100.json"
ARCHIVO_PLAN = CARPETA / "plan_ejecucion_100.json"
ARCHIVO_RESULTADOS = CARPETA / "resultados_evaluacion_100.csv"

with ARCHIVO_CASOS.open(encoding="utf-8") as archivo:
    casos = json.load(archivo)

with ARCHIVO_FICHAS.open(encoding="utf-8") as archivo:
    fichas = json.load(archivo)

fichas_por_id = {
    ficha["id_caso"]: ficha
    for ficha in fichas
}

if len(casos) != 100:
    raise ValueError("Se esperaban exactamente 100 casos.")

if len(fichas_por_id) != 100:
    raise ValueError("Se esperaban 100 fichas únicas.")

plan = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso not in fichas_por_id:
        raise ValueError(f"Falta la ficha de {id_caso}")

    ficha = fichas_por_id[id_caso]

    plan.append({
        "id_caso": id_caso,
        "poblacion": caso["poblacion"],
        "prioridad_objetivo": caso["prioridad_objetivo"],
        "prioridad_esperada": caso.get("prioridad_esperada"),
        "estado_validacion": caso.get(
            "estado_validacion",
            "pendiente_revision_clinica"
        ),
        "estado_extraccion": ficha["estado_extraccion"],
        "estado_simulacion": "pendiente",
        "id_pretriage": None,
        "ruta_sistema": None,
        "prioridad_ia": None,
        "accion_sistema": None,
        "numero_preguntas": 0,
        "error": None
    })

# No sobrescribir un plan que pudiera contener avances.
if ARCHIVO_PLAN.exists():
    raise FileExistsError(
        "Ya existe plan_ejecucion_100.json. "
        "No se sobrescribió para proteger los avances."
    )

with ARCHIVO_PLAN.open("w", encoding="utf-8") as archivo:
    json.dump(plan, archivo, ensure_ascii=False, indent=2)

COLUMNAS = [
    "id_caso",
    "poblacion",
    "prioridad_objetivo",
    "prioridad_esperada",
    "estado_validacion",
    "ruta_sistema",
    "accion_sistema",
    "prioridad_ia",
    "numero_preguntas",
    "estado_simulacion",
    "error"
]

# Crear el CSV vacío sin sobrescribir resultados anteriores.
with ARCHIVO_RESULTADOS.open(
    "x",
    encoding="utf-8",
    newline=""
) as archivo:
    escritor = csv.DictWriter(
        archivo,
        fieldnames=COLUMNAS
    )
    escritor.writeheader()

distribucion = Counter(
    caso["poblacion"]
    for caso in plan
)

print("\n=== PLAN DE SIMULACIONES URGENTIA ===")
print("Casos preparados:", len(plan))

for poblacion, cantidad in sorted(distribucion.items()):
    print(f"{poblacion}: {cantidad}")

print("\nArchivos creados:")
print("-", ARCHIVO_PLAN.name)
print("-", ARCHIVO_RESULTADOS.name)

print("\nSimulaciones ejecutadas: 0")
print("No se realizaron solicitudes al backend.")
print("Plan preparado correctamente.")