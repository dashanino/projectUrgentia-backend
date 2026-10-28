import json
from pathlib import Path
from collections import Counter

RUTA = Path(__file__).resolve().parent / "casos_estudio_100.json"

BANDERAS_PERMITIDAS = {
    1: {2, 3, 4, 5, 6},
    2: {2, 3, 4, 5, 6},
    3: {2, 3, 4, 5, 6, 7},
    4: {2, 4, 8, 9, 10, 11, 12, 13, 14},
    5: {3, 4, 5, 15, 16, 17, 18, 19, 20},
}

# Corrección: la bandera 2 no está habilitada
# para embarazadas en el catálogo revisado.
BANDERAS_PERMITIDAS[4].discard(2)

PRIORIDADES = {"alta", "media_alta", "media_baja", "baja"}

with RUTA.open(encoding="utf-8") as archivo:
    casos = json.load(archivo)

errores = []
advertencias = []
ids = []

for caso in casos:
    codigo = caso.get("id_caso", "SIN_ID")
    ids.append(codigo)

    poblacion = caso.get("poblacion_id")
    prioridad = caso.get("prioridad_objetivo")
    banderas = caso.get("banderas_ids", [])

    if poblacion not in BANDERAS_PERMITIDAS:
        errores.append(f"{codigo}: población inválida")
        continue

    if prioridad not in PRIORIDADES:
        errores.append(f"{codigo}: prioridad objetivo inválida")

    if not caso.get("historia_clinica"):
        errores.append(f"{codigo}: historia clínica vacía")

    if not isinstance(banderas, list):
        errores.append(f"{codigo}: banderas_ids no es una lista")
        continue

    for bandera in banderas:
        if bandera not in BANDERAS_PERMITIDAS[poblacion]:
            errores.append(
                f"{codigo}: bandera {bandera} no permitida "
                f"para población {poblacion}"
            )

    if not banderas:
        advertencias.append(
            f"{codigo}: sin banderas rojas seleccionadas; "
            "verificar que el flujo NN permita continuar"
        )

    if caso.get("prioridad_esperada") is None:
        advertencias.append(
            f"{codigo}: prioridad esperada pendiente de revisión clínica"
        )

repetidos = [
    codigo for codigo, cantidad in Counter(ids).items()
    if cantidad > 1
]

for codigo in repetidos:
    errores.append(f"{codigo}: identificador duplicado")

print("\n=== AUDITORÍA DE CASOS URGENTIA ===")
print("Total de casos:", len(casos))
print("Identificadores únicos:", len(set(ids)))
print("Historias clínicas completas:",
      sum(bool(c.get("historia_clinica")) for c in casos))

print("\nDistribución por población:")
for poblacion, cantidad in sorted(
    Counter(c.get("poblacion_id") for c in casos).items()
):
    print(f"  Población {poblacion}: {cantidad}")

print("\nDistribución por prioridad objetivo:")
for prioridad, cantidad in sorted(
    Counter(c.get("prioridad_objetivo") for c in casos).items()
):
    print(f"  {prioridad}: {cantidad}")

print("\nERRORES:", len(errores))
for error in errores:
    print("  ERROR:", error)

print("\nADVERTENCIAS:", len(advertencias))
for advertencia in advertencias:
    print("  AVISO:", advertencia)

print("\nAuditoría terminada.")