#!/usr/bin/env python3
"""Apply the reviewed catalog normalization once; remove migration inputs afterward."""
from pathlib import Path
from collections import defaultdict
from pprint import pformat
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
source=ROOT/'catalog/use-cases.json'
old=json.loads(source.read_text())
assert old.get('schema_version',1)==1
original={e['id']:e for e in old['entries']}
assert len(original)==54
plans=[]
for name in ('case-plan-devops.json','case-plan-security-finops.json'):
    plans.extend(json.loads((ROOT/'catalog'/name).read_text()))
mechanisms={m['id']:m for m in json.loads((ROOT/'catalog/mechanisms.json').read_text())['entries']}
entries=[];alias_map={}
for plan in plans:
    previous=[original[x] for x in plan['from']]
    e=dict(previous[0])
    e.update({k:v for k,v in plan.items() if k not in ('from','steps')})
    e['schema_version']=2
    e['platforms']=plan.get('platforms',[plan['platform']])
    e['legacy_ids']=plan['from']
    e['aliases']=[p['title'] for p in previous]
    e['summary']=plan['objective']
    e['narrative_status']='Authored engineering workflow using documented mechanisms; not an executed service result.'
    e['steps_basis']='The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.'
    e['sections']=list(dict.fromkeys(s for p in previous for s in p['sections']))
    e['workflow']=[]
    for row in plan['steps']:
        mid,title,purpose,*tail=row
        dependency=tail[0] if tail else 'required'
        condition=tail[1] if len(tail)>1 else 'Applies to the selected implementation.'
        m=mechanisms.get(mid)
        s=dict(title=title,purpose=purpose,mechanism=mid,dependency=dependency,condition=condition,actor='Service execution; accountable engineer reviews the result' if m else 'Responsible engineer or reviewer',configuration_features=m['features'] if m else [],effect=m['effect'] if m else 'Team decision; no implicit service action',verification=m['verification'] if m else 'Record the decision with the source identifiers and evidence needed for the case completion criteria.',on_failure=m['on_failure'] if m else 'Keep the result unresolved and assign the missing decision or evidence to an owner.')
        e['workflow'].append(s)
        if m and m['platform']==e['platform']:
            e['sections']=list(dict.fromkeys(e['sections']+m['sections']))
    e['variants']=[dict(name=v[0],changes=v[1],controls=v[2]) for v in plan['variants']]
    for oid in plan['from']:
        item=alias_map.setdefault(oid,dict(id=oid,title=original[oid]['title'],disposition='Retained outcome or consolidated variant',targets=[]))
        item['targets'].append(e['id'])
    entries.append(e)

