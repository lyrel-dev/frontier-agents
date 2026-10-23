# Cross-service architecture: presentation notes



Presentation: 27 minutes, including 4 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. An agent is an executor, not the surrounding workspace

00:00–03:00 · Agents and their operating context

Start with the simple execution cycle, then identify the actual nouns of each service. This is an explanatory comparison, not a common AWS resource type or a universal internal agent framework.



Concept | Meaning in this collection | Example

Agent | A configured or managed AI executor using permitted operations and context | DevOps managed role or custom definition

Execution | One scoped piece of work and its evidence | Investigation, assessment run or task

Context | Information and procedures made available through product-specific paths | Skill, application context or uploaded cost mapping

Workspace | Configuration and access scope around work | Operational Agent Space, application Agent Space or FinOps instance

Result | A produced record that still needs interpretation | Diagnosis, finding or report


Detailed reference: [From one agent execution to product-specific workflows](../guides/architecture.html#A-90)



Detailed reference: [Agents, tools, context, and executions](../guides/architecture.html#A-00)


## 02. The agent execution cycle

03:00–06:00 · Agents and their operating context

A request supplies scope; applicable context informs an execution; authorized operations return observations; the execution produces a result or another step. Retention and action approval are separate product-specific paths. This logical cycle does not disclose the foundation model or internal orchestration implementation.



![Agent execution and evidence cycle](../assets/diagrams/agent-execution.svg)



Detailed reference: [From one agent execution to product-specific workflows](../guides/architecture.html#A-90)



Detailed reference: [Agents, tools, context, and executions](../guides/architecture.html#A-00)


## 03. Context and control differ between the three products

06:00–09:00 · Agents and their operating context

Do not carry the DevOps meaning of skills or custom agent into the other two products. Similar responsibilities can be implemented through different configuration objects and lifecycle rules.



Concern | DevOps | Security | FinOps

Behavior | Managed instructions or custom prompt | Assessment settings and criteria | Request, task instructions and context files

Reusable context | Skills and selected memory | Application context, requirements and specific retained state | Files, persistent memory and conversation summary

Execution | Managed investigation or custom invocation | Assessment-specific run or one-off review | Conversation or explicit queued task

Scope | Operational Agent Space | Application Agent Space with shared settings | Agent instance and destination connections


Detailed reference: [From one agent execution to product-specific workflows](../guides/architecture.html#A-90)



Detailed reference: [Knowledge construction and retrieval models](../guides/architecture.html#A-02)



Detailed reference: [Capabilities, product features, and mechanisms](../guides/architecture.html#A-12)


## 04. Three different meanings of coordination

09:00–12:00 · Coordination, boundaries and evidence

The term multi-agent must not collapse these cases. Explain exactly what passes: a signal, a retained entry, a finding identity, an event, or a team-owned handoff. Where the service does not document the internal graph, leave it unspecified.



Level | Documented or authored relationship | Boundary

Inside DevOps incident work | Managed roles contribute to an investigation; Learning supplies later context | No customer-authored internal routing graph is implied

Within a Security or FinOps workflow | Linked assessments/results or automation-created tasks | Not a documented roster of DevOps-style peer agents

Across the three products | A team transfers explicit evidence and a new request | Separate identities, scope and authorization

Acceptance | A reviewer checks the receiving work against its own criteria | A generated summary is not a transferred approval


Detailed reference: [Coordination within a service and handoff between services](../guides/architecture.html#A-91)



Detailed reference: [Product specialization and use-case traceability](../guides/architecture.html#A-11)



Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)


## 05. Cross-service evidence handoff

12:00–15:00 · Coordination, boundaries and evidence

A team may use an incident investigation to frame a security assessment or a cost inquiry. The handoff carries evidence identities, target revision, period, question and owner. It does not transfer credentials, permissions or an established root cause.



![Team-managed evidence handoff](../assets/diagrams/shared-handoff.svg)



Detailed reference: [Coordination within a service and handoff between services](../guides/architecture.html#A-91)



Detailed reference: [Cross-team evidence handoffs](../guides/architecture.html#A-06)



Detailed reference: [Integration direction and evidence ownership](../guides/architecture.html#A-08)


## 06. Controls follow the effect

15:00–18:00 · Coordination, boundaries and evidence

Network reachability and instruction text do not establish authorization. Conversely, an approved effect still requires the correct technical identity. Show how each control belongs to the operation rather than to a vague autonomy level.



Effect | Control to identify | Evidence to retain

Read source data | Source identity, permission and network path | Actual source result and scope

Change infrastructure | Directed-action configuration and applicable approval | Requested parameters, attribution and resulting state

Exercise an application | Authorized target, test identity and exclusions | Run, tested revision and observations

Publish externally | Destination and invocation-specific rule | Actual issue, comment or message result

Accept a conclusion | Independent engineering or financial review | Acceptance verdict and unresolved questions


Detailed reference: [Authorization of state-changing operations](../guides/architecture.html#A-04)



Detailed reference: [Network, identity, and tool-access boundaries](../guides/architecture.html#A-03)


## 07. A use case applies platform facilities to a defined objective

18:00–21:00 · Apply the model to approved operational work

Use the frozen use cases to apply—not redefine—the concepts. A configuration recipe is a way to supply environment-specific choices for an objective. It is not an AWS facility or a new type of agent.



Example | Facilities used | Completion evidence

Service-health report | Current source reads; optional context; optional custom schedule | Measurements, interval and explicit gaps

Finding revalidation | Original finding; deployed repair; configured test identity | Revalidation result under stated conditions

Cost anomaly investigation | Anomaly, cost queries and optional change evidence | Reconciled contribution and causal limits

Operational review | Reviewed outputs and team-owned decisions | Owners, actions and criteria for closure


Detailed reference: [Operational objectives and implementation dependencies](../guides/architecture.html#A-09)



Detailed reference: [From one agent execution to product-specific workflows](../guides/architecture.html#A-90)


## 08. Exercise: one event, three independently scoped inquiries

21:00–25:00 · Apply the model to approved operational work

Use the supplied tabletop. The same event can motivate three questions without establishing one shared cause or one shared execution. Ask the audience which facts are transferred and which must be verified again by the receiving workflow.



0–1 min | Define the observation | Service symptom, revision and observation period

1–2 min | Assign incident work | Current evidence and unresolved dependencies

2–3 min | Define Security and FinOps questions | Authorized target/revision and comparable cost basis

3–4 min | Record handoff and acceptance | Separate owners, permissions and verification criteria


Detailed reference: [Cross-platform operational review: worked example](../guides/architecture.html#A-U01)



Detailed reference: [Coordination within a service and handoff between services](../guides/architecture.html#A-91)


## 09. Reading path after the presentation

25:00–27:00 · Apply the model to approved operational work

The presentation builds the mental model and demonstrates its use. The guide retains detailed configuration, source qualifications and limits. Do not turn the reference taxonomy into the required teaching order.



Need | Read | Expected understanding

Understand one product | Agent overview, then capability chapters | Objects, context, access and work

Perform a task | Approved use-case page | Scope, workflow, configuration and acceptance

Inspect identity and ownership | Resource model | Product-specific objects and qualified relationships

Configure or troubleshoot | Detailed procedure and official reference | Actual controls, limits and expected observations


Detailed reference: [From one agent execution to product-specific workflows](../guides/architecture.html#A-90)



Detailed reference: [Capabilities, product features, and mechanisms](../guides/architecture.html#A-12)



Detailed reference: [Architecture assumptions and references](../guides/architecture.html#A-07)
