---
id: aws-fis-quality-review
title: Adversarial review of FIS analysis and assessment workflow proposal
status: reviewed
updated: "2026-11-05"
---

# Quality review

The original FIS entity boundaries remain useful. The package did not yet meet an implementation-quality bar: the UI had observation/provenance defects, historical assessments lacked a complete frozen input contract, artifact checks could conceal a stale PDF, and the generalized API/model left important runtime semantics open. This review corrected those defects and records which parts remain proposals.

The review covered the FIS Markdown/PDF/source register, all five provider diagrams, application code and fixtures, model tests, renderer/manifests, README/review/validation records, screenshots, and the generalized scenario/model/API answer. The generalized answer had not been committed previously; it is now maintained under [workflow/](workflow/README.md).

## Review basis and independence

The user requested a challenge informed by prior interactions. Earlier-history retrieval was disabled. The review therefore used the visible conversation and the repository's actual [editorial standard](../../../EDITORIAL_STANDARD.md), plus concrete conventions in the neighboring [API protocol](../../resilience-hub/analysis/api/protocol.md). It does not attribute unobserved preferences to the user.

Those recorded principles require scoped identity, explicit entity kinds/ownership, qualified cardinalities, unknown-preserving observations, a separation of configuration/execution/evidence/acceptance, narrow writable DTOs, and honest validation boundaries. Separate reviewers examined FIS fidelity/artifacts, application behavior, and the workflow/API semantics. An independent reviewer supplied 39 normative decision cases before the corresponding reference helpers were implemented.

Priorities below mean: **P1**, capable of misleading an operator or permitting inconsistent implementation; **P2**, model/build/maintainability defect that weakens correctness or reviewability. “Corrected” denotes changes in this package, not certification of a production system.

## 1. Corrected application findings

| ID | Priority | Finding and consequence | Correction and evidence |
| --- | --- | --- | --- |
| A01 | P1 | Simulated stop froze some data but continued advancing the original scenario's successful-fetch time. Old source evidence appeared fresh. | Pure `applyStopIntervention` starts from the captured observation and advances only labelled local simulation. Tests and browser replay at 700 seconds preserve a 470-second source age. |
| A02 | P1 | A configured unobserved report exported as not configured; interruption invented a new pending report. | Unknown/unobserved, absent configuration and known report states are separate. Original scenario artifacts are invalidated after intervention; no replacement is invented. |
| A03 | P1 | Missing telemetry coerced to zero, and lines joined across missing samples. | `metricSeries` accepts only finite numbers, sorts source times, retains unknown latest/peak values and breaks paths across missing samples or declared-period gaps. |
| A04 | P2 | EKS container choices were included in pod identity, overstating resource counts. | Pod identity uses cluster/namespace/pod name within one run; container choice remains membership data. It does not claim stable pod incarnation across runs. |
| A05 | P2 | Unidentified memberships were counted as identified resources. | Identified-resource count, unidentified-membership count, collection completeness and identity completeness are separate. |
| A06 | P2 | “Related evidence” was a free-text search and could include unrelated records mentioning the action. | Exact action association is an explicit, visible filter with its own clear control. |
| A07 | P2 | Active timeline bars extended past the last source observation while labelled observed. | Observed intervals end at the source observation; elapsed wall time is retained separately. Local simulation is explicitly labelled. |
| A08 | P2 | Scenario navigation reset cursors and could show an interrupted run as running in the sidebar. | Each run retains its cursor/intervention; selected and nonselected statuses use that projection. Browser navigation verified. |
| A09 | P2 | Fixture validation claims exceeded the checks, and invalid timestamps could pass through null comparison. | Required/string parameters, account/target membership, schedule identity and valid timestamps are now checked. Focused malformed-fixture tests reproduce the former gaps. |
| A10 | P2 | Dialog navigation lost useful focus; targetless wait actions implied unresolved scope. | Dependency navigation focuses the new heading; controls expose pressed state; targetless actions say no target is configured. |

The complete app suite has 27 tests. The browser recheck used the exact current HTML/app/model/fixture/style bytes in an isolated preview. The [validation record](VALIDATION.md) records the observations and the uncompleted narrow-layout recheck.

