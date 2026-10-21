# AWS DevOps Agent

Operational investigation, controlled actions and release assessment

Reviewed: 2026-10-21

A technical reference for operators and platform engineers. This guide distinguishes the service's functions from the context and permissions that make those functions work. Operational procedures are proposed team practices, not accounts of executed demonstrations.

## Availability

Production operations, on-demand tasks and custom agents are documented service functions. Release management and Sandbox are preview features with narrower regional availability. Check the feature-level region table before enabling either; release management is documented in us-east-1 only.

Official documentation: [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## Product objects

### Agent Space

The configured operational boundary containing associated accounts, integrations, knowledge and investigations. It is not equivalent to an AWS account or an application deployment.

Official documentation: [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html)


### Registration and association

Register a provider connection, then associate the relevant connection with an Agent Space. A registered provider does not by itself establish that every investigation can reach the intended resource or repository.

Official documentation: [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html)


### Investigation

A persisted incident analysis with a timeline, collected evidence, conclusions and mitigation proposals. A Chat conversation can initiate or guide one but is not the same object.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)


### Custom agent and invocation

A reusable definition of prompt, selected tools, skills and memory stores; an invocation is one execution of that definition. A scheduled report is an application of this facility, not a separately supplied report product.

Official documentation: [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)


### Skill, instruction and memory

A skill is a selectively loaded procedure; an instruction is injected at session start; a memory stores informational context. None substitutes for IAM or tool-side authorization.

Official documentation: [Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)


## Product functions

### Environment inspection

Inspect the accessible environment and obtain current operational evidence before making an incident claim.

#### D01 — Discover and inspect application topology

Availability: Documented. Activation: See invocation and prerequisites.

The service discovers resources and builds a representation of application components and their relationships. The Topology view exposes that representation; the environment summary and generated understanding reuse the discovered context. This helps locate a service's resources and dependencies before querying live telemetry.

**Input.** Associated cloud resources, repositories, deployment pipelines and observability connections.

**Output.** A topology and versioned environment summary. These are derived views, not a guarantee that every resource, dependency or recent deployment has been discovered.

**Invocation and prerequisites.** Associate the required providers with the Agent Space; inspect Topology. Use Regenerate when deliberately refreshing derived understanding.

**Limitations and effects.** Discovery is limited by provider scope and permissions. Scheduled refresh and source changes have different update behavior; check timestamps rather than treating the map as live configuration.

**Proposed operator verification — not executed.** Select one service and reconcile its resource identifiers, repository and critical dependency against the deployment inventory. Record missing mappings before using the map for incident scope.

Official documentation: [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html) · [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Learned skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)


#### D02 — Query connected resources and telemetry in Chat

Availability: Documented. Activation: See invocation and prerequisites.

On-demand Chat calls available tools to inspect infrastructure and retrieve operational data. It can combine resource configuration, metrics, logs and change information when those integrations are available. It is an interactive query interface, not a replacement collector that creates missing telemetry.

**Input.** A specific operational question, resource or service identity, time window, and connected data sources.

**Output.** A response supported by tool results, with tables or charts where applicable. Tool access failures and missing data remain limitations of the answer.

**Invocation and prerequisites.** Open Chat in the Agent Space and state the account, region, identifiers and UTC interval. Move a complex issue into a formal investigation when a persistent incident record is needed.

**Limitations and effects.** A successful Chat response does not prove that all intended sources were queried. Source permissions, telemetry retention and query limits still apply.

**Proposed operator verification — not executed.** Inspect the called tool, query window and returned identifiers. Re-run one material query in the source system; distinguish an empty result from denied or unavailable access.

Official documentation: [On-demand DevOps tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html) · [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)


#### D15 — Execute analysis code in an investigation sandbox

Availability: Preview. Activation: Explicit Agent Space opt-in.

