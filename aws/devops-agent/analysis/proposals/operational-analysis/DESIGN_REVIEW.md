---
title: Operational analysis model — adversarial design review
id: operational-analysis-design-review
type: design-review
created: '2026-11-05'
updated: '2026-11-05'
reviewed: '2026-11-05'
status: design-reviewed
test_execution: none
tags:
  - operational-analysis
  - domain-model
  - api-design
  - evidence
related:
  - README.md
  - API.md
  - AWS_EVIDENCE.md
  - ../../QUALITY_REVIEW.md
  - ../../../../../consolidated-operations-console/DESIGN_PRINCIPLES.md
---

# Adversarial design review

## Scope and disposition

This is a **conceptual design review and a future acceptance plan**, not a test report. It challenges the proposed seven-entity model before implementation: **Subject, Analysis, Assertion, QueryRun, Evidence, Assessment and Review**. No application API, collector, evaluator or live cloud behavior has been implemented or tested by this document. The cases below specify the counterexamples an implementation must handle and the evidence required to accept it.

The [model proposal and its class diagram](README.md) define the design under review. The earlier [investigation-package quality review](../../QUALITY_REVIEW.md) supplies concrete motivation for preserving scoped identity, exact provenance, bounded coverage and reproducible history. Its executed prototype checks do not establish that this new generalized design works.

The governing follow-up is the user's 5 November correction recorded in the [consolidated design principles](../../../../../consolidated-operations-console/DESIGN_PRINCIPLES.md): every entity has common identity/version/publication fields; a version is not a separate entity; exact references include kind, ID and version; and diagrams use reviewed Draw.io layouts. The unified RPC convention also governs this proposal. These are repository-backed instructions, not inferred preferences from inaccessible personal conversations.

The core remains small by treating QuerySpec, RunReceipt, AssertionResult, citations, scope, time windows and payload references as typed owned values. They inherit their owner's entity version rather than acquiring competing counters or CRUD identities. Adapter/evaluator contract versions identify the external interpretation code used; they are not another version of an owned value. Calling something a value object does not excuse an ambiguous contract.

### Bounded cross-check and clarifications

The completed conceptual pass compared the [model proposal](README.md), Draw.io entity diagram source, [proposed RPC API](API.md) and [AWS evidence examples](AWS_EVIDENCE.md) against the governing consolidation. Its scope was the seven-entity inventory, common version/reference rules, analysis-owned assertions/runs/assessments, workspace-owned evidence reuse, complete expected assertion-instance sets, exact version/receipt pins, temporal coverage and attributed operator reviews. It found no unresolved structural inconsistency within those checked boundaries. Rendered layout checks are documented separately in the [validation record](qa/VALIDATION.md).

The following ambiguities and follow-up requirements are addressed by the proposal:

| Finding | Incorporated design clarification |
| --- | --- |
| An explicitly empty logical population could be mistaken for operational readiness. | An assertion's logical semantics may permit an empty population, but the readiness policy still requires a nonempty applicable required/target domain. Empty or unresolved domains cannot produce readiness success. |
| Reassessing one criterion could appear to omit other required instances. | Remaining expected instances stay visible; omitted required inputs cannot make the whole Analysis pass. Deliberate narrowing needs an explicit definition version or named subset policy and a clearly narrower claim. |
| An evidence reference's input role could be confused with its stance toward a conclusion. | Input roles such as transitions or deliveries bind evaluator inputs. A result citation's supporting/refuting/context stance is separately named. |
| Definition-only revisions, result counters and unversioned append-only records would conflict with the governing common-version rule. | All seven entities expose `id`, `workspaceId`, `version`, `createdAt` and `updatedAt`. History uses `EntityRef {kind, id, version}` within the authorized workspace. A selected QueryRun version pins its owned receipts/result manifest; append-only facts may remain at version 1. No version-only entity or competing owned-value version is introduced. |
| The earlier transport and diagram choices did not incorporate the newly retrieved consolidation rules. | Use the uniform RPC operation envelope and Draw.io class diagram. Model coverage, source consistency, rendered layout and runtime behavior are separately bounded checks. |
| Requiring owned assertion references during initial Analysis creation would create a circular authoring dependency. | Create the Analysis with empty criterion bindings, create its owned Assertions, then publish an Analysis version binding their exact versions. An Assessment still requires at least one assertion instance. |
| An unspecified knowledge cutoff could allow a retained result to depend on inputs selected after evaluation admission. | The backend freezes the local publication cutoff at Assessment admission. Every selected exact reference must exist by that cutoff; the evaluator does not resolve inputs through latest-state reads. |

