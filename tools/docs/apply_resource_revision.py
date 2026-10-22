#!/usr/bin/env python3
"""Finalize the source revision once; the maintained build needs no migration."""
from pathlib import Path
from pprint import pformat
import ast
import copy
import re
import build
from structure import CHAPTERS,DECK_CHAPTERS
from presentation import DECKS

ROOT=Path(__file__).resolve().parents[2]
guides=build.load_guides()
g=guides['architecture']
g['sections']['A-01']['title']='Resource identity across service boundaries'
g['sections']['A-01']['body']='''A useful cross-service record preserves the original identity instead of replacing every object with a generic agent ID. The configured workspace identifies the operating scope, the definition identifies reusable settings, and the execution identifies a particular result. An external source revision or observation period identifies what that result describes. These responsibilities are separate even when a user interface displays them together. [AS50] [AS51] [AS52]

For example, an incident handoff should distinguish the operational space from its investigation. A security handoff should retain the assessment and original finding, not just the application name. A cost report should retain its query basis and task or conversation context rather than claiming that the agent instance itself identifies the analysis. The following fields are an authored evidence convention, not an AWS API request schema.

| Identity component | Purpose | Interpretation |
|---|---|---|
| Product and scope | Identify the service, account/Region and relevant space or instance | Similar resource labels in different namespaces remain different objects |
| Configuration reference | Identify the selected definition or settings where applicable | A configuration can outlive and create several executions |
| Execution reference | Identify the investigation, run, review, job or task | Status describes this piece of work, not every subsequent action |
| Source identity | Preserve resource IDs, query basis, revision and observation window | The source system remains the authority for original observations |
| Result and review | Connect the output to the accepted interpretation and residual uncertainty | A completed execution does not establish outcome correctness |

Use native identifiers where documented and meaningful context otherwise. Do not invent an ARN or parent field for a derived view, a retained procedure or a normalized relationship. In particular, the FinOps instance has its own AgentSpace IAM naming within the finops-agent service; that naming does not make a DevOps policy or API interchangeable with it. [AS53]

A-11 provides the product responsibility crosswalk, while the resource register supplies the detailed entity and relationship dictionary. This section concerns how identities survive an engineering handoff, not a second definition of the product hierarchies. [AS50] [AS51]
'''
pieces=[g['intro'],'']
for number,c in enumerate(CHAPTERS['architecture'],1):
    pieces += [f'## {number:02d}. {c["title"]}',c['purpose'],'']
    for sid in c['sections']:
        sec=g['sections'][sid];pieces += [f'### {sid} — {sec["title"]}',sec['body'],'']
pieces += [f'[{sid}]: {url}' for sid,url in g['refs'].items()]
(ROOT/'guides/architecture.md').write_text('\n\n'.join(pieces).rstrip()+'\n')

rows={
'devops':[
 ['Object','Identity or membership','Relationship to inspect'],
 ['Agent Space','agentSpaceId and service scope','Account roles and selected associations'],
 ['Service association','associationId and serviceId','Registered provider plus space-specific configuration'],
 ['Custom definition','custom_agent assetId','Existing skill and memory-store asset IDs'],
 ['Memory','Parent store and content version','Activation, attachment and observed retrieval'],
 ['Invocation or investigation','Execution record and actual interval','Tool evidence, conclusion and any separate approval']
],
'security':[
 ['Object','Identity or membership','Lifecycle distinction'],
 ['Agent Space','Application or project scope','Shared integration registration is separate'],
 ['Penetration test','Saved configuration and independent run','Record current target revision and test identity'],
 ['Code review','Full-scan configuration or repository event settings','Keep the actual reviewed revision'],
 ['Design review','Individual assessment','Cloning creates a new review'],
 ['Finding and revalidation','Original finding plus separate job','Our normalized result association is not a native API resource']
],
'finops':[
 ['Object','Identity or membership','Lifecycle distinction'],
 ['Agent instance','finops-agent AgentSpace actions and agentspace ARN','Service-specific scope; not a DevOps resource'],
 ['Integration / connection','Account registration / instance destination binding','Authorization and destination selection differ'],
 ['Conversation / task','Interaction / separately recorded execution','A direct answer need not create a task'],
 ['Automation','Rule that creates future tasks','Deleting a rule does not delete existing work'],
 ['File / memory / artifact','Reference input / retained context / output','Each has its own update and removal behavior']
]}
for key in rows:
    old=DECKS[key]['slides'][1]
    DECKS[key]['slides'][1]=dict(title='Resource identities and lifecycle boundaries',seconds=old['seconds'],refs=[{'devops':'D-13','security':'S-10','finops':'F-09'}[key]],kind='table',data=rows[key],message='Identify the actual product object before configuring, invoking, correcting or removing it. The resource kind determines which operation is meaningful.')
(ROOT/'tools/docs/presentation.py').write_text('"""HTML lessons aligned with the canonical product resource models."""\nDECKS='+pformat(DECKS,width=105,sort_dicts=False)+'\n')

# Remove only genuinely unreferenced predecessor figures, not workflow illustrations.
path=ROOT/'tools/docs/diagrams.py';text=path.read_text();tree=ast.parse(text)
assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIAGRAMS' for t in n.targets))
base=ast.literal_eval(assignment.value)
raw_guides='\n'.join((ROOT/f'guides/{k}.md').read_text() for k in DECKS)
used_slides={sl.get('diagram') for deck in DECKS.values() for sl in deck['slides']}
for key in ('devops-architecture','security-architecture','finops-architecture'):
    if f'{key}.svg' not in raw_guides and key not in used_slides:
        base.pop(key,None)
        (ROOT/f'assets/diagrams/{key}.svg').unlink(missing_ok=True)
lines=text.splitlines()
text='\n'.join(lines[:assignment.lineno-1])+ '\nDIAGRAMS='+pformat(base,width=105,sort_dicts=False)+'\n'+'\n'.join(lines[assignment.end_lineno:])+'\n'
text=text.replace("if __name__=='__main__':print(build())",'')
text=text.rstrip()+"\n\nif __name__=='__main__':\n    print(build())\n"
path.write_text(text)

path=ROOT/'tools/docs/build.py';text=path.read_text()
text=text.replace('The comparison is intended','The comparison is intended')
text=text.replace('Resource ER diagrams qualify undocumented multiplicity and logical associations in their relationship register.</span></figcaption>', 'Resource ER diagrams qualify undocumented multiplicity and logical associations in their relationship register.</span> <a href="../assets/diagrams/{key}.svg" target="_blank" rel="noopener">Open full-size SVG</a></figcaption>')
text=text.replace('New integration and scheduling material and selected knowledge mechanisms were reviewed on 22 October 2026; retained sections keep their earlier references. See [the source-review record](../qa/source-review.json).','Product-specific resource identities and relationships were reviewed on 22 October 2026; retained sections keep their earlier references. See [the product-model source record](../qa/product-source-review.json) and [the earlier source-review record](../qa/source-review.json).')
path.write_text(text)
Path(__file__).unlink()
print('Consolidated model explanations, removed unreferenced predecessor figures and retained one maintained renderer.')
