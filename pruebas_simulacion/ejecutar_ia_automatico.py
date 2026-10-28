import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from flask_jwt_extended import create_access_token, decode_token

from app import create_app
from pruebas_simulacion.respondedor_100 import responder_caso

BASE = Path(__file__).resolve().parent
URL = "http://127.0.0.1:3000"
REPORTE = BASE / "resultados_ia_automaticos.csv"
APP = create_app()

CAMPOS = [
    "id_caso", "id_pretriage", "estado", "preguntas_enviadas",
    "tiempo_http_segundos", "codigo_http", "detalle"
]


def leer(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))


def guardar(ruta, datos):
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    temporal.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    os.replace(temporal, ruta)


def registrar(fila):
    nuevo = not REPORTE.exists()
    with REPORTE.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        if nuevo:
            escritor.writeheader()
        escritor.writerow({k: fila.get(k, "") for k in CAMPOS})


def renovar(sesion):
    anterior = sesion["access_token"]

    with APP.app_context():
        claims = decode_token(anterior, allow_expired=True)

        if str(claims.get("sub")) != str(sesion["id_user"]):
            raise ValueError("Usuario del token no coincide")

        if str(claims.get("id_pretriage")) != str(sesion["id_pretriage"]):
            raise ValueError("Pretriaje del token no coincide")

        if claims.get("tipo_acceso") != "emergencia":
            raise ValueError("Token no corresponde a emergencia")

        return create_access_token(
            identity=str(sesion["id_user"]),
            additional_claims={
                "id_pretriage": sesion["id_pretriage"],
                "tipo_acceso": "emergencia"
            }
        )


def solicitar(ruta, sesion, contenido):
    inicio = time.perf_counter()

    try:
        respuesta = requests.post(
            URL + ruta,
            headers={
                "Authorization": f"Bearer {sesion['access_token']}"
            },
            json=contenido,
            timeout=60
        )
        duracion = round(time.perf_counter() - inicio, 4)

        try:
            datos = respuesta.json()
        except ValueError:
            datos = {"texto": respuesta.text[:300]}

        return respuesta.status_code, datos, duracion

    except requests.RequestException as error:
        duracion = round(time.perf_counter() - inicio, 4)
        return None, {"error": str(error)}, duracion


def preguntas_de(resultado):
    accion = resultado.get("accion")

    if accion == "bloque_preguntas":
        return resultado.get("preguntas", [])

    if accion in ("pregunta", "pregunta_pendiente"):
        return [resultado]

    return []


def revisar_seguridad(resultado):
    revision = resultado.get("revision_seguridad") or {}

    return (
        revision.get("requiere_aclaracion") is True
        or revision.get("accion") not in (None, "continuar")
        or resultado.get("requiere_aclaracion") is True
    )


