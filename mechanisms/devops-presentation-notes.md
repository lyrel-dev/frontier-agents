# AWS DevOps Agent — mechanism reference speaker notes

All reference slides are untimed. Optional exercises are additional to the core programme.

## D-M01 — Recall recurring alarm causes

The learning agent summarizes earlier investigations into monitor-specific memory. At a new session, store descriptions are exposed first; relevant entries are fetched selectively rather than injecting every incident. Memory versions retain change history.

**Setup:** Open Knowledge → Memories. Inspect the monitors store and its Active setting. Open a monitor entry and review its evidence and versions. Use the store or entry toggle to allow or exclude recall. Open Agents → Managed agents → Learning to inspect available history. Custom-agent attachment is a separate step; see D-M03.

**Proposed verification:** In a non-production Agent Space, select a resolved incident whose cause was independently confirmed. Record its alarm identity, evidence links and memory version. Start a separate investigation using new evidence, not a duplicate event. Compare the agent’s cited past context with current logs. A matching conclusion alone is not proof that memory was read.

**Boundary:** A previous cause is a hypothesis, not a finding about the current incident. The guide does not describe model-weight training.

## D-M02 — Refresh environment and tool-use knowledge

Environment, repository, pipeline and tool-use knowledge is maintained as managed memory. Older learned-skill entries move to Memories on their next refresh; no manual conversion is required.

**Setup:** Open Knowledge and inspect the learned item. If it still appears under Skills, follow its migration state rather than creating a duplicate. Use Topology → Regenerate, or request a refresh in chat. Inspect the versioned summary in the console Summary report or web-app Artifacts.

**Proposed verification:** Compare one service-to-repository link with deployment configuration. Check the memory version after an authorized refresh; do not infer completion merely from clicking Regenerate. Audit one tool-use recommendation against a successful tool result and its permissions.

**Boundary:** Cached documentation differs on historical refresh thresholds. This guide does not use a numeric threshold as an acceptance criterion.

## D-M03 — Attach retained context to a custom agent

A custom agent can read attached memory stores and write to attached custom stores. Managed stores are read-only to custom agents. A newly created custom agent has no memory access until stores are attached.

**Setup:** Create a store through Knowledge → Memories → Create memory store; describe its subject and when it should be used. Create or edit the custom agent and select the Memory stores field, or ask Chat to attach a named store. Configure MCP tools separately through Chat; attaching knowledge does not grant a tool.

**Proposed verification:** Run a read-only task with a non-sensitive synthetic fact in an attached custom store. Compare the result with an otherwise equivalent agent without that attachment. Confirm the custom agent cannot treat managed history as its own editable store.

**Boundary:** Permission to read retained knowledge does not authorize infrastructure changes. Description matching does not guarantee recall on every run.

## D-M04 — Apply always-on agent instructions

Global and agent-specific AGENTS.md content is loaded for new sessions. Both scopes apply when relevant. An instruction update does not replace the content already loaded in an in-progress session.

**Setup:** Open a managed agent’s Agent definition. Edit Global instructions for space-wide guidance, or Agent instructions for that agent type. Save; global changes require confirmation. Start a new session to assess the revision.

**Proposed verification:** Set a harmless output requirement and verify it in a new session. Check that an existing session is not being used to test a newly saved instruction. Keep a negative authorization test separate from the instruction test.

**Boundary:** Instructions are prompt context, not an IAM permission boundary or a guarantee that every requested behavior will occur.

## D-M05 — Load a procedure through a skill

A skill packages instructions and references. The name and description guide relevance selection; agent-type targeting limits where it is offered.

**Setup:** Choose Knowledge → Skills → Add skill → Create skill. Enter a specific name, applicability description and Markdown procedure; select intended agent types and Active status. For packaged references, use the documented ZIP import with a root SKILL.md and required frontmatter.

**Proposed verification:** Use one task matching the description and one clearly unrelated task. Inspect whether the expected procedure and evidence requests appear. Review reference freshness; a well-formed skill can still contain an incorrect procedure.

**Boundary:** The skill page contains differing script-upload wording and a Sandbox-preview exception. Do not assume executable skill support from this document-only example.

## D-M06 — Discover resources without confusing scope with access

