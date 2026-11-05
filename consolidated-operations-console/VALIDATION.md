# Validation and evidence boundaries

This package is **contract revision 2 of the phase-one model and API specification**. Its checks establish structural consistency, source traceability, uniform entity versioning, exact historical selection and selected domain invariants in synthetic data. They do not establish production persistence, identity enforcement, actual cloud execution or service behavior.

## Reproduce the checks

Run from `consolidated-operations-console/` in a checkout containing the pinned source commit:

```sh
python -m pip install -r tools/requirements.txt
python tools/validate.py --json
python tools/render_model.py --check
python api/generate.py --check
```

The validator resolves the model and RPC schema IDs locally. It does not fetch the illustrative `.example` schema URLs. JSON numbers are parsed with Decimal so millisecond timestamp constraints are checked before comparison; duplicate JSON keys are rejected. The model and API regeneration checks compare existing bytes without first regenerating them.

The diagram check reads the committed Draw.io atlas and exports offline. Full regeneration uses the pinned official Draw.io engine and its dependencies as described in [diagrams/README.md](diagrams/README.md). Geometry is authored in [model.drawio](diagrams/model.drawio); schema synchronization preserves positions and waypoints. SVG exports come from Draw.io, and Inkscape produces the PNG previews. The maintained package has no Mermaid or Graphviz diagram pipeline.

## Executed results

**PASS**, checked on 5 November 2026 after the model and diagram corrections. The machine-readable result is [validation.json](validation.json).

| Check | Executed result |
| --- | --- |
| Source inventory | All 226 active source files match the pinned Git tree, blob hashes and byte sizes. |
| Uniform entity contract | Every one of the 36 entity schemas requires version, createdAt and updatedAt. No version-only entity or competing projection/overlay version counter remains. |
| Worked model history | 215 schema-valid representations of 171 logical example entities, including multiple versions of Source, Service, Scenario, Collection, ReadAttempt, Run, StepRun and StepAttempt. |
| Semantic cases | 79 cases pass their stated expectation: 17 valid cases accepted and 62 invalid cases rejected for the expected reason. |
| Source crosswalk | 174 mapping rows, 340 original source aliases and 65 profiles preserved; 182 independently extracted source concepts are accounted for. |
| RPC contracts | 108 operations, all 216 request/response payloads and three typed error payloads validate. |
| Historical API selection | All 36 entity getters support exact versions. Reviewed examples include older Service, Source and published Scenario versions despite newer heads. Parent-selected workflow lists use exact child references. |
| Admission example | The generated StartRun Command, Run, Snapshot and three StepRuns were composed with the canonical dataset: zero schema errors and zero semantic errors. |
| Operation migration | 161 predecessor mappings account for 44 Resilience facade operations, 16 workflow operations and all 101 first-consolidation operations. |
| Draw.io source coverage | Eight native editable pages cover all 36 entities and all 45 declared relationships, with actual class fields, edge endpoints and cardinalities checked against the schema. |
| Native diagram rendering | All eight pages pass Draw.io codec round trips. Rendered geometry reports no class overlap, connector intrusion, relationship-label intrusion or text overflow; deliberately invalid geometry is rejected by negative controls. |
| Visual inspection | All eight page previews were inspected. Connector labels, cardinalities, long field wrapping and the Scenario definition union were corrected during review. |
| Reproducibility and links | Model/reference/diagram and API generation checks pass; all checked relative Markdown links resolve. |

The schema, fixture, operation and diagram counts are independently inspectable in [model/schema.json](model/schema.json), [model/examples.json](model/examples.json), [api/operations.json](api/operations.json) and [diagrams/manifest.json](diagrams/manifest.json). The diagram manifest binds the schema, editable atlas, generated reference, native rendering report and exports by hash.

## Versioning and historical selection checks

The revised corpus tests the failure modes introduced by inconsistent entity versioning: missing or invalid version metadata, conflicting representations with the same identity/version, unstable creation time, backwards publication time, changing logical source identity, duplicate Projection or Recommendation identities, and exact references to missing or future versions.

Positive cases demonstrate that a Source returning from content A to B to A uses three versions of one entity; a later Service edit leaves an older capture intact; a later Scenario draft does not alter the published version used by a Run; and a later ComponentDeployment observation does not change an older lifecycle projection. Repeated Finding reads of the same exact Source version reuse the captured Recommendation identity and preserve its original provenance.

Workflow checks pin the Run's Scenario, input Snapshot and selected StepRun versions, plus each StepRun's known and selected StepAttempt versions. Admission bindings and Collection query definitions cannot change during their lifecycle. Settled ReadAttempt, StepAttempt and Run records cannot be reopened through an additional version. A snapshot rejects future execution state and closes over exact canonical references instead of copied ReadAttempt records.

The earlier domain cases remain: workspace/parent isolation, public versus organization Health impact, result phase selection, missing versus empty evidence, absence over partial/open coverage, frozen criterion denominators, workflow cycles, uncertain effects, policy capture consistency, incomplete finding detail, topology endpoint scope, target selection versus fault evidence, stale current status and empty denominators. Successful technical execution can coexist with failed acceptance, and completed local work cannot rewrite provider impact or finding evidence.

## What the examples establish

The worked data is synthetic. The API payloads are independent contract illustrations, not an executed transaction log. Version-sensitive examples state or select their relevant prior representation. A response admitting a command does not establish the later provider outcome.

Fixture digests use a deliberately restricted canonical JSON subset for source-content tests: ASCII keys/strings, safe integers, booleans, null, arrays and objects. Exact UTF-8 artifact strings are checked separately. The validator is not a general RFC 8785 implementation or a source authentication mechanism. Production importers must use a conforming canonicalizer or retained raw bytes under the declared digest profile.

The Draw.io exports use the pinned official engine in a DOM runtime with native font metrics. Native XML round trips, resolved geometry and visual previews are verified. These checks do not certify a particular installed desktop build, nor do diagram coverage checks prove domain semantics.

## Remaining implementation gates

| Area | Evidence still required |
| --- | --- |
| Version storage | Atomic next-version publication, compare-and-swap admission, immutable old records, consistent head selection, concurrent updates and retained-version integrity. |
| Authorization | Trusted Workspace/principal binding, complete evidence-closure authorization, scope revocation, current provider permissions and authorized historical export. |
| Commands and replay | Durable token reservation/results, independent field authority on shared entity versions, outbox/crash recovery, provider dispatch and uncertain-effect reconciliation. |
| Collection | Real native pagination, empty/failed/partial reads, source identity/profile conformance, ordering and duplicate-receipt handling, raw request/response retention. |
| Workflow | Trusted operation registry, expression/type conformance, admission races, retry eligibility, persisted dispatch identity, cancellation fencing and bounded finalization. |
| Retention | Historical references, payload availability, tombstones and exact-version retrieval after policy changes. Snapshot correction writing is deferred; current CaptureSnapshot creates a new logical capture. |
| UI | Actual console integration, accessibility, responsive behavior and exact evidence selection against the common backend. |

[REVIEW.md](REVIEW.md) records the model and presentation defects and their corrections. Earlier prototype test results remain evidence about those earlier packages.
