"""Apply this reviewed source revision once; remove the migration script afterward."""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path
from pprint import pformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASELINE = '13b619a7cddd8249fbaa54931ca2099409eb8890'
DATE = '2026-10-23'
REVISION = DATE+'-technical-editorial-review'
changes = []


def write(path, text):
    (ROOT/path).write_text(text.rstrip()+'\n', encoding='utf-8')


def patch(path, before, after, count=1):
    text = (ROOT/path).read_text(encoding='utf-8')
    found = text.count(before)
    if found != count:
        raise ValueError(f'{path}: expected {count} anchors, found {found}: {before[:90]}')
    write(path, text.replace(before, after))
    changes.append({'file': path, 'operation': 'replace', 'occurrences': found, 'before': before[:200], 'after': after[:200]})


def function(path, name, replacement):
    text = (ROOT/path).read_text(encoding='utf-8')
    start = re.search(r'^def '+re.escape(name)+r'\(', text, re.M)
    if not start:
        raise ValueError('Function missing: '+name)
    end = re.search(r'^def \w+\(', text[start.end():], re.M)
    stop = start.end()+end.start() if end else len(text)
    write(path, text[:start.start()]+replacement.strip()+'\n\n\n'+text[stop:])
    changes.append({'file': path, 'operation': 'replace function', 'function': name})


# Procedure detail remains in one maintained registry. The renderer no longer
# repeats a methodology disclaimer beneath every mechanism.
function('tools/docs/mechanism_detail.py', 'block', r'''
def block(entry):
    d=entry['review'];refs=list(dict.fromkeys(c['source'] for c in d['claims']))
    cite=' '.join('['+r+']' for r in refs)
    lines=[f"#### {entry['id']} — {entry['title']}",'']
    lines.extend(p+' '+cite+'\n' for p in d['narrative'])
    lines.extend(['**Inputs.** '+d['inputs'],''])
    if d.get('diagram'):
        lines.extend([f"![{entry['title']}: state and control paths](../assets/diagrams/{d['diagram']}.svg)",''])
    lines.extend(['**Configuration**',''])
    for i,(control,procedure,scope) in enumerate(d['configuration'],1):
        lines.append(f'{i}. **{control} — {scope.rstrip(".")}.** {procedure}')
    lines.extend(['',cite,'','**Lifecycle and operator actions**','',
                  markdown_table(['Initial condition','Operation or event','Result'],d['lifecycle']), '',
                  '**Constraints.** '+d['controls'],'',
                  '**Inspection points.** '+d['observable_output'],'',
                  '**Implementation limits.** '+d['undocumented'],'',
                  '**Verification procedure (proposed)**',''])
    for i,t in enumerate(d['test'],1):lines.append(f'{i}. {t}')
    lines.append('')
    if entry.get('related_mechanisms'):
        lines.append('**Related mechanism.** '+' '.join(f"[{r['id']}](../catalog/mechanisms.html#{r['id']}): {r['dependency']} — {r['condition']}" for r in entry['related_mechanisms']))
        lines.append('')
    lines.extend(['**Source mapping**','',markdown_table(['Reference','Documentation section','Supported behavior'],[['['+c['source']+']',c['section'],c['assertion']] for c in d['claims']]),''])
    return '\n'.join(lines)
''')
patch('tools/docs/mechanism_detail.py', "path.write_text(body.rstrip()+'\\n\\n'+definitions+'\\n'+newdefs+'\\n',encoding='utf-8')", "path.write_text(re.sub(r'\\n{3,}', '\\n\\n', body.rstrip()+'\\n\\n'+definitions+'\\n'+newdefs+'\\n'),encoding='utf-8')")
patch('tools/docs/mechanism_detail.py', 'Read the complete mechanism explanation and procedure', 'Read the configuration, lifecycle, and verification procedure')
patch('tools/docs/mechanism_detail.py', '<strong>Evidence boundary.</strong> ', '<strong>Implementation limits.</strong> ')

# Factual corrections are explicit, source-linked exceptions to frozen summary
# fields. Identity and feature dependency changes remain checked independently.
path = ROOT/'catalog/mechanisms.json'
data = json.loads(path.read_text())
entries = {e['id']: e for e in data['entries']}
corrections = []

