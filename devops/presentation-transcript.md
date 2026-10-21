# AWS DevOps Agent: presentation transcript

Total 35:00, including 8:00 prepared-result demonstrations. No service-completion-time guarantee. Questions, preparation and live setup are additional.

## 1. Investigate, propose, authorize

0:00–1:00; allocation 1:00

These are separate operations, not stages that imply automatic permission to change production.

| Investigate | Propose | Authorize |
|---|---|---|
| Read connected telemetry and change context. | Produce a diagnosis and mitigation proposal. | Use the separate directed-action gate for an eligible mutation. |

### Presenter notes

Open with the distinction the team must preserve during an incident: analysis can run with read access, a proposal remains advice, and execution needs the appropriate configured and approved path. The guide covers environment inspection, incident operations, reliability recommendations, custom automation and preview release assessment. It does not claim that every account or source is connected, or that the agent replaces the incident commander.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)


## 2. Know which object you are configuring

1:00–3:00; allocation 2:00

Scope, work, context and execution are not the same object.

| Object | Contains or represents | Operator decision |
|---|---|---|
| Agent Space | Associated accounts, tools and knowledge | Which environment is accessible? |
| Investigation | Incident timeline, evidence and conclusions | Which problem and interval are being analyzed? |
| Custom agent / invocation | Reusable definition / one run | Which tools and context can this run use? |
| Instructions / skill / memory | Standing rules / procedure / retained context | What is always loaded, selected or recalled? |

### Presenter notes

Use the object model to prevent configuration errors. Registering an integration is not the same as associating it with the operational space. A Chat exchange is not necessarily a formal investigation. A custom agent definition is not an execution result. When someone says the agent knows the environment, ask which retained representation is involved, how recently it was refreshed, and whether the current run could actually read it.

Official documentation: [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html) · [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) · [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)


## 3. The functional map

3:00–5:00; allocation 2:00

Group by product responsibility; do not label an example incident as a capability.

| Area | Documented operations | Result to inspect |
|---|---|---|
| Environment | Discover topology; query connected sources | Resource mapping and tool results |
| Incident | Open; triage; investigate; steer/fork; Review | Incident record and separate quality assessment |
| Response | Propose mitigation; approve action; prevention | Proposal, execution record or recommendation |
| Automation | Run a configured custom agent; channel delivery | Invocation trajectory or delivered message |
| Release — preview | Review code; test a running UI/API | Readiness report or executed test evidence |

### Presenter notes

Explain why these areas are separate. Querying a metric is not an incident diagnosis. Creating a recommendation is not deploying it. A recurring health report is a configured task using selected functions, not a universal built-in report. Release readiness examines a change; release testing exercises a running application. The full report provides operation-level inputs and boundaries, so this slide is a map rather than the whole reference.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) · [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)


## 4. Accessible evidence is not necessarily inspected evidence

5:00–7:30; allocation 2:30

Trace a material conclusion back through the query, source and permission boundary.

| Scope | Access | Observation | Conclusion |
|---|---|---|---|
| Alarm/resource ID; account; region; UTC interval | Associated integration and effective role permissions | Actual tool query, returned timestamps and identifiers | Hypothesis supported by the current result |

Denied access, missing data and a genuine empty query result must remain distinct.

### Presenter notes

Take one claimed cause and work backwards. Was the right log group queried? Was the interval correct? Did the result contain the affected resource? Did the source return no records, or did the call fail? Only after those checks should the conclusion be weighed. This is a proposed evidence-review discipline, not a guarantee of how every agent response is formatted. The same discipline applies to a topology map: inspect freshness and identifiers before assuming it describes the current deployment.

Official documentation: [On-demand DevOps tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html) · [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Connect MCP servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html)


## 5. Triage and investigation controls have different effects

7:30–9:30; allocation 2:00

Choose the control that changes the intended object, not merely the visible conversation.

