import json
from pathlib import Path

from simular_urgentia import (
    guardar_antecedentes_nn,
    seleccionar_poblacion_nn,
    guardar_banderas_rojas_nn,
    evaluar_reglas_nn
)

CARPETA = Path(__file__).resolve().parent

ARCHIVO_SESION = CARPETA / "sesion_URG-002.json"
ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_CONTROL = CARPETA / "control_URG-002.json"


def cargar_json(ruta):
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_control(control):
    temporal = ARCHIVO_CONTROL.with_suffix(".tmp")

    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(
            control,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    temporal.replace(ARCHIVO_CONTROL)


def main():
    print("\n=== EVALUACIÓN URG-002 ===")

    paciente = cargar_json(ARCHIVO_SESION)
    casos = cargar_json(ARCHIVO_CASOS)

    caso = next(
        c for c in casos
        if c["id_caso"] == "URG-002"
    )

    if ARCHIVO_CONTROL.exists():
        control = cargar_json(ARCHIVO_CONTROL)
    else:
        control = {
            "id_caso": "URG-002",
            "id_pretriage": paciente["id_pretriage"],
            "antecedentes": False,
            "poblacion": False,
            "banderas": False,
            "reglas_evaluadas": False,
            "resultado_reglas": None
        }
        guardar_control(control)

    if control["id_pretriage"] != paciente["id_pretriage"]:
        raise ValueError("La sesión no coincide con el control.")

    pasos = [
        (
            "antecedentes",
            lambda: guardar_antecedentes_nn(
                paciente,
                caso["antecedentes_ids"]
            )
        ),
        (
            "poblacion",
            lambda: seleccionar_poblacion_nn(
                paciente,
                caso["poblacion_id"]
            )
        ),
        (
            "banderas",
            lambda: guardar_banderas_rojas_nn(
                paciente,
                caso["banderas_ids"]
            )
        )
    ]

    for nombre, ejecutar in pasos:
        if control[nombre]:
            print(f"{nombre}: ya registrado.")
            continue

        print(f"\nRegistrando {nombre}...")

        if not ejecutar():
            print("Proceso detenido en:", nombre)
            print(
                "Antes de reintentar, verifica si "
                "el backend guardó este paso."
            )
            return

        control[nombre] = True
        guardar_control(control)

    if control["reglas_evaluadas"]:
        print("\nLas reglas ya fueron evaluadas.")
        print(control["resultado_reglas"])
        return

    print("\n=== EVALUANDO REGLAS CLÍNICAS ===")

    resultado = evaluar_reglas_nn(paciente)

    if resultado is None:
        print(
            "No se confirmó la evaluación. "
            "Verifica su estado antes de reintentar."
        )
        return

    control["resultado_reglas"] = resultado
    control["reglas_evaluadas"] = True
    guardar_control(control)

    print("\n=== RESULTADO GUARDADO ===")
    print("Caso:", control["id_caso"])
    print("Pretriaje:", control["id_pretriage"])
    print("Resultado:", resultado)
    print("\nNo se ejecutó el cuestionario de IA.")


if __name__ == "__main__":
    main()