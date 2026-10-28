import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-092": {
        "edad": 25,
        "sexo": "Femenino",
        "banderas_ids": [17],
        "motivo_consulta": "Dolor de muñeca después de una caída.",
        "historia_clinica": (
            "Mujer de 25 años que cayó sobre la mano derecha hace "
            "tres horas. Presenta dolor de muñeca de intensidad "
            "4/10, hinchazón leve y molestias al moverla. "
            "No observa deformidad, heridas ni cambios de color "
            "en los dedos. Conserva la sensibilidad y movilidad "
            "de los dedos. No se ha descartado una fractura."
        ),
        "respuestas_ia": {
            "1": "Me caí sobre la mano derecha hace tres horas.",
            "2": "Me duele la muñeca.",
            "3": "El dolor es de 4 sobre 10.",
            "4": "Está un poco hinchada, pero no deformada.",
            "5": "Puedo mover los dedos y los siento normalmente."
        }
    },
    "URG-093": {
        "edad": 38,
        "sexo": "Masculino",
        "banderas_ids": [20],
        "motivo_consulta": "Quemadura superficial pequeña.",
        "historia_clinica": (
            "Hombre de 38 años que sufrió una quemadura por "
            "contacto con una superficie caliente hace dos horas. "
            "Presenta enrojecimiento localizado en una pequeña "
            "zona del antebrazo izquierdo y dolor de intensidad "
            "3/10. No presenta ampollas, pérdida de sensibilidad "
            "ni lesiones en otras zonas. Niega exposición a humo."
        ),
        "respuestas_ia": {
            "1": "Me quemé el antebrazo hace dos horas.",
            "2": "Fue al tocar una superficie caliente.",
            "3": "El dolor es de 3 sobre 10.",
            "4": "La piel está roja, pero no tengo ampollas.",
            "5": "La quemadura es pequeña y no respiré humo."
        }
    },
    "URG-094": {
        "edad": 30,
        "sexo": "Femenino",
        "banderas_ids": [],
        "motivo_consulta": "Dolor de tobillo después de una torcedura.",
        "historia_clinica": (
            "Mujer de 30 años que sufrió una torcedura del "
            "tobillo derecho mientras caminaba hace cuatro horas. "
            "Presenta dolor de intensidad 4/10 e hinchazón leve. "
            "Puede apoyar el pie y caminar varios pasos, aunque "
            "con molestias. Niega deformidad, heridas abiertas, "
            "pérdida de sensibilidad y cambios de coloración."
        ),
        "respuestas_ia": {
            "1": "Me torcí el tobillo hace cuatro horas.",
            "2": "Me duele 4 sobre 10.",
            "3": "Está un poco hinchado.",
            "4": "Puedo apoyar el pie y caminar.",
            "5": "No tengo heridas ni deformidad."
        }
    },
    "URG-095": {
        "edad": 44,
        "sexo": "Masculino",
        "banderas_ids": [16],
        "motivo_consulta": "Golpe leve en la cabeza.",
        "historia_clinica": (
            "Hombre de 44 años que se golpeó la cabeza "
            "contra una puerta hace dos horas. Presenta "
            "dolor local de intensidad 3/10. Niega pérdida "
            "del conocimiento, vómitos, confusión, alteraciones "
            "visuales y debilidad. Está orientado. "
            "No se ha documentado uso de anticoagulantes."
        ),
        "respuestas_ia": {
            "1": "Me golpeé la cabeza con una puerta hace dos horas.",
            "2": "Me duele un poco donde me golpeé.",
            "3": "El dolor es de 3 sobre 10.",
            "4": "No perdí el conocimiento ni he vomitado.",
            "5": "No tengo confusión ni problemas de visión."
        }
    },
    "URG-096": {
        "edad": 35,
        "sexo": "Femenino",
        "banderas_ids": [3],
        "motivo_consulta": "Dolor localizado en el tórax después de un golpe.",
        "historia_clinica": (
            "Mujer de 35 años que recibió un golpe leve "
            "en el costado del tórax durante una actividad "
            "deportiva hace tres horas. Presenta dolor localizado "
            "de intensidad 4/10 que aumenta al tocar la zona. "
            "Niega dificultad respiratoria, pérdida del "
            "conocimiento y empeoramiento progresivo. "
            "No se dispone de signos vitales."
        ),
        "respuestas_ia": {
            "1": "Recibí un golpe en el costado del pecho hace tres horas.",
            "2": "Me duele 4 sobre 10.",
            "3": "El dolor aumenta cuando me toco la zona.",
            "4": "No tengo dificultad para respirar.",
            "5": "No me he desmayado y el dolor no ha empeorado."
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

        if caso["prioridad_objetivo"] != "media_baja":
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