# Shared architecture — HTML presentation reference



Open [architecture.html](architecture.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. The three services expose different resource models

**Chapter:** Resource and context models. **Schedule:** 00:00–02:00. **Slide budget:** 02:00.

Use platform-specific identifiers rather than a universal ambiguous agent ID.



Layer | DevOps | Security | FinOps

Scope | Agent Space | Application + shared resources | Agent instance

Configuration | Agents, tools, knowledge | Assessment definitions | Context, automations, connections

Execution | Investigation / invocation | Run / revalidation job | Conversation / task



**Guide:** [A-01](../guides/architecture.html#A-01)



## 2. Retained context has different producers and lifecycles

**Chapter:** Resource and context models. **Schedule:** 02:00–04:00. **Slide budget:** 02:00.

Do not reduce these to one “learning enabled” setting.



Material | Producer | Consumer

Monitor knowledge | Managed investigation learning | Relevant later investigation

Login skill | Successful authentication navigation | Later login

Reference file | Operator upload | Agent task or conversation

Conversational memory | Preferences/corrections | Later session



**Guide:** [A-02](../guides/architecture.html#A-02)



## 3. Connectivity is not authorization

**Chapter:** Access and effect boundaries. **Schedule:** 04:00–06:00. **Slide budget:** 02:00.

Test each layer with observed results and an expected denial.



Route | Can the endpoint be reached?

Identity | Who authenticated?

Permission | Which operation is allowed?

Behavior | What does prompt guidance request?



**Guide:** [A-03](../guides/architecture.html#A-03)



## 4. The effect determines the relevant approval boundary

**Chapter:** Access and effect boundaries. **Schedule:** 06:00–08:00. **Slide budget:** 02:00.

No universal “read-only” or “human-approved” label is sufficient.



Effect | Control to inspect

Resource mutation | Specific directed-action authorization

Application testing | Targets, credentials, exclusions and permitted effects

Source change | Repository review and deployment controls

External publication | Destination and invocation-specific approval



**Guide:** [A-04](../guides/architecture.html#A-04)



## 5. Configuration, runs and artifacts have separate lifecycles

**Chapter:** Lifecycle and handoffs. **Schedule:** 08:00–10:00. **Slide budget:** 02:00.

Stopping future starts does not reverse completed effects.



Future work | Pause a schedule or disable an automation.

Current work | Cancel the invocation/task using its supported control.

Retained evidence | Manage versions, findings, files and artifacts according to their own semantics.



**Guide:** [A-05](../guides/architecture.html#A-05)



## 6. A handoff transfers evidence—not credentials or authority

**Chapter:** Lifecycle and handoffs. **Schedule:** 10:00–12:00. **Slide budget:** 02:00.

The receiving team obtains its own access and makes its own authorization decision.



Origin | Platform, configuration and execution IDs

Subject | Service, revision and UTC observation window

Request | Owner, question and permitted effect

Acceptance | Required evidence and unresolved questions



**Guide:** [A-06](../guides/architecture.html#A-06)



## 7. Keep implementation unknowns visible

**Chapter:** Evidence boundaries. **Schedule:** 12:00–14:00. **Slide budget:** 02:00.

An attractive diagram is not evidence of undocumented internals.



Documented | Resource relationships, selected controls, retention and execution behavior.

Not established | Shared vector database, retrieval-ranking algorithm, cross-agent runtime or model-training pipeline.



**Guide:** [A-07](../guides/architecture.html#A-07)



## 8. Tabletop: three observations, three evidence obligations

**Chapter:** Prepared-result tabletop. **Schedule:** 14:00–18:00. **Slide budget:** 04:00.

Synthetic comparison; no shared runtime or live execution assumed.



0–1 min | Identify the required inputs | Latency evidence, authorization identity and cost basis

1–3 min | Check consistency | Same intended revision, target and comparable windows

3–4 min | Assign unresolved questions | Do not invent a single shared root cause



**Guide:** [A-U01](../guides/architecture.html#A-U01)



## 9. Accept documents on operating usefulness

**Chapter:** Acceptance criteria. **Schedule:** 18:00–20:00. **Slide budget:** 02:00.

Link and layout checks are necessary but do not prove technical completeness.



Model | Resources and scope are clear before a scenario begins.

Procedure | Inputs, choices, confirmation and failure paths are described.

Evidence | Claims have sources; examples and live outcomes are not conflated.



**Guide:** [A-07](../guides/architecture.html#A-07)
