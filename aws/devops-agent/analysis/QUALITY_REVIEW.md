---
title: AWS DevOps Agent — adversarial quality review
id: aws-devops-analysis-quality-review
kind: obsidian-note
service: aws-devops-agent
type: adversarial-review
created: '2026-11-05'
updated: '2026-11-05'
reviewed_base_commit: 302128e5628acb4d832c20db79da2ab878c95e48
status: reviewed-prototype
tags:
  - aws/devops-agent
  - investigation
  - quality-review
  - api-contract
related:
  - report.md
  - REVIEW.md
  - VALIDATION.md
---

# Adversarial quality review

## Assessment

The first package was a useful presentation prototype, but its verification was too narrow for several of its stated invariants. Its fixed scenario passed while plausible duplicate observations, cross-scope identities, mixed result phases and damaged saved state exposed incorrect behavior. The second review treats those counterexamples as contract failures and adds regression checks for them.

The review uses the user's explicit requirements: complete and accurately bounded API analysis, defensible entity relationships, readable Obsidian diagrams, an operator view that remains truthful while collection is incomplete, and reproducible historical results. Earlier conversations outside the visible context could not be retrieved because Personal Context was disabled; this document does not claim additional remembered preferences.

The review covers every maintained document and deliverable in this service's `analysis` package: reports and annexes, model and fixture, interface, generated page, diagram sources and SVGs, build and checking tools, and validation evidence. The wider repository's earlier conceptual guides have their own source cutoff and approved entity register. This review reconciles the investigation package's vocabulary with that product terminology; it does not silently refresh every older guide or change its frozen register.

## Questions used to challenge the design

| Review question | Required evidence |
| --- | --- |
| Where does this fact come from? | Native operation/shape, documented content profile, application rule or fixture-only profile identified explicitly |
| Does the same identifier mean the same entity in another space? | Scoped keys, unambiguous tuple encoding and collision tests |
| What changes when the same response arrives twice? | Stable logical counts, preserved observations and distinct revision handling |
| Can a later failure or mitigation overwrite an investigation result? | Phase-scoped completion selection and retained prior result evidence |
| Does the source inspector explain the value on the screen? | Exact source revision selected from the same view publication |
| What does “complete” actually establish? | Named query/scope, as-of time, known gaps and separate artifact availability |
| Can history still open when a live refresh fails? | Authorized retained payload independent of technical refresh success; comparison availability and access policy separate |
| What does this API actually implement? | Separate official AWS transport, local model functions and proposed backend routes |
| Can another developer reproduce the review? | Pinned models, executable schema comparisons, stale-bundle detection and behavioral tests |
| Can an operator use the controls and read the diagrams? | Focus behavior, meaningful contrast, bounded target-renderer checks and browser inspection |

## Findings register

Severity **P1** means an incorrect investigation, result, provenance or retained-history behavior that blocks the prototype quality bar. **P2** means misleading interpretation, accessibility, contract completeness or reproducibility that also needs correction before presenting the reviewed package as complete. These are review priorities for this prototype, not an AWS service-risk classification.

| ID | Priority | Finding in the reviewed base | Incorporated correction |
| --- | --- | --- | --- |
| Q01 | P1 | Current task inspector selected the first retained Task source; a completed header could open the original in-progress version. | Publish and consume the exact current Task source reference. |
| Q02 | P1 | Summary candidates mixed investigation and mitigation records, and an unrelated later failure event could displace a completed result. | Select within a named result phase; only matching completion events carry completion selection. |
| Q03 | P1 | Repeated memberships and journal observations inflated entity counts; summary selection could retain the first observed revision. | Separate logical identity, retained revision and observation; deduplicate current collections deterministically. |
| Q04 | P1 | Bare task IDs and several derived/snapshot filters could cross Agent Space boundaries. Unescaped delimiter joins could collide. | Use full scoped keys throughout lookup, portfolio, projections and captures; encode opaque components. |
| Q05 | P1 | Historical view construction depended on building a current live view first; historical export also included changing live-comparison metadata. | Render a selected retained capture independently and preserve its export bytes; expose an unavailable comparison without bypassing access or retention policy. |
| Q06 | P2 | Shallow saved-state checks allowed malformed snapshot objects and duplicate snapshot identifiers. | Validate restored captures and counter consistency, reject invalid state explicitly and preserve recoverable saved data. |
| Q07 | P2 | Candidate-result panel displayed an unrelated finding instead of the selected summary candidate. | Render the selected candidate body and its own source; preserve unsupported JSON content as raw data. |
| Q08 | P2 | “Evidence complete” and “Complete history” overstated bounded query observations. | Use bounded collection wording and retain the query/known-gap scope. |
| Q09 | P2 | API inventory omitted endpoint prefixes, success codes and a modeled error matrix; error guidance omitted material 400/402/413 cases. | Expand transport/error coverage and define operation-aware handling. |
| Q10 | P2 | Schema-comparison claims could not be reproduced with the committed tools. | Commit a pinned-model audit and compact evidence with explicit comparison coverage. |
| Q11 | P2 | Package checks could pass with a stale generated application or drifted Mermaid copies in annexes. | Compare generated bytes and every published diagram copy against canonical inputs. |
| Q12 | P2 | Rerenders could remove keyboard focus, and several secondary text colors lacked sufficient normal-text contrast. | Preserve meaningful focus, isolate the open mobile drawer and darken relevant text. |
| Q13 | P2 | Pele rendering was the only executable Mermaid compatibility check. | Add a pinned Mermaid syntax check and distinguish that result from testing an installed Obsidian version. |
| Q14 | P2 | Asset export wording obscured the JSON `content.zipFile` byte path; modeled string-length limits could be mistaken for accepted UTF-8 upload capacity. | Correct the byte path and distinguish modeled length, UTF-8 bytes, encoded-request and asset-profile limits; verify effective acceptance before advertising capacity. |
| Q15 | P2 | The logical model conflated payload revisions with successful, empty and failed collection attempts. | Add D07 and explicit CollectionPass, ReadAttempt, SourceObservation and bounded CoverageClaim contracts. |
| Q16 | P2 | Storage-write failure was hidden on narrow screens while captures still appeared retained. | Show a visible session-only/recovery state and preserve export before reload. |
| Q17 | P2 | U03 depicted only terminal capture although the application permits manual active/partial captures. | Include manual capture and name the bounded query-set reconciliation decision. |
| Q18 | P2 | Inherited object properties could be mistaken for retained source IDs. | Restrict source lookup to own entries and test reserved property names. |

