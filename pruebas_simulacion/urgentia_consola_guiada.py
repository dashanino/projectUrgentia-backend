#!/usr/bin/env python3
"""Urgentia: respuestas supervisadas por consola. No modifica app/.
Copiar a backend/pruebas_simulacion/. Ejecutar desde backend.
"""
import argparse, csv, json, os, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE=Path(__file__).resolve().parent
URL='http://127.0.0.1:3000'

def leer(p): return json.loads(p.read_text(encoding='utf-8'))
def guardar(p,obj):
    t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); os.replace(t,p)
def marca(): return datetime.now(timezone.utc).isoformat()
def respuesta_sugerida(caso,pregunta):
    q=pregunta.casefold()
    if ('principal motivo' in q and ('urgencias' in q or 'acudir' in q)) or 'qué te está pasando' in q:
        return caso.get('historia_clinica','').strip()
    return ''  # Nunca inferir negaciones ni asociar respuestas por orden.

def imprimir_ficha(caso,ficha):
    print('\n'+'='*70)
    print(f"CASO {caso['id_caso']} | {caso.get('poblacion')} | edad {caso.get('edad')} | {caso.get('sexo')}")
    print('MOTIVO:',caso.get('motivo_consulta'))
    print('HISTORIA:',caso.get('historia_clinica'))
    d=ficha.get('datos_clinicos',{})
    for titulo,k in [('Inicio','inicio'),('Duración','duracion'),('Intensidad','intensidad_dolor'),('Localización','localizacion'),('Evolución','evolucion'),('Asociados','sintomas_asociados'),('Negados explícitos','sintomas_negados'),('Antecedentes','antecedentes'),('Signos vitales','signos_vitales'),('Signos alarma','signos_alarma')]:
        v=d.get(k)
        if v not in (None,[],{},''): print(f'{titulo}: {v}')
    print('ESTADO FICHA:',ficha.get('estado_extraccion','sin revisar'))
    print('ATENCIÓN: ausencia de un dato NO equivale a negación. La ficha puede estar incompleta.')

def bloqueado(ident):
    h=BASE/f'hallazgo_seguridad_{ident}.json'
    if h.exists() and leer(h).get('continuacion_automatica_autorizada') is False: return 'bloqueo de seguridad documentado'
    if ident=='URG-039': return 'bloqueo de seguridad previo'
    if (BASE/f'resultado_respuesta_{ident}_p1.json').exists(): return 'respuesta previa detectada; conciliar manualmente'
    return None

def preguntas_del_resultado(r):
    a=r.get('accion')
    if a=='bloque_preguntas': return r.get('preguntas') or []
    if a in ('pregunta','pregunta_pendiente'): return [r]
    return []

