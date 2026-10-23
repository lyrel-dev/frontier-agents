"""One-time correction after reviewing the rendered coordination figure."""
from pathlib import Path
import importlib.util
import json
import pprint

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
p=HERE/'teaching_diagrams.py'
spec=importlib.util.spec_from_file_location('current_teaching',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
boxes=dict(m.BOXES)
boxes['destination']=(1170,650,215,110)
products=m.PRODUCTS
updates={
 'devops':{
 'request':('external','Request / signal','Question, incident or configured start'),
 'instructions':('aws','Instructions','Managed AGENTS.md or custom prompt'),
 'skills':('aws','Skills','Applicable or assigned procedures'),
 'knowledge':('aws','Memory stores','Available context; selected entries'),
 'execution':('aws','Agent execution','A managed role or one custom-agent invocation'),
 'connections':('aws','Integrations and tools','Provider association; selected operations'),
 'learning':('aws','Knowledge production','Learning runs; feedback reflections'),
 'sources':('external','Source systems','Resources, telemetry, code and deployment'),
 'result':('aws','Result / record','Findings, proposals, artifacts and history'),
 'operator':('external','Operator','Scope, feedback, approval and review'),
 'destination':('external','Destination','Configured channel or event consumer')},
 'security':{
 'request':('external','Assessment request','Target, revision or document scope'),
 'instructions':('aws','Assessment settings','Type, target rules and credentials'),
 'skills':('aws','Selected criteria','Shared requirements used by eligible reviews'),
 'knowledge':('aws','Application context','Selected source and application documents'),
 'execution':('aws','Assessment execution','Assessment-specific run or one-off review'),
 'connections':('aws','Source and target access','Repository, network path and test identity'),
 'learning':('aws','Specific retained state','Login procedure; finding preferences'),
 'sources':('external','Application and sources','Deployed target, code and documents'),
 'result':('aws','Assessment result','Findings and verification evidence'),
 'operator':('external','Application team','Authorize, review, deploy and accept'),
 'destination':('external','Repository / Jira','Configured review or issue destination')},
 'finops':{
 'request':('external','Question / trigger','Question, explicit task or automation'),
 'instructions':('aws','Work instructions','Query basis and requested analysis'),
 'skills':('aws','Context files','Mappings, instructions and report templates'),
 'knowledge':('aws','Persistent memory','Preferences, corrections and task outcomes'),
 'execution':('aws','Analysis execution','Direct conversation or an explicitly created queued task'),
 'connections':('aws','Data and destination access','Source permissions; separate Jira / Slack binding'),
 'learning':('aws','Context maintenance','Memory updates; separate compaction'),
 'sources':('external','AWS data sources','Cost, anomaly and recommendation services'),
 'result':('aws','Analysis result','Answer, artifact and task result'),
 'operator':('external','Service owner','Reconcile, review publication and own changes'),
 'destination':('external','Jira / Slack','Selected project or channel')}
}
for product,nodes in updates.items():
 products[product]['nodes']=nodes
 for view,(title,refs,active) in list(products[product]['views'].items()):
  if view=='space' or (product=='finops' and view=='reporting'):
   active=list(active)+['destination']
  products[product]['views'][view]=(title,refs,active)
products['devops']['scope']='Agent Space — access, definitions, context and execution records'
products['security']['scope']='Application Agent Space — settings, selected context and assessment records'
products['finops']['scope']='Agent instance — access, context, work records and destination connections'
header='''"""Fixed-position teaching views over the unchanged product model.

Colors retain definition ownership. Numbered marks are editorial reading steps;
they are not API states or an internal service call graph.
"""
from html import escape
from pathlib import Path
import textwrap

'''
header+='PALETTE='+repr(m.PALETTE)+'\nBOXES='+pprint.pformat(boxes,sort_dicts=False)+'\nPRODUCTS='+pprint.pformat(products,sort_dicts=False,width=115)+'\n'
renderer=r'''

def key_for(product,view):return 'teaching-'+product+'-'+view

def definitions():
 return {key_for(p,v):(title,'Stable component positions. Color identifies concept ownership; heavier borders and numbered reading steps identify the active workflow. This is a logical teaching view, not a service call graph.',refs,'') for p,spec in PRODUCTS.items() for v,(title,refs,active) in spec['views'].items()}

DIAGRAMS=definitions()
PATHS={
 'incident':('request','execution','connections','result'),
 'mitigation':('operator','execution','sources','result'),
 'learning':('result','learning','knowledge','execution'),
 'reporting':('request','instructions','connections','result'),
 'knowledge':('operator','skills','learning','knowledge'),
 'change':('request','execution','sources','result'),
 'review':('result','operator'),
 'assessment':('request','instructions','connections','result'),
 'repair':('result','operator','execution','sources'),
 'context':('skills','knowledge','learning','execution'),
 'analysis':('request','connections','sources','result'),
 'optimization':('sources','execution','result','operator')}


def render(key):
 product,view=key.removeprefix('teaching-').split('-',1)
 spec=PRODUCTS[product];title,refs,active=spec['views'][view]
 basic=view=='agent';show_scope=view not in ('agent','coordination')
 publish=show_scope and view in ('space','reporting','repair','incident')
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 825" role="img" aria-labelledby="{key}-title {key}-desc" data-diagram="{key}" data-layout="teaching-fixed-v1" data-product="{product}" data-view="{view}">',f'<title id="{key}-title">{escape(title)}</title>',f'<desc id="{key}-desc">{escape(DIAGRAMS[key][1])}</desc>',
 '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8" fill="#465768"/></marker></defs>',
 '<style>text{font-family:Arial,sans-serif;fill:#182d3d}.label{font-size:21px;font-weight:600}.detail{font-size:19px}.tag{font-size:14px;font-weight:700}.edge{fill:none;stroke:#465768;stroke-width:2.2;marker-end:url(#arrow)}.edge-soft{fill:none;stroke:#6b7785;stroke-width:1.6;stroke-dasharray:7 5;marker-end:url(#arrow)}</style>']
 if show_scope:
  out.append('<rect x="240" y="35" width="900" height="580" rx="12" fill="#fbfcfd" stroke="#348761" stroke-width="2" stroke-dasharray="9 5"/>')
  out.append(f'<text x="255" y="58" font-size="18">{escape(spec["scope"])}</text>')
 paths=[('request','execution','M220 350 H270'),('instructions','execution','M400 222 V270'),('skills','execution','M690 222 V270'),('knowledge','execution','M980 222 V270'),('execution','result','M1110 350 H1170'),('execution','connections','M645 410 V470'),('connections','sources','M645 610 V650')]
 for a,b,d in paths:
  cls='edge' if a in active and b in active else 'edge-soft'
  reverse=' marker-start="url(#arrow)"' if (a,b) in (('execution','connections'),('connections','sources')) else ''
  out.append(f'<path data-edge="{a}-{b}" class="{cls}" d="{d}"{reverse}/>')
 out+=['<text x="665" y="447" font-size="16">invoke / observe</text>','<text x="665" y="637" font-size="16">authorized access</text>']
 if not basic:
  out.append('<path class="edge-soft" data-edge="result-learning" d="M1170 380 H1150 V540 H1110"/>')
  if product=='security':out.append('<path class="edge-soft" data-edge="reuse-execution" d="M995 470 V410"/>')
  else:out.append('<path class="edge-soft" data-edge="learning-knowledge" d="M995 470 V438 H1125 V245 H980 V222"/>')
  if product=='devops':out.append('<path class="edge-soft" data-edge="sources-learning" d="M820 705 H1150 V570 H1110"/>')
  out.append('<path class="edge-soft" data-edge="operator-execution" d="M220 540 H250 V380 H270"/>')
 if view in ('review','mitigation','repair','optimization'):
  out.append('<path class="edge-soft" data-edge="result-operator" d="M1277 420 V625 H118 V610"/>')
  out.append('<text x="250" y="644" font-size="16">team review / acceptance</text>')
 if product=='devops' and view=='learning':
  out.append('<path class="edge-soft" data-edge="operator-feedback" d="M118 610 V632 H855 V540 H875"/>')
  out.append('<text x="245" y="625" font-size="16">verified correction</text>')
 if product=='devops' and view=='knowledge':
  out.append('<path class="edge-soft" data-edge="operator-skill" d="M118 470 V242 H690 V222"/>')
  out.append('<text x="285" y="237" font-size="16">reviewed procedure</text>')
 if publish:
  out.append('<path class="edge-soft" data-edge="result-destination" d="M1385 350 H1393 V705 H1385"/>')
  out+=['<text x="1200" y="565" font-size="16">Optional publication</text>','<text x="1200" y="588" font-size="16">Destination-specific</text>','<text x="1200" y="611" font-size="16">authorization</text>']
 steps=PATHS.get(view,())
 for ident,(x,y,w,h) in BOXES.items():
  if (basic and ident in ('learning','operator','destination')) or (ident=='destination' and not publish):continue
  owner,head,body=spec['nodes'][ident]
  if ident=='execution' and product=='devops' and view in ('coordination','incident','mitigation'):
   head='Managed incident work';body='Roles contribute to the investigation context and its outputs.'
  fill,stroke,tag=PALETTE[owner];weight='4' if ident in active else '1'
  out.append(f'<g data-node="{ident}" data-box="{x},{y},{w},{h}" data-owner="{owner}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>')
  out.append(f'<text class="tag" x="{x+12}" y="{y+20}">{tag}</text>')
  headings=textwrap.wrap(head,width=max(13,int((w-24)/11.8)))
  lines=textwrap.wrap(body,width=max(16,int((w-24)/10.2)))
  for i,line in enumerate(headings):out.append(f'<text class="label" x="{x+12}" y="{y+43+i*23}">{escape(line)}</text>')
  for i,line in enumerate(lines):out.append(f'<text class="detail" x="{x+12}" y="{y+43+(len(headings)+i)*23}">{escape(line)}</text>')
  if ident=='execution' and product=='devops' and view in ('coordination','incident','mitigation'):
   for j,(role,purpose) in enumerate((('Incident triage','Route the signal'),('Incident RCA','Investigate evidence'),('Incident mitigation','Propose a response'),('Incident UI','Present the output'))):
    px=x+14+j*204
    out.append(f'<rect x="{px}" y="{y+82}" width="194" height="45" rx="3" fill="#ffffff" stroke="#348761"/><text x="{px+8}" y="{y+100}" font-size="16">{role}</text><text x="{px+8}" y="{y+118}" font-size="14">{purpose}</text>')
  if ident in steps:
   step=steps.index(ident)+1
   out.append(f'<circle data-reading-step="{step}" cx="{x+w-15}" cy="{y+17}" r="12" fill="#DCEBFF" stroke="#447AC2"/><text x="{x+w-19}" y="{y+22}" font-size="14">{step}</text>')
  out.append('</g>')
 if view=='coordination':
  notes={'devops':'Incident roles are distinct responsibilities, not a mandatory sequence. Learning runs separately.',
         'security':'Assessment → finding → proposal → team deployment → revalidation. These are work records, not peer agents.',
         'finops':'Direct conversation or explicit task; schedules and matching events create tasks, not additional agents.'}
  out.append(f'<text x="20" y="785" font-size="17">{escape(notes[product])}</text>')
 elif steps:out.append('<text x="20" y="785" font-size="17">Numbered circles mark reading steps. Other components remain in place for comparison.</text>')
 out.append('<text x="20" y="810" font-size="17">DOC: documentation-defined  |  AWS: documented service concept  |  EXT: external system or team</text></svg>')
 return ''.join(out)


def build_one(key,directory):Path(directory,key+'.svg').write_text(render(key),encoding='utf-8')
'''
p.write_text(header+renderer)
css=HERE/'styles.css';t=css.read_text().replace('.diagram-viewport{max-width:920px;margin:auto}', '.diagram-viewport{max-width:1080px;margin:auto}')
css.write_text(t)
# Keep maintenance instructions accurate rather than rewriting generated output by hand.
p=HERE/'reader.py';s=p.read_text()
s=s.replace('Guides distinguish workspace organization, definition, context, invocation, integrations, network connectivity, execution controls, managed functions, outputs, and administration.',
 'Guides begin with agent composition, coordination, scope and prioritized workflows. The ten capability dimensions follow as the configuration reference.')
p.write_text(s)
p=ROOT/'qa/educational-review.json';r=json.loads(p.read_text())
r['visual_review']={'basis':'Rendered the branch DevOps coordination SVG locally and inspected its label and connector layout.',
 'findings':['A responsibility caption touched the execution-box border.','Arrow origins were inside resized boxes.','Generic execution wording obscured the managed-incident view.','The publication path needed an explicit external destination.'],
 'corrections':['Move coordination note to the figure footer.','Terminate paths at current box boundaries.','Add named responsibilities and concise action descriptions.','Use product-specific external destination with a qualified publication path.','Use larger diagram labels and numbered reading steps; retain frozen ownership colors.'],
 'validation':'The amended views are subsequently checked in the browser for text bounds and layout; the inspected prior image is not claimed as an amended-output screenshot.'}
p.write_text(json.dumps(r,indent=2)+'\n')
Path(__file__).unlink()
