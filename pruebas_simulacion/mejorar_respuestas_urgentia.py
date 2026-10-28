"""Prepara respuestas de simulación basadas en texto clínico original.
NO realiza peticiones HTTP ni cambia el motor clínico.
Ejecutar desde backend: python pruebas_simulacion/mejorar_respuestas_urgentia.py
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
ORIGEN = BASE / 'revision_clinica_37.json'
DESTINO = BASE / 'respuestas_preparadas_37.json'

if not ORIGEN.is_file() or not DESTINO.is_file():
    raise SystemExit('Faltan revision_clinica_37.json o respuestas_preparadas_37.json en pruebas_simulacion')

revision = json.loads(ORIGEN.read_text(encoding='utf-8'))
preparadas = json.loads(DESTINO.read_text(encoding='utf-8'))
if not isinstance(revision, list) or not isinstance(preparadas, list):
    raise SystemExit('Formato de archivos no esperado')

por_caso = {c['id_caso']: c for c in revision}
if len(por_caso) != 37 or len(preparadas) != 37:
    raise SystemExit('Se esperaban 37 casos distintos; no se modificó nada')

n = 0
for caso in preparadas:
    ident = caso['id_caso']
    if ident not in por_caso:
        raise SystemExit(f'Falta ficha para {ident}')
    ficha = por_caso[ident].get('ficha_clinica') or {}
    historia = ficha.get('historia_clinica')
    if not isinstance(historia, str) or not historia.strip():
        raise SystemExit(f'Falta historia clínica en {ident}')
    ids_originales = {p['id_pregunta'] for p in por_caso[ident]['preguntas']}
    ids_actuales = {p['id_pregunta'] for p in caso['respuestas']}
    if ids_originales != ids_actuales or len(ids_actuales) != 4:
        raise SystemExit(f'Las preguntas cambiaron para {ident}; no se modificó nada')

# Solo tras validar todos los casos, escribir un archivo NUEVO, no sobreescribir el original.
mejoradas = []
for caso in preparadas:
    ficha = por_caso[caso['id_caso']]['ficha_clinica']
    historia = ficha['historia_clinica'].strip()
    respuestas = []
    for pregunta in caso['respuestas']:
        respuestas.append({
            'id_pregunta': pregunta['id_pregunta'],
            'pregunta': pregunta['pregunta'],
            'respuesta': (
                'Información documentada en el caso simulado: ' + historia +
                ' Los detalles solicitados que no estén descritos explícitamente '
                'en esta historia no se encuentran documentados.'
            ),
            'tipo_respuesta': 'historia_clinica_literal_con_limites',
            'requiere_revision_clinica': True,
            'fuente': 'ficha_clinica.historia_clinica'
        })
        n += 1
    mejoradas.append({
        'id_caso': caso['id_caso'],
        'id_pretriage': caso['id_pretriage'],
        'respuestas': respuestas,
        'estado': 'preparado_no_enviado'
    })

salida = BASE / 'respuestas_mejoradas_37.json'
salida.write_text(json.dumps(mejoradas, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Casos: {len(mejoradas)} | Respuestas: {n}')
print('Salida:', salida)
print('Sin solicitudes HTTP. No se alteraron los registros originales.')
print('AVISO: Las respuestas reproducen la historia completa, no una extracción pregunta por pregunta.')
