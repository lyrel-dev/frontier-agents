# Model and API design principles

The consolidation should preserve the repository's strongest design decisions while reducing repeated infrastructure concepts. A smaller model is useful only if it still tells the truth about identity, ownership, missing evidence and the effects of an operation.

**Provenance:** these principles are recovered from `main` at `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`, inspected on **5 November 2026**. Personal Context was disabled, so earlier chats could not be retrieved. This document does not claim unobserved user preferences. The sources below record earlier decisions and corrections; the current request supplies the new consolidation objective and AWS RPC style requirement. The [inventory](INVENTORY.md) identifies the complete source boundary.

## Recorded model conventions

### Identify the concept before offering operations

Every concept needs an explicit kind and owner: provider resource, owned configuration member, execution record, retained evidence, local workflow or derived view. A source shape does not automatically become an entity with its own CRUD lifecycle. A logical class diagram describes relationships and selected attributes; it does not claim to expose AWS's internal physical schema. [E] [F]

Native behavior, application behavior and synthetic examples need separate labels. For example, the DevOps investigation view is an application aggregate over a native Task of type `INVESTIGATION`; a proposed `GetInvestigation` facade must not be described as a native AWS operation. A Health acknowledgement is local workflow because Health does not expose that mutation. [D] [DR] [H]

| Convention | Consequence for consolidation | Repository evidence |
| --- | --- | --- |
| **Give an entity independent identity only when its lifecycle requires it.** | Keep simple values within their owner. A query, alarm reference, assertion or report configuration does not need an independent CRUD resource merely because it appears in a UI. Clearly list owned values and external references alongside identity-bearing entities. | [F], especially “Model decisions kept deliberately small”; [FM] |
| **Keep product namespace and full scope in identity.** | Preserve partition, account, Region, service/provider space, parent and native ID wherever the source contract requires them. Friendly names, array positions and unqualified IDs are not stable joins. Encode composite keys unambiguously rather than concatenating opaque components with an unsafe delimiter. | [D] Q04; [RP] “Identities, references and field presence”; [H] |
| **Qualify relationships and cardinalities.** | Define same-run, same-context, same-service and same-snapshot foreign-key constraints. Retain explicit unresolved references. A missing cached object is not proof that the domain relation is absent. | [FR] R01; [RR] corrections; [DR] R05/R08 |
| **Consolidate common meaning, preserve domain meaning.** | Reuse identity, provenance, collection, retention and local workflow contracts. Keep provider state vocabularies, result selection, ownership and control limits in their modules. Similar names alone do not establish equivalent entities. | [E] “Outcomes and implementation relationships”; all four reports |

### Separate source facts, observations and projections

A logical object, a distinct payload revision, a collection observation and a derived projection revision answer different questions. The same source payload can be observed repeatedly without becoming a new logical object or a different source revision. An empty response or failed read is still relevant to collection coverage even when it yields no resource payload. A current projection must reference the exact source revisions used to compute it. [D] Q01/Q03/Q15; [DR]

