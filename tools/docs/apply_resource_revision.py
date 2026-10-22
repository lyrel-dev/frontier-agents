#!/usr/bin/env python3
"""One-time plain-text source migration; removes itself after applying changes."""
from __future__ import annotations
import copy
import json
import re
from pathlib import Path
from pprint import pformat
import build as renderer
from structure import CHAPTERS, DECK_CHAPTERS, TYPES, LABELS
from presentation import DECKS

ROOT=Path(__file__).resolve().parents[2]
REVISION='2026-10-22-product-resource-models'
BASELINE='cd65b98e04e20e7a4bcf59165db7f98315417964'
guides=renderer.load_guides()
model_path=ROOT/'catalog/resource-models.json'
model=json.loads(model_path.read_text())

# Refine collectively named objects before publishing the entity dictionary.
d=model['products']['devops'];s=model['products']['security'];f=model['products']['finops']
def entity(p,ident):return next(e for e in p['entities'] if e['id']==ident)
def relationship(p,ident):return next(r for r in p['relationships'] if r['id']==ident)
def new_entity(p,ident,name,kind,identity,scope,meaning,sources,owner='aws'):
    p['entities'].append(dict(id=ident,name=name,owner=owner,kind=kind,identity=identity,scope=scope,meaning=meaning,sources=sources))
def new_rel(p,ident,a,b,verb,targets,reverse,basis,note,sources):
    p['relationships'].append(dict(id=ident,**{'from':a,'to':b},verb=verb,targets=targets,sources_per_target=reverse,basis=basis,note=note,sources=sources))
