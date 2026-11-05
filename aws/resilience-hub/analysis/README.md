---
id: "aws-resilience-hub-analysis-index"
title: "AWS Resilience Hub — reviewed model and operator prototype"
type: "index"
service: "aws-resilience-hub"
status: "reviewed"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "operator-ui"
  - "api-design"
aliases:
  - "Resilience Hub workspace"
related:
  - "report.md"
  - "review.md"
  - "validation.md"
  - "api/index.md"
---

# AWS Resilience Hub — reviewed model and operator prototype

An interactive, single-page operator workspace demonstrating the reviewed **next-generation AWS Resilience Hub** entity model. The fictional **Northstar Commerce** portfolio makes shared service ownership, resilience posture, runtime health, discovery coverage and event-driven updates visible together.

The browser application is a static HTML/CSS/JavaScript page with no build step, external runtime dependency, CDN, AWS SDK or credentials. It runs without a backend, and its state changes persist in the current browser through `localStorage` when available. A separate runnable [mock RPC API](api/index.md) implements the proposed operator contract. All records, events, telemetry, cost estimates and operator actions are synthetic.

All documentation is maintained as Obsidian-compatible Markdown with YAML properties. Each of the five diagram notes includes editable fenced Mermaid source; SVG assets provide the stable layout used by the browser.

![Northstar Resilience workspace overview](assets/overview.jpg)

## Open the application

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Then open:

```text
http://localhost:8080/aws/resilience-hub/analysis/
```

The entry point is [index.html](index.html). Direct file opening also renders the application because it uses ordinary deferred scripts and local assets, but HTTP provides consistent browser-storage behavior. No installation is needed to run the application.

The **Simulate event** button advances a fixed demo clock. There is no background timer or connection to live AWS data. **Export snapshot** downloads the full synthetic state and its provenance as JSON. The reset control in the top bar restores the initial portfolio after confirmation.

## Run the mock RPC API

From this analysis directory, start the separate Node.js process:

```sh
node api/server.cjs
```

The default endpoint is `http://127.0.0.1:8787/`. Requests use `POST /`, `Content-Type: application/x-amz-json-1.1` and an operation-specific `X-Amz-Target` header:

```sh
curl http://127.0.0.1:8787/ \
  -H 'Content-Type: application/x-amz-json-1.1' \
  -H 'X-Amz-Target: ResilienceWorkspace_20261105.ListServices' \
  --data '{"maxResults":2}'
```

Use `node api/server.cjs --port 8788` to select another loopback port. The `--role reader|operator|admin|ingestor|demo` option fixes the mock principal on the server; the default `demo` role permits all mock operations. Clients cannot assert their role or tenant in request bodies. See the [API reference](api/index.md) for request and response shapes, operation behavior, pagination, version checks, idempotency and native AWS mappings.

The API process maintains its own in-memory state, which resets on restart. **The browser UI is not yet connected to this HTTP API:** browser actions modify its local mock state, and RPC actions modify only the server's state. Both begin with the Northstar portfolio, so either interface can demonstrate the model independently.

The RPC namespace is a proposed product facade. It resembles AWS JSON RPC conventions but is not the native Resilience Hub v2 wire protocol or an AWS endpoint; the [native mapping](api/aws-mapping.md) records that distinction.

## What to explore

| Workspace | Working behavior |
| --- | --- |
| Overview | Independent health, posture, open-finding and assessment-coverage cards; scoped service watchlist; attention priorities; business context; recent events. |
| Systems & journeys | Three systems and five user journeys, their policies, shared member services and deduplicated attention counts. |
| Services | Search and system/journey filters; service identity; permission model; input sources; associations; discovery configuration. |
| Findings | Status/severity filters, all three recommendation categories, local estimates and editable operator disposition/comments. |
| Dependencies | Consumer-scoped DNS relationships, criticality editing, local governance labels, query-window observations and discovery gaps. |
| Event stream | EventBridge, entity-timeline, telemetry and local-action provenance; occurrence/receipt timestamps; refresh outcomes; normalized event inspection. |
| Data model | The ten requested concepts, the five reviewed ER diagrams, editable Markdown/Mermaid notes, the reviewed report, review record and RPC API reference. |

Each service has six detail tabs: overview, findings, policy and posture, dependencies, topology, and assessments. Topology nodes can be inspected, and typed edges can be filtered. Arrow direction represents the captured source/destination relationship; it does not assert failure propagation.

### Suggested walkthrough

1. Start at **Overview**. Customer identity is healthy with retained achievable posture even though its latest assessment failed. Customer notifications has expired health evidence and no assessed posture. These conditions remain distinct.
2. Open **Systems & journeys**. Order ledger and Customer notifications belong to three systems. Portfolio totals count each service once; the same service may appear in several business contexts.
3. Select **Simulate event → Payment latency rises**. Payments health becomes degraded while its resilience posture and findings stay unchanged.
4. Select **Dependency discovered**, then inspect the new fraud-screening dependency. Edit its consumer criticality and comment. Its local allow-list review and runtime health remain separate.
5. Open Checkout orchestration → **Assessments → Start assessment**. Use the simulator inside that service dialog and select **Assessment completes**. The new Checkout run completes; the unrelated active Orders run is untouched.
6. Open a finding, mark it resolved and record a comment. The UI explicitly says verification is pending. Triage does not directly make runtime health or posture green.
7. Simulate **Duplicate and delayed events**, then inspect the event stream. Older evidence remains historical and cannot replace a newer current observation. **Telemetry goes stale** advances the clock beyond signal expiry and makes affected health unknown.

