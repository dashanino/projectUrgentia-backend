import argparse
import json
from pathlib import Path

from ejecutar_100 import ejecutar

BASE = Path(__file__).resolve().parent
PLAN = BASE / "plan_ejecucion_100.json"

ESTADOS_PROTEGIDOS = {
    "completado",
    "bloqueado_alerta_seguridad",
}

def leer_plan():
    return json.loads(PLAN.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cantidad", type=int, default=10)
    parser.add_argument("--desde", default=None)
    parser.add_argument("--ejecutar", action="store_true")
    args = parser.parse_args()

    if args.cantidad < 1:
        parser.error("--cantidad debe ser mayor que cero")

    plan = leer_plan()
    candidatos = []

    for registro in plan:
        id_caso = registro["id_caso"]

        if args.desde and id_caso < args.desde:
            continue

        if registro["estado_simulacion"] in ESTADOS_PROTEGIDOS:
            continue

        # No repetir fases ya iniciadas.
        if registro.get("id_pretriage") is not None:
            continue

        archivo_sesion = BASE / f"sesion_{id_caso}.json"
        archivo_control = BASE / f"control_{id_caso}.json"

        if archivo_sesion.exists() or archivo_control.exists():
            print(f"OMITIDO {id_caso}: existe sesión o control previo")
            continue

        candidatos.append(id_caso)

        if len(candidatos) >= args.cantidad:
            break

    print("\n=== LOTE DE SIMULACIÓN URGENTIA ===")
    print("Casos seleccionados:", len(candidatos))
    print("Modo:", "EJECUCIÓN" if args.ejecutar else "VISTA PREVIA")

    for id_caso in candidatos:
        print("-", id_caso)

    if not args.ejecutar:
        print("\nNo se creó ningún paciente.")
        print("Para ejecutar, agrega --ejecutar")
        return

    for id_caso in candidatos:
        print(f"\n{'=' * 50}")
        print("Procesando:", id_caso)

        try:
            ejecutar(id_caso)
        except Exception as error:
            print(f"DETENIDO {id_caso}: {type(error).__name__}: {error}")
            print("Revisar el caso antes de reintentarlo.")

    print("\n=== RESUMEN DEL PLAN ===")

    actualizado = leer_plan()
    conteo = {}

    for registro in actualizado:
        estado = registro["estado_simulacion"]
        conteo[estado] = conteo.get(estado, 0) + 1

    for estado, cantidad in sorted(conteo.items()):
        print(f"{estado}: {cantidad}")

if __name__ == "__main__":
    main()
