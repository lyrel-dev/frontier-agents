# AWS DevOps Agent — platform capabilities and mechanisms

Platform resources, configuration, contextual state, execution and authorization. Operational scenarios are applications of these capabilities, not capability names.

Availability is feature-specific. Sandbox is documented as preview and investigation-only in the reviewed guidance. Confirm feature and Region eligibility before configuration.

## Classification

**Platform capability**: A reusable ability exposed by the platform. Example: Retain operational context across investigations.

**Operation**: An action on a platform resource or configuration object. Example: Attach a memory store or change its active state.

**Mechanism**: The documented process connecting inputs, state, execution and outputs. Example: Select a store by description, then retrieve relevant entries.

**Use case**: An engineering problem that combines capabilities and mechanisms. Example: Investigate a recurring alarm while checking contradictory telemetry.

## Capability inventory

### D-C01 — Scoped operational workspaces

**Group:** Scope and connectivity

An Agent Space binds infrastructure access, integrations and operator access to a configured operational context.

**Platform resources:** Agent Space; resource-investigation role; operator web-app role.

**Supported operations:** Create a space; associate accounts and integrations; configure the separate roles.

**Boundary:** Workspace membership does not override the permission policies on connected resources.

**Sources:** [D01](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html)

### D-C02 — Selected external-tool access

**Group:** Scope and connectivity

Account-level MCP providers expose tools that are explicitly associated with individual Agent Spaces.

**Platform resources:** Capability provider; authentication configuration; Agent Space association; selected tools.

**Supported operations:** Register and authenticate a provider; associate it; select tools; update supported connection settings.

**Boundary:** Streamable HTTP transport, network reachability, authentication, selected tools and action classification are separate concerns.

