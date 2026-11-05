---
title: AWS DevOps Agent investigation prototype — validation record
date: '2026-11-05'
type: validation-record
status: adversarially-reviewed-prototype
tags:
  - aws/devops-agent
  - prototype
  - validation
---

# Validation record

This record distinguishes reviewed AWS contracts, synthetic model behavior, diagram readability, and browser interactions. The application uses fictional data and performs no live AWS requests. [QUALITY_REVIEW.md](QUALITY_REVIEW.md) records the current adversarial findings; [REVIEW.md](REVIEW.md) preserves the narrower initial review. All results below are local executions or explicitly identified browser observations, not a remote CI or live-service run.

## Model semantics

Command, run from this `analysis` directory:

```bash
node --test app/tests/*.test.cjs
```

**Result: 42 tests passed, 0 failed: 33 model tests and 9 rendered-UI/control tests.** The initial edition had 16 model tests. The added regressions use counterexamples that the original fixed scenario did not exercise.

| Check | Verified behavior |
| --- | --- |
| Counting units | Task, execution, journal, artifact, and coverage counts agree with their own collections. |
| Scope | Identical execution/record IDs in different Agent Spaces do not join across scopes. |
| Membership | Native execution bodies contain no fabricated task ID; listing context supplies membership. |
| State separation | Task completion, stopped executions, and summary readiness remain independent. |
| Exact summary selection | An event-referenced summary is selected instead of a newer same-type candidate. |
| Resume and history | The same task resumes with new observations while retained captures remain unchanged. |
| Partial captures | Snapshots retain gaps and separate capture time from collection time. |
| Unknown content | Array and null journal content remain valid and inspectable. |
| Coverage | Exhausted journal pagination can coexist with missing external diagnostics. |
| Query identity | Retained read queries use the actual native Agent Space ID. |
| Revision stability | Equivalent source and projection payloads keep stable revision identities. |
| Hashes | Source/projection canonical-JSON hashes and downloadable UTF-8 file hashes agree with independent Node SHA-256 calculations. |
| Graph attribution | Edges have source references and distinguish the supported pool-contention hypothesis from the unsupported database-saturation alternative. |
| Clocks | Publication, observation, execution, and metric-sample times are coherent. |
| Metrics | Only available source points, units, windows, and sourced thresholds feed charts. |
| Serialization | Detached views and exports rehydrate through the model API; the pinned asset version remains stable. |

### Adversarial regressions

| Boundary challenged | Verified behavior |
| --- | --- |
| Exact displayed provenance | Current and historical Task cards and inspectors resolve the displayed revision, not the first collected Task. |
| Task identity | Repeated task IDs in different Agent Spaces cannot cross-select derived items or snapshots; ambiguous bare IDs fail. |
| Opaque key components | Delimiter-containing execution/record IDs cannot produce the same compound key. |
| Duplicate collection | Repeated execution memberships and record observations preserve logical counts while retaining observation/revision evidence. |
| Changed/re-observed records | Current selection and metric joins follow the retained record lineage. |
| Result phase | Investigation and mitigation candidates/pointers remain separate; an unrelated lifecycle event cannot erase an earlier completed result. |
| Conflicting result references | Equal-time conflicting completion pointers remain unresolved independent of arrival order. |
| Missing or malformed reference | Not observed, omitted, unusable and exact references remain machine-readable distinct states; malformed supplied IDs are not treated as omission. |
| Open JSON | Object, array, scalar, boolean and null summary content remains escaped JSON with matching artifact media type, not fabricated Markdown. |
| Candidate rendering | The rendered candidate body and inspector use the actual unselected summary, not an unrelated finding. |
| Source lookup | Inherited JavaScript property names cannot masquerade as source observations. |
| Saved-state integrity | Incomplete captures, scope mismatches, changed bodies, invalid counters and duplicate identities are rejected; corrupt browser data is retained for recovery. |
| Legacy state | A checked-in original schema-1 capture remains readable without rewriting its retained content. |
| Technical live failure | Model/export and the already selected historical UI survive unavailable current-view and portfolio assembly; comparison is explicitly unavailable. |
| Historical stability | Exported captured content stays byte-stable as live observations advance; derived-only changes still appear in live comparison. |
| Hash encoding | Independent SHA-256 agrees with `sorted-json-utf8/v1`, including lexical ordering of numeric-looking property names. |
| Bounded coverage | Header and History comparison use bounded labels, including legacy-label and missing-label fallbacks; unavailable live data stays unavailable. |
| Persistence failure | A visible session-only notice remains present on narrow layouts; invalid stored state is not overwritten by routine persistence. |

The initial read-only review also checked **3 EventBridge notifications** and all **18 task/stage combinations**. Those observations validate synthetic examples, not service delivery guarantees. The 46 native-shaped objects now also have the repeatable schema gate below. The UI tests exercise rendered HTML and delegated handlers in a controlled document stub; browser layout, actual keyboard focus and CSS behavior are reviewed separately.

## Repeatable API and fixture checks

