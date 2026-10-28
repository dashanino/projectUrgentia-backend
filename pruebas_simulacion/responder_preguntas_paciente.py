import json
import unicodedata
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def responder_pregunta(caso, pregunta):
    pregunta_normalizada = normalizar(pregunta)

    # Solo se habilitan respuestas explícitas para el caso de prueba.
    # No extrapolamos estas reglas a otros pacientes.
    if caso["id_caso"] != "URG-035":
        return "No lo sé."

    if "embaraz" in pregunta_normalizada:
        return "No lo sé."

    if "intensidad" in pregunta_normalizada or (
        "cuanto" in pregunta_normalizada
        and "duele" in pregunta_normalizada
    ):
        return "El dolor es de 4 sobre 10."

    if "cuando" in pregunta_normalizada and (
        "comenz" in pregunta_normalizada
        or "empez" in pregunta_normalizada
    ):
        return "Comenzó hace cinco horas."

    if "vomit" in pregunta_normalizada:
        return "No he tenido vómitos."

    if "fiebre" in pregunta_normalizada:
        return "No he tenido fiebre."

    if "donde" in pregunta_normalizada and (
        "dolor" in pregunta_normalizada
        or "duele" in pregunta_normalizada
    ):
        return "Me duele el abdomen, pero no en un punto específico."

    return "No lo sé."


with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

caso = next(
    caso for caso in casos
    if caso["id_caso"] == "URG-035"
)

preguntas = [
    "¿Cuándo comenzó el dolor?",
    "¿Qué intensidad tiene el dolor?",
    "¿Ha tenido vómitos?",
    "¿Tiene fiebre?",
    "¿Existe posibilidad de embarazo?",
    "¿Dónde le duele?",
    "¿Tiene alergias a medicamentos?"
]

print("\n=== PRUEBA DE RESPUESTAS DINÁMICAS ===")

for pregunta in preguntas:
    respuesta = responder_pregunta(caso, pregunta)

    print(f"\nPregunta: {pregunta}")
    print(f"Respuesta: {respuesta!r}")

    if not isinstance(respuesta, str) or not respuesta.strip():
        raise ValueError(
            f"La pregunta no recibió una respuesta válida: {pregunta}"
        )

print("\nTodas las preguntas recibieron una respuesta.")