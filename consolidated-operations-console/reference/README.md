# HTML reference: sources, regeneration and verification

[Open the complete HTML reference](../reference.html). Download it and open it in a browser for local navigation, filtering, diagram zoom and printing. The document contains its styles, script, eight native Draw.io SVG exports and licensed diagram fonts; reading and searching do not require network access. Repository source links intentionally open the exact cited commit.

## Coverage

| Content | Included |
| --- | ---: |
| Versioned entities | 36 |
| Entity fields | 450 |
| Entity use cases | 72 |
| Historical entity-origin explanations | 74 |
| API operations and individual operation use cases | 108 |
| Request / response fields | 441 / 211 |
| Request / response payload examples | 216 |
| Error examples | 3 |
| Cross-module use cases | 7 |
| Model / RPC owned value types | 64 / 8 |
| Declared entity relationships | 45 |
| Draw.io pages | 8 |
| Source-concept mapping rows / aliases | 174 / 340 |
| Native source profiles | 65 |
| Predecessor operation dispositions | 161 |

Every entity has purpose, identity, ownership, lifecycle, invariants, fields, use cases, relationships, historical definitions and uses, relevant source mappings, API links and a checked fixture example. Every operation has purpose, actor/scenario/steps, preconditions, wire target, permission and effect, request/response fields, semantics, errors, examples, predecessor mappings and related next operations.

The current model/API source baseline is [`31980a1`](https://github.com/lyrel-dev/frontier-agents/commit/31980a1b7540b1ad74274b0edfc7fc1f08f6a396). Earlier AWS analysis sources remain pinned to [`d926a81`](https://github.com/lyrel-dev/frontier-agents/commit/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3). The original consolidated V1 predecessor catalog is pinned to [`db142c8`](https://github.com/lyrel-dev/frontier-agents/commit/db142c84bcfd691d5c71071681731cac81a52c7b). The document distinguishes previously defined native resources and application aggregates from shared infrastructure introduced by consolidation.

## Inputs and ownership

| Input | Responsibility |
| --- | --- |
| [model/schema.json](../model/schema.json) | Authoritative entities, fields, value types, relationships and version/authority metadata |
| [api/operations.json](../api/operations.json) | Operation effects, permissions, delivery phases, semantics, errors, coverage and predecessor mapping |
| [api/rpc.schema.json](../api/rpc.schema.json) | Exact request and response shapes |
| [model/examples.json](../model/examples.json), [api/examples.json](../api/examples.json) | Schema-checked synthetic examples; individual illustrations have their own admission assumptions |
| [model/adapter-profiles.json](../model/adapter-profiles.json) | Complete source-concept and native profile crosswalk |
| [diagrams/manifest.json](../diagrams/manifest.json), [model.drawio](../diagrams/model.drawio) and its SVG exports | Reviewed Draw.io atlas; source geometry and SVG files remain unchanged |
| [entity-notes.json](entity-notes.json) | Editorial entity purpose, lifecycle, ownership, use cases and section-level historical provenance |
| [operation-notes.json](operation-notes.json) | Editorial operation purpose, use cases, preconditions, pitfalls and related operations |
| [reference.css](reference.css), [reference.js](reference.js) | Responsive/print layout and progressive navigation enhancements |
| [tools/build_reference.py](../tools/build_reference.py) | Deterministic HTML assembly, shared guide and seven cross-module journeys, completeness checks |

The generator uses the contracts directly instead of copying schema fields into the narrative notes. All 36 preferred entity examples resolve to existing fixture representations. Request/response examples are copied unchanged from the checked API fixtures. Their displayed HTTP wrapper uses the catalog target and media type.

The embedded Draw.io SVGs only receive document-unique XML IDs and corresponding reference updates, which prevent collisions between eight inline pages. They are not redrawn. Small DejaVu Sans and Mono WOFF subsets preserve diagram typography offline; their redistribution notice is in [fonts/LICENSE.txt](fonts/LICENSE.txt) and embedded in the HTML. The subsets contain the characters used in the existing atlas, were produced with FontTools from the installed DejaVu fonts, and are committed build inputs. Ordinary regeneration does not require FontTools or a font download.

## Reproduce

From the repository root:

```bash
python consolidated-operations-console/tools/build_reference.py
python consolidated-operations-console/tools/build_reference.py --check
```

The builder uses the Python standard library and local Git history. It writes the HTML and [build-report.json](build-report.json), including all input hashes and the exact HTML hash. `--check` performs the same build without writing, rejects stale output, and verifies exact entity/operation/type/profile coverage, use-case completeness, valid related names, pinned entity source paths, unique HTML/SVG IDs, all internal links, and absence of external runtime assets.

Edit the notes for narrative changes and the canonical model/API files for contract changes. Then regenerate. Do not hand-edit `reference.html` or the generated build report.

## Review and validation

The source and narrative review verified every one of the 74 historical origins against its pinned file and heading. All related entity and operation names resolve. Independent HTML inspection verified every distinct pinned repository link against local Git objects, including the earlier operation packages; the links use full commit SHAs.

JSDOM 26.1 executed the actual embedded script and checked:

- Exact 36-entity and 108-operation card coverage, unique IDs and internal links.
- Case-insensitive search, zero-result behavior, combined module/type filters and reset/focus behavior.
- Deep links into filtered-out entries, all eight diagram zoom controls, and restoration of disclosure state after print.

WeasyPrint 70 rendered the full print document. Text-bound checks found no horizontal overflow; representative cover, entity, API and diagram pages were visually inspected. The review corrected a diagram-heading orphan by keeping the toolbar with its image. Wide and narrow CSS-resolved screen probes were also inspected for introductory layout and wrapping. The complete print reference is intentionally long because it includes every operation's response example; duplicate raw JSON Schema disclosures remain available in the HTML and are omitted from print.

This is **not Chromium screenshot verification**: Chromium execution was unavailable in the executor, and the native browser blocked access to the local repository. JSDOM does not implement print layout and emits a known unsupported nested `@page` rule warning; it reported no script errors. WeasyPrint provides print and CSS-layout evidence, not full browser-engine conformance. These limits do not change the schema/source coverage checks.

The HTML remains a contract reference with synthetic examples. It does not implement or demonstrate production authentication, persistence, AWS mutations, durable command replay or workflow execution.
