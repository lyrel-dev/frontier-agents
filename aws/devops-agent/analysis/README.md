---
title: AWS DevOps Agent — reviewed model and investigation workspace
date: '2026-11-05'
service: aws-devops-agent
type: analysis-index
status: reviewed-prototype
tags:
  - aws/devops-agent
  - investigation
  - data-model
  - prototype
---

# AWS DevOps Agent: reviewed model and investigation workspace

**Open [index.html](index.html) to explore Lens**, a single-page operator application using realistic, entirely fictional investigation data. The generated page contains its styles, scripts, fixture, and all ten reviewed diagram SVGs. It runs offline in a modern browser with no package installation or AWS account. Keep the adjacent Markdown and diagram files to follow the documentation links.

The application demonstrates the central conclusion of the reviewed API model: an investigation is a native **Task** of type `INVESTIGATION`, related to **Executions** through observed task membership, with published **JournalRecords**. Timelines, evidence graphs, artifact collections, and historical reports are application views with retained provenance. Task lifecycle, execution status, result availability, and collection coverage are presented separately.

## Read the analysis

| Material | Purpose |
| --- | --- |
| [Reviewed report](report.md) | Consolidated API and logical-model analysis, all ten Mermaid diagrams, UI implications, and evidence boundaries |
| [Adversarial quality review](QUALITY_REVIEW.md) | Counterexamples, corrected contract failures, API maturity and remaining production gates |
| [Initial review record](REVIEW.md) | Earlier source/schema review, retained with its scope and limitations |
| [API catalog](annexes/Investigation_API_Catalog.md) | All 63 native operations and transport/error mappings; 19 detailed request and 52 selected entity/value schemas |
| [UI contract](annexes/Investigation_UI_Contract.md) | Live reconciliation, streams, summaries, snapshots, approvals, and future capture scenarios |
| [Detailed data model](annexes/Investigation_Data_Model.md) | Entity dictionary, identity rules, provenance, graphs, artifacts, and retained history |
| [Source register](annexes/Investigation_API_Sources.md) | Official references, pinned model commits/hashes, source reconciliation, and verification scope |
| [Prototype model contract](app/MODEL_CONTRACT.md) | Fixture/read-model interfaces and replay semantics |
| [Validation record](VALIDATION.md) | Executed semantic, package, diagram, and browser checks |
| [Generalized operational analysis proposal](proposals/operational-analysis/README.md) | Separate seven-entity model for assertions, queries, evidence, assessments and operator reviews, with a complete class diagram |

The source review is dated **5 November 2026** and uses the native API version **2026-01-01**. The mock observations demonstrate that contract; they are not captured AWS responses. Open record types prefixed `demo.` and their payload profiles belong to this fixture. Diagram and API source verification does not establish live account behavior.

The generalized proposal is a separate design. Its class diagram is validated through its own registry and is not presented as an implemented feature of the ten-diagram native-model application.

## Presentation walkthrough

The main checkout-latency investigation progresses through six explicit, fictional observations. **Next** steps the scenario; **Play** advances it automatically, and **Pause** stops it. These are demonstration controls, not AWS API operations or a documented transition matrix.

| Stage | What to inspect |
| --- | --- |
| 1. Investigating | Task in progress, published evidence, active executions, and partial journal collection |
| 2. Evidence correlated | Attributed findings, metric observations, graph relationships, and an available summary candidate |
| 3. Completed · result pending | Task is `COMPLETED`; a captured completion event points to an exact summary record that has not yet been collected |
| 4. Result retrieved | The referenced summary arrives and is selected by exact identity; a historical checkpoint is retained |
| 5. Investigation resumed | The same investigation returns to active work with another execution; the earlier snapshot remains unchanged |
| 6. Follow-up complete | A later result and additional observations are available while the earlier capture remains reproducible |

Suggested review sequence:

1. Open the checkout investigation and inspect its independent lifecycle, result, and coverage indicators.
2. Open a timeline item or journal source. Compare event time, record time, and observation time; inspect the retained raw JSON.
3. Move to **Evidence**. Select a graph node and inspect its attribution and source. Read the units, query, and observation window behind a metric.
4. Advance to **Completed · result pending**. Verify that an older candidate summary is not promoted over the missing exact reference.
5. Advance once more and inspect the selected summary and artifact availability. Capture an additional snapshot if useful.
6. Resume the investigation, then open **History**. Review the earlier capture and return to the current view; the retained capture should not acquire later observations.
7. Select the completed database case and the timed-out case. The latter retains incomplete and stale collection as explicit uncertainty.
8. Open **Model & report** to inspect all ten reviewed diagrams and their editable Mermaid sources. D07 explains why a repeated observation is neither a new record nor a new payload revision.

