import csv
from datetime import datetime
from pathlib import Path
import requests

BASE_URL = "http://127.0.0.1:3000"
CARPETA = Path(__file__).resolve().parent
ARCHIVO_RESULTADOS = CARPETA / "resultados_simulaciones.csv"

POBLACIONES = {
    1: "Niño",
    2: "Adulto",
    3: "Adulto Mayor",
    4: "Embarazada",
    5: "Trauma/Accidente",
}

COLUMNAS = [
    "id_caso",
    "fecha",
    "id_pretriage",
    "poblacion",
    "prioridad_esperada",
    "prioridad_obtenida",
    "alerta_reglas",
    "revision_clinica",
    "estado",
    "observaciones",
]



def comprobar_backend():
    try:
        respuesta = requests.get(
            f"{BASE_URL}/api/health",
            timeout=10
        )
        print(f"Backend: HTTP {respuesta.status_code}")
        return respuesta.ok

    except requests.RequestException as error:
        print(f"No se pudo conectar con Urgentia: {error}")
        return False


def preparar_resultados():
    if not ARCHIVO_RESULTADOS.exists():
        with ARCHIVO_RESULTADOS.open(
            "w", newline="", encoding="utf-8-sig"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=COLUMNAS
            )
            escritor.writeheader()

    print(f"Archivo de resultados: {ARCHIVO_RESULTADOS}")
def crear_paciente_nn():
    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage",
            timeout=20
        )

        if respuesta.status_code != 201:
            print(f"Error al crear paciente NN: HTTP {respuesta.status_code}")
            print(respuesta.text[:500])
            return None

        datos = respuesta.json()

        campos = ("id_user", "id_pretriage", "access_token")

        if not all(datos.get(campo) for campo in campos):
            print("La respuesta no contiene todos los datos necesarios.")
            return None

        print("Paciente NN creado correctamente.")
        print(f"ID usuario: {datos['id_user']}")
        print(f"ID pretriage: {datos['id_pretriage']}")

        return datos

    except requests.RequestException as error:
        print(f"Error de conexión: {error}")
        return None
def guardar_antecedentes_nn(paciente, ids_antecedentes):
    id_pretriage = paciente["id_pretriage"]
    token = paciente["access_token"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage/{id_pretriage}/antecedentes",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "id_antecedentes": ids_antecedentes
            },
            timeout=20
        )

        print(f"Antecedentes: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:500])
            return False

        print("Antecedentes registrados correctamente.")
        return True

    except requests.RequestException as error:
        print(f"Error al guardar antecedentes: {error}")
        return False
def seleccionar_poblacion_nn(paciente, id_poblacion):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage/{id_pretriage}/poblacion",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_poblacion": id_poblacion
            },
            timeout=20
        )

        print(f"Población: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:500])
            return False

        print(f"Población seleccionada: {POBLACIONES[id_poblacion]}")
        return True

    except requests.RequestException as error:
        print(f"Error al seleccionar población: {error}")
        return False
def guardar_banderas_rojas_nn(paciente, ids_banderas):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage/{id_pretriage}/banderas-rojas",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_banderas": ids_banderas
            },
            timeout=20
        )

        print(f"Banderas rojas: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:500])
            return False

        print("Banderas rojas registradas correctamente.")
        return True

    except requests.RequestException as error:
        print(f"Error al guardar banderas rojas: {error}")
        return False
def evaluar_reglas_nn(paciente):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage/{id_pretriage}/evaluar-triage",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            timeout=30
        )

        print(f"Evaluación de reglas: HTTP {respuesta.status_code}")

        datos = respuesta.json()

        if not respuesta.ok:
            print("Error:", datos)
            return None

        print("Resultado de las reglas:", datos)
        return datos

    except requests.RequestException as error:
        print(f"Error al evaluar reglas: {error}")
        return None
def guardar_sintomas_nn(paciente, ids_sintomas):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage/{id_pretriage}/sintomas",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "ids_sintomas": ids_sintomas
            },
            timeout=20
        )

        print(f"Síntomas: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:500])
            return False

        print("Etapa de síntomas completada correctamente.")
        return True

    except requests.RequestException as error:
        print(f"Error al guardar síntomas: {error}")
        return False
def obtener_pregunta_ia(paciente):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage-agent/pregunta",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_pretriage": id_pretriage
            },
            timeout=60
        )

        print(f"Pregunta IA: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:1000])
            return None

        datos = respuesta.json()
        resultado = datos.get("resultado", {})

        print("Acción:", resultado.get("accion"))

        if resultado.get("accion") == "pregunta":
            print("ID pregunta:", resultado.get("id_pregunta"))
            print("Pregunta:", resultado.get("pregunta"))

        elif resultado.get("accion") == "bloque_preguntas":
            for pregunta in resultado.get("preguntas", []):
                print(
                    f"Pregunta {pregunta.get('orden')}: "
                    f"{pregunta.get('pregunta')}"
                )

        else:
            print("Respuesta IA:", resultado)

        return resultado

    except requests.RequestException as error:
        print(f"Error al obtener pregunta IA: {error}")
        return None
def enviar_primera_respuesta_nn(paciente, id_pregunta, texto_respuesta):
    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage-agent/respuestas",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_pretriage": paciente["id_pretriage"],
                "respuestas": [
                    {
                        "id_pregunta": id_pregunta,
                        "respuesta": texto_respuesta
                    }
                ]
            },
            timeout=60
        )

        print(f"Respuesta IA: HTTP {respuesta.status_code}")

        if not respuesta.ok:
            print(respuesta.text[:1000])
            return False

        print("Primera respuesta registrada correctamente.")
        print("Resultado:", respuesta.json())
        return True

    except requests.RequestException as error:
        print(f"Error al enviar respuesta IA: {error}")
        return False