**Sources:** [D02](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [D12](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

### D-C03 — Private integration connectivity

**Group:** Scope and connectivity

Private connections provide a network path to endpoints hosted inside a VPC.

**Platform resources:** Private connection and endpoint configuration.

**Supported operations:** Create a connection in the Agent Space Region; configure endpoint routing and network access.

**Boundary:** Cross-Region reachability requires additional customer connectivity. Network access does not grant application authorization.

**Sources:** [D03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html)

### D-C04 — Environment knowledge maintenance

**Group:** Context and behavior

A managed learning agent examines infrastructure, dependencies, pipelines and previous investigations to produce environment-specific knowledge.

**Platform resources:** Managed learning agent; learned knowledge; History and Triggers views.

**Supported operations:** Inspect learning runs and their triggers; inspect the produced knowledge.

**Boundary:** Learning schedules are platform-owned. Learned skills are transitioning automatically to memory; consult the current memory representation rather than assuming a separate permanent store.

**Sources:** [D04](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [D15](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)

### D-C05 — Persistent contextual knowledge

**Group:** Context and behavior

Managed and custom memory stores retain synthesized information that an agent can selectively retrieve across sessions.

**Platform resources:** Memory store; Markdown memory entry; description; immutable versions; active state.

**Supported operations:** Inspect entries and versions; activate or deactivate stores and entries; maintain custom context; attach stores to custom agents.

**Boundary:** Context retrieval is not customer-controlled model-weight training. Stored information does not establish that it was used or that a new diagnosis is correct.

**Sources:** [D05](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [D09](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

### D-C06 — Standing instruction injection

**Group:** Context and behavior

Global and agent-specific AGENTS.md content is included at the start of applicable sessions.

**Platform resources:** Global instructions and managed-agent instructions.

**Supported operations:** Edit the appropriate Agent definition; save content; start a new session.

**Boundary:** Existing sessions retain startup content. Prompt guidance is not a deterministic authorization control.

**Sources:** [D06](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

### D-C07 — Conditional procedural guidance

**Group:** Context and behavior

Skills supply reusable procedures and supporting material when their descriptions match the work and their agent scope applies.

**Platform resources:** SKILL.md; optional supporting resources; description; agent-type targeting.

**Supported operations:** Create or import a skill; select its scope; revise its description and procedure.

**Boundary:** An available skill is not necessarily selected. Procedural instructions, informational memory and always-loaded instructions are distinct.

**Sources:** [D07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

### D-C08 — Constrained custom-agent definitions

**Group:** Execution and control

A custom-agent definition combines a system prompt with selected tools, skills and attached memory stores.

**Platform resources:** Custom agent; prompt; tool selection; skill and store attachments.

**Supported operations:** Create or edit the definition; use Chat to configure tools; attach only required stores.

**Boundary:** New custom agents have no memory attachments. Attached managed stores are read-only to the custom agent; attached custom stores can support writes.

**Sources:** [D08](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [D09](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

### D-C09 — Explicit invocation and scheduling

**Group:** Execution and control

Built-in investigations and custom-agent invocations expose different initiation paths.

**Platform resources:** Investigation; webhook or connected incident system; custom-agent trigger; invocation.

**Supported operations:** Start an investigation manually or through supported incident integration; run a custom agent on demand or on a schedule.

**Boundary:** Do not describe built-in incident triggers and custom-agent schedules as one interchangeable event framework.

**Sources:** [D09](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [D10](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

### D-C10 — Investigation-local computation

**Group:** Execution and control

Sandbox supplies an ephemeral Linux execution environment with configurable dependencies and outbound access rules.

**Platform resources:** Agent Space Sandbox settings; package configuration; network allowlist.

**Supported operations:** Opt in; configure permitted packages and outbound endpoints; inspect a controlled investigation execution.

**Boundary:** The reviewed preview guidance limits this execution surface to investigations. It is not durable memory or a general deployment runner.

**Sources:** [D11](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html), [D14](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

### D-C11 — Authorized state-changing actions

**Group:** Execution and control

Directed actions allow eligible mutations only after separate enablement, access configuration and specific approval.

**Platform resources:** Agent Space setting; account elevated role; tool classification; approval record.

**Supported operations:** Enable the feature; configure eligible accounts and tools; review, adjust, approve or reject a proposed operation.

**Boundary:** A mitigation recommendation is not permission to execute it. A configured elevated role is a permission ceiling, not standing approval.

**Sources:** [D12](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

### D-C12 — Configuration resources and execution evidence

**Group:** Execution and control

Asset APIs manage supported configuration resources; invocation trajectories expose tool calls and outputs for inspection.

**Platform resources:** Asset records and identifiers; custom-agent invocation trajectory.

**Supported operations:** Manage supported assets programmatically; inspect a run and its outputs.

**Boundary:** Use asset identifiers where required by the API. A recorded trajectory is evidence of execution, not independent verification of the conclusion.

**Sources:** [D13](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html), [D09](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

## Mechanisms and enablement

### D-M01 — Recurring-monitor knowledge production

**Capabilities:** D-C04, D-C05

**Trigger:** Recent investigations within the Agent Space.

**Process:** Completed investigations → Managed learning process → Per-monitor synthesized entries → Later investigation context

The monitors store groups recurring cause history by alarm or metric. The documented daily learning process runs when there are investigations within the preceding two weeks; it retains per-investigation evidence.

**State and lifecycle:** Entries without updates for two weeks are removed; capacity pressure removes the oldest item. This store is bounded operational context, not an incident archive.

**Enablement:**

1. Confirm the Agent Space has completed investigations and inspect the managed learning agent History.
2. Open Knowledge → Memories and inspect the monitors store and matching entry.
3. Confirm the store and entry are active; monitor memory is documented as enabled by default.

**Controls:** Keep current telemetry authoritative when it contradicts historical patterns. Learning runs and data retention are not a model-training control.

**Proposed verification:** Proposed check: retain an earlier verified cause, inspect the resulting entry, then examine a later incident with a different cause but similar symptom. Distinguish entry existence, observable retrieval and diagnosis correctness.

**Sources:** [D04](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [D05](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [D14](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

### D-M02 — Corrective-feedback reflections

**Capabilities:** D-C04, D-C05

**Trigger:** An operator supplies corrective feedback on a completed investigation.

**Process:** Completed diagnosis → Verified correction → Reflection memory → Future alarm investigation

The documented reflections store records lessons about a missed or incorrect cause. Feedback submission and recurring-monitor synthesis are different production paths.

**State and lifecycle:** Feedback can be updated; the latest submission replaces prior feedback for that investigation. Do not assume that every downstream state is immediately refreshed.

**Enablement:**

1. Open the completed investigation and choose Add feedback, or provide the correction through Chat.
2. Record the verdict and actual cause; inspect the relevant memory under Knowledge → Memories.
3. Treat the separate opt-in to share feedback with AWS as a distinct decision.

**Controls:** Use a verified correction, not a convenient hypothesis. AWS sharing requires explicit confirmation; local feedback and external sharing are not the same operation.

**Proposed verification:** Proposed check: link the correction to the original evidence, inspect the stored lesson, and challenge the next diagnosis using current contradictory evidence. Without visible access evidence, report recall as unverified.

**Sources:** [D10](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [D05](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [D14](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

### D-M03 — Selective retrieval and store attachment

**Capabilities:** D-C05, D-C08

**Trigger:** An agent session needs contextual information relevant to its task.

**Process:** Store descriptions → Relevant store selection → Entry descriptions → Selected full content

The documented retrieval sequence exposes descriptions before full content. For custom agents, store attachments constrain the accessible collection; new agents start without attachments.

**State and lifecycle:** Updates create immutable entry versions. Deactivating a store or entry removes it from active access without deleting it.

**Enablement:**

1. Write specific descriptions stating the store subject and relevant situations.
2. Edit the custom agent and attach only required stores; inspect the resulting definition.
3. Use supported controls to deactivate stale entries and examine previous versions.

**Controls:** A custom agent can write to attached custom stores; attached managed stores remain read-only. Retrieval internals beyond the documented description-selection process are not asserted.

**Proposed verification:** Proposed check: compare an agent with and without a non-sensitive test-store attachment. Inspect observable reads and verify the answer independently. A repeated phrase alone does not prove retrieval.

**Sources:** [D05](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [D08](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [D09](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

### D-M04 — Startup instruction injection

**Capabilities:** D-C06

**Trigger:** A new applicable agent session starts.

**Process:** Saved global instructions → Agent-specific instructions → Startup context → Session behavior

The service retrieves applicable AGENTS.md content at startup rather than letting the agent select it by relevance.

**State and lifecycle:** Saved changes apply to new sessions; already-running sessions keep their startup content.

**Enablement:**

1. Open Agents → Managed agents and select the relevant agent.
2. On Agent definition, edit Global instructions or that agent's own instructions.
3. Save and start a new session to assess the change.

**Controls:** Global changes affect all applicable managed agents. Instructions guide behavior but do not expand or restrict IAM authorization by themselves.

**Proposed verification:** Proposed check: use a harmless output-format instruction, compare a pre-existing session with a new one, and record the content revision used. Treat compliance as observed behavior, not guaranteed policy enforcement.

**Sources:** [D06](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

### D-M05 — Description-based skill selection

**Capabilities:** D-C07

**Trigger:** The current task matches a skill description and agent-type scope.

**Process:** Task and agent type → Skill description → Procedure loading → Tool-guided work

Skills supply procedural instructions through SKILL.md and optional supporting resources. They are selected on demand rather than unconditionally injected like standing instructions.

**State and lifecycle:** Description, procedure and scope are separate configuration fields that should be maintained together.

**Enablement:**

1. Open Knowledge → Skills and add or import the procedure.
2. Write a description defining when it applies and select the relevant agent types.
3. Verify available tools separately; a procedure cannot grant missing tool permissions.

**Controls:** An enabled skill can remain unused when its description or scope does not match. A skill is not an authorization boundary.

**Proposed verification:** Proposed check: submit one matching and one nonmatching task. Inspect available invocation evidence for selection instead of inferring it solely from answer wording.

**Sources:** [D07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html), [D06](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

### D-M06 — Tool association and directed-action authorization

**Capabilities:** D-C02, D-C03, D-C11

**Trigger:** The agent selects an associated external tool or proposes an eligible AWS-resource mutation.

**Process:** Registered provider or account → Scoped access and tool class → Specific approval → Attributed execution

MCP registration, authentication, Agent Space association and selected tools establish availability. Mutating operations additionally require directed-action controls. AWS actions use the configured elevated role and approval scoped to the operation and resource.

**State and lifecycle:** Provider configuration, selected tools, role policies and approvals are different records. Approval is not reusable for a different operation or resource.

**Enablement:**

1. Register and authenticate the provider, associate it with the Agent Space, and select the required tools.
2. Review tool classifications explicitly. Programmatically registered tools without classification are documented to default to READ_ONLY.
3. For eligible mutations, enable directed actions and configure the account role or integration; review the exact operation before approval.

**Controls:** Misclassifying a mutating server tool as read-only is an operational hazard. Destructive third-party tools are a separate non-invocable class. A network path does not grant application access.

**Proposed verification:** Proposed check: in an authorized test environment, verify a read, a rejected mutation and one narrowly approved mutation. Retain tool parameters, approval identity and independent resource state before and after.

**Sources:** [D02](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [D03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html), [D12](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

### D-M07 — Ephemeral sandbox execution

**Capabilities:** D-C10

**Trigger:** An investigation uses the explicitly enabled Sandbox capability.

**Process:** Agent Space configuration → Investigation runtime → Permitted code and network work → Investigation output

The platform provides investigation-local computation with preconfigured packages and outbound endpoint rules. This execution surface is separate from directed-action authorization.

**State and lifecycle:** The environment is ephemeral and scoped to an investigation; do not use it as a persistent knowledge store.

**Enablement:**

1. Open Capabilities → Sandbox → Configure for the Agent Space.
2. Opt in and set package requirements and permitted outbound hosts, methods and paths.
3. Confirm current feature and Region availability before an authorized test investigation.

**Controls:** The reviewed preview scope is investigations, not all chat or custom-agent work. Network permissions and workload permissions remain separate controls.

**Proposed verification:** Proposed check: run a harmless computation, confirm allowed and denied outbound requests, and verify that the output is retained in investigation evidence rather than assumed to persist in the runtime.

**Sources:** [D11](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html), [D14](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

## Optional verification exercise

Verify contextual recall without accepting a stale diagnosis

Proposed prepared-result exercise; no live execution or runtime guarantee; 8 minutes.

1. 2 min — Inspect a completed investigation and its verified correction.
2. 2 min — Inspect the monitor entry or reflection and its current state.
3. 2 min — Review a later invocation for observable retrieval evidence.
4. 2 min — Challenge the conclusion with current contradictory telemetry and record unknowns.

**Acceptance:** Report three separate outcomes: memory exists, memory use is observable or unverified, and diagnosis is independently supported or rejected.

## Evidence boundary

Official product documentation supports the product statements. Configuration steps are documented guidance; verification exercises are proposed and were not executed. Selected critical sources were rechecked on 21 October 2026; other links are retained from the preceding review. This is not an exhaustive service catalog, a fresh audit of every historical claim, or a live AWS test.

## Official source register

- [D01 — Creating an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html) — retained from preceding review
- [D02 — Connecting MCP servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) — selected content rechecked
- [D03 — Connecting to privately hosted tools](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html) — retained from preceding review
- [D04 — Managed agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) — selected content rechecked
- [D05 — DevOps Agent memories](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) — selected content rechecked
- [D06 — Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) — selected content rechecked
- [D07 — DevOps Agent skills](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) — selected content rechecked
- [D08 — Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) — selected content rechecked
- [D09 — Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) — selected content rechecked
- [D10 — Incident initiation and corrective feedback](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) — selected content rechecked
- [D11 — Set up a Sandbox](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) — retained from preceding review
- [D12 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) — selected content rechecked
- [D13 — Managing assets](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html) — retained from preceding review
- [D14 — Documented changes and defaults](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) — selected content rechecked
- [D15 — Learned skills and migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html) — selected content rechecked