def correct(mid, field, after, reason, urls):
    before = entries[mid][field]
    if before == after:
        raise ValueError('Correction already applied: '+mid+'/'+field)
    entries[mid][field] = after
    corrections.append({'id': mid, 'field': field, 'before': before, 'after': after, 'reason': reason, 'official_sources': urls})

correct('MX-F-ARTIFACT','state','Report artifact, originating conversation or task, and query basis',
        'Report generation also returns artifacts in conversation; a task is not a universal parent resource.',
        ['https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html'])
correct('MX-F-MEMORY','trigger','Conversation preferences, corrections or task outcomes; explicit remember, update or forget requests',
        'The memory input model includes retained task outcomes and is not limited to imperative remember requests.',
        ['https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html'])
correct('MX-S-GENERATE','trigger','Policy documents are submitted for requirement generation',
        'Approval of policy source is a team control, not a documented service-side approval gate.',
        ['https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html'])
correct('MX-D-QUERY','sections',entries['MX-D-QUERY']['sections']+['D-07'],
        'Place invocation instructions in the operations chapter; retain the high-level overview and integration references.',[])
entries['MX-D-QUERY']['review']['primary_section']='D-07'
entries['MX-F-ARTIFACT']['review']['inputs']='Cost-report request, authorized source access, query parameters, output format and optional report template.'
entries['MX-F-ARTIFACT']['review']['observable_output']='Report artifact and its source conversation or task. Record the query parameters and output identity used for reconciliation.'
entries['MX-F-MEMORY']['review']['inputs']='Conversation preferences, corrections, task outcomes, and explicit requests to remember, update or forget information within the instance.'
entries['MX-S-GENERATE']['review']['inputs']='Documents submitted for a custom requirement pack. The team reviews the policy source and replacement before enabling the pack.'
# Keep operational terminology precise without broadening behavior.
replacements = {
    'The useful result': 'The output',
    'The right procedure is to': 'To verify the result,',
    'a harmless report task': 'a report task using non-sensitive inputs',
    'a harmless read-only account query': 'a read-only query in an authorized account',
    'a harmless required heading': 'a test-only required heading',
    'A custom definition is useful for a recurring or specialized procedure, not a repair for missing read access.': 'Use a custom definition for a recurring or specialized procedure; configure source access independently.',
    'No universal source-completeness or exact query-planning guarantee is provided.': 'The cited guide does not specify the query-selection algorithm. Inspect the sources and query parameters used by the execution.',
    'Complete inference logic, causal accuracy and guaranteed agreement with differently scoped console queries are not established.': 'The source guides do not specify the query-planning algorithm. Queries with different dates, metrics or filters are not directly comparable.',
    'Exact relevance thresholds and a universal selection trace are not guaranteed; unavailable observability remains unverified.': 'The cited guide does not specify relevance thresholds or guarantee a skill-selection event in every execution trace.',
    'do not invent it.': 'do not assume a precedence order.'
}

def language(value):
    if isinstance(value,str):
        for before,after in replacements.items():
            value=value.replace(before,after)
        return value
    if isinstance(value,list):return [language(v) for v in value]
    if isinstance(value,dict):return {k:language(v) for k,v in value.items()}
    return value
for entry in entries.values():
    entry['review']=language(entry['review'])
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

patch('tools/docs/mechanism_detail.py',
      "    if changed:errors.append('Existing mechanism identity/dependency summaries changed: '+json.dumps(changed))",
      "    edit_record=ROOT/'qa/technical-edit-record.json'\n    permitted=json.loads(edit_record.read_text())['core_corrections'] if edit_record.exists() else []\n    for item in changed:\n        old_entry=next(e for e in old if e['id']==item['id'])\n        for field in item['fields']:\n            matches=[c for c in permitted if c['id']==item['id'] and c['field']==field and c['before']==old_entry.get(field) and c['after']==current[item['id']].get(field)]\n            if len(matches)!=1:errors.append(item['id']+': unreviewed summary change '+field)")
patch('tools/docs/mechanism_detail.py', "'added_mechanism':'MX-S-PERSONALIZE','regression_checks':regression", "'added_mechanism':'MX-S-PERSONALIZE','reviewed_core_corrections':permitted,'regression_checks':regression")

