import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent

ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_FICHAS = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO_CASOS.open(encoding="utf-8") as archivo:
    casos = json.load(archivo)

with ARCHIVO_FICHAS.open(encoding="utf-8") as archivo:
    fichas = json.load(archivo)

casos_por_id = {
    caso["id_caso"]: caso
    for caso in casos
}

errores = []
advertencias = []

if len(casos) != 100:
    errores.append(f"Se encontraron {len(casos)} casos originales.")

if len(fichas) != 100:
    errores.append(f"Se encontraron {len(fichas)} fichas.")

ids_fichas = [f["id_caso"] for f in fichas]

if len(ids_fichas) != len(set(ids_fichas)):
    errores.append("Hay identificadores de ficha duplicados.")

for ficha in fichas:
    id_caso = ficha["id_caso"]
    original = casos_por_id.get(id_caso)

    if original is None:
        errores.append(f"{id_caso}: no existe en los casos originales.")
        continue

    for campo in [
        "poblacion",
        "edad",
        "sexo",
        "motivo_consulta",
        "historia_clinica"
    ]:
        if ficha.get(campo) != original.get(campo):
            errores.append(f"{id_caso}: cambió el campo {campo}.")

    desconocidos_originales = set(
        original.get("datos_clinicos_desconocidos", [])
    )

    desconocidos_ficha = set(
        ficha.get("datos_desconocidos", [])
    )

    if not desconocidos_originales.issubset(desconocidos_ficha):
        errores.append(
            f"{id_caso}: se perdió información desconocida."
        )

    datos = ficha.get("datos_clinicos", {})

    if not isinstance(datos, dict):
        errores.append(f"{id_caso}: datos_clinicos no es un objeto.")
        continue

    if not isinstance(datos.get("sintomas_negados"), list):
        errores.append(f"{id_caso}: síntomas negados inválidos.")

    if not isinstance(
        ficha.get("datos_especificos_poblacion"), dict
    ):
        errores.append(
            f"{id_caso}: faltan los datos específicos de población."
        )

    if (
        ficha.get("estado_extraccion") != "pendiente"
        and not datos.get("sintomas_asociados")
        and not datos.get("signos_alarma")
    ):
        advertencias.append(
            f"{id_caso}: extracción sin síntomas asociados ni alarmas."
        )

extraidas = [
    f for f in fichas
    if f.get("estado_extraccion") == "extraido_pendiente_revision"
]

pendientes = [
    f for f in fichas
    if f.get("estado_extraccion") == "pendiente"
]

print("\n=== AUDITORÍA DE FICHAS CLÍNICAS ===")
print("Casos originales:", len(casos))
print("Fichas clínicas:", len(fichas))
print("Fichas extraídas:", len(extraidas))
print("Fichas pendientes:", len(pendientes))
print("Errores:", len(errores))
print("Advertencias:", len(advertencias))

for error in errores:
    print("ERROR:", error)

for advertencia in advertencias:
    print("ADVERTENCIA:", advertencia)

if errores:
    print("\nAUDITORÍA: REQUIERE CORRECCIONES")
else:
    print("\nAUDITORÍA ESTRUCTURAL: APROBADA")
    print("Las extracciones aún requieren revisión clínica.")
    