| Control | Effect | Failure to avoid |
|---|---|---|
| Proceed | Start a new investigation | Assuming a repeated alarm always has the old cause |
| Link / unlink | Combine with, or separate from, related work | Treating temporal proximity as proof of common cause |
| Skip / unskip | Suppress, or restore, investigation of an event | Suppressing critical alerts with a broad maintenance rule |
| Steer / resume / fork | Redirect, continue or branch the analysis | Losing the original hypothesis and evidence trail |

### Presenter notes

The operator should be able to explain why an event was linked or skipped. A maintenance exception is an operational policy that needs exact scope, not a generic request to ignore noise. For an investigation already underway, steering adds information; for an alternative line, a fork preserves the original. These controls manage the analysis lifecycle. They neither silence the originating monitoring system nor confer authority to change resources.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


## 6. Diagnosis, Review and feedback are different evidence

9:30–12:00; allocation 2:30

A quality assessment reads the record; it does not rerun the incident against the environment.

| Operation | Produces | Does not establish |
|---|---|---|
| Investigation | Findings and a root-cause explanation | Correctness without source evidence |
| Review | Helpful/not-helpful and criterion-level assessments | Independent runtime verification |
| Corrective feedback | A recorded correction; documented reflections | A measured accuracy improvement from one submission |

Review Accuracy can be not applicable when no reference diagnosis exists on the linked incident.

### Presenter notes

A review can assess grounding and completeness, but it is constrained by the same recorded evidence. Explain the special case where Accuracy is not applicable: the grader has no established root cause to compare with. Corrective feedback is a separate operator input. Current documentation connects it to reflections for later investigations, but seeing a reflection is not evidence that a later run retrieved it or reached the right conclusion.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Document history: reflections and memory changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/document-history.html)


## 7. A proposed mitigation has no execution authority

12:00–14:30; allocation 2:30

Directed actions add a controlled mutation path; they do not remove the need to verify recovery.

| Enable | Scope | Approve | Observe |
|---|---|---|---|
| Agent Space directed-action opt-in | Registered elevated account role or allowed mutating tool | Individual operation, parameters and target in Chat | API result, audit event and independent service state |

Release testing sends application writes through a different execution path.

### Presenter notes

Walk through the gates in order. A broad role is not permission to skip the Chat approval, and a Chat approval does not override service-level prohibitions. A custom MCP classification is metadata; inspect the backend's real privileges. For the demonstration, do not perform a production change. Show a prepared approval and rejected-action case, then explain the additional recovery metric needed after any actual approved mutation.

Official documentation: [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)


## 8. What persists after an incident?

14:30–17:30; allocation 3:00

Retained context, generated environment knowledge and correction records have distinct lifecycles.

| Knowledge | Origin | Meaning for a later run |
|---|---|---|
| Monitor memory | Recurring causes from recent investigations | A historical hypothesis to test against current telemetry |
| Reflections | Corrective feedback on a failed investigation | A lesson associated with the monitor, not proof of recall |
| Environment/tool-use knowledge | Managed learning and refresh | Derived context with a timestamp and update conditions |
| Custom store | Operator or permitted custom-agent writes | Only useful when described, active and attached as needed |

### Presenter notes

Avoid the phrase learns from everything. Describe an inspectable object instead: its store, content, version and last update. Current documentation maintains learned environment knowledge as memory, while older cached pages describe learned skills. Monitor and tool-use stores have different update cadences. The underlying model-training implementation is not established by these documents. The practical question is whether relevant, accurate context was available and actually used in the later task.

Official documentation: [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Learned skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html) · [Managed agents and Learning history](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)


## 9. Enable and verify memory deliberately

17:30–20:00; allocation 2:30

Presence, activation, retrieval and correctness are four different checks.

| Inspect | Configure | Observe | Challenge |
|---|---|---|---|
| Knowledge → Memories: content, version and timestamp | Activate the intended store; attach it to the custom agent | Learning History/Triggers and available run read evidence | Compare the recalled cause with present telemetry |

Managed stores are read-only to custom agents; attached custom stores can be written.

### Presenter notes

A new custom agent has no memory access until stores are attached. The built-in incident behavior and custom-agent attachments should not be conflated. Demonstrate the proposed verification process with a prepared store: identify what should be recalled, inspect the later run where evidence is visible, and state unverified when the interface does not expose that read. Deactivate misleading context while correcting it; do not delete the incident's source record.

