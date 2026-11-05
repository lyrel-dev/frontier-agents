---
title: AWS DevOps Agent investigation prototype — validation record
date: '2026-11-05'
type: validation-record
status: verified-prototype
tags:
  - aws/devops-agent
  - prototype
  - validation
---

# Validation record

This record distinguishes reviewed AWS contracts, synthetic model behavior, diagram readability, and browser interactions. The application uses fictional data and performs no live AWS requests. [REVIEW.md](REVIEW.md) contains the independent documentation and fixture review.

## Model semantics

Command, run from this `analysis` directory:

```bash
node --test app/tests/model.test.cjs
```

**Result: 16 tests passed, 0 failed.**

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

An independent read-only review also checked **46 native-shaped fixture objects**, **3 EventBridge notifications**, and all **18 task/stage combinations**. These checks validate a synthetic contract example, not actual service delivery guarantees.

## Diagrams

All nine Mermaid sources parse and render using the pinned **Pele 1.6.0** renderer. Each generated SVG is valid XML with an accessible title and positive bounds. Each source has an exact corresponding Mermaid fence in [report.md](report.md).

All nine diagrams were inspected individually at full resolution for label readability, clipping, cardinalities, arrow direction, and layout. The ERDs have at most two entities across; the reconciliation sequence has four participants. No overlapping or clipped labels were found. [qa/diagram-render.json](qa/diagram-render.json) records reproducible source/output SHA-256 hashes and dimensions.

## Package and build

The standard-library application build embeds four scripts, styles, mock observations, and nine SVGs into `index.html`. No external script, stylesheet, image, or network data dependency is needed to run the application. Documentation links require the adjacent files.

```bash
python3 app/build.py
python3 tools/check.py
node --check app/src/app.js
```

The application was rebuilt from the final source and produced the same bytes. Local Markdown references, parsed YAML frontmatter, Mermaid/source/SVG correspondence, embedded resources, and JavaScript syntax passed verification before commit. The link checker excludes inline and fenced code so API regular expressions are not mistaken for Markdown links.

## Browser review

Browser review uses the generated application through the managed Chrome preview. Desktop layout and a 390-pixel-wide iframe viewport are reviewed separately; the latter is a CSS responsive-layout check, not physical-device testing.

[Reviewed application screenshot](qa/investigation-workspace.png) shows the checkout scenario at the evidence-correlation stage with separate lifecycle, result, record, and coverage indicators.

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

### Corrections found during review

The implemented fixes separate terminal/no-summary wording from ongoing investigation, identify the previous result after resumption, match summary source inspection by execution and record ID, align Overview ordering with its displayed collection clock, distinguish journal pagination from broader evidence gaps, clarify file-versus-JSON hashes, and retain keyboard focus when source inspectors change. Interactive graph labels were enlarged and darkened; long relationships route through clear space. The closed mobile drawer is hidden from focus and accessibility navigation; its open/close actions manage keyboard focus.

## Limits

Validation establishes the reviewed static model and the behavior of this offline prototype. Live AWS authorization, pagination under concurrent updates, actual journal profiles, stream delivery, A2A payloads, backend persistence, and production snapshot consistency require integration fixtures and account-level testing. The detailed future capture scenarios remain in the [UI contract](annexes/Investigation_UI_Contract.md).
