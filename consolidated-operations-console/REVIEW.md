# Consolidation model and diagram review

**Review date:** 5 November 2026. **Reviewed package:** first consolidation at [`db142c8`](https://github.com/lyrel-dev/frontier-agents/commit/db142c84bcfd691d5c71071681731cac81a52c7b). **Source-analysis baseline:** `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`. **Current contract:** revision 2.

The user's review identified a governing model defect: all entities must be versioned, and version records do not warrant separate entities. It also rejected the diagram format and layout. This review addresses those defects across schemas, references, operations, examples, source mappings and diagrams.

The earlier review's claim that no material contradiction remained was too broad. Schema-valid examples and diagram entity counts did not test whether the chosen entity boundaries and versioning mechanism met the intended design. Revision 2 adds those explicit acceptance criteria. Personal Context was disabled; the current user instruction and repository evidence supply the recorded basis.

## Findings in the first consolidation

P1 denotes a structural/history contradiction that can change the meaning of retained state. P2 denotes a narrower consistency or presentation defect. Correction below describes the delivered contract; implementation proof remains a later gate.

| ID | Priority | Observed defect | Correction and review evidence |
| --- | --- | --- | --- |
| V01 | P1 | Only seven of 37 entities had a top-level version. Collection and Run used projectionVersion, while many changing entities had no equivalent. | All 36 current entities require version, createdAt and updatedAt. The schema identifies logical identity, exact record identity and write authority. The validator checks the common contract for every entity. |
| V02 | P1 | SourceRevision and ProjectionRevision identified renditions; Scenario and ScenarioRevision split one concept into a root and a version-only entity. | Source and Projection have stable IDs with ordinary entity versions. Scenario owns draft, publication and archive states. There are no revision-only domain classes. Changed and reverted source content demonstrates stable identity with advancing versions. |
| V03 | P1 | Evidence and entity references used IDs alone. Collapsing revision entities without changing references would make history follow current state. | EntityRef/EvidenceRef require kind, ID and version. EntityIdentity is reserved for deliberate live navigation. Exact retrieval rejects a missing/unavailable version rather than falling back to the current head. |
| V04 | P1 | x-mutable=false labeled Collection, ReadAttempt, Command, Run and StepRun despite their state transitions. It conflated user write access with lifecycle change. | Write authority and sealing rules replace the mutable flag. Authorized publishers append versions; client editability is a separate operation contract. Settled/published content is never reopened. |
| V05 | P1 | Dependency governance and Recommendation enrichment maintained separate nested version counters, alongside local and projection counters elsewhere. | Owned values inherit their entity version. expectedVersion addresses Dependency or Recommendation. Narrow field authority remains explicit; a newer provider representation may correctly conflict with a stale local edit. |
| V06 | P1 | Snapshot copied ReadAttempt entities while those records also existed as canonical roots, creating competing historical representations. | Snapshot.members pins canonical entity versions, including failed/empty ReadAttempts and complete retained evidence closure. Owned capture values remain inside Snapshot; independently authoritative entities are referenced. |
| V07 | P1 | Run and StepRun could resolve current child state through parent identity/attempt number when reconstructing a historical result. | Each Run version pins its StepRun versions through steps. StepRun.selectedAttempt pins one exact StepAttempt version. attemptNo identifies a retry attempt and does not substitute for version. |
| V08 | P2 | Asset embedded an array of AssetVersion values, creating another special history mechanism beside the main entity model. | Each Asset version captures nativeVersion, source and files. Native version remains a provider fact, while application history uses Asset's common version contract. |
| V09 | P2 | Recommendation enrichment duplicated WorkItem assignment and workState, allowing competing operator workflows. Recommendation identity also depended on each observation occurrence. | WorkItem owns assignment/state. Recommendation enrichment keeps estimates/notes under Recommendation.version. A captured suggestion uses Finding + exact Source version + group/ordinal when a native key is absent; repeated observations cannot multiply it. |
| V10 | P2 | Mermaid/Graphviz artifacts and a tall all-edge layout did not satisfy the requested authoring format or provide an acceptable reading layout. Entity coverage was used as a proxy for diagram usability. | The editable source is an eight-page Draw.io atlas. The overview includes all entities with a selected connector set; focused pages cover relationships using boundary references. Native rendered exports, page-level visual review and structural coverage are separate evidence. |

The rejected representation choices are visible in the original [model](https://github.com/lyrel-dev/frontier-agents/blob/db142c84bcfd691d5c71071681731cac81a52c7b/consolidated-operations-console/MODEL.md), [schema](https://github.com/lyrel-dev/frontier-agents/blob/db142c84bcfd691d5c71071681731cac81a52c7b/consolidated-operations-console/model/schema.json), [protocol](https://github.com/lyrel-dev/frontier-agents/blob/db142c84bcfd691d5c71071681731cac81a52c7b/consolidated-operations-console/api/PROTOCOL.md) and [diagram sources](https://github.com/lyrel-dev/frontier-agents/tree/db142c84bcfd691d5c71071681731cac81a52c7b/consolidated-operations-console/diagrams). They remain in Git history for comparison; they are not current contracts.

## Corrected design boundaries

### Identity and history

The common metadata belongs to every entity, including Observation, Source, Projection and Snapshot. A fact can stay at version 1. A changing record appends a version under its owning authority. No public update operation is implied by the existence of versions.

Source logical identity excludes content digest. A repeated read observes the current unchanged Source version; changed content advances the version; A→B→A does not reuse an earlier version number. Provider versions, profile versions and attempt numbers remain separate meanings.

Exact references include version. Ordinary parent IDs establish ownership but cannot load current content into a historical result. Snapshot closes over exact retained inputs. Run's child selection is similarly pinned, so a historical verdict cannot drift when a current attempt changes.

### Ownership and operation contracts

Local writes compare the owning entity's version and update only declared fields. Provider commands retain their native authority/effect boundary. Trusted collector or runtime writes can publish observed/lifecycle state without granting clients arbitrary state setters.

WorkItem owns operator workflow; Recommendation enrichment and Dependency governance are owned local values. The universal version serializes the owning representation. The design deliberately accepts conservative stale-version conflicts instead of inventing another overlay version mechanism.

Scenario publication creates a PUBLISHED version of the same entity. New authoring creates a later DRAFT. Run pins an exact PUBLISHED version and separately checks current admission policy: an ARCHIVED current head blocks a new run, while a current DRAFT does not mutate an earlier publication. Replay of a previously admitted intent remains governed by idempotency ordering.

### Source meaning preserved

The common history mechanism does not collapse domain distinctions. PUBLIC Health visibility does not imply account impact; Finding remains service-scoped; Investigation/Execution membership remains observed; native FIS actions remain owned values; local completion cannot establish provider recovery. Source, receipt and derivation remain distinct substantive concepts.

The crosswalk preserves source names and provider profiles while changing current target representations. Earlier SourceRevision, ScenarioRevision and AssetVersion names occur only as source aliases, migration descriptions or review evidence.

## Earlier findings retained under the new model

The first review addressed useful narrower issues. Their semantics remain, with the common version/reference contract replacing the earlier representation choices.

| Earlier ID | Preserved requirement in revision 2 |
| --- | --- |
| R01 | ReadAttempt pins exact requestSource/responseSource and settles the same attempt identity. A lost response is not an empty success. |
| R02 | Snapshot pins a closed retained closure and capture interval, including ReadAttempt versions. Capture time does not replace source time. |
| R03 | EvidenceLocator distinguishes passages/fields within an exact Source version. |
| R04 | Local work completion, verification, assignment and estimates have narrow commands; WorkItem now owns all operator assignment/state. |
| R05 | Approval requires singleUse only for approval, with rejection fields constrained; decision and resume remain separate effects. |
| R06 | Pagination traversalId is distinct from a domain Snapshot. Version preconditions have typed conflict errors. |
| R07 | Scenario creation yields a DRAFT version. Publication is a distinct command that creates a later PUBLISHED version. |
| R08 | Declared request-capture profiles and payloadStorage distinguish native JSON null from artifact-held bytes. |
| R09 | Historical reads, replay, lists and artifacts recheck current authorization; a snapshot does not freeze entitlement. |

## Verification required for closure

### Independent integration findings

The following defects were found while exercising the corrected contracts and were closed before final validation.

| Finding | Correction and regression evidence |
| --- | --- |
| Adding a later version could reopen a settled ReadAttempt, StepAttempt or Run. | Sealing is checked across each entity history. The three sealed-record cases reject the reopened representation. |
| A Projection or captured Recommendation could gain a second ID for the same logical object. | Stable logical-key and uniqueness checks complement the common record key. Duplicate captures are rejected; repeated Finding observations of the same Source remain valid. |
| Run admission references or Collection query definitions could change between lifecycle versions. | Identity-defining fields are immutable across the history. New query definitions require another Collection identity; a Run keeps its admitted Scenario and input Snapshot. |
| A reference could point to a version published after the referring representation, and an admission snapshot could close over later terminal Run facts. | Publication-time and capture-cutoff checks reject future versions. RUN_INPUT captures the admitted workload and configuration, not its own future execution state. |
| Recommendation selection still compared Observation occurrence IDs. | Current Finding detail is compared by exact Source version, preserving the captured Recommendation across repeated receipts. The positive repeated-observation case verifies this. |
| A historical lifecycle projection selected the current ComponentDeployment during validation. | The validator resolves the exact subject from Projection.subjectRefs. A positive case adds a later deployment version while retaining the original projection. |
| API examples chose unrelated first parent records, understated list completeness, reopened a resolved WorkItem and initialized an unexecuted Run verdict inconsistently. | Examples follow actual parent scope, select exact versions, include bounded list continuation, use a note-only WorkItem edit and start with NOT_EVALUATED. Composed StartRun output passes model semantics. |

### Final gates

[VALIDATION.md](VALIDATION.md) records executed checks and counts. Review requires both positive and adversarial evidence for these invariants:

- All entity schemas and records have the common metadata; versions are unique and ordered within stable identities.
- Same-content repeat observation, changed content and content reversion preserve the correct Source identity/version behavior.
- Pinned references resolve exact records; absent versions, cross-scope links and current-head fallback are rejected.
- A later entity change cannot change an older Snapshot, Run, selected child or policy context.
- Scenario draft/publication/archive selection follows the explicit admission rule.
- Removed revision classes, nested history arrays and overlay/projection version counters do not remain in current contracts.
- API requests/responses, source-profile mappings, generated reference and Draw.io class/relationship coverage agree with the schema.
- Draw.io renders are visually inspected at reading scale for clipping, overlap, label ambiguity and routing, independently of XML validity and entity counts.

The examples are synthetic. These checks establish design consistency and selected invariants; they do not establish a running service, authorization implementation, persistence durability, provider effects or scheduler behavior.

## Implementation gates

Production delivery still requires atomic version publication/current-head selection, authorized historical access, retention integrity, lossless source adapters, durable replay, provider-specific reconciliation and workflow race/fencing checks. [CONSOLIDATION_PLAN.md](CONSOLIDATION_PLAN.md) and [api/PROTOCOL.md](api/PROTOCOL.md) define those gates. Prior prototype tests remain evidence about their own packages.
