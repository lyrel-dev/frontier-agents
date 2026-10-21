#!/usr/bin/env python3
"""One-time scope reduction; removed after execution. Git retains prior revisions."""
from pathlib import Path
import collections, json, re, shutil, sys
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
KEYS = ['devops','security','finops','architecture']
PRODUCTS = KEYS[:3]
REV = '2026-10-21-three-agent-scope'
BAD = re.compile(r'kiro|amazon[\s_-]*q|amazonq|q[\s_-]*developer|qdeveloper',re.I)

def read(p): return json.loads((ROOT/p).read_text())
def write(p,x):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n' if not isinstance(x,str) else x)
def edit(p,fn):
    q=ROOT/p;q.write_text(fn(q.read_text()))
def delete(p):
    q=ROOT/p
    if q.is_dir():shutil.rmtree(q)
    elif q.exists():q.unlink()
def strings(x,fn):
    if isinstance(x,str):return fn(x)
    if isinstance(x,list):return [strings(v,fn) for v in x]
    if isinstance(x,dict):return {k:strings(v,fn) for k,v in x.items() if not BAD.search(k)}
    return x
def three(s):
    for a,b in [('four products','three products'),('four agents','three agents'),('four-agent','three-agent'),('all four products','all three products'),('4 agents','3 agents'),('all five reports','all four reports'),('AWS/Kiro','AWS'),('AWS and Kiro','AWS'),('AWS or Kiro','AWS')]:s=s.replace(a,b)
    return s
def prune_refs(x,removed,caps=None):
    if isinstance(x,dict):
        for k,v in list(x.items()):
            if k=='refs' and isinstance(v,list):x[k]=[a for a in v if a not in removed]
            elif k=='caps' and caps is not None:x[k]=[a for a in v if a in caps]
            else:prune_refs(v,removed,caps)
    elif isinstance(x,list):
        for v in x:prune_refs(v,removed,caps)
def source_bad(s):return bool(BAD.search(json.dumps(s))) or 'code-review-ide-integration' in str(s.get('url','')) or '/ai/frontier-agents/' in str(s.get('url',''))

for p in ['kiro','archive','dist','tools/migrations','.github/workflows/editorial-import.yml','content/mechanisms-import.json','mechanisms/PUBLICATION_RECEIPT.md','mechanisms/CONTINUATION_VALIDATION.md','qa']:
    delete(p)
for p in list(ROOT.rglob('*')):
    if p.is_file() and 'kiro' in p.name.lower():p.unlink()
(ROOT/'qa').mkdir(exist_ok=True)

allowed_caps={};evidences={}
for key in KEYS:
    old=read(f'content/{key}-evidence.json')
    field='patterns' if key=='architecture' else 'capabilities'
    items=old[field]
    if key=='devops':items=[c for c in items if c.get('product')=='AWS DevOps Agent']
    if key=='security':items=[c for c in items if c['id']!='C16']
    for c in items:
        c.pop('original',None)
        if 'implementations' in c:
            c['implementations']=[i for i in c['implementations'] if not BAD.search(i.get('agent',''))]
            if c['id']=='P07':
                sec=next(i for i in c['implementations'] if i['agent']=='Security')
                sec.update(text='The service documents scoped penetration testing from CI/CD with explicit task settings and result handling. This workflow retains its preview status.',refs=['S10','S11'],status='Preview · CI/CD integration')
        if isinstance(c.get('origin'),dict):
            c['origin'].pop('Kiro',None)
            if 'Security' in c['origin']:c['origin']['Security']=c['origin']['Security'].replace('C16, ','')
    sources=[s for s in old['sources'] if not source_bad(s)]
    removed={s['id'] for s in old['sources']}-{s['id'] for s in sources}
    items=strings(items,three);prune_refs(items,removed)
    d={k:old[k] for k in ['title','slug','date','validated','synthesis_boundary'] if k in old}
    d['scope']='Day-to-day '+('shared operating patterns for AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent.' if key=='architecture' else {'devops':'operations with AWS DevOps Agent.','security':'application-security workflows with AWS Security Agent.','finops':'cost-engineering workflows with AWS FinOps Agent.'}[key])
    d.update({field:items,'sources':sources,'scope_revision':REV})
    d['pilot']=old.get('pilot',[])
    if key=='devops':
        d['pilot'][0]['description']='Choose one service, owned accounts and named operators. Record a historical incident baseline and check Region, evidence coverage and least-privilege read access.'
        d['pilot'][1].update(title='Incident investigation',description='Compare a bounded investigation against known telemetry and deployment events. Record rejected hypotheses, missing sources and reviewer effort; do not enable writes for this exercise.')
    if key=='architecture':d['controls']=[c for c in old['controls'] if not BAD.search(c['path'])]
    d=strings(d,three);prune_refs(d,removed)
    if key!='architecture':d['counts']=dict(collections.Counter(c.get('verdict','Qualified') for c in items))
    allowed_caps[key]={c['id'] for c in items};evidences[key]=d
    write(f'content/{key}-evidence.json',d)

