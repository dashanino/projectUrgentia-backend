import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "casos_clinicos.json"

POBLACIONES = {
    1: "Niño",
    2: "Adulto",
    3: "Adulto Mayor",
    4: "Embarazada",
    5: "Trauma/Accidente",
}

PRIORIDADES = [
    "alta",
    "media_alta",
    "media_baja",
    "baja",
]

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

if not isinstance(casos, list):
    raise ValueError("El archivo debe contener una lista de casos.")

ids_existentes = {caso["id_caso"] for caso in casos}

for id_poblacion, nombre_poblacion in POBLACIONES.items():
    for prioridad in PRIORIDADES:
        existentes = sum(
            1
            for caso in casos
            if caso.get("poblacion_id") == id_poblacion
            and caso.get("prioridad_objetivo") == prioridad
        )

        for numero in range(existentes + 1, 6):
            consecutivo = len(casos) + 1
            id_caso = f"URG-{consecutivo:03d}"

            while id_caso in ids_existentes:
                consecutivo += 1
                id_caso = f"URG-{consecutivo:03d}"

            casos.append({
                "id_caso": id_caso,
                "poblacion_id": id_poblacion,
                "poblacion": nombre_poblacion,
                "prioridad_objetivo": prioridad,
                "prioridad_esperada": None,
                "estado_validacion": "pendiente_diseno",
                "edad": None,
                "sexo": None,
                "antecedentes_ids": [],
                "banderas_ids": [],
                "sintomas_ids": [],
                "motivo_consulta": "",
                "historia_clinica": "",
                "respuestas_ia": {}
            })

            ids_existentes.add(id_caso)

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print(f"Total de registros: {len(casos)}")
print(f"Casos clínicos completos: {sum(bool(c.get('historia_clinica')) for c in casos)}")
print("Estructura creada correctamente.")