# Product definitions replace rhetorical openings. Conventions occur once per
# guide rather than being repeated in each mechanism.
abstracts = {
'devops': ('AWS DevOps Agent', 'Resource model, integrations, retained context, and operational execution',
    'AWS DevOps Agent performs incident investigation, operational queries, prevention analysis, and user-defined operational tasks. An Agent Space associates account access, provider connections, and execution context. Investigations and custom-agent invocations are separate execution records. Release-readiness review and active release testing have their own scope and availability. [DS18] [DS08]',
    'The guide first defines the resources and their relationships. It then covers source access, knowledge production and retrieval, execution controls, and the existing operational use cases. The incident example uses synthetic telemetry to distinguish a previous cause from the current failure.'),
'security': ('AWS Security Agent', 'Application scope, assessment configuration, findings, and revalidation',
    'AWS Security Agent analyzes source code and design material, constructs threat models, and performs application penetration tests. An Agent Space selects application sources and assessment configuration. Assessment results, remediation proposals, deployed revisions, and revalidation jobs have separate identities and lifecycles. Feature availability and provider support must be checked for the selected assessment. [SS01] [SS02]',
    'The guide defines shared and application-scoped resources before describing repository access, target rules, authentication, requirements, assessment execution, and finding management. The worked example traces an authorization finding through a proposed repair and targeted revalidation.'),
'finops': ('AWS FinOps Agent', 'Cost-data access, retained context, tasks, and report artifacts',
    'AWS FinOps Agent is documented as a preview service for cost queries, anomaly investigation, reporting, and interpretation of recommendations from AWS optimization services. Analysis depends on the accounts, dates, cost metric, filters, and grouping supplied to authorized source services. The instance retains context, conversations, tasks, and report artifacts. [FS01]',
    'The guide separates source permissions from operator access and publication connections. It then explains uploaded files, persistent memory, conversation summarization, task execution, and data lifecycle. The cost example reconciles the numerical change before assessing operational evidence. The reviewed preview stores agent data in us-east-1; inference can use other US Regions. [FS08] [FS09]'),
'architecture': ('Architecture of AWS operational agents', 'Concept ownership, product resources, execution, and evidence',
    'AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent expose different configuration resources, execution records, and retained state. This guide defines the concepts used by the documentation and maps them to the product-specific models. It does not define a common AWS resource schema or cross-service runtime. [AS30] [AS31] [AS32]',
    'Start with entity ownership and resource identity. The following chapters compare integrations, retained context, authorization, execution lifecycle, and evidence handoffs. The operational-review example combines reviewed outputs while retaining each service\'s configuration and permissions.')}
conventions = ('**Reading conventions.** Product statements link to official AWS documentation. Configuration recommendations and verification procedures are team guidance; the proposed tests and synthetic examples have not been executed against AWS. Lifecycle tables describe service behavior and operator actions, not an API status enumeration unless explicitly cited. DOC (blue), AWS (green), and EXT (orange) identify concept ownership. Source-review dates and qualifications are recorded in the source registers.')
for product,(title,subtitle,first,second) in abstracts.items():
    p=ROOT/f'guides/{product}.md';text=p.read_text()
    text=re.sub(r'\n*<!-- mechanism-review:start [^>]+ -->.*?<!-- mechanism-review:end [^>]+ -->\n*','\n\n',text,flags=re.S)
    chapter=re.search(r'^## 01\.',text,re.M)
    if not chapter:raise ValueError('First chapter missing: '+product)
    text=f'# {title}\n\n{subtitle}\n\n{first}\n\n{second}\n\n{conventions}\n\n'+text[chapter.start():]
    text=language(text)
    text=text.replace('The right procedure is to reproduce the numerical result first, then evaluate the explanation.', 'Reproduce the numerical result before evaluating its explanation.')
    text=text.replace('The useful starting point is therefore the application:', 'The assessment inputs are:')
    text=text.replace('the newer indexed memory guidance', 'the indexed memory guidance retrieved for the source review')
    text=text.replace('the older/newer-page discrepancy', 'the retrieved-page discrepancy')
    text=text.replace('the newer indexed guide and managed-agent page agree', 'the indexed guide and managed-agent page agree')
    text=text.replace('This guide follows the newer task-specific wizard', 'This guide follows the task-specific wizard')
    text=text.replace('before using the reference fields', 'before selecting the configuration profile')
    text=re.sub(r'\n{3,}', '\n\n', text)
    write(f'guides/{product}.md',text)
    changes.append({'file':f'guides/{product}.md','operation':'replace introduction; consolidate conventions; normalize paragraph spacing and version qualification'})

