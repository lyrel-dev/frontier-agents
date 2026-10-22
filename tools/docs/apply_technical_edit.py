"""Apply the final diagram and presentation corrections once."""
from pathlib import Path
from pprint import pformat
import ast
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
record=json.loads((ROOT/'qa/technical-edit-record.json').read_text())

def patch(relative, before, after):
    p=ROOT/relative;text=p.read_text()
    if text.count(before)!=1:raise ValueError(relative+': expected one anchor '+before[:90])
    p.write_text(text.replace(before,after),encoding='utf-8')


def assignment(relative,name,value):
    p=ROOT/relative;text=p.read_text();tree=ast.parse(text);lines=text.splitlines(keepends=True)
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    begin=sum(map(len,lines[:node.lineno-1]));end=sum(map(len,lines[:node.end_lineno]))
    p.write_text(text[:begin]+name+'='+pformat(value,width=105,sort_dicts=False)+'\n'+text[end:],encoding='utf-8')


def literal(relative,name):
    tree=ast.parse((ROOT/relative).read_text())
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    return ast.literal_eval(node.value)

patch('guides/devops.md','### D-07 — Custom-agent configuration and invocation','### D-07 — Operational queries and custom-agent invocations')
p=ROOT/'guides/devops.md';text=p.read_text();heading='### D-07 — Operational queries and custom-agent invocations\n\n'
text=text.replace(heading,heading+'Use the built-in Chat path for an operational question. Use a custom-agent definition when the task requires a prescribed prompt, selected tools, and reusable procedures. Both execution paths depend on configured source access. [DS407]\n\n',1);p.write_text(text)
patch('tools/docs/mechanism_detail.py','        for sid,items in sections.items():\n            if sid not in boundaries:', '        for sid,items in sections.items():\n            if sid=="D-07":items=sorted(items,key=lambda e:e["id"]!="MX-D-QUERY")\n            if sid not in boundaries:')

# Keep team checks out of AWS-owned state labels. Preserve the original palette.
path='tools/docs/mechanism_figures.py'
patch(path,r'history [label="AWS · Prior investigation\nEvidence and verified correction"];',r'history [label="AWS · Prior investigations\nRecorded evidence and conclusions"];'+'\n'+r'feedback [label="AWS · Investigation feedback\nOperator-supplied correction"];')
patch(path,r'history -> store [label="managed synthesis / correction"];',r'history -> store [label="managed synthesis"];'+'\n'+r'feedback -> store [label="corrective context"];'+'\n'+'{rank=same;history;feedback}')
patch(path,r'DOC · Separate checks\nExistence, observed read, correctness',r'DOC · Memory verification\nEntry identity, observed access, current evidence')
patch(path,r'AWS · Later login\nVerify the actual role reached',r'AWS · Later login\nAuthenticated application session')
patch(path,r'DOC · Independent interpretation\nAuthentication coverage is not finding repair',r'DOC · Engineering verification\nConfirm session identity and finding changes')
patch(path,r'DOC · Test the intended representation\nA successful answer alone does not identify its source',r'DOC · Context verification\nCheck file state, retained preference and query constraints')
patch(path,r'manual [label="AWS · Chat / on-demand task"];',r'manual [label="AWS · On-demand task request"];'+'\n'+r'chat [label="AWS · Conversation analysis\nDirect answer or action request"];')
patch(path,r'manual -> task [label="explicit task request"];',r'manual -> task [label="explicit task request"];'+'\n'+r'chat -> jira [label="direct requested action"];'+'\n'+r'chat -> slack [label="direct requested action"];')
patch(path,'{rank=same;manual;auto}','{rank=same;manual;auto;chat}')
patch(path,'Task creation, analysis and delivery have independent outcomes. Jira confirmation depends on invocation mode; Slack does not present a per-message confirmation prompt.', 'Conversations can request publication directly; explicit tasks and automations use the task queue. Jira confirmation depends on invocation mode. Slack has no per-message approval prompt.')