The agent can run shell commands, write files and execute code in an ephemeral Linux environment scoped to one investigation. It can parse evidence or compute results and read them back into the analysis. AWS CLI/SDK access uses the documented read-only proxy; allowed HTTP destinations remain a separate effect boundary.

**Input.** An investigation requiring computation, a configured Sandbox, allowed destinations and preinstalled packages.

**Output.** Computed results and investigation evidence from that environment, not a persistent deployment or a shared execution host.

**Invocation and prerequisites.** Agent Space → Capabilities → Sandbox → Configure. Set narrowly scoped hosts, methods and paths and the required pip/npm packages before saving.

**Limitations and effects.** Preview, limited regions, and investigation use only in the cited guidance. It is not enabled by default and is not documented as a general execution feature for Chat or custom agents. Removing configuration stops provisioning for new investigations.

**Proposed operator verification — not executed.** Use a known small dataset and independently recompute the result. Test a disallowed destination and inspect the configured egress rules; an AWS read-only proxy does not make arbitrary external application endpoints harmless.

Official documentation: [Set up a Sandbox: execution, egress and package configuration](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


### Incident intake and investigation

Create, correlate, investigate and review incident records. These operations have distinct lifecycle effects.

#### D03 — Open an investigation from an event or operator request

Availability: Documented. Activation: See invocation and prerequisites.

An associated trigger or a manual request creates a formal investigation. Native incident integrations and authenticated webhooks supply entry points; manual creation supplies the problem statement directly. The originating system remains responsible for detecting its own event.

**Input.** An alarm, incident or webhook payload, or an operator-specified problem with its occurrence time and starting resource.

**Output.** An investigation linked to the submitted problem and its timeline. Creation is not confirmation of the root cause or severity of business impact.

**Invocation and prerequisites.** Use Incident Response to create an investigation, accept the investigation prompt in Chat, or configure a supported incident integration or signed webhook.

**Limitations and effects.** An event without reliable identifiers or timestamps can produce an incorrectly scoped investigation. A generic webhook still requires the documented payload and credential configuration.

**Proposed operator verification — not executed.** Submit a controlled test event and confirm the correct Agent Space, resource, event time and incident linkage. Check duplicate delivery behavior before production routing.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Invoke through a webhook](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-invoking-devops-agent-through-webhook.html)


#### D04 — Correlate, link or skip incoming incidents

Availability: Documented. Activation: See invocation and prerequisites.

Triage decides whether the event should proceed as a new investigation, be linked to related work, or be skipped under applicable criteria. Linking supplies context to the existing investigation; skipping avoids starting analysis for that event. Operators can unlink or unskip when the decision is wrong.

**Input.** A new incident, recent investigation context and applicable triage instructions or skills.

**Output.** A triage decision and its relationship to an investigation, rather than an independently established diagnosis.

**Invocation and prerequisites.** Configure narrowly scoped triage guidance and inspect the incident's triage decision. Use the documented unlink or unskip control to initiate independent analysis when necessary.

**Limitations and effects.** Similarity in time or service is not proof of a shared cause. Broad maintenance-window rules can suppress relevant incidents. Triage configuration should not be mistaken for disabling the originating alarm.

**Proposed operator verification — not executed.** Test an in-window low-priority event, an out-of-window event and a critical event. The proposed policy must not skip the latter two; retain the underlying alerts independently.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [DevOps Agent skills](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)


#### D05 — Investigate evidence and develop a root-cause explanation

Availability: Documented. Activation: See invocation and prerequisites.

The investigation forms and tests hypotheses by collecting evidence from connected tools. It relates symptoms, dependencies and changes and produces findings and a root-cause explanation. A recent change is a candidate explanation, not automatically the cause.

**Input.** The scoped problem, accessible metrics, logs, traces, deployment history, code and selected historical context.

**Output.** Findings, supporting evidence, an investigation timeline and a conclusion that the operator can inspect. Missing observations may leave the diagnosis incomplete.

