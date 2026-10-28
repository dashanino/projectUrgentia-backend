import json
import re
import unicodedata
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "fichas_clinicas_100.json"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


def cargar_fichas():
    with ARCHIVO.open(encoding="utf-8") as archivo:
        fichas = json.load(archivo)

    return {
        ficha["id_caso"]: ficha
        for ficha in fichas
    }


def texto_valido(valor):
    if valor is None or valor == "":
        return None

    if isinstance(valor, list):
        return ", ".join(map(str, valor)) if valor else None

    if isinstance(valor, dict):
        return None

    return str(valor)


def responder_desde_ficha(ficha, pregunta):
    p = normalizar(pregunta)
    datos = ficha.get("datos_clinicos", {})
    especificos = ficha.get("datos_especificos_poblacion", {})
    historia = ficha.get("historia_clinica", "")
        # Reconocer preguntas sobre el motivo principal de consulta.
    pregunta_normalizada = pregunta.lower()

    preguntas_motivo = (
        "principal motivo",
        "motivo de consulta",
        "por qué deseas acudir",
        "por que deseas acudir",
        "qué te está pasando",
        "que te esta pasando",
        "qué te ocurre",
        "que te ocurre",
        "qué te trae",
        "que te trae",
    )

    if any(
        expresion in pregunta_normalizada
        for expresion in preguntas_motivo
    ):
        motivo = ficha.get("motivo_consulta")

        if motivo:
            return motivo

        historia = ficha.get("historia_clinica")

        if historia:
            return historia
    # Preguntas sobre duración de síntomas.
    if any(x in p for x in [
        "cuanto tiempo",
        "hace cuanto",
        "cuantas horas",
        "desde cuando"
    ]):
        # En trauma no confundir el accidente con
        # el comienzo de los síntomas.
        if (
            ficha.get("poblacion") == "Trauma/Accidente"
            and any(x in p for x in [
                "accidente", "caida", "golpe",
                "lesion", "quemadura", "colision"
            ])
        ):
            return (
                texto_valido(
                    especificos.get("tiempo_desde_accidente")
                )
                or "No lo sé."
            )

        return texto_valido(datos.get("duracion")) or "No lo sé."

    # Intensidad.
    if "intensidad" in p or "escala" in p:
        return (
            texto_valido(datos.get("intensidad_dolor"))
            or "No lo sé."
        )

    # Localización.
    if "donde" in p and any(
        x in p for x in ["dolor", "duele", "molestia"]
    ):
        return (
            texto_valido(datos.get("localizacion"))
            or "No lo sé."
        )

    # Evolución.
    if any(x in p for x in [
        "empeorado", "empeora", "mejorado",
        "evolucion", "progresado"
    ]):
        return (
            texto_valido(datos.get("evolucion"))
            or "No lo sé."
        )

    # Inicio.
    if "cuando" in p and any(
        x in p for x in ["comenzo", "empezo", "inicio"]
    ):
        return (
            texto_valido(datos.get("inicio"))
            or "No lo sé."
        )

    # Antecedentes.
    if any(x in p for x in [
        "antecedentes", "enfermedades previas",
        "cirugias anteriores"
    ]):
        return (
            texto_valido(datos.get("antecedentes"))
            or "No lo sé."
        )

    # Embarazo: usar datos documentados.
    if "embaraz" in p or "gestacion" in p:
        if ficha.get("poblacion") == "Embarazada":
            semanas = especificos.get("semanas_gestacion")
            if semanas:
                return f"Estoy embarazada de {semanas} semanas."
            return "Estoy embarazada."

        return "No lo sé."

    # Preguntas sobre síntomas específicos:
    # no inferir presencia o ausencia a partir
    # de que una palabra aparezca en la historia.
    sintomas_negados = datos.get("sintomas_negados") or []
    sintomas_asociados = datos.get("sintomas_asociados") or []

    if isinstance(sintomas_negados, str):
        sintomas_negados = [sintomas_negados]

    if isinstance(sintomas_asociados, str):
        sintomas_asociados = [sintomas_asociados]

    sintomas = {
        "fiebre": ["fiebre"],
        "vomitos": ["vomito", "vomitos"],
        "nauseas": ["nausea", "nauseas"],
        "sangrado": ["sangrado", "hemorragia"],
        "dificultad respiratoria": [
            "dificultad respiratoria", "disnea"
        ],
        "mareo": ["mareo", "mareos"]
    }

    coincidencias = []

    for nombre, variantes in sintomas.items():
        if any(v in p for v in variantes):
            coincidencias.append((nombre, variantes))

    # Evitar respuestas parciales a preguntas compuestas.
    if len(coincidencias) > 1:
        return "No lo sé."

    if len(coincidencias) == 1:
        nombre, variantes = coincidencias[0]

        negados = normalizar(" ".join(sintomas_negados))
        presentes = normalizar(" ".join(sintomas_asociados))

        if any(v in negados for v in variantes):
            return f"No he presentado {nombre}."

        if any(v in presentes for v in variantes):
            return f"Sí, he presentado {nombre}."

    # No completar información ausente con suposiciones.
    return "No lo sé."


def responder_caso(id_caso, pregunta):
    fichas = cargar_fichas()

    if id_caso not in fichas:
        raise ValueError(f"No existe el caso {id_caso}")

    return responder_desde_ficha(
        fichas[id_caso],
        pregunta
    )


if __name__ == "__main__":
    fichas = cargar_fichas()

    print("\n=== RESPONDEDOR URGENTIA ===")
    print("Casos cargados:", len(fichas))

    for id_caso, pregunta in [
        ("URG-002", "¿Hace cuánto comenzaron los síntomas?"),
        ("URG-022", "¿Qué intensidad tiene el dolor?"),
        ("URG-062", "¿Está embarazada?"),
        ("URG-082", "¿Hace cuánto ocurrió el accidente?")
    ]:
        print(f"\nCaso: {id_caso}")
        print("Pregunta:", pregunta)
        print("Respuesta:", responder_caso(id_caso, pregunta))

    print("\nPrueba local completada.")
def responder_por_orden(id_caso, orden):
    import json
    from pathlib import Path

    archivo = (
        Path(__file__).resolve().parent
        / "casos_estudio_100.json"
    )

    with archivo.open("r", encoding="utf-8") as f:
        casos = json.load(f)

    caso = next(
        (c for c in casos if c["id_caso"] == id_caso),
        None
    )

    if caso is None:
        raise ValueError(f"Caso no encontrado: {id_caso}")

    respuestas = caso.get("respuestas_ia", {})
    respuesta = respuestas.get(str(orden))

    if not respuesta:
        return None

    return respuesta