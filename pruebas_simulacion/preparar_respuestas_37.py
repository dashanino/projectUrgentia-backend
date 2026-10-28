import json
from pathlib import Path
from respondedor_100 import responder_caso

BASE = Path(__file__).resolve().parent
plan = json.loads(
    (BASE / "plan_reanudacion_37.json").read_text(encoding="utf-8")
)

salida = []
faltantes = 0

for caso in plan:
    respuestas = []

    for pregunta in caso["preguntas"]:
        texto = pregunta["pregunta"]
        respuesta = responder_caso(caso["id_caso"], texto)

        sin_dato = (
            not isinstance(respuesta, str)
            or not respuesta.strip()
            or respuesta.strip().lower() in (
                "no lo sé.",
                "no lo sé",
                "no lo se.",
                "no lo se",
                "desconocido"
            )
        )

        if sin_dato:
            respuesta = (
                "No se dispone de información clínica documentada "
                "para responder esta pregunta."
            )
            faltantes += 1

        respuestas.append({
            "id_pregunta": pregunta["id_pregunta"],
            "pregunta": texto,
            "respuesta": respuesta,
            "dato_faltante": sin_dato
        })

    salida.append({
        "id_caso": caso["id_caso"],
        "id_pretriage": caso["id_pretriage"],
        "respuestas": respuestas,
        "estado": "preparado_no_enviado"
    })

destino = BASE / "respuestas_preparadas_37.json"
destino.write_text(
    json.dumps(salida, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Casos preparados:", len(salida))
print("Respuestas generadas:", sum(len(c["respuestas"]) for c in salida))
print("Respuestas sin dato clínico:", faltantes)
print("Archivo:", destino)
print("No se enviaron respuestas al backend.")
