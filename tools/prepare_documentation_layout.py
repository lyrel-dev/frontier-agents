#!/usr/bin/env python3
"""One-time repository restructuring. Git retains every removed revision."""
from pathlib import Path
import json, re, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lesson_plan import DECKS
from docs_structure import CHAPTERS,TYPES,LABELS,section_type
sys.path.insert(0,str(ROOT/'tools/docs'))
from diagrams import DIAGRAMS


def title_case(text):
    text=text[0].upper()+text[1:].lower() if text else text
    names={'aws':'AWS','mcp':'MCP','iam':'IAM','api':'API','apis':'APIs','sop':'SOP','sops':'SOPs','ci/cd':'CI/CD','utc':'UTC','s3':'S3','eks':'EKS','jira':'Jira','slack':'Slack','finops':'FinOps','devops':'DevOps','cloudtrail':'CloudTrail','eventbridge':'EventBridge','kms':'KMS'}
    for old,new in names.items():text=re.sub(r'(?<!\w)'+re.escape(old)+r'(?!\w)',new,text,flags=re.I)
    return text

DIAGRAM_ORDER={
'devops':['devops-architecture','devops-integrations','devops-memory','devops-incident','devops-reporting'],
'security':['security-architecture','security-integrations','security-context','security-authentication','security-revalidation'],
'finops':['finops-architecture','finops-integrations','finops-context','finops-automation'],
'architecture':['agent-execution','shared-handoff']}

NEW_TABLES={
'devops':{'title':'Telemetry, source control, and incident connections','seconds':120,'refs':['D-12'],'kind':'table','message':'Choose the evidence source, incident-initiation path, and result destination independently. Registration and Agent Space association are separate setup steps.','data':[
['Connection family','Documented systems','Purpose and boundary'],
['AWS evidence','CloudWatch, S3, EKS; selected AWS accounts','Read authorized telemetry, objects, and cluster evidence; EKS has additional access setup.'],
['Telemetry providers','Dynatrace; Datadog, Grafana, New Relic, Splunk','Dynatrace has a documented two-way path; other named providers expose reads and separately configured event initiation.'],
['Code and delivery','GitHub, GitLab; Azure Resources and Azure DevOps','Repository, pipeline, or infrastructure context according to the configured provider and resource scope.'],
['Incident coordination','ServiceNow, PagerDuty, Slack','Provider-specific initiation and communication; not a universal write capability.'],
['Additional interfaces','MCP, webhooks, EventBridge','Selected tools, incoming incident signals, and outgoing lifecycle events are different directions.']]},
'security':{'title':'Repository, documentation, and Jira connections','seconds':120,'refs':['S-09'],'kind':'table','message':'Account-level registration authorizes a provider; application-level selection supplies resources. Repository writes and Jira effects require their own settings.','data':[
['Provider family','Documented support','Selection or effect'],
['GitHub','Cloud-hosted GitHub and Enterprise; self-hosted Enterprise Server','Select application repositories; private servers may require private connectivity.'],
['GitLab and Bitbucket','GitLab cloud and Self-Managed; Bitbucket Cloud','Provider-specific repository context and eligible review/remediation settings.'],
['Documentation','Confluence Cloud','Selected pages provide read-only application context.'],
['AWS objects','Same-account S3 resources','Select relevant sources; code-review archives have their own format requirements.'],
['Work tracking','Jira Cloud','Select projects and independently permit issue creation or comments.']]},
'finops':{'title':'Cost-data and publication connections','seconds':120,'refs':['F-08'],'kind':'table','message':'Data-role permissions control AWS evidence retrieval. Provider registration and agent connections control the available collaboration destinations.','data':[
['Source or destination','Information supplied','Interpretation'],
['Cost Explorer','Cost and usage results, forecasts, coverage','Preserve dates, metric, account scope, and grouping.'],
['Cost Anomaly Detection','Deviation and supported event source','A trigger for investigation, not proof of cause.'],
['Cost Optimization Hub / Compute Optimizer','Upstream recommendation and estimate','Review assumptions; estimate is not realized saving.'],
['CloudTrail','Recorded operational changes','Temporal association requires additional causal evidence.'],
['Jira Cloud / Slack','Supported publication actions','Destination and invocation type determine the approval behavior.']]}}

GROUP_NAMES=['Service architecture','Integrations and access','Knowledge and behavior','Execution workflows','Operational use cases','Worked example','Troubleshooting and references']

