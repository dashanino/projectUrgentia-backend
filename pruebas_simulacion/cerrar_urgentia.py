"""Consolida resultados de reglas y evalúa IA solo cuando todas las preguntas registradas tienen respuesta.
No envía respuestas, no crea pacientes y no cambia estados manualmente.
Ejecutar desde backend: PYTHONPATH=. python pruebas_simulacion/cerrar_urgentia.py
"""
import csv, json, traceback
from collections import Counter
from pathlib import Path
from app import create_app
from app.extensions import db
from app.models.pretriage import Pretriage
from app.models.pregunta_ia import PreguntaIA
from app.models.result import Result

BASE = Path('pruebas_simulacion')
plan = json.loads((BASE/'plan_ejecucion_100.json').read_text(encoding='utf-8'))
app = create_app()
rows=[]
with app.app_context():
    from app.services.pretriage_agent_service import PretriageAgentService, RevisionClinicaRequerida
    service = None
    for c in plan:
        cid=c['id_caso']; pid=c.get('id_pretriage')
        r={'id_caso':cid,'id_pretriage':pid,'ruta_plan':c.get('ruta_sistema'),'estado_plan':c.get('estado_simulacion'),'prioridad_objetivo':c.get('prioridad_objetivo'),'prioridad_resultado':None,'accion':None,'preguntas':0,'respondidas':0,'detalle':''}
        p=db.session.get(Pretriage,pid) if pid else None
        if p is None:
            r['accion']='sin_pretriage'; rows.append(r); continue
        qs=PreguntaIA.query.filter_by(id_pretriage=pid).all()
        r['preguntas']=len(qs);r['respondidas']=sum(bool(q.respuesta and q.respuesta.strip()) for q in qs)
        result=Result.query.filter_by(id_pretriage=pid).first()
        if result:
            r['prioridad_resultado']=result.nivel_triage;r['accion']='resultado_bd';rows.append(r);continue
        if p.alerta_reglas is True or p.estado_seguridad_ia == 'alerta':
            r['accion']='alerta_reglas_o_seguridad';r['detalle']='Alerta: no se fuerza evaluación IA';rows.append(r);continue
        if c.get('ruta_sistema')=='reglas':
            r['accion']='reglas_sin_resultado_persistido';rows.append(r);continue
        if not qs or r['respondidas'] != len(qs):
            r['accion']='preguntas_pendientes';rows.append(r);continue
        if p.estado_seguridad_ia not in ('continuar','revisado'):
            r['accion']='seguridad_no_habilitada';r['detalle']=str(p.estado_seguridad_ia);rows.append(r);continue
        try:
            if service is None: service=PretriageAgentService()
            respuesta=service.evaluate(pid)
            r['accion']=respuesta.get('accion','evaluacion_ia') if isinstance(respuesta,dict) else 'evaluacion_ia'
            r['prioridad_resultado']=respuesta.get('prioridad') if isinstance(respuesta,dict) else None
            r['detalle']=json.dumps(respuesta,ensure_ascii=False,default=str)
        except RevisionClinicaRequerida as e:
            r['accion']='revision_clinica';r['detalle']=str(e)
        except Exception as e:
            r['accion']='error_evaluacion';r['detalle']=f'{type(e).__name__}: {e}'
        rows.append(r)
        print(cid, r['accion'],r['prioridad_resultado'],flush=True)
BASE.mkdir(exist_ok=True)
(BASE/'resultados_consolidados_100.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (BASE/'resultados_consolidados_100.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
resumen={'total':len(rows),'acciones':dict(Counter(r['accion'] for r in rows)),'prioridades_obtenidas':dict(Counter(r['prioridad_resultado'] for r in rows if r['prioridad_resultado']))}
(BASE/'resumen_final_ejecucion.json').write_text(json.dumps(resumen,ensure_ascii=False,indent=2),encoding='utf-8')
print('\nRESUMEN:',json.dumps(resumen,ensure_ascii=False,indent=2))
print('Archivos: pruebas_simulacion/resultados_consolidados_100.csv y resumen_final_ejecucion.json')
