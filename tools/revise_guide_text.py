#!/usr/bin/env python3
"""One-time, plain-text editorial revision; removed after applying it."""
from pathlib import Path
import re, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from docs_build import parse_source, group_markdown
from docs_structure import CHAPTERS, TYPES, LABELS, DECK_CHAPTERS
from lesson_plan import DECKS

TITLES={
'D-01':'The agent, Agent Space, and investigation','D-02':'Resource roles and operator roles','D-03':'MCP provider registration and tool selection','D-04':'Private network connections','D-05':'Resource discovery and topology construction','D-M01':'Incident-memory construction and retrieval','D-M02':'Investigation feedback and corrective memory','D-M07':'Memory-store access, versions, and retention','D-M03':'Global and agent-specific instructions','D-M04':'Runbook skills and applicability rules','D-06':'Incident triage, investigation, and prevention','D-07':'Custom-agent configuration and invocation','D-M05':'Sandbox computation and network policy','D-M06':'Directed actions and approval scope','D-08':'Configuration APIs and update semantics','D-09':'Remote access and release-assurance workflows','D-U01':'Recurring-alarm investigation: worked example','D-10':'Execution limits and diagnostic procedures','D-11':'Documentation coverage and references',
'S-01':'The agent, application space, and assessment','S-02':'User access and repository connections','S-03':'Test targets, dependencies, and exclusions','S-M01':'Credential retrieval and application login','S-M02':'Login-workflow retention and reuse','S-M03':'Requirement applicability and evaluation','S-M04':'Requirement generation and replacement','S-M06':'Encryption keys, identities, and access','S-04':'Assessment configuration and run lifecycle','S-05':'Finding review and code remediation','S-M05':'Finding revalidation and evidence lineage','S-06':'Code review, design review, and threat modeling','S-U01':'Authorization-finding remediation: worked example','S-07':'Assessment failures and operating limits','S-08':'Documentation coverage and references',
'F-01':'The agent instance and its execution environment','F-02':'Administrator, service, and operator permissions','F-M01':'Cost queries and recommendation provenance','F-05':'Jira projects and Slack channel connections','F-M02':'Context-file preparation and management','F-M03':'Persistent preferences and corrections','F-M04':'Conversation summarization and context limits','F-03':'Tasks, schedules, and execution history','F-M05':'Anomaly events and task creation','F-04':'Report generation and artifact management','F-M06':'Publication permissions and approvals','F-M07':'Retention, cancellation, and deletion','F-U01':'Cost-variance analysis: worked example','F-06':'Data, task, and integration failures','F-07':'Documentation coverage and references',
'A-01':'Workspace, configuration, and execution models','A-02':'Knowledge construction and retrieval models','A-03':'Network, identity, and tool-access boundaries','A-04':'Authorization of state-changing operations','A-05':'Configuration, execution, and artifact lifecycles','A-06':'Cross-team evidence handoffs','A-U01':'Cross-platform operational review: worked example','A-07':'Architecture assumptions and references'}

INTRO={
'devops':'''# AWS DevOps Agent

Architecture, integrations, knowledge, and operational workflows

An incident rarely arrives with all of its evidence in one place. The alarm identifies a symptom; logs describe individual failures; a deployment system records changes; and a runbook explains the service's expected behavior. AWS DevOps Agent works across the sources made available to an Agent Space to investigate that operational question. The service also supports operational inquiries, prevention analysis, and custom-agent work. Release-assurance features have separate availability and effects. [DS18] [DS08]

This guide begins with the objects an operator configures, then follows the evidence into an execution and into retained knowledge. After the integration and knowledge chapters, it explains incident handling, custom reports, and controlled actions. The worked example shows why an earlier root cause is useful context but cannot replace present measurements. The grouped use-case catalog applies these mechanisms to daily work; it is not a second list of platform capabilities.

Product behavior is linked to official AWS documentation. Diagrams are logical explanations of documented resources and flows, not disclosures of AWS's internal implementation. Procedures marked as engineering guidance and synthetic examples describe proposed team practice. No live AWS execution is claimed.''',
'security':'''# AWS Security Agent

Architecture, application context, assessment, and finding verification

AWS Security Agent assesses an application using the sources, access, criteria, and target scope configured for it. The useful starting point is therefore the application: which revision is being assessed, which documents explain its boundaries, which identities may reach protected routes, and which requirements apply. The service's current documentation places it within AWS Continuum. Availability remains specific to the assessment feature and Region. [SS01] [SS02]

The chapters follow the preparation of an assessment through execution and finding verification. First they establish the Agent Space and supported integrations. Next they explain how source material, credentials, login procedures, and requirements supply different kinds of context. Finally they trace a finding through a proposed repair, deployment, and targeted revalidation. These are separate records with separate evidence.

Diagrams show the documented logical relationships; they are not a claim of a universal security-agent runtime. Engineering guidance and the worked example are explicitly distinguished from product functions. The use-case catalog provides applications of these functions without implying that a successful assessment proves complete security.''',
'finops':'''# AWS FinOps Agent

Architecture, cost-data sources, organizational context, and task execution

AWS FinOps Agent is documented as a preview service for cost inquiry, anomaly investigation, reporting, and the interpretation of upstream optimization recommendations. Its work begins with a defined comparison: the accounts, dates, cost basis, and dimensions under consideration. It combines authorized source results with the organization's uploaded context and retained preferences, then produces an answer, a task result, or a report. [FS01]

This guide follows that sequence. It explains the instance and permissions first, identifies the supported data and collaboration integrations, and then separates reference files, persistent memory, and conversation summarization. The task chapter follows a scheduled or event-driven request into the queue and through publication. The worked example distinguishes a numerical cost contribution from evidence of an operational cause.

During the reviewed preview, agent data is stored in us-east-1 and inference can use other US Regions; those are different boundaries. Diagrams are logical service models. Examples and proposed checks are not live account results, purchase authorizations, or measured savings. [FS08] [FS09]''',
'architecture':'''# Architecture of AWS operational agents

Execution, integration, knowledge, and evidence across three services

The term agent describes a way of carrying out work, not one universal AWS resource type. AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent expose different configuration objects, execution records, and retained context. This guide introduces the common concepts and then compares their concrete product implementations. The comparison is intended to help teams configure each service without importing assumptions from another. [AS30] [AS31] [AS32]

Begin with the distinction between an agent definition and an execution. From there, follow the connections to external systems, the construction and retrieval of knowledge, and the controls on effects. The final chapters describe a team-managed handoff between services. They do not posit a shared memory store, common permission model, or built-in cross-product orchestrator.'''}

