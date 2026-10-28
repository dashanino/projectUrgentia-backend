import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-087": {
        "edad": 28,
        "sexo": "Masculino",
        "banderas_ids": [17],
        "motivo_consulta": "Sospecha de fractura de muñeca.",
        "historia_clinica": (
            "Hombre de 28 años que cayó sobre la mano derecha "
            "hace una hora. Presenta dolor de muñeca de intensidad "
            "8/10, hinchazón y dificultad para moverla. "
            "No presenta herida abierta ni sangrado. "
            "Refiere sensibilidad conservada en los dedos "
            "y no observa cambios en su coloración."
        ),
        "respuestas_ia": {
            "1": "Me caí sobre la mano derecha hace una hora.",
            "2": "Me duele mucho la muñeca.",
            "3": "El dolor es de 8 sobre 10.",
            "4": "Está hinchada y me cuesta moverla.",
            "5": "No tengo heridas ni sangrado.",
            "6": "Siento los dedos normalmente.",
            "7": "Los dedos tienen su color habitual.",
            "8": "No me golpeé la cabeza."
        }
    },
    "URG-088": {
        "edad": 41,
        "sexo": "Femenino",
        "banderas_ids": [15],
        "motivo_consulta": "Herida profunda en antebrazo.",
        "historia_clinica": (
            "Mujer de 41 años que sufrió una herida cortante "
            "en el antebrazo izquierdo hace cuarenta minutos. "
            "La herida es profunda y presenta dolor de intensidad "
            "7/10. El sangrado disminuyó y está controlado "
            "con presión directa. Puede mover los dedos "
            "y conserva la sensibilidad."
        ),
        "respuestas_ia": {
            "1": "Me corté el antebrazo hace cuarenta minutos.",
            "2": "La herida es profunda.",
            "3": "Me duele 7 sobre 10.",
            "4": "El sangrado está controlado con presión.",
            "5": "Puedo mover los dedos.",
            "6": "Siento normalmente la mano.",
            "7": "No tengo mareo ni desmayo.",
            "8": "No me golpeé la cabeza."
        }
    },
    "URG-089": {
        "edad": 36,
        "sexo": "Masculino",
        "banderas_ids": [16],
        "motivo_consulta": "Golpe en la cabeza con cefalea y náuseas.",
        "historia_clinica": (
            "Hombre de 36 años que sufrió una caída en bicicleta "
            "hace dos horas y se golpeó la cabeza. "
            "Presenta cefalea de intensidad 6/10 y náuseas. "
            "Niega pérdida del conocimiento, vómitos y confusión. "
            "Está orientado y puede caminar normalmente. "
            "No se ha documentado uso de anticoagulantes."
        ),
        "respuestas_ia": {
            "1": "Me caí de la bicicleta y me golpeé la cabeza.",
            "2": "Fue hace dos horas.",
            "3": "Tengo dolor de cabeza de 6 sobre 10.",
            "4": "Tengo náuseas, pero no he vomitado.",
            "5": "No perdí el conocimiento.",
            "6": "No estoy confundido.",
            "7": "Puedo caminar normalmente.",
            "8": "No sé si tomo algún medicamento que aumente el sangrado."
        }
    },
    "URG-090": {
        "edad": 47,
        "sexo": "Femenino",
        "banderas_ids": [20],
        "motivo_consulta": "Quemadura dolorosa en antebrazo.",
        "historia_clinica": (
            "Mujer de 47 años que sufrió una quemadura térmica "
            "en el antebrazo derecho con agua caliente hace "
            "una hora. Presenta dolor de intensidad 7/10, "
            "enrojecimiento y algunas ampollas. "
            "La lesión está localizada en una zona limitada "
            "del antebrazo. Niega dificultad respiratoria "
            "y exposición a humo."
        ),
        "respuestas_ia": {
            "1": "Me quemé el antebrazo con agua caliente.",
            "2": "Fue hace una hora.",
            "3": "Me duele 7 sobre 10.",
            "4": "Tengo la piel roja y algunas ampollas.",
            "5": "La quemadura está solo en una parte del antebrazo.",
            "6": "No tengo dificultad para respirar.",
            "7": "No estuve expuesta a humo.",
            "8": "No tengo quemaduras en otras partes del cuerpo."
        }
    },
    "URG-091": {
        "edad": 32,
        "sexo": "Masculino",
        "banderas_ids": [3],
        "motivo_consulta": "Dolor torácico después de accidente.",
        "historia_clinica": (
            "Hombre de 32 años involucrado en una colisión "
            "automovilística hace una hora. Presenta dolor "
            "torácico localizado de intensidad 7/10, "
            "que aumenta al respirar profundamente y al tocar "
            "la zona afectada. Puede hablar en frases completas. "
            "Niega pérdida del conocimiento. No se dispone "
            "de saturación de oxígeno ni otros signos vitales."
        ),
        "respuestas_ia": {
            "1": "Tuve un accidente de carro hace una hora.",
            "2": "Me duele el pecho.",
            "3": "El dolor es de 7 sobre 10.",
            "4": "Me duele más cuando respiro profundo.",
            "5": "También me duele al tocarme el pecho.",
            "6": "Puedo hablar normalmente.",
            "7": "No perdí el conocimiento.",
            "8": "No sé cómo está mi oxigenación."
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

        if caso["prioridad_objetivo"] != "media_alta":
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