import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"


def preparar_contexto_paciente(caso):
    desconocidos = caso.get("datos_clinicos_desconocidos", [])

    contexto = {
        "id_caso": caso["id_caso"],
        "poblacion": caso["poblacion"],
        "edad": caso["edad"],
        "sexo": caso["sexo"],
        "motivo_consulta": caso["motivo_consulta"],
        "historia_clinica": caso["historia_clinica"],
        "datos_desconocidos": desconocidos,
        "instrucciones": [
            "Responder únicamente con información documentada.",
            "No inventar síntomas, antecedentes ni signos vitales.",
            "No interpretar ausencia de información como respuesta negativa.",
            "Si la información no está documentada, responder: No lo sé.",
            "No utilizar prioridad_objetivo para construir respuestas.",
            "Responder solamente la pregunta realizada."
        ]
    }

    return contexto


with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

# Caso de prueba: mujer adulta con dolor abdominal
caso_prueba = next(
    caso for caso in casos
    if caso["id_caso"] == "URG-035"
)

contexto = preparar_contexto_paciente(caso_prueba)

print("\n=== CONTEXTO DEL PACIENTE SIMULADO ===")
print(json.dumps(contexto, ensure_ascii=False, indent=2))

print("\nContexto preparado correctamente.")