def procesar(ident, plan):
    sesion_ruta = BASE / f"sesion_{ident}.json"
    control_ruta = BASE / f"control_{ident}.json"
    cuestionario_ruta = BASE / f"cuestionario_pendiente_{ident}.json"
    registro_ruta = BASE / f"respuestas_supervisadas_{ident}.json"
    resultado_ruta = BASE / f"resultado_automatico_{ident}.json"

    if resultado_ruta.exists():
        anterior = leer(resultado_ruta)

        if anterior.get("estado") != "requiere_dato_clinico":
            return "OMITIDO", "Caso ya procesado o requiere conciliación"

        # Solo reanudar casos detenidos por datos faltantes
        # si no existe ninguna solicitud HTTP de envío registrada.
        if any(
            evento.get("evento") == "resultado_http"
            for evento in anterior.get("interacciones", [])
        ):
            return "OMITIDO", "Existe resultado HTTP previo; requiere conciliación"

    if registro_ruta.exists():
        return "OMITIDO", "Tiene historial supervisado; requiere conciliación"

    if (BASE / f"hallazgo_seguridad_{ident}.json").exists():
        return "OMITIDO", "Tiene hallazgo de seguridad"

    if not all(p.exists() for p in (
        sesion_ruta, control_ruta, cuestionario_ruta
    )):
        return "OMITIDO", "Faltan archivos de sesión, control o cuestionario"

    sesion = leer(sesion_ruta)
    control = leer(control_ruta)
    cuestionario = leer(cuestionario_ruta)

    esperado = plan.get("id_pretriage")

    if any(str(x.get("id_pretriage")) != str(esperado)
           for x in (sesion, control, cuestionario)):
        return "OMITIDO", "Identificadores inconsistentes"

    if not control.get("reglas_evaluadas"):
        return "OMITIDO", "Reglas no evaluadas"

    accion_reglas = (control.get("resultado_reglas") or {}).get("accion")

    if accion_reglas not in ("continuar_submenu", "continuar_ia"):
        return "OMITIDO", "Reglas no autorizan IA"

    sesion["access_token"] = renovar(sesion)

    # Guardamos un token renovado para la sesión existente.
    guardar(sesion_ruta, sesion)

    registro = {
        "id_caso": ident,
        "id_pretriage": esperado,
        "estado": "iniciado",
        "interacciones": [],
        "fecha_inicio": datetime.now(timezone.utc).isoformat()
    }

    guardar(resultado_ruta, registro)

    respuesta_ia = cuestionario.get("respuesta_original_ia") or {}
    total = 0

    for vuelta in range(15):
        if not preguntas_de(respuesta_ia):
            if revisar_seguridad(respuesta_ia):
                registro["estado"] = "revision_seguridad"
                break

            # Sin preguntas, no asumimos que el triaje terminó.
            registro["estado"] = "sin_preguntas"
            break

        preguntas = preguntas_de(respuesta_ia)
        respuestas = []

        for pregunta in preguntas:
            pid = pregunta.get("id_pregunta")
            texto = pregunta.get("pregunta")

            if not pid or not texto:
                registro["estado"] = "pregunta_incompleta"
                guardar(resultado_ruta, registro)
                return "RETENIDO", "Pregunta incompleta"

            sugerencia = responder_caso(ident, texto)

            if (
                not isinstance(sugerencia, str)
                or not sugerencia.strip()
                or sugerencia.strip().lower() in (
                    "no lo sé.", "no lo se.", "desconocido"
                )
            ):
                sugerencia = (
                    "No se dispone de información clínica documentada "
                    "para responder esta pregunta."
                )
                registro.setdefault("datos_faltantes", []).append({
                    "id_pregunta": pid,
                    "pregunta": texto,
                    "respuesta": sugerencia
                })

            respuestas.append({
                "id_pregunta": pid,
                "respuesta": sugerencia
            })

        # Checkpoint ANTES del envío para evitar duplicaciones.
        registro["estado"] = "envio_incierto"
        registro["interacciones"].append({
            "evento": "intento_envio",
            "respuestas": respuestas
        })
        guardar(resultado_ruta, registro)

        codigo, datos, duracion = solicitar(
            "/api/pretriage-agent/respuestas",
            sesion,
            {
                "id_pretriage": esperado,
                "respuestas": respuestas
            }
        )

        evento = {
            "evento": "resultado_http",
            "codigo_http": codigo,
            "tiempo_http_segundos": duracion,
            "respuesta_backend": datos
        }

        registro["interacciones"].append(evento)

        if codigo != 200:
            registro["estado"] = "envio_incierto"
            break

        total += len(respuestas)
        registro["estado"] = "respuesta_confirmada"
        guardar(resultado_ruta, registro)

        resultado = datos.get("resultado", datos)

        if revisar_seguridad(resultado):
            registro["estado"] = "revision_seguridad"
            break

        # Consultar la siguiente pregunta del backend.
        codigo, datos, duracion = solicitar(
            "/api/pretriage-agent/pregunta",
            sesion,
            {"id_pretriage": esperado}
        )

        registro["interacciones"].append({
            "evento": "consulta_siguiente_pregunta",
            "codigo_http": codigo,
            "tiempo_http_segundos": duracion,
            "respuesta_backend": datos
        })

        if codigo != 200:
            registro["estado"] = "consulta_incierta"
            break

        respuesta_ia = datos.get("resultado", datos)

        if revisar_seguridad(respuesta_ia):
            registro["estado"] = "revision_seguridad"
            break

    else:
        registro["estado"] = "limite_preguntas"

    registro["preguntas_enviadas"] = total
    guardar(resultado_ruta, registro)

    tiempos = [
        x.get("tiempo_http_segundos", 0)
        for x in registro["interacciones"]
        if x.get("tiempo_http_segundos") is not None
    ]

    codigos = [
        x.get("codigo_http")
        for x in registro["interacciones"]
        if x.get("codigo_http") is not None
    ]

    registrar({
        "id_caso": ident,
        "id_pretriage": esperado,
        "estado": registro["estado"],
        "preguntas_enviadas": total,
        "tiempo_http_segundos": round(sum(tiempos), 4),
        "codigo_http": codigos[-1] if codigos else "",
        "detalle": ""
    })

    return registro["estado"], f"{total} respuestas"


def main():
    planes = leer(BASE / "plan_ejecucion_100.json")

    candidatos = [
        p for p in planes
        if p.get("estado_simulacion") == "pendiente_ia"
    ]

    print(f"Casos pendientes de IA: {len(candidatos)}")

    for numero, plan in enumerate(candidatos, 1):
        ident = plan["id_caso"]
        print(f"[{numero}/{len(candidatos)}] {ident}", flush=True)

        try:
            estado, detalle = procesar(ident, plan)
            print(f"  {estado}: {detalle}", flush=True)

        except Exception as error:
            print(
                f"  ERROR: {type(error).__name__}: {error}",
                flush=True
            )

    print("\nEjecución terminada.")
    print("Reporte:", REPORTE)


if __name__ == "__main__":
    main()
