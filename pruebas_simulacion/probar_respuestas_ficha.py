import json
import unicodedata
from pathlib import Path


ARCHIVO = (
    Path(__file__).resolve().parent
    / "fichas_clinicas_100.json"
)


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())

    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


def responder_desde_ficha(ficha, pregunta):
    p = normalizar(pregunta)
    datos = ficha["datos_clinicos"]

    negados = {
        normalizar(sintoma)
        for sintoma in datos.get("sintomas_negados", [])
    }

    # 1. Preguntas sobre antecedentes o eventos pasados.
    # No debemos interpretar síntomas actuales como antecedentes.
    if any(
        palabra in p
        for palabra in [
            "anteriormente",
            "alguna vez",
            "en el pasado",
            "antecedente",
            "antes de este episodio"
        ]
    ):
        return "No lo sé."

    # 2. Información desconocida explícita.
    if "embaraz" in p:
        return "No lo sé."

    # 3. Preguntas compuestas.
    if "fiebre" in p and "vomit" in p:
        if "fiebre" in negados and "vomitos" in negados:
            return "No he tenido fiebre ni vómitos."

        return "No lo sé."

    # Otras preguntas compuestas no están implementadas.
    # Es más seguro reconocer la limitación.
    if " o " in f" {p} " or " y " in f" {p} ":
        return "No lo sé."

    # 4. Intensidad del dolor.
    if "intensidad" in p or "escala" in p:
        valor = datos.get("intensidad_dolor")

        return (
            f"El dolor es de {valor}."
            if valor
            else "No lo sé."
        )

    # 5. Duración.
    if (
        "cuanto tiempo" in p
        or "hace cuanto" in p
        or "cuantas horas" in p
    ):
        return datos.get("duracion") or "No lo sé."

    # 6. Inicio.
    if "cuando" in p and any(
        palabra in p
        for palabra in ["comenz", "empez", "inicio"]
    ):
        return datos.get("inicio") or "No lo sé."

    # 7. Localización.
    if "donde" in p and any(
        palabra in p
        for palabra in ["dolor", "duele"]
    ):
        return datos.get("localizacion") or "No lo sé."

    # 8. Síntomas negados.
    if "vomit" in p:
        if "vomitos" in negados:
            return "No he tenido vómitos."

        return "No lo sé."

    if "fiebre" in p:
        if "fiebre" in negados:
            return "No he tenido fiebre."

        return "No lo sé."

    # 9. Información no documentada.
    return "No lo sé."


if __name__ == "__main__":

    with ARCHIVO.open(encoding="utf-8") as archivo:
        fichas = json.load(archivo)

    ficha = next(
        f for f in fichas
        if f["id_caso"] == "URG-035"
    )

    preguntas = [
        "¿Qué intensidad tiene el dolor?",
        "¿Existe posibilidad de embarazo?",
        "¿Ha presentado vómitos?",
        "¿Cuándo comenzó el dolor?",
        "¿Dónde le duele?",
        "¿Tiene fiebre?",
        "¿Tiene alergias a medicamentos?"
    ]

    print("\n=== RESPUESTAS DESDE FICHA CLÍNICA ===")

    for pregunta in preguntas:
        respuesta = responder_desde_ficha(ficha, pregunta)

        print(f"\nPregunta: {pregunta}")
        print(f"Respuesta: {respuesta!r}")

        assert respuesta.strip(), "Respuesta vacía"

    print("\nPrueba completada correctamente.")