ADDITIONS={
'D-12':('Supported integrations and connection directions','''An integration answers two separate questions: which system can supply evidence, and which system can receive an action or update? Those directions matter. A telemetry connection may permit reading metrics without posting findings back. A webhook may start an investigation without granting any permission to query the originating monitoring system. The following inventory separates these paths rather than treating every connected brand as an equivalent connector. [DS30] [DS31]

| Connection family | Documented systems | Information or effect | Setup boundary |
|---|---|---|---|
| AWS resource and telemetry access | Primary and secondary AWS accounts; CloudWatch | Authorized resource inspection and telemetry queries | Account roles and selected account associations |
| Object-based evidence | Amazon S3 | Read logs, configuration, and other objects | Scope ListBucket and GetObject to required buckets and objects |
| Kubernetes inspection | Amazon EKS | Cluster, pod-log, and event inspection | EKS access setup and network reachability are additional prerequisites |
| Two-way observability | Dynatrace | Telemetry/topology reads; configured problem initiation; investigation updates | Provider setup and the Dynatrace workflow determine the actual paths |
| One-way telemetry access | Datadog, Grafana, New Relic, Splunk | Telemetry reads through the documented provider path | Source authorization; event initiation is separately configured through webhooks |
| Code and delivery context | GitHub, GitLab | Repository and pipeline evidence for operational investigations | Connect the relevant sources and deployment mapping |
| Azure infrastructure | Azure Resources | Subscription-scoped discovery and investigation | Register the tenant connection, then associate subscriptions |
| Azure delivery context | Azure DevOps | Selected project and pipeline-history context | Separate registration and project association; pipeline history does not imply access to externally hosted code |
| Incident coordination | ServiceNow, PagerDuty, Slack | Provider-specific incident initiation and communication | Configure each provider's documented route and permitted destination |
| Additional tools | Compatible remote or private MCP servers | The tools explicitly selected for the Agent Space | MCP authentication, tool selection, effect classification, and networking |
| External initiation | Authenticated webhooks | Incoming incident information | Caller authentication and request format; not a telemetry-read grant |
| Lifecycle delivery | Amazon EventBridge | Investigation and mitigation lifecycle events sent to configured targets | Event routing and destination permissions; not an arbitrary custom-agent trigger claim |

The named built-in providers above come from the integration overview and provider guidance. A Prometheus or proprietary source can be exposed through the bring-your-own MCP/webhook route; that is not the same claim as a maintained native connector. The three-way distinction between built-in two-way telemetry, built-in one-way telemetry, and bring-your-own sources is documented by AWS. [DS30] [DS31]

![Provider registration and Agent Space association](../assets/diagrams/devops-integrations.svg)

Registration establishes an account-level provider connection. Association makes selected resources or tools available in a particular Agent Space. Authentication is then exercised when the agent invokes the tool. An engineer can therefore diagnose a missing result in sequence: confirm registration, confirm association and tool selection, confirm the route, then inspect the actual call and returned identity. The MCP-specific choices are described in D-03; private routing is described in D-04.

Azure adds another scope decision. Azure Resources and Azure DevOps are independently registered capabilities. The former associates subscriptions; the latter associates projects. The documented registration options include administrator consent and a customer-managed Entra application with federation. Connecting a pipeline whose code lives elsewhere does not automatically provide that repository's contents. [DS32]

For a first operational deployment, choose the smallest useful evidence chain: the affected AWS service, one telemetry source, and the repository or pipeline that deploys it. Add incident coordination after confirming a read with known service and revision identifiers. This staged verification is an engineering recommendation, not an additional service requirement.'''),
'S-09':('Supported source and collaboration integrations','''Security assessment needs both application evidence and a reachable test surface. A repository explains code; a design page explains intent; a deployed endpoint exposes actual behavior. Connecting one of those sources does not substitute for the others. The account-level integration is registered once, while each Agent Space selects the repositories, pages, buckets, or projects appropriate to its application. [SS30]

| Source or destination | Documented support | Selection in the application space | Effect boundary |
|---|---|---|---|
| GitHub | Cloud-hosted GitHub and cloud-hosted GitHub Enterprise | Connected repositories | Read analysis; repository write features are separate opt-ins |
| GitHub Enterprise Server | Self-hosted server | Selected repositories and configured reachability | Private connectivity may be necessary |
| GitLab | Cloud-hosted GitLab | Selected repositories | Provider-specific review comments and remediation configuration |
| GitLab Self-Managed | Self-hosted instance | Selected repositories and reachable endpoint | Authentication and private routing require their own setup |
| Bitbucket | Bitbucket Cloud | Selected repositories | Do not extend Cloud support to self-hosted editions |
| Confluence | Confluence Cloud | Selected pages | Read-only documentation context, not a source-code repository |
| Amazon S3 | Connected same-account buckets or prefixes | Resources selected for an assessment | Code-review sources use supported source archives; supporting documents have their own formats |
| Jira | Jira Cloud | Selected projects | Finding issue creation and comments are independently allowed per project |

Connecting a repository grants read context to the eligible assessment functions that share the space. Code-review comments and code-remediation changes are enabled separately per repository. The integration overview excludes these write actions for public repositories; do not interpret read access as permission to publish a patch or comment. [SS30]

![Application-source registration and selection](../assets/diagrams/security-integrations.svg)

To configure a source, first authorize its supported provider account from Integrations. Open the application Agent Space, select resources from that registration, and save the selection. Then configure the assessment that consumes those resources. For Confluence, selecting a page supplies read context; there are no per-page assessment toggles. For S3, connect the bucket or prefix once and select the needed resources when authoring an assessment. The S3 guide specifies same-account buckets and separate requirements for code-review sources. [SS31] [SS33]

Jira follows a related but action-oriented sequence. Install and authorize the documented Forge application, register the Jira Cloud site, then choose projects for the Agent Space. Allow issue creation, comments, or both according to the workflow. Existing Jira issues are external records: removing the connection does not remove the issues already created. [SS32]

Private source-control access, penetration-test network access, and credential retrieval are separate paths. A reachable repository does not prove that the test runner can reach a private application. Similarly, a readable secret does not establish that its contents successfully log in to that application. The next chapter follows these distinctions through authentication and context construction.'''),
'S-M07':('Application-context construction and reuse','''An assessment starts with the application material selected for that task. Source code supplies implementation evidence; API and design documents describe interfaces and intended relationships; scope documents delimit what a threat model should analyze. The Agent Space makes connected material available, but the assessment configuration still determines what is relevant to a particular run. An engineering record should identify the source revision and document version used rather than simply say that the agent knows the application. [SS03] [SS16] [SS31]

![Application context, assessment criteria, and findings](../assets/diagrams/security-context.svg)

The context is consolidated into an assessment of the selected system. In a threat-model workflow, this can include a system overview, data flows, trust boundaries, and candidate threats. In a penetration test, source and documentation context supports exploration of the authorized deployed target. Review the inferred model before evaluating its conclusions: a missing identity boundary or a document for the wrong release changes the question being answered. [SS16] [SS34]

Three different forms of reuse must remain distinct. A saved assessment configuration retains reusable setup. A requirement pack supplies criteria to later eligible reviews. Login Optimization retains a successful authentication procedure. None of these establishes the DevOps Agent monitor-memory mechanism for Security Agent. The reviewed guidance does not describe a universal customer-editable vulnerability-memory store or an automatic model-training process across all assessments. [SS03] [SS09] [SS14]

For an application change, reconnect or select the current sources, update the scope where necessary, and create the next run. For a wrong requirement, edit the governing criteria; for a changed login, test the current credential flow. Historical findings remain evidence of earlier executions, not a substitute for the new source and target state. A revalidation job retrieves selected existing finding evidence and tests that finding again; it is narrower than reconstructing or rescanning the whole application. [SS13]

A practical verification starts with a small known boundary: two application roles, one protected resource, and the repository revision deployed to staging. Inspect whether the inferred system and the resulting finding refer to those same roles and revision. When the evidence does not expose which document or procedure was used, record that limitation rather than infer it from plausible output.'''),
'F-08':('Supported data sources and publication destinations','''The data connections answer different financial and operational questions. Cost Explorer supplies cost and usage results. Anomaly Detection supplies a detected deviation. Optimization services supply candidate changes and savings estimates. CloudTrail supplies recorded API activity that may help explain a change. The agent combines these inputs; a permission to query one does not imply access to the others. [FS01] [FS03]

| System | Role in the workflow | Configuration dependency | Interpretation |
|---|---|---|---|
| AWS Cost Explorer | Cost and usage queries, forecasts, coverage and commitment analysis | Available cost data and the required role actions | Preserve the metric, dates, account scope, and grouping |
| AWS Cost Anomaly Detection | Anomaly monitor and event source | Relevant monitors and configured event automation | A deviation is a reason to investigate, not its explanation |
| AWS Cost Optimization Hub | Consolidated optimization recommendations | Service setup and authorized recommendation reads | Savings estimates belong to the source recommendation |
| AWS Compute Optimizer | Resource and rightsizing recommendations | Eligible resources and permitted reads | Review utilization assumptions and workload constraints |
| AWS CloudTrail | API-activity evidence | Permitted LookupEvents and relevant available records | A nearby change is evidence to evaluate, not proof of causality |
| Amazon EventBridge | Managed anomaly-to-task routing | Required managed-rule actions in the agent role | Creates work through the supported event path |
| Jira Cloud | Read connected issues; create issues and add comments | Account registration and agent-level project connection | No general issue-field, transition, deletion, or workflow-management capability |
| Slack | Post results to connected channels | Workspace registration, channel connection, and app membership | One-way publication in the documented preview |

This is the supported service-and-destination model described in the reviewed guides, not a claim of arbitrary external-tool connectivity. In particular, the existence of MCP integration in DevOps Agent should not be copied into this platform's architecture. Exact AWS action requirements remain in the IAM setup guide. [FS03] [FS12] [FS13]

![Cost-data retrieval and collaboration connections](../assets/diagrams/finops-integrations.svg)

Jira and Slack each use an account-level registration plus a connection owned by the individual agent. The registration stores provider authorization; the connection selects a project or channel. That distinction makes it possible for two agents to use the same registered provider while having different destinations. It does not give either agent access to the other's files, memory, or tasks. [FS12] [FS13] [FS08]

Test the paths separately. First reproduce a small cost query with known dates and dimensions. Then inspect a recommendation from its upstream source. Finally publish a non-sensitive test result to the intended destination and inspect where it arrived. A failed Slack post is not repaired by widening cost-data access. A missing CloudTrail event does not invalidate arithmetic that was reproduced independently, but it does limit the causal explanation.'''),
'A-00':('Agents, tools, context, and executions','''In these guides, an agent is a software system that carries out a bounded task by using a model to interpret the request and by invoking the tools or assessment functions the service makes available. The useful unit of observation is the execution: the particular investigation, assessment run, conversation, or task that receives inputs and produces results. The configured agent or application space is longer-lived and can supply permissions, instructions, sources, and retained information to many executions. The three AWS services implement that distinction with different named resources. [AS30] [AS31] [AS32]

A tool is an interface to another system, such as an authorized telemetry query or an issue-creation operation. Tool output supplies observations. Instructions express how the agent should perform its work. Memory or reference material supplies context. These are different responsibilities: a statement in a document cannot make an unauthorized API call succeed, and a granted API permission does not guarantee that a run will choose the correct query.

![Logical agent execution cycle](../assets/diagrams/agent-execution.svg)

The diagram is a reading model, not a shared AWS implementation. A request or event establishes the task; applicable configuration and context shape the execution; tools or assessment components produce observations; the service uses those observations to continue the work or produce an output. Where an effect requires approval, the approval boundary belongs to that operation. A retained lesson may influence a later run without altering the underlying model's weights.

This kind of agent is also different from a telemetry collection agent installed on a machine. The latter collects or forwards measurements. An operational reasoning service consumes evidence exposed through its configured access paths. Calling both an agent does not mean that DevOps Agent installs a universal host collector or that Security Agent continuously observes every request to an application.

The rest of the comparison keeps four questions separate: what reusable capability exists; which operation configures or invokes it; what documented mechanism carries it out; and which engineering use case combines those pieces. The product guides provide the procedures. The catalog provides concrete applications and their prerequisites.'''),
'A-08':('Integration direction and evidence ownership','''Start an integration design by drawing the direction of every exchange. An event producer can initiate work, a data source can answer a query, an execution target can receive active requests, and a publication destination can receive findings. One system may occupy several roles, but those roles still require distinct permissions and failure handling. [AS30] [AS31] [AS32]

| Integration role | DevOps Agent | Security Agent | FinOps Agent |
|---|---|---|---|
| Evidence source | AWS resources, observability, code and delivery systems, selected MCP tools | Selected repositories, S3 resources, design and Confluence documents | Authorized cost, anomaly, optimization, and change data |
| Work initiation | Operator request, supported incident integration/webhook, custom schedule | Operator assessment, supported repository or pipeline path, configured schedule | Conversation/task request, schedule, supported anomaly event |
| Active target | Approved resource/tool action; release-test application | Explicitly authorized application and authentication scope | Supported service queries; separately authorized collaboration actions |
| Result destination | Investigation record and configured communication path | Finding, remediation proposal, revalidation history, connected Jira project | Response, artifact, connected Jira project or Slack channel |

![Evidence handoff between independently configured services](../assets/diagrams/shared-handoff.svg)

The handoff in the diagram is team-composed. For example, an operational investigation can produce a service identifier and a deployment revision. An application owner can use those identifiers to scope a security assessment, while a cost engineer can use the service and time window to define a cost inquiry. The receiving service uses its own configuration and permissions. The handoff should carry references and decisions, not borrowed credentials or an assertion that an earlier approval applies everywhere.

Ownership remains with the original systems. A source repository owns the reviewed revision, an assessment owns its finding, and a destination owns the published ticket or message. Removing a connection can stop future access or publication without deleting those external records. This is why a cross-platform workflow needs an explicit record of source identity, execution identity, and publication destination rather than one ambiguous status called complete.''')}