| Convention | Consequence for consolidation | Repository evidence |
| --- | --- | --- |
| **Unknown remains unknown.** | Preserve absent fields, explicit null, known empty collections, known zero, unknown provider values, inaccessible evidence, stale observations and unconfigured features as distinct conditions. Open provider enums retain their raw value. Read normalization must not manufacture a safe state. | [E]; [F] A02/A03; [H]; [RP] |
| **A refresh does not rewrite source time.** | Keep source creation/update/occurrence/measurement time, receipt time, successful observation time, local edit time and projection computation time distinct. Recomputing a view cannot make old source evidence fresh; collecting an event cannot freshen its entities. | [DR] R06; [F] A01/A07; [H]; [RP] |
| **Coverage names its exact scope.** | Retain the requested query/scope/window, pagination status, per-item failures, detail hydration and known gaps. A complete list traversal is not a complete external history, resolved resource selection or atomic multi-API snapshot. | [D] Q08/Q15; [F] D02; [RR] |
| **Absence needs sufficient evidence.** | An empty page, timeout or silence cannot establish a negative assertion. Require a closed scope with adequate collection coverage. A restricted existential witness may prove presence from a valid matching record; it does not prove universal completeness. | [F] W05–W07; [FM] |
| **Source evidence is inspectable.** | Return the exact source revision, policy context, result phase, representation and field-presence metadata behind the selected value. Retained detail cannot silently make a newer summary complete. | [D] Q01/Q07; [R]; [RP] “Evidence behind a status” |
| **History pins meaning as well as bytes.** | Freeze the input/context, definition or policy, operation dependencies, parser/normalizer/evaluator versions, evidence references and accepted cutoff that produced a historical result. Later evidence or changed meaning creates a new result. | [F] D01/W01; [D] Q05; [RR] policy-context corrections |
| **Hashes have a bounded meaning.** | Declare which bytes or canonical representation are hashed. A digest detects content disagreement; it does not authenticate an AWS response or make browser storage tamper-proof. Historical access still obeys current authorization and retention rules. | [D] “Model decisions strengthened by the review”; [DR] F05/F06 |

### Preserve independent states and counting units

The existing reviews repeatedly found that one convenient status can conceal several different facts. The common model should expose these dimensions explicitly and allow them to disagree. [F] W04; [H]; [R]

| Dimension | What it establishes | What it cannot establish by itself |
| --- | --- | --- |
| Provider resource state | What a source reported for a scoped object at its source time | Current observation freshness, local work completion or recovery |
| Collection coverage | What the collector observed within a named query and time scope | Universal absence, exact atomic provider state or healthy workloads |
| Execution state/outcome | Whether execution is queued, active or technically settled | Whether acceptance criteria passed |
| Assessment verdict | Evaluation of declared criteria against pinned evidence and rules | Successful cleanup, stopped remote effects or workload recovery outside those criteria |
| Finalization/effect state | What is known about cleanup and outstanding effects | Satisfaction of business or resilience objectives |
| Artifact availability | Whether a particular report/content can be retrieved | Execution success or completeness of the underlying evidence |
| Operational health/posture | A qualified observation or derivation within its evidence and policy context | Exact present health after expiry, or end-to-end journey compliance from membership alone |
| Local operator disposition | Assignment, acknowledgement, suppression, completion or a claimed repair | A provider state transition or independently verified remediation |

Local completion must not clear an AWS Health pending impact. A finding marked resolved creates a need for verification; it must not manufacture a successful assessment or healthy service. A completed experiment may have a failed acceptance criterion; a passed assessment may coexist with incomplete cleanup. [H] [R] [F]

Counts need a named population, scoped deduplication rule and qualified denominator. Events, communication deliveries, account contexts, entity impacts, resources, services, findings and required criteria have different units. Public Health visibility does not add an affected account. Shared services and findings count once in an aggregate. Required workflow criteria are frozen at admission so runtime skips cannot disappear from the pass denominator. An empty denominator is not automatic 100 percent coverage. [H] [R] [F] W03; [D] Q03

## Recorded API conventions

### Use explicit contracts at every boundary

The Resilience package provides an existing AWS-style application facade: root `POST`, `application/x-amz-json-1.1`, `X-Amz-Target`, PascalCase operation names and lowerCamelCase JSON. It distinguishes native-backed adapters, composed reads, local commands and trusted ingestion. Those classifications explain an operation's source and effect; reusing a native name does not imply byte-for-byte native payloads. [RP] [RR]

The FIS workflow proposal uses REST bindings and RFC 3339 timestamps. It shares many command semantics with the Resilience facade, but it is not evidence of a prior universal RPC preference. Adopting one AWS RPC style and one timestamp convention in the consolidated API is a **new decision made under the current user instruction**. The consolidation must preserve the stronger semantics when normalizing the transport. [FA] [RP]