This reconciliation establishes conceptual consistency within the stated scope. It does not certify the API as a complete formal schema or establish adapter, evaluator, persistence, authorization or rendering behavior. The 16 acceptance cases below remain unexecuted.

## Design commitments being challenged

| Commitment | Consequence for acceptance |
| --- | --- |
| Every entity uses the same version mechanism. | Require `id`, `workspaceId`, `version`, `createdAt` and `updatedAt` for all seven entities. Stored versions are immutable; append-only facts may remain at version 1. Historical EntityRefs always include kind, ID and version within the authorized workspace. |
| Analysis versions freeze the question being asked. | Pin the selected Assertion versions, requiredness, applicability policy, target domain and time/phase bindings. Collector progress publishes QueryRun versions and does not change an unrelated Analysis definition. |
| A QueryRun executes a complete frozen QuerySpec. | Preserve the resolved request, adapter version, limits, authorization-context reference and native handles. A mutable recipe name is insufficient provenance. |
| Evidence records a captured observation or result. | Distinguish capture identity, payload identity and logical native event identity. A capture does not establish the truth of every statement within it. |
| Assessment is an immutable input-and-result record. | Pin exact Evidence versions and QueryRun versions, with their selected result manifests/run receipts and collection coverage. A read publication sequence does not replace an entity version. |
| AssertionResult is owned by an Assessment. | Key each result by exact Assertion version plus target binding and window/phase. Its local identity and stored content inherit the Assessment version. |
| General assertion verdicts remain explicit. | Use `supported`, `refuted`, `inconclusive` or `not_applicable`; preserve reasons such as `conflicting_evidence`. |
| Requirement rollup is optional and policy-driven. | General hypotheses do not automatically determine operational acceptability. Empty required or target sets cannot produce a passing rollup. |
| Review is an attributed decision about one assessment representation. | Target an exact Assessment EntityRef. Accepting a failed or inconclusive assessment can be correct. A review does not rewrite evidence or computed verdicts. |

## Acceptance cases

**Execution status for every case: not executed.** Each row is a proposed acceptance criterion, including the counterexample and the observable result expected from a future implementation.

