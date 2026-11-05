---
id: "aws-resilience-hub-validation"
title: "Resilience Hub prototype and API validation record"
type: "validation"
service: "aws-resilience-hub"
status: "reviewed"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "validation"
  - "operator-ui"
aliases:
  - "Resilience Hub validation"
related:
  - "README.md"
  - "report.md"
  - "review.md"
  - "api/index.md"
---

# Validation record

Reviewed 5 November 2026. The application uses synthetic data throughout. This record describes checks of the prototype, model, RPC implementation and documentation; it does not claim a live AWS integration or production readiness.

## Complete package result

**39 tests passed, zero failed:** 13 domain tests, six UI contract tests, 16 RPC runtime tests and four HTTP integration tests. The HTTP catalogue test invokes all 44 operations through a real loopback server. The runtime catalogue test executes all 44 documented examples against fresh fixture states.

Run the reproducible package checks from this directory:

```sh
node --test tests/*.test.cjs
node scripts/generate_api_docs.cjs --check
python3 scripts/check_notes.py
python3 scripts/render_diagrams.py
```

The checked documentation contains **60 Markdown notes**, each with a unique YAML ID and all ten standard properties. The note checker validates relative links, related-note references, local heading anchors and closed fences. There are five ER diagram notes and two API workflow Mermaid blocks. The generated API reference contains 44 operation notes plus its index, schema reference and error reference; its examples are generated from executable handlers rather than copied by hand.

## RPC implementation checks

| Area | Evidence |
| --- | --- |
| Catalogue and schemas | All 44 operation examples execute and validate against the contract. An independent JSON Schema 2020-12 review validated 34 reusable shape definitions, all 88 input/output schemas, and the corresponding executed request/response examples. |
| HTTP transport | All 44 operations return their expected response through `POST /`; tests cover media type, target namespace, path, method, malformed/non-object JSON, body limits with declared length and chunking, request IDs, typed errors and safe unexpected-error responses. |
| Mutations and relationships | CRUD lifecycle, same-system journey associations, failed-command atomicity, provider field names, input-source unions, EKS selector constraints, active-assessment/deletion guards and retained historical reads. |
| Concurrency and retries | Version conflicts; identical retries before version checking; changed-body token conflicts; no repeated mutation or audit effect on replay. |
| Pagination | Stable local traversal across mutations; signed tokens scoped to principal, operation and filters; tampering, mismatched scope and expiry rejected. |
| Authorization | Trusted server-side roles and tenant context; reader write rejection; client-supplied role/tenant fields and headers cannot grant privileges. |
| Health and events | Old and equal-time observations retained without rollback; independent expiry; duplicate and seeded event-key collision handling; events request a refresh without claiming refreshed posture or completed assessment. |
| Evidence ownership | Immutable recommendation source content and observation scope; separate enrichment/governance versions; finding disposition independent of health and assessed posture. |
| Topology | Captures retain source observation time, scoped graph identity and partial/unresolved coverage; no provider read or atomic AWS snapshot is asserted. |

The runtime uses a small validator for the schema keywords in this contract. The independent schema review used a separate JSON Schema implementation during this review; no third-party runtime dependency is required to run the server or its tests. Documentation regeneration uses a fixed clock and signing secret for stable examples. A normally started server advances the demo clock with elapsed process time and generates its own cursor secret.

## Browser-model automated checks

Run from this directory:

```sh
node --check app.js
node --check data.js
node --check model.js
node --test tests/model.test.cjs tests/ui-contract.test.cjs
```

**Result: all three JavaScript syntax checks passed; 19 tests passed, 0 failed.**

The 13 domain tests cover scoped keys and relationships, shared-service and finding deduplication, independent policy ownership and assignment, separation of health from posture, preservation of posture after a failed assessment, unverified operator triage, scoped assessment completion, immutable recommendation history across captures, omitted versus empty recommendation details, telemetry expiry, duplicate and delayed events, discovery coverage and local governance, and preservation of hydrated details when merging summaries.

The six UI contract tests execute the actual browser scripts against a small in-memory DOM surface. They verify that all seven workspace views, all six tabs for every service, and all finding/dependency/event inspectors render; that system/journey selections display their distinct member services; that unestimated costs stay unknown; that a run started in a service modal is completed for that service; that triage persists escaped comments while retaining health and posture; and that local entrypoint/model links resolve, the documentation has YAML properties, and all five diagram notes contain Mermaid source and matching SVG assets.

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
| Cross-account permission field | Fresh fixtures use the native `permissionModel.crossAccountRoles[].crossAccountRoleArn` field, consistent with the reviewed source mapping. |
| Editable documentation | The report, review and diagram notes use Markdown with YAML properties; UI links point to these notes and the API reference. |

## Documentation conversion checks

The documentation conversion preserves all 48 official source definitions in the report and the exact Mermaid content of all five diagrams. Every analysis and diagram note has flat YAML properties. Regenerating the SVGs with `python3 scripts/render_diagrams.py` produces the same diagram assets as the reviewed implementation, and the renderer validates the extracted Mermaid relationships against their presentation layouts.

The obsolete PDF artifact and its PDF-only build dependencies were removed because Markdown is now the maintained document format. The browser continues to display the existing SVG diagrams and provides links to their editable Markdown notes.

## Verification boundaries

AWS-shaped records are manually authored mock fixtures. EventBridge delivery, production IAM permissions, native AWS pagination, provider-side mutation semantics, live telemetry adapters, and reconciliation against a real account are outside this prototype. A production implementation must preserve the report's source and observation distinctions when those adapters are added.

The [RPC API package](api/index.md) is a separate local mock implementation with its own in-memory state. The browser tests above exercise the existing browser state and do not establish RPC transport or operation correctness. Browser actions do not issue HTTP requests to that server.

## Previously completed browser verification

Before the Markdown and RPC extension, the application was exercised in the managed Chrome preview with its actual DOM and controls. The following checks passed. The current extension preserves those browser interactions; its documentation-link and fixture-field changes are covered by the rerun automated checks above.

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
