import json
from pathlib import Path

from probar_respuestas_ficha import responder_desde_ficha

CARPETA = Path(__file__).resolve().parent

with (CARPETA / "fichas_clinicas_100.json").open(
    encoding="utf-8"
) as archivo:
    fichas = json.load(archivo)

ficha = next(
    f for f in fichas
    if f["id_caso"] == "URG-035"
)

pruebas = [
    {
        "pregunta": "¿Tiene fiebre o vómitos?",
        "esperada": "No he tenido fiebre ni vómitos."
    },
    {
        "pregunta": "¿Cuánto tiempo lleva con dolor?",
        "esperada": "Cinco horas"
    },
    {
        "pregunta": "¿Ha tenido fiebre anteriormente?",
        "esperada": "No lo sé."
    },
    {
        "pregunta": "¿Es posible que esté embarazada?",
        "esperada": "No lo sé."
    },
    {
        "pregunta": "¿Qué intensidad tiene el dolor?",
        "esperada": "El dolor es de 4/10."
    }
]

print("\n=== AUDITORÍA DE RESPUESTAS ===")

aciertos = 0

for prueba in pruebas:
    obtenida = responder_desde_ficha(
        ficha,
        prueba["pregunta"]
    )

    correcta = obtenida == prueba["esperada"]

    if correcta:
        aciertos += 1

    print(f"\nPregunta: {prueba['pregunta']}")
    print(f"Esperada: {prueba['esperada']}")
    print(f"Obtenida: {obtenida}")
    print("Resultado:", "CORRECTO" if correcta else "REVISAR")

print(f"\nCoincidencias: {aciertos}/{len(pruebas)}")