# Remove duplicated explanations, retaining examples, concrete fields, tables,
# authorization limits and nonduplicate operating instructions.
removals={
'guides/devops.md':[
'A correction becomes useful only when it identifies what the original investigation got wrong and supplies the verified alternative. That is a different input from simply collecting another similar incident. The feedback path records that distinction so later work can treat a prior conclusion as corrected context.',
'Some guidance belongs in every new session, such as the format of an incident finding or the conventions used to name services. Standing instructions provide that context at startup. They are appropriate for persistent behavioral guidance rather than a procedure relevant only to one symptom.',
'Global and agent-specific `AGENTS.md` text is supplied at startup; it is not selected by relevance. Changes apply to sessions started after saving. A running session retains its startup content. [DS09]',
'**Procedure:** add a skill from **Knowledge → Skills**, write a description naming the relevant symptoms and services, choose agent scope, and supply the procedure. Test a matching request and a nonmatching request. Inspect available run evidence for selection and tool use; document an unavailable signal as unverified rather than asserting selection.'
],
'guides/finops.md':[
'A cost question becomes a set of data queries with a specific comparison basis. The returned amounts, recommendations, and change records then support different conclusions. Reproducing the amount is the first step; explaining its cause requires additional evidence.',
'The agent translates an inquiry into supported data-source calls, interprets returned evidence using the instance\'s context, and generates a response or artifact. Cost Explorer totals, anomaly events, recommendation records and CloudTrail change records answer different questions. [FS01] [FS03]'
]}
for relative,paragraphs in removals.items():
    text=(ROOT/relative).read_text()
    for paragraph in paragraphs:
        if text.count(paragraph)!=1:raise ValueError('Duplicate-removal anchor: '+paragraph[:90])
        text=text.replace(paragraph+'\n\n','')
        changes.append({'file':relative,'operation':'remove explanation duplicated by the maintained mechanism detail','text':paragraph})
    if relative.endswith('finops.md'):
        text=text.replace('### F-M01 — Cost queries and recommendation provenance\n\n', '### F-M01 — Cost queries and recommendation provenance\n\nHistorical amounts, forecasts, anomalies, and recommendations are different source results. Define the query parameters before comparing them. [FS01] [FS03]\n\n')
    write(relative,text)

# Add a source omitted from the integration matrix. This is a provider binding,
# not a new use case, feature abstraction, or assumed GA declaration.
security=(ROOT/'guides/security.md').read_text()
anchor='| Confluence | Confluence Cloud |'
pos=security.index(anchor)
row='| Azure DevOps | Git repositories; TFVC unsupported | Authorized organization and selected repositories | Entra service principal and Azure DevOps permissions; review comments and remediation configured separately [SS490] |\n'
security=security[:pos]+row+security[pos:]
anchor='![Application-source registration and selection]'
pos=security.index(anchor)
paragraph=('For Azure DevOps, registration authorizes the Microsoft Entra application. Add its service principal to the Azure DevOps organization and grant repository and service-hook permissions before selecting repositories in an Agent Space. Public-repository remediation is not supported. The provider guide describes project limits and required permissions; registration alone does not complete access setup. [SS490]\n\n')
security=security[:pos]+paragraph+security[pos:]
security+='\n[SS490]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-azure-devops.html\n'
write('guides/security.md',security)

