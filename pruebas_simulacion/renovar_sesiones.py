import argparse
import json
from pathlib import Path
from flask_jwt_extended import create_access_token, decode_token
from app import create_app

BASE = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()
parser.add_argument("--caso", required=True)
args = parser.parse_args()

ident = args.caso.upper()
ruta = BASE / f"sesion_{ident}.json"
control_ruta = BASE / f"control_{ident}.json"

if not ruta.exists() or not control_ruta.exists():
    raise SystemExit("Faltan archivos de sesión o control.")

sesion = json.loads(ruta.read_text(encoding="utf-8"))
control = json.loads(control_ruta.read_text(encoding="utf-8"))

id_user = sesion.get("id_user")
id_pretriage = sesion.get("id_pretriage")

if not id_user or not id_pretriage:
    raise SystemExit("Faltan identificadores originales.")

if control.get("id_pretriage") != id_pretriage:
    raise SystemExit("El pretriaje no coincide con el control.")

app = create_app()

with app.app_context():
    token_anterior = sesion.get("access_token")
    if not token_anterior:
        raise SystemExit("La sesión no tiene token anterior.")

    claims = decode_token(token_anterior, allow_expired=True)

    if str(claims.get("sub")) != str(id_user):
        raise SystemExit("La identidad del token anterior no coincide.")

    if claims.get("id_pretriage") != id_pretriage:
        raise SystemExit("El pretriaje del token anterior no coincide.")

    if claims.get("tipo_acceso") != "emergencia":
        raise SystemExit("El token anterior no es de emergencia.")

    nuevo_token = create_access_token(
        identity=str(id_user),
        additional_claims={
            "id_pretriage": id_pretriage,
            "tipo_acceso": "emergencia"
        }
    )

    sesion["access_token"] = nuevo_token

    respaldo = ruta.with_suffix(".json.bak")
    respaldo.write_text(
        ruta.read_text(encoding="utf-8"),
        encoding="utf-8"
    )

    ruta.write_text(
        json.dumps(sesion, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

print(f"Sesión renovada: {ident}")
print(f"Usuario original: {id_user}")
print(f"Pretriaje original: {id_pretriage}")
print("No se creó ningún paciente ni se modificó el backend.")
