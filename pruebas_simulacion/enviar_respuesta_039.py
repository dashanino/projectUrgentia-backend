
import json
from pathlib import Path

from simular_urgentia import enviar_primera_respuesta_nn
from respondedor_100 import responder_caso

CARPETA = Path(__file__).resolve().parent

ID_CASO = "URG-039"
ID_PREGUNTA = 144

ARCHIVO_SESION = CARPETA / f"sesion_{ID_CASO}.json"
ARCHIVO_CONTROL = CARPETA / f"control_{ID_CASO}.json"

with ARCHIVO_SESION.open(encoding="utf-8") as archivo:
    paciente = json.load(archivo)

with ARCHIVO_CONTROL.open(encoding="utf-8") as archivo:
    control = json.load(archivo)

if control.get("primera_respuesta_enviada"):
    print("La primera respuesta ya fue enviada.")
    raise SystemExit(0)

if control.get("resultado_reglas", {}).get("accion") != "continuar_ia":
    raise ValueError("El caso no puede continuar a IA.")

if not control.get("sintomas_registrados"):
    raise ValueError("Falta completar la selección de síntomas.")

pregunta = (
    "¿Cuál es el principal motivo por el que deseas acudir "
    "a urgencias? Explícanos brevemente qué te está pasando."
)

respuesta = responder_caso(ID_CASO, pregunta)

if not respuesta or respuesta.strip().lower() in (
    "no lo sé", "no lo se", "no sé", "no se"
):
    raise ValueError("La respuesta necesita revisión.")

print("\n=== ENVIANDO PRIMERA RESPUESTA ===")
print("Caso:", ID_CASO)
print("Pretriaje:", paciente["id_pretriage"])
print("Pregunta:", pregunta)
print("Respuesta:", respuesta)

confirmacion = enviar_primera_respuesta_nn(
    paciente,
    ID_PREGUNTA,
    respuesta
)

if not confirmacion:
    raise RuntimeError(
        "No se confirmó el envío. "
        "Verifica el backend antes de reintentar."
    )

control["primera_respuesta_enviada"] = True
control["primera_pregunta_id"] = ID_PREGUNTA
control["primera_respuesta"] = respuesta

temporal = ARCHIVO_CONTROL.with_suffix(".tmp")

with temporal.open("w", encoding="utf-8") as archivo:
    json.dump(control, archivo, ensure_ascii=False, indent=2)

temporal.replace(ARCHIVO_CONTROL)

print("\nPrimera respuesta enviada y registrada correctamente.")