for key in KEYS:
    n=read(f'content/narratives/{key}.json')
    if key=='devops':
        n['stages'][5].update(title='Hand off an operational work item and verify closure',caps=['C01','C02','C04'],paragraphs=[
          'The proposed team handoff turns an accepted investigation into an owned engineering work item. Include the incident window, affected service and revision, evidence references, remaining uncertainty and the required recovery check. Preparing a code or configuration change is a responsibility of the receiving engineering team; it is not an additional DevOps Agent capability claimed here.',
          'Use the existing review and delivery process for any change. The service owner checks current telemetry after deployment, records whether the symptom recovered and reopens the investigation when the evidence does not support closure. A generated recommendation alone is not a completed incident.'])
        n['related']='Use the Security Agent report for an authorized assessment, the FinOps Agent report for cost analysis, and the architecture report for a reviewed handoff contract.'
    elif key=='security':
        n['stages'][5]['paragraphs'][1]=n['stages'][5]['paragraphs'][1].replace('IDE, S3 differential-scan and CI/CD','S3 differential-scan and CI/CD')
        n['related']='Use the DevOps Agent report for operational investigation and the architecture report to retain finding provenance without transferring assessment authority.'
    elif key=='architecture':
        n['stages'][0]['paragraphs'][0]='Start with the evidence and outcome required. DevOps Agent supports operational investigations, Security Agent supports authorized application assessments, and FinOps Agent supports cost analysis. Select only the specialist needed for the task. Code implementation, merge and deployment remain assigned engineering responsibilities rather than an additional agent role in this collection.'
    n['number']=f'{KEYS.index(key)+1:02}'
    n=strings(n,three);prune_refs(n,set(),allowed_caps[key]);write(f'content/narratives/{key}.json',n)

def matrix(title,takeaway,rows,refs,caps,notes):
    return dict(title=title,takeaway=takeaway,kind='matrix',seconds=90,phase='Operational handoff',refs=refs,caps=caps,notes=notes,headers=['Operational record','Receiving team action','Independent acceptance'],rows=rows)
