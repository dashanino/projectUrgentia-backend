"""Orquestador de pruebas de Urgentia. SOLO carpeta pruebas_simulacion.

Fase 1: llama al ejecutor existente de reglas, sin reiniciar pretriajes.
Fase 2: registra síntomas de casos con checkpoint, obtiene preguntas reales
        y prepara respuestas para revisión; NO envía respuestas ni clasifica.
"""
import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
CASOS = BASE / 'casos_estudio_100.json'
PLAN = BASE / 'plan_ejecucion_100.json'
CSV = BASE / 'resultados_evaluacion_100.csv'
COLUMNAS = ['id_caso','poblacion','prioridad_objetivo','prioridad_esperada',
            'estado_validacion','ruta_sistema','accion_sistema','prioridad_ia',
            'numero_preguntas','estado_simulacion','error']
FINAL = {'completado', 'bloqueado_alerta_seguridad'}


def leer(ruta):
    return json.loads(ruta.read_text(encoding='utf-8'))


def guardar_nuevo(ruta, datos):
    with ruta.open('x', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write('\n')


def guardar_atomico(ruta, datos):
    tmp = ruta.with_name(ruta.name + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, ruta)


def bloqueado(identificador):
    hallazgo = BASE / f'hallazgo_seguridad_{identificador}.json'
    if hallazgo.exists():
        h = leer(hallazgo)
        if h.get('continuacion_automatica_autorizada') is False:
            return 'bloqueo de seguridad documentado'
    if (BASE / f'resultado_respuesta_{identificador}_p1.json').exists():
        return 'respuesta previa enviada: requiere conciliación manual'
    return None


def sincronizar_csv():
    """Regenera SOLO el CSV de pruebas desde plan y casos; conserva campos clínicos."""
    casos = {c['id_caso']: c for c in leer(CASOS)}
    plan = {p['id_caso']: p for p in leer(PLAN)}
    if set(casos) != set(plan):
        raise ValueError('Los identificadores de casos y plan no coinciden')
    columnas = COLUMNAS
    if CSV.exists():
        with CSV.open(newline='', encoding='utf-8-sig') as f:
            actuales = csv.DictReader(f)
            if actuales.fieldnames:
                columnas = list(dict.fromkeys(actuales.fieldnames + COLUMNAS))
    tmp = CSV.with_name(CSV.name + '.tmp')
    with tmp.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        for identificador, caso in casos.items():
            p = plan[identificador]
            fila = {**caso, **p}
            # Valores de referencia pertenecen al caso, nunca al resultado del algoritmo.
            for clave in ('poblacion', 'prioridad_objetivo',
                          'prioridad_esperada', 'estado_validacion'):
                fila[clave] = caso.get(clave)
            w.writerow({k: fila.get(k) for k in columnas})
    os.replace(tmp, CSV)


def candidatos_reglas(cantidad):
    seleccion = []
    for p in leer(PLAN):
        ident = p['id_caso']
        if p.get('estado_simulacion') in FINAL or p.get('estado_simulacion') == 'pendiente_ia':
            continue
        if bloqueado(ident):
            continue
        # Nunca reiniciar un pretriaje ya iniciado con un checkpoint incompleto.
        if p.get('id_pretriage') is not None or (BASE / f'sesion_{ident}.json').exists() or (BASE / f'control_{ident}.json').exists():
            print(f'RETENIDO {ident}: pretriaje/checkpoint existente; no se duplica')
            continue
        seleccion.append(ident)
        if len(seleccion) >= cantidad:
            break
    return seleccion


def fase_reglas(cantidad, ejecutar):
    ids = candidatos_reglas(cantidad)
    print(f'FASE REGLAS | candidatos={len(ids)} | modo={"EJECUTAR" if ejecutar else "PREVISUALIZAR"}')
    print(' '.join(ids))
    if not ejecutar:
        return
    from ejecutar_100 import ejecutar as ejecutar_reglas
    for ident in ids:
        try:
            print(f'\n--- {ident} ---', flush=True)
            ejecutar_reglas(ident)
        except Exception as exc:
            print(f'RETENIDO {ident}: {type(exc).__name__}: {exc}')
            print('Verificar checkpoint/BD antes de reintentar')
        finally:
            sincronizar_csv()
    print('FASE REGLAS terminada; CSV sincronizado')


def fase_ia(cantidad, ejecutar):
    casos = {c['id_caso']: c for c in leer(CASOS)}
    ids = []
    for p in leer(PLAN):
        ident = p['id_caso']
        if p.get('estado_simulacion') != 'pendiente_ia':
            continue
        if bloqueado(ident):
            print(f'RETENIDO {ident}: {bloqueado(ident)}')
            continue
        sesion = BASE / f'sesion_{ident}.json'
        control = BASE / f'control_{ident}.json'
        if not sesion.exists() or not control.exists():
            print(f'RETENIDO {ident}: falta sesión/control local (no se recrea)')
            continue
        if (BASE / f'cuestionario_pendiente_{ident}.json').exists():
            print(f'RETENIDO {ident}: cuestionario ya consultado; revisar archivo')
            continue
        ids.append(ident)
        if len(ids) >= cantidad:
            break
    print(f'FASE IA | candidatos={len(ids)} | modo={"CONSULTAR" if ejecutar else "PREVISUALIZAR"}')
    print(' '.join(ids))
    if not ejecutar:
        return
    from simular_urgentia import guardar_sintomas_nn, obtener_pregunta_ia
    from respondedor_100 import responder_caso
    for ident in ids:
        try:
            p = next(x for x in leer(PLAN) if x['id_caso'] == ident)
            paciente = leer(BASE / f'sesion_{ident}.json')
            ruta_control = BASE / f'control_{ident}.json'
            control = leer(ruta_control)
            if paciente.get('id_pretriage') != p.get('id_pretriage') or control.get('id_pretriage') != p.get('id_pretriage'):
                raise ValueError('IDs de pretriaje inconsistentes')
            accion = (control.get('resultado_reglas') or {}).get('accion')
            if not control.get('reglas_evaluadas') or accion not in ('continuar_submenu','continuar_ia'):
                raise ValueError(f'Reglas no permiten esta fase: {accion}')
            if not control.get('sintomas_registrados'):
                ids_sintomas = casos[ident].get('sintomas_ids')
                if not isinstance(ids_sintomas, list):
                    raise ValueError('IDs de síntomas no definidos')
                # [] es una selección técnica vacía, NO equivale a ausencia de síntomas.
                if not guardar_sintomas_nn(paciente, ids_sintomas):
                    raise RuntimeError('Síntomas no confirmados; comprobar BD antes de reintentar')
                control['sintomas_registrados'] = True
                guardar_atomico(ruta_control, control)
            respuesta = obtener_pregunta_ia(paciente)
            if not isinstance(respuesta, dict):
                raise RuntimeError('No se confirmó cuestionario; revisar BD antes de reintentar')
            accion_ia = respuesta.get('accion')
            if accion_ia == 'bloque_preguntas':
                preguntas = respuesta.get('preguntas', [])
            elif accion_ia in ('pregunta', 'pregunta_pendiente'):
                preguntas = [respuesta]
            else:
                preguntas = []
            propuestas = []
            for q in preguntas:
                texto = q.get('pregunta')
                if not q.get('id_pregunta') or not texto:
                    raise ValueError('Pregunta sin ID/texto')
                propuestas.append({'id_pregunta': q['id_pregunta'],
                                   'pregunta': texto,
                                   'respuesta_sugerida_no_validada': responder_caso(ident, texto)})
            salida = {'id_caso': ident, 'id_pretriage': p['id_pretriage'],
                      'accion_ia': accion_ia, 'preguntas': propuestas,
                      'respuesta_original_ia': respuesta,
                      'estado': 'pendiente_revision_humana',
                      'respuestas_enviadas': False}
            guardar_nuevo(BASE / f'cuestionario_pendiente_{ident}.json', salida)
            print(f'{ident}: cuestionario guardado; {len(propuestas)} preguntas; NO se enviaron respuestas')
        except Exception as exc:
            print(f'RETENIDO {ident}: {type(exc).__name__}: {exc}')
            print('No reintentar sin verificar estado remoto si hubo una solicitud HTTP')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fase', choices=('reglas','ia','reporte'), required=True)
    parser.add_argument('--cantidad', type=int, default=100)
    parser.add_argument('--ejecutar', action='store_true', help='Permite solicitudes al backend')
    a = parser.parse_args()
    if a.cantidad < 1:
        parser.error('--cantidad debe ser positivo')
    if a.fase == 'reglas':
        fase_reglas(a.cantidad, a.ejecutar)
    elif a.fase == 'ia':
        fase_ia(a.cantidad, a.ejecutar)
    else:
        sincronizar_csv()
    print('ESTADOS:', dict(Counter(x.get('estado_simulacion') for x in leer(PLAN))))


if __name__ == '__main__':
    main()
