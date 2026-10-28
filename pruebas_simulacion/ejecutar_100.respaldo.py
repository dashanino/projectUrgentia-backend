
import csv
import json
import os
import sys
from pathlib import Path

from simular_urgentia import (
    comprobar_backend,
    crear_paciente_nn,
    guardar_antecedentes_nn,
    seleccionar_poblacion_nn,
    guardar_banderas_rojas_nn,
    evaluar_reglas_nn,
)

CARPETA = Path(__file__).resolve().parent
ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_PLAN = CARPETA / "plan_ejecucion_100.json"
ARCHIVO_CSV = CARPETA / "resultados_evaluacion_100.csv"


def leer(ruta):
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)


def guardar(ruta, datos):
    temporal = ruta.with_name(ruta.name + ".tmp")
    with temporal.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    os.replace(temporal, ruta)


def ejecutar(id_caso):
    casos = leer(ARCHIVO_CASOS)
    plan = leer(ARCHIVO_PLAN)

    caso = next(
        (x for x in casos if x["id_caso"] == id_caso),
        None
    )
    registro = next(
        (x for x in plan if x["id_caso"] == id_caso),
        None
    )

    if caso is None or registro is None:
        print("Caso no encontrado:", id_caso)
        return

    print(f"\n=== URGENTIA: {id_caso} ===")
    print("Población:", caso["poblacion"])
    print("Motivo:", caso["motivo_consulta"])
    print("Estado:", registro["estado_simulacion"])

    estados_finalizados = {
        "completado",
        "bloqueado_alerta_seguridad",
    }

    if registro["estado_simulacion"] in estados_finalizados:
        print("Caso ya procesado:", registro["estado_simulacion"])
        print("No se repetirá ni se sobrescribirá su resultado.")
        return

    archivo_sesion = CARPETA / f"sesion_{id_caso}.json"
    archivo_control = CARPETA / f"control_{id_caso}.json"

    if archivo_control.exists():
        control = leer(archivo_control)
    else:
        control = {
            "id_caso": id_caso,
            "id_pretriage": None,
            "antecedentes": False,
            "poblacion": False,
            "banderas": False,
            "reglas_evaluadas": False,
            "resultado_reglas": None,
        }

    if archivo_sesion.exists():
        paciente = leer(archivo_sesion)
        print("Reutilizando sesión:", paciente["id_pretriage"])
    else:
        if registro["id_pretriage"] is not None:
            print("Existe un pretriaje sin archivo de sesión.")
            print("Se detiene para evitar duplicados.")
            return

        if not comprobar_backend():
            return

        print("\nCreando paciente...")
        paciente = crear_paciente_nn()

        if paciente is None:
            print("Creación no confirmada. Revisar antes de reintentar.")
            return

        # Se guarda inmediatamente la sesión.
        with archivo_sesion.open("x", encoding="utf-8") as f:
            json.dump(paciente, f, ensure_ascii=False, indent=2)

        archivo_sesion.chmod(0o600)

        registro["id_pretriage"] = paciente["id_pretriage"]
        registro["estado_simulacion"] = "iniciado"
        guardar(ARCHIVO_PLAN, plan)

    if (
        registro["id_pretriage"] is not None
        and registro["id_pretriage"] != paciente["id_pretriage"]
    ):
        raise ValueError("ID de pretriaje inconsistente.")

    control["id_pretriage"] = paciente["id_pretriage"]
    guardar(archivo_control, control)

    pasos = [
        (
            "antecedentes",
            lambda: guardar_antecedentes_nn(
                paciente, caso["antecedentes_ids"]
            ),
        ),
        (
            "poblacion",
            lambda: seleccionar_poblacion_nn(
                paciente, caso["poblacion_id"]
            ),
        ),
        (
            "banderas",
            lambda: guardar_banderas_rojas_nn(
                paciente, caso["banderas_ids"]
            ),
        ),
    ]

    for nombre, funcion in pasos:
        if control[nombre]:
            continue

        print("\nRegistrando:", nombre)

        if not funcion():
            print("Operación no confirmada.")
            print("Verifica el backend antes de reintentar.")
            return

        control[nombre] = True
        guardar(archivo_control, control)

    if not control["reglas_evaluadas"]:
        print("\nEvaluando reglas clínicas...")
        resultado = evaluar_reglas_nn(paciente)

        if resultado is None:
            print("Evaluación no confirmada. Revisar.")
            return

        control["resultado_reglas"] = resultado
        control["reglas_evaluadas"] = True
        guardar(archivo_control, control)

    resultado = control["resultado_reglas"]

    if (
        resultado.get("accion") == "alerta"
        and resultado.get("alta_prioridad") is True
    ):
        ruta = "reglas"
        accion = "alerta"
        estado = "completado"
        print("\nALERTA POR REGLAS CLÍNICAS")

    else:
        ruta = "pendiente_ia"
        accion = resultado.get("accion", "sin_alerta")
        estado = "pendiente_ia"
        print("\nSin alerta confirmada por reglas.")
        print("Pendiente de cuestionario IA.")

    registro["ruta_sistema"] = ruta
    registro["accion_sistema"] = accion
    registro["prioridad_ia"] = None
    registro["numero_preguntas"] = 0
    registro["estado_simulacion"] = estado
    registro["error"] = None

    # Registrar una sola fila por caso.
    with ARCHIVO_CSV.open(
        "r", encoding="utf-8", newline=""
    ) as f:
        lector = csv.DictReader(f)
        columnas = lector.fieldnames
        filas = list(lector)

    if not columnas:
        raise ValueError("El CSV no tiene encabezados.")

    filas = [
        fila for fila in filas
        if fila["id_caso"] != id_caso
    ]

    filas.append({
        columna: registro.get(columna)
        for columna in columnas
    })

    temporal_csv = ARCHIVO_CSV.with_name(
        ARCHIVO_CSV.name + ".tmp"
    )

    with temporal_csv.open(
        "w", encoding="utf-8", newline=""
    ) as f:
        escritor = csv.DictWriter(
            f, fieldnames=columnas
        )
        escritor.writeheader()
        escritor.writerows(filas)

    os.replace(temporal_csv, ARCHIVO_CSV)
    guardar(ARCHIVO_PLAN, plan)

    print("\nRESULTADO GUARDADO")
    print("Caso:", id_caso)
    print("Pretriaje:", paciente["id_pretriage"])
    print("Ruta:", ruta)
    print("Estado:", estado)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python pruebas_simulacion/ejecutar_100.py URG-022")
        sys.exit(1)

    ejecutar(sys.argv[1])
