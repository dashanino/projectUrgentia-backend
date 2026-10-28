import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent
SALIDA = BASE / "plan_reanudacion_37.json"

def leer(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))

plan = []
resumen = Counter()

for ruta in sorted(BASE.glob("resultado_automatico_URG-*.json")):
    registro = leer(ruta)

    if registro.get("estado") != "requiere_dato_clinico":
        continue

    caso = registro["id_caso"]
    eventos = registro.get("interacciones", [])

    respuestas_confirmadas = [
        e for e in eventos
        if e.get("evento") == "resultado_http"
        and e.get("codigo_http") == 200
        and isinstance(e.get("respuesta_backend"), dict)
        and e["respuesta_backend"].get("ok") is True
    ]

    consultas = [
        e for e in eventos
        if e.get("evento") == "consulta_siguiente_pregunta"
        and e.get("codigo_http") == 200
    ]

    if len(respuestas_confirmadas) != 1 or not consultas:
        resumen["requiere_revision"] += 1
        continue

    respuesta = consultas[-1]["respuesta_backend"]
    resultado = respuesta.get("resultado", {})

    if resultado.get("accion") != "bloque_preguntas":
        resumen["requiere_revision"] += 1
        continue

    preguntas = resultado.get("preguntas", [])

    if not preguntas or any(
        not isinstance(p.get("id_pregunta"), int)
        or not p.get("pregunta")
        for p in preguntas
    ):
        resumen["requiere_revision"] += 1
        continue

    plan.append({
        "id_caso": caso,
        "id_pretriage": registro["id_pretriage"],
        "preguntas": preguntas,
        "respuestas_confirmadas_previas": 1,
        "estado": "listo_para_preparar_respuestas"
    })

    resumen["preparados"] += 1

SALIDA.write_text(
    json.dumps(plan, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Casos preparados:", resumen["preparados"])
print("Casos que requieren revisión:", resumen["requiere_revision"])
print("Archivo:", SALIDA)
print("Preguntas pendientes:", sum(len(x["preguntas"]) for x in plan))
print("No se enviaron solicitudes HTTP.")