## 2. Corrected FIS model and artifact findings

| ID | Priority | Finding and consequence | Correction and evidence |
| --- | --- | --- | --- |
| D01 | P1 | A criterion revision alone did not freeze mutable metric/query bindings, units, normalizer/evaluator versions or accepted sample cutoff. A historical verdict could be reinterpreted. | `ResilienceAssessment.inputSnapshot` and `evidenceCutoffAt` pin the evaluated meaning. Late data or changed policy creates a new assessment. Diagram 5, report and PDF agree. |
| D02 | P2 | Resource-resolution completion and client pagination completion were too easily conflated. | The report records collection identity/scope, resolution-ended evidence, page traversal and observation interval. A successful empty page alone does not prove empty selection. |
| D03 | P2 | Dependency/child integrity and historical catalogue interpretation were implicit. | Same-run references, no cycles/self/duplicate edges, incomplete validation and captured catalogue provenance are explicit application invariants. |
| D04 | P1 | Diagram-only rendering dropped the PDF's build provenance and could conceal a stale PDF. | Manifest v2 preserves the original PDF build inputs and exposes stale state. Both modes validate before writes; `--check` never regenerates before checking. |
| D05 | P2 | PDF date/edition were hard-coded and source-register/renderer hashes were missing. | Front matter owns edition/date; provenance includes report, sources, renderer, diagram inputs and build environment. |
| D06 | P2 | Duplicate source URLs, unknown citations and duplicate embedded figures were not fully enforced despite validation wording. | Checks now reject each case; seven isolated renderer regression tests cover failure paths. |
| D07 | P2 | Forced page breaks produced sparse continuation pages and exposed an orphan heading/line during revision. | Pagination/grouping corrected. Edition 1.2 contains 24 pages, 14 sections, five diagrams and 53 official source references; every page was rendered for review. |

The second source review revisited 22 official AWS pages covering the central shapes and lifecycle/control boundaries. It found no additional incorrect field or lifecycle claim in the central FIS model. This was a targeted recheck, not a fresh exhaustive review of all 53 source pages. Existing source references remain in [sources.json](sources.json).

## 3. Corrected generalized model/API findings

| ID | Priority | Challenge | Revised decision |
| --- | --- | --- | --- |
| W01 | P1 | An immutable text revision can still change behavior if `@1` is resolved again for each run. | Resolve complete contracts at publication. Admission uses retained digests; alias rotation leaves old revisions unchanged. Missing/revoked artifacts reject execution rather than substitute code. |
| W02 | P1 | Dependencies mixed ordering, technical success and assertion success. | `needs` orders work; default requires technical success; settled diagnostics are explicit. Only declared preconditions gate mutating descendants. A false criterion does not silently block the next criterion. |
| W03 | P1 | Skipped checks could disappear from the pass denominator. | Freeze required criteria at admission. Runtime skips, errors and cancellation remain inconclusive requirements. Admission-only applicability is separate from runtime `if`. |
| W04 | P1 | A single success flag blurred false criteria, failed execution and cleanup failure. | Independent execution outcome, assessment verdict/finality and finalization/effect state. A successful assertion may establish failure; a passed assessment may coexist with incomplete cleanup. |
| W05 | P1 | Generic expressions over partial results were treated as proofs. | General assertions require complete, sufficiently covered evidence. Restricted existential witness assertions may pass from a valid matching record; absence needs a closed covered scope. |
| W06 | P1 | Missing alarm transitions became adapter timeouts, hiding the actual acceptance requirement. | Transition and receiver receipt are separate required criteria over typed bounded observations. Missing evidence and conclusive absence have different outcomes. |
| W07 | P1 | A probe notification could be presented as proof of production receiver delivery or business processing. | Bind the exact receiver and claim. Probe receipt proves only probe receipt; actual receiver/process claims need that receiver's evidence. |
| W08 | P1 | Cancellation lacked durable acceptance, replay/race semantics and a remote-state boundary. | Monotonic intent fences main dispatch. Exact replay returns its original receipt; terminal races are explicit. Local completion never proves remote cessation. |
| W09 | P1 | Retrying an uncertain Start after cancel could create new work. | Non-creating reconciliation only after cancellation; unresolved effects remain visible and retain the protective scope hold. |
| W10 | P1 | Cleanup guarded only by a returned handle missed lost-response starts and had ambiguous ordering. | Unconditional finalizers inspect StepRefs and original intents, including zero-attempt/no-effect cases. Explicit settled dependency orders stop before capture close. |
| W11 | P1 | `deploymentRef` described the subject without constraining adapter effects. | Trusted binding/scope policy must constrain account/Region/resources; later dynamic target resolution remains evidence. A preview does not freeze selection. |
| W12 | P2 | Multiple statuses/versions looked independently writable, and later reconciliation could mutate sealed attempts. | Durable facts and control intent are authoritative; one public Run projection version. Later observations reference an origin effect and update its projection without rewriting prior attempt facts. |
| W13 | P2 | The six-entity claim obscured scoped values and undeclared context. | Six retained identity-bearing concepts, with owned values and external references listed separately. All inputs, bindings, output references and graph phases are declared. |
| W14 | P2 | Writable fields, null/update behavior, idempotency conditions, pagination and compatibility were incomplete. | Explicit command DTOs and one HTTP binding; conditional headers participate in idempotency; stable scoped traversal and typed errors are specified. |

