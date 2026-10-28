"""Preparación conservadora para revisión humana; NO realiza solicitudes HTTP."""
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENTRADA = BASE / 'revision_clinica_37.json'
SALIDA = BASE / 'respuestas_especificas_37.json'
FALTANTE = 'No se dispone de información clínica documentada para responder esta pregunta.'

# Conceptos que conectan preguntas con expresiones frecuentes de las historias.
CONCEPTOS = {
 'edad': ['edad', 'anos'], 'peso': ['peso', 'pesa', 'kg'],
 'inicio': ['inicio', 'comenzo', 'comenz', 'desde cuando', 'hace cuanto', 'aparecio', 'repentina', 'subita', 'gradual'],
 'duracion': ['duracion', 'dura', 'desde cuando', 'hace cuanto', 'tiempo', 'episodio'],
 'localizacion': ['donde', 'parte', 'zona', 'localiza', 'localizacion', 'bilateral', 'ombligo', 'difuso'],
 'intensidad': ['intensidad', 'fuerte', 'escala', '0 a 10', 'maxima'],
 'evolucion': ['empeor', 'mejor', 'aument', 'disminu', 'igual', 'cambi', 'constante', 'intermitente', 'continuo'],
 'fiebre': ['fiebre', 'temperatura'], 'respiracion': ['respira', 'disnea', 'aire', 'costillas', 'quejido'],
 'vomitos': ['vomit', 'nausea'], 'diarrea': ['diarrea', 'evacua', 'heces', 'estrenimiento'],
 'orina': ['orin', 'urin', 'miccion'], 'alimentacion': ['comer', 'come', 'comida', 'aliment', 'apetito', 'liquido', 'beber', 'bebe', 'hidrata'],
 'actividad': ['actividad', 'activo', 'caminar', 'mover', 'juega', 'comportamiento', 'despierto', 'somnolencia'],
 'neurologia': ['confusion', 'confund', 'debilidad', 'fuerza', 'hablar', 'vision', 'desmayo', 'conocimiento', 'equilibrio', 'hormigueo', 'orientad'],
 'dolor': ['dolor', 'molestia', 'cefalea'], 'trauma': ['accidente', 'lesion', 'golpe', 'caida', 'fractura'],
 'sangrado': ['sangrado', 'sangre', 'hemorragia'], 'embarazo': ['embarazo', 'embarazada', 'menstruacion'],
 'medicacion': ['medicamento', 'medicacion', 'dosis', 'toma', 'tratamiento', 'analgesico'],
 'pecho': ['pecho', 'toracico', 'torax'], 'cuello': ['cuello', 'rigidez'],
 'piel': ['piel', 'palidez', 'manchas', 'morados', 'azulados'],
}
STOP = set('que cual cuando como donde desde hace esta este estos estas tiene tenido han has para sobre alguna algun alguna una unos unas del las los por con sin entre hacia puede presenta presentado parte normal normalmente ahora durante inicio caso paciente niño niña adulto mujer hombre dolor'.split())

def normal(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).lower()) if unicodedata.category(c) != 'Mn')

def palabras(s):
    return {w for w in re.findall(r'[a-z]{4,}', normal(s)) if w not in STOP}

def conceptos(s):
    n = normal(s)
    return {k for k, variants in CONCEPTOS.items() if any(v in n for v in variants)}

def oraciones(historia):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])', historia.strip()) if s.strip()]

def responder(ficha, pregunta):
    q = normal(pregunta)
    qc = conceptos(pregunta)
    qt = palabras(pregunta)
    hallazgos = []
    # La edad es un dato explícito independiente de la redacción de la historia.
    if 'edad' in qc and isinstance(ficha.get('edad'), (int, float)):
        hallazgos.append(f"Edad documentada: {ficha['edad']} años.")
    hist = ficha.get('historia_clinica') or ''
    # Selecciona citas literales pertinentes; nunca infiere negaciones.
    candidatos = []
    for idx, s in enumerate(oraciones(hist)):
        sc = conceptos(s)
        st = palabras(s)
        comunes = qc & sc
        overlap = sum(any(t.startswith(w[:5]) or w.startswith(t[:5]) for w in st) for t in qt)
        # Conceptos amplios como dolor no bastan para responder una pregunta de signos específicos.
        especificos = (qc - {'dolor', 'inicio', 'duracion', 'localizacion', 'intensidad', 'evolucion'})
        if especificos and not (especificos & sc) and overlap < 2:
            continue
        puntuacion = 3 * len(comunes) + overlap
        if puntuacion >= 3:
            candidatos.append((puntuacion, idx, s))
    candidatos.sort(key=lambda x: (-x[0], x[1]))
    # Máximo dos frases originales; evita reproducir toda la ficha.
    for _, _, frase in candidatos[:2]:
        hallazgos.append(frase)
    # No presenta la respuesta como completa si hay subpreguntas no cubiertas.
    if not hallazgos:
        return FALTANTE, [], True
    return ('Información documentada: ' + ' '.join(hallazgos) +
            ' Los aspectos de la pregunta no descritos explícitamente permanecen sin documentar.'), hallazgos, True

def main():
    if not ENTRADA.exists():
        raise SystemExit(f'Falta {ENTRADA}. Debe contener las 37 fichas y preguntas originales.')
    casos = json.loads(ENTRADA.read_text(encoding='utf-8'))
    assert len(casos) == 37, 'Se esperaban exactamente 37 casos'
    salida = []
    vacias = 0
    for caso in casos:
        ficha = caso['ficha_clinica']
        assert ficha and ficha['id_caso'] == caso['id_caso']
        respuestas = []
        for r in caso['preguntas']:
            respuesta, evidencia, revision = responder(ficha, r['pregunta'])
            vacias += not bool(evidencia)
            respuestas.append({
                'id_pregunta': r['id_pregunta'], 'pregunta': r['pregunta'],
                'respuesta': respuesta, 'evidencia_literal': evidencia,
                'requiere_revision_clinica': revision,
                'tipo_respuesta': 'seleccion_literal_conservadora',
            })
        salida.append({'id_caso': caso['id_caso'],
                       'id_pretriage': next((x['id_pretriage'] for x in json.loads((BASE/'respuestas_mejoradas_37.json').read_text(encoding='utf-8')) if x['id_caso']==caso['id_caso']), None) if (BASE/'respuestas_mejoradas_37.json').exists() else None,
                       'respuestas': respuestas, 'estado': 'preparado_no_enviado'})
    total = sum(len(x['respuestas']) for x in salida)
    assert total == 148, f'Se esperaban 148 preguntas, hay {total}'
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Casos: {len(salida)} | Preguntas: {total}')
    print(f'Sin evidencia encontrada: {vacias} | Con evidencia candidata: {total-vacias}')
    print('Todas las respuestas requieren revisión clínica antes del envío.')
    print('Archivo:', SALIDA)
    print('Sin solicitudes HTTP. No se modificó el backend ni los archivos originales.')

if __name__ == '__main__':
    main()
