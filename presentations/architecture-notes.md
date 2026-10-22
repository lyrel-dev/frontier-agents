# Shared Architecture — HTML presentation reference



Open [architecture.html](architecture.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Comparison Framework

**Chapter:** Part I · Comparison Framework. **Schedule:** 00:00–02:00. **Slide budget:** 02:00.

Cross-platform comparison begins with the actual resource and execution model.



Question | DevOps Agent | Security Agent | FinOps Agent

Scope object | Agent Space | Application Agent Space plus shared resources | Agent instance

Configuration | Agents, tools and knowledge | Assessment definitions and criteria | Context, tasks, automations and connections

Execution | Investigation or invocation | Run, review or revalidation job | Conversation or task

Primary evidence | Tool results and investigation history | Findings and linked verification | Source query, task and artifact



**Guide:** [A-01](../guides/architecture.html#A-01)



## 2. Use Case Families Across the Three Platforms

**Chapter:** Part I · Comparison Framework. **Schedule:** 02:00–05:00. **Slide budget:** 03:00.

Similar business labels can map to different platform objects and authorization boundaries.



Family | DevOps Agent | Security Agent | FinOps Agent

Event response | Incident triage and investigation | Assessment run from configured target or source | Anomaly-triggered investigation

Recurring review | Health and operational review report | Scheduled assessment or review workflow | Cost and FinOps review report

Pattern analysis | Recurring causes and prevention recommendations | Requirement and finding trends | Cost drivers and optimization candidates

Documentation | Topology, SOP skills and environment memory | Threat model and requirement packs | Context files and report artifacts

Controlled effect | Directed resource action | Repository remediation or issue tracking | Jira/Slack publication; engineering change outside agent



**Guide:** [A-01](../guides/architecture.html#A-01), [A-07](../guides/architecture.html#A-07)



## 3. Resource and Context Models

**Chapter:** Part II · Resource, Context and Access. **Schedule:** 05:00–07:00. **Slide budget:** 02:00.

The three services do not expose one common memory mechanism.



Material | Producer | Consumer | Lifecycle distinction

Incident memory | Managed learning or corrective feedback | Relevant later investigation | Version, active state and bounded retention

Login procedure | Successful authenticated navigation | Later security test session | Configuration-specific reuse

Requirement pack | Administrator or document generation | Eligible design/code assessment | Enablement and replacement

Reference file | FinOps operator upload | Task or conversation | Soft delete and restore

Conversational memory | Explicit user request | Later FinOps session | Update or forget



**Guide:** [A-01](../guides/architecture.html#A-01), [A-02](../guides/architecture.html#A-02)



## 4. Connectivity, Identity and Authorization

**Chapter:** Part II · Resource, Context and Access. **Schedule:** 07:00–09:00. **Slide budget:** 02:00.

Reachability and prompt guidance do not establish authorization for an effect.



Connectivity | Can the endpoint, repository, account or application be reached?

Identity | Which operator, role, credential or application user authenticated?

Permission | Which read, test, publication or mutation operation is allowed?

Behavioral guidance | Which instructions, skills or prompt rules shape the work?



**Guide:** [A-03](../guides/architecture.html#A-03)



## 5. Execution and Approval Boundaries

**Chapter:** Part III · Execution, Lifecycle and Handoffs. **Schedule:** 09:00–11:00. **Slide budget:** 02:00.

Approval follows the concrete effect; there is no universal human-approved agent mode.



Effect | Required control | Evidence

AWS resource mutation | Specific directed-action enablement, role and approval | Approval and resulting resource state

Application security testing | Authorized target, credentials, exclusions and stop owner | Run identity, requests and findings

Repository change | Provider access and normal code-review controls | Patch, pull request, tests and reviewer

Jira or Slack publication | Destination and invocation-specific rule | Issue/comment/post and task history

Recommendation only | No execution authority | Proposal and acceptance criteria



**Guide:** [A-04](../guides/architecture.html#A-04)



## 6. Configuration, Execution and Artifact Lifecycles

**Chapter:** Part III · Execution, Lifecycle and Handoffs. **Schedule:** 11:00–13:00. **Slide budget:** 02:00.

Stopping future starts does not reverse completed effects or delete retained evidence.



Layer | Create or configure | Stop or remove | What may remain

Configuration | Agent, assessment, automation or connection | Disable, detach or delete | Prior executions and outputs

Future execution | Schedule or event trigger | Pause/disable/delete trigger | Existing tasks or runs

Current execution | Invocation, assessment or task | Cancel or stop where supported | Partial results and audit history

Retained context | Memory, requirement or file | Deactivate, replace, forget or soft-delete | Versions or recoverable data

External artifact | Ticket, message or exported report | Destination-specific removal | Copies outside the platform



**Guide:** [A-05](../guides/architecture.html#A-05)



## 7. Handoff Record Between Platforms and Teams

**Chapter:** Part III · Execution, Lifecycle and Handoffs. **Schedule:** 13:00–15:00. **Slide budget:** 02:00.

A handoff transfers evidence and responsibility, not credentials or authorization.



Field | Required content | Reason

Origin | Platform, configuration and execution identifiers | Trace the producing context

Subject | Service, revision, target and UTC window | Avoid ambiguous scope

Evidence | Source links, findings, totals and failed reads | Support independent review

Request | Question, owner, deadline and permitted effect | Bound the receiving work

Acceptance | Required check and unresolved questions | Prevent generated text from becoming automatic closure



**Guide:** [A-06](../guides/architecture.html#A-06)



## 8. Tabletop: One Operational Symptom, Three Different Jobs

**Chapter:** Part IV · Tabletop. **Schedule:** 15:00–19:00. **Slide budget:** 04:00.

The same business event creates different evidence obligations for each platform.



0–1 min | Define the observation | Latency, application revision, authorization identity and cost window

1–2 min | Assign DevOps work | Investigate current service evidence and dependency path

2–3 min | Assign Security and FinOps work | Assess the authorized application change; reconcile related cost movement

3–4 min | State unresolved questions | No single shared root cause or cross-agent runtime is assumed



**Guide:** [A-U01](../guides/architecture.html#A-U01)



## 9. Documentation and Presentation Acceptance Criteria

**Chapter:** Part V · Acceptance Criteria. **Schedule:** 19:00–22:00. **Slide budget:** 03:00.

A presentation is an indexed technical explanation, not a sequence of slogans.



Area | Acceptance criterion | Failure signal

Structure | Resource model, capabilities, use cases, mechanisms and procedures are distinct | A scenario is labeled as a capability

Use case catalog | Grouped, searchable and classified by delivery mode and availability | Duplicated or unclassified entries

Procedure | Prerequisite, decision, confirmation and failure interpretation are present | Generic “configure and verify” language

Presentation | Descriptive chapter titles and evidence-bearing slides | Slogan titles and empty visual panels

Evidence | Material product claims link to official guidance | Source count used as proof of completeness

Validation | Browser, data and link checks are separated from live product testing | Packaging checks presented as operational proof



**Guide:** [A-07](../guides/architecture.html#A-07)