messages={
'Incident response outcomes':'Triage determines routing. Investigation evaluates current evidence. A mitigation plan is a proposal; execution requires the applicable action authorization and a separate recovery check.',
'Reporting and reliability outcomes':'A health report summarizes measurements for a defined period. A deployment review traces actual release records. Pattern analysis and prevention evaluation use multiple investigations to identify and prioritize follow-up work.',
'Operational knowledge and release assurance':'SOP consolidation maintains reviewed procedural content. Topology documentation records discovered and inferred relationships. Release-readiness analysis and active testing apply to different subjects and have different effects.',
'Service-health reporting: workflow dependencies':'Current telemetry is required for a health conclusion. Context is optional unless the reporting profile depends on it. A recurring profile adds a trigger; an external destination adds a separate publication operation.',
'Application, source and design assessment objectives':'Select the assessment by subject: a running target, a source revision, a design document, or a scoped system model. Authentication and network configuration are variants of the running-application assessment.',
'Finding disposition, repair and verification':'Disposition records the team decision about a finding. A remediation proposal changes source only after review and merge. Revalidation evaluates selected findings against the deployed target.',
'Application assessment: independent configuration choices':'Target authorization, public or private connectivity, application credentials, source context, and invocation mode are independent settings. Inspect each setting before interpreting coverage.',
'Historical cost, forecasting and commitment coverage':'Historical analysis reports observed cost under a specified query. Forecasting estimates a future period. Commitment coverage reports the covered share of eligible usage. Retain the source and calculation basis for each.',
'Reporting, anomaly investigation and optimization':'Reporting formats source analysis. Anomaly investigation evaluates a deviation. Recommendation review prioritizes upstream proposals; savings measurement evaluates an implemented change using comparable periods.',
'Cost-anomaly investigation: trigger and publication controls':'Inspect event matching, task creation, source queries, and publication as separate steps. Jira approval depends on how the action starts. Slack publication requires destination review before invocation.',
'Operational objectives, mechanisms and features':'The use case supplies the objective and completion criteria. Each workflow step links to a mechanism and its product feature. The implementation profile supplies environment-specific configuration and verification steps.',
'Service-health reporting: required and conditional dependencies':'A missing required data source blocks the corresponding conclusion. Optional history changes the available context. Schedule and destination dependencies apply only to profiles that enable them.',
'Operational-review profiles and evidence handoffs':'The reliability profile uses service measurements and incident records. The cost profile uses reconciled amounts and recommendations. Both produce decisions, assigned owners, and unresolved evidence requests; neither transfers service permissions.'}
renames={
'Incident response outcomes':'Incident triage, investigation, and mitigation',
'Reporting and reliability outcomes':'Health reporting, deployment review, and prevention',
'Sandbox and directed actions':'Sandbox execution and directed-action approval',
'Resource and context models':'Retained context: producers, consumers, and lifecycle',
'Tabletop: one operational symptom, three different jobs':'Exercise: incident, security, and cost evidence handoff'}
decks=literal('tools/docs/presentation.py','DECKS');removed=[]
for product,deck in decks.items():
    result=[]
    for index,slide in enumerate(deck['slides']):
        old_title=slide['title']
        if product=='architecture' and old_title=='Comparison framework':
            removed.append(index);continue
        if old_title in messages:slide['message']=messages[old_title]
        if slide['message'].startswith('Follow the operational objective through its workflow,'):
            raise ValueError('Missing specific presenter explanation: '+old_title)
        slide['title']=renames.get(old_title,old_title)
        for row in slide.get('data',[]):
            if row and row[0]=='Conversational memory' and len(row)>1:
                row[1]='Conversation preferences, corrections and task outcomes'
        if old_title=='Tasks, schedules and event automations':
            slide['message']='An automation stores the trigger and task instructions. Each created task has its own execution history and publication result.'
        if old_title=='Task execution and destination-specific approval':
            slide['title']='Conversation actions, queued tasks, and publication approval'
            slide['message']='A conversation can request Jira or Slack publication directly. Explicit tasks and automations use the queue. Jira confirmation depends on invocation mode; Slack has no per-message approval.'
        if old_title=='Use case families across the three platforms':
            for row in slide['data']:
                if row[0]=='Pattern analysis':row[2]='Finding personalization; cross-run trend analysis is team-composed'
            if 'A-02' not in slide['refs']:slide['refs'].append('A-02')
        if old_title=='Documentation and presentation acceptance criteria':
            slide.update(title='Operational prerequisites and verification records',refs=['A-03','A-04','A-05','A-06'],message='Check access, execution scope, context, effects, and result evidence separately. Record unmet prerequisites and unresolved results before handing work to the next owner.',data=[
                ['Check','Record to inspect','Failure interpretation'],
                ['Source access','Calling identity, selected operation and returned resource','An inaccessible source leaves an evidence gap.'],
                ['Execution scope','Configuration ID, revision, target and observation period','A completed run against the wrong subject is not acceptance.'],
                ['Retained context','Applicable file, memory or procedural state','Availability and observed use are separate checks.'],
                ['State-changing operation','Target, permitted effect and required approval','A generated recommendation is not authorization.'],
                ['Result and handoff','Source references, execution ID, reviewer and unresolved items','Completion and delivery do not establish correctness.']])
        result.append(slide)
    deck['slides']=result
    if product=='architecture':deck['title']='Cross-service architecture'