# The shared review has its own narrative and native profile dependencies, not mixed source identifiers.
shared=next(e for e in entries if e['id']=='UC-G01')
shared.update(sections=['A-05','A-06','A-U01'],delivery='Team-composed workflow',availability='Component feature eligibility applies; no native cross-product orchestrator',inputs='Reviewed reliability or cost evidence, prior action list, decision owners and reporting period.',output='Decision-oriented agenda with evidence references, owners and next verification dates.',constraints='Independent products keep their own access and runtime state. A handoff does not transfer credentials or approval.',example='Prepare the operational review from the reviewed reports and prior action list; identify decisions, evidence, owners and unresolved questions.')
next(e for e in entries if e['id']=='UC-D06').update(delivery='Native inquiry or configured reporting',cadence='On demand or scheduled',availability='Selected native or custom-agent path; inspect feature-specific eligibility',inputs='Service identity, complete periods, selected telemetry tools and report instructions; optional relevant context.',output='Sourced health snapshot, period comparison or trend report.',example='Report service health for the declared period and comparison basis, showing material changes and unavailable signals.')
next(e for e in entries if e['id']=='UC-S01').update(delivery='Configured application assessment',cadence='Manual, recurring or supported pipeline path',availability='On-demand and optional invocation paths have different feature eligibility',inputs='Authorized target, actual deployed revision, network scope, test identities where needed, sources and work limits.',constraints='Testing can change application state. Network and identity variants preserve the same assessment objective but require their own authorization and coverage evidence.')
next(e for e in entries if e['id']=='UC-F01').update(cadence='On demand',inputs='Complete dates, metric, currency, account scope, grouping and optional ownership mapping.',output='Reconciled total, breakdown or historical variance with attribution limits.',example='Analyze the selected complete periods using the same basis; reconcile totals and explain only the changes supported by evidence.')
next(e for e in entries if e['id']=='UC-F02').update(inputs='Forecast horizon, cost basis, account scope and supported upstream forecast source.',output='Reviewed forecast with source and planning limitations.',example='Review the forecast for the specified horizon and scope; separate projections from observed costs.',constraints='A projection is not realized expenditure and does not authorize a commitment purchase.')
next(e for e in entries if e['id']=='UC-F03').update(inputs='Commitment type, observation period, eligible workload scope and supported coverage source.',output='Reviewed commitment coverage observation.',example='Review existing commitment coverage for the selected usage and period without recommending or executing a purchase.',constraints='Coverage, utilization and forecasts answer different questions. Purchasing requires its own decision and authority.')
next(e for e in entries if e['id']=='UC-F05').update(cadence='On demand or supported anomaly event',delivery='Native analysis with optional automation')

support={'D-UC15':'MX-D-INSTRUCTIONS','D-UC17':'MX-D-TOPOLOGY','D-UC20':'PR-EVIDENCE','S-UC05':'MX-S-LOGIN','S-UC07':'MX-S-JIRA','S-UC12':'MX-S-CRITERIA','S-UC16':'PR-S-PIPELINE','F-UC11':'MX-F-FILES','F-UC12':'MX-F-MEMORY','F-UC13':'MX-F-SCHEDULE','F-UC14':'MX-F-JIRA','F-UC15':'MX-F-SLACK','F-UC16':'MX-F-ARTIFACT'}
for oid,target in support.items():
    assert oid not in alias_map
    alias_map[oid]=dict(id=oid,title=original[oid]['title'],disposition='Supporting mechanism or configuration procedure',targets=[target])
alias_map['F-UC04']['disposition']='Split: forecast and commitment coverage have different completion criteria'
assert len(entries)==30 and len({e['id'] for e in entries})==30
assert set(alias_map)==set(original)
intros={
 'Incident response':'Incident response moves from signal routing to investigation, then to mitigation planning and separately authorized execution. A status bulletin communicates progress without becoming a new diagnosis.',
 'Operational reporting':'Health reports and change-activity reviews produce comparable observations. Their cadence and presentation format are choices within a defined objective; a later operational review uses the results for decisions.',
 'Reliability improvement':'Pattern identification establishes recurring evidence. Prevention prioritization decides which proposals deserve owned implementation. These are related but independently reviewable outcomes.',
 'Operational knowledge':'Procedure consolidation produces reviewed instructions; topology documentation produces an owner-reviewed system description. Both use source evidence, but their maintained outputs differ.',
 'Configuration assurance':'A scoped audit compares actual resource settings with approved rules and retains unassessed resources as gaps rather than passes.',
 'Release assurance':'Readiness analysis examines a proposed revision, while active testing exercises a deployed target. Source evidence, application effects and completion criteria are different.',
 'Application assessment':'The assessment objective remains stable while network path, application identities and invocation mode vary. Each combination must preserve authorized scope and record actual coverage.',
 'Source and design assessment':'Code review, design review and threat modeling examine different evidence and produce different review objects. Variants within an assessment must not erase its resource lifecycle.',
 'Findings and repair':'Disposition, a proposed source repair and verification of a deployed repair are distinct outcomes linked by finding identity.',
 'Assessment governance':'Maintaining requirements is controlled authoring work. Applying those requirements during an assessment is a supporting mechanism, not another duplicate case.',
 'Cost analysis':'Historical analysis starts with a reproducible query. Totals, dimensional breakdowns and variance are analytical profiles; monetary attribution is not automatically operational causality.',
 'Planning and commitments':'A forecast projects expenditure. Commitment coverage describes eligible usage covered by existing commitments. Their evidence and completion criteria remain separate.',
 'Cost reporting':'A report retains a comparable period and analytical basis for a defined audience. Recurrence and external publication are separately configured choices.',
 'Anomalies and optimization':'Anomaly investigation explains a deviation, recommendation review prioritizes proposed work, and post-change measurement evaluates observed outcomes. Estimates do not replace measurements.',
 'Operational governance':'An operational review assembles reviewed results into decisions and owned follow-up. Reliability and cost-management profiles share a meeting narrative, not credentials or an execution runtime.'}
