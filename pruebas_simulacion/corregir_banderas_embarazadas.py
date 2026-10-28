import json
from pathlib import Path

ARCHIVO = Path(__file__).resolve().parent / "casos_estudio_100.json"

IDS_CORREGIR = {"URG-073", "URG-075"}

with ARCHIVO.open("r", encoding="utf-8") as archivo:
    casos = json.load(archivo)

corregidos = []

for caso in casos:
    if caso["id_caso"] in IDS_CORREGIR:

        if caso["poblacion_id"] != 4:
            raise ValueError(
                f"{caso['id_caso']} no pertenece a embarazadas"
            )

        if caso["banderas_ids"] != [2]:
            raise ValueError(
                f"Banderas inesperadas en {caso['id_caso']}: "
                f"{caso['banderas_ids']}"
            )

        caso["banderas_ids"] = []
        corregidos.append(caso["id_caso"])

if set(corregidos) != IDS_CORREGIR:
    raise ValueError("No se encontraron los dos casos esperados")

with ARCHIVO.open("w", encoding="utf-8") as archivo:
    json.dump(casos, archivo, ensure_ascii=False, indent=2)

print("Casos corregidos:", ", ".join(sorted(corregidos)))
print("Total de casos:", len(casos))
print("Historias clínicas completas:",
      sum(bool(c.get("historia_clinica")) for c in casos))