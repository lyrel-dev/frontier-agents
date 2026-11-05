---
id: fis-revised-current-review
title: Revised package review
type: review-record
service: aws-fis
status: reviewed-mock-package
version: "1.0"
created: "2026-11-05"
updated: "2026-11-05"
tags: [aws, fis, review, ui, assessment]
aliases: [FIS revised package review]
related: [README.md, VALIDATION.md, docs/README.md, docs/initial/report.md, docs/suggested/model.md]
---

# Revised package review

This review covers the preserved initial interface, the new suggested interface, the complete reviewed reports, all diagrams, and Obsidian YAML metadata. The package is ready for design review and synthetic exploration. The generalized execution model and API remain proposals; the UI does not implement their runtime guarantees.

Earlier findings remain available in the [baseline adversarial review](docs/review/quality-review.md). This note records the additional inconsistencies found and corrected while building the revised deliverables. [VALIDATION.md](VALIDATION.md) distinguishes automated checks, browser observations and implementation limits.

## Design boundaries

The initial interface continues to model native FIS experiments and named action executions. The suggested interface models Scenario, ScenarioRevision, Run, StepRun, StepAttempt and Evidence. FIS experiments remain provider executions associated with attempts; their native action children are not presented as individually controllable workflow steps.

The suggested UI keeps technical execution, required-criterion assessment and finalization distinct. Evidence collection and source coverage are inspectable. Unknown external disposition cannot be turned into a confirmed stop by a local cancellation or elapsed replay time. All controls and operational data remain explicitly synthetic. Pending checks appear as **Evaluating** in the interface while retaining the underlying verdict and finality in the snapshot.

## Findings corrected in this revision

| ID | Quality gap or challenge | Resolution and evidence |
| --- | --- | --- |
| R01 | Mock inputs and successful outputs did not conform to their pinned operation schemas. A detail view labelled as actual resolved input must not show an incompatible excerpt. | The fixture generator now resolves the published `with` definitions against admitted bindings, inputs and prior outputs. Typed connections and authenticated observation provenance are present. A maintained test validates all **87** recorded input/success-output DTOs. |
| R02 | Server-enriched CheckResult metadata had been placed inside closed adapter output schemas. | Adapter output and the owned CheckResult value are separate. Predicate identity, evidence references and evaluator/cutoff metadata remain inspectable without expanding a provider's output contract. |
| R03 | Admitted capabilities disagreed with the authoring declarations, and unavailable input changed a pinned predicate's identity. | Bound capabilities match the revision. Revision-to-Scenario identity, admission/input digests, scoped attempt references and predicate identity are checked. A blocked run retains the same 180-second/60-second requirements. |
| R04 | The late-notification trace marked a transition window closed before its endpoint. Adapter prose also implied waiting even after both positive witnesses were established. | The early window remains open/partial. **DOC01** explicitly permits settlement after both validated positive witnesses, preserving actual collection, coverage and closure. Absence still requires its applicable window/grace and adequate proof. The substantive clarification is recorded in [documentation provenance](docs/manifest.json). |
| R05 | Receipt timing lacked a stated clock bound, and normalized witnesses did not consistently link to original source identity. | All three receipt records have a synthetic ±250 ms clock bound and clock basis. All five positive witnesses link to the corresponding source record and occurrence time. The 48-second/75-second examples are outside the uncertainty margin around the 60-second deadline. |
| R06 | A finalization policy flag caused completed runs to show a protective hold after remote termination was already confirmed. | Header, summary and effect inspection now distinguish policy from the current unresolved-effect projection. Browser checks show no hold for the completed Orders and Payments runs; the ambiguous-start run retains its hold. |
| R07 | Unqualified graph badges made a failed criterion look like a failed operation. A dependency spanning a graph level passed behind an unrelated node. | Check badges explicitly identify criterion or precondition verdicts; execution remains independently named. Graph alignment keeps the capture-to-injection dependency clear of the baseline precondition. The Payments view shows successful execution and cleanup beside a failed criterion. |
| R08 | Provider namespace aliases appeared as duplicate freshness sources. Local control states could also be read as AWS-reported states. | Freshness reduces each supported provider authority to one row with its newest observation. Local readiness/unconfirmed state is labelled separately from provider state. The regression suite covers FIS and Logs aliases. |
| R09 | Rewinding before a saved cancellation still described the intervention as active. A local branch could otherwise be mistaken for continued provider observation. | The banner identifies history before the accepted intervention. Source data freezes at acceptance; only labelled local control records advance. Browser replay verified that advancing from 110 to 170 seconds preserved the last source timestamps and produced an indeterminate result with incomplete cleanup. |
| R10 | Windows, cutoffs, source timing and evidence association were too difficult to inspect. | Criterion and evidence dialogs expose the proof boundary, receiver receipt/ingestion time, exact receiver, source IDs and digests. Exact step filtering returned only the collecting step's record; text filtering produced a clear empty state. |
| R11 | Responsive rules hid source freshness, and button styling overrode the hidden state of the diagram's inapplicable JSON-copy control. | Freshness remains available below 1240 pixels. The hidden attribute is explicitly respected. A 390-pixel layout check verified the freshness dialog, diagram navigation, hidden copy control and absence of page-level horizontal overflow. |

