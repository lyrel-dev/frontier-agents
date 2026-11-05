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
  - "quality-review.md"
  - "api/index.md"
---

# Validation record

Reviewed 5 November 2026. All data and operations are synthetic. This record separates executable verification, independent schema review, documentation/diagram checks and browser visual verification. Passing the mock checks does not establish live AWS integration or production readiness.

## Current review result

**61 tests passed, zero failed:** 20 model tests, nine UI contract tests, 25 RPC runtime/regression tests, four HTTP integration tests and three cross-surface evidence tests. The runtime and HTTP catalogue checks each execute all 44 operations. The three JavaScript syntax checks passed.

| Gate | Result |
| --- | --- |
| Independent JSON Schema 2020-12 validation | 53 reusable shapes, 88 operation request/response schemas and 88 executed examples passed. |
| Generated API documentation | All 47 notes match the executable contract and fixed-clock runtime examples. |
| Obsidian documentation | 61 notes, unique YAML IDs, valid required properties and closed fences; 1,282 links/properties checked at the final gate. |
| Diagrams | All five ER SVGs regenerate from the maintained Mermaid/layout sources; seven Mermaid blocks are present across the package. |
| Diff hygiene | `git diff --check` passed. All task changes are confined to `aws/resilience-hub/analysis`. |
| Fresh browser visual QA | Unverified; access was blocked as described below. |

The earlier 39-test result belongs to baseline commit `973685d8f45e0321f5bf87912f6693e217f2a26b`. It did not detect the semantic failures reproduced in [quality-review.md](quality-review.md) and is not the acceptance result for this revision.

Run the maintained checks from this directory:

```sh
node --check app.js
node --check data.js
node --check model.js
node --test tests/*.test.cjs
node scripts/generate_api_docs.cjs --check
python3 scripts/check_notes.py
python3 scripts/render_diagrams.py
```

An additional, independently implemented schema check is reproducible with Python's `jsonschema` package installed:

```sh
python3 scripts/check_api_schemas.py
```

That optional review dependency is not required by the browser, server, Node tests or documentation generator. The check loads the canonical contract and executed examples, then validates their structure using JSON Schema 2020-12 independently of the runtime's own validator. It cannot establish domain correctness or enforce the custom `x-precision` annotation; focused runtime regressions cover those obligations.

## What the regression suite establishes

| Area | Evidence and purpose |
| --- | --- |
| Independent assessment evidence | Paired workflows produce the same simulated assessment response before and after changing operator dispositions. Resolving or suppressing findings cannot synthesize green posture or verified remediation. |
| Coverage and applicability | Current evidence is distinct from retained history. Tests advance the clock, remove captured context, omit an expected outcome and use an availability-only policy. Current mutable policy content cannot rewrite a historical coverage result. |
| Explainable attention | Open findings, health/posture conditions, failed work, discovery gaps, incomplete finding/assessment evidence and relevant configuration changes produce named reasons. The service union is deduplicated. |
| Browser/API agreement | Cross-surface tests assert six current assessments, seven retained observations and eight services needing attention at baseline; zero current coverage after 48 hours; and null percentages for an empty denominator. They compare per-service reasons and expected components. |
| Read-model evidence | Current target/context, selected health/posture observations and finding capture/detail coverage can be inspected through public responses rather than private server state. Unknown provider fields retain explicit normalization information. |
| Timestamp integrity | Sub-millisecond inputs are rejected before storage. Equal-time and older health observations are retained without replacing the current observation. Missing provider timestamps remain null. |
| Mutation ownership | Telemetry, finding dispositions and assessment observations do not consume service configuration versions. Recommendation enrichment and dependency governance use their own nested edit versions. Relevant configuration changes invalidate evidence separately from metadata edits. |
| Events and audit subjects | Create/update/delete events retain the affected typed entity scope. Bounded raw envelopes and correlation IDs survive ingestion without becoming authoritative state patches. Scoped duplicate delivery cannot create a second side effect. |
| Native-shaped boundaries | Documented opaque ARNs, nullable permission observations, bounded report/tag/EKS inputs and strict writable enums are exercised beyond the happy-path fixtures. |
| HTTP and operation catalogue | All 44 operations execute through a real loopback HTTP server. Tests cover transport headers/routes, body limits, malformed JSON, request IDs, typed errors, authorization, idempotency and signed pagination. |
| History and relationship scopes | Shared-service deduplication, same-system journey membership, service-scoped child identities, immutable recommendation evidence, topology endpoint scope and deletion guards remain covered. |
| UI behavior | In-memory DOM tests execute actual browser scripts for all views, service tabs and inspectors; command dispatch, escaped comments, absent recommendation/query data, coverage labels and legacy cache handling are checked. |