for key in KEYS:
    d=read(f'content/{key}-presentation.json')
    if key=='devops':
        d['slides'][13]=matrix('Translate investigation findings into owned work','A proposed engineering handoff does not transfer production authorization.',[
          ['Incident evidence','Record resource, revision, UTC window and missing signals','A reviewer can locate and challenge the source evidence'],
          ['Mitigation candidate','Choose a safe change and document rollback assumptions','Change owner authorizes the exact effect'],
          ['Prevention recommendation','Create a scoped work item with a named owner','Closure requires a test or other independent evidence']],['D03','D04','D13'],['C01','C02','C04'],
          'This is a proposed team procedure using the documented investigation, mitigation and prevention outputs. It is not a native implementation or deployment feature. The receiving engineers decide whether a change is justified and use their existing repository, test and release controls. Preserve the distinction between an observed symptom, a hypothesis, a recommended action and a verified result.')
        d['slides'][14]=matrix('Verify recovery before closing the incident','Completion is a service-owner decision supported by current telemetry.',[
          ['Accepted change','Use normal review and delivery controls','The reviewed revision is the one actually deployed'],
          ['Recovery record','Compare the original symptom with post-change telemetry','Errors, latency and relevant business checks are independently reviewed'],
          ['Follow-up work','Assign unresolved risks and prevention tasks','Do not mark untested recommendations as completed']],['D03','D04','D05'],['C01','C03','C04'],
          'Retain a small closure record with the deployed revision, verification window, observed result and owner. These are proposed team acceptance criteria, not guaranteed product-generated fields. When evidence is missing or the symptom persists, keep the incident open and continue the investigation. The walkthrough does not demonstrate an automated code-change workflow.')
        d['slides'][17]['notes']=d['slides'][17]['notes'].replace('every original capability','every retained capability')
    elif key=='security':
        s=d['slides'][14]
        s.update(title='Submit and verify a differential source review',takeaway='A build submission calls a service; retain the source revision and scan evidence.',refs=['S27'],caps=['C17'],notes='The documented S3 differential-review workflow uses uploaded source and diff context. Record the base and head revisions, approved bucket and role, scan identifier and returned findings. Review the source payload for secrets and unnecessary content before submission. A scan result is not itself authorization to merge or deploy; the promotion rule is a separately proposed team control.')
        s['left']={'title':'Prepare source context','body':'Prepare the supported source and diff artifacts; retain base and head revisions and check the payload before upload.','tag':'PREVIEW'}
        s['right']={'title':'Submit and inspect findings','body':'Use the documented S3/API workflow. Retain the scan result and determine which findings apply to the proposed change.','tag':'PREVIEW'}
        s['callout']='Acceptance: confirm the uploaded scope, analyzed revisions and finding disposition before applying a team-owned release rule.'
    elif key=='architecture':
        for s in d['slides']:
            if s['kind']=='matrix':s['rows']=[r for r in s['rows'] if not BAD.search(str(r[0]))]
            if 'items' in s:s['items']=[i for i in s['items'] if not BAD.search(i.get('tag',''))]
        d['slides'][0]['metrics'][2]=['3 agents','distinct execution boundaries']
        d['slides'][1]['notes']='DevOps Agent provides operational evidence, Security Agent provides application-security assessment evidence, and FinOps Agent provides cost-analysis evidence. Their permissions and output records remain distinct. A shared work-item format is a proposed team convention, not a shared execution runtime. The engineering team retains implementation, review, merge and deployment responsibilities.'
        d['slides'][3]['rows'][0][1]='DevOps evidence → team-owned change request'
        d['slides'][7]['notes']='Approval must match the actual effect. DevOps directed actions require explicit enablement and approval. Active application tests can change the target through real requests. FinOps collaboration writes have trigger-dependent approval rules. Code implementation and release remain team-owned responsibilities. Do not infer a prompt before every mutation.'
        d['slides'][9]['rows']=[['DevOps remote servers','Scoped client access to an Agent Space','Shared credentials across specialists'],['Security CI/CD integration','Submit scoped assessment work and inspect results','Blanket coverage or automatic release authority'],['FinOps Jira / Slack','Route outputs through configured destinations','General Jira administration or inbound Slack commands']]
        d['slides'][9]['refs']=['D37','D38','S28','F13','F14']
        d['slides'][14]['notes']='Record the exact feature, maturity, service Region, inference behavior and output destination. DevOps production operations and release preview have different availability. Security features have different maturity and source/target requirements. FinOps remains a separately qualified preview workflow. Review these boundaries for each use case rather than applying a portfolio-wide approval.'
        d['slides'][6]['left']['body']='Prompts, instructions, skills, memory and context explain the task and preferred procedure.'
        d['slides'][6]['notes']=d['slides'][6]['notes'].replace('Steering, skills','Instructions, skills')
        d['slides'][15]['steps'][2][1]='Inspect the team-owned change handoff'
    old=d['sources'];d['sources']={k:v for k,v in old.items() if not source_bad(v)}
    removed=set(old)-set(d['sources']);d=strings(d,three);prune_refs(d,removed,allowed_caps[key])
    d['scope_revision']=REV;write(f'content/{key}-presentation.json',d)

