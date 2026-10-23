# Cross-service architecture: presentation notes



Presentation: 38 minutes, including 4 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. Concept ownership and resource identity

00:00–03:00 · Concept ownership and product resource models

Blue, green and orange classify concept ownership. Resource kind and source qualification prevent false equivalence.



Class | What it defines | Examples | Interpretation

Documentation-defined | How the reference explains operational work | Use case; mechanism explanation; implementation profile | Not an AWS resource or SDK payload

AWS-defined resource | A documented service facility | Agent Space; assessment configuration; automation | Use the exact product namespace and lifecycle

AWS-defined state or view | A documented representation or component | Topology; retained login procedure; conversation summary | Do not invent independent CRUD operations

External or engineering-owned | Original system or accepted artifact | Repository revision; deployed target; Jira issue; review | Preserve source identity and independent authorization


Detailed reference: [Concept ownership and the approved entity model](../guides/architecture.html#A-10)


## 02. Product-specific configuration and execution models

03:00–06:00 · Concept ownership and product resource models

Similar responsibilities do not imply interchangeable resources, permissions or deletion behavior.



Responsibility | DevOps | Security | FinOps

Scope | Operational Agent Space | Application Agent Space; shared requirements | Independent instance; finops-agent AgentSpace IAM name

Reusable definition | Custom agent; skill; test profile | Assessment-specific configuration | Automation; instance settings

Execution | Investigation; invocation; Learning run | Run; one-off design review; revalidation job | Conversation work; task

Retained context | Stores, memories and versions | Application context; requirements; login procedure | Files; persistent memory; conversation summary


Detailed reference: [Product specialization and use-case traceability](../guides/architecture.html#A-11)


## 03. Agent execution and evidence cycle

06:00–08:00 · Concept ownership and product resource models

A task and its configuration guide an execution. Authorized tools return observations. Those observations can lead to another step or a result. Retention is a separate, product-specific path.



![Agent execution and evidence cycle](../assets/diagrams/agent-execution.svg)



Detailed reference: [Agents, tools, context, and executions](../guides/architecture.html#A-00)


## 04. Retained context: producers, consumers, and lifecycle

08:00–10:00 · Concept ownership and product resource models

The three services do not expose one common memory mechanism.



Material | Producer | Consumer | Lifecycle distinction

Incident memory | Managed learning or corrective feedback | Relevant later investigation | Version, active state and bounded retention

Login procedure | Successful authenticated navigation | Later security test session | Configuration-specific reuse

Requirement pack | Administrator or document generation | Eligible design/code assessment | Enablement and replacement

Reference file | FinOps operator upload | Task or conversation | Soft delete and restore

Conversational memory | Conversation preferences, corrections and task outcomes | Later FinOps session | Update or forget


Detailed reference: [Resource identity across service boundaries](../guides/architecture.html#A-01)



Detailed reference: [Knowledge construction and retrieval models](../guides/architecture.html#A-02)


## 05. Operational objectives, mechanisms and features

10:00–12:00 · Concept ownership and product resource models

The use case supplies the objective and completion criteria. Each workflow step links to a mechanism and its product feature. The implementation profile supplies environment-specific configuration and verification steps.



![Outcome, workflow, mechanism, and feature relationships](../assets/diagrams/workflow-feature-map.svg)



Detailed reference: [Capabilities, product features, and mechanisms](../guides/architecture.html#A-12)



Detailed reference: [Operational objectives and implementation dependencies](../guides/architecture.html#A-09)


## 06. Service-health reporting: required and conditional dependencies

12:00–15:00 · Concept ownership and product resource models

A missing required data source blocks the corresponding conclusion. Optional history changes the available context. Schedule and destination dependencies apply only to profiles that enable them.



Element | Purpose | Configuration and evidence

Current telemetry | Required basis for the health conclusion | Selected source tools; verify period and material measurement.

Historical context | Optional interpretation of prior behavior | Available relevant memory; distinguish retrieval from correctness.

Recurring execution | Conditional on the chosen reporting profile | Configured trigger; timing and measurement window differ.

External destination | Optional publication effect | Destination-specific authorization and delivery result.


Detailed reference: [Operational objectives and implementation dependencies](../guides/architecture.html#A-09)



Detailed reference: [Knowledge construction and retrieval models](../guides/architecture.html#A-02)



Detailed reference: [Authorization of state-changing operations](../guides/architecture.html#A-04)


## 07. Use case families across the three platforms

15:00–18:00 · Concept ownership and product resource models

Similar business labels can map to different platform objects and authorization boundaries.



Family | DevOps Agent | Security Agent | FinOps Agent

Event response | Incident triage and investigation | Assessment run from configured target or source | Anomaly-triggered investigation

Recurring review | Health and operational review report | Scheduled assessment or review workflow | Cost and FinOps review report

Pattern analysis | Recurring causes and prevention recommendations | Finding personalization; cross-run trend analysis is team-composed | Cost drivers and optimization candidates

Documentation | Topology, SOP skills and environment memory | Threat model and requirement packs | Context files and report artifacts

Controlled effect | Directed resource action | Repository remediation or issue tracking | Jira/Slack publication; engineering change outside agent


Detailed reference: [Resource identity across service boundaries](../guides/architecture.html#A-01)



Detailed reference: [Architecture assumptions and references](../guides/architecture.html#A-07)



Detailed reference: [Knowledge construction and retrieval models](../guides/architecture.html#A-02)


## 08. Team-managed evidence handoff

18:00–20:00 · Integration and authorization boundaries

An operational finding can become input to separate security and cost work. Each receiving service uses its own configuration and authorization; only identifiers, evidence references, and decisions are handed over.



![Team-managed evidence handoff](../assets/diagrams/shared-handoff.svg)



Detailed reference: [Integration direction and evidence ownership](../guides/architecture.html#A-08)



Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 09. Connectivity, identity and authorization

20:00–22:00 · Integration and authorization boundaries

Reachability and prompt guidance do not establish authorization for an effect.



Connectivity | Can the endpoint, repository, account or application be reached?

Identity | Which operator, role, credential or application user authenticated?

Permission | Which read, test, publication or mutation operation is allowed?

Behavioral guidance | Which instructions, skills or prompt rules shape the work?


Detailed reference: [Network, identity, and tool-access boundaries](../guides/architecture.html#A-03)


## 10. Execution and approval boundaries

22:00–24:00 · Integration and authorization boundaries

Approval follows the concrete effect; there is no universal human-approved agent mode.



Effect | Required control | Evidence

AWS resource mutation | Specific directed-action enablement, role and approval | Approval and resulting resource state

Application security testing | Authorized target, credentials, exclusions and stop owner | Run identity, requests and findings

Repository change | Provider access and normal code-review controls | Patch, pull request, tests and reviewer

Jira or Slack publication | Destination and invocation-specific rule | Issue/comment/post and task history

Recommendation only | No execution authority | Proposal and acceptance criteria


Detailed reference: [Authorization of state-changing operations](../guides/architecture.html#A-04)


## 11. Operational prerequisites and verification records

24:00–27:00 · Integration and authorization boundaries

Check access, execution scope, context, effects, and result evidence separately. Record unmet prerequisites and unresolved results before handing work to the next owner.



Check | Record to inspect | Failure interpretation

Source access | Calling identity, selected operation and returned resource | An inaccessible source leaves an evidence gap.

Execution scope | Configuration ID, revision, target and observation period | A completed run against the wrong subject is not acceptance.

Retained context | Applicable file, memory or procedural state | Availability and observed use are separate checks.

State-changing operation | Target, permitted effect and required approval | A generated recommendation is not authorization.

Result and handoff | Source references, execution ID, reviewer and unresolved items | Completion and delivery do not establish correctness.


Detailed reference: [Network, identity, and tool-access boundaries](../guides/architecture.html#A-03)



Detailed reference: [Authorization of state-changing operations](../guides/architecture.html#A-04)



Detailed reference: [Configuration, execution, and artifact lifecycles](../guides/architecture.html#A-05)



Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 12. Operational-review profiles and evidence handoffs

27:00–30:00 · Execution lifecycles and evidence handoffs

The reliability profile uses service measurements and incident records. The cost profile uses reconciled amounts and recommendations. Both produce decisions, assigned owners, and unresolved evidence requests; neither transfers service permissions.



Profile | Reviewed inputs | Review outcome

Reliability | Health, deployments, incident patterns and prevention proposals | Priorities, owners and evidence needed for closure.

Cost management | Reconciled amounts, anomalies, recommendations and measured outcomes | Decisions with estimates separate from observed benefits.

Combined team review | Independently configured service results | Retained source identities; no shared credentials or approval.


Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)



Detailed reference: [Operational objectives and implementation dependencies](../guides/architecture.html#A-09)



Detailed reference: [Cross-platform operational review: worked example](../guides/architecture.html#A-U01)


## 13. Configuration, execution and artifact lifecycles

30:00–32:00 · Execution lifecycles and evidence handoffs

Stopping future starts does not reverse completed effects or delete retained evidence.



Layer | Create or configure | Stop or remove | What may remain

Configuration | Agent, assessment, automation or connection | Disable, detach or delete | Prior executions and outputs

Future execution | Schedule or event trigger | Pause/disable/delete trigger | Existing tasks or runs

Current execution | Invocation, assessment or task | Cancel or stop where supported | Partial results and audit history

Retained context | Memory, requirement or file | Deactivate, replace, forget or soft-delete | Versions or recoverable data

External artifact | Ticket, message or exported report | Destination-specific removal | Copies outside the platform


Detailed reference: [Configuration, execution, and artifact lifecycles](../guides/architecture.html#A-05)


## 14. Handoff record between platforms and teams

32:00–34:00 · Execution lifecycles and evidence handoffs

A handoff transfers evidence and responsibility, not credentials or authorization.



Field | Required content | Reason

Origin | Platform, configuration and execution identifiers | Trace the producing context

Subject | Service, revision, target and UTC window | Avoid ambiguous scope

Evidence | Source links, findings, totals and failed reads | Support independent review

Request | Question, owner, deadline and permitted effect | Bound the receiving work

Acceptance | Required check and unresolved questions | Prevent generated text from becoming automatic closure


Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 15. Exercise: incident, security, and cost evidence handoff

34:00–38:00 · Cross-platform worked example

The same business event creates different evidence obligations for each platform.



0–1 min | Define the observation | Latency, application revision, authorization identity and cost window

1–2 min | Assign DevOps work | Investigate current service evidence and dependency path

2–3 min | Assign Security and FinOps work | Assess the authorized application change; reconcile related cost movement

3–4 min | State unresolved questions | No single shared root cause or cross-agent runtime is assumed


Detailed reference: [Cross-platform operational review: worked example](../guides/architecture.html#A-U01)