# Use concrete presenter explanations instead of the same instruction on every
# resource diagram. Update the existing provider table without adding slides.
p=HERE/'presentation.py';text=p.read_text();tree=ast.parse(text)
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DECKS' for t in n.targets))
decks=ast.literal_eval(node.value)
messages={
'er-devops-scope':'An Agent Space associates account roles and providers. A custom-agent definition selects tools and context; each invocation records a separate execution. Provider registration and space association are distinct configuration operations.',
'er-devops-knowledge':'A custom definition references existing skill and memory-store assets. A store contains entries; updates create entry versions. Activation and attachment control availability, while retrieval occurs during execution.',
'er-security-scope':'Shared registrations and requirement packs are separate from application-scoped configuration. An Agent Space selects sources and users. The target application and published issue retain external ownership.',
'er-security-assessments':'Penetration tests, full-code reviews, and threat models have reusable configurations and separate runs. A design review is a one-off assessment. Record the assessed revision and scope for each execution.',
'er-security-lineage':'Preserve the original finding identity through proposal, deployment, and revalidation. The documentation-defined result association records the outcome of a particular revalidation job; it is not an additional AWS API resource.',
'er-finops-scope':'The instance uses separate data-access and operator roles. Account-level Jira or Slack registration is followed by an instance-specific project or channel connection.',
'er-finops-work':'A conversation may answer directly. An explicit task has a separate queue and execution record. An automation creates future tasks. Report artifacts can originate from a conversation or task.',
'er-finops-context':'Files, retained preferences, and conversation summaries supply different context. File restoration, memory correction, and conversation compaction operate on different state.',
'er-devops-incidents':'A signal can be linked, skipped, or investigated. Steering changes the active analysis; completed-investigation feedback provides a corrective input. Resource mutation requires its separate approval path.',
'er-concept-model':'Blue nodes are documentation concepts; green nodes are AWS-defined concepts; orange nodes represent external systems or engineering records. Relationships describe the documentation model, not a shared AWS runtime.'}
for key,deck in decks.items():
    for slide in deck['slides']:
        if slide.get('diagram') in messages:slide['message']=messages[slide['diagram']]
        if slide['title']=='Login optimization':slide['title']='Login Optimization and retained authentication procedures'
        slide['message']=language(slide['message'])
        if key=='security' and slide['title']=='Repository, documentation, and Jira connections':
            slide['data'].insert(3,['Azure DevOps','Git repositories; TFVC unsupported','Entra authorization, organization permissions, repository selection; writes configured separately.'])
            slide['message']='Register the provider, grant its required permissions, and select application resources. Repository comments, remediation proposals, and Jira publication are separate configured operations.'
        if key=='devops' and slide['title']=='Resource identities and lifecycle boundaries':slide['title']='Agent Space, asset, and invocation identities'
        if key=='security' and slide['title']=='Resource identities and lifecycle boundaries':slide['title']='Assessment configuration, run, and finding identities'
        if key=='finops' and slide['title']=='Resource identities and lifecycle boundaries':slide['title']='Instance, conversation, task, and artifact identities'
write('tools/docs/presentation.py', '"""HTML presentations: product resources, mechanisms, and operational procedures."""\nDECKS='+pformat(decks,width=105,sort_dicts=False)+'\n')

# Product-specific chapter transitions replace identical introductory prose.
p=HERE/'structure.py';text=p.read_text()
text=text.replace('REVISION="2026-10-22-mechanism-review"', 'REVISION="'+REVISION+'"')
# Handle either quote style emitted by earlier tooling.
text=re.sub(r'^REVISION\s*=.*$', 'REVISION="'+REVISION+'"',text,flags=re.M)
write('tools/docs/structure.py',text)

# Source checks and concise methods remain visible; repeated negative guarantees
# and marketing are not substitutes for evidence.
patch('tools/docs/build.py', 'Read the service architecture, supported integrations, knowledge mechanisms, and operating workflows for three AWS services.', 'Technical reference for the resource models, integrations, retained context, and execution workflows of three AWS services.')
patch('tools/docs/build.py', 'The guides explain the platforms; the use-case catalog applies them to daily engineering work; the HTML presentations provide a timed teaching sequence.', 'The guides define product behavior and configuration. The catalog links operational objectives to mechanisms and implementation profiles. HTML presentations use the same sources.')
patch('tools/docs/build.py', 'Logical model, not AWS internal deployment. Resource ER diagrams qualify undocumented multiplicity and logical associations in their relationship register.', 'Logical model. Entity ownership and relationship qualifications are defined in the resource register.')
# Generated documentation and metadata use the amended renderer on every build.
patch('tools/docs/check.py', 'from resource_model import validate as validate_resources', 'from resource_model import validate as validate_resources\nfrom editorial_check import validate as validate_editorial')
patch('tools/docs/check.py', '    model_result=validate_model(guides, browser=browser)', '    editorial_result=validate_editorial(guides)\n    errors.extend(editorial_result["errors"])\n    model_result=validate_model(guides, browser=browser)')
patch('tools/docs/check.py', "    results['relationship_model']=model_result", "    results['relationship_model']=model_result\n    results['technical_editorial_review']=editorial_result")

