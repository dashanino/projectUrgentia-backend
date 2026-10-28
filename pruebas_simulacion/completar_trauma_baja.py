import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-097": {
        "edad": 23,
        "sexo": "Masculino",
        "banderas_ids": [],
        "motivo_consulta": "Golpe leve en el antebrazo.",
        "historia_clinica": (
            "Hombre de 23 años que se golpeó el antebrazo derecho "
            "contra una mesa hace dos horas. Presenta dolor "
            "localizado de intensidad 2/10 y enrojecimiento leve. "
            "Conserva la movilidad completa del brazo y la mano. "
            "Niega deformidad, herida abierta, pérdida de sensibilidad "
            "y aumento progresivo del dolor."
        ),
        "respuestas_ia": {
            "1": "Me golpeé el antebrazo contra una mesa.",
            "2": "Fue hace dos horas.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "Puedo mover el brazo y la mano normalmente.",
            "5": "No tengo heridas, deformidad ni pérdida de sensibilidad."
        }
    },
    "URG-098": {
        "edad": 31,
        "sexo": "Femenino",
        "banderas_ids": [20],
        "motivo_consulta": "Quemadura superficial pequeña.",
        "historia_clinica": (
            "Mujer de 31 años que sufrió una quemadura por contacto "
            "con una taza caliente hace una hora. Presenta una zona "
            "pequeña de enrojecimiento en el antebrazo, con dolor "
            "de intensidad 2/10. No presenta ampollas ni pérdida "
            "de sensibilidad. Niega exposición a humo y lesiones "
            "en otras partes del cuerpo."
        ),
        "respuestas_ia": {
            "1": "Me quemé el antebrazo con una taza caliente.",
            "2": "Fue hace una hora.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "La piel está roja, pero no tengo ampollas.",
            "5": "Es una quemadura pequeña y no respiré humo."
        }
    },
    "URG-099": {
        "edad": 27,
        "sexo": "Masculino",
        "banderas_ids": [],
        "motivo_consulta": "Torcedura leve de tobillo.",
        "historia_clinica": (
            "Hombre de 27 años que se torció el tobillo izquierdo "
            "mientras caminaba hace tres horas. Presenta dolor "
            "de intensidad 2/10 e hinchazón mínima. Puede apoyar "
            "el pie y caminar normalmente. Niega deformidad, "
            "heridas abiertas, pérdida de sensibilidad y "
            "cambios de coloración."
        ),
        "respuestas_ia": {
            "1": "Me torcí el tobillo mientras caminaba.",
            "2": "Fue hace tres horas.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "Puedo apoyar el pie y caminar.",
            "5": "No tengo deformidad, heridas ni pérdida de sensibilidad."
        }
    },
    "URG-100": {
        "edad": 40,
        "sexo": "Femenino",
        "banderas_ids": [],
        "motivo_consulta": "Contusión leve en la pierna.",
        "historia_clinica": (
            "Mujer de 40 años que recibió un golpe leve en la "
            "pierna derecha contra un mueble hace cuatro horas. "
            "Presenta dolor localizado de intensidad 2/10 "
            "y un hematoma pequeño. Puede caminar sin dificultad. "
            "Niega deformidad, herida abierta, pérdida de sensibilidad "
            "y aumento del dolor."
        ),
        "respuestas_ia": {
            "1": "Me golpeé la pierna contra un mueble.",
            "2": "Fue hace cuatro horas.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "Tengo un morado pequeño.",
            "5": "Puedo caminar normalmente y no tengo heridas."
        }
    },
    "URG-101": {
        "edad": 29,
        "sexo": "Masculino",
        "banderas_ids": [],
        "motivo_consulta": "Dolor muscular leve después de esfuerzo físico.",
        "historia_clinica": (
            "Hombre de 29 años con dolor muscular localizado "
            "en el muslo derecho de intensidad 2/10 después "
            "de realizar ejercicio hace seis horas. "
            "No refiere caída, golpe directo ni accidente. "
            "Puede caminar normalmente. Niega hinchazón importante, "
            "deformidad, pérdida de fuerza y alteraciones "
            "de sensibilidad."
        ),
        "respuestas_ia": {
            "1": "Me duele un poco el músculo del muslo después de hacer ejercicio.",
            "2": "Comenzó hace seis horas.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "Puedo caminar normalmente.",
            "5": "No tuve golpes ni caídas y no tengo debilidad."
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

        if caso["prioridad_objetivo"] != "baja":
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