| ID | Counterexample to construct | Required behavior and acceptance evidence |
| --- | --- | --- |
| OA-R01 | The same native resource is read through two roles; another account or Region contains an identically named resource. | The two roles do not create two Subjects for the same owning identity. The other owning scope cannot join to it by a bare name or ID. Inspect structured owning identity and separate access context; exercise opaque-ID delimiter collisions. |
| OA-R02 | A service's tag selector resolves to three resources at collection time and five before assessment or review. | Preserve the exact Subject/Analysis versions, selector, resolution time and resolved bindings actually used. Do not silently reassess the newer five-resource set. An incomplete resolution remains a scope limitation, and a later resolution belongs to a new basis. |
| OA-R03 | An assertion threshold, requirement role or applicability rule changes after an assessment is reviewed; some record types are incorrectly left unversioned. | All seven schemas retain the common entity fields and immutable stored versions. Publish a successor on the entity that owns the change: a criterion role belongs to its Analysis definition. The old assessment pins its earlier Analysis and Assertion versions. Evidence, Assessment and Review still expose version 1 when append-only. A rule-only change is identified separately from new evidence. |
| OA-R04 | One assertion is applied to two deployments and to baseline and recovery windows. | Retain four distinct assertion instances/results, with the expected instance set in the assessment basis. No result overwrites another under the assertion ID alone. Missing target or phase results remain visible and affect only the rollup required by the pinned policy. |
| OA-R05 | Two reads return the same event; a later read returns changed content under the same native event ID. | Preserve distinct captures, reuse identical content-addressed payloads where permitted, and avoid inflating the count of distinct source events. Preserve changed source renditions and their captures. If no stable native identity exists, expose that limitation rather than claiming certain deduplication. |
| OA-R06 | An asynchronous query produces partial polls, final pages and an overlapping rerun; a partial assessment precedes final retrieval. | Pin the selected QueryRun version and its coherent result manifest, page/receipt chain and coverage. Later progress publishes another version of that QueryRun; a rerun is a distinct execution identity. Do not union overlapping results or improve the earlier assessment retroactively. Owned receipts do not acquire a second version counter. |
| OA-R07 | A query returns no rows after access denial, truncation, missing instrumentation, an unclosed observation window or retention loss. | Preserve the distinct collection outcomes. Absence is supported only when the assertion's source, scope, window, sampling and lateness requirements are adequate. A successful query or zero-row result alone cannot establish that an operational event never occurred. |
| OA-R08 | One valid receipt proves existence, or one valid counterexample refutes a universal claim, while other collection remains incomplete. | Evaluate adequacy for the predicate being tested. A useful witness is not discarded merely because unrelated queries failed. A known required violation is not erased by another inconclusive result. The exact witness and its target/window binding remain cited. |
| OA-R09 | Evidence concerning yesterday's incident arrives after its assessment and review. | Create a new assessment for the same valid interval and a later knowledge cutoff. Keep the earlier assessment and review unchanged. Distinguish newly captured unchanged data, new logical events, changed payloads and changed rules when reporting subsequent activity. |
| OA-R10 | Two sources disagree about the same target and valid interval, with no pinned rule establishing precedence. | Return `inconclusive` with `conflicting_evidence` and retain both citations. Do not use arrival order or latest capture as an undeclared authority rule. Different valid times may instead represent a normal state transition and must be aligned before declaring a conflict. |
| OA-R11 | A deterministic rule, an operator judgment and a reasoned agent interpretation all discuss the same causal proposition. | Preserve the method, actor/evaluator version, input selection and explanation for each result. Label a manual or reasoned assessment explicitly. Source attribution or correlation does not silently become verified causality; a generated confidence number is not a substitute for a declared evidential criterion. |
| OA-R12 | There are no required assertions, no resolved targets, or every required assertion becomes inapplicable; a general hypothesis is refuted. | An empty required/target set cannot yield a passing operational rollup. Applicability follows the pinned rule and domain; it is not a way to bypass required checks. A hypothesis verdict affects operational acceptability only when an explicit requirement policy says it should. |
| OA-R13 | An alarm is configured for SNS, one subscriber accepts a notification, another has no receipt, and the first consumer later fails processing. | Keep configuration, alarm transition/action, message publication, each recipient's delivery and processing as separate propositions. Bind evidence to the intended topic, message, recipient and deadline. Delivery to one recipient does not establish delivery to all, and transport acceptance does not establish processing success. Missing correlation or instrumentation produces bounded uncertainty. |
| OA-R14 | An operator accepts an assessment with a failed requirement; another reviewer disputes it; a later assessment has different evidence. | Acceptance targets the exact Assessment EntityRef and does not change its verdict. Reviews remain versioned even when append-only at version 1. Preserve both decisions and rationales. Any aggregate review status follows explicit policy; there is no implicit latest-review-wins rule. An earlier review cannot validate a different assessment/version automatically. |
| OA-R15 | Imported or manually supplied evidence claims to be directly collected, is attached to another analysis, or loses access after the first review. | Preserve supplied provenance as a claim and separately record actual ingestion origin and authenticated actor. Reuse preserves original capture identity/time and producer; it is not a fresh read. Check authorization for reuse, retrieval and export independently of content hashes. Retention loss or revoked access must not fabricate retained content. |
| OA-R16 | A query start response is lost, cancellation races completion, an adapter reaches a budget limit, or a client attempts to supply a computed verdict. | Use the uniform RPC contract and the changed entity's common `expectedVersion` where required; reauthorize exact replay before current-version checks. Preserve ambiguous dispatch and reconcile native handles before any duplicate start. Keep execution, result availability and verdict separate. Computed outcomes remain authority-owned; manual judgments use an attributed input path. |

## Rejected alternatives

