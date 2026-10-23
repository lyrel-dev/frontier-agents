"""Standalone pinned report with measured interactive graphs and no network calls."""
from __future__ import annotations
import html
import json
from pathlib import Path
import secrets
from .util import canonical, digest, iso

ROOT=Path(__file__).resolve().parents[1]


def report_document(store,identifier):
    export=store.export(identifier); entity=export['entity']; data=entity['data']
    assessment=None
    key=data.get('assessment_id') or data.get('comparison_id')
    if key:
        assessment=store.record(key)
        for ref,expected in assessment['data'].get('input_hashes',{}).items():
            if store.record(ref)['sha256']!=expected:
                raise ValueError('Report input hash mismatch')
        if assessment['kind']=='assessment':
            capture=store.record(assessment['data']['probe_capture_id'])['data']
            if digest(capture['samples'])!=assessment['data']['probe_input_sha256']:
                raise ValueError('Pinned probe capture digest mismatch')
            export['probes']=capture['samples']
    report={'entity':entity,'assessment':assessment,'events':export['events'],'probes':export['probes'],
            'record_hashes':{r['id']:r['sha256'] for r in export['records']},'exported_at':iso(),'export_sha256':digest(export)}
    payload=canonical(report).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    nonce=secrets.token_urlsafe(24)
    csp=f"default-src 'none'; script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'"
    script='''
const data=JSON.parse(document.getElementById('report-data').textContent);
const host=document.getElementById('charts');
function chart(title,unit,series){const box=document.createElement('div');host.append(box);LabCharts.draw(box,{title,unit,series});}
if(data.assessment?.kind==='assessment'){
 const summary=data.assessment.data;
 for(const [metric,value]of Object.entries(summary.metrics)){const def=summary.metric_definitions?.[metric];chart(def?.title||metric.replaceAll('_',' '),def?.unit||(metric.endsWith('_seconds')?'s':metric.endsWith('_ms')?'ms':'measured'),[{name:'Pinned observation',isolated:true,points:value===null?[]:[{t:data.assessment.created_at,value,source:data.assessment.id}]}]);}
 chart('Real probe latency','ms',[{name:'Recorded workload',points:data.probes.map(p=>({t:p.at,value:p.attempted?p.latency_ms:null})),interval_ms:15000}]);
 const rows=document.getElementById('claims');for(const [key,val]of Object.entries(summary.dimensions)){const tr=document.createElement('tr');for(const text of [key,val.outcome,val.reason]){const td=document.createElement('td');td.textContent=text;tr.append(td);}rows.append(tr);}
}
if(data.assessment?.kind==='comparison'){
 for(const pair of data.assessment.data.pairs){const tr=document.createElement('tr');for(const text of [pair.baseline_trial+' / '+pair.replay_trial,pair.outcome,pair.reason]){const td=document.createElement('td');td.textContent=text;tr.append(td);}document.getElementById('claims').append(tr);
 for(const metric of ['bad_probe_seconds','failed_probe_requests','probe_latency_p95_ms'])chart(metric.replaceAll('_',' '),'recorded scalar',[{name:'Baseline',isolated:true,points:[{t:data.assessment.created_at,value:pair.baseline_metrics[metric]}]},{name:'Replay',isolated:true,points:[{t:data.assessment.created_at,value:pair.replay_metrics[metric]}]}]);}
}
document.getElementById('manifest').textContent=JSON.stringify(data.record_hashes,null,2);
'''
    document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="{html.escape(csp,quote=True)}"><title>{html.escape(data.get('title',identifier))} · experiment report</title><style nonce="{nonce}">{(ROOT/'static/style.css').read_text()}</style></head><body><main class="report"><div class="kicker">DEVOPS AGENT · PINNED EXPERIMENT EVIDENCE</div><h1>{html.escape(data.get('title',identifier))}</h1><p>{html.escape(identifier)} · {html.escape(entity['state'])}</p><div class="notice">Locally collected evidence and attributed reviews. No readiness certificate or automatic causal claim. This export makes no network calls. Original records remain in AWS; local hashes establish consistency, not source authenticity.</div><p class="small muted">Export SHA-256: {report['export_sha256']}</p><table><thead><tr><th>Claim</th><th>Outcome</th><th>Reason</th></tr></thead><tbody id="claims"></tbody></table><div id="charts" class="metric-grid"></div><details><summary>Pinned record hashes</summary><pre id="manifest"></pre></details><script nonce="{nonce}" type="application/json" id="report-data">{payload}</script><script nonce="{nonce}">{(ROOT/'static/charts.js').read_text()}</script><script nonce="{nonce}">{script}</script></main></body></html>'''
    return document,csp


def report_html(store,identifier):
    return report_document(store,identifier)[0]
