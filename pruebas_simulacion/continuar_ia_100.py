import json
import sys
from pathlib import Path

from simular_urgentia import (
    guardar_sintomas_nn,
    obtener_pregunta_ia,
)
from respondedor_100 import responder_caso

CARPETA = Path(__file__).resolve().parent


def leer(ruta):
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(ruta, datos):
    temporal = ruta.with_suffix(".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
    temporal.replace(ruta)


def continuar(id_caso):
    casos = leer(CARPETA / "casos_estudio_100.json")
    plan = leer(CARPETA / "plan_ejecucion_100.json")

    caso = next(
        (c for c in casos if c["id_caso"] == id_caso),
        None
    )
    registro = next(
        (r for r in plan if r["id_caso"] == id_caso),
        None
    )

    if caso is None or registro is None:
        raise ValueError("Caso no encontrado.")

    if registro["estado_simulacion"] != "pendiente_ia":
        print(
            "Caso no disponible para continuar:",
            registro["estado_simulacion"]
        )
        return

    archivo_sesion = CARPETA / f"sesion_{id_caso}.json"
    archivo_control = CARPETA / f"control_{id_caso}.json"

    if not archivo_sesion.exists() or not archivo_control.exists():
        raise ValueError(
            "Faltan archivos de sesión o control. "
            "No se creará otro paciente."
        )

    paciente = leer(archivo_sesion)
    control = leer(archivo_control)

    if paciente["id_pretriage"] != registro["id_pretriage"]:
        raise ValueError("ID de pretriaje inconsistente.")

    if control.get("resultado_reglas", {}).get("accion") != "continuar_ia":
        raise ValueError(
            "El resultado de reglas no permite continuar con IA."
        )

    print("\n=== CONTINUACIÓN IA ===")
    print("Caso:", id_caso)
    print("Pretriaje:", paciente["id_pretriage"])
    print("Motivo:", caso["motivo_consulta"])

    if not control.get("sintomas_registrados"):
        print("\nRegistrando síntomas...")

        if not guardar_sintomas_nn(
            paciente,
            caso["sintomas_ids"]
        ):
            raise RuntimeError(
                "No se confirmó el registro de síntomas. "
                "Verifica el backend antes de reintentar."
            )

        control["sintomas_registrados"] = True
        guardar(archivo_control, control)

    print("\nConsultando cuestionario IA...")

    resultado = obtener_pregunta_ia(paciente)

    if not resultado:
        raise RuntimeError(
            "No se recibió una respuesta válida del backend."
        )

    print("Acción:", resultado.get("accion"))

    if resultado.get("accion") == "bloque_preguntas":
        preguntas = resultado.get("preguntas", [])
    elif resultado.get("accion") in (
        "pregunta",
        "pregunta_pendiente"
    ):
        preguntas = [resultado]
    else:
        print("Estado del cuestionario:", resultado)
        return

    for pregunta in preguntas:
        texto = pregunta.get("pregunta", "")
        respuesta = responder_caso(id_caso, texto)

        print("\n-----------------------------")
        print("ID pregunta:", pregunta.get("id_pregunta"))
        print("Orden:", pregunta.get("orden"))
        print("Pregunta:", texto)
        print("Respuesta propuesta:", respuesta)

        if not respuesta or respuesta.strip().lower() in (
            "no lo sé", "no lo se", "no sé", "no se"
        ):
            print("REQUIERE REVISIÓN CLÍNICA")

    print("\nNo se enviaron respuestas a Urgentia.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Uso: python pruebas_simulacion/"
            "continuar_ia_100.py URG-039"
        )
        sys.exit(1)

    continuar(sys.argv[1])