model['sources']['DS63']={'url':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html','section':'Platform-owned managed agents; Learning history and triggers versus incident roles','basis':'Retrieved current official indexed text; direct cached URL was unavailable'}
model['sources']['DS59']['basis']='Retrieved official HTML; evaluation and recommendation relationship reviewed'
model['sources']['SS58']['basis']='Retrieved official indexed text; project selection and finding publication reviewed'
entity(d,'D-Signal')['name']='Incident signal'
new_entity(d,'D-Managed','Managed agent role','platform-owned component','Agent type shown in Managed agents','One Agent Space','Platform-owned role; it is not a user-created custom_agent asset. Incident roles participate in investigations. Only Learning exposes its own run history and platform-owned triggers.',['DS63'])
new_entity(d,'D-LearningRun','Learning execution','execution record','Run selected in the Learning history','Managed Learning role','Observable synthesis and refresh execution; do not infer a separately runnable record for every managed incident role.',['DS63','DS55'])
new_rel(d,'DR24','D-Space','D-Managed','exposes managed roles','?','1','documented','Roles are platform-owned, not custom-agent definitions.',['DS63'])
new_rel(d,'DR25','D-Managed','D-LearningRun','Learning role has history','0..*','1','documented','This edge applies to Learning only; other managed roles execute within investigations.',['DS63'])
new_rel(d,'DR26','D-LearningRun','D-Memory','synthesizes retained context','?','?','documented','Completion and a resulting version must be inspected; this is not customer-controlled model training.',['DS63','DS55'])
d['feature_bindings']['FT-D-TOPOLOGY'].extend(['D-Managed','D-LearningRun'])
d['feature_bindings']['FT-D-MEMORY'].append('D-LearningRun')
entity(s,'S-CodeConfig').update(name='Full-code review configuration',meaning='Reusable selection of repositories or S3 sources for full scans; repository-event review settings are modeled separately.')
new_entity(s,'S-CodeSettings','Repository code-review settings','service configuration','Settings on the connected repository','Agent Space source connection','Controls eligible change review, selected analysis modes and comments. These settings are not the full-scan configuration.',['SS50'])
new_rel(s,'SR25','S-CodeSettings','S-CodeRun','enables change-triggered reviews','0..*','?','documented','Provider-specific events and source revision identify the change-review path.',['SS50'])
relationship(s,'SR15').update(verb='starts full-source scans',note='This relationship describes full scans. Repository-event reviews originate through their own connected-source settings.')
s['feature_bindings']['FT-S-CODE'].append('S-CodeSettings')
entity(s,'S-Remediation').update(name='Remediation attempt',kind='operation record',meaning='Finding-linked attempt to produce a code proposal; it is not the repository settings or the resulting deployment.')
new_entity(s,'S-RemediationSettings','Remediation repository settings','service configuration','Eligible source repositories and feature settings','Application Agent Space','Determines where supported fix proposals can be created. Settings alone do not represent a remediation attempt.',['SS50','SS55'])
new_rel(s,'SR26','S-RemediationSettings','S-Remediation','permits proposal generation','0..*','?','documented','Provider eligibility and the accepted finding remain required.',['SS55'])
s['feature_bindings']['FT-S-FIX'].append('S-RemediationSettings')
new_entity(s,'S-CodeFinding','Code-review finding','result record','Review identity, source revision and finding location','Source-code review','Static-analysis result with source evidence. Penetration-test revalidation is not inferred for this result type.',['SS50'])
new_rel(s,'SR27','S-CodeRun','S-CodeFinding','produces source findings','0..*','1','documented','Keep source-review results distinct from running-application findings.',['SS50'])
s['feature_bindings']['FT-S-FINDINGS'].append('S-CodeFinding')
entity(f,'F-Source').update(owner='documentation',kind='normalized evidence family',meaning='Our grouping of distinct AWS-source results: cost query, forecast, coverage, anomaly, recommendation and change event. It is not one FinOps resource type or a shared evidence API.')
model_path.write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')

TEXT={}
def section(key,sid,title,body):
    TEXT[(key,sid)]=(title,body.strip())

section('devops','D-01','Agent Space, configuration and execution',r'''
AWS DevOps Agent uses an Agent Space to scope operational work. The space brings together the AWS account access, selected external services and retained context needed to investigate an application. It is not an individual investigation and it is not the running application being observed. A new investigation creates a record of work within that configured environment; it does not create another Agent Space. [DS50] [DS56]

The resource model has three layers. Provider registration establishes an integration and its authentication. Association then selects how that registered service is used by an Agent Space. Executions use the available operations and applicable context to collect evidence or produce a result. A connection error belongs to the first two layers; an unsupported diagnosis belongs to the execution and evidence layer. These faults require different corrective actions. [DS51] [DS62]

![DevOps Agent scope, providers and execution](../assets/diagrams/er-devops-scope.svg)

Green boxes are AWS-defined objects or documented concepts. The label beneath each name distinguishes an independently addressable resource from a configuration member or derived view. Orange boxes identify external source systems. The blue concepts used by this collection, such as a use case or implementation profile, organize the explanation but are not resources created in the service. The complete ownership convention is described in the shared guide A-10.

Managed and custom agents have different administrative models. Managed roles belong to the platform; the incident roles operate as part of an investigation. Learning has its own history and platform-owned triggers. A custom agent is instead a saved definition whose prompt, selected tools, skills and memory access the team configures. Running that definition creates an invocation with a separate status and trajectory. [DS63] [DS53] [DS54]

These distinctions connect the service to the approved outcomes. Incident triage and investigation use the built-in operational path. A native health inquiry can use Chat. A repeatable report with a prescribed structure may use a custom definition and optional trigger. A mitigation proposal is an output; carrying out a directed action introduces additional authorization. Release-readiness review and deployed-application testing are separate preview paths with different subjects and effects. [DS56] [DS57] [DS60] [DS61]

The following section explains identities and relationships. Subsequent chapters follow the same model through integration setup, knowledge production, execution and the approved use cases. The [resource index](../catalog/resource-models.html#model-devops) provides the entity dictionary and individually qualified relationship multiplicities; it is not an inventory of resources in your account.
''')
section('devops','D-13','Configuration identities and knowledge relationships',r'''
A resource name is useful to a person, but it does not necessarily identify a valid relationship in an API. An Agent Space has an `agentSpaceId`. A service association records the space, `serviceId` and `associationId`, together with provider-specific configuration. Registering a provider and associating it are therefore different operations. The association API also documents replacement of an existing association of the same service; adding an association is not an unrestricted append operation. [DS51]

The asset model provides another identity layer. A custom-agent definition, skill, instruction file, memory store or memory entry can be represented through its documented asset type. References between these assets use the expected identifiers. In particular, the `skills` and `memory_stores` arrays of a custom-agent definition refer to existing asset IDs in the same Agent Space, not display names. A memory entry identifies its parent store. These are concrete relationships that can be inspected and configured, rather than abstract claims that an agent has access to all organizational knowledge. [DS52]

![Stored knowledge and configuration references](../assets/diagrams/er-devops-knowledge.svg)

Knowledge has both a production path and a use path. Managed learning synthesizes environment or investigation information into retained context. A later execution selects relevant available stores and entries rather than receiving every file indiscriminately. Versions describe changes to an entry; active state and custom-agent attachment describe availability. None of those observations alone proves that a particular investigation used the information correctly. D-M08 describes consolidation, D-M01 retrieval, and D-M07 access and lifecycle in detail. [DS55] [DS63]

A custom definition begins without attached stores. An attached managed store is read-only to that custom agent, while attached custom stores support the documented write behavior. Managed-agent knowledge access and custom-agent attachment should consequently not be represented by one universal permission rule. Standing instructions and applicable skills are other kinds of context: they are not memory entries and do not grant source-system permissions. [DS53] [DS55]

| Object or relationship | What changes | What remains a separate concern |
|---|---|---|
| Provider association | Selected provider-specific configuration | Authentication, target routing and actual tool result |
| Custom-agent definition | Prompt and references to available tools, skills and stores | Each invocation and its output |
| Memory entry version | Retained content | Activation, attachment and observed retrieval |
| Learning execution | A particular knowledge-production run | Correctness and freshness of the resulting representation |
| Custom trigger | Future start conditions | Existing invocation cancellation and observation window |
| Directed-action approval | Authorization for the requested operation and target | Permission ceiling, actual resource state and service recovery |

The table summarizes different lifecycles; it is not an instruction to apply the same update or delete operation to every object. Custom-agent execution and cancellation are documented under D-07. Directed actions have a separate control sequence under D-M06. Topology is a derived representation of discovered and inferred relationships; its visible boundary is not the full IAM access boundary. [DS54] [DS57] [DS58]

In the diagrams, `0..*` means an optional repeated logical association, not an unlimited service quota. `?` means that the reviewed documentation does not establish exact multiplicity. Dashed edges mark logical or editorial associations rather than asserted service foreign keys. Each qualification and its supporting source is retained in the [relationship register](../catalog/resource-models.html#model-devops).
''')
section('devops','D-14','Incident and reporting use cases in the resource model',r'''
The approved incident-investigation case begins with an operational objective: explain the current incident using current evidence. Its first objects are the incident signal, any triage decision and the resulting investigation. A signal may join existing work or be skipped; an investigation can also begin manually. The signal and investigation must therefore remain separate records. A correction to routing changes their relationship, while steering changes the investigation analysis. [DS56]

![Incident records and action authorization](../assets/diagrams/er-devops-incidents.svg)

For [UC-D02, investigate a service incident](../catalog/index.html#UC-D02), evidence retrieval traverses the space's selected source operations. Historical context is optional: the investigation may examine a relevant memory entry, but its conclusion still depends on observations from the current interval. After completion, verified corrective feedback can record what the original conclusion got wrong. The feedback operation and later retained corrective context are connected, but the public material does not establish a universal one-feedback-to-one-memory cardinality. [DS55] [DS56]

[UC-D06, service health and trends](../catalog/index.html#UC-D06), uses the same source-access layer for a different result. A native snapshot may be answered in Chat. The configured reporting profile instead uses a custom definition, selected telemetry tools and any required service mappings. Its invocation records the actual reads and failures. A trigger adds recurring starts without redefining the observation period or turning the result into continuous monitoring. [DS53] [DS54] [DS61]

| Approved outcome | Objects to configure or inspect | Record used to evaluate completion |
|---|---|---|
| Investigate an incident | Space, source association, signal, investigation, applicable memory | Current observations, hypotheses and conclusion |
| Report service health | Chat or custom definition, selected tools, optional store and trigger | Observation window, source measurements, failed reads and report |
| Document topology | Discovery inputs, learning execution, derived topology and knowledge version | Owner-reviewed relationships and unresolved edges |
| Consolidate SOPs | Reviewed procedure, skill asset, applicability and selected tools | Matching and nonmatching procedure tests |
| Execute approved mitigation | Opt-in, role binding, classified tool and exact approval | Action attribution, resulting state and recovery measurements |

The table is a map of the existing cases, not additional native functionality. In particular, the engineering team owns SOP reconciliation and architecture-document acceptance. The service supplies the documented skills, discovery and execution facilities those processes use. A report does not automatically publish itself to an external destination, and a mitigation recommendation does not authorize a change. [DS52] [DS57] [DS58]

To troubleshoot a case, locate the first missing relationship. A registered provider with no usable association is different from an invocation that queried the wrong interval. A stored memory with no attachment is different from a retrieved entry that conflicts with current data. The detailed case dependencies identify whether to stop, continue with a qualification or transfer work to an engineer. Those failure decisions are authored operating guidance; they are not an additional AWS workflow engine.
''')

section('security','S-01','Shared configuration, Agent Spaces and assessments',r'''
AWS Security Agent organizes work around an application Agent Space. The space groups application sources, assessment settings and user assignments. Some configuration is shared above that boundary, including registered integrations and security requirements. The guide calls this tenant or organizational scope; this model does not turn that phrase into an AWS Organizations resource or infer automatic cross-account policy propagation. [SS50]

A source is connected in stages. The administrator authorizes an integration; the application space selects repositories or documentation; capability settings determine how those sources are used. One repository can supply several spaces without making their assessment settings identical. Source access, permission to submit a fix and permission to publish a finding are separate relationships. [SS50] [SS51]

![Shared configuration and application scope](../assets/diagrams/er-security-scope.svg)

The assessment type determines the execution model. Penetration testing and threat modeling use reusable configurations with separate runs. Full-code scans also have reusable configuration, while repository-event review has provider-specific settings. Design review is a one-off assessment; cloning creates a new review. A generic Configuration → Run arrow is therefore an explanatory starting point, not a universal schema for every Security Agent function. [SS50]

Application context, criteria and access play different roles. Code and documents explain the system. Requirements define what eligible design and code reviews should evaluate. Target rules and credentials define the reachable identity and boundary for a running-application assessment. A retained successful login procedure helps reuse authentication navigation; it is not evidence of a general incident-memory service. [SS52] [SS53] [SS56]

Green nodes below and in the resource index denote AWS-defined concepts; their subtitles distinguish reusable configuration, a run, a result and managed state. Orange denotes the actual repository, test application or external issue. Blue denotes our normalized associations and review structure, not service resources. This distinction becomes important when tracing one original finding through several revalidation jobs.

The next section explains the assessment-specific relationships. Later chapters configure sources and targets, examine authentication and criteria, and follow the existing assessment, remediation and verification use cases. The [product resource index](../catalog/resource-models.html#model-security) records entity identities and the evidence supporting each relationship.
''')
section('security','S-10','Assessment configurations, runs and result identities',r'''
A saved configuration answers what should be assessed. A run answers what happened during a particular execution. Keeping those identities separate prevents a later configuration change from being mistaken for a change to an earlier result. It also allows the same application to be assessed repeatedly while retaining the conditions of each run. This configuration-and-run relationship is documented for penetration tests, full-code scans and threat models, but not for one-off design reviews. [SS50] [SS57]

![Assessment configurations and executions](../assets/diagrams/er-security-assessments.svg)

For penetration testing, target rules and credential definitions belong to the saved assessment configuration. The execution then reaches the actual deployed application using the available identity. The repository revision used for source context and the revision deployed at the target may differ. A successful credential read is not confirmation that the target login succeeded, and a successful login is not proof that every protected route was exercised. The configuration and the observed conditions of the run must both be retained. [SS52] [SS56]

For code review, separate a full-scan configuration from connected-repository settings for change-triggered analysis. Both can produce source findings, but the event, selected revision and review mode determine what was analyzed. A source-code finding should not be treated as a penetration-test finding merely because both concern authorization. The selected-finding revalidation procedure described later applies to existing penetration-test findings, not to an invented universal finding subtype. [SS50] [SS54]

Requirements also have their own identity. Each requirement belongs to a pack, and enabled criteria inform future eligible reviews. A requirement is a reusable criterion, not the compliance result for every application. Updating a shared requirement does not retroactively rewrite earlier review findings. The criteria-generation workflow has its own replacement behavior, detailed in S-M04. [SS53]

| Subject | Maintained object | Execution or result | Correct interpretation of reuse |
|---|---|---|---|
| Running application | Penetration-test configuration | Independent run and findings | Repeat the configuration; record current target and identity each time |
| Full source | Code-review configuration | Source review and code findings | Repeat against an identified source revision |
| Repository change | Connected-repository review settings | Revision-specific review | Verify supported event and current revision |
| Proposed design | Individual design review | Findings from that assessment | Clone into a new review; do not claim rerun of the same object |
| System threats | Threat-model configuration | Run-specific overview and threats | Re-run with reviewed scope and sources |
| Organization criterion | Requirement pack and requirement | Result within an eligible review | Apply to later assessments, not retroactive result mutation |

These differences determine both operation and failure diagnosis. A draft configuration is not a completed assessment. A code-review comment is not a deployed repair. A threat-model output built around the wrong boundary needs corrected input, not merely a new label on its threats. The supported operations are detailed in S-04 and S-06; the table is their resource-model interpretation. [SS50] [SS57]

Some relationships deliberately remain unspecified. The public guidance documents retained login reuse but does not establish an independently editable skill resource for it. The diagrams use `?` where counts or parent fields are not documented, rather than inventing a universal resource schema. See the [qualified relationship register](../catalog/resource-models.html#model-security) before translating any diagram into implementation assumptions.
''')
section('security','S-11','Finding lineage from assessment to repair verification',r'''
The approved running-application assessment case ends with reviewed findings and known coverage, not with an automatically repaired application. An accepted finding may lead to a code proposal; that proposal must pass the engineering delivery process before its effect can be tested. The resource model keeps the original finding, remediation attempt, external change and later verification separate so the result can be traced through that sequence. [SS54] [SS55]

![Finding, repair and revalidation lineage](../assets/diagrams/er-security-lineage.svg)

In [UC-S01, assess a running application](../catalog/index.html#UC-S01), public or private reachability and authentication are configuration dimensions. They do not create four separate assessment objectives. The configuration selects the authorized surface, while the run records what was reached. Login Optimization can reuse a successful navigation procedure; the operator must still inspect the current role and reachability when interpreting coverage. [SS52] [SS56]

In [UC-S06, prepare a code-remediation proposal](../catalog/index.html#UC-S06), source and remediation settings determine where eligible proposal work can occur. The remediation attempt and its output are not the same object: an attempt may fail, and a produced patch or pull request remains an external engineering artifact. Its review, test and deployment records belong to the delivery process. The guide does not infer deployment authority from permission to create a proposal. [SS55]

In [UC-S07, revalidate a finding](../catalog/index.html#UC-S07), the operator selects one or more existing findings after deploying the repair to the original authorized environment. A separate job repeats the selected validation steps using current configuration and authentication. The original finding remains linked to the revalidation history. This is scoped retesting, not new broad vulnerability discovery. [SS54]

The blue Finding-to-revalidation result node is introduced by this documentation. It records the relationship between an original finding and a particular revalidation job, including the observed disposition and any incomplete evidence. It is useful because one finding can be retested repeatedly and one job can select several findings. The model does not claim that AWS exposes a separate API resource with that name. A pending or failed job may not yet have a conclusive result.

| Transition | Identity to preserve | Acceptance question |
|---|---|---|
| Configuration to assessment | Test configuration, run, target revision and role | Was the intended surface actually assessed? |
| Finding to proposal | Original finding and proposed source revision | Does the change address the evidenced issue without unrelated changes? |
| Proposal to deployment | Reviewed change and deployed revision | Did the accepted repair reach the test environment? |
| Finding to revalidation job | Original finding and new job | Were the selected validation steps reached under the intended identity? |
| Result to work tracking | Finding link and external issue key | Does the ticket describe the observed result rather than only completion status? |

These acceptance questions are authored engineering procedure. AWS documents the assessment, proposal and revalidation operations; the team decides whether the evidence is sufficient to accept the outcome. A linked Jira issue is another external record with its own audience and lifecycle. Removing the integration does not erase the previously published finding details. [SS54] [SS58]
''')

section('finops','F-01','Agent instance, access roles and retained state',r'''
AWS FinOps Agent presents an independent agent instance in its console and web application. The IAM documentation uses service-specific AgentSpace action names, including `finops-agent:CreateAgentSpace`, and an `agentspace` resource path in the ARN. This is a naming correspondence within FinOps Agent, not proof that the instance is the same resource type as a DevOps Agent Space. The service namespace and its documented operations remain part of the identity. [FS50] [FS51]

The instance groups its permissions, retained context, task queue and connections. Two roles have separate responsibilities: the agent data role accesses source services, and the operator role supports web-application operations. End users also need their own entry permissions. A user successfully opening the application does not establish that the data role can perform a particular source query. [FS50] [FS51]

![Instance access and integration connections](../assets/diagrams/er-finops-scope.svg)

Collaboration configuration has two levels. An integration registers Jira or Slack authorization at account level. An agent connection selects the destination for a particular instance. The destination remains an external Jira project or Slack channel, and a published issue or message is not stored solely inside the FinOps task record. Source access, destination membership and publication behavior therefore need separate review. [FS55] [FS56]

Work starts either as a conversation or as a task. A direct conversation can answer a question without creating a task. An automation is a rule for creating future tasks on a schedule or supported event; it is not a task that is already running. Reports can be produced through conversations or task work, so the model does not require every artifact to have a universal task-parent field. [FS52] [FS58]

Retained files and memory supply context to the execution runtime. They survive differently from session state, and conversation compaction has a different purpose again. The context chapter follows these distinct representations rather than treating them as one mutable knowledge store. [FS53] [FS54]

Green boxes identify AWS-defined concepts and cross-service dependencies such as IAM roles. Blue identifies our normalized groupings, including the evidence family used to discuss cost queries, anomalies and recommendations together. Those upstream results have different source identities; they are not one native FinOps Evidence resource. The [resource index](../catalog/resource-models.html#model-finops) makes this distinction explicit before the guide applies the model to reporting and anomaly investigation.
''')
section('finops','F-09','Conversations, automations, tasks and artifacts',r'''
A conversation represents interaction with the agent. A task represents separately recorded execution. An automation represents instructions for future task creation. These objects may be connected, but their lifecycles are not interchangeable. A request can be answered directly; an explicit task can enter the queue; and a recurring automation can create another task at each applicable start. [FS52]

![Conversation, automation and task records](../assets/diagrams/er-finops-work.svg)

The event-driven path adds a cross-service dependency. The documented preview uses Cost Anomaly Detection events and service-managed EventBridge rules. The automation matches the supported event and creates work. The public guide does not establish that every automation owns exactly one rule, so that multiplicity is left unspecified in the ER diagram. IAM conditions restrict management to the permitted managed rules rather than general administration of the event bus. [FS51] [FS52]

Results have identities outside this orchestration path. A source query is defined by dates, metric, scope and dimensions; a forecast, anomaly and recommendation are different upstream results. A report artifact contains an interpretation of those results. A Jira issue or Slack post is an external publication. The team should retain these references when it needs to reconstruct a decision, without assuming a universal service-side lineage graph that the public guide does not document. [FS57] [FS58]

| Object | Relevant change or stop operation | What the operation does not imply |
|---|---|---|
| Conversation | Continue or cancel applicable current work | Every answer becomes a task or artifact |
| Task | Inspect execution; cancel where supported | Its retained history or external publication is deleted |
| Automation | Update, disable or delete future work | Already-created tasks are cancelled |
| Agent connection | Change or remove the destination binding | Previously published messages are withdrawn |
| Context file | Soft delete or restore the uploaded input | A matching remembered fact is also changed |
| Report artifact | Inspect, revise, download or delete | Every downloaded or externally published copy disappears |

The object-specific data lifecycle is documented under F-M07. This table explains why an operator must identify the intended object before selecting an action. For example, replacing a weekly report requires checking for the previous automation as well as testing the new report; merely using a new task name can leave two schedules active. [FS52] [FS54]

Publication also depends on invocation mode. Jira actions requested interactively or through on-demand tasks require the documented approval, whereas scheduled or event-created actions use setup-time authorization. Slack does not present the same per-message approval prompt. A generic Result → Destination arrow is therefore incomplete unless the product, operation and invocation path are retained in the implementation profile. [FS57]

The model establishes relationships the reader can reason about; it does not provision them. The [feature/resource crosswalk](../catalog/resource-models.html#model-finops) links each approved feature reference to the actual instance, connection, task or context object and its supporting documentation.
''')
section('finops','F-10','Context and evidence in reporting and anomaly use cases',r'''
The approved reporting and anomaly cases reuse data access and context, but they start with different questions. A periodic report asks for a stable comparison over a defined period. An anomaly investigation asks what contributed to a detected deviation and what evidence supports an operational explanation. Both depend on source identity and query basis before retained preferences or formatting become useful. [FS52] [FS57] [FS58]

![Retained inputs and session context](../assets/diagrams/er-finops-context.svg)

For [UC-F04, prepare a periodic cost report](../catalog/index.html#UC-F04), the operator maintains authoritative ownership or allocation mappings in context files. The agent can read those files but does not rewrite them through conversation. Persistent memory can retain reporting preferences and corrections for subsequent work. Older messages within a long conversation may instead be summarized to fit the context window. These are separate mechanisms and should be tested with different known facts. [FS53]

The runtime loads retained context for a session, but ending that runtime is not deletion of the stored files, memory, conversations or artifacts. The configuration belongs to the instance, and the guide does not establish shared knowledge across instances. When a team changes ownership, it should update the authoritative mapping and the uploaded file deliberately rather than assuming a conversational correction changed every representation. [FS54]

For [UC-F05, investigate a cost anomaly](../catalog/index.html#UC-F05), the event-created variant adds an automation and managed-event dependency to the same analytical objective. Trace the source event to the matching automation, then to the queued task and its result. A task that never started indicates a different problem from a finished task whose Slack delivery failed. Review the condition and publication destination before enabling unattended operation. [FS52] [FS55] [FS56]

| Approved case | Product objects used | Evidence that belongs to the outcome |
|---|---|---|
| Historical cost analysis | Instance, source-access role and conversation or task | Reproducible query basis and reconciled figures |
| Periodic cost report | Context file, optional memory, automation, task and artifact | Reviewed period, comparisons, missing inputs and actual output |
| Anomaly investigation | Source anomaly, optional event rule, automation and task | Contributors, change evidence and unresolved causes |
| Recommendation prioritization | Upstream recommendation and workload context | Assumptions, conflicts, accepted or deferred decision |
| Post-change measurement | Before/after source data and engineering change record | Observed difference and explicit attribution limits |

The last column is an engineering acceptance model, not a list of automatically populated AWS fields. In particular, a cost decrease is not itself proof that a change caused the saving. A source recommendation is a candidate, not a purchase or infrastructure-change authorization. [FS57]

The shared operational-review case can consume these outputs alongside service-health reports. That handoff is a team process between independently scoped services. It preserves source and execution identities; it does not transfer credentials, merge memory or create a cross-product orchestration engine.
''')

section('architecture','A-10','Concept ownership and the approved entity model',r'''
The approved conceptual model separates an operational objective from the product objects used to implement it. A use case identifies who needs a result and how completion is judged. Its workflow orders the work. A mechanism explanation describes how a documented process operates, and a feature reference leads to the concrete configuration and execution facilities used by that process. An implementation profile supplies a reviewed configuration recipe. These are this collection's concepts, not universal AWS resource types.

![Concept model and product resource bindings](../assets/diagrams/er-concept-model.svg)

Blue identifies concepts defined by this documentation. Green identifies AWS-defined resources or documented concepts. Orange identifies an external system, original source evidence or an engineering-owned artifact or decision. Color concerns the authority that defines the concept, not who wrote its content. A customer-authored DevOps skill is green because AWS defines the skill facility; an owner-reviewed SOP document is orange. Our implementation profile is blue, even when it configures an AWS release test profile that is green. [AS50]

Green does not mean independently creatable. A service resource, an asset subtype, a configuration member, an execution record and a derived view all have different administrative behavior. For that reason every entity in the specialized models has a kind, scope and identity description as well as a name. The model does not create new CRUD operations for retained login navigation, a topology view or a conversation summary. The relevant services document those concepts without establishing one common object interface. [AS51] [AS52]

The product diagrams refine the model rather than flattening the products into it. DevOps associates providers with operational spaces and offers managed and custom execution paths. Security separates shared configuration from application assessments and gives different assessment types different lifecycles. FinOps uses an instance-local context and task model whose IAM vocabulary includes service-specific AgentSpace names. Similar labels do not establish interchangeable resources. [AS50] [AS51] [AS53]

Relationships are qualified in three classes. A solid relationship is explicitly documented. A dashed logical relationship is an explanatory association inferred from the described behavior, such as recording a task's optional automation origin without asserting a particular API field. A dashed editorial relationship is introduced by this collection, such as linking a use-case step to a mechanism. Exact multiplicity remains `?` when the reviewed source does not establish it. `0..*` describes a repeatable logical relationship, not an unlimited service quota.

The [resource-model reference](../catalog/resource-models.html) is the generated dictionary and relationship register. It links back to the maintained guide explanations and forward to feature dependencies. It is not a new parallel use-case catalog or a database migration for any AWS service.
''')
section('architecture','A-11','Product specialization and use-case traceability',r'''
Stage 2 specializes the approved model in three directions: configuration scope, execution lifecycle and knowledge ownership. The purpose is not to make the products look the same, but to let the reader locate the corresponding responsibility while preserving its actual implementation. Start with a use case, follow its conditional mechanism dependencies, then inspect the product-specific resource bindings before configuring anything. [AS50] [AS51] [AS52]

| Conceptual responsibility | DevOps specialization | Security specialization | FinOps specialization |
|---|---|---|---|
| Scope | Agent Space with source associations and knowledge | Application Agent Space with some shared tenant configuration | Independent instance; service-specific AgentSpace name in IAM |
| Reusable definition | Custom-agent definition, skill or test profile | Assessment-specific configuration; design review is the exception | Automation and instance configuration |
| Execution | Investigation, custom invocation or Learning execution | Assessment run, one-off design review or revalidation job | Conversation work or separately recorded task |
| Retained context | Stores, memory entries and versions; instructions and skills | Application sources, requirements and retained login procedure | Context files, persistent memory and conversation summaries |
| Evidence result | Investigation output, invocation trajectory or recommendation | Source or application findings and linked revalidation results | Analysis and report artifact; upstream evidence stays distinct |
| External effect | Eligible approved directed operation or active application test | Application requests, code proposal or finding publication | Supported Jira or Slack publication |

This is a responsibility crosswalk. It does not declare that the objects in a row share an API, permission model or deletion behavior. The exact definitions and exceptions appear in D-13, S-10 and F-09. In particular, the FinOps IAM name is documented as `finops-agent:CreateAgentSpace`; it must not be silently replaced with the DevOps service namespace in scripts or policies. [AS53]

The thirty approved use cases remain the authoritative outcome list. Their source records, identifiers, variants, mechanisms and implementation profiles are preserved in this revision. Each feature reference now has an explicit binding to the product objects it uses. That extra relationship answers a question the earlier catalog could not answer precisely: which actual configuration or execution record must an engineer inspect for this step?

For an incident investigation, follow the signal and investigation, then any selected source and memory. For application repair verification, follow the original finding, reviewed change, deployed target and revalidation job. For cost reporting, follow the query basis, retained mapping, optional automation, task and artifact. A failed relationship changes the interpretation of the outcome: missing current telemetry cannot be repaired by recalling an earlier diagnosis; an unreachable authenticated route cannot establish a repaired vulnerability; a correct total with a stale owner mapping is still an incorrect allocation. These are engineering acceptance rules applied to documented operations, not extra native agent capabilities. [AS50] [AS51] [AS52]

The shared operational-review case, [UC-G01](../catalog/index.html#UC-G01), combines reviewed results rather than native runtime state. The receiving engineer gets source identifiers, observation period, result and unresolved questions. Credentials and approval authority stay with their original product boundary. The same separation applies to knowledge: no relationship in this model asserts a shared cross-product memory service or automatic transfer of learned context.

The reverse index supports configuration review. From a feature, the reader can inspect its resource bindings and the use cases that may depend on it. Conditional profiles remain conditional; the index is not a live impact detector or a proof that every linked case is deployed. The model review checks these relationships and preserves uncertain multiplicities, while live access and execution would require a separate authorized test.
''')

# Update source references and canonical prose while preserving every stable section ID.
for key,g in guides.items():
    prefix={'devops':'DS','security':'SS','finops':'FS','architecture':'AS'}[key]
    for sid,record in model['sources'].items():
        if sid.startswith(prefix):g['refs'][sid]=record['url']
    if key=='architecture':
        for sid,target in {'AS50':'DS53','AS51':'SS50','AS52':'FS54','AS53':'FS51'}.items():g['refs'][sid]=model['sources'][target]['url']
for (key,sid),(title,body) in TEXT.items():
    guides[key]['sections'][sid]={'id':sid,'title':title,'body':body,'sources':sorted(set(re.findall(r'\b[DSFA]S\d+\b',body)))}
    TYPES[sid]='overview' if sid in ('A-10','D-01','S-01','F-01') else 'reference'

for key,ds,ap in [('devops','D-13','D-14'),('security','S-10','S-11'),('finops','F-09','F-10')]:
    CHAPTERS[key][0]['title']='Resource model and scope'
    CHAPTERS[key][0]['purpose']='Begin with the product-specific entities, their scope and their relationships. Configuration, executions, knowledge and external evidence are distinct objects with different lifecycles.'
    CHAPTERS[key][0]['sections'].append(ds)
    example=next(c for c in CHAPTERS[key] if c['slug']=='example')
    example['title']='Applying the model to operational outcomes'
    example['purpose']='Trace the approved use cases through their concrete configuration and execution objects, then examine the prepared evidence. The examples remain synthetic, not live AWS results.'
    example['sections'].insert(0,ap)
CHAPTERS['architecture'][0]['sections']=['A-00','A-10','A-11','A-09','A-01','A-02']
CHAPTERS['architecture'][0]['title']='Concept ownership and product resource models'
CHAPTERS['architecture'][0]['purpose']='Read the approved conceptual model, its ownership notation and each product specialization before comparing knowledge or execution behavior.'

for key,g in guides.items():
    pieces=[g['intro'],'']
    for i,c in enumerate(CHAPTERS[key],1):
        pieces.extend([f'## {i:02d}. {c["title"]}',c['purpose'],''])
        for sid in c['sections']:
            sec=g['sections'][sid];pieces.extend([f'### {sid} — {sec["title"]}',sec['body'],''])
    pieces.extend(f'[{sid}]: {url}' for sid,url in g['refs'].items())
    (ROOT/f'guides/{key}.md').write_text('\n\n'.join(pieces).rstrip()+'\n')

# Retain the timed lessons and exercises, replacing their old generic overview
# with the specialized ER and adding explicit configuration/lineage explanations.
def diagram_slide(title,key,refs,minutes=2):
    return dict(title=title,seconds=minutes*60,refs=refs,kind='diagram',diagram=key,data=[],message='Read the entity kind and ownership label before following the relationship. A question mark leaves exact multiplicity unspecified; the detailed register explains each logical association.')
def table_slide(title,refs,rows,minutes=2,message=''):
    return dict(title=title,seconds=minutes*60,refs=refs,kind='table',data=rows,message=message)

for key,scope,detail,caseview,detailrefs,caserefs in [
    ('devops','er-devops-scope','er-devops-knowledge','er-devops-incidents',['D-13'],['D-14']),
    ('security','er-security-scope','er-security-assessments','er-security-lineage',['S-10'],['S-11']),
    ('finops','er-finops-scope','er-finops-work','er-finops-context',['F-09'],['F-10'])]:
    old=DECKS[key]['slides'];new=[];newgroups=[]
    for gi,(name,indices) in enumerate(DECK_CHAPTERS[key]):
        start=len(new)
        for index in indices:
            sl=copy.deepcopy(old[index])
            if index==0:
                sl=diagram_slide({'devops':'Agent Space, provider associations and custom invocations','security':'Shared configuration and application Agent Spaces','finops':'Instance roles and destination connections'}[key],scope,[model['products'][key]['overview_section']])
            new.append(sl)
        if gi==0:
            new.append(diagram_slide({'devops':'Memory stores, entries and definition references','security':'Assessment configurations and distinct execution lifecycles','finops':'Conversations, automations, tasks and artifacts'}[key],detail,detailrefs,3))
            name='Product-specific resource model'
        if 'Operational objectives' in name:
            new.append(diagram_slide({'devops':'Incident records and action-specific authorization','security':'Original findings and revalidation history','finops':'Retained context and session-local execution'}[key],caseview,caserefs,3))
        newgroups.append((name,list(range(start,len(new)))))
    DECKS[key]['slides']=new;DECK_CHAPTERS[key]=newgroups

arch=DECKS['architecture']['slides'];rebuilt=[];groups=[]
for gi,(name,indices) in enumerate(DECK_CHAPTERS['architecture']):
    start=len(rebuilt)
    if gi==0:
        rebuilt.append(table_slide('Concept ownership and resource identity',['A-10'],[
            ['Class','What it defines','Examples','Interpretation'],
            ['Documentation-defined','How the reference explains operational work','Use case; mechanism explanation; implementation profile','Not an AWS resource or SDK payload'],
            ['AWS-defined resource','A documented service facility','Agent Space; assessment configuration; automation','Use the exact product namespace and lifecycle'],
            ['AWS-defined state or view','A documented representation or component','Topology; retained login procedure; conversation summary','Do not invent independent CRUD operations'],
            ['External or engineering-owned','Original system or accepted artifact','Repository revision; deployed target; Jira issue; review','Preserve source identity and independent authorization']
        ],3,'Blue, green and orange classify concept ownership. Resource kind and source qualification prevent false equivalence.'))
        rebuilt.append(table_slide('Product-specific configuration and execution models',['A-11'],[
            ['Responsibility','DevOps','Security','FinOps'],
            ['Scope','Operational Agent Space','Application Agent Space; shared requirements','Independent instance; finops-agent AgentSpace IAM name'],
            ['Reusable definition','Custom agent; skill; test profile','Assessment-specific configuration','Automation; instance settings'],
            ['Execution','Investigation; invocation; Learning run','Run; one-off design review; revalidation job','Conversation work; task'],
            ['Retained context','Stores, memories and versions','Application context; requirements; login procedure','Files; persistent memory; conversation summary']
        ],3,'Similar responsibilities do not imply interchangeable resources, permissions or deletion behavior.'))
    rebuilt.extend(copy.deepcopy(arch[i]) for i in indices)
    groups.append((('Concept model and product specialization' if gi==0 else name),list(range(start,len(rebuilt)))))
DECKS['architecture']['slides']=rebuilt;DECK_CHAPTERS['architecture']=groups

(ROOT/'tools/docs/structure.py').write_text('"""Maintained chapter membership and presentation grouping."""\nREVISION='+repr(REVISION)+'\nBASELINE='+repr(BASELINE)+'\nCHAPTERS='+pformat(CHAPTERS,width=105,sort_dicts=False)+'\nDECK_CHAPTERS='+pformat(DECK_CHAPTERS,width=105,sort_dicts=False)+'\nTYPES='+pformat(TYPES,width=105,sort_dicts=False)+'\nLABELS='+pformat(LABELS,width=105,sort_dicts=False)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n')
(ROOT/'tools/docs/presentation.py').write_text('"""HTML lessons aligned with the canonical product resource models."""\nDECKS='+pformat(DECKS,width=105,sort_dicts=False)+'\n')

# Integrate one maintained renderer; do not leave alternate catalogs or migrations.
path=ROOT/'tools/docs/diagrams.py';text=path.read_text()
text += '\n# The canonical resource register supplies specialized ER figures.\nfrom resource_model import diagram_definitions\nDIAGRAMS.update(diagram_definitions())\n'
path.write_text(text)
path=ROOT/'tools/docs/build.py';text=path.read_text()
text=text.replace('import catalog as catalogue','import catalog as catalogue\nimport resource_model')
text=text.replace('build_catalog(catalog,guides);indexes(catalog);metadata(guides,catalog)','build_catalog(catalog,guides);indexes(catalog);metadata(guides,catalog)\n    resource_model.resource_index(guides,frame,write,figure)\n    resource_model.integrate_pages(write)')
text=text.replace('Logical model; arrows show documented relationships, not AWS internal deployment.','Logical model, not AWS internal deployment. Resource ER diagrams qualify undocumented multiplicity and logical associations in their relationship register.')
text=text.replace('## Operational use cases\\n\\n[Read and search the catalog]','## Product resource models\\n\\n[Read the ownership-coded resource models](catalog/resource-models.html). The guides introduce the model in their overview, explain identities and lifecycles, and trace the approved use cases through concrete resource bindings. [Model source](catalog/resource-models.json) and [review evidence](qa/product-source-review.json) are maintained with the build.\\n\\n## Operational use cases\\n\\n[Read and search the catalog]')
text=text.replace('canonical cases, mechanisms, features, profiles and alias data','canonical cases, mechanisms, features, profiles, aliases and product resource data')
text=text.replace('Canonical cases, mechanisms, features, profiles and alias data','Canonical cases, mechanisms, features, profiles, aliases and product resource data')
text=text.replace('and recipes in `catalog/profiles.json`, chapter membership','recipes in `catalog/profiles.json`, product entities and relationships in `catalog/resource-models.json`, chapter membership')
path.write_text(text)
path=ROOT/'tools/docs/check.py';text=path.read_text()
text=text.replace('from model_check import validate_model','from model_check import validate_model\nfrom resource_model import validate as validate_resources')
text=text.replace("html_paths=[ROOT/'catalog/mechanisms.html'","html_paths=[ROOT/'catalog/resource-models.html',ROOT/'catalog/mechanisms.html'")
text=text.replace('errors.extend(model_result["errors"])','errors.extend(model_result["errors"])\n    resource_result=validate_resources(guides,browser=browser)\n    errors.extend(resource_result["errors"])')
text=text.replace("results['relationship_model']=model_result","results['relationship_model']=model_result\n    results['product_resource_model']=resource_result")
text=text.replace('The [relationship checks](qa/relationships.json) additionally','The [product resource checks](qa/resource-models.json) verify entity ownership, qualified relationships, all feature/resource bindings and unchanged approved catalog sources. [Product-source evidence](qa/product-source-review.json) identifies the exact reviewed claims and version qualifications.\\n\\nThe [relationship checks](qa/relationships.json) additionally')
path.write_text(text)

(ROOT/'CHANGELOG.md').write_text('# Documentation changes\n\n## 22 October 2026 — product-specific resource models\n\nSpecialized the approved conceptual model for DevOps, Security and FinOps. Added ownership-coded resource diagrams, entity and relationship registers, feature/resource bindings and model-led guide chapters. Preserved all thirty approved use cases and the existing mechanism, feature, profile and alias source files byte-for-byte. Added model explanations to the HTML presentation flow.\n\nDocumented distinctions include managed versus custom DevOps execution, assessment-specific Security lifecycles, the documentation-defined finding/job result association, and the FinOps instance/AgentSpace naming correspondence. Unknown cardinalities remain explicit. No live AWS operation was executed. Git retains prior editions; no manual archives were created.\n')
standard=ROOT/'EDITORIAL_STANDARD.md'
standard.write_text(standard.read_text().rstrip()+'\n\n## Product resource model\n\nUse ownership labels and colors consistently: DOC blue for this collection, AWS green for documented product concepts, EXT orange for external systems and engineering artifacts. Always state entity kind: resource, configuration member, execution record, retained state or derived view. A green label does not imply independent CRUD operations. Qualify relationship multiplicity; unknown remains unknown. Product namespace is part of identity. Keep configuration, execution, original evidence and acceptance distinct. The resource register binds features to objects without replacing or rewriting approved use cases.\n')
(ROOT/'qa/stage2-content-review.json').write_text(json.dumps({'revision':REVISION,'baseline':BASELINE,'scope':'Product-specific resource validation and model-led guide restructuring','approved_catalog_sources':'Preserved byte-for-byte; enforced by resource-model validator','guide_sections':{'overviews_rewritten':['D-01','S-01','F-01'],'added':['D-13','D-14','S-10','S-11','F-09','F-10','A-10','A-11']},'important_distinctions':['Managed and custom DevOps agents are different administrative concepts','Security design review is one-off; full-code and repository-triggered settings are distinct','Finding/job result is a documentation-defined association','FinOps instance uses service-specific AgentSpace IAM names','Derived state is not automatically a separately addressable AWS resource'],'boundary':'Targeted official-source review; not exhaustive re-audit, runtime discovery, access validation or executed use-case test.'},indent=2)+'\n')
Path(__file__).unlink()
print('Applied product-specific model revision; one-time migration removed.')