if len(removed)!=1:raise ValueError('Expected exactly one duplicate architecture slide')
assignment('tools/docs/presentation.py','DECKS',decks)
groups=literal('tools/docs/structure.py','DECK_CHAPTERS')
groups['architecture']=[(title,[i-sum(x<i for x in removed) for i in indexes if i not in removed]) for title,indexes in groups['architecture']]
groups['architecture']=[(title,indexes) for title,indexes in groups['architecture'] if indexes]
assignment('tools/docs/structure.py','DECK_CHAPTERS',groups)

# Check the corrected graph paths and ownership labels in future builds.
patch('tools/docs/editorial_check.py',"    from presentation import DECKS", "    from presentation import DECKS\n    from mechanism_figures import DIAGRAMS as MECHANISM_FIGURES")
patch('tools/docs/editorial_check.py',"    protected = {}", "    publication=MECHANISM_FIGURES['mechanism-finops-publication'][3]\n    if 'chat -> jira' not in publication or 'chat -> slack' not in publication:errors.append('Diagram omits direct conversation publication')\n    if 'Verify the actual role reached' in MECHANISM_FIGURES['mechanism-security-learning'][3]:errors.append('Team verification remains inside an AWS-owned state label')\n    if any(s['title']=='Documentation and presentation acceptance criteria' for d in DECKS.values() for s in d['slides']):errors.append('Document-quality meta-slide remains in the technical programme')\n    protected = {}")
record['diagram_review']={
 'basis':'Visual inspection of the supplied Stage 3 images and review of the maintained DOT source.',
 'corrections':['Separate prior investigations and operator feedback as memory inputs.','Move the verification instruction out of the AWS-owned authenticated-session node.','Replace generic interpretation labels with named checks.','Show direct conversation publication separately from queued tasks.'],
 'ownership_palette':'Unchanged DOC/AWS/EXT colors and labels.',
 'current_render_validation':'Performed by the subsequent build and browser checks; prior screenshots are not claimed as screenshots of the amended output.'}
record['presentation_review']={
 'removed_duplicate':'Architecture comparison table duplicated the product-configuration and execution comparison.',
 'replaced_meta_slide':'Document-quality criteria replaced with operational prerequisites and verification records.',
 'speaker_notes':'Repeated generic outcome-to-mechanism statements replaced with case-specific explanations.',
 'memory_producer':'Conversation preferences, corrections and task outcomes propagated to both comparison tables.',
 'timing':'Removed duplicate had a two-minute allocation; all other allocations retained.'}
(ROOT/'qa/technical-edit-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
Path(__file__).unlink()
print(json.dumps({'diagram_labels_and_paths_corrected':True,'duplicate_slides_removed':len(removed),'slides':sum(len(d['slides']) for d in decks.values()),'minutes':sum(s['seconds'] for d in decks.values() for s in d['slides'])//60}))
