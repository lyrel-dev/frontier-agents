# AWS DevOps Agent: presentation notes



Presentation: 80 minutes, including 8 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. Agent Space, provider associations and custom invocations

00:00–02:00 · Workspace and resource organization

An Agent Space associates account roles and providers. A custom-agent definition selects tools and context; each invocation records a separate execution. Provider registration and space association are distinct configuration operations.



![DevOps Agent: scope, providers and execution](../assets/diagrams/er-devops-scope.svg)



Detailed reference: [Agent Spaces and AWS account scope](../guides/devops.html#D-01)


## 02. Agent Space, asset, and invocation identities

02:00–05:00 · Workspace and resource organization

Identify the actual product object before configuring, invoking, correcting or removing it. The resource kind determines which operation is meaningful.



Object | Identity or membership | Relationship to inspect

Agent Space | agentSpaceId and service scope | Account roles and selected associations

Service association | associationId and serviceId | Registered provider plus space-specific configuration

Custom definition | custom_agent assetId | Existing skill and memory-store asset IDs

Memory | Parent store and content version | Activation, attachment and observed retrieval

Invocation or investigation | Execution record and actual interval | Tool evidence, conclusion and any separate approval


Detailed reference: [Assets, identities, and configuration references](../guides/devops.html#D-13)


## 03. Memory stores, entries and definition references

05:00–08:00 · Workspace and resource organization

A custom definition references existing skill and memory-store assets. A store contains entries; updates create entry versions. Activation and attachment control availability, while retrieval occurs during execution.



![DevOps Agent: stored knowledge and configuration references](../assets/diagrams/er-devops-knowledge.svg)



Detailed reference: [Assets, identities, and configuration references](../guides/devops.html#D-13)


## 04. Managed agents and customer-defined agents

08:00–11:00 · Agent definition and customization

Agent definition specifies behavior and available resources. Trigger configuration specifies when the definition runs.



Control | Managed agent | Custom-agent definition

Lifecycle | Provided by AWS | Created and maintained by the customer

Behavior | Global and agent-specific instructions | Customer system prompt

Tools and skills | Platform-managed | Explicitly selected and assigned

Memory access | Applicable managed access | Explicit store attachments

Invocation | Managed workflow entry point | On demand, schedule, or webhook trigger


Detailed reference: [AWS-managed agents](../guides/devops.html#D-15)



Detailed reference: [Custom-agent definitions and configuration](../guides/devops.html#D-16)


## 05. Environment-knowledge consolidation

11:00–13:00 · Knowledge and behavioral context management

Discovery, connected evidence, and completed investigations feed distinct retained knowledge. A later execution selects the relevant context; it still reads current source evidence.



![Environment-knowledge consolidation](../assets/diagrams/devops-knowledge.svg)



Detailed reference: [Managed knowledge production and refresh](../guides/devops.html#D-M08)



Detailed reference: [Topology, environment summaries, and export](../guides/devops.html#D-05)


## 06. Memory production, availability and selective retrieval

13:00–15:00 · Knowledge and behavioral context management

Separate retained content, access to the entry, observable retrieval and the correctness of the new conclusion.



![Incident memory: production, availability and retrieval](../assets/diagrams/mechanism-devops-retrieval.svg)



Detailed reference: [Memory construction and progressive retrieval](../guides/devops.html#D-M01)



Detailed reference: [Corrective feedback and reflection memory](../guides/devops.html#D-M02)



Detailed reference: [Memory-store access, versions, and retention](../guides/devops.html#D-M07)


## 07. Memory, instructions and skills

15:00–18:00 · Knowledge and behavioral context management

Availability, selection and diagnostic influence are separate questions for retained context.



Mechanism | When loaded | Typical content | Lifecycle control

Managed memory | Selected by description during relevant work | Recurring causes and environment understanding | Version, active state and managed refresh

Custom memory | Selected after store attachment | Team or service context | Create, edit, deactivate, detach or delete

Corrective reflection | Future investigation of the alarm | Verified correction to an earlier diagnosis | Latest feedback and visible memory

Agent instructions | Every new applicable session | Standing policies and output rules | Edit and start a new session

Skill | When description and agent scope match | Specialized procedure and references | Edit description, content and targeting


Detailed reference: [Memory construction and progressive retrieval](../guides/devops.html#D-M01)



Detailed reference: [Corrective feedback and reflection memory](../guides/devops.html#D-M02)



Detailed reference: [Standing instructions and session initialization](../guides/devops.html#D-M03)



Detailed reference: [Skills, applicability, and supporting files](../guides/devops.html#D-M04)



Detailed reference: [Memory-store access, versions, and retention](../guides/devops.html#D-M07)


## 08. Incident pattern analysis and prevention recommendations

18:00–21:00 · Knowledge and behavioral context management

Incident pattern identification produces context and recommendations, not an automatically implemented fix.



Stage | Input | Output | Operator decision

Monitor memory refresh | Recent completed investigations | Monitor-specific recurring-cause context | Inspect version and relevance

Prevention evaluation | Multiple incident investigations | Observability, infrastructure, governance or code recommendations | Run, stop or wait for scheduled evaluation

Recommendation review | Incident evidence and expected impact | Keep, discard or implemented state | Assign owner and acceptance criteria

Corrective feedback | Verified diagnosis correction | Reflection for future investigations | Separate local learning from AWS sharing


Detailed reference: [Memory construction and progressive retrieval](../guides/devops.html#D-M01)



Detailed reference: [Corrective feedback and reflection memory](../guides/devops.html#D-M02)



Detailed reference: [Incident triage, investigation, and prevention](../guides/devops.html#D-06)


## 09. Operational knowledge and release assurance

21:00–24:00 · Knowledge and behavioral context management

SOP consolidation maintains reviewed procedural content. Topology documentation records discovered and inferred relationships. Release-readiness analysis and active testing apply to different subjects and have different effects.



Operational outcome | Completion evidence | Implementation boundary

Consolidate and maintain operational procedures | Conflicting or stale instructions are resolved. | Composed workflow

Document service topology and dependencies | Observed and inferred relationships are distinguished. | Built-in function with composed documentation

Audit resource configurations against approved standards | Each finding identifies resource, rule and observed value. | Configured custom agent

Assess release readiness | The candidate revision is unambiguous. | Preview function

Test a deployed application release | Target revision, identities and permitted effects are explicit. | Preview function


Detailed reference: [Skills, applicability, and supporting files](../guides/devops.html#D-M04)



Detailed reference: [Managed knowledge production and refresh](../guides/devops.html#D-M08)



Detailed reference: [Console, web application, and inbound remote access](../guides/devops.html#D-09)


## 10. Health reporting, deployment review, and prevention

24:00–27:00 · Invocation and triggers

A health report summarizes measurements for a defined period. A deployment review traces actual release records. Pattern analysis and prevention evaluation use multiple investigations to identify and prioritize follow-up work.



Operational outcome | Completion evidence | Implementation boundary

Assess and report service health and trends | Service dimensions and observation periods are explicit. | Native inquiry or configured reporting

Review deployment and change activity | Deployment states and immutable revisions are traceable. | Configured custom agent

Identify recurring incident patterns | Supporting investigation identities are retained. | Built-in function

Prioritize incident-prevention work | Accepted proposals retain source incidents. | Built-in function


Detailed reference: [On-demand invocation and scheduled triggers](../guides/devops.html#D-07)



Detailed reference: [Incident triage, investigation, and prevention](../guides/devops.html#D-06)


## 11. Webhook triggers: condition and payload projection

27:00–30:00 · Invocation and triggers

A JMESPath predicate selects an event. A projection also changes the context passed to the invocation. Neither is an outbound EventBridge notification.



Input or result | Service behavior

Active webhook integration | Available event source

False, null, or empty expression result | No invocation

Boolean true | Invocation receives the original payload

Another truthy result | Invocation receives the projected value

Limits | 4,096-character expression; 10,000-character invocation context

Removed source | Trigger remains listed but cannot run


Detailed reference: [Webhook events, filtering, and payload projection](../guides/devops.html#D-18)


## 12. Provider registration and Agent Space association

30:00–32:00 · External system integrations

Provider authentication is registered at account level. Association and tool selection make an explicit subset available to the Agent Space. The invocation still needs a working authenticated route.



![Provider registration and Agent Space association](../assets/diagrams/devops-integrations.svg)



Detailed reference: [Supported integrations and connection directions](../guides/devops.html#D-12)



Detailed reference: [MCP provider registration and tool selection](../guides/devops.html#D-03)


## 13. Telemetry, source control, and incident connections

32:00–34:00 · External system integrations

Choose the evidence source, incident-initiation path, and result destination independently. Registration and Agent Space association are separate setup steps.



Connection family | Documented systems | Purpose and boundary

AWS evidence | CloudWatch, S3, EKS; selected AWS accounts | Read authorized telemetry, objects, and cluster evidence; EKS has additional access setup.

Telemetry providers | Dynatrace; Datadog, Grafana, New Relic, Splunk | Dynatrace has a documented two-way path; other named providers expose reads and separately configured event initiation.

Code and delivery | GitHub, GitLab; Azure Resources and Azure DevOps | Repository, pipeline, or infrastructure context according to the configured provider and resource scope.

Incident coordination | ServiceNow, PagerDuty, Slack | Provider-specific initiation and communication; not a universal write capability.

Additional interfaces | MCP, webhooks, EventBridge | Selected tools, incoming incident signals, and outgoing lifecycle events are different directions.


Detailed reference: [Supported integrations and connection directions](../guides/devops.html#D-12)


## 14. Service-health reporting: workflow dependencies

34:00–37:00 · External system integrations

Current telemetry is required for a health conclusion. Context is optional unless the reporting profile depends on it. A recurring profile adds a trigger; an external destination adds a separate publication operation.



Workflow step | Mechanism and configuration | Completion or failure decision

Read current observations | Authorized evidence sources and explicit scope | Missing current data prevents a health conclusion.

Choose the execution profile | Built-in operational query OR configured custom agent | A native inquiry does not require a custom definition.

Use relevant context | Optional available memory or reviewed reporting procedure | Retained history never substitutes for current observations.

Repeat or publish | Conditional schedule and optional destination | Timing and publication controls remain separate from the report objective.


Detailed reference: [MCP provider registration and tool selection](../guides/devops.html#D-03)



Detailed reference: [On-demand invocation and scheduled triggers](../guides/devops.html#D-07)



Detailed reference: [Memory construction and progressive retrieval](../guides/devops.html#D-M01)



Detailed reference: [Memory-store access, versions, and retention](../guides/devops.html#D-M07)


## 15. Outbound tools and remote-agent delegation

37:00–40:00 · External system integrations

Integration direction determines which endpoint, identity, and operation must be configured.



Path | Caller and target | Configuration

Outbound MCP | DevOps Agent calls a tool server | Provider authentication and selected tools

Outbound A2A | DevOps Agent calls an external agent | Agent-card endpoint and supported authentication

Inbound MCP/A2A | External client calls DevOps Agent | Remote-server endpoint and scoped caller credentials

Custom agent | Definition executes inside DevOps Agent | System prompt, assigned tools, skills, stores


Detailed reference: [MCP provider registration and tool selection](../guides/devops.html#D-03)



Detailed reference: [Outbound A2A delegation](../guides/devops.html#D-20)



Detailed reference: [Console, web application, and inbound remote access](../guides/devops.html#D-09)


## 16. Private connectivity: gateway, DNS, and endpoint routes

40:00–43:00 · Network connectivity

Provider authentication and private routing are configured independently.



Property | Configuration consequence

VPC Lattice resource gateway | Private traffic arrives through gateway interfaces in selected subnets

Shared VPC | Use the documented self-managed connection arrangement

DNS | Select public or in-VPC resolution for the target hostname

Port ranges | Explicitly include nonstandard ports; omitted ranges allow 443

OAuth endpoint | Can use a different private route from the tool endpoint

Scope | Network transport does not relocate the agent service into the VPC


Detailed reference: [Private endpoints, routing, and DNS](../guides/devops.html#D-04)


## 17. Stopping future triggers and current invocations

43:00–46:00 · Execution runtime and action control

Pause the trigger to stop future starts. Cancel the invocation separately; an in-flight tool call can still complete and previously completed evidence remains.



![Custom work: future triggers and current invocations](../assets/diagrams/mechanism-devops-cancellation.svg)



Detailed reference: [Invocation state, trajectory, and continuation](../guides/devops.html#D-19)



Detailed reference: [On-demand invocation and scheduled triggers](../guides/devops.html#D-07)


## 18. Sandbox execution and directed-action approval

46:00–49:00 · Execution runtime and action control

Execution authority depends on the specific effect; there is no universal read-only agent mode.



Execution surface | Purpose | Primary controls | Evidence

Sandbox | Investigation-local computation and data processing | Packages, network rules and existing AWS permissions | Code, outputs and failed network calls

Directed AWS action | Eligible resource mutation | Space opt-in, elevated role and specific approval | Approval, CloudTrail and resulting resource state

External MCP mutation | Tool-defined effect | Tool classification, selected tool and approval behavior | Tool arguments and external result

Recommendation only | Describe a possible change | No execution authorization | Proposal, risk, rollback and verification plan


Detailed reference: [Sandbox computation and network policy](../guides/devops.html#D-M05)



Detailed reference: [Directed actions and approval scope](../guides/devops.html#D-M06)


## 19. Incident triage and investigation workflow

49:00–51:00 · Built-in managed workflows

A signal can be linked, skipped, or investigated independently. Steering affects the current analysis; completed-investigation feedback supplies a separate corrective input.



![Incident triage and investigation workflow](../assets/diagrams/devops-incident.svg)



Detailed reference: [Incident triage, investigation, and prevention](../guides/devops.html#D-06)


## 20. Incident triage and investigation lifecycle

51:00–54:00 · Built-in managed workflows

Routing correction, diagnosis correction and mitigation approval are distinct operations.



Incoming signal | Alert, ticket, webhook or manual request with incident context.

Triage decision | Linked, skipped or proceed; inspect the reason before diagnosing absence.

Investigation | Evidence collection, hypotheses, root-cause versions and steering.

Closure and feedback | Mitigation decision, recovery evidence and correction of routing or diagnosis.


Detailed reference: [Incident triage, investigation, and prevention](../guides/devops.html#D-06)


## 21. Incident triage, investigation, and mitigation

54:00–57:00 · Built-in managed workflows

Triage determines routing. Investigation evaluates current evidence. A mitigation plan is a proposal; execution requires the applicable action authorization and a separate recovery check.



Operational outcome | Completion evidence | Implementation boundary

Triage incident signals | Decision and reason are visible. | Built-in function

Investigate a service incident | Affected service and UTC interval are explicit. | Built-in function

Prepare a mitigation plan | Target and proposed effect are explicit. | Built-in function

Execute an approved mitigation and verify recovery | Exact operation and target were approved. | Controlled action

Prepare an incident-status bulletin | Incident and measurement window are identified. | Configured custom agent


Detailed reference: [Incident triage, investigation, and prevention](../guides/devops.html#D-06)



Detailed reference: [Directed actions and approval scope](../guides/devops.html#D-M06)


## 22. Release readiness review and release testing

57:00–59:00 · Built-in managed workflows

Readiness review, managed verification and active application testing are separate preview operations.



Preview path | Subject | Primary output | Important boundary

Release readiness review | Code change and dependency context | Risk findings and recommended actions | Feature and repository eligibility are specific

Managed verification | Build or test evidence for the change | Verification task and results | Not equivalent to production recovery evidence

Active release testing | Running web application or API | Observed application behavior | Requests can create, modify or delete application data

Custom-agent release tools | Release Manager tasks and reports | Created or analyzed release task | Use selected tools and inspect task state


Detailed reference: [Release-readiness review and release testing](../guides/devops.html#D-22)


## 23. Access roles, tool providers and private connectivity

59:00–62:00 · Administration, security, and automation

Reachability, authentication, tool selection and authorization must each be tested.



Configuration area | Decision | Confirmation | Typical failure

Resource access | Allowed accounts, actions and resources | Known resource can be read under expected identity | Missing source data

Operator access | Who can enter and operate the space | Intended operator signs in | Administrator-only access works

MCP provider | Endpoint, authentication and registration | Provider validates or associates successfully | Wrong token endpoint or SigV4 fields

Tool association | Selected tools for the space or custom agent | Expected tool visible; excluded tool absent | Provider registered but tool unavailable

Private connection | VPC, subnets, security groups and ports | Target host and port reachable | Route or port failure mistaken for credential failure


Detailed reference: [Resource roles and operator roles](../guides/devops.html#D-02)



Detailed reference: [MCP provider registration and tool selection](../guides/devops.html#D-03)



Detailed reference: [Private endpoints, routing, and DNS](../guides/devops.html#D-04)


## 24. Troubleshooting matrix and operating limits

62:00–64:00 · Administration, security, and automation

Diagnose the failed layer and retest the smallest relevant operation.



Symptom | First object to inspect | Second check | Do not do first

No investigation | Triage decision and incident link | Concurrency and trigger status | Broaden all permissions

Missing data | Resource role and source connection | Time window and resource identity | Assume the source has no data

Memory not used | Store/entry active state and description | Agent attachment and new session | Claim retrieval from answer wording

Tool unavailable | Provider association and selected tools | Authentication and private route | Rotate a valid secret without network evidence

Mutation denied | Directed-action enablement and classification | Role trust, exact operation and approval | Treat a chat request as authorization


Detailed reference: [Execution limits and diagnostic procedures](../guides/devops.html#D-10)



Detailed reference: [Documentation coverage and references](../guides/devops.html#D-11)


## 25. Asset APIs, declarative management, and audit

64:00–67:00 · Administration, security, and automation

The source of configuration and the audit of its use are separate administrative responsibilities.



Facility | Supported role | Distinct operation

Asset API | Manage eight asset types | Triggers remain separate resources

CloudFormation Asset | Complete metadata and file set | Per-file edits and historical content operations remain API calls

CloudFormation Trigger | Documented scheduled starts | Do not infer event-trigger properties from UI support

CloudTrail | Attribution of documented service operations | Not a correctness score

CloudWatch usage metrics | Execution time and request counts | Accounting scopes differ by metric


Detailed reference: [Configuration APIs and update semantics](../guides/devops.html#D-08)



Detailed reference: [Identity providers, credential maintenance, and service telemetry](../guides/devops.html#D-24)


## 26. Configured operational-report workflow

67:00–69:00 · Worked example and reference material

The team defines the report period and selected evidence. An invocation queries sources, produces a report, and exposes results for review. Schedule timing and the reporting window are separate configuration decisions.



![Configured operational-report workflow](../assets/diagrams/devops-reporting.svg)



Detailed reference: [Incident and reporting use cases in the resource model](../guides/devops.html#D-14)



Detailed reference: [Custom-agent definitions and configuration](../guides/devops.html#D-16)



Detailed reference: [On-demand invocation and scheduled triggers](../guides/devops.html#D-07)


## 27. Incident records and action-specific authorization

69:00–72:00 · Worked example and reference material

A signal can be linked, skipped, or investigated. Steering changes the active analysis; completed-investigation feedback provides a corrective input. Resource mutation requires its separate approval path.



![DevOps Agent: incident records and directed-action boundary](../assets/diagrams/er-devops-incidents.svg)



Detailed reference: [Incident and reporting use cases in the resource model](../guides/devops.html#D-14)


## 28. Worked example: recurring alarm with different current evidence

72:00–80:00 · Worked example and reference material

Prepared evidence demonstrates how historical context can be useful without becoming the current diagnosis.



0–2 min | Inspect prior context | Earlier database pool saturation and its verified evidence

2–4 min | Compare current database signals | 34/100 connections and query p95 of 18 ms

4–6 min | Evaluate current dependency signals | Inventory p95 of 2,900 ms and checkout p95 of 3,100 ms

6–8 min | Record the conclusion | Historical memory is relevant; upstream latency is the current lead; cause remains bounded


Detailed reference: [Recurring-alarm investigation: worked example](../guides/devops.html#D-U01)



Detailed reference: [Memory construction and progressive retrieval](../guides/devops.html#D-M01)



Detailed reference: [Corrective feedback and reflection memory](../guides/devops.html#D-M02)
