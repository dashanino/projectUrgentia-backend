import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-022": {
        "edad": 54,
        "sexo": "Masculino",
        "banderas_ids": [3],
        "motivo_consulta": "Dolor intenso y opresivo en el pecho desde hace 30 minutos.",
        "historia_clinica": (
            "Hombre de 54 años con dolor torácico opresivo de intensidad "
            "9/10, iniciado hace 30 minutos en reposo. El dolor se irradia "
            "al brazo izquierdo. Presenta sudoración fría, náuseas y "
            "dificultad para respirar. No ha perdido el conocimiento."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor muy fuerte en el pecho desde hace media hora.",
            "2": "Comenzó de repente mientras estaba sentado y no ha mejorado.",
            "3": "Es una presión muy fuerte, de 9 sobre 10, que llega al brazo izquierdo.",
            "4": "Estoy sudando frío, tengo náuseas y me cuesta respirar.",
            "5": "Nunca había tenido un dolor así. No me he desmayado."
        }
    },
    "URG-023": {
        "edad": 42,
        "sexo": "Femenino",
        "banderas_ids": [5],
        "motivo_consulta": "Dificultad respiratoria intensa incluso estando en reposo.",
        "historia_clinica": (
            "Mujer de 42 años con dificultad respiratoria intensa de "
            "inicio reciente. Refiere que no puede completar frases "
            "sin detenerse a respirar. Presenta sensación de ahogo "
            "en reposo y empeoramiento progresivo durante la última hora."
        ),
        "respuestas_ia": {
            "1": "Me cuesta muchísimo respirar, incluso sin moverme.",
            "2": "Empezó hace una hora y ha empeorado.",
            "3": "No puedo hablar una frase completa sin detenerme.",
            "4": "Siento que me falta el aire incluso sentada.",
            "5": "No he tenido golpes ni accidentes."
        }
    },
    "URG-024": {
        "edad": 38,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal súbito y extremadamente intenso.",
        "historia_clinica": (
            "Hombre de 38 años con dolor abdominal generalizado de "
            "inicio súbito, intensidad 10/10, constante. Refiere abdomen "
            "muy rígido y dolor intenso al mínimo movimiento. "
            "Presenta náuseas y un episodio de vómito."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor insoportable en todo el abdomen.",
            "2": "Empezó de repente hace 40 minutos y no disminuye.",
            "3": "Es un dolor constante de 10 sobre 10.",
            "4": "Tengo el abdomen muy duro y moverme me produce más dolor.",
            "5": "He tenido náuseas y vomité una vez."
        }
    },
    "URG-025": {
        "edad": 61,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza súbito y extremadamente intenso.",
        "historia_clinica": (
            "Mujer de 61 años con cefalea súbita de intensidad 10/10, "
            "descrita como el peor dolor de cabeza de su vida. "
            "Comenzó hace 20 minutos. Un familiar refiere que la "
            "paciente está confundida y responde de manera incoherente."
        ),
        "respuestas_ia": {
            "1": "Me empezó un dolor de cabeza terrible de repente.",
            "2": "Comenzó hace unos 20 minutos.",
            "3": "Es el peor dolor de cabeza que he sentido, de 10 sobre 10.",
            "4": "Mi familiar dice que estoy confundida.",
            "5": "No recuerdo haber tenido un dolor parecido."
        }
    },
    "URG-026": {
        "edad": 57,
        "sexo": "Masculino",
        "banderas_ids": [3],
        "motivo_consulta": "Dolor torácico opresivo acompañado de desmayo.",
        "historia_clinica": (
            "Hombre de 57 años con dolor torácico opresivo intenso "
            "desde hace 25 minutos. Presentó pérdida transitoria "
            "del conocimiento durante aproximadamente un minuto. "
            "Al despertar continúa con dolor torácico, debilidad "
            "y sudoración fría."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor fuerte en el pecho y me desmayé hace poco.",
            "2": "El dolor comenzó hace unos 25 minutos.",
            "3": "Es una presión intensa en el centro del pecho.",
            "4": "Perdí el conocimiento cerca de un minuto.",
            "5": "Ahora estoy despierto, pero sigo débil y sudando frío."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 2:
            raise ValueError(f"Población incorrecta en {id_caso}")

        if caso["prioridad_objetivo"] != "alta":
            raise ValueError(f"Prioridad objetivo incorrecta en {id_caso}")

        caso.update(CASOS[id_caso])
        caso["antecedentes_ids"] = []
        caso["sintomas_ids"] = []
        caso["prioridad_esperada"] = None
        caso["estado_validacion"] = "pendiente_revision_clinica"

        actualizados.append(id_caso)

if len(actualizados) != 5:
    raise ValueError(
        f"Se esperaban 5 casos y se actualizaron {len(actualizados)}"
    )

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("Casos clínicos actualizados:")
for id_caso in actualizados:
    print(f"  {id_caso}")

print(f"\nTotal de casos del estudio: {len(casos)}")
print(
    "Casos con historia clínica:",
    sum(bool(c.get("historia_clinica")) for c in casos)
)