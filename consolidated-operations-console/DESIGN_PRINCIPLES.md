# Model and API design principles

## Authority and provenance

The user's correction on **5 November 2026** governs this revision: **all entities are versioned; an entity is not created merely to represent a version; every diagram uses Draw.io and a reviewed layout**. These requirements supersede the incompatible choices in the first consolidation.

Personal Context was disabled when earlier interactions were requested. This document therefore uses the visible instruction and repository evidence. It does not attribute unseen preferences or approval to the user. The earlier model/API conventions below are supported by the source analyses, reviews and [editorial standard][E] at `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`. New choices made during consolidation are identified as such.

| Governing rule | Concrete consequence |
| --- | --- |
| Every entity is versioned | Every schema requires stable identity, `version`, `createdAt` and `updatedAt`, regardless of whether its owner is a user command, collector, derivation or runtime. |
| Versioning is a common entity property | Source and Projection keep their identities across versions. Scenario owns draft/publication/archive versions. There are no SourceRevision, ProjectionRevision or ScenarioRevision entities. |
| History references exact versions | EntityRef includes kind, ID and version. ID-only EntityIdentity is reserved for explicit live navigation. Historical reads never fall back to latest. |
| Owned values inherit their owner's version | Governance, enrichment, steps, criteria and files do not acquire competing version counters or CRUD identities merely because they appear in a screen. |
| Draw.io is the diagram format | The editable atlas and its rendered pages use deliberate page composition, readable routing, consistent class notation and linked source sections. Entity coverage and visual quality are separate checks. |

## Identity, ownership and simplicity

An entity names a domain concept with identity and lifecycle: a service, an observation, a command, a run. A version names one representation of that same concept. An attribute collection, serialization artifact or display panel does not automatically create another entity. The original reviews already required the concept and owner to be identified before offering operations. [E] [F] [FM]

The first consolidation violated this distinction by making version-only classes and mixing local edit tokens, projection counters and unversioned records. Revision 2 corrects the model rather than hiding those differences behind renamed IDs. All stored versions are immutable; the owning authority can publish a successor under the same identity. An immutable fact may remain at version 1. Versioning does not imply public mutability.

| Principle | Application to the model | Evidence |
| --- | --- | --- |
| Full identity scope is explicit | Keep provider namespace, owning account/Region, parent scope and native key. A Connection is an access path, not native identity. Friendly names and unsafe concatenation are not joins. | [D] Q04; [RP]; [H] |
| Relationship claims are qualified | Same-workspace, same-service, same-context and same-run rules remain explicit. An unresolved object is not proof that a relationship is absent. | [FR] R01; [RR]; [DR] |
| Common meaning is consolidated | Reuse versions, references, collection, evidence and command intent. Preserve domain-specific state, attribution and control boundaries. | [E]; [F]; [H]; [R] |
| One owner writes one value | Service owns catalogue membership. WorkItem owns operator assignment and work state. Native provider configuration is changed only through the corresponding command boundary. | Current correction; [RP]; [HR] |
| Open native content has a bounded location | Arbitrary JSON stays in retained native/source documents or explicit schema/content contracts. Ordinary application writes use closed typed inputs. | [D]; [RP] |

The current request favors a simple, extensible model. Entity count alone does not establish simplicity. A consistent identity/version/reference mechanism removes special cases while allowing typed module ownership.

## Evidence and time

Source, Observation and Projection answer different questions: what document was retained, when it was seen, and what a rule concluded. Their distinction remains useful; each now has the same entity-version mechanism. Repeated reads can observe the same Source version. A changed source payload or derivation publishes a successor without rewriting history. Failed and empty reads remain ReadAttempt facts. [D] Q01/Q03/Q15; [DR]

| Principle | Consequence | Evidence |
| --- | --- | --- |
| Unknown stays unknown | Preserve absence, null, empty collections, zero, unavailable evidence, stale observations and unconfigured features. Preserve unfamiliar provider values rather than defaulting to success. | [E]; [F] A02/A03; [H]; [RP] |
| Entity time and source time differ | `createdAt`/`updatedAt` describe application identity/publication. Source creation/update/measurement time, observation time and projection computation remain separate. | Current versioning rule; [DR] R06; [H]; [RP] |
| Coverage identifies its scope | Record query/window, page completion, failures, hydration and unresolved identity. A complete local traversal is not complete provider history or an atomic multi-API snapshot. | [D] Q08/Q15; [F] D02; [RR] |
| Absence needs adequate evidence | Silence, an empty page or a timeout cannot establish universal absence. A valid presence witness does not establish full coverage. | [F] W05–W07; [FM] |
| Conclusions expose their inputs | Pin the exact Source, Observation, Projection and subject versions, plus policy/result phase and field presence. Retained detail cannot make a new summary complete. | [D] Q01/Q07; [R]; [RP] |
| History pins meaning | Retain exact inputs, definitions, rule/evaluator/adapter contracts, accepted cutoff and coverage. Later interpretation creates a later version or a new evaluation. | [F] D01/W01; [D] Q05; [RR] |
| Digests have a stated meaning | Declare raw bytes or canonical representation. Hash equality does not establish native identity, observation occurrence, authenticity or current access. | [D]; [DR] F05/F06 |

