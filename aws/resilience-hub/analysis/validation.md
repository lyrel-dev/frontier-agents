# Validation record

Reviewed 5 November 2026. The application uses synthetic data throughout. This record describes checks of the prototype and its model; it does not claim a live AWS integration or production readiness.

## Automated checks

Run from this directory:

```sh
node --check app.js
node --check data.js
node --check model.js
node --test tests/model.test.cjs tests/ui-contract.test.cjs
```

**Result: all three JavaScript syntax checks passed; 19 tests passed, 0 failed.**

The 13 domain tests cover scoped keys and relationships, shared-service and finding deduplication, independent policy ownership and assignment, separation of health from posture, preservation of posture after a failed assessment, unverified operator triage, scoped assessment completion, immutable recommendation history across captures, omitted versus empty recommendation details, telemetry expiry, duplicate and delayed events, discovery coverage and local governance, and preservation of hydrated details when merging summaries.

The six UI contract tests execute the actual browser scripts against a small in-memory DOM surface. They verify that all seven workspace views, all six tabs for every service, and all finding/dependency/event inspectors render; that system/journey selections display their distinct member services; that unestimated costs stay unknown; that a run started in a service modal is completed for that service; that triage persists escaped comments while retaining health and posture; and that the entrypoint assets, reviewed report and all five diagram pairs exist.

These contract tests exercise render functions and command dispatch. They do **not** substitute for a browser's layout, focus, accessibility or download behavior.

## Review corrections carried into the implementation

| Concern | Implemented behavior |
| --- | --- |
| Undefined recommendation observation reference | Explicit observation primary keys and recommendation foreign keys; historical instances remain available after later captures. |
| Summary/detail ambiguity | Finding captures distinguish list collection from detail hydration and omitted recommendation arrays from known empty arrays. |
| Shared-service counts | Service membership is deduplicated, and business attention uses the common model rule. |
| Unknown recommendation cost | A null estimate renders as **Not estimated**, rather than zero. |
| Assessment completion target | The simulator is reachable within the service modal and receives the selected service context. |
| Event severity presentation | Warning/error events have matching semantic styles; dependency events use a dependency marker. |
| Topology coverage | The UI identifies representative subgraphs, capture completeness, unresolved resources and the broader synthetic inventory. |
| Keyboard interactions | Tab lists support arrow/Home/End navigation, and selected tab/node focus is restored after rendering. |
| User-entered comments | Comments are rendered as escaped text. No credentials or AWS requests are used. |

## Verification boundaries

AWS-shaped records are manually authored mock fixtures. EventBridge delivery, IAM permissions, pagination, provider-side mutation semantics, live telemetry adapters, and reconciliation against a real account are outside this prototype. A production implementation must preserve the report's source and observation distinctions when those adapters are added.

## Browser verification

The application was exercised in the managed Chrome preview with its actual DOM and controls. The following checks passed:

- The desktop overview displayed all eight services and the expected independent health, posture, finding and assessment totals.
- A new Checkout orchestration assessment moved to queued, then completed through the simulator inside that service's dialog. The existing Orders assessment remained active.
- A high-severity Checkout finding was marked resolved with an operator comment. The inspector displayed **verification pending** and kept service health and posture unchanged.
- A topology resource could be selected and inspected. The view showed the representative six-resource scope, broader 34-resource inventory, capture time and completeness. Resource labels fit their nodes.
- The model view loaded and displayed the business-structure and assessment/finding SVG diagrams, including the corrected observation key and qualified assessment correlation.
- Overview search for **identity** retained the failed-run attention card despite healthy runtime evidence and achievable retained posture. This also verified the corrected attention empty state.
- The 390-pixel responsive frame displayed two-column summary cards and working mobile navigation. After correcting the visually hidden label's positioning, document scroll width equaled client width; wide tables and diagrams scroll inside their own containers.
- Finding triage persisted across reload. Reset restored the original dataset and counts.
- **Export snapshot** produced a nonempty, parseable JSON file containing `SYNTHETIC_DEMO_SNAPSHOT`, eight services, fourteen findings and the baseline mock clock after reset.

The responsive check used a same-origin 390 × 844 iframe to exercise CSS viewport behavior; it was not physical-device or touch testing. Temporary preview files were removed before committing. Browser checks do not establish WCAG conformance or replace live AWS adapter tests.