REPLACE={
'D-01':'''AWS DevOps Agent is a managed operational service. An Agent Space is the configuration boundary through which administrators connect infrastructure, tools, and people. The individual agents operating within that space perform different jobs: an incident investigation examines a particular problem, managed learning develops environment-specific context, and a custom agent follows the system prompt and tool selection configured for a recurring or on-demand task. A space is therefore not itself an investigation, and a saved custom-agent definition is not a completed report. [DS02] [DS06] [DS10]

An operator typically begins with a service and a time window. The relevant execution can query the authorized sources, compare observations, and present findings. The answer depends on what those sources expose and on the context available to the run. Configuring access to a monitoring provider does not manufacture missing logs, and retaining an earlier diagnosis does not make it the cause of the next alert.

![DevOps Agent logical architecture](../assets/diagrams/devops-architecture.svg)

The upper part of the architecture is configuration: account roles, provider registrations, Agent Space associations, instructions, and selected knowledge. The lower part is execution: a request or incident signal results in work that consumes evidence and produces an investigation or invocation record. The learning path produces retained context for later work. The arrows indicate documented logical relationships rather than an AWS internal deployment topology. [DS02] [DS06] [DS10]

The built-in functions include incident investigation, operational inquiries, and incident-prevention recommendations. Custom agents provide a way to define specialist work using selected tools, skills, and memory. A weekly health report is one application of that facility. Release-readiness review and active release testing are separate preview paths and should be evaluated independently of production-operations availability. [DS01] [DS18]

| Responsibility | Reusable capability | Principal objects | Next section |
|---|---|---|---|
| Access | Scope resource reads and operator entry | Account association; resource role; operator role | D-02 |
| Integration | Connect selected evidence and tool interfaces | Provider registration; association; tool selection | D-12, D-03 |
| Context | Discover resources and retain relevant knowledge | Topology; store; entry; version; active state | D-05, D-M01 |
| Behavior | Supply standing guidance and selected procedures | Instructions; skill; applicability | D-M03, D-M04 |
| Execution | Investigate incidents and run configured work | Triage; investigation; custom invocation; trigger | D-06, D-07 |
| Effects | Perform eligible approved changes | Elevated access; classification; approval | D-M06 |

The following chapter turns this model into a connection plan. Its integration inventory distinguishes telemetry reads, incident initiation, code and deployment context, and result publication before describing the MCP and private-network procedures.''',
'D-M01':'''Incident memory has a producer and a consumer. The producer synthesizes information from earlier work; the consumer is a later execution deciding which retained information is relevant. The managed monitors store records recurring-cause history for an alarm or metric, with evidence associated with earlier investigations. AWS describes a daily learning pass when the Agent Space has had investigations during the previous two weeks. Its retention and eviction behavior makes this a working operational memory, not an incident archive. [DS07]

![Incident-memory construction and retrieval](../assets/diagrams/devops-memory.svg)

At the beginning of a session, the agent receives store names and descriptions, rather than every stored file. It can select a relevant store, list its entries, evaluate their descriptions, and read the content it needs. A description is therefore part of the retrieval interface: an entry about inventory timeouts hidden behind an uninformative description may be available without being selected. The reviewed guidance describes progressive disclosure; it does not document a universal vector index, ranking algorithm, or customer-controlled model-training pipeline. [DS07]

Corrections provide a different input. Investigation feedback supplies the actual cause when a conclusion was wrong; the change guidance identifies reflections for that corrective context. The distinction is important operationally. Repeated appearances in history can establish a recurring theme, while a verified correction can explain why an earlier conclusion should not be repeated. Neither removes the need to read current telemetry. The feedback operation is described in D-M02. [DS08] [DS19]

To inspect the mechanism, open Knowledge, select Memories, and examine the relevant store and entry. Record its description, active state, version, and modification time. The monitor store is documented as enabled by default; individual availability still depends on activation, and custom-agent access additionally depends on attachment. The latter is configured in the custom-agent definition and is described in D-M07. [DS07] [DS10] [DS19]

For a recurring alarm, a useful response compares the previous cause with evidence from the new incident. In the worked example D-U01, healthy database metrics weaken the old database hypothesis while new upstream latency provides a different lead. A historical match should change where the investigation looks, not predetermine its conclusion.

There are also two meanings of recovery. Retrieving knowledge means making a relevant stored entry available to a current task. Restoring knowledge means recovering content after a change or loss. Versions allow inspection of earlier content and supported editing can create a corrected version; activation can make retained content available again. These controls are not evidence of an undocumented backup, undelete, or disaster-recovery service. Keep authoritative SOPs and configuration source in Git and keep incident evidence in its system of record. [DS07]''',
'F-01':'''AWS FinOps Agent combines authorized AWS data with an instance's organizational context to perform cost-related work. The instance is the durable configuration: it has an agent data role, operator access, files, memory, connections, and a task queue. A conversation or task is a particular execution within that instance. This distinction explains why a saved automation can create many tasks and why cancelling one task does not remove the automation. [FS02] [FS05] [FS08]

![FinOps Agent logical architecture](../assets/diagrams/finops-architecture.svg)

The architecture separates data retrieval from interpretation and publication. Upstream services return cost records, anomalies, recommendations, or change events. Organizational context gives those records a business meaning, such as which team owns an account. The agent can produce an answer or artifact and, through a configured integration, publish supported results. The permissions for retrieving evidence and those for publishing a result are not interchangeable. [FS01] [FS03] [FS12] [FS13]

Each instance has its own retained content and execution records. The data-protection guide describes persistent encrypted storage and an ephemeral runtime isolated per session. Files and memory can be loaded into that runtime for use, while conversation and task records are retained separately. The ephemeral runtime should not be mistaken for the only place the data exists. [FS08]

| Function | Required platform abilities | Detailed explanation |
|---|---|---|
| Cost inquiry | Authorized source queries and a defined comparison basis | F-M01 |
| Organizational reporting | Context-file retrieval, retained preferences, report generation | F-M02, F-M03, F-04 |
| Anomaly investigation | Monitor event, automation, queue, source evidence | F-M05 |
| Recommendation review | Upstream recommendation retrieval and workload context | F-M01, F-08 |
| Recurring delivery | Scheduled task creation and an appropriate destination | F-03, F-05, F-M06 |

Optimization recommendations originate from the documented upstream recommendation services. The agent's explanation can help a team interpret and route them, but it is not an independent measurement of realized savings. The next chapter identifies those sources and the permissions that make each one available. [FS01] [FS06]''',
'S-01':'''AWS Security Agent is organized around an application and the assessments performed against it. The Agent Space connects the application's sources and users. A saved penetration-test, code-review, or threat-model configuration describes reusable setup; a run records one assessment under particular conditions. Design review has a different one-off lifecycle. These distinctions matter when deciding what to update, repeat, or compare. [SS01] [SS03]

![Security Agent logical architecture](../assets/diagrams/security-architecture.svg)

The architecture has three kinds of input. Application sources provide implementation and design context. Security requirements state the criteria for eligible reviews. Target and credential configuration defines what a dynamic test may actually reach. Assessment results and findings belong to a particular execution, while the configured resources can be reused. Shared account registrations or requirement packs should not be mistaken for application-private resources merely because a run is attached to one space. [SS03] [SS30]

The product functions include application penetration testing, source-code review, design review, and threat modeling. Supporting capabilities supply source selection, authentication, reusable criteria, execution observation, proposed remediation, and revalidation. An assessment function is broader than any one mechanism. Login-procedure reuse, for example, supports authenticated testing but is not itself a substitute for that test. [SS01] [SS09]

| Responsibility | Principal resources | Explanation |
|---|---|---|
| Application and identity | Agent Space, user assignment, source connections | S-02, S-09 |
| Evidence and scope | Repository revision, documents, target and exclusions | S-M07, S-03 |
| Authentication | Credential definition, login instructions, learned login skill | S-M01, S-M02 |
| Criteria | Requirement and requirement pack | S-M03, S-M04 |
| Assessment | Saved configuration, run, work limit, logs | S-04 |
| Finding lifecycle | Finding, proposed repair, deployed revision, revalidation job | S-05, S-M05 |

A practical setup follows this resource model. Establish the intended user's access, connect the application's evidence, define the authorized target, and then select the assessment. The following integration inventory makes explicit which providers and resource types the service documents; the context chapter explains how their information is used.''',
'F-M03':'''Persistent memory allows a later session to use preferences and corrections supplied earlier. For example, a team may specify the owner of a set of accounts, a preferred reporting breakdown, or a recommendation category that needs special treatment. The service can retain that context and apply it to later questions or tasks. This is a different path from uploading an account-mapping file, and it is different again from summarizing old messages within one long conversation. [FS04]

![Reference files, memory, and the session runtime](../assets/diagrams/finops-context.svg)

The persistence boundary is the agent instance. The data-protection guide describes context and memory files in encrypted AWS-managed storage, loaded at session start into an isolated ephemeral runtime. Conversation and task records are retained alongside their own execution records. The guide does not establish a shared memory across instances or an automatic precedence rule that resolves conflicting statements in a file and a remembered preference. [FS08]

Operators manage conversational memory by asking the agent to remember, update, or forget a specific fact. Uploads remain operator-maintained files: a request to forget a preference is not an edit to a CSV containing the same information. When ownership changes, identify which representation is authoritative, update the file where appropriate, and correct the retained preference separately. Earlier reports remain historical artifacts rather than being silently rewritten. [FS04] [FS08]

A useful acceptance exercise uses a harmless preference, such as placing the comparison table before commentary. Set it, start a new conversation, and check whether it is applied. Correct or forget it and repeat. Test file retrieval with a different known fact. These observations distinguish successful application of retained context from an assumption about hidden model state. The procedure is a proposed test, not a result observed in an AWS account.

Recovery is object-specific. A soft-deleted context file can be restored through its workspace; memory can be corrected conversationally; earlier conversations and task records have the documented preview retention restrictions. None of these controls proves a general backup-and-restore capability for an entire instance. F-M07 describes the supported lifecycle actions. [FS08]'''}

