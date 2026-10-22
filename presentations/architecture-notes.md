# Shared Architecture: presentation notes



Presentation: 26 minutes, including 4 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. Agent execution and evidence cycle

00:00–02:00 · Service architecture

A task and its configuration guide an execution. Authorized tools return observations. Those observations can lead to another step or a result. Retention is a separate, product-specific path.



![Agent execution and evidence cycle](../assets/diagrams/agent-execution.svg)



Detailed reference: [Agents, tools, context, and executions](../guides/architecture.html#A-00)


## 02. Comparison framework

02:00–04:00 · Service architecture

Cross-platform comparison begins with the actual resource and execution model.



Question | DevOps Agent | Security Agent | FinOps Agent

Scope object | Agent Space | Application Agent Space plus shared resources | Agent instance

Configuration | Agents, tools and knowledge | Assessment definitions and criteria | Context, tasks, automations and connections

Execution | Investigation or invocation | Run, review or revalidation job | Conversation or task

Primary evidence | Tool results and investigation history | Findings and linked verification | Source query, task and artifact


Detailed reference: [Workspace, configuration, and execution models](../guides/architecture.html#A-01)


## 03. Resource and context models

04:00–06:00 · Service architecture

The three services do not expose one common memory mechanism.



Material | Producer | Consumer | Lifecycle distinction

Incident memory | Managed learning or corrective feedback | Relevant later investigation | Version, active state and bounded retention

Login procedure | Successful authenticated navigation | Later security test session | Configuration-specific reuse

Requirement pack | Administrator or document generation | Eligible design/code assessment | Enablement and replacement

Reference file | FinOps operator upload | Task or conversation | Soft delete and restore

Conversational memory | Explicit user request | Later FinOps session | Update or forget


Detailed reference: [Workspace, configuration, and execution models](../guides/architecture.html#A-01)



Detailed reference: [Knowledge construction and retrieval models](../guides/architecture.html#A-02)


## 04. Team-managed evidence handoff

06:00–08:00 · Integrations and access

An operational finding can become input to separate security and cost work. Each receiving service uses its own configuration and authorization; only identifiers, evidence references, and decisions are handed over.



![Team-managed evidence handoff](../assets/diagrams/shared-handoff.svg)



Detailed reference: [Integration direction and evidence ownership](../guides/architecture.html#A-08)



Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 05. Connectivity, identity and authorization

08:00–10:00 · Integrations and access

Reachability and prompt guidance do not establish authorization for an effect.



Connectivity | Can the endpoint, repository, account or application be reached?

Identity | Which operator, role, credential or application user authenticated?

Permission | Which read, test, publication or mutation operation is allowed?

Behavioral guidance | Which instructions, skills or prompt rules shape the work?


Detailed reference: [Network, identity, and tool-access boundaries](../guides/architecture.html#A-03)


## 06. Execution and approval boundaries

10:00–12:00 · Execution workflows

Approval follows the concrete effect; there is no universal human-approved agent mode.



Effect | Required control | Evidence

AWS resource mutation | Specific directed-action enablement, role and approval | Approval and resulting resource state

Application security testing | Authorized target, credentials, exclusions and stop owner | Run identity, requests and findings

Repository change | Provider access and normal code-review controls | Patch, pull request, tests and reviewer

Jira or Slack publication | Destination and invocation-specific rule | Issue/comment/post and task history

Recommendation only | No execution authority | Proposal and acceptance criteria


Detailed reference: [Authorization of state-changing operations](../guides/architecture.html#A-04)


## 07. Configuration, execution and artifact lifecycles

12:00–14:00 · Execution workflows

Stopping future starts does not reverse completed effects or delete retained evidence.



Layer | Create or configure | Stop or remove | What may remain

Configuration | Agent, assessment, automation or connection | Disable, detach or delete | Prior executions and outputs

Future execution | Schedule or event trigger | Pause/disable/delete trigger | Existing tasks or runs

Current execution | Invocation, assessment or task | Cancel or stop where supported | Partial results and audit history

Retained context | Memory, requirement or file | Deactivate, replace, forget or soft-delete | Versions or recoverable data

External artifact | Ticket, message or exported report | Destination-specific removal | Copies outside the platform


Detailed reference: [Configuration, execution, and artifact lifecycles](../guides/architecture.html#A-05)


## 08. Handoff record between platforms and teams

14:00–16:00 · Execution workflows

A handoff transfers evidence and responsibility, not credentials or authorization.



Field | Required content | Reason

Origin | Platform, configuration and execution identifiers | Trace the producing context

Subject | Service, revision, target and UTC window | Avoid ambiguous scope

Evidence | Source links, findings, totals and failed reads | Support independent review

Request | Question, owner, deadline and permitted effect | Bound the receiving work

Acceptance | Required check and unresolved questions | Prevent generated text from becoming automatic closure


Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 09. Tabletop: one operational symptom, three different jobs

16:00–20:00 · Worked example

The same business event creates different evidence obligations for each platform.



0–1 min | Define the observation | Latency, application revision, authorization identity and cost window

1–2 min | Assign DevOps work | Investigate current service evidence and dependency path

2–3 min | Assign Security and FinOps work | Assess the authorized application change; reconcile related cost movement

3–4 min | State unresolved questions | No single shared root cause or cross-agent runtime is assumed


Detailed reference: [Cross-platform operational review: worked example](../guides/architecture.html#A-U01)


## 10. Use case families across the three platforms

20:00–23:00 · Troubleshooting and references

Similar business labels can map to different platform objects and authorization boundaries.



Family | DevOps Agent | Security Agent | FinOps Agent

Event response | Incident triage and investigation | Assessment run from configured target or source | Anomaly-triggered investigation

Recurring review | Health and operational review report | Scheduled assessment or review workflow | Cost and FinOps review report

Pattern analysis | Recurring causes and prevention recommendations | Requirement and finding trends | Cost drivers and optimization candidates

Documentation | Topology, SOP skills and environment memory | Threat model and requirement packs | Context files and report artifacts

Controlled effect | Directed resource action | Repository remediation or issue tracking | Jira/Slack publication; engineering change outside agent


Detailed reference: [Workspace, configuration, and execution models](../guides/architecture.html#A-01)



Detailed reference: [Architecture assumptions and references](../guides/architecture.html#A-07)


## 11. Documentation and presentation acceptance criteria

23:00–26:00 · Troubleshooting and references

A presentation is an indexed technical explanation, not a sequence of slogans.



Area | Acceptance criterion | Failure signal

Structure | Resource model, capabilities, use cases, mechanisms and procedures are distinct | A scenario is labeled as a capability

Use case catalog | Grouped, searchable and classified by delivery mode and availability | Duplicated or unclassified entries

Procedure | Prerequisite, decision, confirmation and failure interpretation are present | Generic “configure and verify” language

Presentation | Descriptive chapter titles and evidence-bearing slides | Slogan titles and empty visual panels

Evidence | Material product claims link to official guidance | Source count used as proof of completeness

Validation | Browser, data and link checks are separated from live product testing | Packaging checks presented as operational proof


Detailed reference: [Architecture assumptions and references](../guides/architecture.html#A-07)