The second adversarial pass also challenged the new checks themselves. It caught a lock validator coupled to current aliases, contradictory no-effect cleanup output, an available observation without a value, an unavailable observation with a value, and witness input without a records collection. Those were corrected before delivery. The reference suite has 68 tests, including the independent 39 cases; it does not implement the runtime guarantees those cases describe.

## 4. Model decisions kept deliberately small

The core remains **Scenario, ScenarioRevision, Run, StepRun, StepAttempt and Evidence**. Step definitions, locks, check results, input snapshots, cancellation intent and external effect references are owned values. Operations, deployment inventory and connections belong to explicit external contracts.

There is no separate CRUD entity for each query language, alarm, message, assertion or report. FIS actions remain provider detail within a native experiment, not fictional individually controllable workflow steps. A flat main DAG and a bounded cleanup DAG are sufficient for the examples; jobs, stages, schedules, approvals, nesting and generalized retry controls are deferred until a concrete lifecycle requires them.

The class diagrams cover all six entities and the owned-value relationships. They use the same sources embedded in [model.md](workflow/model.md), with source/output hashes and portable SVG presentation values. The model's additional precision lives in invariants and operation contracts, rather than an expanding list of entities.

## 5. Remaining boundaries

| Area | Current status | Evidence needed before claiming production readiness |
| --- | --- | --- |
| General workflow execution | Proposal plus static checks/reference reducers | Durable scheduler, crash recovery, leases/fencing and integration tests for cancellation/uncertain dispatch. |
| API | Documented proposal; no server | Authenticated tenant boundary, persisted idempotency, conditional updates, pagination and actual transport conformance. |
| Expressions | Declared CEL environment; reference-scope checks only | Selected runtime, full type checking, deterministic/resource-bounded evaluation and compatibility tests. |
| Provider adapters | Typed synthetic catalogue; implementation hashes are synthetic labels | Implementations, provider-specific permission/scope checks, pagination, reconciliation and contract tests. |
| Negative assertions | Explicit completeness/coverage rules | Collector-specific coverage evidence; no generic timeout or empty result can supply this automatically. |
| Notification claims | Correct receiver/transition/time contract | Instrumented intended receiver, clock uncertainty, durable capture and tested delivery/processing correlation. |
| Browser | Desktop second-pass interactions verified; earlier responsive check retained historically | A new narrow-layout pass, broader browser/device/accessibility testing as required by product release. |
| PDF | Visually inspected 24-page report | Tagged/accessibility-certified output if that becomes a delivery requirement. |

Proposed retention periods, cursor expiry and scope-lock policies are product choices recorded for review. They are not AWS guarantees or inferred user decisions. No AWS account was connected, no fault was injected, and no production readiness claim follows from these tests.