standard=(ROOT/'EDITORIAL_STANDARD.md').read_text()
standard+='''\n## Technical language and evidence status\n\nUse the product object, operation, input, output, and condition as the subject of each explanation. Replace unmeasured benefit claims with documented behavior. Avoid slogans, rhetorical questions, evaluative adjectives, conversational asides, and repeated statements about the quality of the document. Retain exact AWS feature names even where their wording differs from house style.\n\nSeparate product prerequisites from team procedures. A recommended approval is not a native service gate; a proposed acceptance test is not a recorded result. Describe cancellation, deletion, publication, and permission effects for the specific object. Use one reading-conventions paragraph per guide; retain mechanism-specific constraints next to the operation.\n\nDo not declare one retrieved documentation version newer solely because it was indexed more recently. Record conflicting content and qualify the affected procedure. Targeted rechecks do not update the review date of all retained claims. An editorial checker detects selected regressions; it does not establish technical completeness or writing quality.\n'''
write('EDITORIAL_STANDARD.md',standard)
change=(ROOT/'CHANGELOG.md').read_text()
heading=change.find('\n')
change=change[:heading+1]+'''\n## 2026-10-23 — Technical editorial review\n\nReplaced rhetorical introductions, removed repeated mechanism boilerplate and overlapping explanations, and revised diagram presenter notes. Corrected FinOps artifact provenance and memory inputs, separated team policy approval from requirement generation, and added the documented Azure DevOps source binding to the Security integration inventory. The 30 use-case records and approved resource model are unchanged.\n\n'''+change[heading+1:].lstrip()
write('CHANGELOG.md',change)
record={
'reviewed_on':DATE,'baseline':BASELINE,
'scope':'Technical wording, guide narrative, presentation explanations, selected factual corrections and corresponding regression checks.',
'protected':'The use-case, feature, profile, alias and resource-model source files are unchanged.',
'core_corrections':corrections,'editorial_changes':changes,
'additional_source_checks':[
{'url':'https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html','section':'Generating cost reports','finding':'Artifacts can be returned in conversation; scheduled reporting uses tasks.','action':'Correct artifact provenance and inspection text.'},
{'url':'https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html','section':'Agent memory across sessions','finding':'Retained context includes preferences, corrections and task outcomes.','action':'Correct the trigger and input summary.'},
{'url':'https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html','section':'Generate requirements by uploading documents','finding':'Generation replaces pack content; source approval is a team control.','action':'Separate native trigger from team review.'},
{'url':'https://docs.aws.amazon.com/securityagent/latest/userguide/connect-azure-devops.html','section':'How Azure DevOps integration works; Register; Grant access','finding':'Git repositories are supported; TFVC is excluded; registration, organization permission and repository selection are separate.','action':'Add qualified provider row and procedure summary. Retrieved from the official indexed page; direct retrieval returned no content.'},
{'url':'https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html','section':'How memories work; Deleting a memory store','finding':'Direct and indexed page representations differ in coverage.','action':'Retain documented behavior but remove unsupported relative-age claims.'},
{'url':'https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html','section':'Review personalized findings','finding':'Personalization adjusts finding attributes; it does not repair the application.','action':'Retain the mechanism and its existing control distinction.'},
{'url':'https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html','section':'Read-write actions','finding':'Jira approval is invocation-dependent; Slack posting has no per-message approval.','action':'Retain separate controls.'},
{'url':'https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html','section':'Managing your data','finding':'Context files, memory, tasks and automations have distinct controls.','action':'Retain object-specific lifecycle guidance.'}
],
'boundary':'Targeted product-source checks and editorial corrections. Other sources retain their existing review dates. No live AWS workflow, performance test or savings measurement was executed.'}
write('qa/technical-edit-record.json',json.dumps(record,ensure_ascii=False,indent=2))
# This is a migration, not a second maintained renderer or document archive.
Path(__file__).unlink()
print(json.dumps({'editorial_revision':REVISION,'core_corrections':len(corrections),'approved_use_cases_changed':False,'migration_removed':True}))
