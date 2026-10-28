import csv
import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent

ARCHIVO_CONTROL = CARPETA / "control_URG-002.json"
ARCHIVO_PLAN = CARPETA / "plan_ejecucion_100.json"
ARCHIVO_CSV = CARPETA / "resultados_evaluacion_100.csv"

with ARCHIVO_CONTROL.open(encoding="utf-8") as archivo:
    control = json.load(archivo)

with ARCHIVO_PLAN.open(encoding="utf-8") as archivo:
    plan = json.load(archivo)

resultado = control.get("resultado_reglas")

if not control.get("reglas_evaluadas") or not resultado:
    raise ValueError("No existe una evaluación confirmada.")

if (
    resultado.get("accion") != "alerta"
    or resultado.get("origen") != "reglas"
    or resultado.get("alta_prioridad") is not True
):
    raise ValueError("Resultado distinto al esperado. Revisar.")

registro = next(
    r for r in plan
    if r["id_caso"] == "URG-002"
)

if registro["id_pretriage"] != control["id_pretriage"]:
    raise ValueError("El ID del pretriaje no coincide.")

if registro["estado_simulacion"] == "completado":
    print("URG-002 ya está registrado. No se duplicó.")
    raise SystemExit(0)

if registro["estado_simulacion"] != "iniciado":
    raise ValueError("Estado inesperado del caso.")

with ARCHIVO_CSV.open(
    "r", encoding="utf-8", newline=""
) as archivo:
    lector = csv.DictReader(archivo)
    columnas = lector.fieldnames
    filas = list(lector)

if not columnas:
    raise ValueError("El CSV no tiene encabezados.")

if any(f["id_caso"] == "URG-002" for f in filas):
    raise ValueError(
        "URG-002 ya aparece en el CSV. Revisar antes de continuar."
    )

registro["ruta_sistema"] = "reglas"
registro["accion_sistema"] = "alerta"
registro["prioridad_ia"] = None
registro["numero_preguntas"] = 0
registro["estado_simulacion"] = "completado"
registro["error"] = None

fila = {
    columna: registro.get(columna)
    for columna in columnas
}

filas.append(fila)

# Primero guardar el CSV. Si el proceso se interrumpe,
# una nueva ejecución detectará el registro existente.
temporal_csv = ARCHIVO_CSV.with_suffix(".tmp")

with temporal_csv.open(
    "w", encoding="utf-8", newline=""
) as archivo:
    escritor = csv.DictWriter(
        archivo, fieldnames=columnas
    )
    escritor.writeheader()
    escritor.writerows(filas)

temporal_csv.replace(ARCHIVO_CSV)

temporal_plan = ARCHIVO_PLAN.with_suffix(".tmp")

with temporal_plan.open("w", encoding="utf-8") as archivo:
    json.dump(
        plan, archivo, ensure_ascii=False, indent=2
    )

temporal_plan.replace(ARCHIVO_PLAN)

print("\n=== RESULTADO REGISTRADO ===")
print("Caso: URG-002")
print("Pretriaje:", control["id_pretriage"])
print("Ruta: reglas")
print("Acción: alerta")
print("Clasificación IA: no aplica")
print("Estado: completado")
print("Casos completados:", sum(
    r["estado_simulacion"] == "completado"
    for r in plan
))