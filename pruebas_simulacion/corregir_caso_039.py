import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

encontrado = False

for caso in casos:
    if caso["id_caso"] == "URG-039":

        if caso["poblacion_id"] != 2:
            raise ValueError("URG-039 no pertenece a Adulto")

        if caso["banderas_ids"] != [6]:
            raise ValueError(
                f"Banderas inesperadas: {caso['banderas_ids']}"
            )

        caso["banderas_ids"] = []

        caso["motivo_consulta"] = (
            "Congestión nasal y temperatura ligeramente elevada."
        )

        caso["historia_clinica"] = (
            "Mujer de 41 años con temperatura máxima reportada "
            "de 37,8 °C, congestión nasal y estornudos desde ayer. "
            "No presenta dificultad respiratoria, dolor torácico, "
            "confusión ni signos de deshidratación. "
            "Se alimenta normalmente. "
            "No se ha documentado el método de medición "
            "de la temperatura."
        )

        caso["respuestas_ia"] = {
            "1": "Tengo congestión nasal y estornudos.",
            "2": "Comenzó ayer.",
            "3": "Mi temperatura máxima fue de 37,8 grados.",
            "4": "No tengo dificultad para respirar.",
            "5": "Estoy comiendo normalmente y no me siento confundida."
        }

        caso["prioridad_esperada"] = None
        caso["estado_validacion"] = "pendiente_revision_clinica"

        encontrado = True
        break

if not encontrado:
    raise ValueError("No se encontró URG-039")

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("URG-039 corregido correctamente")
print("Banderas actuales:", caso["banderas_ids"])
print("Motivo:", caso["motivo_consulta"])
print("Prioridad objetivo:", caso["prioridad_objetivo"])
print("Total de casos:", len(casos))