| Alternative | Why it is rejected for this core |
| --- | --- |
| Use an AWS DevOps Agent Task as the generalized Analysis identity and lifecycle. | The application must combine sources and operate without that service. A native task is an external reference or evidence source, with its own state semantics. |
| Add independently managed QueryDefinition and Evaluation entities immediately. | Frozen QuerySpec and owned AssertionResult values satisfy this scope. A reusable recipe catalogue or independently addressable evaluation workflow can justify later promotion, but neither should be added only to normalize every noun. |
| Create version-only entities, leave immutable facts unversioned or add competing receipt/edit version counters. | Version is a common property of the existing entity. Owned values inherit it; immutable facts can remain at version 1. Publication sequences are read-consistency boundaries, not substitutes for entity versions. |
| Represent everything as a generic node/edge or key/value entity. | That weakens ownership, input typing, required relationships, temporal rules and API invariants. Graphs remain useful derived views over explicit entities and citations. |
| Treat a retained payload as an unquestionable fact. | Sources can disagree, be incomplete, contain attributed claims or be imported. The model preserves observations and provenance; the assessment states what they support. |
| Select the latest query, evidence, definition or review implicitly. | Reassessment becomes irreproducible, results from different QueryRun versions can mix and history can change. Current-view conveniences must resolve to explicit versioned inputs before assessment. |
| Persist a second authoritative Timeline or mutable Finding store. | It creates another place where operational facts and timestamps can diverge. Timelines, graphs and finding presentations should derive from retained evidence and versioned assessment rules. |
| Use a single `done` or `healthy` status across all objects. | Work management, query execution, evidence adequacy, assertion verdict, requirement rollup and human acceptance answer different questions. |
| Let a reviewer overwrite an automated result or silently promote an agent statement. | The assessment loses its reproducible meaning and attribution. Add a new attributed judgment or new assessment while preserving the original result. |
| Run arbitrary uploaded assertion code in the query/evaluator process. | Extensibility requires a versioned typed evaluator/adapter contract with explicit capabilities. A generic code-execution mechanism is a separate execution and trust boundary. |

## Remaining design and implementation gates

The proposal must still choose concrete schemas and policies before implementation acceptance:

- **Predicate and adapter contracts:** define the initial operators, input/output schemas, units, normalization profiles, supported query variants and version compatibility. Unknown source payloads remain retainable even when they cannot be evaluated richly.
- **Temporal and coverage policy:** specify window boundaries, source-event versus observation clocks, lateness allowance, retention assumptions, target-resolution behavior and how each predicate uses partial evidence. No single global completeness flag can settle all of these.
- **Persistence and publication:** implement immutable entity versions, atomic assessment manifests, durable owned run receipts and stable view pagination. Keep the view's publication sequence distinct from entity version. The core class diagram does not prescribe a physical database layout or prove transaction behavior.
- **Authorization and retention:** define workspace ownership, cross-analysis evidence reuse, principal-sensitive cache boundaries, review authority, export authorization and content-retention behavior. Content-addressed storage deduplication does not grant access to matching bytes.
- **Query execution:** implement provider-specific start/poll/page/cancel/reconcile behavior, bounded retries and cost/deadline controls. A provider's successful query status does not prove complete historical instrumentation.
- **Human and reasoned assessment:** define attribution and the permitted write path for manually evaluated results, including what a reviewer accepts and how disagreements are represented. Deterministic, manual and reasoned methods must remain distinguishable.
- **AWS acceptance:** verify representative account captures for the selected operations, correlation fields, delivery endpoints and configured telemetry. This document does not establish CloudWatch, CloudTrail or SNS delivery behavior.

Connections, credential resolution, connector registration, recipe catalogues and mutating operational commands belong to integration or execution contexts outside these seven domain entities. Their absence from the entity diagram is a scope decision; their contracts remain required wherever an implementation depends on them.

## Acceptance evidence to retain

A future implementation review should retain the fixture inputs, exact API requests, receipt/evidence manifests, produced assessments and expected outcomes for OA-R01–OA-R16. Tests should demonstrate the counterexample, not merely mirror a constructor or schema. Provider integration checks should record the actual scope, permissions, configuration, observation interval and missing instrumentation.

The conceptual design review is complete against the governing common-version, RPC and Draw.io rules. No acceptance case in this document is marked passed: implementation and integration acceptance remain a separate, unexecuted set of gates.
