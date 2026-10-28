import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-082": {
        "edad": 34,
        "sexo": "Masculino",
        "banderas_ids": [5],
        "motivo_consulta": "Accidente de tránsito con dificultad respiratoria grave.",
        "historia_clinica": (
            "Hombre de 34 años involucrado en una colisión de motocicleta "
            "hace veinte minutos. Presenta dificultad respiratoria intensa, "
            "dolor torácico de intensidad 9/10 y respiración rápida. "
            "Tiene dificultad para completar frases y refiere "
            "empeoramiento progresivo."
        ),
        "respuestas_ia": {
            "1": "Tuve un accidente de moto hace veinte minutos.",
            "2": "Me cuesta mucho respirar.",
            "3": "Tengo dolor en el pecho de 9 sobre 10.",
            "4": "Estoy respirando muy rápido.",
            "5": "Me cuesta hablar y estoy empeorando."
        }
    },
    "URG-083": {
        "edad": 27,
        "sexo": "Femenino",
        "banderas_ids": [15],
        "motivo_consulta": "Herida profunda con sangrado abundante.",
        "historia_clinica": (
            "Mujer de 27 años que sufrió una herida profunda en el muslo "
            "derecho con un objeto cortante hace quince minutos. "
            "Presenta sangrado abundante que continúa a pesar "
            "de la presión directa inicial. Refiere mareo y debilidad."
        ),
        "respuestas_ia": {
            "1": "Me corté profundamente el muslo hace quince minutos.",
            "2": "Estoy sangrando mucho.",
            "3": "El sangrado no se detiene con la presión.",
            "4": "Me siento mareada.",
            "5": "También siento debilidad."
        }
    },
    "URG-084": {
        "edad": 45,
        "sexo": "Masculino",
        "banderas_ids": [16, 18],
        "motivo_consulta": "Golpe en la cabeza con confusión.",
        "historia_clinica": (
            "Hombre de 45 años que sufrió una caída desde una escalera "
            "hace treinta minutos, con golpe directo en la cabeza. "
            "Un acompañante refiere que está desorientado, repite "
            "preguntas y no recuerda claramente el accidente. "
            "Presenta cefalea intensa."
        ),
        "respuestas_ia": {
            "1": "Me caí de una escalera y me golpeé la cabeza.",
            "2": "Fue hace treinta minutos.",
            "3": "Me duele mucho la cabeza.",
            "4": "No recuerdo bien qué pasó.",
            "5": "Mi acompañante dice que estoy confundido."
        }
    },
    "URG-085": {
        "edad": 39,
        "sexo": "Femenino",
        "banderas_ids": [19],
        "motivo_consulta": "Accidente con sospecha de lesión de columna.",
        "historia_clinica": (
            "Mujer de 39 años involucrada en un accidente de tránsito "
            "hace cuarenta minutos. Presenta dolor cervical intenso "
            "y hormigueo en ambas piernas. Refiere dificultad "
            "para moverlas después del impacto. "
            "Permanece consciente y orientada."
        ),
        "respuestas_ia": {
            "1": "Tuve un accidente de tránsito hace cuarenta minutos.",
            "2": "Me duele mucho el cuello.",
            "3": "Siento hormigueo en las dos piernas.",
            "4": "Me cuesta mover las piernas.",
            "5": "Estoy consciente y puedo responder preguntas."
        }
    },
    "URG-086": {
        "edad": 52,
        "sexo": "Masculino",
        "banderas_ids": [20, 5],
        "motivo_consulta": "Quemadura extensa con dificultad respiratoria.",
        "historia_clinica": (
            "Hombre de 52 años expuesto a un incendio en un espacio "
            "cerrado hace veinticinco minutos. Presenta quemaduras "
            "extensas en tórax y brazos, tos y dificultad respiratoria. "
            "Refiere dolor intenso y exposición a humo."
        ),
        "respuestas_ia": {
            "1": "Estuve en un incendio hace veinticinco minutos.",
            "2": "Tengo quemaduras en el pecho y los brazos.",
            "3": "Me duele mucho.",
            "4": "Respiré humo y ahora tengo tos.",
            "5": "Me cuesta respirar."
        }
    }
}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

actualizados = []

for caso in casos:
    id_caso = caso["id_caso"]

    if id_caso in CASOS:
        if caso["poblacion_id"] != 5:
            raise ValueError(f"Población incorrecta: {id_caso}")

        if caso["prioridad_objetivo"] != "alta":
            raise ValueError(f"Prioridad incorrecta: {id_caso}")

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

print("Casos actualizados:")
for id_caso in actualizados:
    print(f"  {id_caso}")

print(f"\nTotal de casos: {len(casos)}")
print(
    "Casos con historia clínica:",
    sum(bool(c.get("historia_clinica")) for c in casos)
)