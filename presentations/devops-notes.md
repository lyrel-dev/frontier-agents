# AWS DevOps Agent — HTML presentation reference



Open [devops.html](devops.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Product Functions and Agent Space Resource Model

**Chapter:** Part I · Product Model. **Schedule:** 00:00–03:00. **Slide budget:** 03:00.

Configuration objects, executions and effects must be reviewed as separate records.



Layer | Primary objects | Operational purpose | Evidence to inspect

Account and Region | Provider registrations; AWS account roles | Make selected sources and tools available | Registered provider, role ARN, Region

Agent Space | Associations; selected tools; operator access | Define the operational boundary | Space ID, integrations, operator role

Knowledge and behavior | Topology; memory; instructions; skills | Provide environment context and procedures | Version, active state, attachment

Execution | Investigation; custom-agent invocation; evaluation | Perform a bounded task | Trajectory, tool results, status

Effect | Recommendation; approval; directed action | Separate advice from state change | Approval identity and resulting state



**Guide:** [D-01](../guides/devops.html#D-01)



## 2. Use Case Taxonomy and Delivery Modes

**Chapter:** Part II · Use Case Catalog. **Schedule:** 03:00–05:00. **Slide budget:** 02:00.

The catalog distinguishes native functions from configured and team-composed workflows.



Delivery mode | Meaning | Representative use cases | Required configuration

Built-in function | AWS-managed incident, query or prevention behavior | Triage, investigation, on-demand health, pattern analysis | Agent Space, sources and operator access

Configured custom agent | Operator-defined prompt, tools, skills, memory and schedule | Health reports, operational reviews, audits, trend reports | Custom-agent definition and trigger

Configured knowledge | Reusable context or procedure | SOP consolidation, report standards, topology notes | Memory, skill or instructions

Controlled action | Explicitly authorized state change | Approved mitigation | Directed actions, role, classification and approval

Preview function | Feature-specific pre-production path | Release readiness and release testing | Eligibility, Region and test target



**Guide:** [D-01](../guides/devops.html#D-01), [D-06](../guides/devops.html#D-06), [D-07](../guides/devops.html#D-07)



## 3. Incident Operations Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 05:00–08:00. **Slide budget:** 03:00.

Triage, diagnosis, recommendation and execution are different stages with different records.



Use case | Initiation | Primary inputs | Reviewable output

Incident signal triage | Alert, ticket or webhook | Signal identity, correlation and skip criteria | Linked, skipped or proceed decision with reason

Root-cause investigation | Automatic or manual investigation | Metrics, logs, traces, changes and topology | Evidence, hypotheses, root-cause versions

Investigation steering | Operator follow-up in context | Contrary evidence or missing source | Revised analysis and new root-cause version

Mitigation planning | Completed or active investigation | Proposed effect, target, risk and rollback | Reviewable mitigation proposal

Approved mitigation | Explicit operator approval | Exact operation and resource | Attributed action and independently checked state



**Guide:** [D-06](../guides/devops.html#D-06), [D-M06](../guides/devops.html#D-M06), [D-10](../guides/devops.html#D-10)



## 4. Operational Reporting and Review Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 08:00–11:00. **Slide budget:** 03:00.

Recurring reports are custom-agent workflows; the report contract and data window must be explicit.



Use case | Cadence | Source scope | Expected output

On-demand service health | Ad hoc | Selected service metrics, alarms and deployments | Timestamped health answer with missing signals

Minute incident status report | On demand or short schedule | Current logs, metrics and active investigation | Changed observations, open hypotheses and next check

Daily or weekly health report | Scheduled | Named services and complete reporting window | Trend summary, incidents, deployments and data gaps

Deployment activity report | Scheduled or ad hoc | CI/CD history and service ownership | Revision list, failed changes and affected services

Operational review pack | Weekly or monthly | Health, incidents, prevention and changes | Review agenda, decisions and owned follow-up



**Guide:** [D-07](../guides/devops.html#D-07), [D-03](../guides/devops.html#D-03), [D-05](../guides/devops.html#D-05)



## 5. Knowledge and Documentation Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 11:00–14:00. **Slide budget:** 03:00.

Memory, instructions, skills and topology serve different documentation purposes and lifecycles.



Use case | Primary mechanism | Maintained object | Boundary

Incident pattern identification | Managed learning and prevention evaluation | Monitor memory and recommendation | Historical pattern is not the current cause

SOP consolidation | Skill and supporting resources | Reviewed SKILL.md bundle | Team workflow; procedure does not grant tools

Standing operational policy | Agent instructions | Global or agent-specific AGENTS.md | Prompt context, not IAM enforcement

Topology documentation | Discovery and learned understanding | Topology and environment summary | Graph is not an access-control boundary

Service-specific context | Custom memory store | Descriptions, entries and versions | Attachment and active state control access



**Guide:** [D-05](../guides/devops.html#D-05), [D-M01](../guides/devops.html#D-M01), [D-M02](../guides/devops.html#D-M02), [D-M03](../guides/devops.html#D-M03), [D-M04](../guides/devops.html#D-M04), [D-M07](../guides/devops.html#D-M07)



## 6. Access Roles, Tool Providers and Private Connectivity

**Chapter:** Part III · Access and Knowledge. **Schedule:** 14:00–17:00. **Slide budget:** 03:00.

Reachability, authentication, tool selection and authorization must each be tested.



Configuration area | Decision | Confirmation | Typical failure

Resource access | Allowed accounts, actions and resources | Known resource can be read under expected identity | Missing source data

Operator access | Who can enter and operate the space | Intended operator signs in | Administrator-only access works

MCP provider | Endpoint, authentication and registration | Provider validates or associates successfully | Wrong token endpoint or SigV4 fields

Tool association | Selected tools for the space or custom agent | Expected tool visible; excluded tool absent | Provider registered but tool unavailable

Private connection | VPC, subnets, security groups and ports | Target host and port reachable | Route or port failure mistaken for credential failure



**Guide:** [D-02](../guides/devops.html#D-02), [D-03](../guides/devops.html#D-03), [D-04](../guides/devops.html#D-04)



## 7. Memory, Instructions and Skills

**Chapter:** Part III · Access and Knowledge. **Schedule:** 17:00–20:00. **Slide budget:** 03:00.

Availability, selection and diagnostic influence are separate questions for retained context.



Mechanism | When loaded | Typical content | Lifecycle control

Managed memory | Selected by description during relevant work | Recurring causes and environment understanding | Version, active state and managed refresh

Custom memory | Selected after store attachment | Team or service context | Create, edit, deactivate, detach or delete

Corrective reflection | Future investigation of the alarm | Verified correction to an earlier diagnosis | Latest feedback and visible memory

Agent instructions | Every new applicable session | Standing policies and output rules | Edit and start a new session

Skill | When description and agent scope match | Specialized procedure and references | Edit description, content and targeting



**Guide:** [D-M01](../guides/devops.html#D-M01), [D-M02](../guides/devops.html#D-M02), [D-M03](../guides/devops.html#D-M03), [D-M04](../guides/devops.html#D-M04), [D-M07](../guides/devops.html#D-M07)



## 8. Custom Agents, Schedules and Invocation Records

**Chapter:** Part III · Access and Knowledge. **Schedule:** 20:00–23:00. **Slide budget:** 03:00.

A schedule creates future work; it does not define the data window or cancel an existing run.



Object | Configuration | Run-time behavior | Stop or change control

Custom agent | System prompt, selected tools, skills and stores | Loads only assigned resources | Edit or disable definition

Schedule trigger | Rate or cron expression | Creates future invocations | Pause or delete trigger

Invocation | Run Now, prompt or trigger | Produces status, trajectory and outputs | Cancel current invocation

Artifact or recommendation | Generated by assigned skills/tools | Separate output object | Review and manage independently

Asset API | IDs, metadata, files and versions | Programmatic configuration management | Respect PATCH/replacement semantics



**Guide:** [D-07](../guides/devops.html#D-07), [D-08](../guides/devops.html#D-08)



## 9. Incident Triage and Investigation Lifecycle

**Chapter:** Part IV · Incident Operations and Control. **Schedule:** 23:00–26:00. **Slide budget:** 03:00.

Routing correction, diagnosis correction and mitigation approval are distinct operations.



Incoming signal | Alert, ticket, webhook or manual request with incident context.

Triage decision | Linked, skipped or proceed; inspect the reason before diagnosing absence.

Investigation | Evidence collection, hypotheses, root-cause versions and steering.

Closure and feedback | Mitigation decision, recovery evidence and correction of routing or diagnosis.



**Guide:** [D-06](../guides/devops.html#D-06)



## 10. Incident Pattern Analysis and Prevention Recommendations

**Chapter:** Part IV · Incident Operations and Control. **Schedule:** 26:00–29:00. **Slide budget:** 03:00.

Incident pattern identification produces context and recommendations, not an automatically implemented fix.



Stage | Input | Output | Operator decision

Monitor memory refresh | Recent completed investigations | Monitor-specific recurring-cause context | Inspect version and relevance

Prevention evaluation | Multiple incident investigations | Observability, infrastructure, governance or code recommendations | Run, stop or wait for scheduled evaluation

Recommendation review | Incident evidence and expected impact | Keep, discard or implemented state | Assign owner and acceptance criteria

Corrective feedback | Verified diagnosis correction | Reflection for future investigations | Separate local learning from AWS sharing



**Guide:** [D-M01](../guides/devops.html#D-M01), [D-M02](../guides/devops.html#D-M02), [D-06](../guides/devops.html#D-06)



## 11. Sandbox and Directed Actions

**Chapter:** Part IV · Incident Operations and Control. **Schedule:** 29:00–32:00. **Slide budget:** 03:00.

Execution authority depends on the specific effect; there is no universal read-only agent mode.



Execution surface | Purpose | Primary controls | Evidence

Sandbox | Investigation-local computation and data processing | Packages, network rules and existing AWS permissions | Code, outputs and failed network calls

Directed AWS action | Eligible resource mutation | Space opt-in, elevated role and specific approval | Approval, CloudTrail and resulting resource state

External MCP mutation | Tool-defined effect | Tool classification, selected tool and approval behavior | Tool arguments and external result

Recommendation only | Describe a possible change | No execution authorization | Proposal, risk, rollback and verification plan



**Guide:** [D-M05](../guides/devops.html#D-M05), [D-M06](../guides/devops.html#D-M06)



## 12. Release Readiness Review and Release Testing

**Chapter:** Part IV · Incident Operations and Control. **Schedule:** 32:00–34:00. **Slide budget:** 02:00.

Readiness review, managed verification and active application testing are separate preview operations.



Preview path | Subject | Primary output | Important boundary

Release readiness review | Code change and dependency context | Risk findings and recommended actions | Feature and repository eligibility are specific

Managed verification | Build or test evidence for the change | Verification task and results | Not equivalent to production recovery evidence

Active release testing | Running web application or API | Observed application behavior | Requests can create, modify or delete application data

Custom-agent release tools | Release Manager tasks and reports | Created or analyzed release task | Use selected tools and inspect task state



**Guide:** [D-09](../guides/devops.html#D-09), [D-10](../guides/devops.html#D-10)



## 13. Worked Example: Recurring Alarm with Different Current Evidence

**Chapter:** Part V · Worked Example. **Schedule:** 34:00–42:00. **Slide budget:** 08:00.

Prepared evidence demonstrates how historical context can be useful without becoming the current diagnosis.



0–2 min | Inspect prior context | Earlier database pool saturation and its verified evidence

2–4 min | Compare current database signals | 34/100 connections and query p95 of 18 ms

4–6 min | Evaluate current dependency signals | Inventory p95 of 2,900 ms and checkout p95 of 3,100 ms

6–8 min | Record the conclusion | Historical memory is relevant; upstream latency is the current lead; cause remains bounded



**Guide:** [D-U01](../guides/devops.html#D-U01), [D-M01](../guides/devops.html#D-M01), [D-M02](../guides/devops.html#D-M02)



## 14. Troubleshooting Matrix and Operating Limits

**Chapter:** Part VI · Troubleshooting. **Schedule:** 42:00–44:00. **Slide budget:** 02:00.

Diagnose the failed layer and retest the smallest relevant operation.



Symptom | First object to inspect | Second check | Do not do first

No investigation | Triage decision and incident link | Concurrency and trigger status | Broaden all permissions

Missing data | Resource role and source connection | Time window and resource identity | Assume the source has no data

Memory not used | Store/entry active state and description | Agent attachment and new session | Claim retrieval from answer wording

Tool unavailable | Provider association and selected tools | Authentication and private route | Rotate a valid secret without network evidence

Mutation denied | Directed-action enablement and classification | Role trust, exact operation and approval | Treat a chat request as authorization



**Guide:** [D-10](../guides/devops.html#D-10), [D-11](../guides/devops.html#D-11)