## Mock portfolio

The initial dataset contains **3 systems, 5 journeys, 8 services, 4 policies, 9 assessments, 14 findings, 25 recommendation instances, 9 dependencies and 8 topology captures**. It also includes scoped finding captures/observations, effective-target observations, policy context, health/posture history and provenance-bearing events.

Initial displayed totals are **5 healthy, 2 degraded and 1 unknown service; 3 services with at-risk posture; 10 open findings, including 4 high severity; and 7 services with assessment evidence**. One assessment is active. The broader attention rule identifies six services because it also includes failed assessment execution, stale/missing evidence and discovery gaps.

Each topology intentionally shows a **six-resource representative mock subgraph**, with its scope and the broader mock inventory count displayed. A completed collection is not presented as a complete real-world service graph or an atomic provider snapshot.

## Model decisions embodied in the UI

The detailed rationale and official API references are in [report.md](report.md); the review corrections are recorded in [review.md](review.md).

- **Shared ownership:** systems and journeys associate with services through scoped many-to-many relationships. Membership does not imply a request sequence.
- **Separate dimensions:** assessment execution, component achievability, live health, finding disposition, discovery coverage and evidence age are independent.
- **Conservative business summaries:** a journey's member services can need attention without proving that the journey failed its own potentially looser objectives. Aggregates retain distinct contributors and membership context.
- **Historical evidence:** findings belong to a service. A local capture may correlate them with an assessment without inventing a native assessment-to-finding foreign key. Recommendations belong to immutable detail observations.
- **Optional fields:** missing, null, zero, empty, unknown and stale have different meanings. Unestimated remediation cost is not zero. Summary refreshes preserve omitted detail.
- **Policy provenance:** `SELF`/`CROSS_ACCOUNT` denotes ownership; direct/inherited assignment is separate evidence. A local policy-context capture is not a provider-evaluated policy revision.
- **Event handling:** native events prompt synthetic authoritative refreshes; duplicate identity is scoped by channel and stream. Older evidence cannot roll back current health.
- **Local extensions:** runtime-health rules, recommendation names/costs/complexity, dependency governance, topology snapshots and aggregate attention are explicitly application-owned.

The fixture generator chooses effective targets from fictional policy inputs to make the demo coherent. A production adapter should consume AWS-returned effective values; this demo is not an independent implementation or certification of AWS policy evaluation.

## Files

| Path | Purpose |
| --- | --- |
| [index.html](index.html), [app.css](app.css), [app.js](app.js) | Single-page user interface and accessible interactions. |
| [data.js](data.js) | Deterministic Northstar fixtures and mock clock. |
| [model.js](model.js) | Scoped selectors, evidence projections, event ingestion and local mutation scenarios. |
| [report.md](report.md) | Reviewed analysis, logical model, operation mapping and 48 official AWS references. |
| [review.md](review.md) | Review findings, applied corrections and integration boundaries. |
| [validation.md](validation.md) | Automated and browser verification record. |
| [api/index.md](api/index.md) | Proposed AWS-style RPC operation reference and runnable local mock server. |
| [diagrams/](diagrams/) | Five Obsidian Markdown notes with Mermaid blocks, matching SVGs and deterministic presentation layouts. |
| [tests/](tests/) | Dependency-free Node domain, UI contract, RPC runtime and HTTP integration tests. |
| [scripts/render_diagrams.py](scripts/render_diagrams.py) | Optional SVG renderer for the Mermaid blocks; not required by the application. |

## Verify

From this directory, using a modern Node.js runtime with the built-in test runner:

```sh
node --check app.js
node --check data.js
node --check model.js
node --test tests/*.test.cjs
node scripts/generate_api_docs.cjs --check
python3 scripts/check_notes.py
```

The complete suite contains 39 passing tests. Browser-model checks cover scoped keys, shared-service counts, policy provenance, independent health/posture, failed-run preservation, triage, selected-service assessment completion, immutable recommendation history, omitted/empty detail, expiry, duplicate/delayed events, discovery/governance separation, partial summary hydration, rendering, safe comment escaping and Markdown diagram assets. The RPC tests exercise all 44 operations, including through the HTTP server, along with scope validation, concurrency, idempotency, signed pagination and trusted-role enforcement. In-memory UI contract checks complement the earlier browser checks documented in [validation.md](validation.md). The [API reference](api/index.md) documents its runtime and generation commands.

## Maintain the documentation

Open this directory in an Obsidian vault, or add it to an existing vault. Standard relative Markdown links work in both Obsidian and repository viewers. YAML properties describe each note, and fenced Mermaid blocks render directly in Obsidian. The Markdown notes are the canonical documents.

To regenerate the portable SVGs from the five diagram notes:

```sh
python3 scripts/render_diagrams.py
```

The renderer uses only the Python standard library. It extracts each note's Mermaid block and uses `diagrams/diagram-layouts.json` for stable presentation geometry, checking entity declarations, relationships, routes and field bounds. SVG generation requires no external renderer or CDN.

## Integration scope

This prototype demonstrates the model, operator interactions and a corresponding mock RPC contract. It does not connect to an AWS account, authenticate real users, synchronize browser and server state, run real telemetry subscriptions or validate production IAM permissions. Before enabling live writes, verify association replacement/removal, clearing semantics, authorization, pagination and concurrent edits against the selected SDK and controlled account responses, as detailed in the report.
