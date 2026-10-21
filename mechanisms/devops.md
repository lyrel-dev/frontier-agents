# AWS DevOps Agent — mechanisms and enablement

Reviewed 21 October 2026. Independent checks and examples are proposed; no live workflow was executed.

## Mechanism model

A recurring alarm does not prove that its previous root cause has returned. Use historical context to select hypotheses, then test those hypotheses against current telemetry. The documentation describes retained Markdown knowledge, routing by descriptions, and a managed learning process. It does not document a customer-operated model-training switch.

Historical investigations → managed learning runs → versioned memory → relevance-based retrieval → a new investigation. User instructions, selected skills and tool permissions remain separate controls.

Documented operational mechanisms; controls and learning schedules are feature-specific. Managed-agent UI availability may vary by rollout.

## D-M01 — Recall recurring alarm causes

**Surface:** Agent Space / Operator Web App

**Availability:** Documented managed memory

**Activation:** Automatic learning; inspect and activate stores

### Documented mechanism

The learning agent summarizes earlier investigations into monitor-specific memory. At a new session, store descriptions are exposed first; relevant entries are fetched selectively rather than injecting every incident. Memory versions retain change history.

### Enable and configure

An Agent Space with investigation history and connected evidence sources.

1. Open Knowledge → Memories. Inspect the monitors store and its Active setting.

2. Open a monitor entry and review its evidence and versions. Use the store or entry toggle to allow or exclude recall.

3. Open Agents → Managed agents → Learning to inspect available history. Custom-agent attachment is a separate step; see D-M03.

### Scope and persistence

Current guidance: daily monitor-memory refresh when investigations exist in the preceding two weeks; a monitor memory without updates for two weeks can be removed. Full stores evict the oldest item.

### Independent checks — proposed

- In a non-production Agent Space, select a resolved incident whose cause was independently confirmed.

- Record its alarm identity, evidence links and memory version. Start a separate investigation using new evidence, not a duplicate event.

- Compare the agent’s cited past context with current logs. A matching conclusion alone is not proof that memory was read.

### Record to retain — proposed

Investigation IDs, memory/store identifier, version and timestamp, retrieved evidence, reviewer decision.

### Stop, correct or remove

Use memory/store toggles to stop recall. Chat can request a correction or deletion. Managed refresh may later regenerate relevant content.

### Limits and fallback

A previous cause is a hypothesis, not a finding about the current incident. The guide does not describe model-weight training.

When no memory is present, inspect recent learning activity and store activation; use the approved incident record explicitly and label the manual context.

### Illustrative task — not executed

Illustrative: “For this staging alarm, compare current evidence with relevant prior causes. Cite what was recalled and list disconfirming signals. Do not change resources.”

### Official guidance

