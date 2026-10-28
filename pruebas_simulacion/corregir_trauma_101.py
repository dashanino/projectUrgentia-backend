import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

encontrado = False

for caso in casos:
    if caso["id_caso"] == "URG-101":

        if caso["poblacion_id"] != 5:
            raise ValueError("URG-101 no pertenece a Trauma/Accidente")

        caso["motivo_consulta"] = (
            "Dolor muscular leve después de una lesión deportiva."
        )

        caso["historia_clinica"] = (
            "Hombre de 29 años que sufrió una distensión muscular "
            "leve en el muslo derecho durante una actividad deportiva "
            "hace seis horas, al realizar un movimiento brusco. "
            "Presenta dolor localizado de intensidad 2/10. "
            "Puede caminar normalmente. Niega caída, golpe directo, "
            "hinchazón importante, deformidad, pérdida de fuerza "
            "y alteraciones de sensibilidad."
        )

        caso["respuestas_ia"] = {
            "1": "Me lesioné el muslo haciendo deporte.",
            "2": "Fue hace seis horas al hacer un movimiento brusco.",
            "3": "El dolor es de 2 sobre 10.",
            "4": "Puedo caminar normalmente.",
            "5": "No tengo hinchazón importante ni pérdida de fuerza."
        }

        caso["estado_validacion"] = "pendiente_revision_clinica"
        caso["prioridad_esperada"] = None

        encontrado = True
        break

if not encontrado:
    raise ValueError("No se encontró URG-101")

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("URG-101 actualizado correctamente")
print("Motivo:", caso["motivo_consulta"])
print("Población:", caso["poblacion"])
print("Prioridad objetivo:", caso["prioridad_objetivo"])
print("Total de casos:", len(casos))