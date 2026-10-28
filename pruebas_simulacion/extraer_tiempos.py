import json
import re
import unicodedata
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    equivalencias = {
        "un": "1",
        "una": "1",
        "uno": "1",
        "dos": "2",
        "tres": "3",
        "cuatro": "4",
        "cinco": "5",
        "seis": "6",
        "siete": "7",
        "ocho": "8",
        "nueve": "9",
        "diez": "10",
        "quince": "15",
        "veinte": "20",
        "treinta": "30",
        "cuarenta": "40",
        "sesenta": "60"
    }

    for palabra, numero in equivalencias.items():
        texto = re.sub(
            rf"\b{palabra}\b",
            numero,
            texto
        )

    return texto.strip()


NUMEROS = {
    "un": 1, "una": 1, "uno": 1,
    "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7,
    "ocho": 8, "nueve": 9, "diez": 10,
    "quince": 15, "veinte": 20,
    "treinta": 30, "cuarenta": 40,
    "sesenta": 60
}

PATRON = re.compile(
    r"\b(?:desde\s+)?hace\s+"
    r"(\d+|[a-z]+)\s+"
    r"(minutos?|horas?|dias?|semanas?)\b"
)


def extraer_tiempo(historia):
    texto = normalizar(historia)
    coincidencias = PATRON.findall(texto)

    resultados = []

    for numero, unidad in coincidencias:
        if numero.isdigit():
            cantidad = int(numero)
        else:
            cantidad = NUMEROS.get(numero)

        if cantidad is None:
            continue

        resultados.append((cantidad, unidad.rstrip("s")))

    resultados = list(dict.fromkeys(resultados))

    if len(resultados) != 1:
        return None, len(resultados) > 1

    cantidad, unidad = resultados[0]

    unidad_texto = unidad if cantidad == 1 else unidad + "s"

    return f"{cantidad} {unidad_texto}", False


with ARCHIVO.open(encoding="utf-8") as archivo:
    fichas = json.load(archivo)

detectados = 0
agregados = 0
existentes = 0
conflictos = []
ejemplos = []

for ficha in fichas:
    tiempo, ambiguo = extraer_tiempo(ficha["historia_clinica"])

    if ambiguo:
        conflictos.append(
            (ficha["id_caso"], "Múltiples tiempos encontrados")
        )
        continue

    if tiempo is None:
        continue

    detectados += 1

    datos = ficha["datos_clinicos"]

    # Guardamos el tiempo documentado como duración.
    # No inferimos automáticamente la hora exacta de inicio.
    actual = datos.get("duracion")

    if actual is None:
        datos["duracion"] = tiempo
        agregados += 1

    elif normalizar(actual) == normalizar(tiempo):
        existentes += 1

    else:
        conflictos.append(
            (ficha["id_caso"], f"Registrado: {actual}; detectado: {tiempo}")
        )

    if len(ejemplos) < 10:
        ejemplos.append((ficha["id_caso"], tiempo))

print("\n=== EXTRACCIÓN AUTOMÁTICA DE TIEMPOS ===")
print("Fichas totales:", len(fichas))
print("Tiempos únicos detectados:", detectados)
print("Duraciones nuevas:", agregados)
print("Duraciones ya registradas:", existentes)
print("Casos para revisar:", len(conflictos))

print("\nEjemplos:")
for id_caso, tiempo in ejemplos:
    print(f"{id_caso}: {tiempo}")

if conflictos:
    print("\nRevisión necesaria:")
    for id_caso, motivo in conflictos[:20]:
        print(f"{id_caso}: {motivo}")

# No guardar si encontramos conflictos.
if not conflictos:
    with ARCHIVO.open("w", encoding="utf-8") as archivo:
        json.dump(fichas, archivo, ensure_ascii=False, indent=2)

    print("\nExtracción guardada correctamente.")
else:
    print("\nNo se guardaron cambios. Revisaremos los conflictos.")

print("Las fichas mantienen su estado de revisión clínica.")