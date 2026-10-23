"""Progressive teaching views; no canonical entity or use-case records are changed.

Every view of one product uses the same node positions and ownership palette.
Emphasis describes the path being taught, not an undocumented runtime call graph.
"""
from __future__ import annotations
from html import escape
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]
PALETTE = {'aws': ('#D9F2E5', '#348761', 'AWS'),
           'documentation': ('#DCEBFF', '#447AC2', 'DOC'),
           'external': ('#FCE8D5', '#C78335', 'EXT')}
# The frame, connection layer and evidence sources do not move between views.
BOXES = {
    'request': (15, 280, 205, 140),
    'instructions': (270, 82, 260, 140),
    'skills': (560, 82, 260, 140),
    'knowledge': (850, 82, 260, 140),
    'execution': (270, 270, 840, 140),
    'connections': (470, 470, 350, 140),
    'learning': (875, 470, 235, 140),
    'sources': (470, 650, 350, 110),
    'result': (1170, 280, 215, 140),
    'operator': (15, 470, 205, 140),
}
PRODUCTS = {
    'devops': {
        'name': 'AWS DevOps Agent', 'scope': 'Agent Space: configured access, agents, retained context and execution records',
        'nodes': {
            'request': ('external', 'Request or signal', 'Question, incident or configured trigger'),
            'instructions': ('aws', 'Instructions / prompt', 'Managed AGENTS.md or custom system prompt'),
            'skills': ('aws', 'Skills', 'Applicable or explicitly assigned procedures'),
            'knowledge': ('aws', 'Memory stores', 'Relevant available entries; informational context'),
            'execution': ('aws', 'Agent execution', 'Managed role in a workflow, or one custom-agent invocation'),
            'connections': ('aws', 'Authorized source operations', 'Space associations and available tools; custom agents select a subset'),
            'learning': ('aws', 'Knowledge production', 'Learning runs and corrective feedback'),
            'sources': ('external', 'Connected source systems', 'AWS resources, telemetry, code and delivery'),
            'result': ('aws', 'Execution output', 'Findings, proposals, reports and run evidence'),
            'operator': ('external', 'Engineer / operator', 'Scope, verified feedback and action approval'),
        },
        'views': {
            'agent': ('An agent uses guidance, procedures, context and authorized operations', ['D-90','D-15','D-16'], ['request','instructions','skills','knowledge','execution','connections','sources','result']),
            'coordination': ('Managed responsibilities and knowledge reuse', ['D-91','D-15','D-M08'], ['request','execution','knowledge','learning','result','connections','sources']),
            'space': ('The Agent Space contains configuration and execution context', ['D-92','D-01','D-12'], list(BOXES)),
            'incident': ('Incident triage and current-evidence investigation', ['D-93','D-06'], ['request','execution','connections','sources','knowledge','result']),
            'mitigation': ('Mitigation planning and separately approved execution', ['D-93','D-M06'], ['operator','execution','connections','sources','result']),
            'learning': ('Investigation history and correction become later context', ['D-93','D-M01','D-M02','D-M08'], ['result','operator','learning','knowledge','execution']),
            'reporting': ('Service-health reporting reuses the same configured facilities', ['D-93','D-16','D-19'], ['request','instructions','skills','execution','connections','sources','result']),
            'knowledge': ('Procedure maintenance and environment documentation', ['D-93','D-M04','D-05'], ['operator','skills','sources','learning','knowledge','result']),
            'change': ('Configuration and release assurance use explicit subjects and effects', ['D-93','D-22'], ['request','instructions','execution','connections','sources','operator','result']),
            'review': ('An operational review consumes independently verified outputs', ['D-93','D-14'], ['result','operator','knowledge']),
        },
    },
    'security': {
        'name': 'AWS Security Agent', 'scope': 'Application Agent Space: selected sources, assessment configurations, runs and findings',
        'nodes': {
            'request': ('external', 'Assessment request', 'Target, revision or document scope'),
            'instructions': ('aws', 'Assessment settings', 'Assessment type, target rules and credentials'),
            'skills': ('aws', 'Requirement references', 'Shared packs applied to eligible reviews'),
            'knowledge': ('aws', 'Application context', 'Selected source, design and application documents'),
            'execution': ('aws', 'Assessment execution', 'Run or one-off review; not a customer-defined agent roster'),
            'connections': ('aws', 'Source and target access', 'Repository selection, network path and authenticated test identity'),
            'learning': ('aws', 'Specific retained state', 'Login procedure and eligible finding preferences'),
            'sources': ('external', 'Application and source systems', 'Deployed target, repository and documentation'),
            'result': ('aws', 'Assessment output', 'Findings, evidence and verification results'),
            'operator': ('external', 'Application team', 'Authorize, review, deploy and accept'),
        },
        'views': {
            'agent': ('Security assessment inputs and execution', ['S-90','S-12'], ['request','instructions','skills','knowledge','execution','connections','sources','result']),
            'coordination': ('Assessment, repair and verification are separate work records', ['S-91','S-10'], ['request','execution','result','operator','connections','sources']),
            'space': ('Application scope and shared assessment criteria', ['S-92','S-01'], list(BOXES)),
            'assessment': ('Assess source or an authorized running application', ['S-93','S-03','S-06'], ['request','instructions','knowledge','execution','connections','sources','result']),
            'repair': ('Finding triage, repair proposal, deployment and revalidation', ['S-93','S-05','S-M05'], ['result','operator','execution','connections','sources']),
            'context': ('Criteria, application context and narrowly scoped reuse', ['S-93','S-M03','S-M02','S-13'], ['skills','knowledge','learning','execution','result']),
        },
    },
    'finops': {
        'name': 'AWS FinOps Agent', 'scope': 'Agent instance: access roles, organizational context, conversations, tasks and connections',
        'nodes': {
            'request': ('external', 'Question or trigger', 'Query, explicit task, schedule or anomaly event'),
            'instructions': ('aws', 'Request / task instructions', 'Query basis and requested analysis'),
            'skills': ('aws', 'Context files', 'Ownership mappings, instructions and report templates'),
            'knowledge': ('aws', 'Persistent memory', 'Preferences, corrections and retained task outcomes'),
            'execution': ('aws', 'Analysis execution', 'Direct conversation or an explicitly created queued task'),
            'connections': ('aws', 'Data access and destinations', 'Agent data role; separate Jira or Slack connection'),
            'learning': ('aws', 'Context maintenance', 'Memory updates; session compaction is separate'),
            'sources': ('external', 'Underlying AWS sources', 'Cost Explorer, anomaly and recommendation services'),
            'result': ('aws', 'Analysis output', 'Answer, report artifact and recorded task result'),
            'operator': ('external', 'FinOps / service owner', 'Reconcile, authorize publication and own changes'),
        },
        'views': {
            'agent': ('FinOps analysis combines source data and organizational context', ['F-90','F-11'], ['request','instructions','skills','knowledge','execution','connections','sources','result']),
            'coordination': ('Requests and automations coordinate work through tasks', ['F-91','F-03'], ['request','execution','connections','result','operator']),
            'space': ('Instance-scoped context, work and destinations', ['F-92','F-01','F-09'], list(BOXES)),
            'analysis': ('Historical cost and anomaly analysis retain source provenance', ['F-93','F-M01'], ['request','instructions','execution','connections','sources','result']),
            'reporting': ('Periodic reporting adds a task definition and publication path', ['F-93','F-03','F-04','F-M06'], ['request','instructions','skills','execution','connections','result','operator']),
            'optimization': ('Recommendations are reviewed before engineering change and measurement', ['F-93','F-14'], ['sources','connections','execution','result','operator']),
        },
    },
}