| Convention | Consequence for the consolidated API | Repository evidence |
| --- | --- | --- |
| **Use narrow operation-specific command DTOs.** | Accept only the writable fields of the named operation. Do not accept a read model wholesale or provide arbitrary state setters. Define omission, null, empty values and array replacement explicitly. | [RP]; [FA] §§ 1/6 |
| **Read tolerance differs from write validation.** | Reject unsupported writable fields and invalid input unions before mutation. Preserve unfamiliar provider output values and partial representations with diagnostics instead of rejecting all reads or inventing defaults. | [RP] |
| **Version the owner being edited.** | A configuration edit token belongs to the configuration owner. Telemetry, source observations and projection recomputation must not consume that edit revision. Local enrichment may have its own version. Immutable evidence and published revisions have no update operation. | [RP] “Mutation lifecycle”; [FA] § 3 |
| **Local concurrency is not provider atomicity.** | Explain what an expectedVersion comparison protects and what it cannot protect against out-of-band AWS changes. Use durable command/reconciliation state around provider calls; do not promise distributed compare-and-swap. | [RP] |
| **Resolve exact replay before mutable checks.** | Scope client-token deduplication to authenticated identity, operation and semantic payload, including conditional fields. Reauthorize the caller, then return the original receipt for an exact replay before applying a now-stale edit check. Changed payloads conflict; matching in-flight work has an explicit response. | [FA] § 3; [RP] |
| **State idempotency retention and uncertainty.** | Document replay lifetime, expiration and recovery. HTTP replay protection alone does not guarantee exactly-once external effects. A lost provider response is a state to reconcile, not permission to infer success or dispatch a second command. | [FA] §§ 3/4; [FM] |
| **Admission and completion are separate.** | Starting work returns a durable admitted identity and an inspectable lifecycle. Accepting cancellation records monotonic intent and fences new dispatch; it does not prove remote work has stopped. | [FA] §§ 2/4; [RP] |
| **Finalization covers uncertain side effects.** | Retain origin intents even when a handle was never returned. After cancellation, reconciliation must not create new work. Unresolved effects remain visible and retain the required protective scope hold. | [F] W08–W10; [FM] |
| **Pagination has its own contract.** | Use opaque tokens tied to authenticated scope, parent, operation, filters, order and a retained projection snapshot. Define page bounds, token expiry and restart behavior. Native pagination tokens are not application stream cursors. | [FA] § 5; [RP]; [D] |
| **Typed errors guide recovery.** | Provide stable types/codes, field paths, request correlation and operation-aware retry guidance. Do not make clients parse human messages. Retrying the same intent preserves its token; changing intent requires a new one. | [FA] § 6; [RE]; [D] Q09 |
| **Guard historical integrity when deleting.** | Reject deletion that would orphan active work or required references. Retain historical evidence/audit and an appropriate tombstone, or use archive when destructive deletion has no requirement. Do not cascade-delete history through a friendly-name owner. | [RP]; [FA] § 1 |
| **Keep scope and credentials server-controlled.** | Authorize connection references at admission and dispatch; do not accept arbitrary credentials, provider URLs, caller-selected roles or claimed successful outcomes. Reading evidence and executing work can require distinct permissions. | [FA] §§ 2/6; [RP] |

Compatibility includes meaning, not just JSON shape. Changing identity scope, units, state/verdict semantics, required inputs, pagination or replay guarantees is a breaking change. Additive read fields and unfamiliar provider values need tolerant consumers; request contracts remain deliberate and closed. [FA] § 6; [RP]

## Domain boundaries the common model must retain

