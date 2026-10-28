from respondedor_100 import responder_caso

casos_prueba = [
    ("URG-002", "¿Hace cuánto comenzaron los síntomas?"),
    ("URG-022", "¿Qué intensidad tiene el dolor?"),
    ("URG-062", "¿Está embarazada?"),
    ("URG-082", "¿Hace cuánto ocurrió el accidente?")
]

print("\n=== INTEGRACIÓN DE RESPUESTAS URGENTIA ===")

for id_caso, pregunta in casos_prueba:
    respuesta = responder_caso(id_caso, pregunta)

    assert respuesta and respuesta.strip()

    print(f"\nPaciente: {id_caso}")
    print(f"Pregunta IA: {pregunta}")
    print(f"Respuesta enviada: {respuesta}")

print("\nIntegración local completada correctamente.")