Topology discovery uses CloudFormation and, for tagged non-CloudFormation resources, AWS Resource Explorer. Observability and deployment data contribute relationships. Investigation can use accessible resources outside the displayed graph. For investigation sessions, effective permissions intersect the account role with the service-applied session policy; adding an IAM permission outside that policy does not make it usable.

**Setup:** Verify the connected primary and source accounts. Enable Resource Explorer in a target account when tagged resources outside CloudFormation must be discovered. Inspect Topology. Restrict the account role to enforce actual access boundaries.

**Proposed verification:** Compare a CloudFormation resource and an externally deployed tagged resource against inventory. Confirm an out-of-scope resource is inaccessible under the role, even if named in chat.

**Boundary:** An absent node may indicate discovery or telemetry gaps, not absence of the deployed resource. Directed actions use a separate opt-in execution path; see D-M09.

## D-M07 — Trigger investigations through authenticated events

An external HTTP event can enqueue an investigation. Generic webhooks support HMAC or bearer-token authentication; delivery acceptance does not prove that an investigation started.

**Setup:** Open the Agent Space Capabilities tab and add a generic webhook. Select HMAC or API key, save the one-time credential securely and configure the sender using the documented schema. Send a controlled event with a unique incident ID and current timestamp; inspect the investigation, not only HTTP status.

**Proposed verification:** Use a non-production event and trace sender ID to investigation ID. Confirm malformed or unauthorized requests do not become accepted work. Record rotation readiness without deliberately exposing production credentials.

**Boundary:** Never include secrets in sample payloads. A successful HTTP response means queued processing, not a completed analysis.

## D-M08 — Schedule a bounded custom-agent job

A custom agent can run on demand or through a schedule. Each invocation has a history entry and recorded tool activity. The managed learning schedule is a different, service-owned mechanism.

**Setup:** Open the custom agent and use Run Now to validate its configuration. In Triggers, create a Schedule and provide the documented cron or rate expression. Inspect the listed next-run time and the invocation History after execution.

**Proposed verification:** Use a daily read-only staging review with a narrow time window. Confirm the actual run time, tools used and output completeness. Verify no unexpected external publication occurred.

**Boundary:** Report generation requires suitable source access and an explicit output definition. No completion-time guarantee follows from the schedule.

## D-M09 — Authorize mutating directed actions

Directed actions require an enabled Agent Space, an elevated account role or tool configuration, and operator approval for the specific mutation. The role is a permission ceiling; execution is further scoped.

**Setup:** Enable directed actions in Agent Space settings. Register the target account’s elevated role; follow the documented trust policy and action restrictions. Review the proposed operation, resource, parameters and rollback before approving a single action.

**Proposed verification:** Use a reversible staging change only after separate authorization. Check the approved operation and resource against CloudTrail and actual state. Reject a deliberately out-of-scope proposal; confirm no mutation occurred.

**Boundary:** The API preferences update replaces the supplied preference map; preserve other settings. Do not infer that all AWS operations are supported.

## D-M10 — Record a corrected cause through investigation feedback

Corrective feedback can create a memory in the reflections store for later investigations of the alarm. This is distinct from recurring-cause summaries and does not establish model-weight training.

**Setup:** Open the completed investigation and choose Add feedback, or provide the correction in Chat. Select an incorrect verdict and supply the actual root cause. Sharing with AWS requires separate confirmation. Inspect Knowledge → Memories → reflections and retain the relevant entry and version.

**Proposed verification:** Proposed: use a reviewed, non-production incident whose established cause differs from the original result. Record feedback and any resulting reflection; check a separate investigation against new evidence. Report recall as unverified unless the run exposes evidence that the memory was read.

**Boundary:** A reflection is retained context, not proof of a future diagnosis or broader execution authority.

## Optional use-case exercise



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

### 6. Record a corrected outcome · 10:30–12:00

**Role:** Incident reviewer · **Mechanism:** D-M10

Submit the reviewed cause using Add feedback; inspect the reflection or a prepared record.

**Gate:** Feedback and memory version retained; later recall checked separately.

### Exit

Accept only when the new conclusion is supported by current evidence and the retained context is correctly scoped. Record recall as unproven when no read evidence is available.

### Fallback

Use a prepared memory record and investigation trace. Do not wait for the managed learning schedule during a live session.

