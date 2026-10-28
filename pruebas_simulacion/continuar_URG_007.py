import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

base = Path("pruebas_simulacion")
sesion = json.loads((base / "sesion_URG-007.json").read_text(encoding="utf-8"))
registro_path = base / "respuestas_supervisadas_URG-007.json"
registro = json.loads(registro_path.read_text(encoding="utf-8"))

if sesion["id_pretriage"] != 168 or registro["id_pretriage"] != 168:
    raise SystemExit("ERROR: ID de pretriaje inconsistente.")

if registro.get("estado") in ("envio_incierto", "error_http"):
    raise SystemExit("Hay un envío incierto. Revisar antes de continuar.")

preguntas = [
    (216, "¿Qué edad tiene el niño y desde cuándo comenzó el dolor abdominal?",
     "El niño tiene 9 años y el dolor comenzó hace aproximadamente 8 horas."),
    (217, "¿Dónde duele, se desplazó y qué intensidad tiene?",
     "Comenzó alrededor del ombligo, se desplazó a la parte inferior derecha y tiene intensidad de 7/10."),
    (218, "¿Vómitos, diarrea, fiebre o sangre?",
     "Presenta náuseas y pérdida del apetito. No se reporta sangrado. No hay información confirmada sobre vómitos, diarrea o fiebre."),
    (219, "¿Abdomen duro, sensibilidad o dificultad para caminar?",
     "Presenta dolor al caminar. No hay información confirmada sobre rigidez o sensibilidad abdominal.")
]

enviadas = {
    x.get("id_pregunta")
    for x in registro["interacciones"]
    if x.get("evento") == "respuesta_confirmada"
}
if any(pid in enviadas for pid, _, _ in preguntas):
    raise SystemExit("Una de estas preguntas ya figura como enviada. No se duplicará.")

respuestas = []

for pid, pregunta, sugerencia in preguntas:
    print(f"\nPREGUNTA {pid}: {pregunta}")
    print("Sugerencia:", sugerencia)
    texto = input("Respuesta (Enter acepta sugerencia, /salir cancela): ").strip()
    if texto == "/salir":
        raise SystemExit("Cancelado sin enviar.")
    respuestas.append({"id_pregunta": pid, "respuesta": texto or sugerencia})

print("\nRESPUESTAS QUE SE ENVIARÁN:")
print(json.dumps(respuestas, ensure_ascii=False, indent=2))

if input("\nConfirmar envío de las 4 respuestas [S/n]: ").strip() != "S":
    raise SystemExit("Cancelado sin enviar.")

def guardar():
    registro_path.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

registro["estado"] = "envio_incierto"
registro["interacciones"].append({
    "evento": "intento_envio_bloque",
    "respuestas": respuestas,
    "fecha": datetime.now(timezone.utc).isoformat()
})
guardar()

# Usa la URL del simulador existente, sin modificar el backend.
import sys
sys.path.insert(0, str(base.resolve()))
from simular_urgentia import BASE_URL

inicio = time.perf_counter()
try:
    respuesta = requests.post(
        f"{BASE_URL}/api/pretriage-agent/respuestas",
        headers={"Authorization": f"Bearer {sesion['access_token']}"},
        json={"id_pretriage": 168, "respuestas": respuestas},
        timeout=75
    )
    duracion = round(time.perf_counter() - inicio, 4)

    try:
        resultado = respuesta.json()
    except ValueError:
        resultado = {"mensaje": "Respuesta no JSON", "http": respuesta.status_code}

    confirmado = respuesta.ok and (
        resultado.get("resultado", {}).get("respuestas_guardadas") == 4
        or resultado.get("respuestas_guardadas") == 4
    )

    registro["interacciones"].append({
        "evento": "respuesta_bloque_confirmada" if confirmado else "envio_bloque_por_conciliar",
        "ids_preguntas": [216, 217, 218, 219],
        "http": respuesta.status_code,
        "duracion_seg": duracion,
        "resultado": resultado,
        "fecha": datetime.now(timezone.utc).isoformat()
    })
    registro["estado"] = "revision_seguridad" if confirmado else "envio_incierto"
    guardar()

    print("\nHTTP:", respuesta.status_code)
    print("Duración:", duracion, "segundos")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    if not confirmado:
        print("\nATENCIÓN: no se pudo confirmar que se guardaran las cuatro respuestas. No reintentar sin revisar la BD.")

except requests.RequestException as error:
    registro["interacciones"].append({
        "evento": "envio_bloque_no_confirmado",
        "error": str(error),
        "fecha": datetime.now(timezone.utc).isoformat()
    })
    guardar()
    print("Envío incierto:", error)
    print("No repetir sin conciliar con la base de datos.")
