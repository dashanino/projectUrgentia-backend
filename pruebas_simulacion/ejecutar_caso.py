
import json
import sys
from pathlib import Path

from simular_urgentia import comprobar_backend

CARPETA = Path(__file__).resolve().parent

ARCHIVO_CASOS = CARPETA / "casos_estudio_100.json"
ARCHIVO_PLAN = CARPETA / "plan_ejecucion_100.json"

ID_CASO = "URG-002"


def cargar_json(ruta):
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def main():
    print("\n=== EJECUTOR URGENTIA ===")

    casos = cargar_json(ARCHIVO_CASOS)
    plan = cargar_json(ARCHIVO_PLAN)

    caso = next(
        (c for c in casos if c["id_caso"] == ID_CASO),
        None
    )

    registro = next(
        (r for r in plan if r["id_caso"] == ID_CASO),
        None
    )

    if caso is None or registro is None:
        print("ERROR: No se encontró el caso en los archivos.")
        sys.exit(1)

    print("\nCASO SELECCIONADO")
    print("ID:", ID_CASO)
    print("Población:", caso["poblacion"])
    print("ID población:", caso["poblacion_id"])
    print("Edad:", caso["edad"])
    print("Motivo:", caso["motivo_consulta"])
    print("Antecedentes:", caso["antecedentes_ids"])
    print("Banderas:", caso["banderas_ids"])
    print("Síntomas:", caso["sintomas_ids"])

    print("\nESTADO")
    print("Simulación:", registro["estado_simulacion"])
    print("Pretriaje:", registro["id_pretriage"])

    if (
        registro["estado_simulacion"] != "pendiente"
        or registro["id_pretriage"] is not None
    ):
        print("\nEste caso ya tiene actividad registrada.")
        print("No se iniciará una nueva sesión.")
        return

    print("\nCOMPROBANDO BACKEND")

    if not comprobar_backend():
        print("El backend no está disponible.")
        return

        print("\n=== CREANDO PACIENTE NN ===")

    from simular_urgentia import crear_paciente_nn

    paciente = crear_paciente_nn()

    if paciente is None:
        print("No se pudo confirmar la creación del paciente.")
        print("Revisa el backend antes de volver a intentar.")
        return

    # Guardar primero la sesión, incluido el token,
    # para poder continuar sin crear otro paciente.
    archivo_sesion = (
        CARPETA / f"sesion_{ID_CASO}.json"
    )

    with archivo_sesion.open("x", encoding="utf-8") as archivo:
        json.dump(
            paciente,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    # Proteger el archivo que contiene el token JWT.
    archivo_sesion.chmod(0o600)

    # Vincular el pretriaje con el caso clínico.
    registro["id_pretriage"] = paciente["id_pretriage"]
    registro["estado_simulacion"] = "iniciado"

    with ARCHIVO_PLAN.open("w", encoding="utf-8") as archivo:
        json.dump(
            plan,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    print("\n=== SESIÓN REGISTRADA ===")
    print("Caso:", ID_CASO)
    print("Pretriaje:", paciente["id_pretriage"])
    print("Estado: iniciado")
    print("Sesión guardada:", archivo_sesion.name)
    print("\nNo se enviaron antecedentes ni banderas rojas.")


if __name__ == "__main__":
    main()
