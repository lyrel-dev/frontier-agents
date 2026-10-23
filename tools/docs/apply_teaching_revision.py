"""One-time migration to an agent-first teaching sequence; deletes itself."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import pprint
import re
import subprocess

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASELINE='1a62b5686ec361d1b4ab894df0a0ab249cfe1d78'
FROZEN=('use-cases','mechanisms','features','profiles','aliases','resource-models')
before={n:(ROOT/f'catalog/{n}.json').read_bytes() for n in FROZEN}
from build import parse_source
from structure import CHAPTERS, TYPES, LABELS, BASELINE as RESOURCE_BASELINE
import course

SOURCES={
 'devops':{
 'DS701':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html',
 'DS702':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html',
 'DS703':'https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html',
 'DS704':'https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html',
 'DS705':'https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html',
 'DS706':'https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html',
 'DS707':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html',
 'DS708':'https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html'},
 'security':{
 'SS701':'https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html',
 'SS702':'https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html',
 'SS703':'https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html'},
 'finops':{
 'FS701':'https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html',
 'FS702':'https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html',
 'FS703':'https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html'},
 'architecture':{
 'AS701':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html',
 'AS702':'https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html',
 'AS703':'https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html'}
}
PROSE={
'devops':{
'D-90':('An agent, its configuration, and one execution',r'''In this guide, an agent is the AI executor that uses applicable instructions, procedures, informational context and permitted source operations to work on a request. AWS DevOps Agent is the service; it provides managed agent roles and also lets a customer define custom agents. A saved custom-agent definition is reusable configuration. One invocation is a particular run of that definition. Managed incident roles instead contribute to an investigation. [DS701] [DS702]

![An agent and its operating context](../assets/diagrams/teaching-devops-agent.svg)

Read the figure from the request to the execution, down to the connected source and back to the result. The upper boxes explain why the agent behaves differently from an unconfigured model call. Instructions define behavior. A skill supplies a procedure. Memory supplies retained facts or lessons selected for the work. Tools perform the actual source operations. An integration supplies the provider connection; it is not itself an instruction, and a stored memory is not a current telemetry query. [DS702] [DS704] [DS708]

For a custom agent, the customer selects the system prompt, tools, skills and attached stores. For managed agents, AWS maintains the underlying role, tools and skills; customers can provide the documented global and agent-specific instructions. The same picture therefore represents two control models, not a claim that every box is editable for every agent. [DS701] [DS702]

Consider a request to investigate checkout timeouts. A skill may describe which dependency measurements to compare. A memory may retain a previously verified database cause. The current tool results may instead show upstream latency. The informational context helps frame the inquiry, but the conclusion must follow the evidence for the current incident. This example illustrates the roles of the components; the supplied synthetic walkthrough appears in D-U01.

The diagram is a logical teaching view of documented facilities. Its aggregate boxes do not add native resource types to the approved entity model. The fixed positions are reused below so each workflow changes the highlighted path, not the vocabulary.'''),
'D-91':('How managed agents contribute to coordinated work',r'''AWS exposes managed responsibilities including Chat, Incident triage, Incident RCA, Incident mitigation, Incident UI, Grader and Learning. The incident roles run within an investigation rather than as standalone custom invocations. Learning has separate run history and platform-owned triggers. These facts describe the supported operating model; they do not disclose a complete internal call graph. [DS701]

![Managed responsibilities and knowledge reuse](../assets/diagrams/teaching-devops-coordination.svg)

Triage acts on the incoming incident signal. It may link that signal to an existing investigation, skip it according to configured criteria, or schedule independent investigation work. A linked signal contributes context to the existing investigation. The RCA responsibility concerns evidence and explanation; mitigation concerns proposed responses; Incident UI concerns the investigation's outputs. A useful diagram must therefore show a shared investigation context without implying that every event runs all roles in an unconditional sequence. [DS701] [DS705]

Learning supplies a different relationship: earlier activity and connected environment evidence contribute to retained knowledge that later agents can read. An engineer's correction, a managed investigation Review, a learning refresh and a prevention evaluation are not the same operation. In particular, prevention evaluation examines multiple investigations to propose improvements; it is not simply the name of every background learning run. [DS701] [DS704] [DS706]

Custom-agent continuation and registered external-agent delegation are also different from the incident-role model. AWS documents automatic continuation when a custom invocation approaches its context limit. That does not establish customer control of an arbitrary graph of managed agents. D-19 explains continuation and invocation state; D-20 describes separately configured external delegation. [DS702]

To follow coordinated work, inspect the record that actually connects the activities: the signal-to-investigation link, the investigation evidence, the retained memory entry, or the referenced output. Do not infer an additional runtime relationship from two agent names appearing on the same diagram.'''),
'D-92':('Agent Space, connections, and access scope',r'''An Agent Space is the logical container around operational work. It defines connected AWS account access, third-party integrations and user permissions. Investigation records, incident history and Chat history are isolated by space. The Agent Space is not one agent, one invocation, the application under investigation, or a customer-hosted execution cluster. [DS703]

![The enclosing Agent Space](../assets/diagrams/teaching-devops-space.svg)

The enclosing boundary is the addition to the preceding picture; the agent, context, source-access path and output remain in the same positions. Provider registration establishes an authenticated integration. Association selects its use in a particular Agent Space. A custom-agent definition then selects the tools and memory stores it can use. A registered provider, a valid association, an assigned operation and a successful source read are different observations. D-12 and D-03 explain the provider-specific setup; D-16 explains custom selection. [DS702] [DS703]

Network reachability is another concern. A private connection provides a route to a supported endpoint; it does not place the whole DevOps Agent service inside the customer VPC and does not grant a tool additional permission. Operator access, execution identity and approval for a state-changing action remain separate controls, detailed in D-02, D-04 and D-M06. [DS707]

The diagrams show only the relationships needed for the teaching sequence. Use D-13 and the approved resource-model reference when an exact asset identity, parent scope or relationship qualification is needed. The teaching view does not replace that model.'''),
'D-93':('Incident response and the order of operational workflows',r'''For a DevOps or SRE audience, the teaching sequence begins with immediate incident work, then moves to routine reporting, recurring-incident improvement, operational knowledge and change assurance. Operational reviews consume the resulting evidence. This priority is an editorial choice based on the audience's work, not an AWS ranking. The approved use-case definitions and groupings are unchanged.

| Teaching order | Existing use cases | Question being answered |
|---|---|---|
| Incident operations | UC-D01–UC-D05 | What is happening, what response is justified, and what has changed? |
| Operational reporting | UC-D06 and UC-D07 | What do current measurements and deployment records show? |
| Reliability improvement | UC-D08 and UC-D09 | What recurs, and which prevention work should be prioritized? |
| Operational knowledge | UC-D10 and UC-D11 | Which procedures and environment descriptions should be maintained? |
| Configuration and release assurance | UC-D12–UC-D14 | Does an identified configuration or change meet the relevant criteria? |
| Operational review | UC-G01 | Which decisions and follow-up actions are supported by the assembled evidence? |

![Incident evidence path](../assets/diagrams/teaching-devops-incident.svg)

Incident work begins with a signal identity, an affected service and the actual observation interval. Triage chooses a relationship to investigation work; a linked signal is not a missing incident, and a skipped signal is not a health verdict. The investigation reads current evidence through authorized tools and may retrieve relevant earlier context. Its result is a supported explanation, a set of hypotheses or an explicit evidence gap. [DS705]

![Planning and authorized effects](../assets/diagrams/teaching-devops-mitigation.svg)

A proposed mitigation adds a target, parameters and validation or rollback conditions. Execution adds a separate permission and approval boundary. The resulting resource state and the service recovery measurements must be inspected independently: an accepted proposal, approved operation and recovered service are three different outcomes. An incident bulletin reports the investigation's current state at a declared cutoff; it does not create a new root cause or authorize another effect. [DS705] [DS707]

The corresponding catalog articles are [triage](../catalog/UC-D01.html), [investigation](../catalog/UC-D02.html), [mitigation planning](../catalog/UC-D03.html), [approved execution](../catalog/UC-D04.html) and [incident communication](../catalog/UC-D05.html). They retain their own completion criteria and failure handling.'''),
'D-94':('Health reporting and deployment review',r'''Routine reporting reuses the evidence path without requiring a new incident. A native Chat inquiry can answer a scoped operational question. A custom definition is appropriate when the team needs repeatable source selection, a prescribed report structure or recurring invocation. Its prompt, skills, tools and optional memory attachments define how that work is performed. [DS702]

![Reporting on the same architecture](../assets/diagrams/teaching-devops-reporting.svg)

The request now specifies services, the UTC interval, measures, aggregation and comparison period. The tools retrieve current observations; a skill can define the reviewed reporting procedure; retained context can explain service names or dependencies. The output should preserve material values, the query basis and failed reads. Missing telemetry is not a healthy result, and an old memory is not a replacement measurement.

A deployment review shares some sources but asks a different question. It identifies immutable revisions, environments, deployment states and relevant changes. The service-health report evaluates observations and trends; the deployment review accounts for change activity. Their distinct approved objectives remain [UC-D06](../catalog/UC-D06.html) and [UC-D07](../catalog/UC-D07.html).

When recurrence is needed, a trigger creates future invocations. The observation interval, actual start and delivery time remain separate. Configure and inspect a trial run before relying on a recurring report. The detailed invocation, schedule and cancellation procedures are in D-07 and D-19. [DS702]'''),
'D-95':('Incident learning, procedure maintenance, and topology documentation',r'''Earlier investigations are inputs to later context and improvement work, but these outputs serve different purposes. Monitor-memory construction retains cause history; corrective feedback supplies verified corrections; prevention evaluation compares investigations to propose improvements. The Learning agent and the prevention workflow must not be represented as one operation with one schedule. [DS704] [DS705] [DS706]

![Production and later use of context](../assets/diagrams/teaching-devops-learning.svg)

Follow knowledge production and retrieval separately. An entry can exist without being available to a particular custom agent; available content can remain unselected; a retrieved entry can be inconsistent with current evidence. In a recurring-alarm investigation, inspect the actual source observations before adopting the previous cause. [DS702] [DS704]

[Incident-pattern identification](../catalog/UC-D08.html) asks what recurs across the evidence. [Prevention prioritization](../catalog/UC-D09.html) asks which improvement should be acted on and how success will be evaluated. These remain separate objectives even when they share investigation history.

![Procedure and environment knowledge paths](../assets/diagrams/teaching-devops-knowledge.svg)

For [SOP consolidation](../catalog/UC-D10.html), the team reconciles conflicting procedures and publishes an approved skill with concrete applicability and tool prerequisites. It is maintaining procedural guidance, not synthesizing another incident finding. For [topology documentation](../catalog/UC-D11.html), connected evidence and managed understanding provide a representation to compare with deployed reality. The accepted architecture document must distinguish observed, inferred and unresolved relationships. Skills and informational memory have different purposes and loading behavior. [DS702] [DS704]

Detailed procedures follow in the knowledge chapters. The current walkthrough keeps the original source evidence, the service's retained representation and the team-accepted document distinct.'''),
'D-96':('Configuration assurance, release assurance, and operational reviews',r'''A configuration audit compares identified resource values with declared rules. A release-readiness review examines a proposed change and its dependencies. Active release testing exercises a configured deployed UI or API target. The architecture is reused, but the subject, permitted effects and evidence of completion differ. D-16 and D-22 describe the applicable product facilities and qualifications. [DS702]

![Change assurance on the same access and execution model](../assets/diagrams/teaching-devops-change.svg)

Keep the approved objectives separate: [configuration audit](../catalog/UC-D12.html), [release readiness](../catalog/UC-D13.html), and [deployed-release testing](../catalog/UC-D14.html). A reviewed code revision is not proof that the same revision was deployed. A generated test result must identify the target and identity used. A native release test profile is product configuration; the catalog's configuration recipes are authored guidance rather than another AWS resource.

![Team review of the resulting evidence](../assets/diagrams/teaching-devops-review.svg)

The shared [operational-review case](../catalog/UC-G01.html) consumes verified health reports, deployment records, incident patterns and prevention proposals. The team decides priorities, accountable owners and closure criteria. Sending an output to a Security or FinOps inquiry requires a separately scoped request and authorization; this documentation does not assert a shared runtime among the services.

After this overview, use the ten capability chapters as a reference: workspace organization, definition, knowledge, invocation, integrations, networking, execution control, managed workflows, outputs and administration. They answer configuration questions raised by the workflows rather than substituting a taxonomy for the learning sequence.''')},
'security':{
'S-90':('What AWS Security Agent executes',r'''AWS Security Agent performs application-security assessments using the sources, criteria, target access and assessment settings configured for the selected work. The public operating model exposes code review, design review, threat modeling and penetration testing, together with finding and remediation operations. It does not expose the DevOps managed-agent roster or an equivalent customer-defined prompt/tool/skill composition. [SS701] [SS702]

![Security assessment composition](../assets/diagrams/teaching-security-agent.svg)

Begin with the question and its evidence. Reviewing a proposed design uses supplied documents and applicable requirements. A source review identifies a code revision. A dynamic assessment needs a deployed target and permitted identity. These inputs cannot be substituted merely because every operation returns findings. Assessment settings, criteria, application context, access and results therefore occupy distinct positions in the diagram. [SS701]

The figure is an explanatory view, not a claim that each box is a separately creatable resource. The approved resource model defines the actual application and shared configuration objects.'''),
'S-91':('How assessment, remediation and verification are coordinated',r'''The useful coordination model is the lineage of work: an assessment produces a finding; a remediation operation can propose a code change; the application team reviews and deploys it; a subsequent verification evaluates the deployed result. The proposal, deployment and verification record remain different objects. [SS701] [SS703]

![Assessment and result lineage](../assets/diagrams/teaching-security-coordination.svg)

These arrows explain responsibilities and evidence handoff. They do not invent named internal peer agents or promise an automatic end-to-end repair loop. Revalidation repeats validation for selected existing findings and retains its relationship to the earlier finding. It is not a new broad discovery run. The original evidence remains necessary to interpret the later result. [SS703]

One-off design reviews and reusable code-review, threat-model or penetration-test configurations also have different execution lifecycles. The detailed procedure must use the lifecycle of the actual assessment rather than a generic instruction to rerun every review. [SS702]'''),
'S-92':('Application Agent Spaces and shared assessment criteria',r'''An Agent Space represents an application or project. It selects application sources, user assignments, assessment configuration and result records. Some facilities, including shared requirement packs and provider registration, have broader scope and are referenced by application work. The diagram's selected-criteria box does not imply that the application owns the shared pack. [SS702]

![Application scope and referenced criteria](../assets/diagrams/teaching-security-space.svg)

Repository authorization, selecting the repository for an application, deciding how it is used, reaching a test endpoint and resolving a test credential are separate configuration decisions. A source registration is not permission to test every deployed application, and retrieving a secret is not proof of successful login as the expected role. The detailed access and authentication chapters explain those paths. [SS701] [SS702]'''),
'S-93':('Assessment and finding-resolution workflows',r'''The teaching sequence follows a complete assessment-and-resolution cycle before introducing less frequent configuration details. This is an editorial priority for development and security teams, not an AWS ranking. All approved cases retain their definitions.

![Assessment inputs, access and outputs](../assets/diagrams/teaching-security-assessment.svg)

Start with [assessing a running application](../catalog/UC-S01.html) or [reviewing source code](../catalog/UC-S02.html). The input contract specifies the target or revision, scope, criteria and authorized effects. Public/private connectivity and authentication are variants of the assessment, not new agent types. Interpret findings within the surface that was actually reachable. [SS701]

![Finding-to-verification path](../assets/diagrams/teaching-security-repair.svg)

Then [triage findings](../catalog/UC-S05.html), [prepare a remediation proposal](../catalog/UC-S06.html), and [revalidate after repair](../catalog/UC-S07.html). Record the finding identity, proposed revision, deployed revision and test identity. A finding disposition or merged pull request alone does not establish that the target was repaired. [SS701] [SS703]

Earlier feedback is addressed through [design review](../catalog/UC-S03.html), [threat modeling](../catalog/UC-S04.html), and [security-requirement consolidation](../catalog/UC-S08.html). These use different subjects and lifecycles. Requirement maintenance supplies criteria; application context supplies evidence; retained login procedures and eligible finding personalization supply narrowly scoped reuse rather than universal cross-run memory. S-M03, S-M02 and S-13 explain the respective mechanisms. [SS702]

The capability chapters below retain the detailed configuration procedures and product-specific constraints. The supplied S-U01 exercise traces a finding through a proposed and deployed repair without asserting that a live assessment was performed.''')},
'finops':{
'F-90':('An analysis request, its context, and the agent execution',r'''AWS FinOps Agent answers cost-management questions using authorized AWS source services and organization-specific context. A question specifies a scope and analysis basis. Source services provide cost, anomaly or recommendation evidence. Uploaded files and persistent memory supply mappings, preferences and other context. The agent interprets the available material and produces an answer or artifact. [FS701] [FS703]

![FinOps analysis composition](../assets/diagrams/teaching-finops-agent.svg)

This is not the DevOps custom-agent definition model. Uploaded instructions and templates are context files, not a native SKILL.md registry. A task instruction specifies work, not another agent instance. Recommendation estimates retain the provenance of the upstream source; analysis does not itself authorize an infrastructure change or financial commitment. [FS701]

Read the picture from the question, through the authorized data path, to the result. The contextual inputs explain how organizational terms affect the answer, but they do not replace the source query or its dates, filters and cost basis.'''),
'F-91':('How conversations and automations coordinate tasks',r'''Ordinary requests can be answered directly in a conversation. When the user explicitly asks for a task, the service creates queued work. A scheduled or supported event-based automation creates new tasks when its condition matches. These are execution arrangements within the configured instance, not a roster of cooperating DevOps-style agents. [FS702]

![Direct interaction and task creation](../assets/diagrams/teaching-finops-coordination.svg)

Inspect the automation condition, task identity, analysis result and destination effect separately. A matching anomaly event does not establish that the task completed, and completed analysis does not establish successful publication. Stopping future task creation, cancelling current work and removing retained data have different consequences. [FS702]

The publication path also changes the control question. Jira actions started interactively or from an on-demand task request approval; scheduled or event-driven actions rely on authorization established during automation setup. Slack posting has no per-message approval prompt. There is no single universal approval switch for every effect. [FS702]'''),
'F-92':('Agent-instance scope and source access',r'''The instance groups its configured access, context, conversations, tasks and connections. Data-source permissions, operator access and publication destinations are separate controls. The detailed F-01, F-02 and F-05 sections define their resource identities and setup procedures. [FS701] [FS702]

![FinOps instance and its connections](../assets/diagrams/teaching-finops-space.svg)

Uploaded context files, retained memory and a conversation summary are different representations. Files are maintained through their workspace; conversational corrections update memory; compaction summarizes older conversation content. Applying one control does not update or delete all other copies of a fact. These distinctions matter when a report uses an outdated ownership mapping or format preference. [FS703]

The diagram shows the source-access and output paths without treating the instance as the underlying billing system or a shared memory across AWS agentic services. A verified source result remains necessary even when the organizational context is correctly configured.'''),
'F-93':('Cost-analysis, reporting and optimization workflows',r'''For the technical audience, the sequence begins with a reproducible cost inquiry, then anomaly investigation and reporting, before planning and optimization decisions. This teaching order is editorial; the approved cases remain separate.

![Source-backed analysis path](../assets/diagrams/teaching-finops-analysis.svg)

[Historical cost and usage analysis](../catalog/UC-F01.html) establishes accounts, interval, currency, metric, grouping and filters. [Anomaly investigation](../catalog/UC-F05.html) adds a reason to inspect a deviation and, when available, corroborating operational evidence. Numerical contribution, temporal correlation and an established cause are different conclusions. [FS701] [FS702]

![Reporting and publication path](../assets/diagrams/teaching-finops-reporting.svg)

[Periodic reporting](../catalog/UC-F04.html) reuses the query basis and adds a reviewed format, optional recurrence and an explicit destination. A report artifact can originate from a conversation or task; its content and publication outcome should be inspected separately. F-04 and F-M06 explain those controls. [FS702]

[Forecast review](../catalog/UC-F02.html) concerns projected expenditure; [commitment-coverage review](../catalog/UC-F03.html) concerns covered eligible usage. Do not merge their horizons or denominators. [Optimization prioritization](../catalog/UC-F06.html) reviews source recommendations and constraints. [Outcome measurement](../catalog/UC-F07.html) examines a comparable period after an implemented change. An estimate is not the measured result. [FS701]

![Recommendation and team-decision path](../assets/diagrams/teaching-finops-optimization.svg)

The shared [operational-review case](../catalog/UC-G01.html) assembles reconciled reports, unresolved anomalies, original recommendation assumptions and measured outcomes into decisions owned by the team. It does not introduce native cross-service orchestration. The detailed capability chapters provide the access, context, task, output and retention procedures underlying this sequence.''')},
'architecture':{
'A-90':('From one agent execution to product-specific workflows',r'''Begin with one executor working on one scoped request. It uses applicable instructions and contextual information, calls permitted operations, and produces observations and a result. A saved configuration, a particular execution, the workspace containing it and the accepted engineering outcome are different concepts. The diagram is an explanatory cycle, not an assertion of shared implementation internals. [AS701] [AS702] [AS703]

![Agent execution and evidence cycle](../assets/diagrams/agent-execution.svg)

The product terms must then be specialized. DevOps exposes managed roles and custom-agent definitions with selected tools and context. Security exposes assessment-specific settings, inputs, runs and results. FinOps exposes direct conversation, tasks and automations using authorized source data and organizational context. Importing DevOps skill or custom-agent terminology into the other products would obscure their actual configuration model. [AS701] [AS702] [AS703]

Use the approved entity model to keep those concepts distinct, not as a list of headings to reproduce mechanically. The product teaching sequences introduce the worker, expand to coordination and access scope, and then follow the existing use cases through the same fixed-position diagrams. The ten capability dimensions remain the detailed reference organization.'''),
'A-91':('Coordination within a service and handoff between services',r'''Coordination has different meanings at different scopes. Within DevOps incident work, managed responsibilities contribute to an investigation and retained knowledge can inform later work. Within Security, assessment, finding, repair and verification records form an evidence lineage. Within FinOps, requests and automations create work through documented conversation and task paths. Similar words do not establish an identical native agent graph. [AS701] [AS702] [AS703]

![Explicit evidence transfer between independently scoped work](../assets/diagrams/shared-handoff.svg)

Across services, this collection defines a team-managed handoff. An incident result may motivate a security assessment or cost inquiry, but the receiving work needs its own target, evidence, identity, authorization and completion criteria. Transfer source and execution identifiers, relevant observations, unresolved questions and a responsible owner. Do not transfer credentials or treat a generated summary as approval.

This preserves the shared operational-review use case without claiming a built-in cross-service orchestrator. The four-minute tabletop asks participants to define three independently testable questions from one event rather than assume one shared cause.''')}
}

chapters=copy.deepcopy(CHAPTERS)
types=dict(TYPES)
for product,additions in PROSE.items():
    path=ROOT/f'guides/{product}.md'
    original=parse_source(path.read_text())
    for sid,(title,body) in additions.items():
        if sid in original['sections']:raise ValueError('New teaching section collides: '+sid)
        original['sections'][sid]={'title':title,'body':body}
        types[sid]='overview'
    prefix=course.DECKS[product]['prefix']
    first={'slug':'agent-overview','title':'The agent and its operating context','purpose':'Start with one execution, then add coordinated responsibilities and the surrounding access scope. The same diagram is reused in the workflow walkthroughs.','sections':[prefix+'-90',prefix+'-91'] if product=='architecture' else [prefix+'-90',prefix+'-91',prefix+'-92'],'teaching':True}
    extra=[]
    if product!='architecture':
        extra=[{'slug':'workflow-overview','title':'Essential operational workflows','purpose':'Follow the existing use cases through inputs, context, authorized operations, outputs and the decisions that require an engineer. Teaching priority is an editorial choice, not an AWS ranking.','sections':[s for s in additions if int(s.split('-')[-1])>=93],'teaching':True}]
    chapters[product]=[first,*extra,*chapters[product]]
    old_intro=original['intro']
    # Keep the product-specific source-grounded introduction but make its reading
    # order explicit; do not change any frozen catalog narrative.
    old_intro=re.sub(r'The chapters distinguish ten capability dimensions:[\s\S]*?The separate use-case catalog applies those facilities to operational objectives\.',
       'Begin with the agent and its operating context, then trace the operational workflows. The ten capability dimensions that follow provide the configuration reference. The separate use-case catalog retains the approved objectives and completion criteria.',old_intro,count=1)
    if product!='devops':
        old_intro += '\n\nStart with the agent overview and workflow walkthroughs. Use the subsequent capability chapters for detailed setup, lifecycle behavior and troubleshooting. The use-case catalog remains separate and unchanged.'
    lines=[old_intro.strip(),'']
    for number,c in enumerate(chapters[product],1):
        lines += [f'## {number:02d}. {c["title"]}','',c['purpose'],'']
        for sid in c['sections']:
            sec=original['sections'][sid]
            lines += [f'### {sid} — {sec["title"]}','',sec['body'].strip(),'']
    refs=original['refs']|SOURCES[product]
    lines += [f'[{r}]: {url}' for r,url in refs.items()]
    path.write_text('\n'.join(lines).rstrip()+'\n')

# Replace, rather than retain, the old curriculum. One maintained slide outline.
(HERE/'presentation.py').write_text((HERE/'course.py').read_text())
(HERE/'course.py').unlink()
structure='"""Capability reference chapters and agent-first teaching order."""\n'
structure += "REVISION='2026-10-23-educational-sequence'\nBASELINE="+repr(RESOURCE_BASELINE)+'\n'
structure += 'CHAPTERS='+pprint.pformat(chapters,sort_dicts=False,width=110)+'\n'
structure += 'DECK_CHAPTERS='+pprint.pformat(course.DECK_CHAPTERS,sort_dicts=False,width=110)+'\n'
structure += 'TYPES='+repr(types)+'\nLABELS='+repr(LABELS)+'\n'
structure += 'def section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n'
(HERE/'structure.py').write_text(structure)


def patch(path,old,new):
    p=HERE/path;s=p.read_text()
    if old not in s:raise ValueError('Expected source not found in '+str(path)+': '+old[:90])
    p.write_text(s.replace(old,new,1))

patch('diagrams.py','    for key,(title,description,sections,dot) in DIAGRAMS.items():',
'''    for key,(title,description,sections,dot) in DIAGRAMS.items():
        if key.startswith('teaching-'):
            from teaching_diagrams import build_one
            build_one(key, out)
            continue''')
patch('diagrams.py',"if __name__=='__main__':", "from teaching_diagrams import DIAGRAMS as TEACHING_DIAGRAMS\nDIAGRAMS.update(TEACHING_DIAGRAMS)\n\nif __name__=='__main__':")
patch('build.py',"    if s['kind']=='diagram':return figure(s['diagram'],prefix)",
'''    if s['kind']=='diagram':
        explanation = '<ol class="diagram-steps">'+''.join('<li>'+esc(x)+'</li>' for x in s.get('explain',[]))+'</ol>' if s.get('explain') else ''
        return figure(s['diagram'],prefix)+explanation''')
patch('build.py',"    title,description,refs,_=DIAGRAMS[key]\n    return", "    title,description,refs,_=DIAGRAMS[key]\n    return")
# Figure attribution: full-size diagrams remain accessible with one direct link.
patch('build.py','Logical model. Entity ownership and relationship qualifications are defined in the resource register.',
 'Logical teaching or resource view; ownership colors and qualified native relationships are defined in the resource model.')
patch('exposition_check.py',"        chapters=CHAPTERS[product]", "        chapters=[c for c in CHAPTERS[product] if not c.get('teaching')]")
patch('exposition_check.py',"'basis':'Supplied ten-part DevOps capability outline, adapted to documented facilities of the other two services.'", "'basis':'Supplied ten-part capability reference retained after the agent-first teaching overview; product-specific facilities remain distinct.'")
# Stop first-page introductions from remaining above every later chapter.
p=HERE/'reading.js';js=p.read_text()
# Chapter code is left intact; a separate observer only adjusts the introduction.
js += '''\n(() => { if(document.body.dataset.reader !== 'guide') return;
 const intro=document.querySelector('.guide-introduction');
 const first=document.querySelector('[data-reader-chapter]');
 if(!intro || !first) return;
 const update=()=>{intro.hidden=first.hidden && !document.getElementById('read-all').checked;};
 new MutationObserver(update).observe(first,{attributes:true,attributeFilter:['hidden']});
 addEventListener('afterprint',update);update();})();\n'''
p.write_text(js)
css='''\n/* Teaching diagrams keep a stable coordinate system; labels remain searchable in SVG. */
.diagram-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:12px 0;padding-left:25px;font-size:17px;line-height:1.35}
.diagram-steps li{padding-right:10px}.slide:has([data-layout="teaching-fixed-v1"]) .diagram{margin:6px 0}
.slide:has([data-layout="teaching-fixed-v1"]) .diagram-viewport{max-width:920px;margin:auto}
.slide:has([data-layout="teaching-fixed-v1"]) .diagram figcaption{font-size:12px;line-height:1.3;margin:3px 0}
@media(max-width:700px){.diagram-steps{display:block;font-size:16px}.diagram-steps li{margin:8px 0}}
@media print{.guide-introduction[hidden]{display:block!important}.diagram-steps{font-size:12px}}
'''
(HERE/'styles.css').write_text((HERE/'styles.css').read_text()+css)
(HERE/'reading.css').write_text((HERE/'reading.css').read_text()+'\n@media print{.guide-introduction[hidden]{display:block!important}}\n')

# Refine fixed-view semantics and prevent long labels from crossing their boxes.
p=HERE/'teaching_diagrams.py';s=p.read_text()
s=s.replace("'sources': (470, 650, 350, 86)","'sources': (470, 650, 350, 110)")
s=s.replace('viewBox="0 0 1400 790"','viewBox="0 0 1400 825"').replace('y="770"','y="810"')
s=s.replace("'Behavioral guidance', 'Managed AGENTS.md or custom system prompt'","'Instructions / prompt', 'Managed AGENTS.md or custom system prompt'")
s=s.replace("'Procedures', 'Applicable or explicitly assigned skills'","'Skills', 'Applicable or explicitly assigned procedures'")
s=s.replace("'Retained knowledge', 'Relevant available memory stores and entries'","'Memory stores', 'Relevant available entries; informational context'")
s=s.replace("'Learning / feedback', 'Produce and correct retained context'","'Knowledge production', 'Learning runs and corrective feedback'")
s=s.replace("'Selected criteria', 'Shared requirement packs applied to eligible reviews'","'Requirement references', 'Shared packs applied to eligible reviews'")
s=s.replace("'Requested work', 'Query basis and task or automation instructions'","'Request / task instructions', 'Query basis and requested analysis'")
s=s.replace("'Uploaded context files', 'Ownership mappings, instructions and report templates'","'Context files', 'Ownership mappings, instructions and report templates'")
s=s.replace("        out+=['<path class=\"edge-soft\" data-edge=\"result-learning\" d=\"M1275 396 V603 H1118 V526 H1110\"/>',\n              '<path class=\"edge-soft\" data-edge=\"learning-knowledge\" d=\"M995 470 V430 H1122 V220 H980 V200\"/>']",'''        out.append('<path class="edge-soft" data-edge="result-learning" d="M1275 396 V603 H1118 V526 H1110"/>')
        if product == 'security':
            out.append('<path class="edge-soft" data-edge="reuse-execution" d="M995 470 V400"/>')
        else:
            out.append('<path class="edge-soft" data-edge="learning-knowledge" d="M995 470 V430 H1122 V220 H980 V200"/>')''')
old='''        out.append(f'<text class="label" x="{x+12}" y="{y+45}">{escape(head)}</text>')
        wrap=max(19,int((w-24)/9.4))
        for i,line in enumerate(textwrap.wrap(body,width=wrap)):
            out.append(f'<text class="detail" x="{x+12}" y="{y+69+i*21}">{escape(line)}</text>')'''
new='''        head_lines=textwrap.wrap(head,width=max(18,int((w-24)/10.6)))
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
                out.append(f'<text x="{px+8}" y="{y+104}" font-size="17">{role}</text>')'''
if old not in s:raise ValueError('Teaching SVG text renderer changed')
s=s.replace(old,new)
s=s.replace("line='Incident roles: Triage | RCA | Mitigation | UI. Learning runs separately; not every role is a mandatory step.'", "line='Roles contribute to an investigation; this is not a mandatory sequence or an internal RPC diagram.'")
p.write_text(s)

# Guide pointers in teaching slides resolve to the correct overview paragraph.
# Product workflow map remains D-93/S-93/F-93; detailed refs carry the exact procedure.
for name,data in before.items():
    if (ROOT/f'catalog/{name}.json').read_bytes()!=data:raise AssertionError('Frozen record changed: '+name)

review={'revision':'2026-10-23-educational-sequence','baseline':BASELINE,
 'requested_change':'Definition of an agent, coordinated responsibilities and enclosing space before prioritized workflows; stable diagram reused through the flows.',
 'source_basis':'User-supplied capability outline retained for detailed chapters; official DevOps managed/custom/space/memory/incident guidance rechecked; Security and FinOps keep their native resource and execution models.',
 'corrections':['The opening no longer starts with asset identifiers.','Teaching order is distinct from the ten-dimension reference taxonomy.','Same product diagram keeps node positions and ownership across overlays.','Managed incident responsibilities are not presented as a configurable internal call graph.','Security record lineage and FinOps task creation are not portrayed as DevOps-style peer agents.','Each workflow identifies its input, source path, output and independent acceptance boundary.','Model, cases and dependencies remain frozen.'],
 'reviewed_official_urls':sorted({url for refs in SOURCES.values() for url in refs.values()}),
 'retrieval_qualification':'Direct and indexed representations of the DevOps custom/managed documentation differ. Attachment terminology and indexed full custom/managed content support explicit memory attachment and managed roles; no internal ranking or routing algorithm is inferred.',
 'source_changes':'Only teaching exposition, presentation sequence, diagram overlays and reader controls change; retained guide sections retain their previous source review dates.',
 'frozen_sha256':{name:hashlib.sha256(data).hexdigest() for name,data in before.items()},
 'priority_basis':'Audience-based editorial order, not AWS ranking.',
 'live_aws_execution':False}
(ROOT/'qa/educational-review.json').write_text(json.dumps(review,indent=2)+'\n')
with (ROOT/'CHANGELOG.md').open('a') as f:f.write('\n## 2026-10-23 — Agent-first educational sequence\n\nTeach the configured worker, service coordination and access scope before operational workflows. Reuse fixed-layout product diagrams. Retain the approved model and all use cases. Replace the previous presentation outline rather than adding another course.\n')
# The full reader and model suites remain. Add the educational invariants separately.
patch('check.py','from exposition_check import validate as validate_exposition','from exposition_check import validate as validate_exposition\nfrom teaching_check import validate as validate_teaching')
# Insert a standalone call before the existing result is written; do not bypass any check.
patch('check.py',"    write('qa/checks.json',json.dumps(results,indent=2))", "    teaching_result=validate_teaching(guides,browser=browser)\n    errors.extend(teaching_result['errors'])\n    results['educational_review']=teaching_result\n    write('qa/checks.json',json.dumps(results,indent=2))")
Path(__file__).unlink()
print('Authored educational sequence applied; frozen model and use-case sources unchanged.')
