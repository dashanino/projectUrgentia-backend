
import json
from pathlib import Path

from simular_urgentia import (
    obtener_pregunta_ia,
    guardar_sintomas_nn
)
from respondedor_100 import responder_caso

CARPETA = Path(__file__).resolve().parent
ID_CASO = "URG-039"

ARCHIVO_SESION = CARPETA / f"sesion_{ID_CASO}.json"
ARCHIVO_CONTROL = CARPETA / f"control_{ID_CASO}.json"

with ARCHIVO_SESION.open(encoding="utf-8") as archivo:
    paciente = json.load(archivo)

with ARCHIVO_CONTROL.open(encoding="utf-8") as archivo:
    control = json.load(archivo)

if not control.get("reglas_evaluadas"):
    raise ValueError("Las reglas clínicas no se han evaluado.")

resultado_reglas = control.get("resultado_reglas", {})

if resultado_reglas.get("accion") != "continuar_ia":
    raise ValueError("El caso no está autorizado para continuar a IA.")
# Completar la selección de síntomas una sola vez.
if not control.get("sintomas_registrados", False):

    print("\n=== REGISTRANDO SÍNTOMAS ===")

    archivo_casos = CARPETA / "casos_estudio_100.json"

    with archivo_casos.open(encoding="utf-8") as archivo:
        casos = json.load(archivo)

    caso = next(
        c for c in casos
        if c["id_caso"] == ID_CASO
    )

    if not guardar_sintomas_nn(
        paciente,
        caso["sintomas_ids"]
    ):
        raise RuntimeError(
            "No se confirmó el registro de síntomas. "
            "Revisa el backend antes de reintentar."
        )

    control["sintomas_registrados"] = True

    temporal = ARCHIVO_CONTROL.with_suffix(".tmp")

    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(
            control,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    temporal.replace(ARCHIVO_CONTROL)

    print("Síntomas registrados correctamente.")
print("\n=== PRIMERA PREGUNTA REAL DE IA ===")
print("Caso:", ID_CASO)
print("Pretriaje:", paciente["id_pretriage"])

resultado = obtener_pregunta_ia(paciente)

if not resultado:
    raise RuntimeError("No se recibió respuesta de la IA.")

accion = resultado.get("accion")
print("\nAcción:", accion)

if accion in ("pregunta", "pregunta_pendiente"):
    preguntas = [resultado]
elif accion == "bloque_preguntas":
    preguntas = resultado.get("preguntas", [])
else:
    preguntas = []
    print("Respuesta del sistema:", resultado)

for pregunta in preguntas:
    texto = pregunta.get("pregunta", "")
    respuesta = responder_caso(ID_CASO, texto)

    print("\n-----------------------------")
    print("ID pregunta:", pregunta.get("id_pregunta"))
    print("Pregunta:", texto)
    print("Respuesta propuesta:", respuesta)

    if respuesta.strip().lower() in (
        "no lo sé",
        "no lo se",
        "no sé",
        "no se"
    ):
        print("REQUIERE REVISIÓN DE LA FICHA CLÍNICA")

print("\nNo se enviaron respuestas a la IA.")
print("Solo se consultaron las preguntas y se prepararon respuestas.")