source.write_text(json.dumps(dict(schema_version=2,revision='2026-10-22-linked-catalog',description='Thirty outcome-oriented use cases linked through explicit workflow steps to mechanisms, platform features and configuration profiles.',entries=entries,group_introductions=intros,classification_boundary='Outcome grouping, workflow order, configuration recipes and acceptance tests are authored engineering design, not an AWS service schema.'),ensure_ascii=False,indent=2)+'\n')
(ROOT/'catalog/aliases.json').write_text(json.dumps(dict(schema_version=2,entries=sorted(alias_map.values(),key=lambda x:x['id'])),ensure_ascii=False,indent=2)+'\n')

# Replace catalog rendering, not the detailed guide renderer.
build=HERE/'build.py';text=build.read_text()
text=text.replace('from diagrams import DIAGRAMS, build as build_diagrams','from diagrams import DIAGRAMS, build as build_diagrams\nimport catalog as catalogue')
text=text.replace("'finops':'AWS FinOps Agent'}","'finops':'AWS FinOps Agent','architecture':'Shared operational practice'}")
a=text.index('def catalog_sources(');b=text.index('def report(',a)
text=text[:a]+'''def catalog_sources(e,guides):return catalogue.sources(e,guides)
def catalog_controls(entries,platform=False):return catalogue.controls(entries,platform)
def catalog_entry(e,guides,embedded=False):return catalogue.entry(e,guides,embedded)
def catalog_content(catalog,guides,key=None):return catalogue.content(catalog,guides,key)

'''+text[b:]
a=text.index('def build_catalog(');b=text.index('def indexes(',a)
text=text[:a]+'''def build_catalog(catalog,guides):
    catalogue.build_pages(catalog,guides,frame,write)

'''+text[b:]
text=text.replace("cases=[e for e in catalog['entries'] if e['platform']==key]","cases=[e for e in catalog['entries'] if catalogue.includes(e,key)]")
text=text.replace("write(f'guides/{key}.html',frame(deck['title']+' — guide',body,'report',key))","write(f'guides/{key}.html',catalogue.decorate(frame(deck['title']+' — guide',body,'report',key)))")
text=text.replace('The catalog is an application layer, not a competing definition of platform capabilities.','Workflow steps link to shared mechanisms, concrete feature configuration and implementation profiles. Browse the [mechanism index](catalog/mechanisms.html), [feature impact index](catalog/features.html), [profiles](catalog/profiles.html) and [consolidation map](catalog/migration.md).')
text=text.replace('catalog/         Maintained narrative JSON; generated HTML and Markdown','catalog/         Canonical cases, mechanisms, features, profiles and alias data; generated reading indexes')
text=text.replace('use-case narratives in `catalog/use-cases.json`','cases in `catalog/use-cases.json`, mechanism and feature relationships in `catalog/mechanisms.json` and `catalog/features.json`, and recipes in `catalog/profiles.json`')
text=text.replace('Figures are logical models of the documented resource relationships and workflow steps,','Figures are logical models of documented resource relationships or explicitly labeled documentation dependencies,')
compile(text,str(build),'exec');build.write_text(text)