def llamada(ruta,sesion,payload,timeout=75):
    inicio=time.perf_counter()
    try:
        r=requests.post(URL+ruta,headers={'Authorization':'Bearer '+sesion['access_token']},json=payload,timeout=timeout)
    except requests.RequestException as e:
        print('CONEXIÓN INCIERTA:',type(e).__name__,'No reintentar sin verificar BD.'); return None,round(time.perf_counter()-inicio,4)
    dur=round(time.perf_counter()-inicio,4)
    try: datos=r.json()
    except ValueError: datos={'mensaje':r.text[:400]}
    if not r.ok:
        print('HTTP',r.status_code, str(datos)[:600]);return None,dur
    return datos,dur

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--caso',required=True,help='Ej: URG-005')
    ap.add_argument('--max-preguntas',type=int,default=8)
    a=ap.parse_args(); ident=a.caso.upper()
    if a.max_preguntas<1 or a.max_preguntas>20: ap.error('max-preguntas entre 1 y 20')
    casos={x['id_caso']:x for x in leer(BASE/'casos_estudio_100.json')}
    fichas={x['id_caso']:x for x in leer(BASE/'fichas_clinicas_100.json')}
    plan={x['id_caso']:x for x in leer(BASE/'plan_ejecucion_100.json')}
    if ident not in casos: ap.error('Caso no encontrado')
    if bloqueado(ident): ap.error(f'{ident} retenido: {bloqueado(ident)}')
    p=plan[ident]
    if p.get('estado_simulacion')!='pendiente_ia': ap.error('Caso no está pendiente_ia; no se modifica')
    sp=BASE/f'sesion_{ident}.json'; cp=BASE/f'control_{ident}.json'; qp=BASE/f'cuestionario_pendiente_{ident}.json'
    if not (sp.exists() and cp.exists() and qp.exists()): ap.error('Falta sesión, control o cuestionario; no se recrea')
    sesion,control,q=leer(sp),leer(cp),leer(qp)
    if any(x.get('id_pretriage')!=p.get('id_pretriage') for x in (sesion,control,q)):
        ap.error('ID de pretriaje inconsistente')
    if not control.get('reglas_evaluadas') or not control.get('sintomas_registrados'):
        ap.error('Reglas/síntomas no confirmados')
    registro=BASE/f'respuestas_supervisadas_{ident}.json'
    datos=leer(registro) if registro.exists() else {'id_caso':ident,'id_pretriage':p['id_pretriage'],'interacciones':[],'estado':'en_curso'}
    if datos['id_pretriage']!=p['id_pretriage']: ap.error('Registro no coincide')
    if datos.get('estado') in ('envio_incierto','error_http'):
        ap.error('Hay un envío incierto; conciliar con BD antes de continuar')
    imprimir_ficha(casos[ident],fichas.get(ident,{}))
    print('\nLos datos de la ficha son orientación para revisión humana, NO verdad clínica validada.')
    print('El programa SOLO envía una respuesta cuando confirmas expresamente con S.')
    if input('¿Continuar con este paciente? [s/N]: ').strip().lower()!='s': return
    pregunta_cache=q.get('respuesta_original_ia',{})
    for _ in range(a.max_preguntas):
        if pregunta_cache:
            r=pregunta_cache; pregunta_cache=None
        else:
            datos_api,tiempo=llamada('/api/pretriage-agent/pregunta',sesion,{'id_pretriage':p['id_pretriage']})
            datos['interacciones'].append({'evento':'consulta_pregunta','duracion_seg':tiempo,'fecha':marca()})
            guardar(registro,datos)
            if datos_api is None: print('Detenido.'); return
            r=datos_api.get('resultado',datos_api)
        qs=preguntas_del_resultado(r)
        if not qs:
            print('Sin nuevas preguntas. Acción:',r.get('accion'),'Detalles:',str(r)[:700]);break
        for pregunta in qs:
            pid=pregunta.get('id_pregunta'); txt=pregunta.get('pregunta')
            if not pid or not txt: print('Pregunta incompleta, detenido');return
            if any(x.get('evento')=='respuesta_confirmada' and x.get('id_pregunta')==pid for x in datos['interacciones']):
                print('Pregunta ya enviada según registro local:',pid,'; detener para evitar duplicado');return
            print('\n'+'-'*70+'\nPREGUNTA',pid,':',txt)
            propuesta=respuesta_sugerida(casos[ident],txt)
            if propuesta: print('SUGERENCIA (solo historia textual, NO validada):',propuesta)
            else: print('SIN RESPUESTA SEGURA AUTOMÁTICA: consulta la ficha y escribe tú.')
            print('Escribe respuesta, Enter para usar sugerencia si existe, /desconocido, o /salir.')
            entrada=input('Respuesta: ').strip()
            if entrada=='/salir': print('Guardado; sin enviar esta pregunta');return
            if entrada=='/desconocido': entrada='No se dispone de esa información en la historia clínica simulada.'
            if not entrada: entrada=propuesta
            if not entrada: print('Sin respuesta: detenido sin enviar');return
            print('SE ENVIARÍA:',entrada)
            if input('Confirmar envío real a Urgentia [S/n]: ').strip()!='S':
                print('Detenido sin enviar esta respuesta');return
            # Guardar intento ANTES de HTTP: ante un timeout no repetir automáticamente.
            datos['estado']='envio_incierto'
            datos['interacciones'].append({'evento':'intento_envio','id_pregunta':pid,'pregunta':txt,'respuesta':entrada,'fecha':marca()})
            guardar(registro,datos)
            resp,t=llamada('/api/pretriage-agent/respuestas',sesion,{'id_pretriage':p['id_pretriage'],'respuestas':[{'id_pregunta':pid,'respuesta':entrada}]})
            datos['interacciones'].append({'evento':'respuesta_confirmada' if resp is not None else 'envio_no_confirmado','id_pregunta':pid,'duracion_seg':t,'fecha':marca(),'resultado':resp})
            datos['estado']='en_curso' if resp is not None else 'envio_incierto'
            guardar(registro,datos)
            if resp is None: print('DETENIDO: comprobar BD antes de reintentar');return
            print('Respuesta confirmada; duración HTTP:',t,'s')
            rev=resp.get('revision_seguridad') or {}
            if rev.get('requiere_aclaracion') or rev.get('accion') not in (None,'continuar'):
                print('ALERTA/ACLARACIÓN DE SEGURIDAD:',rev)
                datos['estado']='revision_seguridad';guardar(registro,datos)
                print('Detenido para revisión; no se enviarán más respuestas.');return
            result=resp.get('resultado') or {}
            if result.get('accion') not in (None,'revision_seguridad_pendiente','continuar'):
                print('Resultado del backend:',result)
                if result.get('accion') in ('revision_clinica','alerta'):
                    datos['estado']='revision_seguridad';guardar(registro,datos);return
        if input('\n¿Consultar siguiente pregunta? [s/N]: ').strip().lower()!='s': break
    print('\nSesión guardada en',registro.name)
    print('No se ejecutó clasificación final automáticamente; requiere confirmación separada.')

if __name__=='__main__': main()
