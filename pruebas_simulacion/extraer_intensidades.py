import json
import re
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    fichas = json.load(archivo)

detectadas = 0
agregadas = 0
ya_registradas = 0
conflictos = []
ejemplos = []

for ficha in fichas:
    historia = ficha["historia_clinica"]

    # Buscar intensidades explícitas de 0/10 a 10/10.
    coincidencias = re.findall(
        r"(?<!\d)(?:10|[0-9])\s*/\s*10(?!\d)",
        historia
    )

    valores = list(dict.fromkeys(
        re.sub(r"\s+", "", valor)
        for valor in coincidencias
    ))

    if not valores:
        continue

    detectadas += 1

    # Si aparecen distintas intensidades, no elegimos una.
    if len(valores) > 1:
        conflictos.append(ficha["id_caso"])
        continue

    intensidad = valores[0]
    actual = ficha["datos_clinicos"].get("intensidad_dolor")

    if actual is None:
        ficha["datos_clinicos"]["intensidad_dolor"] = intensidad
        agregadas += 1

    elif actual == intensidad:
        ya_registradas += 1

    else:
        conflictos.append(ficha["id_caso"])
        continue

    if len(ejemplos) < 10:
        ejemplos.append((ficha["id_caso"], intensidad))

# Guardar solo si no hay conflictos.
if not conflictos:
    with ARCHIVO.open("w", encoding="utf-8") as archivo:
        json.dump(fichas, archivo, ensure_ascii=False, indent=2)

print("\n=== EXTRACCIÓN AUTOMÁTICA DE INTENSIDADES ===")
print("Fichas totales:", len(fichas))
print("Historias con intensidad detectada:", detectadas)
print("Intensidades nuevas agregadas:", agregadas)
print("Intensidades ya registradas:", ya_registradas)
print("Conflictos:", len(conflictos))

print("\nEjemplos:")
for id_caso, intensidad in ejemplos:
    print(f"{id_caso}: {intensidad}")

if conflictos:
    print("\nNo se guardaron cambios por conflictos:")
    for id_caso in conflictos:
        print("-", id_caso)
else:
    print("\nExtracción guardada correctamente.")

print(
    "Nota: las fichas pendientes siguen pendientes "
    "de extracción y revisión clínica."
)