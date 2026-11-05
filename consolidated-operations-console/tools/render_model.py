#!/usr/bin/env python3
"""Render entity reference and complete/focused class diagrams from model/schema.json.

No network access is used. --check verifies generated text, existing SVG manifest
hashes and schema provenance without rewriting any file. Graphviz is only needed
when rendering, not when checking previously committed outputs.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'model/schema.json'
MODULES = [('foundation','Shared foundation'),('workload','Workload catalogue'),('health','AWS Health'),('resilience','Resilience'),('investigation','Investigations'),('workflow','Assessment workflow'),('fis','AWS FIS')]
COLORS = {'foundation':'#EAF1F8','workload':'#E7F2EC','health':'#FFF0DE','resilience':'#EDE9F8','investigation':'#E2F2F3','workflow':'#F9E7EA','fis':'#F9E7EA'}
LAYOUT_ROWS = {
    'foundation': [['Workspace','Connection'],['Resource','Collection'],['SourceRevision','ReadAttempt'],['Observation'],['ProjectionRevision','Snapshot'],['WorkItem','Command']],
    'workload': [['System'],['UserJourney','Service'],['Dependency']],
    'health': [['HealthEvent'],['EventContext'],['EntityImpact','Communication'],['LifecycleEntry','ComponentDeployment']],
    'resilience': [['ResiliencePolicy','ResilienceAssessment'],['Finding'],['Recommendation']],
    'investigation': [['AgentSpace'],['Investigation','Execution'],['Asset','ApprovalRequest','JournalRecord']],
    'workflow': [['Scenario'],['ScenarioRevision'],['Run'],['StepRun'],['StepAttempt']],
    'fis': [['Experiment']],
}

def digest(data): return hashlib.sha256(data).hexdigest()
def typename(s):
    if '$ref' in s: return s['$ref'].split('/')[-1]
    if 'anyOf' in s: return ' | '.join(typename(x) for x in s['anyOf'])
    if 'enum' in s: return 'enum'
    if 'const' in s: return str(s['const'])
    if s.get('type')=='array': return 'List['+typename(s['items'])+']'
    return s.get('type','JsonValue')

def display_fields(name, spec):
    props=spec['properties']; own=name[0].lower()+name[1:]+'Id'
    choices=[own]+[p for p in props if p not in [own,'workspaceId'] and (p.endswith('Id') or p in ['identity','version','projectionVersion','kind','profile','state','phase','executionOutcome','assessmentVerdict','rawProviderStatus','rawExperimentState'])]
    if len(choices)<4: choices.extend(p for p in props if p not in choices and p!='workspaceId')
    return choices[:5]

def mermaid(schema, names, title):
    out=['%% Generated from model/schema.json; edit the schema and rerun tools/render_model.py.',f'%% {title}','classDiagram','direction TB']
    for n in names:
        d=schema['$defs'][n]; out += [f'class {n} {{',f'  <<{d["x-module"]}>>']
        for p in display_fields(n,d):
            t=typename(d['properties'][p]).replace(' | null','?').replace('[','~').replace(']','~')
            out.append(f'  +{t} {p}')
        out.append('}')
    for r in schema['x-relationships']:
        if r['from'] in names and r['to'] in names:
            out.append(f'{r["from"]} "{r["fromCardinality"]}" --> "{r["toCardinality"]}" {r["to"]} : {r["label"]}')
    out += ['%% All entities are workspace-scoped; all foreign references require same-workspace validation.','%% EventContext impacts exclude ORG_SUMMARY; Investigation-Execution is observed membership.','%% Cross-module references remain typed fields when a focused panel omits their target.']
    return '\n'.join(out)+'\n'

def dot(schema,names,title):
    # At most three visible class boxes per rank. Invisible anchors stack module
    # panels vertically. Real association edges cannot change this readable layout.
    out=['digraph Model {','graph [rankdir=TB, bgcolor="white", pad=0.25, nodesep=0.9, ranksep=1.0, newrank=true, splines=polyline, fontname="DejaVu Sans", fontsize=20, labelloc=t, label='+json.dumps(title,ensure_ascii=False)+'];','node [shape=plain, fontname="DejaVu Sans"];','edge [fontname="DejaVu Sans", fontsize=9, labelfontsize=9, labeldistance=2.5, labelangle=25, color="#718096", arrowsize=0.65];']
    previous_bottom=None
    for mi,(module,label) in enumerate(MODULES):
        members=[n for n in names if schema['$defs'][n]['x-module']==module]
        if not members: continue
        top=f'anchor_{mi}_top'; bottom=f'anchor_{mi}_bottom'
        out += [f'subgraph cluster_{mi} {{',f'label={json.dumps(label,ensure_ascii=False)}; color="#CCD5DF"; fontcolor="#334155"; fontsize=15; style="rounded";',f'{top} [shape=point,width=0,height=0,label="",style=invis];',f'{bottom} [shape=point,width=0,height=0,label="",style=invis];']
        for n in members:
            spec=schema['$defs'][n]
            fields=''.join('<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10">'+html.escape(p+': '+typename(spec['properties'][p]))+'</FONT></TD></TR>' for p in display_fields(n,spec))
            table=f'<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" COLOR="#8492A6"><TR><TD BGCOLOR="{COLORS[module]}"><B>{n}</B></TD></TR>{fields}</TABLE>'
            out.append(f'{n} [label=<{table}>];')
        prev=[top]
        rows=[[n for n in row if n in members] for row in LAYOUT_ROWS[module]]
        rows=[row for row in rows if row]
        placed={n for row in rows for n in row}
        rows.extend([[n] for n in members if n not in placed])
        for row in rows:
            out.append('{rank=same; '+'; '.join(row)+';}')
            for a,b in zip(row,row[1:]): out.append(f'{a} -> {b} [style=invis,weight=100];')
            for a in prev:
                for b in row: out.append(f'{a} -> {b} [style=invis,weight=100];')
            prev=row
        for a in prev: out.append(f'{a} -> {bottom} [style=invis,weight=100];')
        out.append('}')
        if previous_bottom: out.append(f'{previous_bottom} -> {top} [style=invis,weight=100,minlen=2];')
        previous_bottom=bottom
    for r in schema['x-relationships']:
        if r['from'] in names and r['to'] in names:
            label=r['label']
            out.append(f'{r["from"]} -> {r["to"]} [constraint=false,xlabel={json.dumps(label,ensure_ascii=False)},taillabel={json.dumps(r["fromCardinality"])},headlabel={json.dumps(r["toCardinality"])}];')
    out.append('}')
    return '\n'.join(out)+'\n'

def reference(schema):
    defs=schema['$defs']; out=['# Entity and value reference','','Generated from [schema.json](schema.json). Edit the schema, then run `python tools/render_model.py` from this package. [MODEL.md](../MODEL.md) defines the invariants and ownership rules that JSON Schema cannot express.','','The model contains **37 entities**. Every entity except Workspace includes `workspaceId`. Foreign references must resolve in that workspace and satisfy the documented parent scope. Provider identifiers are retained separately from application IDs.','','## Entity index','','| Module | Entity | Owner | Identity |','| --- | --- | --- | --- |']
    for n in schema['x-entities']:
        d=defs[n]; out.append(f'| {d["x-module"]} | [{n}](#{n.lower()}) | {d["x-owner"]} | `{d["x-identity"]}` |')
    out += ['','## Entities','']
    for n in schema['x-entities']:
        d=defs[n]; out += [f'### {n}','',d['description'],'',f'**Owner:** {d["x-owner"]}. **Module:** {d["x-module"]}. **Identity:** `{d["x-identity"]}`.','','| Field | Type | Required |','| --- | --- | --- |']
        for p,s in d['properties'].items(): out.append(f'| `{p}` | `{typename(s).replace(" | ", " or ")}` | {"Yes" if p in d.get("required",[]) else "No"} |')
        out.append('')
    out += ['## Owned values and scalar contracts','','Owned values have identity only within their owner or their pinned revision. Naming a shape does not create another CRUD resource. ReadAttempt, StepRun and StepAttempt remain explicit entities because their lifecycle and references require independent tracking.','','| Shape | Meaning |','| --- | --- |']
    for n,d in defs.items():
        if n not in schema['x-entities']: out.append(f'| `{n}` | {d.get("description",typename(d)).replace("|","/")} |')
    out += ['','## Relationship register','','All multiplicities describe the logical model; a partial cache can contain unresolved references. The full diagram is [complete-model.svg](../diagrams/complete-model.svg).','','| From | Cardinality | To | Cardinality | Meaning |','| --- | --- | --- | --- | --- |']
    for r in schema['x-relationships']: out.append(f'| {r["from"]} | {r["fromCardinality"]} | {r["to"]} | {r["toCardinality"]} | {r["label"]} |')
    return '\n'.join(out)+'\n'

def outputs(schema):
    result={'model/REFERENCE.md':reference(schema)}
    panels=[('complete-model','Complete model — all 37 entities',schema['x-entities'])]
    for module,label in MODULES:
        if module=='fis': continue
        mods=[module,'fis'] if module=='workflow' else [module]
        panels.append((module,'Consolidated Operations Console — '+label,[n for n in schema['x-entities'] if schema['$defs'][n]['x-module'] in mods]))
    for stem,title,names in panels:
        result[f'diagrams/{stem}.mmd']=mermaid(schema,names,title)
        result[f'diagrams/{stem}.dot']=dot(schema,names,title)
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    schema=json.loads(SCHEMA.read_text()); generated=outputs(schema); manifest_path=ROOT/'diagrams/manifest.json'
    if args.check:
        errors=[]
        for p,body in generated.items():
            if not (ROOT/p).exists() or (ROOT/p).read_text()!=body: errors.append('Stale/missing '+p)
        if not manifest_path.exists(): errors.append('Missing diagram manifest')
        else:
            m=json.loads(manifest_path.read_text())
            if m['schemaSha256']!=digest(SCHEMA.read_bytes()): errors.append('Diagram schema provenance is stale')
            for entry in m['diagrams']:
                for ext in ['mmd','dot','svg']:
                    p=ROOT/entry[ext]['path']
                    if not p.exists() or digest(p.read_bytes())!=entry[ext]['sha256']: errors.append('Stale/missing '+str(p.relative_to(ROOT)))
        if errors: raise SystemExit('\n'.join(errors))
        print(f'Generated reference and {len([p for p in generated if p.endswith(".mmd")])} diagram sources/outputs match.'); return
    for p,body in generated.items(): (ROOT/p).write_text(body)
    entries=[]
    for path in generated:
        if not path.endswith('.dot'): continue
        stem=path[:-4]; subprocess.run(['dot','-Tsvg',str(ROOT/path),'-o',str(ROOT/(stem+'.svg'))],check=True,capture_output=True,text=True)
        entries.append({ext:{'path':stem+'.'+ext,'sha256':digest((ROOT/(stem+'.'+ext)).read_bytes())} for ext in ['mmd','dot','svg']})
    manifest={'schemaSha256':digest(SCHEMA.read_bytes()),'renderer':subprocess.run(['dot','-V'],capture_output=True,text=True).stderr.strip(),'mermaid':'Editable sources; SVG is rendered from the same schema via Graphviz, not claimed to be Mermaid render parity.','diagrams':entries}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Rendered {len(entries)} diagrams and model/REFERENCE.md.')

if __name__=='__main__': main()
