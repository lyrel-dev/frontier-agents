"""One-time refinement of the authored capability exposition; no frozen record writes."""
from pathlib import Path
import json
import pprint
import re
import sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from structure import CHAPTERS,TYPES,LABELS
from presentation import DECKS

p=ROOT/'guides/devops.md';text=p.read_text()
old='Native test profiles store endpoint, test type, personas, API specification where applicable, and secret references. The supplied source outline identifies TOTP and email-based UI authentication support; consult the linked release-testing procedure for the selected profile type and current availability. The reviewed product guide\'s preview scope must not be expanded to all Regions or all assessment interfaces. [DS504] [DS61]'
new='Native test profiles store the target endpoint, test type, applicable personas and API specification, and credential configuration. TOTP authentication is supported for UI and API profiles; email-based 2FA applies to UI profiles only. The email option supplies a profile-specific forwarding address and an optional sender filter. Release testing sends real application requests, including writes, so its target and credentials must be suitable for the intended test effects. [DS516]'
if old not in text:raise ValueError('Missing release-profile paragraph')
text=text.replace(old,new)
text += '\n[DS516]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html\n'
# Remove stale constraints retained from the schedule-only overview; replace only precise affected statements.
text=text.replace('Custom agents are schedule-only.', 'The execution guide documents on-demand, scheduled, and webhook-event invocation; see D-07 and D-18.')
p.write_text(text)

# The frozen register remains unchanged. Editorial routing locates the relevant authored explanation.
p=HERE/'reader.py';text=p.read_text()
old="                mechanisms = [m for m in self.mechanisms.values() if m['platform']==product and m['review']['primary_section']==sid]"
new="                explanation_sections = {'MX-D-QUERY':'D-21','MX-D-CUSTOM':'D-19','MX-S-PERSONALIZE':'S-13'}\n                mechanisms = [m for m in self.mechanisms.values() if m['platform']==product and explanation_sections.get(m['id'],m['review']['primary_section'])==sid]"
if old not in text:raise ValueError('Reader explanation selection not found')
text=text.replace(old,new)
p.write_text(text)

# Reassociate existing slides with the actual topic they teach instead of a former catch-all section.
for product,d in DECKS.items():
    for s in d['slides']:
        if product=='devops':
            if s['title']=='Release readiness review and release testing':s['refs']=['D-22']
            if s['title']=='Stopping future triggers and current invocations':s['refs']=['D-19','D-07']
            if s['title']=='Configured operational-report workflow':s['refs']=['D-14','D-16','D-07']
        if product=='security' and s['title']=='Authentication reuse and finding personalization':s['refs']=['S-M02','S-13']
        if product=='architecture' and s['title']=='Operational objectives, mechanisms and features':s['refs']=['A-12','A-09']

def table(title,refs,rows,message,seconds=120):
    return {'title':title,'refs':refs,'kind':'table','data':rows,'message':message,'seconds':seconds}

DECKS['security']['slides'].extend([
 table('Private source access and application-target connectivity',['S-15'],[['Path','Purpose','Separate prerequisite'],['Repository connection','Read source code and revision context','Provider authorization and source selection'],['Private application route','Reach the test endpoint','VPC path, DNS, security groups'],['Credential retrieval','Read the configured credential source','Secret or credential-provider permission'],['Application login','Establish the test identity','Successful target authentication'],['Target rules','Define what may be tested','Authorized scope and exclusions']],'Source reachability, target reachability, and authenticated application access are independent conditions.'),
 table('Assessment interfaces and result records',['S-16'],[['Interface or record','Purpose'],['Administrative console','Configure application scope, integrations, and access'],['Assessment workspace','Create and inspect assessments'],['Run and finding','Identify the analyzed subject and supporting evidence'],['Repository proposal','Review a generated change before deployment'],['Revalidation job','Retest selected findings against the current deployment'],['Jira issue','Track work in an external system']],'The originating assessment, reviewed revision, deployed revision, and verification job remain separate identities.')])
DECKS['finops']['slides'].extend([
 table('Source interfaces, stored data, and inference location',['F-12'],[['Boundary','Documented property'],['AWS source access','Data-role permissions for the named source services'],['Collaboration access','Registered Jira or Slack integration and instance connection'],['Persistent storage','Preview data stored in us-east-1'],['Inference','Can use other US Regions'],['Private-tool networking','No DevOps VPC resource-gateway interface is asserted for this service']],'Storage geography, inference geography, and source authorization answer different configuration questions.'),
 table('Conversations, task history, and report artifacts',['F-15'],[['Workspace','Purpose'],['Conversation','Immediate analytical interaction'],['Tasks','Separately queued work and its results'],['Automations','Rules that create future tasks'],['Context files','Uploaded organizational reference material'],['Artifacts','Generated reports, including conversation-originated reports']],'Not every answer is a task, and not every artifact has a task as its parent. A report revision must retain its intended analytical basis.')])

DC={}
for product,deck in DECKS.items():
    positions={sid:i for i,c in enumerate(CHAPTERS[product]) for sid in c['sections']}
    buckets={i:[] for i in range(len(CHAPTERS[product]))}
    for s in deck['slides']:
        buckets[positions[s['refs'][0]]].append(s)
    ordered=[];groups=[]
    for i,c in enumerate(CHAPTERS[product]):
        values=buckets[i]
        if not values:continue
        start=len(ordered);ordered.extend(values)
        groups.append((c['title'],list(range(start,len(ordered)))))
    deck['slides']=ordered;DC[product]=groups
(HERE/'presentation.py').write_text('"""HTML curriculum organized by documented capability dimensions."""\nDECKS='+pprint.pformat(DECKS,width=105,sort_dicts=False)+'\n')
(HERE/'structure.py').write_text('"""Capability-oriented reading structure; frozen semantic records are unchanged."""\nREVISION="2026-10-23-capability-exposition"\nBASELINE="75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9"\nCHAPTERS='+pprint.pformat(CHAPTERS,width=105,sort_dicts=False)+'\nDECK_CHAPTERS='+pprint.pformat(DC,width=105,sort_dicts=False)+'\nTYPES='+repr(TYPES)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else TYPES.get(sid,"reference")\n')
p=ROOT/'qa/exposition-review.json';review=json.loads(p.read_text())
review['official_rechecks'].append({'url':'https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html','supports':'UI/API test-profile authentication; TOTP for both, email for UI only; real application requests including writes.'})
review['routing_corrections']={'MX-D-QUERY':'D-21: conversational assistance','MX-D-CUSTOM':'D-19: custom invocation','MX-S-PERSONALIZE':'S-13: finding-edit personalization'}
review['timing']={p:{'minutes':sum(s['seconds'] for s in d['slides'])//60,'exercise_minutes':sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')//60} for p,d in DECKS.items()}
p.write_text(json.dumps(review,indent=2)+'\n')
Path(__file__).unlink()
