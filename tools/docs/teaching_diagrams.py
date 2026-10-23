"""Fixed-position teaching views over the unchanged product model.

Colors retain definition ownership. Numbered marks are editorial reading steps;
they are not API states or an internal service call graph.
"""
from html import escape
from pathlib import Path
import textwrap

PALETTE={'aws': ('#D9F2E5', '#348761', 'AWS'), 'documentation': ('#DCEBFF', '#447AC2', 'DOC'), 'external': ('#FCE8D5', '#C78335', 'EXT')}
BOXES={'request': (15, 280, 205, 140),
 'instructions': (270, 82, 260, 140),
 'skills': (560, 82, 260, 140),
 'knowledge': (850, 82, 260, 140),
 'execution': (270, 270, 840, 140),
 'connections': (470, 470, 350, 140),
 'learning': (875, 470, 235, 140),
 'sources': (470, 650, 350, 110),
 'result': (1170, 280, 215, 140),
 'operator': (15, 470, 205, 140),
 'destination': (1170, 650, 215, 110)}
PRODUCTS={'devops': {'name': 'AWS DevOps Agent',
            'scope': 'Agent Space — access, definitions, context and execution records',
            'nodes': {'request': ('external', 'Request / signal', 'Question, incident or configured start'),
                      'instructions': ('aws', 'Instructions', 'Managed AGENTS.md or custom prompt'),
                      'skills': ('aws', 'Skills', 'Applicable or assigned procedures'),
                      'knowledge': ('aws', 'Memory stores', 'Available context; selected entries'),
                      'execution': ('aws', 'Agent execution', 'A managed role or one custom-agent invocation'),
                      'connections': ('aws',
                                      'Integrations and tools',
                                      'Provider association; selected operations'),
                      'learning': ('aws', 'Knowledge production', 'Learning runs; feedback reflections'),
                      'sources': ('external', 'Source systems', 'Resources, telemetry, code and deployment'),
                      'result': ('aws', 'Result / record', 'Findings, proposals, artifacts and history'),
                      'operator': ('external', 'Operator', 'Scope, feedback, approval and review'),
                      'destination': ('external', 'Destination', 'Configured channel or event consumer')},
            'views': {'agent': ('An agent uses guidance, procedures, context and authorized operations',
                                ['D-90', 'D-15', 'D-16'],
                                ['request',
                                 'instructions',
                                 'skills',
                                 'knowledge',
                                 'execution',
                                 'connections',
                                 'sources',
                                 'result']),
                      'coordination': ('Managed responsibilities and knowledge reuse',
                                       ['D-91', 'D-15', 'D-M08'],
                                       ['request',
                                        'execution',
                                        'knowledge',
                                        'learning',
                                        'result',
                                        'connections',
                                        'sources']),
                      'space': ('The Agent Space contains configuration and execution context',
                                ['D-92', 'D-01', 'D-12'],
                                ['request',
                                 'instructions',
                                 'skills',
                                 'knowledge',
                                 'execution',
                                 'connections',
                                 'learning',
                                 'sources',
                                 'result',
                                 'operator',
                                 'destination']),
                      'incident': ('Incident triage and current-evidence investigation',
                                   ['D-93', 'D-06'],
                                   ['request', 'execution', 'connections', 'sources', 'knowledge', 'result']),
                      'mitigation': ('Mitigation planning and separately approved execution',
                                     ['D-93', 'D-M06'],
                                     ['operator', 'execution', 'connections', 'sources', 'result']),
                      'learning': ('Investigation history and correction become later context',
                                   ['D-93', 'D-M01', 'D-M02', 'D-M08'],
                                   ['result', 'operator', 'learning', 'knowledge', 'execution']),
                      'reporting': ('Service-health reporting reuses the same configured facilities',
                                    ['D-93', 'D-16', 'D-19'],
                                    ['request',
                                     'instructions',
                                     'skills',
                                     'execution',
                                     'connections',
                                     'sources',
                                     'result']),
                      'knowledge': ('Procedure maintenance and environment documentation',
                                    ['D-93', 'D-M04', 'D-05'],
                                    ['operator', 'skills', 'sources', 'learning', 'knowledge', 'result']),
                      'change': ('Configuration and release assurance use explicit subjects and effects',
                                 ['D-93', 'D-22'],
                                 ['request',
                                  'instructions',
                                  'execution',
                                  'connections',
                                  'sources',
                                  'operator',
                                  'result']),
                      'review': ('An operational review consumes independently verified outputs',
                                 ['D-93', 'D-14'],
                                 ['result', 'operator', 'knowledge'])}},
 'security': {'name': 'AWS Security Agent',
              'scope': 'Application Agent Space — settings, selected context and assessment records',
              'nodes': {'request': ('external', 'Assessment request', 'Target, revision or document scope'),
                        'instructions': ('aws', 'Assessment settings', 'Type, target rules and credentials'),
                        'skills': ('aws', 'Selected criteria', 'Shared requirements used by eligible reviews'),
                        'knowledge': ('aws', 'Application context', 'Selected source and application documents'),
                        'execution': ('aws', 'Assessment execution', 'Assessment-specific run or one-off review'),
                        'connections': ('aws',
                                        'Source and target access',
                                        'Repository, network path and test identity'),
                        'learning': ('aws', 'Specific retained state', 'Login procedure; finding preferences'),
                        'sources': ('external', 'Application and sources', 'Deployed target, code and documents'),
                        'result': ('aws', 'Assessment result', 'Findings and verification evidence'),
                        'operator': ('external', 'Application team', 'Authorize, review, deploy and accept'),
                        'destination': ('external',
                                        'Repository / Jira',
                                        'Review or issue')},
              'views': {'agent': ('Security assessment inputs and execution',
                                  ['S-90', 'S-12'],
                                  ['request',
                                   'instructions',
                                   'skills',
                                   'knowledge',
                                   'execution',
                                   'connections',
                                   'sources',
                                   'result']),
                        'coordination': ('Assessment, repair and verification are separate work records',
                                         ['S-91', 'S-10'],
                                         ['request', 'execution', 'result', 'operator', 'connections', 'sources']),
                        'space': ('Application scope and shared assessment criteria',
                                  ['S-92', 'S-01'],
                                  ['request',
                                   'instructions',
                                   'skills',
                                   'knowledge',
                                   'execution',
                                   'connections',
                                   'learning',
                                   'sources',
                                   'result',
                                   'operator',
                                   'destination']),
                        'assessment': ('Assess source or an authorized running application',
                                       ['S-93', 'S-03', 'S-06'],
                                       ['request',
                                        'instructions',
                                        'knowledge',
                                        'execution',
                                        'connections',
                                        'sources',
                                        'result']),
                        'repair': ('Finding triage, repair proposal, deployment and revalidation',
                                   ['S-93', 'S-05', 'S-M05'],
                                   ['result', 'operator', 'execution', 'connections', 'sources']),
                        'context': ('Criteria, application context and narrowly scoped reuse',
                                    ['S-93', 'S-M03', 'S-M02', 'S-13'],
                                    ['skills', 'knowledge', 'learning', 'execution', 'result'])}},
 'finops': {'name': 'AWS FinOps Agent',
            'scope': 'Agent instance — access, context, work records and destination connections',
            'nodes': {'request': ('external', 'Question / trigger', 'Question, explicit task or automation'),
                      'instructions': ('aws', 'Work instructions', 'Query basis and requested analysis'),
                      'skills': ('aws', 'Context files', 'Mappings, instructions and report templates'),
                      'knowledge': ('aws', 'Persistent memory', 'Preferences, corrections and task outcomes'),
                      'execution': ('aws',
                                    'Analysis execution',
                                    'Direct conversation or an explicitly created queued task'),
                      'connections': ('aws',
                                      'Data and destination access',
                                      'Source permissions; separate Jira / Slack binding'),
                      'learning': ('aws', 'Context maintenance', 'Memory updates; separate compaction'),
                      'sources': ('external', 'AWS data sources', 'Cost, anomaly and recommendation services'),
                      'result': ('aws', 'Analysis result', 'Answer, artifact and task result'),
                      'operator': ('external', 'Service owner', 'Reconcile, review publication and own changes'),
                      'destination': ('external', 'Jira / Slack', 'Selected project or channel')},
            'views': {'agent': ('FinOps analysis combines source data and organizational context',
                                ['F-90', 'F-11'],
                                ['request',
                                 'instructions',
                                 'skills',
                                 'knowledge',
                                 'execution',
                                 'connections',
                                 'sources',
                                 'result']),
                      'coordination': ('Requests and automations coordinate work through tasks',
                                       ['F-91', 'F-03'],
                                       ['request', 'execution', 'connections', 'result', 'operator']),
                      'space': ('Instance-scoped context, work and destinations',
                                ['F-92', 'F-01', 'F-09'],
                                ['request',
                                 'instructions',
                                 'skills',
                                 'knowledge',
                                 'execution',
                                 'connections',
                                 'learning',
                                 'sources',
                                 'result',
                                 'operator',
                                 'destination']),
                      'analysis': ('Historical cost and anomaly analysis retain source provenance',
                                   ['F-93', 'F-M01'],
                                   ['request', 'instructions', 'execution', 'connections', 'sources', 'result']),
                      'reporting': ('Periodic reporting adds a task definition and publication path',
                                    ['F-93', 'F-03', 'F-04', 'F-M06'],
                                    ['request',
                                     'instructions',
                                     'skills',
                                     'execution',
                                     'connections',
                                     'result',
                                     'operator',
                                     'destination']),
                      'optimization': ('Recommendations are reviewed before engineering change and measurement',
                                       ['F-93', 'F-14'],
                                       ['sources', 'connections', 'execution', 'result', 'operator'])}}}


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