# One JS filter supports a shared outcome in more than one platform profile.
js=HERE/'interactions.js';text=js.read_text()
text=text.replace("el.value===entry.dataset[name]","(name==='platform'?entry.dataset.platform.split(' ').includes(el.value):el.value===entry.dataset[name])")
js.write_text(text)

# Update assertions to the normalized model instead of preserving obsolete record counts.
check=HERE/'check.py';text=check.read_text()
text=text.replace('from structure import BASELINE','from structure import BASELINE\nfrom model_check import validate_model')
text=text.replace("sum(e['platform']==key for e in entries)","sum(key in e.get('platforms',[e['platform']]) for e in entries)")
text=text.replace("count()==22","count()==15")
text=text.replace("#D-UC07","#UC-D05").replace("location.hash='S-UC01'","location.hash='UC-S01'").replace("#S-UC01","#UC-S01")
text=text.replace("html_paths=[ROOT/'index.html',ROOT/'catalog/index.html',ROOT/'presentations/index.html'","html_paths=[ROOT/'catalog/mechanisms.html',ROOT/'catalog/features.html',ROOT/'catalog/profiles.html',ROOT/'index.html',ROOT/'catalog/index.html',ROOT/'presentations/index.html'")
text=text.replace('    if browser and not errors:','    model_result=validate_model(guides, browser=browser)\n    errors.extend(model_result["errors"])\n    if browser and not errors:')
text=text.replace("    write('qa/checks.json',json.dumps(results,indent=2))","    results['relationship_model']=model_result\n    write('qa/checks.json',json.dumps(results,indent=2))")
text=text.replace('Checks cover stable section identifiers,','The [relationship checks](qa/relationships.json) additionally validate all 54 former-record mappings, 30 outcome definitions, workflow dependency types, feature configuration references, implementation profiles, reverse impact links and semantic regression cases. These are modeled dependencies, not live availability tests.\\n\\nChecks cover stable section identifiers,')
compile(text,str(check),'exec');check.write_text(text)

# Add the conceptual model to the existing architecture guide, not another parallel book.
body='''### A-09 — Operational objectives and implementation dependencies

A use case describes an operational objective with a recognizable completion condition. Its workflow identifies the sequence of work and the decisions needed to reach that condition. Mechanisms describe how the service carries out individual parts of that work, while platform features identify concrete objects and configuration surfaces. These are different reading levels, not competing names for the same catalog entry. The classification below is an editorial model; the services retain their own resource hierarchies and execution lifecycles. [AS30] [AS31] [AS32]

![Outcome, workflow, mechanism, and feature relationships](../assets/diagrams/workflow-feature-map.svg)

The catalog starts with the outcome rather than with the trigger or output format. For example, a service-health snapshot and a recurring health report share a health-reporting objective but use different execution profiles. A private authenticated penetration test is a configuration of the application-assessment case. In contrast, mitigation planning and execution remain separate because approving a proposal and changing a resource require different evidence and authority.

Each workflow step names the responsible actor, required mechanism, configuration features, effect, acceptance evidence, and behavior when the step cannot proceed. A required dependency blocks that selected implementation when it is missing. An optional dependency can be omitted with the stated limitation. A conditional dependency applies only when the named variant is selected. These declarations belong to the authored workflow; they are not claims that every AWS invocation uses the same sequence.

Consider service-health reporting. Current telemetry is required to assert current health. Retained service context can help interpret names and relationships, but missing history may still permit a qualified current-state report. A schedule is needed only for recurring execution; it does not define the measurement window. External publication adds a destination-specific effect rather than becoming another report use case. The configuration procedure is in D-07, and the source/knowledge paths are described in D-03, D-M01 and D-M07.

Knowledge production and knowledge use also have different lifecycles. A learning or feedback path produces retained context. A later execution selects relevant available context and compares it with current evidence. The maintained explanation is in A-02 and the product knowledge chapters; a retained entry's existence, an observed read and a correct result remain separate observations. None establishes customer-controlled model training. [AS04] [AS05] [AS06] [AS07]

Configuration recipes collect choices that are reused across cases: actual resource identifiers, selected tools, context references, schedule semantics, destinations and proposed acceptance tests. A recipe is not a universal agent deployment schema. In particular, automated Jira publication and interactive Jira publication have different FinOps approval behavior, and active application testing has effects that cannot be characterized only by infrastructure permissions. These controls remain attached to the selected execution path after consolidation. [AS10] [AS11] [AS12]

The linked catalog supports three reading directions. Start with an outcome to see its workflow and required configuration. Start with a mechanism to find all steps and profiles that use it. Start with a feature to inspect the outcomes potentially affected when it is disabled or changed. Reverse dependency links describe documentation relationships, not a live diagnosis of an account. [AS30] [AS31] [AS32]

The shared operational-review case combines reviewed reliability or cost-management results into decisions, owners and follow-up. Each service uses its own sources and authority. The review carries evidence identity and unresolved questions, not credentials, shared memory or inherited approval. A-06 describes that team handoff.

'''
guide=ROOT/'guides/architecture.md';text=guide.read_text();anchor='### A-01 —'
assert anchor in text
text=text.replace(anchor,body+anchor,1);guide.write_text(text)