m=read('content/mechanisms.json');m['agents']={k:v for k,v in m['agents'].items() if k in PRODUCTS}
m['agents']['security']['records']=[r for r in m['agents']['security']['records'] if r['id']!='S-M07']
m['comparison']=[r for r in m['comparison'] if not BAD.search(r[0])]
m['evidence_notes']=[x for x in m['evidence_notes'] if not BAD.search(x) and 'CONTINUATION_VALIDATION' not in x]
m['evidence_notes'].append('Scope revision retains the existing official evidence for the three included agents. This revision does not constitute a fresh external source audit or a live AWS test.')
old=m['sources'];m['sources']={k:v for k,v in old.items() if not source_bad(v)};removed=set(old)-set(m['sources'])
prune_refs(m,removed)
for control in m['controls']:control[2]=[r for r in control[2] if r not in removed]
m=strings(m,three);m['revision']=REV;m['scope']='Documented mechanisms and enablement for AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent.'
write('content/mechanisms.json',m)

ann=read('content/format-annotations.json')
for field in ['capability_records','stage_owners']:ann[field]={k:v for k,v in ann[field].items() if k in KEYS}
for k in KEYS:ann['capability_records'][k]={c:v for c,v in ann['capability_records'][k].items() if c in allowed_caps[k]}
ann['revision']=REV;write('content/format-annotations.json',ann)
write('documentation-build.json',{'revision':REV,'scope':['AWS DevOps Agent','AWS Security Agent','AWS FinOps Agent'],'shared_architecture':True,'history_policy':'Git history only; no snapshot directories or committed ZIP distributions','live_aws_execution':False})
write('content/narratives.json',{'revision':REV,'scope':'Source-linked guidance for three AWS agents and their proposed shared operating patterns. No live execution or measured benefit is claimed.','agents':{k:read(f'content/narratives/{k}.json') for k in KEYS}})

write('tools/assemble_content.py','''#!/usr/bin/env python3
"""Validate and assemble the supported documentation source."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
KEYS=('devops','security','finops','architecture')
def main():
    agents={};checks=[]
    for key in KEYS:
        n=json.loads((ROOT/f'content/narratives/{key}.json').read_text())
        assert len(n['stages'])==6
        d=json.loads((ROOT/f'content/{key}-presentation.json').read_text())
        e=json.loads((ROOT/f'content/{key}-evidence.json').read_text())
        caps={x['id'] for x in e.get('capabilities',e.get('patterns',[]))}
        for s in d['slides']:
            assert s['notes'].strip()
            assert set(s.get('refs',[]))<=set(d['sources'])
            assert set(s.get('caps',[]))<=caps
            if s['kind']=='demo':assert sum(x[0] for x in s['steps'])==s['seconds']
        assert sum(x['seconds'] for x in d['slides'])==60*d['minutes']
        assert sum(x['seconds'] for x in d['slides'] if x['kind']=='demo')==60*d['demo']
        agents[key]=n;checks.append({'report':key,'slides':len(d['slides']),'minutes':d['minutes'],'demo_minutes':d['demo'],'source_references_valid':True})
    revision=json.loads((ROOT/'documentation-build.json').read_text())['revision']
    (ROOT/'content/narratives.json').write_text(json.dumps({'revision':revision,'scope':'Three AWS agents and proposed shared operating patterns; no live execution or measured benefit.','agents':agents},ensure_ascii=False,indent=2)+'\\n')
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-validation.json').write_text(json.dumps({'revision':revision,'checks':checks,'boundary':'Structural and timing validation, not live product testing.'},indent=2)+'\\n')
if __name__=='__main__':main()
''')

def tool_keys(t):
    t=t.replace("'kiro', ",'').replace("'kiro',",'')
    t=re.sub(r"'kiro'\s*:\s*(?:'[^']*'|\d+)\s*,?",'',t)
    t=t.replace("        if key == 'kiro' and re.search(r'Web|cloud|sandbox', availability, re.I):\n            availability += ' · Verify surface-specific support'\n",'')
    t=t.replace("'kiro/report.html',", "")
    return t
for p in ['tools/build_suite.py','tools/editorial_lint.py','tools/qa_format.py','tools/qa_mechanisms_browser.py']:
    edit(p,tool_keys)