LEADS={
'D-02':'Resource access lets an execution inspect infrastructure; operator access lets a person use the space. These paths are configured together during setup but fail independently. Establishing the distinction first makes a missing data result easier to diagnose than treating every failure as an agent problem.',
'D-03':'MCP connects the agent to a tool interface exposed by another system. The provider supplies the tool behavior; the Agent Space selects which tools the agent may call. Authentication establishes the calling identity, while the selected tool set constrains the available operations.',
'D-04':'A private integration requires a working route as well as valid credentials. The endpoint address identifies the service, whereas the private connection provides the network path to it. Authentication changes cannot repair a missing route or a blocked port.',
'D-05':'Topology is assembled from discovered resources and evidence of their relationships. It helps the agent connect a service to its deployment, repository, and dependencies. It is a representation of the environment, not the environment itself: an inferred edge can be wrong and an undiscovered resource can still be readable through an authorized tool.',
'D-M02':'A correction becomes useful only when it identifies what the original investigation got wrong and supplies the verified alternative. That is a different input from simply collecting another similar incident. The feedback path records that distinction so later work can treat a prior conclusion as corrected context.',
'D-M07':'A stored entry must be available to the particular execution before retrieval is possible. Availability depends on activation and, for custom agents, explicit store attachment. Versions then describe how the retained content has changed; they do not change which agent is allowed to access it.',
'D-M03':'Some guidance belongs in every new session, such as the format of an incident finding or the conventions used to name services. Standing instructions provide that context at startup. They are appropriate for persistent behavioral guidance rather than a procedure relevant only to one symptom.',
'D-M04':'A runbook describes a procedure for a recognizable situation. A skill packages that procedure with an applicability description so an agent can select it when the task matches. Consolidating SOPs therefore starts with resolving contradictory or stale procedures, not merely concatenating documents into a larger prompt.',
'D-06':'The first operational decision is whether a signal needs new work. Correlation can attach it to an existing investigation, and configured criteria can exclude it. Only after that routing decision should the operator interpret the investigation itself. A correction to routing is consequently different from feedback on a root-cause conclusion.',
'D-07':'A custom agent is a saved definition of specialist work. Its system prompt states the task, its selected tools provide the evidence or actions it can use, and its skills and store attachments supply procedures and context. An invocation executes that definition once; a trigger arranges future invocations.',
'D-M05':'Some investigations need computation on retrieved material rather than another prose response. Sandbox supplies an investigation-local environment for that purpose. Its package and network configuration governs what code can use, while the underlying source permissions remain separate.',
'D-M06':'An investigation can recommend a change before anyone authorizes it. Directed actions add an execution path for eligible changes, with enablement, access, tool classification, and approval as separate gates. The operator should be able to identify the exact operation and resource before the change is attempted.',
'D-08':'Programmatic configuration makes agent settings maintainable alongside other infrastructure definitions. It also requires attention to the resource being updated: changing asset metadata and replacing a preference map have different semantics. Reading the current state is therefore part of preparing a safe update.',
'D-09':'There are several directions of access around the service. An external client can call the agent, the agent can call an external tool, and an incident system can deliver a webhook. Release assurance adds another distinction between reviewing a proposed change and actively exercising a deployed application.',
'S-02':'An administrator prepares the application workspace; an operator performs assessments within it. Source-provider registration authorizes a provider account, while repository connection selects application material. Treat these as distinct setup milestones so an inaccessible repository is not confused with a user-access failure.',
'S-03':'A dynamic assessment is defined by what it may reach and what it may test. Some endpoints are application targets, while others are dependencies needed only for authentication or supporting content. Explicit exclusions keep that supporting access from expanding the test into an unintended environment.',
'S-M01':'Authentication has two stages. The service must obtain a valid test credential, then apply it through the application's login flow. The second stage may involve navigation and MFA even when the first stage is a straightforward secret read. The evidence should identify which stage succeeded.',
'S-M02':'Repeated authentication can reuse a procedure learned from an earlier successful login. This retained procedure concerns navigation through the login flow, not a standing proof that every later run reached the same application role. The role and protected routes remain part of assessment evidence.',
'S-M03':'Security criteria are useful only when their applicability is explicit. A rule about authorization of account-owned invoices should not be evaluated as though it governed every public handler. Requirement packs provide the criteria, while an eligible assessment supplies the evidence against which they are evaluated.',
'S-M04':'Generating criteria from policy documents is an administrative authoring operation. The generated pack needs review because policy language can be ambiguous and because replacement changes what later assessments evaluate. It is separate from evaluating a codebase against an already approved pack.',
'S-M06':'Encryption controls concern both key material and the identity requesting access. A valid key selected in a console is not sufficient when the relevant runtime or asynchronous identity lacks the required permission. The documented hierarchy explains which object each key protects and which policy path to inspect.',
'S-04':'A saved configuration describes how an assessment should run; a run describes what happened under those settings at a particular time. Reuse saves setup effort but does not freeze the target application, source revision, or credentials. Those inputs still need to be identified for each execution.',
'S-05':'A finding begins an engineering decision rather than ending it. Its evidence identifies the affected behavior or code, a proposed repair changes a revision, and deployment makes that revision available to a later test. Linking these objects prevents an unmerged patch from being recorded as a resolved application defect.',
'S-M05':'Revalidation answers a narrower question than a new assessment: can the selected existing finding still be reproduced under the current test configuration? It preserves the original finding and creates a new execution record, allowing the team to inspect what changed between observations.',
'S-06':'Code, design, and threat-model reviews examine different representations of an application. Their inputs and resource lifecycles therefore differ. Source analysis should identify the exact revision; design review should identify the document being reviewed; threat modeling should establish the intended system boundary before assessing individual threats.',
'F-02':'FinOps setup separates the person who administers the service, the identity used for data access, and the people who use the web application. A successful setup performed by an administrator does not prove that a regular operator can enter the agent or that the agent can read every required cost source.',
'F-M01':'A cost question becomes a set of data queries with a specific comparison basis. The returned amounts, recommendations, and change records then support different conclusions. Reproducing the amount is the first step; explaining its cause requires additional evidence.',
'F-05':'Publication starts with a registered provider and an agent-specific destination. The registration establishes authorization to a Jira site or Slack workspace. The connection selects the project or channel used by one agent, so its state and audience must be checked separately from registration.',
'F-M02':'Reference files let the agent interpret account identifiers and costs in the organization's terms. Their value depends on curation: a small current ownership mapping is more useful than a collection of contradictory copies. The operator maintains these files and decides which versions are active.',
'F-M04':'A long conversation has a different lifecycle from persistent memory. As earlier messages are summarized, the session preserves a condensed working context rather than every word of the exchange. Important comparison assumptions should therefore remain explicit in the current task and its authoritative reference material.',
'F-03':'Tasks provide execution records for requested work. Automations are definitions that create tasks later, either on a schedule or from a supported event. Their separate lifecycles explain why stopping future task creation does not remove a result that already exists.',
'F-M05':'An anomaly event is the beginning of an investigation path, not its conclusion. The monitor produces the event, a managed rule and matching automation create work, and the task queue records execution. Publication follows only after a result exists and the destination path succeeds.',
'F-04':'A report is a presentation of an analysis, not another source of cost truth. Its usefulness depends on preserving the comparison basis and making the relevant calculations traceable. The artifact and the task that produced it should therefore remain linked when the report is revised or shared.',
'F-M06':'Publication authorization depends on both the destination and the way work was initiated. An unattended automation can carry authorization established during setup, while an interactive Jira action requests approval. Slack posting follows a different documented behavior, so a single blanket approval statement would be misleading.',
'F-M07':'Stopping work, withdrawing active context, and removing retained data are different intentions. The service offers object-specific controls for those intentions. Choosing the correct operation requires knowing whether the object is an execution, a future trigger, a reference file, or a published artifact.',
'A-01':'A comparison begins with the objects each product actually exposes. The three services all separate configuration from execution, but their scopes and resource relationships are not interchangeable. The table below compares those documented objects without proposing a new universal agent schema.',
'A-02':'Knowledge has a producer, an owner, and a retrieval path. A DevOps monitor entry is synthesized from investigations; a Security login skill comes from successful navigation; a FinOps reference file is uploaded by an operator. Comparing these paths is more informative than asking whether all three products have memory.',
'A-03':'Reachability, identity, and authorization are different boundaries. A route makes an endpoint reachable, credentials identify a caller, and permissions constrain the operation. The execution must satisfy each applicable boundary; a successful check at one layer does not establish the others.',
'A-04':'The effect of an operation determines which controls matter. Reading a metric, posting an issue, changing a resource, and sending an active application test request have different consequences. The comparison should follow those effects rather than assign a single read-only or autonomous label to an entire service.',
'A-05':'The lifecycle of a saved definition differs from the lifecycle of the executions it creates. Disabling a schedule affects future work, while cancellation concerns an existing execution. Artifacts and external messages may remain after either operation. This distinction is central to a maintainable operating procedure.',
'A-06':'A team handoff transfers evidence and a decision to another owner. It does not need to transfer an agent's credentials, memory, or approval authority. A useful handoff therefore identifies the source objects and unresolved questions so the next specialist can reconstruct the relevant context.'}

EXTRA_REFS={
'devops':{'DS30':'https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html','DS31':'https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html','DS32':'https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html','DS33':'https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html'},
'security':{'SS30':'https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html','SS31':'https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html','SS32':'https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html','SS33':'https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html','SS34':'https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html'},
'finops':{},
'architecture':{'AS30':'https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html','AS31':'https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html','AS32':'https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html'}}

CHAPTER_NAMES={
'devops':['Service architecture','Data sources and integration configuration','Knowledge and execution context','Incident response and operational work','Recurring-alarm analysis','Troubleshooting and operating limits','Documentation coverage'],
'security':['Service architecture','Application sources and target access','Application knowledge and assessment criteria','Assessment and finding workflows','Authorization-finding analysis','Troubleshooting and operating limits','Documentation coverage'],
'finops':['Service architecture','Cost-data sources and collaboration connections','Organizational knowledge and session context','Tasks, reporting, and data lifecycle','Cost-variance analysis','Troubleshooting and operating limits','Documentation coverage'],
'architecture':['Agents and resource models','Integration and authorization boundaries','Execution lifecycles and evidence handoffs','Cross-platform worked example','Documentation coverage']}
PURPOSES={
'devops':['The service separates durable configuration from operational executions. This chapter establishes those objects before following their connections to evidence and retained knowledge.','An investigation can use only the evidence exposed through its configured access paths. Start with the supported connection families, then distinguish operator roles, provider authorization, selected tools, and private routing.','Current observations and retained information play different roles in a diagnosis. Discovery builds an environment model; learning produces memories; instructions and skills supply guidance. The following sections explain their producers and retrieval paths.','With access and context configured, a signal can be routed into an investigation or a defined operational task. This chapter follows execution, observation, and the additional controls required for computation or state-changing actions.','The same symptom can have a different cause in a later incident. The following synthetic evidence shows how a useful investigation challenges historical context with current measurements.','Failures can occur before analysis begins: identity, routing, tool selection, and quotas all matter. Diagnose the first failed prerequisite before changing the investigation hypothesis.','The references identify the documented behaviors used in this guide and the procedures that remain linked rather than reproduced.'],
'security':['The application space, assessment configuration, and run have different responsibilities. Establishing that model makes later findings and revalidation records interpretable.','Application evidence and a reachable test target are separate prerequisites. The source inventory is followed by user access and the explicit boundaries of a dynamic test.','Source context explains the application, requirements supply criteria, and authentication provides a reachable identity. Their reuse mechanisms differ and are described separately.','A run produces findings under particular conditions. Proposed changes, deployed revisions, and subsequent verification remain linked but distinct steps in the engineering workflow.','The synthetic example follows one account-authorization defect from the original observation to a deployed repair and scoped revalidation.','An incomplete assessment may reflect an inaccessible source, failed authentication, a wrong criterion, or an execution limit. These cases require different corrective actions.','The source register separates documented product behavior from authored engineering examples and identifies linked procedures.'],
'finops':['The instance persists configuration and context; conversations and tasks perform individual pieces of work. The resource model explains which state belongs to each.','A cost conclusion depends on its source data and query basis. Collaboration destinations add a separate publication path with its own authorization and lifecycle.','Uploaded mappings, retained preferences, and summarized conversations are different representations of organizational context. The operator must know which representation to correct.','Requests and automations create executions; executions produce results and artifacts. This chapter follows that sequence through publication and the supported retention controls.','The synthetic example reconciles the monetary change before using limited operational evidence to explain only part of it.','A numerical disagreement, a missing task, and a failed publication are different faults. Troubleshooting follows the corresponding data, execution, and destination paths.','The references document the source, context, task, and publication behaviors discussed here; unexecuted examples remain explicitly labeled.'],
'architecture':['An agent is an execution model, while an Agent Space or instance is a product-specific configuration resource. The comparison starts with these distinctions and then examines retained context.','An integration connects a source, trigger, target, or destination. The permitted direction and effect determine the relevant network and authorization controls.','A definition, execution, retained artifact, and external record have separate lifecycles. Team handoffs preserve their identities rather than collapsing them into one status.','The worked example assigns different questions to the three services while retaining the source identity and verification responsibility for each.','These diagrams and comparisons are logical explanations of documented behavior, not assertions about undisclosed runtime architecture.']}

DIAGRAM_SECTIONS={'D-06':'devops-incident','D-07':'devops-reporting','S-M01':'security-authentication','S-M05':'security-revalidation','F-M05':'finops-automation'}

def apply():
    guides={k:parse_source((ROOT/f'guides/{k}.md').read_text()) for k in DECKS}
    # Preserve the original detailed procedures, while replacing the lead explanations and every section title.
    for key,g in guides.items():
        g['intro']=INTRO[key]
        for sid,s in g['sections'].items():
            s['title']=TITLES.get(sid,s['title'])
            body=REPLACE.get(sid,s['body'])
            body=re.sub(r'```text\n.*?```\n*','',body,flags=re.S)
            body=body.replace('This table is an index, not a second capability database. The referenced sections are the canonical explanations.','')
            if sid in LEADS:body=LEADS[sid]+'\n\n'+body
            if sid in DIAGRAM_SECTIONS:body='![Workflow: '+s['title']+'](../assets/diagrams/'+DIAGRAM_SECTIONS[sid]+'.svg)\n\n'+body
            if sid=='D-07':body+='\n\nThe CronSchedule API reference specifies a flexible scheduling window of up to 30 minutes for trigger-created custom-agent schedules. A cron expression anchors that window; it is not a guarantee of exact-minute start or completion. Keep telemetry resolution, report lookback window, trigger window, and execution duration separate. For a time-critical incident bulletin, use an explicit on-demand request or a separately engineered trigger path whose latency you test. [DS33]'
            if sid=='D-M03':body=body.replace('## Incident output contract','## Incident reporting instructions')
            if sid=='F-04':body=body.replace('editable PowerPoint','presentation formats documented by the service')
            s['body']=body.strip();s['level']=3
        for sid,(title,body) in ADDITIONS.items():
            if sid[0]==DECKS[key]['prefix']:g['sections'][sid]={'id':sid,'title':title,'body':body,'level':3}
        for sid,url in EXTRA_REFS[key].items():g['refs'][sid]=url
        g['definitions']='\n'.join('['+sid+']: '+url for sid,url in g['refs'].items())
        for i,c in enumerate(CHAPTERS[key]):c['title']=CHAPTER_NAMES[key][i];c['purpose']=PURPOSES[key][i]
    CHAPTERS['devops'][1]['sections'].insert(0,'D-12')
    CHAPTERS['security'][1]['sections'].insert(0,'S-09')
    CHAPTERS['security'][2]['sections'].insert(0,'S-M07')
    CHAPTERS['finops'][1]['sections'].insert(0,'F-08')
    CHAPTERS['architecture'][0]['sections'].insert(0,'A-00')
    CHAPTERS['architecture'][1]['sections'].insert(0,'A-08')
    TYPES.update({'D-12':'reference','S-09':'reference','F-08':'reference','A-00':'overview','A-08':'reference'})
    for k,g in guides.items():(ROOT/f'guides/{k}.md').write_text(group_markdown(k,g))
    # The next preparation step relocates these maintained source modules.
    structure=(ROOT/'tools/docs_structure.py')
    structure.write_text('"""Chapter membership and record types for the maintained guides."""\nREVISION="2026-10-22-narrative-guides"\nBASELINE="c3d6f2dafdd87e083989135690e2f4f169e80fc2"\nCHAPTERS='+repr(CHAPTERS)+'\nDECK_CHAPTERS='+repr(DECK_CHAPTERS)+'\nTYPES='+repr(TYPES)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n')
    reviews=[]
    for k,refs in EXTRA_REFS.items():
        for sid,url in refs.items():reviews.append({'id':sid,'guide':k,'url':url,'reviewed_on':'2026-10-22','scope':'New integration, execution-model, or schedule explanation; not a whole-service audit.'})
    (ROOT/'qa/source-review.json').write_text(json.dumps({'date':'2026-10-22','new_references':reviews,'retained_reference_status':'Earlier source register retained; key memory, context, and authentication pages selectively rechecked. No live service test.'},indent=2)+'\n')
    Path(__file__).unlink()

if __name__=='__main__':apply()