def enviar_bloque_respuestas_nn(paciente, preguntas, id_caso):
    from respondedor_100 import responder_caso

    respuestas = []

    for pregunta in preguntas:
        id_pregunta = pregunta.get("id_pregunta")
        texto_pregunta = pregunta.get("pregunta")

        if not id_pregunta or not texto_pregunta:
            print("Pregunta incompleta:", pregunta)
            return False

        texto_respuesta = responder_caso(
            id_caso,
            texto_pregunta
        )

        print(f"\nCaso: {id_caso}")
        print(f"Pregunta: {texto_pregunta}")
        print(f"Respuesta: {texto_respuesta}")

        respuestas.append({
            "id_pregunta": id_pregunta,
            "respuesta": texto_respuesta
        })

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage-agent/respuestas",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_pretriage": paciente["id_pretriage"],
                "respuestas": respuestas
            },
            timeout=60
        )

        print(
            f"Bloque de respuestas: "
            f"HTTP {respuesta.status_code}"
        )

        if not respuesta.ok:
            print(respuesta.text[:1000])
            return False

        print(
            f"{len(respuestas)} respuesta(s) "
            "registradas correctamente."
        )
        return True

    except requests.RequestException as error:
        print(f"Error al enviar respuestas: {error}")
        return False
def responder_pregunta_pendiente_nn(paciente, pregunta, id_caso):
    return enviar_bloque_respuestas_nn(
        paciente,
        [pregunta],
        id_caso
    )
def evaluar_prioridad_ia_nn(paciente):
    id_pretriage = paciente["id_pretriage"]

    try:
        respuesta = requests.post(
            f"{BASE_URL}/api/pretriage-agent/evaluate",
            headers={
                "Authorization": f"Bearer {paciente['access_token']}"
            },
            json={
                "id_pretriage": id_pretriage
            },
            timeout=120
        )

        print(f"Clasificación IA: HTTP {respuesta.status_code}")

        datos = respuesta.json()

        if not respuesta.ok:
            print("Error al evaluar:", datos)
            return None

        print("\n=== RESULTADO FINAL DE URGENTIA ===")
        print("Respuesta completa:", datos)

        if datos.get("accion") == "revision_clinica":
            print("El caso requiere revisión clínica.")
            return datos

        resultado = datos.get("result", {})
        prioridad = resultado.get("prioridad")

        if prioridad:
            print(f"PRIORIDAD ASIGNADA: {prioridad}")
        else:
            print("No se encontró una prioridad en la respuesta.")

        return datos

    except requests.RequestException as error:
        print(f"Error al solicitar clasificación: {error}")
        return None
if __name__ == "__main__":
    import json

    print("=== SIMULADOR URGENTIA ===")
    print(f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}")

    preparar_resultados()

    if comprobar_backend():
        print("Preparación completada correctamente.")

        archivo_sesion = CARPETA / "sesion_nn_prueba.json"
        paciente = None

        if archivo_sesion.exists():
            with archivo_sesion.open("r", encoding="utf-8") as archivo:
                paciente = json.load(archivo)

            print(f"Continuando pretriaje NN: {paciente['id_pretriage']}")

        else:
            print("No se encontró una sesión NN existente.")
            print("No se creará otro paciente automáticamente.")

        if paciente:
            print("\n=== CONTINUANDO CUESTIONARIO DE IA ===")

            for intento in range(8):
                pregunta_ia = obtener_pregunta_ia(paciente)

                if not pregunta_ia:
                    print("No se pudo obtener la siguiente pregunta.")
                    break

                accion = pregunta_ia.get("accion")

                if accion == "pregunta_pendiente":
                    orden = pregunta_ia.get("orden")

                    if orden in (2, 3, 4, 5, 6, 7, 8):
                        print(f"\n=== RESPONDIENDO PREGUNTA {orden} ===")

                        respuestas_ok = enviar_bloque_respuestas_nn(
                            paciente,
                            [pregunta_ia]
                        )

                        if not respuestas_ok:
                            print("Se detuvo por un error al guardar la respuesta.")
                            break

                    else:
                        print(f"Pregunta {orden} sin respuesta preparada.")
                        break

                elif accion == "bloque_preguntas":
                    preguntas = pregunta_ia.get("preguntas", [])

                    preguntas_validas = [
                        p for p in preguntas
                        if p.get("orden") in (2, 3, 4, 5, 6, 7, 8)
                    ]

                    if len(preguntas_validas) != len(preguntas):
                        print("Hay preguntas sin respuesta preparada.")
                        break

                    if not enviar_bloque_respuestas_nn(
                        paciente,
                        preguntas_validas
                    ):
                        break

                elif accion == "cuestionario_completado":
                    print("Cuestionario completado.")

                    print("\n=== SOLICITANDO CLASIFICACIÓN FINAL ===")
                    evaluar_prioridad_ia_nn(paciente)

                    break

                else:
                    print("Estado del cuestionario:", accion)
                    break
    else:
        print("Verifica que el servidor Flask esté encendido.")