from structure import CHAPTERS,DECK_CHAPTERS,TYPES,LABELS
from presentation import DECKS
CHAPTERS['architecture'][0]['sections'].insert(1,'A-09');TYPES['A-09']='overview'

def slide(title,rows,refs,seconds=180,kind='table',diagram=None):
    value=dict(title=title,seconds=seconds,refs=refs.split(),kind=kind,data=rows,message='Follow the operational objective through its workflow, configured mechanisms and independent completion evidence. The catalog links each dependency to its detailed guide.')
    if diagram:value['diagram']=diagram
    return value
by_id={e['id']:e for e in entries}
def outcome_slide(title,ids,refs):
    rows=[['Operational outcome','Completion evidence','Implementation boundary']]
    for ident in ids:
        e=by_id[ident];rows.append([e['title'],e['completion'][0],e['delivery']])
    return slide(title,rows,refs)
new_groups={
 'devops':[
    outcome_slide('Incident response outcomes',['UC-D01','UC-D02','UC-D03','UC-D04','UC-D05'],'D-06 D-M06'),
    outcome_slide('Reporting and reliability outcomes',['UC-D06','UC-D07','UC-D08','UC-D09'],'D-07 D-06'),
    outcome_slide('Operational knowledge and release assurance',['UC-D10','UC-D11','UC-D12','UC-D13','UC-D14'],'D-M04 D-M08 D-09'),
    slide('Service-health reporting: workflow dependencies',[['Workflow step','Mechanism and configuration','Completion or failure decision'],['Read current measurements','Selected telemetry tools and invocation scope','Missing current evidence prevents a health conclusion.'],['Interpret service context','Relevant available memory; explicit custom-agent attachment where applicable','Optional history is not a substitute for measurements.'],['Produce the report','Reviewed custom-agent definition and reporting procedure','Check observation window, dimensions and failed reads.'],['Repeat or distribute','Optional trigger; separately reviewed destination','Schedule and publication are conditional, not new cases.']],'D-03 D-07 D-M01 D-M07')],
 'security':[
    outcome_slide('Application, source and design assessment objectives',['UC-S01','UC-S02','UC-S03','UC-S04'],'S-01 S-06'),
    outcome_slide('Finding disposition, repair and verification',['UC-S05','UC-S06','UC-S07','UC-S08'],'S-05 S-M05 S-M04'),
    slide('Application assessment: independent configuration choices',[['Choice','Supporting mechanism','Control preserved'],['Network path','Target scope and public/private connectivity','Reachability does not enlarge owner authorization.'],['Application role','Credential resolution, login and optional procedure reuse','Failed login leaves protected paths unassessed.'],['Invocation','Manual, recurring or supported pipeline path','Every run records current revision and coverage.'],['Criteria and closure','Findings, source evidence and separate revalidation','Non-reproduction is scoped to the selected issue and valid test conditions.']],'S-03 S-M01 S-M02 S-04 S-M05')],
 'finops':[
    outcome_slide('Historical cost, forecasting and commitment coverage',['UC-F01','UC-F02','UC-F03'],'F-M01 F-08'),
    outcome_slide('Reporting, anomaly investigation and optimization',['UC-F04','UC-F05','UC-F06','UC-F07'],'F-03 F-04 F-M01'),
    slide('Cost-anomaly investigation: trigger and publication controls',[['Step','Feature configuration','Acceptance boundary'],['Create work','Explicit task or supported anomaly automation','Event matching and queued execution are separate.'],['Investigate','Authorized cost, anomaly and optional change evidence','Reconcile amounts; correlation is not proven cause.'],['Publish to Jira','Configured project and invocation type','Interactive approval differs from setup-authorized automation.'],['Publish to Slack','Configured channel and audience','No per-message approval prompt; review scope before invocation.']],'F-M05 F-M01 F-M06')]
}
for key,deck in DECKS.items():
    rebuilt=[];groups=[]
    for title,indexes in DECK_CHAPTERS[key]:
        current=[deck['slides'][i] for i in indexes]
        if 'use case' in title.lower() and key in new_groups:current=new_groups[key];title='Operational objectives and implementation'
        start=len(rebuilt);rebuilt.extend(current);groups.append((title,list(range(start,len(rebuilt)))))
    if key=='architecture':
        additions=[slide('Operational objectives, mechanisms and features',[], 'A-09',120,'diagram','workflow-feature-map'),slide('Service-health reporting: required and conditional dependencies',[['Element','Purpose','Configuration and evidence'],['Current telemetry','Required basis for the health conclusion','Selected source tools; verify period and material measurement.'],['Historical context','Optional interpretation of prior behavior','Available relevant memory; distinguish retrieval from correctness.'],['Recurring execution','Conditional on the chosen reporting profile','Configured trigger; timing and measurement window differ.'],['External destination','Optional publication effect','Destination-specific authorization and delivery result.']],'A-09 A-02 A-04'),slide('Operational-review profiles and evidence handoffs',[['Profile','Reviewed inputs','Review outcome'],['Reliability','Health, deployments, incident patterns and prevention proposals','Priorities, owners and evidence needed for closure.'],['Cost management','Reconciled amounts, anomalies, recommendations and measured outcomes','Decisions with estimates separate from observed benefits.'],['Combined team review','Independently configured service results','Retained source identities; no shared credentials or approval.']],'A-06 A-09 A-U01')]
        # Insert after the first architecture chapter and rebuild indices without changing existing order.
        ordered=[(t,[rebuilt[i] for i in ids]) for t,ids in groups]
        ordered.insert(1,('Outcome and implementation relationships',additions))
        rebuilt=[];groups=[]
        for title,items in ordered:
            start=len(rebuilt);rebuilt.extend(items);groups.append((title,list(range(start,len(rebuilt)))))
    deck['slides']=rebuilt;DECK_CHAPTERS[key]=groups
