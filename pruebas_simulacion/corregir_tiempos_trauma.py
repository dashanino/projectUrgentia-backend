import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    fichas = json.load(archivo)

corregidos = []

for ficha in fichas:

    if ficha["poblacion"] != "Trauma/Accidente":
        continue

    datos = ficha["datos_clinicos"]
    especificos = ficha["datos_especificos_poblacion"]

    duracion = datos.get("duracion")

    if not duracion:
        continue

    tiempo_accidente = especificos.get(
        "tiempo_desde_accidente"
    )

    # Si existe un tiempo diferente, no sobrescribirlo.
    if tiempo_accidente and tiempo_accidente != duracion:
        print(
            f"REVISAR {ficha['id_caso']}: "
            f"accidente={tiempo_accidente}, "
            f"duracion={duracion}"
        )
        continue

    especificos["tiempo_desde_accidente"] = duracion

    # No afirmar que la duración del síntoma
    # coincide necesariamente con el accidente.
    datos["duracion"] = None

    # Conservar la procedencia y la razón del ajuste.
    ficha.setdefault("observaciones_extraccion", [])

    ficha["observaciones_extraccion"].append(
        "El tiempo documentado corresponde al evento "
        "traumático. La duración independiente de los "
        "síntomas no está confirmada."
    )

    corregidos.append(ficha["id_caso"])

# Evitar guardar cambios si existe alguna discrepancia.
discrepancias = []

for ficha in fichas:
    if ficha["poblacion"] != "Trauma/Accidente":
        continue

    if (
        ficha["datos_clinicos"].get("duracion")
        and ficha["datos_especificos_poblacion"].get(
            "tiempo_desde_accidente"
        )
    ):
        discrepancias.append(ficha["id_caso"])

if discrepancias:
    print("\nNo se guardaron cambios.")
    print("Casos pendientes:", discrepancias)
else:
    with ARCHIVO.open("w", encoding="utf-8") as archivo:
        json.dump(
            fichas,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    print("\n=== CORRECCIÓN DE TIEMPOS DE TRAUMA ===")
    print("Fichas totales:", len(fichas))
    print("Casos corregidos:", len(corregidos))

    for id_caso in corregidos:
        print(id_caso)

    print("\nCorrección guardada correctamente.")