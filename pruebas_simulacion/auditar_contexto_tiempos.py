import json
import re
import unicodedata
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


PATRON = re.compile(
    r"\b(?:desde\s+)?hace\s+"
    r"(?:\d+|[a-z]+)\s+"
    r"(?:minutos?|horas?|dias?|semanas?)\b"
)

with ARCHIVO.open(encoding="utf-8") as archivo:
    fichas = json.load(archivo)

revisiones = []
sin_duracion = []

for ficha in fichas:
    duracion = ficha["datos_clinicos"].get("duracion")

    if not duracion:
        sin_duracion.append(ficha["id_caso"])
        continue

    historia = ficha["historia_clinica"]
    historia_normalizada = normalizar(historia)

    coincidencias = list(PATRON.finditer(historia_normalizada))

    contextos = []

    for coincidencia in coincidencias:
        inicio = max(0, coincidencia.start() - 75)
        fin = min(
            len(historia_normalizada),
            coincidencia.end() + 75
        )

        contextos.append(
            historia[inicio:fin].strip()
        )

    revisiones.append({
        "id_caso": ficha["id_caso"],
        "poblacion": ficha["poblacion"],
        "duracion": duracion,
        "contextos": contextos,
        "historia": historia
    })

print("\n=== AUDITORÍA DE CONTEXTO TEMPORAL ===")
print("Fichas totales:", len(fichas))
print("Fichas con duración:", len(revisiones))
print("Fichas sin duración:", len(sin_duracion))

print("\n=== CASOS DE TRAUMA ===")

for revision in revisiones:
    if revision["poblacion"] != "Trauma/Accidente":
        continue

    print("\n" + "-" * 55)
    print("Caso:", revision["id_caso"])
    print("Duración:", revision["duracion"])
    print("Historia:", revision["historia"])

print("\n=== OTROS EJEMPLOS ===")

otros = [
    r for r in revisiones
    if r["poblacion"] != "Trauma/Accidente"
]

for revision in otros[:5]:
    print("\n" + "-" * 55)
    print("Caso:", revision["id_caso"])
    print("Duración:", revision["duracion"])
    print("Historia:", revision["historia"])

print("\n=== CASOS SIN DURACIÓN ===")
print(", ".join(sin_duracion) if sin_duracion else "Ninguno")

print("\nAuditoría de lectura completada.")