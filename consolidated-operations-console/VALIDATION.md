# Validation and evidence boundaries

This package is a **phase-one model and API specification**. Its checks establish structural consistency, source traceability and selected cross-record invariants in synthetic data. They do not establish production persistence, identity enforcement, actual cloud execution or service behavior.

## Reproduce the checks

Run from `consolidated-operations-console/` in a checkout containing the pinned source commit:

```sh
python -m pip install -r tools/requirements.txt
python tools/validate.py
python tools/render_model.py --check
python api/generate.py --check
```

Python 3.12, `jsonschema` 4.26.0 and `referencing` 0.37.0 were used. The validator resolves the model and RPC schema IDs locally; it does not fetch schemas from their illustrative `.example` URLs. JSON numbers are parsed with Decimal so millisecond timestamp constraints are checked before comparison. Duplicate JSON keys are rejected.

To regenerate the entity reference and diagrams, install Graphviz and run:

```sh
python tools/render_model.py
```

Seven SVGs are rendered from the same authoritative schema as their Mermaid/DOT sources. [The diagram manifest](diagrams/manifest.json) records the schema hash, source/output hashes and actual Graphviz version. `--check` compares existing bytes without first regenerating them, so it cannot hide stale output.

Mermaid syntax uses the pinned JavaScript dependencies:

```sh
npm ci --prefix tools --ignore-scripts
node tools/check_mermaid.mjs
```

For an intentional source change, run `node tools/check_mermaid.mjs --write` after reviewing the diagrams. The checker supports an existing identical dependency installation through `CONSOLE_DIAGRAM_RUNTIME`; the executed review reused that installation. [Syntax evidence](diagrams/mermaid-syntax.json) records Mermaid 11.12.2 and jsdom 26.1.0, every source hash and the rejected malformed-class negative control. SVG rendering uses Graphviz; no rendering equivalence between engines or installed Obsidian certification is claimed.

## Validation results

**PASS**, independently rerun on the completed package on 5 November 2026. The machine-readable result is [validation.json](validation.json). Source counts and design scope are independently inspectable in [inventory.json](inventory.json), [model/schema.json](model/schema.json), [model/examples.json](model/examples.json) and [api/operations.json](api/operations.json).

| Check | Executed result |
| --- | --- |
| Source inventory | All 226 active files match the pinned Git tree, blob hashes and byte sizes. |
| Model schema and examples | 37 entity schemas and 173 connected fictional records validate. |
| Semantic cases | 45 cases pass their stated expectation: nine valid cases and 36 invalid cases rejected for the expected reason. |
| Crosswalk | 174 mapping rows, 340 source aliases, 65 profiles; 182 independently extracted source concepts are accounted for. |
| Source-profile resolution | All worked source profile IDs and normalized bindings resolve to the declared registry/schema. |
| Class diagrams | Seven complete/focused diagrams have matching entity coverage, valid SVG XML and current source/output hashes. |
| Mermaid syntax | All seven sources parse with Mermaid 11.12.2; an unclosed-class negative control is rejected. |
| Model generation | `tools/render_model.py --check` reports no stale generated reference, diagram source or rendered output. |
| API generation | `api/generate.py --check` matches all four generated API artifacts. |
| RPC contracts and examples | 101 operations, all 202 request/response payloads and three typed error payloads validate. |
| Prior operation dispositions | All 44 Resilience facade and 16 workflow predecessor operations have explicit mappings or documented deferrals. |
| Markdown paths | All checked relative links resolve. |

The semantic corpus includes workspace/parent isolation, public versus organization Health impact, phase-specific result selection, duplicate observations, unknown evidence, absence over an open/partial window, skipped required criteria, frozen admission bindings, workflow cycles, uncertain effects, policy capture consistency, incomplete finding detail, snapshot closure, graph endpoint scope, target selection versus fault evidence, stale coverage and a zero-denominator percentage. It also checks that successful execution can coexist with failed acceptance and that completed local work cannot change provider impact/finding evidence.

## Visual review

The complete diagram and all six focused module diagrams were rendered to PNG for inspection. The review corrected a Unicode title-escaping issue and reorganized the rows to reduce overlapping labels. Every entity appears in the complete zoomable SVG. Class boxes show selected fields; the generated [reference](model/REFERENCE.md) supplies the full field and relationship contracts. Focused SVGs provide the practical reading path for individual modules.

## What the examples establish

The worked data is explicitly synthetic. It links the modules through scoped service/resource identities and exact evidence references. It demonstrates repeated observations without duplicated source revisions, distinct native and local state, a failed acceptance criterion after technically successful execution, and independently retained historical captures.

API examples are independent request/response illustrations assembled from that data. They were not executed against an HTTP service and are not a chronological transaction log. A later successful decision or provider observation in one illustration is an explicit precondition in another; an accepted command response cannot be treated as proof of the later outcome.

Fixture source-content digests are verified for a deliberately restricted canonical JSON subset: ASCII keys/strings, safe integers, booleans, null, arrays and objects. Exact UTF-8 artifact strings are checked separately. The validator is not a general RFC 8785 implementation or a source authentication mechanism. Production importers must use a conforming canonicalizer or retained raw bytes under the declared digest profile.

## Remaining implementation gates

| Area | Evidence still required |
| --- | --- |
| Authorization | Trusted workspace/principal binding, complete evidence-closure authorization, scope revocation, provider permissions and export access |
| Persistence | Atomic local command admission, durable token reservation/results, immutable publication, crash recovery and retention/tombstone enforcement |
| Collection | Actual native pagination, partial/failed/empty reads, raw request/response retention, provider update behavior, source-profile conformance and unknown values |
| Provider effects | Native operation mapping, per-operation idempotency limits, lost-response reconciliation, out-of-band changes and final observed state |
| Workflow | Trusted operation registry, expression/type conformance, dispatch intent, retry eligibility, cancellation/dispatch races, leases/fencing and bounded finalization |
| History | Closed snapshot retention, artifact availability and access changes, later source updates and independent historical retrieval |
| UI | Usability, keyboard/accessibility behavior, responsive layouts and exact selected-evidence inspection over the actual common backend |
| Compatibility | Migration tests for the old 44-operation Resilience facade and 16-operation workflow proposal, including deliberate identity/transport/ownership changes |

Earlier packages' test results remain evidence about those packages. They are not counted as tests of a newly implemented consolidated application. [REVIEW.md](REVIEW.md) records the concrete issues found and addressed in this consolidation.