| Source domain | Distinction that must survive consolidation | Source |
| --- | --- | --- |
| DevOps investigations | Task/Execution/Journal identity; observed task-to-execution association; phase-specific completion and exact summary reference; absent notification versus explicit no-summary versus pending hydration; arbitrary journal JSON; graph relationship meaning and scoped endpoints; asset/version/attachment/consumption distinctions; decision, resume, action observation and recovery. | [DR], [D] |
| FIS experiments | Catalog Action versus template member versus ActionExecution; run configuration capture versus later selected resource membership; experiment-level control boundaries; independent report availability; scope lever and alarm evidence; no fictional individual action retry/stop API. | [FR], [F] |
| General assessment workflow | Six identity-bearing concepts with owned step definitions, locks, criteria and effect references; pinned immutable dependencies; technical outcome versus verdict versus finalization; admission-frozen requirements; bounded evidence and non-creating reconciliation. | [FM], [FA], [F] |
| Health | Event/context/impact routing for PUBLIC, ACCOUNT and ORG_SUMMARY; logical communication page versus delivery identity; impact identity versus matched resource identity; catalogue facts versus observed deployments and evidence-based applicability; operator workflow separate from native Health state. | [H], [HR] |
| Resilience Hub | v2 contract; optional policy components and captured applicable targets; account ownership versus policy inheritance; no invented native assessment-owned finding set; recommendation values versus local enrichment; topology endpoints scoped to a capture; discovery versus health; attention rollups versus end-to-end journey compliance. | [RR], [R], [RP] |

## What is new in this consolidation

The current request establishes the new encasing application, a modular yet consolidated first-step data model, a class diagram covering all entities and an AWS RPC style operation surface. The source packages do not prescribe a final shared namespace, common entity count, module registry, retention schedule, database, runtime framework or deployment topology.

The new specification should therefore explain its choices rather than attribute them to earlier user approval. Each source concept needs a traceable outcome: shared entity, typed module extension, owned value, external reference, derived view or explicitly deferred capability. Preserve source identities and old terminology in the crosswalk. A small core is a design goal; a reduced entity count alone is not evidence that the full source meaning was retained. [E] [F]

The immediate implementation boundary is the **data model and API contract**. UI composition, durable scheduling, live provider collectors, authentication enforcement and production adapters can be added in subsequent steps. Contract checks can establish structural consistency and selected semantic invariants; they cannot establish those future runtime guarantees. Each earlier quality review makes this distinction and records failures that nominal fixture tests missed. [D] [F] [R]

## Source register

All references are pinned to the same source commit as the inventory. The precise follow-up commits are [`1b5ae1b`](https://github.com/lyrel-dev/frontier-agents/commit/1b5ae1bd11fc61a2701d74ea89ccce2721889ef0) for FIS, [`6b867f8`](https://github.com/lyrel-dev/frontier-agents/commit/6b867f8e80191f75eabd88c876d40c9ec0f30080) for Resilience Hub and [`d926a81`](https://github.com/lyrel-dev/frontier-agents/commit/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3) for DevOps. Health's main-branch review comes from [`0156b78`](https://github.com/lyrel-dev/frontier-agents/commit/0156b78758a2f35047d985b1a9fc645f30491525).

| Reference | Committed source |
| --- | --- |
| E | [Repository editorial standard][E] |
| D | [DevOps adversarial quality review][D] |
| DR | [DevOps initial review and source interpretation][DR] |
| F | [FIS quality review, including generalized workflow corrections][F] |
| FR | [FIS provider model review][FR] |
| FM | [Assessment workflow model][FM] |
| FA | [Assessment workflow API contract][FA] |
| H | [Health model review][H] |
| HR | [Health model and API report][HR] |
| R | [Resilience Hub adversarial quality review][R] |
| RR | [Resilience Hub model and RPC review][RR] |
| RP | [Resilience Workspace RPC protocol][RP] |
| RE | [Resilience Workspace error contract][RE] |

[E]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/EDITORIAL_STANDARD.md
[D]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/QUALITY_REVIEW.md
[DR]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/REVIEW.md
[F]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/QUALITY_REVIEW.md
[FR]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/REVIEW.md
[FM]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md
[FA]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/api.md
[H]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/REVIEW.md
[HR]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md
[R]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/quality-review.md
[RR]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/review.md
[RP]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/api/protocol.md
[RE]: https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/api/errors.md