[DM: DevOps Agent Memories](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

[DG: Managed agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html)

## D-M02 — Refresh environment and tool-use knowledge

**Surface:** Agent Space knowledge / topology

**Availability:** Documented; learned-skills migration in progress

**Activation:** Automatic refresh; manual regeneration available

### Documented mechanism

Environment, repository, pipeline and tool-use knowledge is maintained as managed memory. Older learned-skill entries move to Memories on their next refresh; no manual conversion is required.

### Enable and configure

Connected resources and integrations; recent completed investigations for activity-based refresh.

1. Open Knowledge and inspect the learned item. If it still appears under Skills, follow its migration state rather than creating a duplicate.

2. Use Topology → Regenerate, or request a refresh in chat.

3. Inspect the versioned summary in the console Summary report or web-app Artifacts.

### Scope and persistence

Environment understanding refreshes after discovery and relevant integration changes. Current memory guidance describes activity-gated refreshes and a separate tool-use threshold; exact cadence is not a delivery-time guarantee.

### Independent checks — proposed

- Compare one service-to-repository link with deployment configuration.

- Check the memory version after an authorized refresh; do not infer completion merely from clicking Regenerate.

- Audit one tool-use recommendation against a successful tool result and its permissions.

### Record to retain — proposed

Before/after knowledge versions, changed integration, a sampled dependency and supporting configuration.

### Stop, correct or remove

Managed-agent schedules belong to the service. Use supported regeneration and knowledge controls rather than inventing a cron override.

### Limits and fallback

Cached documentation differs on historical refresh thresholds. This guide does not use a numeric threshold as an acceptance criterion.

Keep a reviewer-approved topology snapshot as explicit context; investigate permission or discovery gaps before trusting the generated map.

### Illustrative task — not executed

Illustrative: “Refresh the environment understanding and report which version is now available. Distinguish observed dependencies from inferred relationships.”

### Official guidance

[DL: Learned Skills: migration to memory](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)

[DG: Managed agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html)

[DT: Topology and resource discovery](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html)

## D-M03 — Attach retained context to a custom agent

**Surface:** Custom agents / Operator Web App

**Availability:** Documented custom-agent configuration

**Activation:** Explicit attachment

### Documented mechanism

A custom agent can read attached memory stores and write to attached custom stores. Managed stores are read-only to custom agents. A newly created custom agent has no memory access until stores are attached.

### Enable and configure

An Agent Space with an integration, a custom agent and relevant stores.

1. Create a store through Knowledge → Memories → Create memory store; describe its subject and when it should be used.

2. Create or edit the custom agent and select the Memory stores field, or ask Chat to attach a named store.

3. Configure MCP tools separately through Chat; attaching knowledge does not grant a tool.

### Scope and persistence

Attachment is per custom agent, within its Agent Space. Managed chat and custom-agent write behavior must not be conflated.

### Independent checks — proposed

- Run a read-only task with a non-sensitive synthetic fact in an attached custom store.

- Compare the result with an otherwise equivalent agent without that attachment.

- Confirm the custom agent cannot treat managed history as its own editable store.

### Record to retain — proposed

Agent definition, store attachment list, test prompt, output and invocation ID.

### Stop, correct or remove

Remove an attachment in the agent’s configuration when the job no longer needs that context.

### Limits and fallback

Permission to read retained knowledge does not authorize infrastructure changes. Description matching does not guarantee recall on every run.

Pass the fact explicitly for this run and record the missing attachment; do not broaden all tools to solve a context problem.

### Illustrative task — not executed

Illustrative: “Attach staging-service-notes to the weekly-review agent. Permit only the tools needed to read investigations.”

### Official guidance

[DC: Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)

[DM: DevOps Agent Memories](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

## D-M04 — Apply always-on agent instructions

**Surface:** Agents → Managed agents → Agent definition

**Availability:** Documented instruction scopes

**Activation:** User configured

### Documented mechanism

Global and agent-specific AGENTS.md content is loaded for new sessions. Both scopes apply when relevant. An instruction update does not replace the content already loaded in an in-progress session.

### Enable and configure

Agent Space administration access and a reviewed instruction change.

1. Open a managed agent’s Agent definition.

2. Edit Global instructions for space-wide guidance, or Agent instructions for that agent type.

3. Save; global changes require confirmation. Start a new session to assess the revision.

### Scope and persistence

Global scope affects the Agent Space; specific scope affects that managed agent type.

### Independent checks — proposed

- Set a harmless output requirement and verify it in a new session.

- Check that an existing session is not being used to test a newly saved instruction.

- Keep a negative authorization test separate from the instruction test.

### Record to retain — proposed

Reviewed AGENTS.md revision, scope, approver, test session and resulting artifact.

### Stop, correct or remove

Download a copy before replacing or deleting instructions. Restore approved text through the editor when rolling back.

### Limits and fallback

Instructions are prompt context, not an IAM permission boundary or a guarantee that every requested behavior will occur.

Use explicit run-scoped instructions while investigating propagation; retain access restrictions in IAM.

### Illustrative task — not executed

Illustrative instruction: “Distinguish observed facts, hypotheses and missing evidence. Identify the source window for each operational claim.”

### Official guidance

[DI: Agent instructions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

## D-M05 — Load a procedure through a skill

**Surface:** Knowledge → Skills

**Availability:** Documented; this guide uses document-only skills

**Activation:** Description-based selection

### Documented mechanism

A skill packages instructions and references. The name and description guide relevance selection; agent-type targeting limits where it is offered.

### Enable and configure

An Agent Space and an approved procedure. This example requires no executable skill content.

1. Choose Knowledge → Skills → Add skill → Create skill.

2. Enter a specific name, applicability description and Markdown procedure; select intended agent types and Active status.

3. For packaged references, use the documented ZIP import with a root SKILL.md and required frontmatter.

### Scope and persistence

Skills are procedural context. They differ from informational memory and always-on instructions.

### Independent checks — proposed

- Use one task matching the description and one clearly unrelated task.

- Inspect whether the expected procedure and evidence requests appear.

- Review reference freshness; a well-formed skill can still contain an incorrect procedure.

### Record to retain — proposed

SKILL.md version, selected agent types, activation state and matched/unmatched test results.

### Stop, correct or remove

Edit the skill or set it Inactive to prevent use for new work.

### Limits and fallback

The skill page contains differing script-upload wording and a Sandbox-preview exception. Do not assume executable skill support from this document-only example.

Provide the approved procedure explicitly for the current run; improve its description rather than adding unrelated instructions.

### Illustrative task — not executed

Illustrative procedure: compare deployment time, application errors and dependency health before selecting a cause.

### Official guidance

[DS: DevOps Agent Skills](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## D-M06 — Discover resources without confusing scope with access

**Surface:** AWS accounts / topology

**Availability:** Documented topology discovery

**Activation:** Connected account discovery

### Documented mechanism

Topology discovery uses CloudFormation and, for tagged non-CloudFormation resources, AWS Resource Explorer. Observability and deployment data contribute relationships. Investigation can use accessible resources outside the displayed graph. For investigation sessions, effective permissions intersect the account role with the service-applied session policy; adding an IAM permission outside that policy does not make it usable.

### Enable and configure

Configured account connections and appropriately scoped roles; Resource Explorer enabled where its discovery is needed.

1. Verify the connected primary and source accounts.

2. Enable Resource Explorer in a target account when tagged resources outside CloudFormation must be discovered.

3. Inspect Topology. Restrict the account role to enforce actual access boundaries.

### Scope and persistence

Graph inclusion describes context, not authorization. IAM is the access boundary.

### Independent checks — proposed

- Compare a CloudFormation resource and an externally deployed tagged resource against inventory.

- Confirm an out-of-scope resource is inaccessible under the role, even if named in chat.

### Record to retain — proposed

Account/Region scope, sampled resource identifiers, role policy review and discovery comparison.

### Stop, correct or remove

Change role permissions to restrict access; removing a graph item alone is not sufficient.

### Limits and fallback

An absent node may indicate discovery or telemetry gaps, not absence of the deployed resource. Directed actions use a separate opt-in execution path; see D-M09.

Use current inventory as explicit context; resolve missing indexing or account permissions before accepting completeness.

### Illustrative task — not executed

Illustrative: “List which checkout resources were discovered and which evidence sources are missing. Do not treat the topology as an access policy.”

### Official guidance

[DT: Topology and resource discovery](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html)

[DA: Limiting agent access in an AWS account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

## D-M07 — Trigger investigations through authenticated events

**Surface:** Agent Space webhooks

**Availability:** Documented webhook integration

**Activation:** Explicit external event configuration

### Documented mechanism

An external HTTP event can enqueue an investigation. Generic webhooks support HMAC or bearer-token authentication; delivery acceptance does not prove that an investigation started.

### Enable and configure

An Agent Space, an authorized event sender and secure storage for the generated credential.

1. Open the Agent Space Capabilities tab and add a generic webhook.

2. Select HMAC or API key, save the one-time credential securely and configure the sender using the documented schema.

3. Send a controlled event with a unique incident ID and current timestamp; inspect the investigation, not only HTTP status.

### Scope and persistence

Credentials belong to the webhook. Duplicate events can be deduplicated.

### Independent checks — proposed

- Use a non-production event and trace sender ID to investigation ID.

- Confirm malformed or unauthorized requests do not become accepted work.

- Record rotation readiness without deliberately exposing production credentials.

### Record to retain — proposed

Redacted event, sender time, request result and investigation ID/status.

### Stop, correct or remove

Rotate the credential through the webhook editor and update the sender; removing the webhook stops that endpoint.

### Limits and fallback

Never include secrets in sample payloads. A successful HTTP response means queued processing, not a completed analysis.

Open the investigation manually with the same bounded context while fixing authentication, schema or deduplication issues.

### Illustrative task — not executed

Illustrative payload fields: incidentId, title, service, timestamp, current symptom and links to authorized evidence.

### Official guidance

[DW: Invoking DevOps Agent through Webhook](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-invoking-devops-agent-through-webhook.html)

## D-M08 — Schedule a bounded custom-agent job

**Surface:** Custom agent detail / Triggers

**Availability:** Documented custom-agent schedules

**Activation:** User-created schedule

### Documented mechanism

A custom agent can run on demand or through a schedule. Each invocation has a history entry and recorded tool activity. The managed learning schedule is a different, service-owned mechanism.

### Enable and configure

A custom agent with only the required tools, skills and stores.

1. Open the custom agent and use Run Now to validate its configuration.

2. In Triggers, create a Schedule and provide the documented cron or rate expression.

3. Inspect the listed next-run time and the invocation History after execution.

### Scope and persistence

Each invocation uses the configured custom-agent scope. A schedule is not a broader permission grant.

### Independent checks — proposed

- Use a daily read-only staging review with a narrow time window.

- Confirm the actual run time, tools used and output completeness.

- Verify no unexpected external publication occurred.

### Record to retain — proposed

Agent revision, schedule expression and timezone interpretation, invocation trace, report and owner.

### Stop, correct or remove

Review or remove the schedule through trigger management when no longer needed; do not assume removing a future trigger cancels an active invocation.

### Limits and fallback

Report generation requires suitable source access and an explicit output definition. No completion-time guarantee follows from the schedule.

Run the approved task on demand, or perform the review manually, until scheduled execution is verified.

### Illustrative task — not executed

Illustrative: “Summarize completed staging investigations for the last day. Retain unresolved evidence gaps. Do not create tickets.”

### Official guidance

[DX: Executing custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

[DC: Creating a custom agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)

## D-M09 — Authorize mutating directed actions

**Surface:** Agent Space and per-account associations

**Availability:** Documented; disabled by default

**Activation:** Layered opt-in plus per-action approval

### Documented mechanism

Directed actions require an enabled Agent Space, an elevated account role or tool configuration, and operator approval for the specific mutation. The role is a permission ceiling; execution is further scoped.

### Enable and configure

Authorized administrators and operators; a deliberately restricted elevated role for the target account.

1. Enable directed actions in Agent Space settings.

2. Register the target account’s elevated role; follow the documented trust policy and action restrictions.

3. Review the proposed operation, resource, parameters and rollback before approving a single action.

### Scope and persistence

Read-only investigation remains available without elevated access. Tool classifications and roles are not memory settings.

### Independent checks — proposed

- Use a reversible staging change only after separate authorization.

- Check the approved operation and resource against CloudTrail and actual state.

- Reject a deliberately out-of-scope proposal; confirm no mutation occurred.

### Record to retain — proposed

Approval identity, operation/parameters, role scope, audit event and rollback verification.

### Stop, correct or remove

Disable directed actions at the Agent Space to remove elevated capability. Approved execution is attributable in CloudTrail.

### Limits and fallback

The API preferences update replaces the supplied preference map; preserve other settings. Do not infer that all AWS operations are supported.

Keep the investigation read-only and hand the reviewed change to the normal deployment process.

### Illustrative task — not executed

Illustrative: “Describe the proposed staging change and rollback. Request approval before any mutation.”

### Official guidance

[DE: Directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## Proposed use-case exercise

Test recall without assuming the old cause has returned

Optional 12-minute walkthrough; additional to the core programme. Not an agent-runtime guarantee.

Use a non-production Agent Space with a resolved, independently reviewed incident and a distinct new investigation. Keep directed actions disabled. Use prepared records if no managed memory is yet available.

### 1. Scope the comparison · 00:00–01:30

**Role:** Incident owner · **Mechanism:** D-M06

Name the old incident, a new symptom window and the read-only resource boundary.

**Gate:** Two distinct investigation IDs and an agreed evidence window.

### 2. Inspect retained knowledge · 01:30–03:30

**Role:** Operator · **Mechanism:** D-M01

Inspect Knowledge → Memories for the relevant monitor and its versions.

**Gate:** Entry is relevant, active and traceable to the reviewed incident.

### 3. Check the consumer · 03:30–05:30

**Role:** Agent administrator · **Mechanism:** D-M03

For a custom agent, explicitly attach the chosen store.

**Gate:** Correct store attached; no unrelated tool access added.

### 4. Start a separate investigation · 05:30–08:00

**Role:** Operator · **Mechanism:** D-M01

Ask for current evidence and disconfirming observations.

**Gate:** New task, current data and a record of recalled context if observable.

### 5. Challenge the conclusion · 08:00–10:30

**Role:** Service reviewer · **Mechanism:** D-M02

Compare proposed cause with telemetry; do not count a matching narrative as proof of recall.

**Gate:** Independent evidence supports or rejects the hypothesis.

### 6. Correct or exclude stale knowledge · 10:30–12:00

**Role:** Knowledge owner · **Mechanism:** D-M01

Update or deactivate an incorrect item and retain the review record.

**Gate:** Correction recorded and assessed in a new session.

### Exit

Accept only when the new conclusion is supported by current evidence and the retained context is correctly scoped. Record recall as unproven when no read evidence is available.

### Fallback

Use a prepared memory record and investigation trace. Do not wait for the managed learning schedule during a live session.
