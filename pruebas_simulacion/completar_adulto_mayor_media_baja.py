import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

CASOS = {
    "URG-052": {
        "edad": 68,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Dolor abdominal moderado desde esta mañana.",
        "historia_clinica": (
            "Hombre de 68 años con dolor abdominal periumbilical "
            "intermitente de intensidad 4/10 desde hace seis horas. "
            "El dolor no ha aumentado ni se ha desplazado. "
            "Niega fiebre, vómitos, distensión y síntomas urinarios. "
            "Tolera alimentos y líquidos."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor alrededor del ombligo desde esta mañana.",
            "2": "Es de 4 sobre 10, va y viene y no ha empeorado.",
            "3": "No se ha desplazado hacia otra parte.",
            "4": "No tengo fiebre, vómitos ni distensión.",
            "5": "Puedo comer y beber normalmente.",
            "6": "No tengo náuseas.",
            "7": "No tengo el abdomen duro ni dolor intenso al moverme.",
            "8": "No he tenido golpes recientes."
        }
    },
    "URG-053": {
        "edad": 72,
        "sexo": "Femenino",
        "banderas_ids": [2],
        "motivo_consulta": "Dolor de cabeza moderado de inicio gradual.",
        "historia_clinica": (
            "Mujer de 72 años con cefalea bilateral de intensidad "
            "5/10, iniciada gradualmente hace cinco horas. "
            "Está orientada y puede caminar normalmente. "
            "Niega fiebre, vómitos, alteraciones visuales, "
            "confusión y pérdida de fuerza. "
            "No se ha documentado si es una cefalea nueva."
        ),
        "respuestas_ia": {
            "1": "Tengo dolor de cabeza desde hace cinco horas.",
            "2": "Empezó poco a poco.",
            "3": "Es de 5 sobre 10 y lo siento en ambos lados.",
            "4": "No tengo vómitos, fiebre ni cambios en la visión.",
            "5": "Estoy orientada y puedo caminar normalmente."
        }
    },
    "URG-054": {
        "edad": 75,
        "sexo": "Masculino",
        "banderas_ids": [6],
        "motivo_consulta": "Fiebre moderada y malestar general.",
        "historia_clinica": (
            "Hombre de 75 años con temperatura máxima de 38,1 °C "
            "desde hace 24 horas, congestión nasal y cansancio. "
            "Está consciente y orientado, bebe líquidos y "
            "niega dificultad respiratoria, dolor torácico "
            "y confusión."
        ),
        "respuestas_ia": {
            "1": "Tengo fiebre y congestión desde ayer.",
            "2": "La temperatura máxima fue 38,1 grados.",
            "3": "Tengo cansancio y congestión nasal.",
            "4": "Puedo beber líquidos.",
            "5": "No tengo dificultad para respirar ni confusión."
        }
    },
    "URG-055": {
        "edad": 70,
        "sexo": "Femenino",
        "banderas_ids": [7],
        "motivo_consulta": "Caída desde su propia altura con dolor leve de rodilla.",
        "historia_clinica": (
            "Mujer de 70 años que sufrió una caída desde su propia "
            "altura hace tres horas. Presenta dolor leve de rodilla "
            "derecha de intensidad 3/10. Puede caminar sin ayuda. "
            "Niega golpe en la cabeza, pérdida del conocimiento, "
            "confusión y deformidad. No se ha documentado "
            "uso de anticoagulantes."
        ),
        "respuestas_ia": {
            "1": "Me caí hace tres horas y me duele un poco la rodilla.",
            "2": "Fue una caída desde mi propia altura.",
            "3": "El dolor es de 3 sobre 10.",
            "4": "Puedo caminar normalmente.",
            "5": "No me golpeé la cabeza ni perdí el conocimiento."
        }
    },
    "URG-056": {
        "edad": 79,
        "sexo": "Masculino",
        "banderas_ids": [4],
        "motivo_consulta": "Molestia abdominal intermitente sin empeoramiento.",
        "historia_clinica": (
            "Hombre de 79 años con molestia abdominal difusa "
            "de intensidad 4/10 desde hace ocho horas. "
            "El dolor es intermitente y estable. "
            "Niega fiebre, vómitos, sangrado, distensión "
            "y dificultad para evacuar o expulsar gases. "
            "Está orientado y tolera líquidos."
        ),
        "respuestas_ia": {
            "1": "Tengo una molestia abdominal desde hace ocho horas.",
            "2": "Va y viene y no ha empeorado.",
            "3": "Es de 4 sobre 10 y no está en un lugar específico.",
            "4": "No tengo fiebre, vómitos ni sangrado.",
            "5": "Puedo evacuar y expulsar gases.",
            "6": "Puedo beber líquidos normalmente.",
            "7": "No tengo el abdomen duro.",
            "8": "No he tenido golpes recientes."
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