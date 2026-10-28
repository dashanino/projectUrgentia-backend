import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

DATOS_PENDIENTES = {
    "URG-035": ["posibilidad_embarazo"],
    "URG-041": ["posibilidad_embarazo"],
    "URG-053": ["cefalea_nueva_o_diferente"],
    "URG-055": ["uso_anticoagulantes"],
    "URG-071": ["presion_arterial_actual"],
    "URG-089": ["uso_anticoagulantes"],
    "URG-095": ["uso_anticoagulantes"],
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    codigo = caso["id_caso"]

    if codigo in DATOS_PENDIENTES:
        caso["datos_clinicos_desconocidos"] = DATOS_PENDIENTES[codigo]
        caso["prioridad_esperada"] = None
        caso["estado_validacion"] = "pendiente_revision_clinica"

        actualizados.append(codigo)

if set(actualizados) != set(DATOS_PENDIENTES):
    raise ValueError("No se encontraron todos los casos esperados")

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("\n=== DATOS CLÍNICOS DESCONOCIDOS ===")

for codigo in sorted(actualizados):
    print(f"{codigo}: {', '.join(DATOS_PENDIENTES[codigo])}")

print("\nCasos actualizados:", len(actualizados))
print("Total de casos clínicos:", len(casos))