These are corrections to the delivered design and demonstration. They do not establish that real collector completeness, permission enforcement, cancellation fencing or remote reconciliation has been implemented.

## Preservation and documentation

The initial model, fixtures, stylesheet and tests match reviewed commit `1b5ae1bd11fc61a2701d74ea89ccce2721889ef0` byte for byte. Only HTML/rendering navigation paths and the obsolete PDF link label are adapted. The [source manifest](initial/source-manifest.json) records original and packaged hashes; those original hashes were also compared directly with the committed baseline. Both interfaces are individually accessible, and the comparison shell keeps Initial before Suggested while retaining each view's state.

All **33 Markdown documents** have YAML properties, unique note IDs and local navigation. The eight diagrams have individual Obsidian notes plus canonical Mermaid and SVG assets. Embedded diagrams in the two model reports are checked against those sources. The complete examples have Markdown notes alongside canonical YAML and lock files. Historical validation statements are labelled as baseline records; they are not presented as newly executed checks.

The revised package preserves the complete native report's 14 sections and 53-source register, the full proposed model/API/adapter contracts, and the prior adversarial review. It does not replace the earlier analysis directory or introduce a second mutable PDF pipeline.

## Model and API decisions retained

The six core entities remain sufficient for these examples. Query languages, alarms, notification receipts and reports are typed operation/evidence content; they do not each require another independently writable aggregate. Step definitions, admission snapshots, operation locks and check results are owned values. Scoped identities and relationship cardinalities remain explicit in the [class diagrams](diagrams/suggested/README.md).

The API retains narrow commands and writable fields. Clients cannot edit derived statuses or retry an uncertain mutating attempt through a generic StepRun patch. Publication pins contracts; admission freezes requirements; cancellation is monotonic intent; finalization records unresolved effects independently of whether the orchestration record is finished. The [API](docs/suggested/api.md) documents concurrency, idempotency, pagination and typed errors. The UI exports a presentation DTO and does not claim HTTP conformance.

General assertion semantics preserve unknowns. A complete query returning zero is a known query result, but insufficient source coverage still makes the broader claim inconclusive. A matching positive witness may establish existence before the window closes. An empty or partial result cannot establish absence. The notification claim belongs to the explicitly bound probe receiver and does not imply production consumer processing.

## Remaining implementation boundaries

The required next implementation work is a durable scheduler/control store, authenticated API and connection boundary, bounded CEL compilation/evaluation, real digest-addressed operation implementations, source-specific collectors and provider reconciliation. Those components need crash/race/integration tests against real contracts. The retained static validator and synthetic reducer tests exercise decisions; they are not substitutes for those implementations.

The browser review covers desktop and a 390-pixel content viewport. It does not certify a particular mobile device, every browser, screen reader behavior or Obsidian plugin version. All source-backed AWS facts remain attributed in the [native report](docs/initial/report.md) and [source register](docs/initial/sources.md). No cloud account was connected and no live assessment was executed.