def assign(key,slide):
    refs=set(slide['refs']);title=slide['title'].lower()
    if slide['kind']=='demo':return 'Worked example'
    if 'troubleshoot' in title or 'operating limits' in title or refs.intersection({'D-10','D-11','S-07','S-08','F-06','F-07','A-07'}):return 'Troubleshooting and references'
    if any(word in title for word in ('use case','use-case','operational reporting','knowledge and documentation use','operational review')):return 'Operational use cases'
    if refs.intersection({'A-00','D-01','S-01','F-01','A-01'}):return 'Service architecture'
    if refs.intersection({'D-02','D-03','D-04','D-12','S-02','S-03','S-09','F-02','F-05','F-08','A-03','A-08'}):return 'Integrations and access'
    if refs.intersection({'D-05','D-M01','D-M02','D-M03','D-M04','D-M07','S-M02','S-M03','S-M04','S-M07','F-M02','F-M03','F-M04','A-02'}):return 'Knowledge and behavior'
    return 'Execution workflows'


def apply():
    dest=ROOT/'tools/docs';dest.mkdir(exist_ok=True)
    chapters={}
    for key,deck in DECKS.items():
        old=deck['slides']
        for s in old:
            s['title']=title_case(s['title'])
            # A minute-resolution analysis does not promise exact-minute delivery.
            s['data']=[[str(x).replace('Minute-by-minute incident status report','Incident status bulletin').replace('minute-by-minute incident status','timestamped incident status').replace('Every five minutes','On demand for the previous five complete minutes') for x in row] for row in s['data']]
            if 'minute' in json.dumps(s).lower() and key=='devops':
                s['message']+=' Scheduled custom work has a flexible start window of up to 30 minutes; telemetry resolution and report delivery are different.'
        additions=[]
        for diagram in DIAGRAM_ORDER[key]:
            title,description,refs,_=DIAGRAMS[diagram]
            additions.append({'title':title,'seconds':120,'refs':refs,'kind':'diagram','diagram':diagram,'data':[],'message':description})
        if key in NEW_TABLES:additions.append(NEW_TABLES[key])
        buckets={name:[] for name in GROUP_NAMES}
        for s in additions+old:buckets[assign(key,s)].append(s)
        result=[];groups=[]
        for name,slides in buckets.items():
            if not slides:continue
            start=len(result);result.extend(slides);groups.append((name,list(range(start,len(result)))))
        deck['slides']=result;deck['subtitle']='Architecture, integrations, knowledge, and operational workflows'
        chapters[key]=groups
    (dest/'presentation.py').write_text('"""Maintained HTML presentation outline and delivery budgets."""\nDECKS = '+repr(DECKS)+'\n')
    (dest/'structure.py').write_text('"""Maintained chapter membership and section types."""\nREVISION="2026-10-22-narrative-guides"\nBASELINE="c3d6f2dafdd87e083989135690e2f4f169e80fc2"\nCHAPTERS='+repr(CHAPTERS)+'\nDECK_CHAPTERS='+repr(chapters)+'\nTYPES='+repr(TYPES)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n')
    shutil.copyfile(ROOT/'tools/docs-requirements.txt',dest/'requirements.txt')
    # Correct table formatting in generated coverage and use landscape printing for decks.
    build=dest/'build.py';text=build.read_text()
    text=text.replace("write('guides/coverage.md','\\n\\n'.join(coverage))","write('guides/coverage.md','\\n'.join(coverage))")
    text=text.replace("css=(SOURCE/'styles.css').read_text();js=", "css=(SOURCE/'styles.css').read_text();css+=('\\n@media print{@page{size:A4 landscape;margin:12mm}}' if view=='presentation' else '');js=")
    build.write_text(text)
    removed=[]
    for folder in ['devops','security','finops','architecture','mechanisms','platforms']:
        path=ROOT/folder
        if path.exists():
            removed.extend(p.relative_to(ROOT).as_posix() for p in path.rglob('*') if p.is_file());shutil.rmtree(path)
    for name in ['docs_build.py','docs_check.py','docs_structure.py','lesson_plan.py','use_case_catalog.py','docs_styles.css','docs_interactions.js','docs-requirements.txt']:
        path=ROOT/'tools'/name
        if path.exists():removed.append(path.relative_to(ROOT).as_posix());path.unlink()
    for path in (ROOT/'qa').glob('*'):
        if path.is_file() and path.name!='source-review.json':removed.append(path.relative_to(ROOT).as_posix());path.unlink()
    review={'revision':'2026-10-22-narrative-guides','removed_superseded_paths':sorted(removed),'maintained_source_layout':['guides/*.md','catalog/use-cases.json','tools/docs/structure.py','tools/docs/presentation.py','tools/docs/diagrams.py'],'content_changes':['Agent and execution model introduced before configuration.','Named integration providers distinguished by direction and scope.','Knowledge production, retrieval, correction, and restoration boundaries separated.','All catalog workflows receive authored multi-paragraph narratives.','Logical SVG architecture and workflow diagrams replace ASCII sketches.','Technical guide sections and known source references remain cross-linked.'],'boundary':'Content revision and source-linked logical models, not live service verification.'}
    (ROOT/'qa/content-review.json').write_text(json.dumps(review,indent=2)+'\n')
    Path(__file__).unlink()
if __name__=='__main__':apply()