**Invocation and prerequisites.** Open the investigation's Summary and Timeline. Supply additional facts through Chat with investigation rather than silently changing the problem in a separate conversation.

**Limitations and effects.** The agent can reason incorrectly or stop with incomplete evidence. Old monitor memories may bias a new diagnosis; they must be checked against the current incident.

**Proposed operator verification — not executed.** For each material hypothesis, retain the observation that supports it, the observation that would refute it, and the unresolved gap. Do not approve mitigation merely because the explanation is fluent.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)


#### D06 — Steer, resume and fork an investigation

Availability: Documented. Activation: See invocation and prerequisites.

Messages can redirect an investigation. A completed investigation can resume with its prior context; a fork explores another line without changing the original. These controls change the analysis lifecycle, not the underlying production resources.

**Input.** A running or completed investigation, an additional fact or correction, or a selected timeline message from which to fork.

**Output.** An updated or branched investigation record with its own sequence of evidence and conclusions.

**Invocation and prerequisites.** Use Chat with investigation to supply facts or resume completed work. Use Fork on the relevant timeline message to test an alternative line of analysis.

**Limitations and effects.** Resuming can incur additional analysis. Forking inherits prior context, which may include a wrong premise. A new branch of reasoning is not independent verification of its inputs.

**Proposed operator verification — not executed.** Fork a prepared investigation to test a competing hypothesis. Compare the observations each branch actually collected and identify premises inherited without a fresh check.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


#### D14 — Assess the quality of a completed investigation

Availability: Documented. Activation: See invocation and prerequisites.

Review reads the reported problem, collected evidence and conclusion. It produces a separate helpful/not-helpful verdict and criterion-level assessments of scope alignment, evidence grounding, completeness, environment impact and accuracy. It does not rerun the investigation or alter its record.

**Input.** A completed investigation record, with any reference root cause on its linked incident or ticket.

**Output.** A Review result with pass, fail or not applicable per criterion and supporting reasoning. Accuracy is not applicable when no reference diagnosis is available.

**Invocation and prerequisites.** Incident Response → completed investigation → Review; inspect the separate Review tab. The Grader agent instructions can tailor the criteria for future reviews.

**Limitations and effects.** Review assesses the record it is given. A passing grade cannot establish facts absent from that record or substitute for an independent telemetry check.

**Proposed operator verification — not executed.** Inspect whether a real reference root cause exists before interpreting Accuracy. Compare one evidence-grounding judgment with the cited source observation rather than accepting only the overall verdict.

Official documentation: [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) · [Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


### Response and reliability improvement

Separate advice, authorized resource changes and longer-term prevention recommendations.

#### D07 — Generate and refine mitigation proposals

Availability: Documented. Activation: See invocation and prerequisites.

The agent proposes actions to reduce impact and can refine those proposals in the investigation context. A proposal explains the intended change and its rationale; it is a planning output. Current documentation describes inline proposals in the investigation flow rather than a mandatory separate handoff.

**Input.** Investigation findings, the affected resources and operational constraints.

**Output.** A mitigation proposal to review. The team must establish exact targets, expected recovery signals and rollback conditions before using it.

**Invocation and prerequisites.** Review the inline mitigation proposal and request changes to scope or assumptions. Move to the directed-action path only when a supported resource mutation is explicitly intended.

**Limitations and effects.** Generating a proposal neither grants permission nor executes it. A technically plausible rollback can still cause data or compatibility problems not represented in the incident evidence.

**Proposed operator verification — not executed.** Compare the proposal with the deployed version, migration state and service runbook. Require a measurable recovery condition and an owner capable of stopping or reversing the change.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)


#### D08 — Execute an individually approved directed action

Availability: Documented. Activation: Explicit opt-in.

After Agent Space enablement and the relevant elevated account role or third-party tool opt-in, the agent presents an approval for the specific operation. The elevated execution path is separate from normal read-only investigation access. Service guardrails can refuse operations even when IAM would otherwise allow them.