The tests intentionally include independent expected outcomes and multi-step workflows. Generated examples still serve a useful contract-drift role, but agreement between a handler and its own schema is insufficient to prove the operator interpretation correct.

## Documentation and diagram checks

The package contains **61 Markdown notes**, including the new adversarial review. Every note has a unique YAML ID and all ten standard properties. The note checker verifies relative links, related-note references, local heading anchors and closed code fences. All maintained prose documents use Obsidian-compatible Markdown with YAML headers.

The API generator maintains **47 notes**: 44 operation notes plus index, schemas and errors. Each operation's example response comes from an isolated fixed-clock runtime. The generator's check mode detects stale generated notes, including changes in nullable fields, evidence bundles, timestamp precision and nested mutation versions.

There are **five ER diagram notes** and **two workflow Mermaid blocks**. Each ER note contains editable Mermaid source and a deterministic SVG representation. The renderer checks entity declarations, fields, relationship routes and bounds against its presentation layouts. This review adds explicit policy-context capture, recommendation enrichment, dependency governance and event-subject relationships. Capture terminology is consistently `captureEndedAt`; `EventSubject` is the event-to-entity junction and does not collide with the API's `EventEntity` envelope.

The report retains its original 48 official AWS source definitions and adds one current SDK source. The native adapter mapping retains its original sources and adds the current source material used to challenge ARN syntax, permission observations, input bounds and event details. The report's implementation matrix distinguishes implemented, partial and deferred capabilities.

## Current visual verification limit

**Fresh browser layout and accessibility verification is unverified for this revision.** The managed cloud browser could not reach the local preview server. Its URL policy also rejected a local-file preview. No alternate route was used to bypass that restriction. The current scripts were exercised through the in-memory DOM tests, but those do not test CSS layout, browser focus behavior, downloads, physical-device interaction or accessibility conformance.

The prior overview image was removed because it displayed superseded attention and assessment-coverage totals. No older screenshot is presented as evidence of this revision. Updated SVG diagram artifacts were visually inspected separately as rendered static images, and their deterministic source checks pass.

Before treating the revised interface as visually accepted, open it in a browser that can access the local HTTP preview and verify desktop/mobile layout, the new evidence explanation panel, legacy-cache notice, keyboard focus and snapshot export. That is a remaining visual gate, not a completed check.

## Historical browser checks

Before this quality revision, the actual Chrome preview exercised the initial overview, service assessment scenario, finding triage, topology inspection, diagram display, search, a 390-pixel responsive frame, reload/reset and JSON export. Those results remain historical. In particular, the earlier immediate triage check did not continue through the later assessment completion that manufactured verified remediation; this review reproduced that missed failure and added the multi-step regression.

The previous responsive check used a same-origin iframe rather than a physical device. It never established WCAG conformance. These earlier results must not be carried forward as proof that the changed layout and new evidence messages have been visually verified.

## Delivery boundaries

The browser and RPC process still have separate mock stores. Browser controls do not send HTTP requests to the server. The RPC process has no native AWS collector, durable persistence, production authentication, asynchronous completion worker or real EventBridge/telemetry subscriptions. Starting an assessment through the RPC API queues a mock run; the browser's separate completion scenario is not a working HTTP completion pipeline.

Full native partial-visibility references, arbitrary historical policy-content/capture queries, complete native topology descriptors and provider-side write/clearing/concurrency behavior remain partial or deferred as stated in [report.md](report.md). Validating all 44 local operations cannot close those integration gaps.

The corrected package can support design and API review within that explicit mock scope. The [adversarial review](quality-review.md) records the defect evidence and acceptance decision; this validation record states exactly which checks support it and which remain open.
