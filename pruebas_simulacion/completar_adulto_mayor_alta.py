import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-042": {
        "edad": 76,
        "sexo": "Masculino",
        "banderas_ids": [3, 5],
        "antecedentes_ids": [],
        "motivo_consulta": "Dolor intenso en el pecho y dificultad para respirar.",
        "historia_clinica": (
            "Hombre de 76 años con dolor torácico opresivo 9/10 desde "
            "hace 25 minutos, irradiado al brazo izquierdo, acompañado "
            "de sudoración fría, náuseas y dificultad respiratoria "
            "en reposo. Está consciente."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor muy fuerte en el pecho y me cuesta respirar.",
            "2": "Comenzó hace 25 minutos y no ha mejorado.",
            "3": "Es una presión de 9 sobre 10 que llega al brazo izquierdo.",
            "4": "Estoy sudando frío y tengo náuseas.",
            "5": "Me falta el aire incluso estando sentado."
        }
    },
    "URG-043": {
        "edad": 82,
        "sexo": "Femenino",
        "banderas_ids": [5],
        "antecedentes_ids": [],
        "motivo_consulta": "Dificultad respiratoria intensa en reposo.",
        "historia_clinica": (
            "Mujer de 82 años con dificultad respiratoria intensa "
            "de inicio hace una hora, progresiva. No logra completar "
            "frases sin detenerse a respirar y refiere sensación "
            "constante de ahogo incluso estando sentada."
        ),
        "respuestas_ia": {
            "1": "No puedo respirar bien, incluso sentada.",
            "2": "Comenzó hace una hora y está empeorando.",
            "3": "Tengo que detenerme para respirar cuando hablo.",
            "4": "Siento que me estoy ahogando.",
            "5": "No he tenido golpes ni accidentes."
        }
    },
    "URG-044": {
        "edad": 71,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "antecedentes_ids": [],
        "motivo_consulta": "Dolor de cabeza súbito y alteración del estado mental.",
        "historia_clinica": (
            "Mujer de 71 años con cefalea de inicio súbito, intensidad "
            "10/10, hace 15 minutos. Un familiar refiere que está "
            "desorientada y responde de forma incoherente. No se "
            "ha documentado pérdida del conocimiento."
        ),
        "respuestas_ia": {
            "1": "Me empezó un dolor de cabeza insoportable de repente.",
            "2": "Empezó hace unos 15 minutos.",
            "3": "Es el peor dolor de cabeza que he tenido.",
            "4": "Mi familiar dice que estoy desorientada.",
            "5": "Me cuesta responder algunas preguntas."
        }
    },
    "URG-045": {
        "edad": 88,
        "sexo": "Masculino",
        "banderas_ids": [7],
        "antecedentes_ids": [1],
        "motivo_consulta": "Caída con golpe en la cabeza y confusión.",
        "historia_clinica": (
            "Hombre de 88 años que sufrió una caída desde su propia "
            "altura hace 30 minutos y se golpeó la cabeza. "
            "Un familiar refiere confusión posterior al golpe. "
            "El paciente utiliza medicamentos anticoagulantes. "
            "No se conoce si perdió el conocimiento."
        ),
        "respuestas_ia": {
            "1": "Me caí y me golpeé la cabeza.",
            "2": "La caída ocurrió hace media hora.",
            "3": "Mi familiar dice que estoy confundido.",
            "4": "Tomo medicamentos anticoagulantes.",
            "5": "No sabemos si perdí el conocimiento."
        }
    },
    "URG-046": {
        "edad": 79,
        "sexo": "Femenino",
        "banderas_ids": [4],
        "antecedentes_ids": [],
        "motivo_consulta": "Dolor abdominal súbito de intensidad extrema.",
        "historia_clinica": (
            "Mujer de 79 años con dolor abdominal generalizado "
            "de inicio súbito hace 40 minutos, intensidad 10/10, "
            "constante. Refiere abdomen rígido y dolor intenso "
            "con el movimiento. Presenta náuseas y debilidad."
        ),
        "respuestas_ia": {
            "1": "Tengo un dolor insoportable en todo el abdomen.",
            "2": "Comenzó de repente hace 40 minutos.",
            "3": "Es de 10 sobre 10 y no disminuye.",
            "4": "Tengo el abdomen duro y me duele cuando me muevo.",
            "5": "Tengo náuseas y mucha debilidad."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 3:
            raise ValueError(f"Población incorrecta: {id_caso}")

        if caso["prioridad_objetivo"] != "alta":
            raise ValueError(f"Prioridad objetivo incorrecta: {id_caso}")

        caso.update(CASOS[id_caso])
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

print("Casos actualizados:")
for id_caso in actualizados:
    print(f"  {id_caso}")

print(f"\nTotal de casos: {len(casos)}")
print(
    "Casos con historia clínica:",
    sum(bool(c.get("historia_clinica")) for c in casos)
)