(HERE/'presentation.py').write_text('"""Maintained HTML teaching sequence; all budgets include the defined exercises."""\nDECKS = '+pformat(DECKS,width=110,sort_dicts=False)+'\n')
(HERE/'structure.py').write_text('"""Maintained chapter membership and presentation grouping."""\nREVISION="2026-10-22-linked-catalog"\nBASELINE="71a14e8ba76561d65345a696e6de3280b7c8dd00"\nCHAPTERS='+pformat(CHAPTERS,width=110,sort_dicts=False)+'\nDECK_CHAPTERS='+pformat(DECK_CHAPTERS,width=110,sort_dicts=False)+'\nTYPES='+pformat(TYPES,width=110,sort_dicts=False)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n')
fig=HERE/'diagrams.py';text=fig.read_text()
addition='''\nDIAGRAMS['workflow-feature-map']=(
'Outcome, workflow, mechanism, and feature relationships',
'An authored documentation model: each workflow step declares a dependency on a documented mechanism and concrete feature configuration. Reverse links support impact review. This is not an AWS runtime design.',
['A-09'],r"""
rankdir=TB;
outcome [label="Operational objective\\nActor and completion criteria"];
variant [label="Variant\\nScope, trigger, network, format"];
step [label="Workflow step\\nPurpose and responsible actor"];
mechanism [label="Documented mechanism\\nTrigger, state, process, effect"];
feature [label="Platform feature\\nResources and supported operations"];
recipe [label="Implementation profile\\nValues, permissions, checks, failure handling"];
evidence [label="Verification evidence\\nObservable result and limitations"];
outcome -> step [label="is carried out through"];
variant -> step [label="conditions a dependency"];
step -> mechanism [label="requires / optionally uses"];
mechanism -> feature [label="implemented with"];
recipe -> feature [label="configures"];
recipe -> step [label="binds to environment"];
step -> evidence [label="accepted using"];
""")\n'''
marker="if __name__=='__main__':"
if marker in text:text=text.replace(marker,addition+'\n'+marker)
else:text+=addition
compile(text,str(fig),'exec');fig.write_text(text)

review=ROOT/'qa/source-review.json';data=json.loads(review.read_text())
data['catalog_consolidation']={'date':'2026-10-22','scope':'Classification, relationships and implementation recipes. No exhaustive re-audit of retained guide prose.','rechecked_urls':['https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html','https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html','https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html','https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html','https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html','https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html','https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html'],'qualification':'Retrieved DevOps overview/creation versions do not enumerate every attachment detail retained in the existing guide. No absence was interpreted as removal. CronSchedule and Security revalidation could not be newly fetched; their existing references remain qualified rather than marked freshly verified.','live_execution':False}
review.write_text(json.dumps(data,indent=2)+'\n')
(ROOT/'qa/content-review.json').write_text(json.dumps({'revision':'2026-10-22-linked-catalog','primary_cases':30,'former_records_mapped':54,'retained_distinctions':['planning versus execution','assessment versus revalidation','pattern identification versus prioritization','recommendation versus measured outcome','forecast versus commitment coverage'],'changes':['Outcome narratives normalized without retaining superseded records','Workflow dependencies declare purpose, actor, condition, feature configuration, effect, verification and failure handling','Canonical guide explanations linked through searchable mechanism/feature/profile indexes','Reverse impact links distinguish direct and profile-selected dependencies','Shared review has distinct reliability and cost-management profiles'],'boundary':'Classification and proposed operational recipes; not live execution or a full upstream source audit.'},indent=2)+'\n')
(ROOT/'CHANGELOG.md').write_text('# Documentation changes\n\n## 22 October 2026 — linked outcome catalog\n\nConsolidated 54 former records into 30 primary outcomes, preserving variants and 13 supporting-reference mappings. Split forecasting from commitment coverage. Added mechanism, feature and implementation-profile indexes with forward and reverse dependency links. Updated the guides and HTML presentations. Old identifiers resolve to their successors; Git retains previous prose. No archive or binary presentation was produced.\n')

# These files are migration inputs, not a retained parallel catalog.
for name in ('case-plan-devops.json','case-plan-security-finops.json'):(ROOT/'catalog'/name).unlink()
Path(__file__).unlink()
print('Consolidated 30 outcomes and mapped all 54 former identifiers.')
