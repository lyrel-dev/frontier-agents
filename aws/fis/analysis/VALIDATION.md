# Application validation

Validated on 5 November 2026. This is a static mock-data showcase; no AWS account was connected and no service-side fault action or stop request was made.

## Automated model checks

`node --test app/tests/model.test.cjs` passes **19 tests**. The suite covers action identity, same-run dependency edges, target binding integrity, overlapping target memberships, unknown/partial collections, preview semantics, observation-time filtering, execution versus assessment versus report outcomes, structured errors, stale polls, replay immutability, and exports that exclude future simulator data. `node --check app/app.js` passes.

The fixture integrity validator also checks references, resource types, account coverage, target-slot bindings, parameter strings, and dependency ordering. These checks exercise the model; they do not prove live AWS behavior.

## Browser checks

The application was exercised in Chromium through a local static preview.

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

## Report and diagram checks

- All five SVG diagrams loaded in the application; the viewer exposes full-size SVG and Mermaid-source links.
- The 27-page PDF includes all five vector diagrams, all 14 report sections, and the 53-source register.
- The five embedded Mermaid blocks match the standalone `.mmd` sources byte-for-byte.
- All 53 source IDs and URLs are unique; every source citation resolves to the register.
- All SVG files parse as XML. The report renderer rejects source mismatches and records SHA-256 hashes in `tools/render-manifest.json`.
- All PDF pages were rendered for review; the five diagrams and the Experiment field inventory received full-page visual inspection.

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

## Limits

The checks validate synthetic scenario behavior and the reviewed logical boundaries. They do not cover AWS authentication, permissions, throttling, pagination against a live account, service latency, real fault effects, CloudWatch retrieval, report-object access, or cross-browser/device compatibility. The optional source/document links require network access; the application itself has no external JavaScript or API dependency.
