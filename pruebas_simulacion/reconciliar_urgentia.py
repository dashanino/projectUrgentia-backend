"""Auditoria SOLO LECTURA: compara plan local con tablas reales Neon/Flask."""
import csv, json
from collections import Counter
from pathlib import Path
from app import create_app
from app.models.pretriage import Pretriage
from app.models.pregunta_ia import PreguntaIA
from app.models.result import Result

base = Path('pruebas_simulacion')
plan = json.loads((base/'plan_ejecucion_100.json').read_text(encoding='utf-8'))
app = create_app()
rows=[]
with app.app_context():
    for item in plan:
        pid=item.get('id_pretriage')
        p=Pretriage.query.get(pid) if pid else None
        qs=PreguntaIA.query.filter_by(id_pretriage=pid).order_by(PreguntaIA.orden).all() if pid and p else []
        result=Result.query.filter_by(id_pretriage=pid).first() if pid and p else None
        answered=sum(bool(q.respuesta and q.respuesta.strip()) for q in qs)
        row={'id_caso':item['id_caso'],'id_pretriage':pid,'estado_plan':item.get('estado_simulacion'),
             'estado_bd':p.estado if p else 'no_encontrado',
             'preguntas_bd':len(qs),'respondidas_bd':answered,'pendientes_bd':len(qs)-answered,
             'nivel_triage_bd':result.nivel_triage if result else '',
             'estado_seguridad_ia':p.estado_seguridad_ia if p else '',
             'fecha_finalizacion':p.fecha_finalizacion.isoformat() if p and p.fecha_finalizacion else ''}
        rows.append(row)
        print(f"{row['id_caso']}: plan={row['estado_plan']} bd={row['estado_bd']} preguntas={answered}/{len(qs)} nivel={row['nivel_triage_bd'] or '-'}")

out=base/'reconciliacion_bd_100.csv'
with out.open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary={'total':len(rows),'estado_plan':dict(Counter(r['estado_plan'] for r in rows)),
         'estado_bd':dict(Counter(r['estado_bd'] for r in rows)),
         'niveles_triage':dict(Counter(r['nivel_triage_bd'] or 'sin_resultado' for r in rows)),
         'preguntas_registradas':sum(r['preguntas_bd'] for r in rows),
         'preguntas_respondidas':sum(r['respondidas_bd'] for r in rows),
         'casos_con_resultado':sum(bool(r['nivel_triage_bd']) for r in rows),
         'diferencias_plan_bd':[r['id_caso'] for r in rows if r['estado_plan'] != r['estado_bd']]}
(base/'resumen_reconciliacion_bd.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print('\nRESUMEN REAL DE BASE DE DATOS:\n'+json.dumps(summary,indent=2,ensure_ascii=False))
print('\nARCHIVOS:',out,base/'resumen_reconciliacion_bd.json')
print('NO se enviaron solicitudes HTTP, NO se modifico la base de datos ni el plan.')
