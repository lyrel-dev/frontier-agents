# Shared architecture — presenter reference



The schedule includes prepared-result exercises. It is not a promise of live agent completion time. Questions and breaks are additional. Canonical guide sections are reproduced in speaker notes as reference, not as a required verbatim script.



## 1. The three services expose different resource models

**Schedule:** 00:00–02:00. **Type:** table.

Use platform-specific identifiers rather than a universal ambiguous agent ID.

**Display content:**

Layer | DevOps | Security | FinOps

Scope | Agent Space | Application + shared resources | Agent instance

Configuration | Agents, tools, knowledge | Assessment definitions | Context, automations, connections

Execution | Investigation / invocation | Run / revalidation job | Conversation / task

**Canonical reference:** [A-01](../guides/architecture.html#A-01)



## 2. Retained context has different producers and lifecycles

**Schedule:** 02:00–04:00. **Type:** table.

Do not reduce these to one “learning enabled” setting.

**Display content:**

Material | Producer | Consumer

Monitor knowledge | Managed investigation learning | Relevant later investigation

Login skill | Successful authentication navigation | Later login

Reference file | Operator upload | Agent task or conversation

Conversational memory | Preferences/corrections | Later session

**Canonical reference:** [A-02](../guides/architecture.html#A-02)



## 3. Connectivity is not authorization

**Schedule:** 04:00–06:00. **Type:** flow.

Test each layer with observed results and an expected denial.

**Display content:**

Route | Can the endpoint be reached?

Identity | Who authenticated?

Permission | Which operation is allowed?

Behavior | What does prompt guidance request?

**Canonical reference:** [A-03](../guides/architecture.html#A-03)



## 4. The effect determines the relevant approval boundary

**Schedule:** 06:00–08:00. **Type:** table.

No universal “read-only” or “human-approved” label is sufficient.

**Display content:**

Effect | Control to inspect

Resource mutation | Specific directed-action authorization

Application testing | Targets, credentials, exclusions and permitted effects

Source change | Repository review and deployment controls

External publication | Destination and invocation-specific approval

**Canonical reference:** [A-04](../guides/architecture.html#A-04)



## 5. Configuration, runs and artifacts have separate lifecycles

**Schedule:** 08:00–10:00. **Type:** columns.

Stopping future starts does not reverse completed effects.

**Display content:**

Future work | Pause a schedule or disable an automation.

Current work | Cancel the invocation/task using its supported control.

Retained evidence | Manage versions, findings, files and artifacts according to their own semantics.

**Canonical reference:** [A-05](../guides/architecture.html#A-05)



## 6. A handoff transfers evidence—not credentials or authority

**Schedule:** 10:00–12:00. **Type:** flow.

The receiving team obtains its own access and makes its own authorization decision.

**Display content:**

Origin | Platform, configuration and execution IDs

Subject | Service, revision and UTC observation window

Request | Owner, question and permitted effect

Acceptance | Required evidence and unresolved questions

**Canonical reference:** [A-06](../guides/architecture.html#A-06)



## 7. Keep implementation unknowns visible

**Schedule:** 12:00–14:00. **Type:** columns.

An attractive diagram is not evidence of undocumented internals.

**Display content:**

Documented | Resource relationships, selected controls, retention and execution behavior.

Not established | Shared vector database, retrieval-ranking algorithm, cross-agent runtime or model-training pipeline.

**Canonical reference:** [A-07](../guides/architecture.html#A-07)



## 8. Tabletop: three observations, three evidence obligations

**Schedule:** 14:00–18:00. **Type:** demo.

Synthetic comparison; no shared runtime or live execution assumed.

**Display content:**

0–1 min | Identify the required inputs | Latency evidence, authorization identity and cost basis

1–3 min | Check consistency | Same intended revision, target and comparable windows

3–4 min | Assign unresolved questions | Do not invent a single shared root cause

**Canonical reference:** [A-U01](../guides/architecture.html#A-U01)



## 9. Accept documents on operating usefulness

**Schedule:** 18:00–20:00. **Type:** columns.

Link and layout checks are necessary but do not prove technical completeness.

**Display content:**

Model | Resources and scope are clear before a scenario begins.

Procedure | Inputs, choices, confirmation and failure paths are described.

Evidence | Claims have sources; examples and live outcomes are not conflated.

**Canonical reference:** [A-07](../guides/architecture.html#A-07)


