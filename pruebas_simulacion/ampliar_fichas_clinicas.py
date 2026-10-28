import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    fichas = json.load(archivo)

CAMPOS_GENERALES = {
    "signos_vitales": {},
    "signos_alarma": [],
    "informacion_adicional": [],
    "fuente_informacion": None
}

CAMPOS_POBLACION = {
    "Niño": {
        "cuidador": None,
        "signos_respiratorios": [],
        "alimentacion_hidratacion": None
    },
    "Adulto": {
        "dolor_toracico": {},
        "estado_conciencia": None
    },
    "Adulto Mayor": {
        "dolor_toracico": {},
        "estado_conciencia": None,
        "riesgo_caidas": None
    },
    "Embarazada": {
        "semanas_gestacion": None,
        "sangrado_vaginal": None,
        "movimientos_fetales": None,
        "contracciones": None
    },
    "Trauma/Accidente": {
        "mecanismo_trauma": None,
        "tiempo_desde_accidente": None,
        "lesiones_identificadas": [],
        "estado_conciencia": None
    }
}

for ficha in fichas:
    datos = ficha["datos_clinicos"]

    for campo, valor in CAMPOS_GENERALES.items():
        if campo not in datos:
            datos[campo] = valor.copy() if isinstance(
                valor, (dict, list)
            ) else valor

    poblacion = ficha["poblacion"]

    if poblacion not in CAMPOS_POBLACION:
        raise ValueError(
            f"Población desconocida en {ficha['id_caso']}: {poblacion}"
        )

    if "datos_especificos_poblacion" not in ficha:
        ficha["datos_especificos_poblacion"] = (
            CAMPOS_POBLACION[poblacion].copy()
        )

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(fichas, archivo, ensure_ascii=False, indent=2)

print("\n=== AMPLIACIÓN DE FICHAS CLÍNICAS ===")
print("Fichas actualizadas:", len(fichas))

for poblacion in CAMPOS_POBLACION:
    cantidad = sum(
        f["poblacion"] == poblacion
        for f in fichas
    )
    print(f"{poblacion}: {cantidad}")

ficha_035 = next(
    f for f in fichas
    if f["id_caso"] == "URG-035"
)

print(
    "\nURG-035 conserva intensidad:",
    ficha_035["datos_clinicos"]["intensidad_dolor"]
)

print(
    "URG-035 conserva estado:",
    ficha_035["estado_extraccion"]
)

print("\nEstructura ampliada correctamente.")