substitutions={
 'all five sessions':'all four sessions','all five presentation':'all four presentation','All five interactive':'All four interactive','Five engineering reports':'Three agent reports and their shared architecture',
 'five editable PowerPoint decks':'four editable PowerPoint decks','five detailed narrative reports':'four detailed narrative reports','160 minutes':'128 minutes','48 minutes':'35 minutes','88 core slides':'70 core slides','88 timed':'70 timed','83 capability-reference':'50 capability-reference','83 untimed':'50 untimed','83 appendix':'50 appendix',
 '35, 32, 30, 27 and 36':'35, 30, 27 and 36',
 'AWS/Kiro':'AWS','AWS and Kiro':'AWS','2026-10-21-editorial-v2':REV,'5 field guides':'4 field guides','71 capabilities + 12 patterns':'38 capabilities + 12 patterns','83 reference slides':'50 reference slides','160 min including':'128 min including',
 'retained original capability audits, unchanged':'scope-filtered capability evidence records',
 'Original capability audits are retained as 20 October 2026 snapshots.':'The retained capability evidence originates in the earlier documentation review and has been filtered to the current scope.',
 'Preserved the capability audits and original HTML reports.':'Retained the in-scope capability evidence. Earlier editions remain in Git history.',
 'Historical audits, code revisions and unrelated files remain intact.':'Earlier document revisions remain in Git history.',
 '- `archive/2026-10-20/`: original HTML reports preserved for provenance.\\n':'',
 'Historical evidence is retained; recommendations and':'Source evidence is retained; recommendations and',
}
def suite_edit(t):
    for a,b in substitutions.items():t=t.replace(a,b)
    t=t.replace(', zipfile','')
    t=t.replace('Revision 2: Standardized factual capability records', 'Current three-agent revision: Standardized factual capability records')
    t=t.replace('all 50 appendix records','all 50 capability/pattern reference records')
    t=t.replace("    put(f'archive/2026-10-20/{PATHS[key]}', source.read_bytes())\n",'')
    a=t.index("    initial=ROOT/'devops/initial-report.html'");b=t.index('    from build_presentations import build_deck',a)
    t=t[:a]+"    put('devops/initial-report.html','<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta http-equiv=\"refresh\" content=\"0; url=validated-report.html\"><title>Current DevOps Agent report</title></head><body><p><a href=\"validated-report.html\">Open the current DevOps Agent report.</a></p></body></html>')\n"+t[b:]
    t=t.replace('<a class="button" href="https://github.com/lyrel-dev/frontier-agents/blob/main/dist/frontier-agents-document-suite.zip">Document package in GitHub (sign-in may be required)</a>','<a class="button" href="https://github.com/lyrel-dev/frontier-agents">Repository and Git history</a>')
    t=t.replace("    (ROOT/'dist').mkdir(exist_ok=True);(ROOT/'dist/frontier-agents-document-suite.zip').touch(exist_ok=True)\n",'')
    t=t.replace(" and not rel.startswith('dist/')",'')
    t=t.replace("'dist/ convenience archives',",'')
    a=t.index("    target=ROOT/'dist/frontier-agents-document-suite.zip'");b=t.index('\ndef commit_files()',a)
    t=t[:a]+"    print(json.dumps({'generated':len(set(GENERATED)),'structural_checks':result},indent=2))\n"+t[b:]
    t=t.replace("git('add','--',path)","git('add','-A','--',path)")
    t=t.replace("'timing_checks':'all four sessions and demo allocations'","'timing_checks':'four sessions; three agents and shared architecture'")
    return t
edit('tools/build_suite.py',suite_edit)

def mechanisms_edit(t):
    for a,b in [('Across the four products','Across the three products'),('existing five presentations','four retained presentations'),('48 minutes of demonstrations','35 minutes of demonstrations'),('32 mechanism records across four platforms','23 mechanism records across three platforms'),('Four platform guides contain 32','Three platform guides contain 23'),('Five additional reference decks','Four additional reference decks'),('Five reference PowerPoints','Four reference PowerPoints'),('Four optional exercises add 44','Three optional exercises add 34'),('total 44 minutes','total 34 minutes'),('add 44 minutes','add 34 minutes'),('160 minutes','128 minutes'),('160-minute','128-minute'),('48 demo minutes','35 demo minutes'),("'core_minutes_unchanged':160","'core_minutes':128"),("'core_demo_minutes_unchanged':48","'core_demo_minutes':35"),('32 mechanism records, four platform setup guides','23 mechanism records, three platform setup guides'),('five untimed reference decks','four untimed reference decks')]:t=t.replace(a,b)
    t=t.replace('Source register: 46 official AWS/Kiro pages. Original 44-source mechanism review dated 21 October 2026; this follow-up adds two references and rechecks selected critical mechanisms, not every historical claim.','Source register: retained official AWS references for the three included platforms. The scope revision does not claim a fresh external audit of the retained documentation.')
    a=t.index("    put('PUBLISHING.md',");b=t.index('\n\n    for rel,extra',a)
    text='# Publishing and rebuilding\\n\\nOnly current source and generated documents are tracked. Git history is the version record. Do not create snapshot directories, compressed import payloads, or committed distribution ZIP files. Clone the repository and open index.html locally. Repository publication is not a Pages deployment.\\n\\n```sh\\npython tools/assemble_content.py\\npython tools/build_suite.py\\npython tools/build_suite.py --check\\npython tools/editorial_lint.py\\npython tools/validate_scope.py\\n```\\n\\nUpdate documentation-build.json to request publication. Changed documents and deletions are committed individually. Repository visibility is unchanged.\\n'
    t=t[:a]+"    put('PUBLISHING.md','"+text+"')"+t[b:]
    return t