The executed commands used the locally downloaded, checksum-verified Botocore model:

```bash
python3 tools/check_native_api.py --model /path/to/service-2.json --self-test
python3 tools/check_fixture_schema.py --model /path/to/service-2.json --self-test
```

For independent reproduction, substitute `--fetch` for `--model /path/to/service-2.json`. This downloads the exact immutable pin; it does not silently track an evolving SDK branch.

| Audit | Executed result and boundary |
| --- | --- |
| Native operation/schema comparison | 63 methods/routes/top-level response lists; all 63 endpoint-prefix/success/error bindings; 19 request and 52 selected schema tables; 339 expanded member rows passed. |
| API negative controls | All 9 deliberate corruptions were rejected: route, requiredness, type, enum, page limit, endpoint, success code, error and union. An unexpected model checksum also fails closed. |
| Raw synthetic envelopes | 46 objects passed: 7 Task, 12 Execution, 24 JournalRecord, 2 Asset, 1 AssetFile; 23 modeled shapes reached. |
| Fixture controls | All 8 invalid examples were rejected; all 6 open-JSON kinds were accepted. Binary asset content is not exercised by this text fixture. |
| Evidence binding | Audit evidence records model, tool, catalog/fixture and derived-output hashes. It is not a signed attestation or a live AWS capture. |

The API inventory includes all **560 shape names**, not expanded semantic verification of every shape. Strict fixture enum/constraint checks ensure the authored example matches the pin; they must not be copied into production output deserialization as rejection of unknown values. The evidence and tool contracts are documented in the [source register](annexes/Investigation_API_Sources.md), [native audit](qa/native-api-audit.json), [inventory](qa/native-api-inventory.json) and [fixture audit](qa/fixture-schema-audit.json).

## Diagrams

All **ten** Mermaid sources render using pinned **Pele 1.6.0**. An independent gate using **Mermaid 11.12.2** with **JSDOM 26.1.0** parses all ten sources and rejects a deliberately invalid ER relationship. Each generated SVG is valid XML with an accessible title and positive bounds. Each canonical source has exact corresponding Mermaid fences in [report.md](report.md) and its relevant annex; all **20 published copies** are checked.

The initial nine diagrams were inspected individually at full resolution. In this follow-up, revised D02, D03 and U03 and new D07 were inspected in the browser for label readability, clipping, cardinalities, arrow direction and layout. D07 has three entities across its widest rank; the reconciliation sequence has four participants. No overlapping or clipped labels were found in these inspected outputs. [Rendering evidence](qa/diagram-render.json) records source/output hashes and dimensions; [syntax evidence](qa/mermaid-syntax.json) records the independent parser and source hashes. Neither test claims a particular installed Obsidian release or theme was exercised.

## Package and build

The standard-library application build embeds its scripts, styles, mock observations and ten SVGs into `index.html`. No external script, stylesheet, image, or network data dependency is needed to run the application. Documentation links require the adjacent files.

```bash
python3 app/build.py
python3 -m pip install -r tools/requirements.txt
python3 tools/check.py
node --check app/src/app.js
node tools/check-mermaid.mjs
```

The package gate compares `index.html` byte-for-byte with a fresh in-memory build, so stale generated output fails. It parses YAML using pinned PyYAML, checks local Markdown targets, rejects missing/duplicate/undeclared or divergent diagram publications, verifies source/SVG hashes, and checks embedded resources and offline runtime constraints. The link checker excludes inline and fenced code so API regular expressions are not mistaken for Markdown links. Reproduction commands and dependencies are in [README.md](README.md).

The final package gate passed: ten source/SVG pairs, twenty matching Markdown diagram copies, parsed metadata, resolved local Markdown targets and a current deterministic offline bundle. JavaScript syntax and `git diff --check` also passed.

## Browser review

Browser review uses the generated application through the managed Chrome preview. Desktop layout and a 390-pixel-wide iframe viewport are reviewed separately; the latter is a CSS responsive-layout check, not physical-device testing.

[Current review screenshot](qa/quality-review-workspace.png) shows the revised application and retained/live distinction. The [initial screenshot](qa/investigation-workspace.png) is preserved as evidence of the earlier edition.

### Focused follow-up browser review

| Interaction | Observed result |
| --- | --- |
| Current Task source | At completed stage, the lifecycle card opened native Task version 9 and its exact source hash; the original Executions source control remains available. |
| Candidate | The candidate panel showed `summary-draft-01` and its actual preliminary-summary text; source inspection opened the same record. |
| Focus after replay | Advancing to the pending-result stage retained focus on Next rather than losing it during rerender. |
| Retained source after resume | Live Task advanced to version 10 with 16 records; the retained view opened completed version 9 with 14 records and its original source. |
| Coverage wording | Header and History table show bounded known-gap wording; the table's remaining raw `complete` label was corrected during this pass. |
| Revised diagram gallery | All ten figures are registered; revised D02/D03/U03 and new D07 display legibly. Fit control retained focus. |
| Mobile modal | At 390 × 844 CSS pixels, opening the drawer exposed dialog/modal semantics and focused search. Tab from its last action wrapped to Close. Escape restored the menu-button focus; background content was absent from the active accessibility tree. |
| Mobile width | Responsive document width and scroll width both measured 375 CSS pixels after the scrollbar: no horizontal page overflow in the observed overview. |
| Storage unavailable | A sandboxed `allow-scripts` iframe, without same-origin storage access, displayed a visible **Session-only changes** notice. The notice fit the same narrow viewport with no page overflow. |
| Application console | No application-origin errors or warnings were observed in the captured desktop, narrow-layout or storage-unavailable logs. Browser-extension metadata errors were excluded and were not attributed to the application. |