The corrections above passed the final local gates: **42 behavioral tests**, the repeatable native API and fixture audits, all **10** sources through the independent Mermaid syntax gate, all **20** published diagram copies, and exact generated-page parity. The focused browser review confirmed the changed provenance, historical, mobile and persistence behavior. [VALIDATION.md](VALIDATION.md) records the executed checks and separates them from earlier observations. Q01–Q18 are addressed within the stated prototype/design scope; the production evidence gates below remain open.

## API boundaries and maturity

| Surface | What is delivered | What the evidence does not establish |
| --- | --- | --- |
| Official AWS API | Operation inventory and selected detailed schemas, pinned model provenance, transport/error analysis and source comparison tools | Complete semantic validation of every one of the 560 shapes, actual account authorization, service behavior or SDK runtime tests |
| Local `DemoModel` API | Executable fixture read model, explicit state/lookup contracts, snapshots and exports, tested with adversarial fixtures | A network API, a production collector, a generic parser for all AWS journal content, or a secured multi-user store |
| Proposed application HTTP routes | Design examples in the UI annex, with application-owned identities, coverage and update concepts | Implemented endpoints, a finalized OpenAPI contract, deployed auth, cursor retention, or stream recovery guarantees |
| EventBridge | Reviewed lifecycle/summary contract and synthetic notification cases | Live delivery, ordering, duplication, retry or retention measurements |
| Native chat and A2A | Reviewed adapter boundaries and future capture requirements | Implemented chat/approval/A2A integrations or production feature parity |

The prototype's lack of a backend is an explicit scope boundary. It would be a quality failure to present the proposed route names as an implemented API or to reuse native pagination tokens as application stream cursors. Before production, the application API must specify authorization, URI-safe identifiers, section error states, stable pagination against a projection revision, update ordering, cursor expiry and resynchronization, retention and export access. The [UI contract](annexes/Investigation_UI_Contract.md) retains the integration capture plan.

## Model decisions strengthened by the review

A source revision records a distinct payload. A source observation records seeing that payload during a particular read. An unsuccessful or empty read still matters to coverage. [D07](diagrams/D07-collection-observations.svg) makes that distinction explicit and complements D03's projection provenance.

Current results and historical results must use exact scoped identities and source references. A current inspector must not choose the first item in a retained-revision collection. An authorized historical capture must not be rebuilt from current sources; current access and retention policy still apply. Known-query coverage, result readiness, artifact availability and operational recovery remain independent statements.

Hashes detect accidental content disagreement under the declared serialization scheme. They do not authenticate an AWS response or make browser-local storage tamper-proof. “Immutable snapshot” is an application retention invariant; production enforcement requires authorized, durable backend storage and retention controls. The browser prototype demonstrates retained content and comparisons, not that security boundary.

## Remaining evidence gates

The corrected package can support presentation and information-architecture review. Production readiness still requires authorized captures demonstrating native pagination under updates, real journal profiles, permissions and revocation, ambiguous mutation recovery, account/Region scope, event delivery, phase-specific results, retention and independently retrievable snapshots. The tested UI fallback covers an already selected capture when current-view and queue assembly fail; automatic routing from an unavailable live view at startup is not implemented. Effective accepted asset size must be checked against the model, UTF-8/encoded-request limits and the applicable asset profile; these are separate constraint layers, not a proven AWS contradiction.

The exact installed Obsidian version is not known. Mermaid parsing and portable SVG inspection can establish the tested rendering paths; they do not certify every Obsidian release or theme. Open the notes in the deployment's target Obsidian version before claiming that specific environment is supported.