def key_for(product, view):
    return 'teaching-'+product+'-'+view


def definitions():
    return {key_for(p,v):(title,
        'Fixed-position teaching view. Color identifies who defines the concept; heavy outlines identify the current path. Arrows show documented information use or explicitly labeled team actions, not internal RPCs or a universal agent orchestration graph.',
        refs, '') for p,data in PRODUCTS.items() for v,(title,refs,active) in data['views'].items()}


DIAGRAMS = definitions()


def render(key):
    product, view = key.removeprefix('teaching-').split('-',1)
    spec=PRODUCTS[product]; title,refs,active=spec['views'][view]
    basic=view=='agent'; show_scope=view not in ('agent','coordination')
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 825" role="img" aria-labelledby="{key}-title {key}-desc" data-diagram="{key}" data-layout="teaching-fixed-v1" data-product="{product}" data-view="{view}">',
         f'<title id="{key}-title">{escape(title)}</title>',
         f'<desc id="{key}-desc">{escape(DIAGRAMS[key][1])} {escape(spec["scope"])}.</desc>',
         '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8" fill="#465768"/></marker></defs>',
         '<style>text{font-family:Arial,sans-serif;fill:#182d3d}.label{font-size:20px;font-weight:600}.detail{font-size:17px}.tag{font-size:14px;font-weight:700}.edge{fill:none;stroke:#465768;stroke-width:2;marker-end:url(#arrow)}.edge-soft{fill:none;stroke:#6b7785;stroke-width:1.6;stroke-dasharray:7 5;marker-end:url(#arrow)}</style>']
    if show_scope:
        out.append('<rect x="240" y="35" width="900" height="580" rx="12" fill="#fbfcfd" stroke="#348761" stroke-width="2" stroke-dasharray="9 5"/>')
        label=spec['scope']
        if product=='security':
            label='Application execution scope; requirement packs are shared, not owned by the application'
        out.append(f'<text x="255" y="58" font-size="17">{escape(label)}</text>')
    # Connections are deliberately unchanged across views. Hidden context producers
    # are introduced only after the first single-agent explanation.
    paths=[('request','execution','M220 338 H270'),
           ('instructions','execution','M400 200 V270'),
           ('skills','execution','M690 200 V270'),
           ('knowledge','execution','M980 200 V270'),
           ('execution','result','M1110 338 H1170'),
           ('execution','connections','M645 400 V470'),
           ('connections','sources','M645 582 V650')]
    for a,b,d in paths:
        cls='edge' if a in active and b in active else 'edge-soft'
        reverse=' marker-start="url(#arrow)"' if (a,b) in (('execution','connections'),('connections','sources')) else ''
        out.append(f'<path data-edge="{a}-{b}" class="{cls}" d="{d}"{reverse}/>')
    out.append('<text x="665" y="438" font-size="16">invoke / observe</text>')
    out.append('<text x="665" y="636" font-size="16">authorized access</text>')
    if not basic:
        out.append('<path class="edge-soft" data-edge="result-learning" d="M1275 396 V603 H1118 V526 H1110"/>')
        if product == 'security':
            out.append('<path class="edge-soft" data-edge="reuse-execution" d="M995 470 V400"/>')
        else:
            out.append('<path class="edge-soft" data-edge="learning-knowledge" d="M995 470 V430 H1122 V220 H980 V200"/>')
        if product=='devops':
            out.append('<path class="edge-soft" data-edge="sources-learning" d="M820 694 H1155 V526 H1110"/>')
        out.append('<path class="edge-soft" data-edge="operator-execution" d="M220 523 H250 V365 H270"/>')
    if view in ('review','mitigation','repair','optimization'):
        out.append('<path class="edge-soft" data-edge="result-operator" d="M1275 420 V625 H118 V610"/>')
        out.append('<text x="250" y="643" font-size="16">team review / acceptance</text>')
    if product == 'devops' and view == 'learning':
        out.append('<path class="edge-soft" data-edge="operator-feedback" d="M118 610 V632 H855 V540 H875"/>')
        out.append('<text x="245" y="625" font-size="16">verified correction</text>')
    if product == 'devops' and view == 'knowledge':
        out.append('<path class="edge-soft" data-edge="operator-skill" d="M118 470 V242 H690 V222"/>')
        out.append('<text x="285" y="237" font-size="16">reviewed procedure</text>')
    for ident,(x,y,w,h) in BOXES.items():
        owner,head,body=spec['nodes'][ident]
        if basic and ident in ('learning','operator'):
            continue
        fill,stroke,tag=PALETTE[owner]
        weight='4' if ident in active else '1'
        out.append(f'<g data-node="{ident}" data-box="{x},{y},{w},{h}" data-owner="{owner}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>')
        out.append(f'<text class="tag" x="{x+12}" y="{y+20}">{tag}</text>')
        head_lines=textwrap.wrap(head,width=max(14,int((w-24)/11.2)))
        for i,line in enumerate(head_lines):
            out.append(f'<text class="label" x="{x+12}" y="{y+43+i*21}">{escape(line)}</text>')
        wrap=max(19,int((w-24)/9.0))
        body_lines=textwrap.wrap(body,width=wrap)
        for i,line in enumerate(body_lines):
            out.append(f'<text class="detail" x="{x+12}" y="{y+43+(len(head_lines)+i)*21}">{escape(line)}</text>')
        if ident == 'execution' and product == 'devops' and view in ('coordination','incident','mitigation'):
            for j,role in enumerate(('Incident triage','Incident RCA','Incident mitigation','Incident UI')):
                px=x+14+j*204
                out.append(f'<rect x="{px}" y="{y+82}" width="194" height="34" rx="3" fill="#ffffff" stroke="#348761"/>')
                out.append(f'<text x="{px+8}" y="{y+104}" font-size="17">{role}</text>')
        out.append('</g>')
    if view=='coordination':
        if product=='devops':
            line='Roles contribute to an investigation; this is not a mandatory sequence or an internal RPC diagram.'
        elif product=='security':
            line='Run → finding → repair proposal → deployed revision → revalidation. These are records, not named peer agents.'
        else:
            line='Direct conversation OR explicit task. Schedules and matching anomaly events create new tasks; not new agents.'
        for i,line_part in enumerate(textwrap.wrap(line,100)):
            out.append(f'<text x="285" y="{420+i*21}" font-size="17">{escape(line_part)}</text>')
    legend='DOC: documentation-defined  |  AWS: documented service concept  |  EXT: external system or team'
    out.append(f'<text x="20" y="810" font-size="17">{legend}</text>')
    out.append('</svg>')
    return ''.join(out)


def build_one(key, directory):
    Path(directory,key+'.svg').write_text(render(key),encoding='utf-8')