**Input.** A specific mutating operation, parameters and resource scope, requested in Chat.

**Output.** An execution result and associated audit evidence. Successful API execution is not proof that the incident recovered.

**Invocation and prerequisites.** Enable directed actions, register the account's elevated role or classify and allow the integration tool, then review the action approval in Chat. Check validation status before attempting the action.

**Limitations and effects.** Disabled by default. Mutating calls outside the supported Chat approval path fail rather than silently queueing approval. Delete-class and other guarded operations can be refused. Tool classification does not repair an overprivileged backend.

**Proposed operator verification — not executed.** In a non-production account, first reject an approval and confirm no change; then approve a narrowly scoped reversible operation and correlate its result with CloudTrail and independent resource state.

Official documentation: [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)


#### D09 — Generate prevention recommendations from incident patterns

Availability: Documented. Activation: See invocation and prerequisites.

Prevention analysis turns incident patterns into proposed reliability changes. Recommendations describe the problem, supporting incident context and implementation guidance; code-related recommendations can include a specification for engineering work. This is a separate output from the immediate mitigation of one incident.

**Input.** Past incidents, recurring causes and available environmental context.

**Output.** Recommendations in the improvement backlog, with rationale and prioritization. They are proposals, not completed infrastructure changes or measured reductions in incidents.

**Invocation and prerequisites.** Review prevention recommendations and their supporting incidents. Route accepted work through the team's existing engineering change process.

**Limitations and effects.** Incomplete or incorrect historical diagnoses affect recommendation quality. Ranking is not a substitute for reviewing implementation risk, effort and ownership.

**Proposed operator verification — not executed.** Reject a recommendation that cannot identify the recurring failure it addresses. For an accepted item, define the operational metric to compare after deployment and record the observation window.

Official documentation: [Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)


### Configurable operational automation

Run user-defined work with explicitly selected tools and context, or use configured communication channels.

#### D10 — Execute a configured custom agent

Availability: Documented. Activation: See invocation and prerequisites.

A custom agent executes the defined task using its selected toolbox and context. It records an invocation trajectory and can produce text, artifacts or recommendations. Runtime subagent delegation can continue long work with the same tools and skills; it is not permission escalation or a documented orchestrator for the three products in this collection.

**Input.** A reusable definition containing a system prompt, assigned tools, skills and attached memory stores; optional invocation-specific instructions.

**Output.** An invocation record and its outputs. A daily configuration report is a team-defined application of this function, not an independently supplied monitoring feature.

**Invocation and prerequisites.** Agents → Custom Agents → Create agent. Use the form for the definition and optional skills/memory; use Chat to assign MCP tools. Test with Run Now before adding a trigger.

**Limitations and effects.** A new custom agent has no memory access until stores are attached. It reads attached managed stores but writes only attached custom stores. Required integrations must already exist.

**Proposed operator verification — not executed.** Compare the configured toolbox and memory attachments with the task's minimum requirements. Run a fixture with one intentionally unavailable source and require an explicit incomplete-result indication.

Official documentation: [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) · [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) · [Custom-agent outputs](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)


#### D11 — Publish incident updates and converse in supported channels

Availability: Documented. Activation: Configured integration.

Slack supports one-way notifications in public or private channels and bidirectional conversations in private channels when enabled. Microsoft Teams is documented as a one-way notification integration. These are different delivery modes and must not be described as universal chat parity.

**Input.** A registered communication provider and a channel association for the Agent Space.

**Output.** Incident updates or a Slack conversation thread, depending on the configured channel and mode.

**Invocation and prerequisites.** Associate the channel under the Agent Space's communications capabilities. For Slack bidirectional mode, use a private channel, complete the documented setup and mention the regional app in messages.

**Limitations and effects.** Channel membership changes who can see operational evidence. Available conversations and actions remain constrained by Agent Space configuration; a channel connection is not authorization for arbitrary changes.

