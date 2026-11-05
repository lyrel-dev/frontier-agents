---
id: aws-fis-revised-docs-review-baseline-validation
title: FIS and workflow baseline validation
type: historical-validation
service: aws-fis
status: historical-evidence
version: '1.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- historical-validation
aliases:
- FIS and workflow baseline validation
related:
- baseline-review.md
- quality-review.md
- ../../VALIDATION.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/VALIDATION.md
---

# Application validation

> [!info] Historical baseline review
> This note preserves the reviewed baseline at commit [1b5ae1b](https://github.com/lyrel-dev/frontier-agents/commit/1b5ae1bd11fc61a2701d74ea89ccce2721889ef0). Its test counts, screenshots and PDF statements describe that baseline. The current revised interfaces and their checks are recorded in [the revision review](../../REVIEW.md) and [revision validation](../../VALIDATION.md). Historical command examples assume the original analysis directory unless stated otherwise.

Initial validation and adversarial re-review on 5 November 2026. This is a static mock-data showcase; no AWS account was connected and no service-side fault action or stop request was made. The generalized workflow addition is a contract proposal, not an implemented runner or HTTP server.

## Automated model checks

`node --test app/tests/model.test.cjs` passes **27 tests**. The suite covers action identity, same-run dependency edges, target binding integrity, overlapping target memberships, unknown/partial collections, preview semantics, observation-time filtering, execution versus assessment versus report outcomes, structured errors, stale polls, replay immutability, and exports that exclude future simulator data. `node --check app/app.js` and `node --check app/model.js` pass.

The second review adds regression coverage for pure interruption projection and frozen source freshness, unknown replacement reports, configured-but-unobserved report summaries, pod/container identity, unidentified membership counts, observed timeline cutoffs, missing/out-of-order metrics and malformed fixtures. Null telemetry never becomes a measured zero. The simulated stop is now exercised through the same pure model used by the UI.

The fixture integrity validator also checks references, resource types, account coverage, target-slot bindings, parameter strings, and dependency ordering. These checks exercise the model; they do not prove live AWS behavior.

## Initial browser checks

The original application was exercised in Chromium through a local static preview. This table preserves the initial delivery's observations; the second-pass checks and limits follow it.

| Check | Observed result |
| --- | --- |
| Five opening scenarios | Running, completed, stopped, failed, and target-preview views rendered with distinct execution, step, workload, and report outcomes. |
| Completion versus assessment | Orders showed completed execution and three completed actions while the workload criterion failed. Its report was independently ready. |
| Preview | Fulfillment showed three skipped steps, zero completed actions, no assessed workload result, and no generated report. |
| Action details | Selecting `isolatePayments` showed its map-key identity, catalog ID, parameters, predecessor/successor relationships, times, and three selected memberships. |
| Dependencies | The checkout baseline branches into two distinct disruption actions and joins at recovery observation. |
| Resource scope | Checkout showed four unique resources and five memberships. The shared subnet retained both selectors and both bound actions. |
| Resource filters | Selecting `inventoryAz` produced two identities; searching its shared subnet reduced the result to one. |
| Related evidence | The action drilldown opened filtered evidence, retaining separate occurrence and observation times. |
| Replay reset | At offset zero, future actions, observed evidence, and final verdicts were absent. Target collection showed incomplete observation rather than a confirmed zero total. |
| Replay controls | 15× playback advanced the displayed clock; pause stopped playback. Manual advance and reset updated the snapshot. |
| Simulated stop | Checkout entered `stopping`, then `stopped` after 30 replay seconds. Pending work was cancelled; assessment became inconclusive. Mock control records used the corrected replay timestamps. |
| Error provenance | Inventory displayed `AuthorizationFailure`, its account and named action location. Its separate report displayed the reporting-role write failure and `AccessDenied`. |
| Report artifact inspection | The completed Orders report exposed a fictional S3 ARN and configuration, with an explicit synthetic-reference explanation. |
| JSON download | An Inventory export at offset zero parsed successfully and contained no future `AuthorizationFailure`, report `AccessDenied`, `_mock`, or scheduled action data. |
| Keyboard behavior | Main-tab arrow navigation moved selection and focus together. Focus remained on a resource selector after rerendering. |
| Desktop layout | No document-level horizontal overflow at a 1,348 CSS-pixel viewport. |
| Narrow layout | A 390 × 844 CSS-pixel iframe exercised responsive CSS. The document stayed within the viewport and wide action tables scrolled inside their own container. This was a responsive layout check, not physical-device emulation. |

## Second-pass browser checks

The corrected app was exercised in Chromium using an isolated static preview to prevent unrelated documentation edits from reloading the test page. Hashes of the tested `index.html`, application, model, fixtures and stylesheet matched the final repository files. The preview daemon was stopped after testing.

| Check | Observed result |
| --- | --- |
| Stop at 230 seconds | Execution and active actions entered `stopping`; the pending action became cancelled; replacement report became unobserved. |
| Advance 30 seconds | Stopped at 09:04:20 UTC, with 1 completed, 2 stopped and 1 cancelled action. Assessment stayed inconclusive. |
| Source freshness | At 260 seconds: `FIS observed 30s ago · local simulation`. No source poll was invented. |
| Late replay at 700 seconds | Source age 470 seconds; 10 evidence records, 317.2 ms last measured value, 4 resources and 5 memberships. No later original-scenario report/verdict/observations appeared. |
| Scenario navigation | Checkout remained Stopped while Orders was selected; returning restored its 700-second cursor and 470-second source age. |
| Exact action evidence | `isolatePayments` had one associated observed record. Clearing the visible action filter restored all 10 and focused search. |
| Dependency dialog | Following a predecessor updated the dialog and focused its new heading. |
| Distinct outcomes | Orders simultaneously showed completed execution, three completed actions, failed criterion and ready report. |
| Reset | Cleared the intervention and returned to offset zero, incomplete scope and zero observed evidence. |
| Desktop overflow | Document clientWidth and scrollWidth both 1,348 CSS pixels. |

The current overview is [preview.jpg](assets/initial-overview.jpg); the interrupted late-replay state is [qa/stop-intervention.jpg](assets/stop-intervention.jpg).

**The narrow-layout check was not completed in the second pass.** The preview did not serve the added HTTP iframe harness; a data-URL wrapper was rejected by the browser environment's HTTP/HTTPS-only policy. No alternative bypass was attempted. The earlier responsive result remains historical evidence, not a new mobile validation claim.

## Report and diagram checks

- All five SVG diagrams loaded in the application; the viewer exposes full-size SVG and Mermaid-source links.
- The 24-page edition 1.2 PDF includes all five vector diagrams, all 14 report sections, and the 53-source register.
- The five embedded Mermaid blocks match the standalone `.mmd` sources byte-for-byte.
- All 53 source IDs and URLs are unique; every source citation resolves to the register.
- All SVG files parse as XML. The report renderer rejects source mismatches and records SHA-256 hashes and original PDF build provenance in `tools/render-manifest.json`.
- All PDF pages were rendered for review; the five diagrams and the Experiment field inventory received full-page visual inspection.

`python3 tools/render_report.py --check` validates existing artifacts without changing them. `python3 -m unittest discover -s tools -p 'test_*.py' -v` passes **7 tests** covering validation before writes, duplicate source URLs, unknown citations, modified artifacts/renderer, and stale PDF provenance after diagram-only generation. The PDF is visually reviewed but untagged; no accessibility certification is claimed.

The final FIS PDF SHA-256 is `afb7bbe99a0b140cd0859c8c615944df6cd0f8c0d6f4ba63d223f394908560df`.

## Generalized proposal checks

From this analysis directory:

```bash
python3 workflow/contract.py
python3 -m unittest discover -s workflow/tests -v
```

The workflow suite passes **68 tests**, including 39 independently authored review cases and 29 structural/negative/regression cases. The cases cover fixed criterion denominators, provisional versus final results, precondition/technical-success gates, partial evidence and existential witnesses, cancellation receipt races, finalization precedence, duplicate YAML keys, cycles, cross-phase/non-ancestor references, undeclared inputs/bindings/outputs, invalid writable fields, and malformed observation/cleanup shapes.

Both complete YAML examples validate against the authoring schema and proposed operation input contracts. The notification scenario has 7 main steps, 2 finalizers and 2 required criteria; the log-query scenario has 2 main steps, 1 finalizer and 1 required criterion. Their synthetic locks include program/schema/capability digests. Tests verify that alias rotation preserves old published locks, while missing/revoked pinned contracts reject admission without substitution.

All three embedded Mermaid blocks match standalone sources. Pele 1.6.0 parses and renders them; the SVGs include accessible titles/descriptions and literal presentation values for portable rendering. All three SVGs were rendered to images and visually inspected. The six-entity view, owned-value view and local lifecycle remain separate from the FIS PDF's five diagrams.

These are static reference checks. They do **not** compile CEL, run either scenario, authenticate evidence, establish source completeness, enforce real scope permissions, implement transactional API idempotency, contact AWS, or provide a durable scheduler/receiver. Synthetic implementation digests identify example labels rather than executable code. The [quality review](quality-review.md) lists the remaining integration gates.

## Review corrections applied

- Aligned the UI clock, action timeline, and simulated stop timestamps with the model's execution-time origin.
- Plotted pre-experiment baseline observations at negative offsets.
- Preserved observed resource counts while marking incomplete totals explicitly.
- Updated the selected sidebar run's status during replay.
- Kept original-scenario future safety and resource observations out of a simulated interruption.
- Exposed execution and report failures independently.
- Removed simulator schedules and future outcomes from observation exports.
- Preserved keyboard focus when controls are rerendered and paused replay for action/report inspection.
- Cleared the floated mobile search field before the horizontal scenario list.
- Froze source observation timestamps through local interruptions and exposed simulation provenance.
- Preserved each run's replay/intervention through navigation and exact action-evidence filtering.
- Kept missing metric samples, unidentified resources and unobserved reports unknown.
- Pinned historical assessment inputs and cutoff; added non-mutating artifact checks.

## Limits

The checks validate synthetic scenario behavior and the reviewed logical boundaries. They do not cover AWS authentication, permissions, throttling, pagination against a live account, service latency, real fault effects, CloudWatch retrieval, report-object access, or cross-browser/device compatibility. The optional source/document links require network access; the application itself has no external JavaScript or API dependency.