## Application areas

| Area | Operator questions addressed |
| --- | --- |
| Overview | What is happening, what is known, which results are available, and how complete is collection? |
| Timeline | What was published or observed, when, and from which source? |
| Evidence | Which observations support a finding, and which graph relationships are attributed or derived? |
| Executions | Which units of agent work were observed, how are they related, and what is each native status? |
| Artifacts | Which documents/content references are available, versioned, pending, denied, or unresolved? |
| History | What did an operator see at capture time, and what changed afterward? |
| Model & report | How do the screen concepts map to native fields and application-owned projections? |

Investigation selection, search, replay, source inspection, artifact previews, snapshot capture, historical selection, and JSON export are local interactions. Scenario progress and retained snapshots persist in this browser when local storage is available. Reload restores that saved scenario; navigation and filters start afresh. If storage is unavailable, the page shows **Session-only changes** and remains usable in memory. Invalid saved state is preserved for recovery/download until an explicit reset; it is not silently overwritten. Export a snapshot to retain a portable copy. Reset asks for confirmation before restoring the initial fixture and clearing the saved demo state.

The Task lifecycle card opens the exact Task observation displayed in the current or historical view. Investigation and mitigation results have separate model slots, completion references and candidate sets; the primary screen presents the investigation result. Logical record counts deduplicate repeat reads while retaining distinct observations and revisions. Historical exports preserve the captured payload as live activity advances. An already selected capture also renders when current-view or queue assembly fails, with comparison marked unavailable; automatic startup recovery from an unavailable live view is future integration work.

Native `STOPPED` execution status remains `STOPPED`; the application does not relabel it as successful. A task's priority is called priority. Task completion does not establish incident recovery, a recovered service, or an MTTR measurement.

## Diagrams

Every diagram appears as editable Mermaid in [report.md](report.md) and its relevant annex, as a separate `.mmd` source, as a standalone SVG with an accessible title, and in the application gallery. Entity lists are abbreviated logical models; the catalog contains wire fields and requiredness for its selected schemas. Owning account, Region, partition, and Agent Space scoping is explained in the report even when a figure abbreviates keys. Connection and authorization context remain separate from native resource identity.

| ID | Diagram | Editable source | Rendered SVG |
| --- | --- | --- | --- |
| D01 | Workspace, association and external reference | [Mermaid](diagrams/D01-workspace-associations.mmd) | [SVG](diagrams/D01-workspace-associations.svg) |
| D02 | Native investigation core and membership | [Mermaid](diagrams/D02-investigation-core.mmd) | [SVG](diagrams/D02-investigation-core.svg) |
| D03 | Projection provenance | [Mermaid](diagrams/D03-projection-provenance.mmd) | [SVG](diagrams/D03-projection-provenance.svg) |
| D04 | Graph snapshots and typed edges | [Mermaid](diagrams/D04-graph-model.mmd) | [SVG](diagrams/D04-graph-model.svg) |
| D05 | Artifact references and asset versions | [Mermaid](diagrams/D05-artifacts-assets.mmd) | [SVG](diagrams/D05-artifacts-assets.svg) |
| D06 | Immutable historical snapshots | [Mermaid](diagrams/D06-historical-snapshots.mmd) | [SVG](diagrams/D06-historical-snapshots.svg) |
| D07 | Collection evidence and bounded coverage | [Mermaid](diagrams/D07-collection-observations.mmd) | [SVG](diagrams/D07-collection-observations.svg) |
| U01 | Live reconciliation | [Mermaid](diagrams/U01-live-reconciliation.mmd) | [SVG](diagrams/U01-live-reconciliation.svg) |
| U02 | Approval, resume, and observed outcome | [Mermaid](diagrams/U02-approval-lifecycle.mmd) | [SVG](diagrams/U02-approval-lifecycle.svg) |
| U03 | Historical capture workflow | [Mermaid](diagrams/U03-snapshot-workflow.mmd) | [SVG](diagrams/U03-snapshot-workflow.svg) |

The approval diagram documents a future integration boundary. This prototype focuses on observation and history; the report explains the documented chat-only approval flow and separates decisions, resume attempts, tool execution, and operational outcomes.

## Run, rebuild, and validate

Open `index.html` directly. For a consistent local origin, optionally serve this directory:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open <http://localhost:8000/>. The server serves the checked-in files only.

Rebuild the self-contained page using Python 3 from this `analysis` directory:

```bash
python3 app/build.py
```

Edit `app/src/`, then rebuild. Direct edits to `index.html` are overwritten. The build uses the Python standard library and the checked-in SVGs; npm is unnecessary for an application rebuild.

Run behavioral and package checks:

```bash
node --test app/tests/*.test.cjs
python3 -m pip install -r tools/requirements.txt
python3 tools/check.py
```

The 42 tests require a modern Node.js with `node:test` and `structuredClone`. They exercise the model and rendered controls, including duplicate observations, opaque-ID collisions, separate result phases, conflicting completion references, malformed summaries, damaged saved state, historical export stability and unavailable current comparisons. The package checker uses pinned PyYAML to parse frontmatter; it also rejects a stale generated page or a divergent Mermaid copy. These checks do not call AWS.

Reproduce the native contract and synthetic-envelope audits:

```bash
python3 tools/check_native_api.py --fetch --self-test
python3 tools/check_fixture_schema.py --fetch --self-test
```

`--fetch` downloads the immutable Botocore pin and verifies its SHA-256. For offline use, replace `--fetch` with `--model /path/to/service-2.json`; an unexpected checksum fails closed. The API audit compares 63 operations, endpoint/status/error mappings, 19 requests and 52 selected schemas comprising 339 member rows. The fixture audit checks 46 raw objects against 23 reached shapes. Deliberately broken examples verify that both checkers detect the claimed failures. Strict fixture checks are authoring checks; a production reader must preserve unknown output enums and open JSON rather than applying these constraints as response rejection rules.

Regenerate SVGs when Mermaid sources change:

```bash
npm ci --prefix tools --ignore-scripts --no-audit --no-fund
node tools/render-diagrams.mjs
node tools/check-mermaid.mjs --write
python3 app/build.py
python3 tools/check.py
```

The renderer is pinned to **Pele 1.6.0** and the independent syntax gate to **Mermaid 11.12.2**, with **JSDOM 26.1.0**, in `tools/package-lock.json`. After an intentional source change, `--write` refreshes syntax evidence; use `node tools/check-mermaid.mjs` for verification without rewriting evidence. The gate checks all ten sources and a deliberately invalid ER relationship. SVGs use unique diagram prefixes and accessible titles. [Rendering evidence](qa/diagram-render.json) records dimensions and source/output hashes; [syntax evidence](qa/mermaid-syntax.json) records the parser version and source hashes. The initial nine diagrams and the revised/new figures were visually inspected. This establishes the tested Mermaid/SVG paths, not compatibility with an untested installed Obsidian version.

## Source layout

| Path | Responsibility |
| --- | --- |
| `app/src/shell.html` | Semantic application shell and bundle markers |
| `app/src/styles.css` | Layout, visual states, responsive behavior, and focus styling |
| `app/src/mock-data.js` | Normalized fictional observations and scenario progression |
| `app/src/model.js` | Scoped joins, projections, summary resolution, snapshots, and exports |
| `app/src/app.js` | Views, filters, replay, dialogs, inspection, and downloads |
| `app/build.py` | Deterministic standard-library bundler |
| `app/tests/model.test.cjs` | Behavioral model tests |
| `app/tests/ui.test.cjs` | Rendered-control, source-inspector, persistence and retained-view regressions |
| `app/tests/fixtures/legacy-state-v1.json` | Original saved capture used to verify backward readability |
| `tools/render-diagrams.mjs` | Pele SVG generation with accessible titles |
| `tools/check-mermaid.mjs` | Independent Mermaid syntax and negative-control checks |
| `tools/check_native_api.py` | Pinned operation/schema/transport comparison |
| `tools/check_fixture_schema.py` | Strict authoring validation of raw synthetic native envelopes |
| `tools/check.py` | YAML, links, all diagram copies, SVG hashes and exact generated-page parity |
| `qa/` | Hash-bound API, fixture and diagram evidence plus browser screenshots |
| `diagrams/manifest.json` | Ten-diagram registry |

## Production integration boundary

This is a functional, read-oriented UI prototype over synthetic observations. Its `DemoModel` is an in-process JavaScript API. The native AWS API catalog and proposed backend HTTP routes are separate contracts; no backend endpoint or stream server is implemented here. A production implementation would supply authorized collectors; section-specific collection attempts and coverage; optional EventBridge/A2A adapters; principal-sensitive caching; retained source/projection storage; stable pagination and stream recovery; and a server-owned snapshot store. Those integration contracts and unresolved payload questions are documented in the report and UI annex.

Browser-local snapshots and hashes do not authenticate AWS origin, enforce retention or prevent tampering. The current model has no multi-tab write coordination, and the rich fixture profiles are not generic parsers for arbitrary AWS journals. The [quality review](QUALITY_REVIEW.md) states the remaining evidence gates without treating prototype tests as production certification.

The implementation intentionally preserves raw content for unfamiliar journal types and demonstrates that an investigation can finish while an exact result is still being retrieved. These are useful foundations for reviewing the information architecture before connecting a real AWS account.