**Proposed operator verification — not executed.** Use a non-sensitive test incident to verify destination, thread behavior and authorized audience. Test removal of the association separately from unregistering the provider.

Official documentation: [Connecting Slack](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-ticketing-and-chat-connecting-slack.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


### Release assessment

Assess source changes separately from exploratory testing of a deployed application. Both are preview capabilities.

#### D12 — Review source changes for release readiness

Availability: Preview. Activation: See invocation and prerequisites.

Release readiness review analyzes a change for operational risk before deployment. It can apply team standards and inspect affected dependencies. This differs from generic style review and from executing tests against the deployed application.

**Input.** A connected repository change and relevant code, dependency, infrastructure and operational context.

**Output.** A release-readiness report with findings and an advisory release recommendation, such as Block or Proceed with Caution. The label does not by itself enforce a deployment gate.

**Invocation and prerequisites.** Configure release management on the connected repository or request a review in Chat. Automated PR/MR triggers are documented for private repositories; verify provider-specific trigger configuration.

**Limitations and effects.** Preview in us-east-1. Repository connectivity, indexing and available context determine coverage. Branch protection or pipeline gating must be separately configured and tested.

**Proposed operator verification — not executed.** Use a known, non-production risky change and inspect whether the report identifies the affected dependency and relevant lines. Test the pipeline's actual gating behavior independently of the prose recommendation.

Official documentation: [Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html) · [Release readiness code review](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) · [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


#### D13 — Execute exploratory UI or API release tests

Availability: Preview. Activation: See invocation and prerequisites.

The agent generates a test plan and interacts with the application through a browser or HTTP requests. It explores functional behavior and returns failures with reproduction information. This is execution against the target application, not read-only analysis of a repository.

**Input.** A running application URL, a UI or API test profile, test intent and configured authentication when needed.

**Output.** A test run with status, findings and reproduction steps; UI runs can include screenshots. Coverage is exploratory rather than an exhaustive specification-based proof.

**Invocation and prerequisites.** Release Manager → Test profiles → Add test profile; choose target and test type, configure required authentication, then Start testing with a bounded intent.

**Limitations and effects.** Preview in us-east-1. Requests can create, modify or delete application data and trigger external business effects. Directed-action approval for AWS APIs is not a per-request approval gate for these application tests.

**Proposed operator verification — not executed.** Use an authorized staging deployment with disposable data and disabled real payments/notifications. Confirm the tested build and authentication role; reproduce a reported failure independently before assigning a fix.

Official documentation: [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) · [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


## Configuration mechanisms

### DM1 — Establish data access before writing instructions

A provider connection supplies tools; an association puts the connection in the Agent Space. Role policies and provider credentials determine what those tools can read. A skill that says to inspect a database cannot create missing database access. Private connectivity and authentication are separate configuration problems.

1. Create the Agent Space and associate only the intended accounts and provider connections. Record the account, region, repository and telemetry scope.
2. Validate a minimal read for each required source. For remote MCP servers, inspect the advertised tools, authentication method and network path before adding them.
3. Keep investigation reads separate from elevated directed-action roles. Inspect custom MCP tool effect classifications and backend credentials; an omitted classification can default to READ_ONLY.
4. For private endpoints, configure the documented private connection, DNS resolution and port ranges. Verify both the target and any separate OAuth exchange endpoint.

**Lifecycle.** Changing a registration or association can change the available toolbox. Refresh derived environment context after material changes and test reads again.

**Proposed verification.** Proposed check: use a resource outside the intended scope and confirm the backend denies access. A prompt that tells the agent not to read it is not a substitute.

Official documentation: [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html) · [Connect MCP servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


### DM2 — Separate always-loaded instructions from selected skills

Agent instructions are injected when a session begins; skills are procedural documents selected for task relevance. Use instructions for short standing constraints and skills for a specific diagnosis or triage method. Neither is an enforcement boundary.

1. For the current UI, open Agents → Managed agents → the relevant agent → Agent definition. Set global and agent-specific instructions there; older pages still describe the previous Knowledge location.
2. Create a skill under Knowledge → Skills, with a precise name and description stating when it applies. Assign it only to the relevant agent types.
3. For a repository-imported skill, inspect the imported content and explicitly Sync after a reviewed change. Do not assume edits in Git are already active in the Agent Space.
4. Keep triage skip rules bounded by exact resource, priority and maintenance window. Keep root-cause procedures separate from instructions for publishing findings.

**Lifecycle.** New sessions load fresh instructions. In-flight work is not assumed to adopt edits. Learned environment knowledge is now maintained as memory; it should not be confused with user-authored procedural skills.

**Proposed verification.** Proposed check: compare an applicable and a non-applicable task, inspect observable skill selection, and verify that a matching skip rule does not affect critical or out-of-window alerts.

Official documentation: [Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) · [DevOps Agent skills](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) · [Managed agents and Learning history](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Learned skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)


### DM3 — Understand exactly what persists from past incidents

The managed monitors store contains per-monitor cause history. Corrective investigation feedback can produce per-monitor reflections. Generated topology, dependency, pipeline and tool-use knowledge is also maintained as memory. The agent first sees store descriptions, then opens relevant entries; retaining an entry does not prove it was read in a particular run. This is documented context reuse, not evidence of customer-controlled model-weight training.

1. Inspect Knowledge → Memories: store name, activation, entry content, version and timestamp. Monitor memory is enabled by default; do not assume a useful entry already exists.
2. For an incorrect completed diagnosis, use Add feedback or Chat to record the actual root cause and correction. Inspect the resulting reflection rather than treating the feedback submission as proof of future accuracy.
3. Use Agents → Managed agents → Learning to inspect run History and Triggers. Current guidance describes daily monitor refresh when recent investigations exist; stale monitor entries expire after two weeks without updates.
4. Create a custom store only for durable operational context, give it a description explaining when it applies, and attach it explicitly to each custom agent that needs it. Managed attachments are read-only to custom agents; attached custom stores can be written.
5. Deactivate a misleading entry or store while correcting it. Custom stores can be deleted; managed stores cannot. Do not use memory as the only copy of an incident record.

**Lifecycle.** Current memory guidance describes tool-use refresh after at least ten new completed investigations and no more than once every three days. Earlier learned-skill pages used different cadences; the memory and change-history pages take precedence. Agent Space understanding has its own refresh conditions.

**Proposed verification.** Proposed check: retain the entry version, start a later investigation of the same monitor and inspect available read evidence. Require current telemetry to support or refute the historical cause. Record recall as unverified if no read evidence is exposed.

Official documentation: [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Learned skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html) · [Managed agents and Learning history](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) · [Document history: reflections and memory changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/document-history.html) · [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)


### DM4 — Bound custom-agent schedules and execution

A custom-agent definition and its schedule are separate objects. A schedule starts invocations; it does not make an incomplete prompt or missing integration into a reliable daily report. Dynamic subagent delegation continues work within the configured tool and skill boundary.

1. Create the definition with a precise output contract: account/resource scope, time interval, required data, incomplete-result handling and allowed outputs.
2. Assign actual tool names from the connected toolbox through Chat; attach only the required skills and memory stores.
3. Run the agent manually and inspect its History and trajectory. Fix missing-source behavior before creating a recurring trigger.
4. Add a schedule on the Triggers tab using the documented cron or rate syntax and time basis. Review trigger state and invocation history separately.
5. Pause the trigger to stop future scheduled runs. Cancel an active invocation separately; in-flight tool calls may finish.

**Lifecycle.** Only one invocation per custom agent runs at a time under the documented execution model. Invocation timeouts and service quotas still apply; the schedule is not a completion-time guarantee.

**Proposed verification.** Proposed check: run a read-only configuration inventory against a small resource set with a deliberately missing source. Confirm an incomplete artifact rather than a fabricated all-clear report.

Official documentation: [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) · [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) · [Custom-agent outputs](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)


### DM5 — Separate three execution boundaries

Read-only investigation tools, optional investigation Sandbox execution and directed actions are different paths. Release testing is a fourth boundary: it sends real application requests. A single label such as 'human approved' is insufficient to describe all of them.

1. Use source IAM and provider credentials to constrain ordinary investigation reads.
2. For Sandbox preview, explicitly enable it per Agent Space and configure outbound allowlists and package prerequisites. The documented AWS CLI/SDK proxy is read-only; this does not make arbitrary outbound application endpoints harmless.
3. For directed actions, enable the Agent Space preference, configure the account's elevated role or permitted mutating third-party tool, and require the individual Chat approval.
4. For release testing, authorize the target environment and test identity before running the profile. Isolate external side effects; do not rely on the directed-action gate to intercept each form submission.

**Lifecycle.** Removing one execution path does not necessarily disable the others. Review role grants, tool opt-ins, sandbox egress and release profiles independently.

**Proposed verification.** Proposed check: verify denied reads, rejected directed approvals and blocked sandbox destinations independently. For release testing, inspect target-side audit logs and disposable-data cleanup.

Official documentation: [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [Set up a Sandbox: execution, egress and package configuration](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) · [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) · [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## Proposed operational procedures

### DU1 — Investigate a recurrent error-rate alarm without assuming the old cause

Decide whether the current incident supports the previous diagnosis and whether a mitigation is justified.

**Use when:** An identified alarm recurs after a deployment or dependency change. The team has access to current telemetry and a prior investigation.

**Not for:** Proving that the agent learns correctly from a single repeated answer, or automatically rolling back every deployment near an alarm.

**Functions used:** D03, D04, D05, D06, D07, D14

**Inputs**

- Alarm identifier, account, region, affected service and UTC start/end interval.
- Deployment/build identifiers and change times; request volume and error/latency measurements before and after the event.
- Prior investigation and memory entry/version, plus the corrected diagnosis if available.
- Named incident owner, allowed read sources and separate approval authority for any change.

1. **Operator — Confirm the event and scope.** Check the triggering resource and interval against the monitoring system. If identifiers or access are missing, correct those first rather than asking for a cause.

2. **Agent and operator — Inspect triage and form competing hypotheses.** If linked to an old incident incorrectly, unlink. Ask for current evidence for a deployment regression, a dependency failure and the remembered cause; these are proposed hypotheses, not product-supplied categories.

3. **Operator — Challenge the evidence.** Re-run a material log or metric query. Check whether errors preceded the deployment, whether unaffected instances differ, and whether the alleged dependency actually lies on the failed request path.

4. **Operator — Choose continuation or mitigation.** If evidence conflicts, steer or fork the investigation. If a cause is supported, review the mitigation's exact target, recovery signal and rollback condition; do not equate proposal generation with authorization.

5. **Operator — Record the result.** After independent verification, provide structured feedback and inspect any retained reflection. Keep the incident record as the durable source of truth.

**Acceptance:** A diagnosis tied to current observations, a stated alternative that was tested or left unresolved, and an explicit change/no-change decision. A Review may help assess the record but does not replace the telemetry check.

**Stop:** Stop causal claims when required logs are inaccessible, the interval is wrong or the deployment identity is unknown. Escalate to the owning engineer with the evidence gap.

**Example instruction**

```text
Investigate alarm <identifier> for <UTC interval> in <account/region>. Compare the prior diagnosis with current telemetry and deployment <build>. Separate observations, hypotheses and missing evidence. Propose mitigation only; do not change resources.
```

**Demonstration allocation:** 8 minutes.

- 1 min: Show the prepared event, build and scope; identify unavailable sources.
- 2 min: Inspect the stored memory and the current investigation's evidence side by side.
- 2 min: Challenge one causal claim with a source query; show an alternative explanation.
- 2 min: Review a mitigation proposal and explain the separate execution approval.
- 1 min: Show corrective feedback and the evidence needed to claim later recall.

**Fallback:** Use a clearly labeled prepared investigation export and source-query results. Do not invent a completed agent run during the demonstration.

Official documentation: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) · [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) · [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) · [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)


### DU2 — Configure a recurring configuration check without granting change authority

Produce a reviewable list of resources that violate a team-defined configuration rule.

**Use when:** A platform team already has a precise rule, inventory scope and tools capable of reading the relevant configuration.

**Not for:** An assertion that the product includes a universal compliance scanner or that generated findings certify compliance.

**Functions used:** D01, D02, D10

**Inputs**

- A small approved resource set and one explicit rule, such as a required configuration value.
- The exact read tool and returned field used to evaluate that rule.
- A fixture with compliant, non-compliant and inaccessible resources.
- An owner and a report destination; no mutation tools for the first run.

1. **Operator — Define the decision rule.** Write the exact field comparison and specify that inaccessible resources are unknown, not compliant.

2. **Operator — Create the custom agent.** Assign the minimal read toolbox and, only if needed, a reviewed custom context store. Inspect the saved configuration.

3. **Agent and operator — Run against the fixture.** Compare all three resource classes against the expected results. Require resource IDs, observed values and query timestamps in the proposed output contract.

4. **Operator — Add and supervise a trigger.** Enable the schedule only after the manual check passes. Inspect invocation history for failures; pause the trigger independently of cancelling an active invocation.

**Acceptance:** Every in-scope resource is classified as compliant, non-compliant or unknown with evidence. Missing access remains visible. No change action occurs.

**Stop:** Do not schedule if inventory is incomplete, the rule cannot be expressed against an observed field, or output turns access failures into compliant results.

**Example instruction**

```text
Create a read-only custom agent for <resource scope>. Evaluate <field/rule> using <approved tool>. Report resource ID, observed value, query time and compliant/non-compliant/unknown. Treat denied or missing data as unknown. Do not modify resources.
```

**Demonstration allocation:** 0 minutes.



**Fallback:** Review the definition and fixture locally; do not imply that a background schedule was exercised.

Official documentation: [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) · [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) · [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) · [Custom-agent outputs](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)


## Documentation qualifications

Some retrieved HTML pages expose older cached text than the same URL's current indexed documentation. The current change history and feature-specific updates are used for migrated memory and instruction locations. The sources register records the relevant pages; the guide does not preserve obsolete cadence claims as current behavior.

The release-testing page names different GitHub Action identifiers in its prose and sample. This guide does not publish a copy-paste workflow until the intended action and inputs are verified against its official repository.

No inference is made about vector databases, embedding models, training algorithms or a shared runtime across the three products. Documented observable behavior is the boundary.

The procedural-skill guide and newer Sandbox guidance describe different execution contexts. Code bundled with a skill is treated as Sandbox-specific preview behavior, not as a default skill capability.

## Official source register

- [Create an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html)

- [On-demand DevOps tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)

- [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

- [Invoke through a webhook](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-invoking-devops-agent-through-webhook.html)

- [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html)

- [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

- [Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

- [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

- [Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)

- [Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

- [Custom-agent outputs](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)

- [Memories: current stores, refresh and lifecycle](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

- [Learned skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)

- [Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

- [DevOps Agent skills](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

- [Managed agents and Learning history](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html)

- [Connect MCP servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html)

- [Connecting Slack](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-ticketing-and-chat-connecting-slack.html)

- [Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)

- [Release readiness code review](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html)

- [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

- [Set up a Sandbox: execution, egress and package configuration](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html)

- [What's new: dated behavior and UI changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

- [Document history: reflections and memory changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/document-history.html)

- [Feature availability by Region](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

No live product execution or measured operational benefit is claimed.