Official documentation: [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Managed agents and Learning history](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)


## 10. A scheduled report is a configured program of work

20:00–22:30; allocation 2:30

The custom-agent facility provides execution; the team supplies the task definition and acceptance rule.

| Configuration | Required precision | Observable failure |
|---|---|---|
| Prompt | Resource scope, rule and output contract | Vague analysis with no resource-level result |
| Tools | Actual assigned read functions | Missing source reported as compliant |
| Memory/skills | Relevant attachments and procedures | Old context silently reused |
| Trigger | Schedule and invocation ownership | Future runs continue after one task is cancelled |

### Presenter notes

Use the report's configuration-check procedure as an example. A reliable check needs an explicit comparison against an observed field and three possible results: compliant, non-compliant or unknown. Test the unknown case intentionally. Do not create a schedule merely because the agent can produce a plausible report once. Review the selected toolbox and run history; pausing a trigger and cancelling an invocation are separate controls.

Official documentation: [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) · [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) · [Custom-agent outputs](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)


## 11. Source review and application testing differ

22:30–25:00; allocation 2:30

One analyzes the change; the other interacts with the deployed application.

|  | Readiness review — preview | Release testing — preview |
|---|---|---|
| Input | Repository change and dependency context | Target profile, test intent and credentials |
| Operation | Inspect operational risk in the change | Explore UI/API behavior with real requests |
| Output | Findings and advisory release recommendation | Executed test results and reproduction evidence |
| Boundary | Not a deployment gate without integration | Can create, modify or delete application data |

### Presenter notes

Both require feature-level availability checks and are documented in us-east-1 during preview. A report saying Block does not automatically stop a pipeline. An application test may send notifications or process payments if the environment allows those effects. Require safe staging data and explicit target authorization. Do not reuse the directed-action approval model as a claim that every application request needs operator confirmation.

Official documentation: [Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html) · [Release readiness code review](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) · [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) · [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## 12. Demonstration: challenge a recurring diagnosis

25:00–33:00; allocation 8:00

Use prepared evidence to show the decisions; do not promise an eight-minute end-to-end investigation.

| Minutes | Action |
|---|---|
| 1 | Show the prepared event, build and scope; identify unavailable sources. |
| 2 | Inspect the stored memory and the current investigation's evidence side by side. |
| 2 | Challenge one causal claim with a source query; show an alternative explanation. |
| 2 | Review a mitigation proposal and explain the separate execution approval. |
| 1 | Show corrective feedback and the evidence needed to claim later recall. |

Fallback: Use a clearly labeled prepared investigation export and source-query results. Do not invent a completed agent run during the demonstration.

### Presenter notes

Follow the five timed steps in the report. The presenter needs a permission-cleared incident record, prior memory, actual source-query output and a prepared mitigation proposal. No live AWS work has been executed for this documentation. If a live environment is available, retain the same decision sequence and switch to prepared evidence rather than waiting for an unbounded run. The audience should see a material claim challenged, not only a successful agent response.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) · [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)


## 13. Operational acceptance is evidence, not fluency

33:00–35:00; allocation 2:00

Start with a bounded service and retain unresolved gaps explicitly.

| Accept only when… | Keep separate | Stop when… |
|---|---|---|
| Scope and source queries match | Diagnosis versus historical memory | Required telemetry is denied or missing |
| Target and recovery test are explicit | Proposal versus approved execution | Rollback assumptions are unknown |
| Unknown results remain visible | One run versus its recurring trigger | The report fabricates an all-clear result |
| Tests use a safe staging target | Code review versus application testing | Real external side effects are possible |

### Presenter notes

Close with decisions the team can make immediately: one service scope, one useful investigation procedure, one source-reconciliation check and a separate mutation approval policy. These are proposed adoption controls, not measured outcomes. The detailed report includes configuration, evidence sources and known documentation differences. Questions and any live setup work are outside the timed programme.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) · [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