Snapshot retains a deliberately captured, closed manifest of exact entity versions. It is not a replacement for ordinary entity history. Failed and empty ReadAttempts are members of that manifest rather than duplicated entity copies.

## Independent state and counting

Provider resource state, collection coverage, technical execution, acceptance verdict, cleanup/effect state, artifact availability and operator disposition answer different questions. The model permits these dimensions to disagree. A completed local review cannot clear a Health impact; a resolved finding cannot manufacture successful posture; a successful experiment may fail acceptance; a passed criterion may coexist with uncertain cleanup. [H] [R] [F]

Counts identify their population and deduplication rule. Event, delivery, account context, impact, service, finding and criterion are different units. Public notification delivery does not add an affected account. Shared services count once in a rollup. Required workflow criteria are fixed at admission so skipping cannot improve the denominator. An empty denominator is not automatic 100 percent. [H] [R] [F] W03; [D] Q03

## API design

The existing Resilience facade supplies repository evidence for root POST, an AWS JSON media type, X-Amz-Target, PascalCase operations and lowerCamelCase JSON. The FIS workflow used REST bindings. A unified RPC facade follows the current request; it is not presented as a universal earlier preference. [RP] [FA]

| Principle | Consequence for revision 2 | Evidence |
| --- | --- | --- |
| Version the entity being changed | Use its common version for expectedVersion. Owned governance/enrichment inherits that version. This intentionally replaces the earlier package's independent overlay/projection counters. | Current user correction; earlier alternatives recorded in [RP] and [FA] |
| Reads select a representation explicitly | A typed getter can request a version. Current lists retain entity/version pairs for the traversal. Exact historical references reject a missing or unavailable version. | Current correction; history requirements in [D] and [FA] |
| Commands have narrow inputs | A read record is not an update DTO. Specify clearing, omission, null, collection replacement and permitted state transitions for the named operation. | [RP]; [FA] §§ 1/6 |
| Read tolerance differs from write validation | Preserve unfamiliar provider output and diagnostics. Reject unsupported writable members and invalid unions before admitting a mutation. | [RP] |
| Local concurrency is local | An entity version protects application admission/publication. A pinned source precondition is observed context, not a distributed AWS transaction. | [RP] |
| Exact replay precedes current-version checks | Reauthorize, compare the complete canonical intent and return the original receipt for exact replay. Different preconditions under the same token conflict. | [FA] § 3; [RP] |
| Admission and completion are separate | Accepted work has a durable identity and inspectable lifecycle. Accepted cancellation records intent/fencing, not proof of remote cessation. | [FA] §§ 2/4; [RP] |
| Uncertainty is retained | A lost response is a reconciliation state. Provider replay support is operation-specific. Cancellation cannot justify a creating retry merely to discover an effect. | [F] W08–W10; [FM]; [FA] |
| Pagination has its own boundary | Bind opaque tokens to identity/scope, operation, filters, order and retained entity/version selection. Define limits, expiration and restart behavior. | [FA] § 5; [RP]; [D] |
| Typed errors guide recovery | Supply stable exception/code, field paths, request correlation and retry guidance. Clients do not parse human message strings to decide whether an effect occurred. | [FA] § 6; [RE] |
| Retention preserves reference meaning | Do not cascade-delete history through a friendly-name owner or substitute current data for unavailable retained content. Apply current authorization to historical reads. | [RP]; [FA] § 1; [D] |
| Trusted context controls authority | Workspace, actor, credentials, source claims, derived outcomes and operation locks are supplied or verified by the relevant authority. | [FA] §§ 2/6; [RP] |

Changing entity identity, reference shape, version semantics, state meaning, units, replay or pagination is a breaking contract change. Revision 2 therefore uses `ConsolidatedOperationsConsole_20261105V2`. Additive compatible read fields and future provider values need tolerant consumers; write inputs remain explicit.

## Domain distinctions retained

| Domain | Boundary that survives the common version model | Source |
| --- | --- | --- |
| Investigation | Native Task/Execution/Journal scope; observed membership; phase-specific results and exact content selection; asset native-version meaning; approval, resume, action observation and recovery. | [DR], [D] |
| FIS | Catalogue action, template member and action execution remain different provider concepts; selected resources do not prove fault application; only documented experiment-level control is exposed. | [FR], [F] |
| Workflow | Locked published Scenario version; admitted inputs and criteria; distinct Run/attempt identities; cancellation fencing, finalization and non-creating reconciliation. | [FM], [FA], [F]; current revision correction |
| Health | PUBLIC/ACCOUNT/ORG_SUMMARY context; page versus delivery identity; impact versus inventory matching; catalogue facts versus observed deployments; local work versus native state. | [H], [HR] |
| Resilience | Configured policy components and captured targets; assignment versus account ownership; service-scoped findings; captured recommendation versus local enrichment/work; topology and qualified rollups. | [RR], [R], [RP] |

The contract and diagram checks establish consistency of the delivered artifacts and selected invariants. Runtime behavior remains subject to the phased implementation gates. Source prototype tests are evidence about those prototypes, not proof of a consolidated production application.

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
