#!/usr/bin/env python3
"""Finish the reviewed normalization once. Outputs, not this migration, are maintained."""
from pathlib import Path
from pprint import pformat
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
def load(name):return json.loads((ROOT/f'catalog/{name}.json').read_text())
def save(name,value):(ROOT/f'catalog/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def patch(path,old,new):
    text=path.read_text();assert old in text, f'Missing patch target in {path}: {old[:80]}'
    path.write_text(text.replace(old,new))

features=load('features');mechanisms=load('mechanisms');profiles=load('profiles');catalog=load('use-cases')
features['entries'].append({'id':'FT-D-QUERY','platform':'devops','title':'On-demand operational queries','group':'Operational inquiry','objects':['Agent Space','Chat request','Connected evidence'],'configuration':'Use the built-in conversational query path with an explicit service and observation interval. A custom-agent definition is not required for a native inquiry. Source access and the requested scope still apply.','sections':['D-01','D-12']})
mechanisms['entries'].append({'id':'MX-D-QUERY','platform':'devops','title':'Built-in operational inquiry','features':['FT-D-QUERY','FT-D-SOURCES'],'sections':['D-01','D-12'],'trigger':'A scoped conversational question','state':'Request context and connected source evidence','process':'Use the built-in on-demand inquiry path to answer the operational question using available authorized evidence.','effect':'Source read and conversational result','verification':'Inspect scope and reproduce a material observation from the same source query.','on_failure':'Name the missing source and qualify or withhold the answer; creating a custom agent does not by itself repair source access.'})
profiles['entries'] += [
 {'id':'PR-D-QUERY','title':'Native operational-query configuration','platforms':['devops'],'mechanisms':['MX-D-QUERY','MX-D-READ'],'parameters':[['Agent Space','Operator and data access for the relevant environment','Approved space'],['Question scope','Actual service, UTC interval and dimensions','Declared recent observation period']], 'setup':['Verify access to the sources needed for this question.','Ask through the built-in query path, stating service and observation scope.','Inspect returned evidence and reconcile a material observation.'],'tests':['A missing signal is disclosed rather than interpreted as healthy.','The answer uses the requested window and dimensions.'],'stop_behavior':'End or redirect an unsupported inquiry. No custom-agent schedule or external publication is implied.'},
 {'id':'PR-D-PROCEDURE','title':'Reviewed runbook-skill configuration','platforms':['devops'],'mechanisms':['MX-D-SKILL','MX-D-INSTRUCTIONS'],'parameters':[['Procedure source','One approved SOP after conflict resolution','Reviewed source in Git'],['Applicability','Symptoms, services and agent scope','Specific operational situation'],['Tool references','Real tool names used by the procedure','Selected supported operations']], 'setup':['Reconcile conflicting SOPs and obtain an accountable review.','Package the approved procedure as a skill with its applicability description.','Keep broadly applicable reporting conventions in standing instructions only where appropriate.','Test a matching and a nonmatching request using non-sensitive evidence.'],'tests':['Irrelevant tasks do not require the skill.','Required tools exist and unsupported steps stop explicitly.','Changes to standing instructions are tested in a new applicable session.'],'stop_behavior':'Deactivate or revise the relevant procedural configuration using the supported controls. Changing a skill does not undo past actions or grant new access.'},
 {'id':'PR-D-KNOWLEDGE','title':'Environment-knowledge review configuration','platforms':['devops'],'mechanisms':['MX-D-TOPOLOGY','MX-D-READ','MX-D-RECALL'],'parameters':[['Environment scope','Selected accounts, services and connected evidence','Approved resource and repository scope'],['Reference change','Known deployed relationship to verify','New dependency and exact revision'],['Reviewed output','Owner-maintained service description','Evidence-linked topology document']], 'setup':['Verify the relevant discovery and connected sources.','Inspect the managed knowledge refresh and resulting version where available.','Compare a known changed relationship with actual source evidence.','Maintain the owner-reviewed description with unresolved relationships identified.'],'tests':['An inferred edge remains distinguishable from an observed relationship.','A submitted refresh is not treated as completed knowledge production.','A missing graph resource is not automatically interpreted as denied direct access.'],'stop_behavior':'Do not widen permissions to conceal a representation gap. Use authoritative source evidence and record unverified context.'}
]
for p in profiles['entries']:
    if p['id']=='PR-D-INCIDENT':
        p['title']='Incident and prevention configuration'
        p['parameters'].insert(0,['Operation','Investigation, routing, feedback or prevention evaluation','Select the operation matching the objective'])
        p['setup'][1]='For incident work, start from a signal or scoped manual investigation. For prevention work, inspect a manual or scheduled evaluation over existing investigation evidence.'

M={m['id']:m for m in mechanisms['entries']}
def step(mid,title,purpose,dependency,condition):
    m=M[mid]
    return {'title':title,'actor':'Service execution; accountable engineer reviews the result','purpose':purpose,'mechanism':mid,'dependency':dependency,'condition':condition,'configuration_features':m['features'],'effect':m['effect'],'verification':m['verification'],'on_failure':m['on_failure']}
for e in catalog['entries']:
    if e['id']=='UC-D06':
        e['profiles'].insert(0,'PR-D-QUERY')
        e['workflow'].insert(1,step('MX-D-QUERY','Answer a native health inquiry','Use the built-in query path for the native snapshot profile.','conditional','The built-in conversational snapshot profile is selected.'))
        for s in e['workflow']:
            if s['mechanism']=='MX-D-CUSTOM':s.update(dependency='conditional',condition='A configured snapshot, comparison or recurring-report profile is selected.')
            if s['mechanism']=='MX-D-SCHEDULE':s['condition']='Recurring execution of the configured reporting profile is selected.'
        e['sections']=list(dict.fromkeys(e['sections']+['D-01']))
    if e['id']=='UC-D10':e['profiles']=['PR-D-PROCEDURE']
    if e['id']=='UC-D11':e['profiles']=['PR-D-KNOWLEDGE','PR-EVIDENCE']
    if e['id']=='UC-S01':
        for s in e['workflow']:
            if s['mechanism']=='MX-S-CONTEXT':s.update(dependency='optional',condition='Source code or documentation is selected to enrich application context.')
    if e['id']=='UC-F04':
        e['workflow'] += [step('MX-F-JIRA','Publish to the configured Jira destination','Create the supported report follow-up in the approved project.','optional','Jira distribution is selected and invocation-specific authorization is satisfied.'),step('MX-F-SLACK','Publish to the configured Slack channel','Deliver the permitted report summary to its reviewed audience.','optional','Slack distribution is selected; audience review occurs before direct publication.')]
        e['sections']=list(dict.fromkeys(e['sections']+['F-05','F-M06']))
for name,data in [('features',features),('mechanisms',mechanisms),('profiles',profiles),('use-cases',catalog)]:save(name,data)

# Preserve print rules from the maintained stylesheet rather than overriding hidden globally.
patch(HERE/'catalog.py',' [hidden]{display:none!important}',' @media screen{[hidden]{display:none!important}}')
patch(HERE/'check.py',"page.locator('#UC-S01 dl').is_visible()","page.locator('#UC-S01 > .case-reference > dl').is_visible()")
patch(HERE/'check.py','import argparse','import argparse\nimport traceback')
patch(HERE/'check.py',"errors.append(f'{key} at {width}px: '+str(exc))","errors.append(f'{key} at {width}px: '+str(exc)+'; '+traceback.format_exc(limit=2))")
patch(HERE/'model_check.py',"page.locator('#UC-D06 .workflow-steps > li').count()==4","page.locator('#UC-D06 .workflow-steps > li').count()==len(next(c for c in cases if c['id']=='UC-D06')['workflow'])")

# Former supporting labels remain discoverable without inflating the primary outcome count.
renderer=HERE/'catalog.py';text=renderer.read_text()
text=text.replace("    for (platform,group),items in groups.items():","    parts.append(supporting_matches(key))\n    for (platform,group),items in groups.items():")
text=text.replace('No cases match these filters.','No primary outcomes match these filters. Matching supporting references, when present, appear below.')
text=text.replace("('features','Platform features and change impact'","('features','Workflow features and change impact'")
text=text.replace('Inspect the concrete configuration surface and trace which mechanisms, implementation profiles and outcomes depend on it.','Inspect the features used by these workflows and trace their mechanism and profile dependencies. This selected inventory is not an exhaustive service feature matrix.')
insert='''
def supporting_matches(key=None):
    result=[]
    for a in records('aliases'):
        if not a['disposition'].startswith('Supporting'):continue
        platform={'D':'devops','S':'security','F':'finops'}[a['id'][0]]
        if key and key!=platform:continue
        result.append('<li data-support-item data-platform="'+platform+'" hidden>'+esc(a['title'])+' — '+' · '.join(link(t) for t in a['targets'])+'</li>')
    return '<aside data-supporting-matches hidden><h2>Related supporting references</h2><p>These former labels describe configuration or mechanisms, not additional primary cases.</p><ul>'+''.join(result)+'</ul></aside>'

'''
text+=insert
script_add='''
 document.querySelectorAll('[data-usecase-catalog]').forEach(root=>{
  const q=root.querySelector('[data-uc-search]'),p=root.querySelector('[data-uc-platform]'),box=root.querySelector('[data-supporting-matches]');if(!box)return;
  function filterSupport(){const words=q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);let n=0;box.querySelectorAll('[data-support-item]').forEach(el=>{const yes=words.length>0&&words.every(w=>el.textContent.toLowerCase().includes(w))&&(!p?.value||p.value===el.dataset.platform);el.hidden=!yes;if(yes)n++;});box.hidden=n===0;}
  q.addEventListener('input',filterSupport);if(p)p.addEventListener('input',filterSupport);root.querySelector('[data-uc-reset]').addEventListener('click',()=>setTimeout(filterSupport,0));addEventListener('hashchange',()=>setTimeout(filterSupport,0));filterSupport();
 });
'''
text=text.replace(" const input=document.querySelector('[data-ref-search]')",script_add+" const input=document.querySelector('[data-ref-search]')")
compile(text,str(renderer),'exec');renderer.write_text(text)
patch(HERE/'model_check.py',"page.locator('[data-uc-reset]').click();page.locator('#UC-D06 summary').click()","page.locator('[data-uc-reset]').click();page.locator('[data-uc-search]').fill('Persistent reporting preferences')\n                    assert page.locator('[data-supporting-matches]').is_visible()\n                    assert page.locator('[data-supporting-matches] a[href=\"../catalog/mechanisms.html#MX-F-MEMORY\"]').is_visible()\n                    page.locator('[data-uc-reset]').click();page.locator('#UC-D06 summary').click()")

# Preserve a small, explicit comparison of alternate implementation paths in the teaching deck.
from presentation import DECKS
from structure import CHAPTERS,DECK_CHAPTERS,TYPES,LABELS
for s in DECKS['devops']['slides']:
    if s['title']=='Service-health reporting: workflow dependencies':
        s['data']=[['Workflow step','Mechanism and configuration','Completion or failure decision'],['Read current observations','Authorized evidence sources and explicit scope','Missing current data prevents a health conclusion.'],['Choose the execution profile','Built-in operational query OR configured custom agent','A native inquiry does not require a custom definition.'],['Use relevant context','Optional available memory or reviewed reporting procedure','Retained history never substitutes for current observations.'],['Repeat or publish','Conditional schedule and optional destination','Timing and publication controls remain separate from the report objective.']]
        s['message']='One reporting objective has native and configured implementations. Required evidence, optional context and conditional execution remain explicit.'
(HERE/'presentation.py').write_text('"""Maintained HTML teaching sequence."""\nDECKS = '+pformat(DECKS,width=110,sort_dicts=False)+'\n')

review=ROOT/'qa/source-review.json';data=json.loads(review.read_text())
data['catalog_consolidation']['additional_check']='Built-in on-demand queries versus user-defined custom reporting were reconfirmed from the Custom Agents overview. FinOps invocation-dependent publication and the Security configuration/run lifecycle were also rechecked. Source absence was not interpreted as feature removal.'
review.write_text(json.dumps(data,indent=2)+'\n')
for p in (HERE/'catalog.py',HERE/'check.py',HERE/'model_check.py'):compile(p.read_text(),str(p),'exec')
Path(__file__).unlink()
