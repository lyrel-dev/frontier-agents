"""One-time integration of reviewed prose into the maintained mechanism registry.

Only the mechanism register and its temporary source-input files are changed.
Use cases, feature definitions, profiles, aliases and resource models stay intact.
"""
from pathlib import Path
import importlib
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
modules=[importlib.import_module('stage3_'+p) for p in ('devops','security','finops')]
details={}
sources={}
for module in modules:
    details.update(module.DETAILS)
    for ident,(url,scope) in module.SOURCES.items():
        sources[ident]={'url':url,'scope':scope,'reviewed_on':'2026-10-22'}
path=ROOT/'catalog/mechanisms.json'
data=json.loads(path.read_text())
assert len(data['entries'])==40 and len(details)==41
new={
 'id':'MX-S-PERSONALIZE','platform':'security','title':'Finding-edit personalization',
 'features':['FT-S-FINDINGS'],'sections':['S-05'],
 'trigger':'Eligible edits from the most recent completed test when personalization was enabled at test start',
 'state':'Retained finding preferences and original/latest finding attributes',
 'process':'Apply eligible learned preferences to similar findings in subsequent penetration-test runs.',
 'effect':'Finding-attribute personalization, not application remediation',
 'verification':'Inspect original/latest values and the Personalization changes explanation separately from vulnerability evidence.',
 'on_failure':'Treat unobserved personalization as unverified; a severity change does not establish a repaired application.'}
data['entries'].append(new)
for entry in data['entries']:
    entry['review']=details[entry['id']]
next(e for e in data['entries'] if e['id']=='MX-S-FINDING')['related_mechanisms']=[{
 'id':'MX-S-PERSONALIZE','dependency':'conditional',
 'condition':'Findings Personalization was enabled at test start and eligible edits are available; it changes finding attributes, not application state.'}]
figures={
 'MX-D-RECALL':'mechanism-devops-retrieval',
 'MX-D-CUSTOM':'mechanism-devops-cancellation',
 'MX-S-LOGIN':'mechanism-security-learning',
 'MX-S-REVALIDATE':'mechanism-security-replay',
 'MX-F-FILES':'mechanism-finops-context',
 'MX-F-EVENT':'mechanism-finops-publication'}
for entry in data['entries']:
    if entry['id'] in figures:entry['review']['diagram']=figures[entry['id']]
data['review_sources']=sources
data['reviewed_on']='2026-10-22'
data['review_boundary']='Detailed mechanism prose is maintained here and rendered into delimited guide sections. Tests and failure decisions are proposed engineering guidance, not live results.'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for name in ('stage3_devops.py','stage3_security.py','stage3_finops.py'):
    (HERE/name).unlink()
print(json.dumps({'reviewed_mechanisms':len(data['entries']),'official_sources':len(sources),'use_cases_changed':False}))
Path(__file__).unlink()
