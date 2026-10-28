
import json
from pathlib import Path

from simular_urgentia import (
    obtener_pregunta_ia,
    enviar_primera_respuesta_nn,
)
from respondedor_100 import responder_por_orden

CARPETA = Path(__file__).resolve().parent
ID_CASO = "URG-039"

ARCHIVO_SESION = CARPETA / f"sesion_{ID_CASO}.json"
ARCHIVO_CONTROL = CARPETA / f"control_{ID_CASO}.json"

with ARCHIVO_SESION.open(encoding="utf-8") as archivo:
    paciente = json.load(archivo)

with ARCHIVO_CONTROL.open(encoding="utf-8") as archivo:
    control = json.load(archivo)

if not control.get("primera_respuesta_enviada"):
    raise ValueError("La primera respuesta aún no está registrada.")

if control.get("bloque_2_5_enviado"):
    print("Este bloque ya fue enviado. No se repetirá.")
    raise SystemExit(0)

print("\n=== CONSULTANDO PREGUNTAS PENDIENTES ===")

resultado = obtener_pregunta_ia(paciente)

if not resultado:
    raise RuntimeError("No se pudieron consultar las preguntas.")

accion = resultado.get("accion")

if accion == "bloque_preguntas":
    preguntas = resultado.get("preguntas", [])

elif accion in ("pregunta", "pregunta_pendiente"):
    preguntas = [resultado]

else:
    print("Estado actual:", resultado)
    print("No se enviaron respuestas.")
    raise SystemExit(0)

ordenes = [p.get("orden") for p in preguntas]

if not preguntas or any(
    orden not in (2, 3, 4, 5)
    for orden in ordenes
):
    raise ValueError(
        f"Preguntas inesperadas: {ordenes}. "
        "No se enviarán respuestas."
    )

if len(ordenes) != len(set(ordenes)):
    raise ValueError("Hay preguntas duplicadas.")


respuestas = []

for pregunta in preguntas:
    orden = pregunta["orden"]
    texto = pregunta["pregunta"]
    respuesta = responder_por_orden(ID_CASO, orden)

    if not respuesta:
        raise ValueError(
            f"No hay respuesta preparada para la pregunta {orden}."
        )

    respuestas.append({
        "id_pregunta": pregunta["id_pregunta"],
        "respuesta": respuesta
    })

    print(f"\nPregunta {orden}: {texto}")
    print(f"Respuesta: {respuesta}")

print("\n=== ENVIANDO BLOQUE A URGENTIA ===")

import requests

respuesta_http = requests.post(
    "http://127.0.0.1:3000/api/pretriage-agent/respuestas",
    headers={
        "Authorization": f"Bearer {paciente['access_token']}"
    },
    json={
        "id_pretriage": paciente["id_pretriage"],
        "respuestas": respuestas
    },
    timeout=60
)

print("HTTP:", respuesta_http.status_code)
print("Resultado:", respuesta_http.text[:1500])

if not respuesta_http.ok:
    raise RuntimeError(
        "El envío no fue confirmado. "
        "Verifica el backend antes de reintentar."
    )

datos = respuesta_http.json()

if datos.get("ok") is not True:
    raise RuntimeError("El backend no confirmó el guardado.")

control.setdefault("preguntas_ia_enviadas", {})

for pregunta, respuesta in zip(preguntas, respuestas):
    control["preguntas_ia_enviadas"][
        str(pregunta["orden"])
    ] = respuesta

control["bloque_2_5_enviado"] = all(
    str(orden) in control["preguntas_ia_enviadas"]
    for orden in (2, 3, 4, 5)
)

temporal = ARCHIVO_CONTROL.with_suffix(".tmp")

with temporal.open("w", encoding="utf-8") as archivo:
    json.dump(control, archivo, ensure_ascii=False, indent=2)

temporal.replace(ARCHIVO_CONTROL)

print("\nRespuestas enviadas y registradas correctamente.")
print("Órdenes enviados:", ordenes)
print(
    "Bloque 2–5 completo:",
    control["bloque_2_5_enviado"]
)