edit('tools/build_mechanisms.py',mechanisms_edit)
edit('tools/editorial_lint.py',lambda t:t.replace('2026-10-21-editorial-v2',REV))
edit('tools/qa_format.py',lambda t:t.replace('assert n in (19,21,18,13,12)','assert n in (8,17,13,12)'))
for p in ['tools/qa_format.py','tools/qa_mechanisms_browser.py']:
    edit(p,lambda t:'import shutil, tempfile\n'+t.replace("executable_path='/usr/bin/chromium'","executable_path=shutil.which('chromium')").replace("qa=root/'qa'/'editorial_screens'","qa=Path(tempfile.gettempdir())/'frontier-editorial-checks'").replace("Q=ROOT/'qa/mechanism-screens'","Q=Path(tempfile.gettempdir())/'frontier-mechanism-checks'"))
edit('EDITORIAL_STANDARD.md',lambda t:three(t.replace('AWS DevOps Agent, Kiro, AWS Security Agent','AWS DevOps Agent, AWS Security Agent').replace('Kiro **32m / 13m**; ','').replace('160m / 48m','128m / 35m')))

for key in PRODUCTS:
    d=evidences[key];sources={s['id']:s for s in d['sources']}
    lines=[f'# {d["title"]} — capability evidence record',f'Scope revision: {REV}. This is a filtered record of the previously reviewed official evidence, not a new external documentation audit. Earlier editions are available through Git history.','## Current capability records']
    for c in d['capabilities']:
        lines += [f'## {c["id"]} · {c["title"]}',f'**Documented function:** {c["claim"]}',f'**Availability:** {c.get("availability","")}',f'**Prerequisites:** {c.get("setup","")}',f'**Limitations:** {c.get("limit","")}',f'**Proposed verification:** {c.get("check","")}']
        for ref in c.get('refs',[]):
            s=sources[ref];lines.append(f'- [{ref} · {s["title"]}]({s["url"]})')
    lines += ['## Boundary','No live AWS account, workflow, penetration test or cost action was exercised in this scope revision.']
    write(f'{key}/validation-record.md','\n\n'.join(lines)+'\n')

write('SCOPE.md','# Supported scope\n\nThis repository covers AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent. Shared architecture material applies only to these three solutions. Implementation, merge and deployment handoffs are explicitly team-owned unless a retained product-specific capability says otherwise.\n\nGit history is the version record. Do not retain snapshot directories, import payloads, distribution ZIPs or copied historical editions in the current tree. Current HTML, Markdown, source JSON and editable PowerPoint files are rebuilt from the retained source.\n\nProduct evidence is retained from the prior official-documentation review. This scope change is not a fresh external audit or live AWS test.\n')
for p in (ROOT/'content').rglob('*.json'):
    if BAD.search(p.read_text()):raise ValueError('Unresolved excluded content in '+str(p.relative_to(ROOT)))
for p in (ROOT/'tools').glob('*.py'):
    if p.name not in ['apply_scope.py','validate_scope.py'] and BAD.search(p.read_text()):raise ValueError('Unresolved excluded tool content '+p.name)
if Path(__file__).resolve()==(ROOT/'tools/apply_scope.py').resolve():Path(__file__).unlink()
print('Scope data and build tooling updated; next assemble, rebuild and validate.')