The retained-view outage path is exercised by the Node UI regression with current-view and portfolio functions both failing. It was not a real network outage or an AWS outage experiment. Automatic startup recovery with no selected snapshot remains outside this implemented path.

The [storage-unavailable screenshot](qa/quality-review-storage-mobile.png) retains the observed narrow-layout notice. The sandbox harness is a manual browser fault condition; it does not demonstrate storage quota behavior in every browser.

### Initial browser review retained for traceability

The following observations belong to the first package review. The focused follow-up above revisited changed behavior; it did not repeat every initial interaction.

| Interaction | Observed result |
| --- | --- |
| Desktop overview | Readable queue, replay controls, independent lifecycle/result/record/coverage indicators, activity, findings, and metric chart. |
| Timeline filtering/search | Incident evidence narrowed five initial entries to three; searching release returned one entry. |
| Timeline provenance | Drilldown showed event, record, and collection clocks, source revision, scoped identity, exact raw JSON, and read context. |
| Evidence inspection | The database-saturation alternative showed its unsupported disposition and exact published sources; relationship inspection retained attribution. |
| Completion before result | Stage 3 showed native task completed with 11 records and the exact summary still pending. |
| Summary arrival | Stage 4 selected `summary-final-02` with 14 records; all three summary candidates remained in the journal. |
| Snapshot capture and resume | Manual capture retained 14 records and completed task version 9; resumed live view had 16 records and active version 10. The comparison and new-activity banner showed the difference. |
| Snapshot export | The actual browser-downloaded JSON parsed successfully: synthetic flag, completed task, snapshot-002, 14 records, and 26 retained sources. |
| Previous result | Resumed view labeled the retained summary as the previous completed result. |
| Denied artifact | Trace reference remained inspectable, with access denied and no invented content/download. |
| Pinned attachment | Version 3 content and its provenance were shown. The actual downloaded file was 472 UTF-8 bytes and matched the displayed SHA-256. |
| Journal type filter | Selecting `demo.future_profile.v9` returned the unknown array record, whose raw content remained intact. |
| Investigation search | Searching supplier narrowed the queue and opened the intended case. |
| Timed-out investigation | Showed no summary available, retained evidence, stale observation, and explicit evidence gaps. |
| Diagram gallery | All nine diagrams displayed with the expected titles; enlargement, fit, Mermaid-source disclosure, and SVG download worked. The downloaded U01 SVG was byte-identical to the reviewed file. |
| Narrow layout | A 390-pixel iframe displayed the overview and source inspector without horizontal page overflow; content width and scroll width both measured 375 pixels after the scrollbar. |
| Mobile keyboard navigation | The closed drawer was absent from the accessibility tree. Opening focused search; Escape closed it and restored menu focus. Selecting another investigation closed the drawer and displayed that investigation. |
| Completed secondary case | The ledger case showed its completed task, exact selected result, retained records, stale collection observation, and historical worker-retry metric with source references. |
| Replay controls | Play and Pause worked; automatic replay reached the final follow-up stage with 18 records and no running executions. |
| Reset confirmation | Cancel retained the completed stage and two snapshots; confirmation restored stage 1, six records, and zero snapshots. |
| Browser logs | No application-origin error or warning appeared in the captured desktop console log. The review environment emitted browser-extension metadata errors, separate from the application. |

### Corrections found during the initial review

The implemented fixes separate terminal/no-summary wording from ongoing investigation, identify the previous result after resumption, match summary source inspection by execution and record ID, align Overview ordering with its displayed collection clock, distinguish journal pagination from broader evidence gaps, clarify file-versus-JSON hashes, and retain keyboard focus when source inspectors change. Interactive graph labels were enlarged and darkened; long relationships route through clear space. The closed mobile drawer is hidden from focus and accessibility navigation; its open/close actions manage keyboard focus.

## Limits

Validation establishes the stated static comparisons and tested behavior of this offline prototype. It does not establish live AWS authorization, pagination under concurrent updates, actual journal profiles, stream delivery, A2A payloads, backend persistence, production snapshot consistency or a deployed HTTP API. Targeted text contrast was improved, but no full WCAG audit, physical-device test or installed-Obsidian certification is claimed. Browser-local hashes/freezing do not enforce authenticity, access, retention or multi-tab coordination. The future capture scenarios remain in the [UI contract](annexes/Investigation_UI_Contract.md).
