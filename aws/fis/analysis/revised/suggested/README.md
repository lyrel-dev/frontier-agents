---
id: fis-revised-suggested-interface
title: Suggested assessment operator interface
type: interface-guide
service: aws-fis
status: synthetic-prototype
version: "1.0"
created: "2026-11-05"
updated: "2026-11-05"
tags: [aws, fis, assessment, ui, synthetic, workflow]
aliases: [Suggested Assessment Observatory]
related: [../README.md, ../initial/README.md, ../docs/suggested/model.md, ../docs/suggested/api.md, ../docs/suggested/adapters.md, ../VALIDATION.md]
---

# Suggested assessment operator interface

The suggested interface presents the reviewed assessment workflow model through six realistic synthetic runs. Open [index.html](index.html) directly, or use the **Suggested** tab in the [comparison page](../index.html#suggested). The [initial FIS interface](../initial/index.html) remains independently available and appears first in the comparison.

The workspace keeps **execution**, **assessment** and **finalization** visible as separate outcomes. A technically successful run can fail its criteria. A completed query can leave an assessment inconclusive. A finished orchestration record can retain an unknown remote effect and incomplete cleanup.

## Explore the six runs

| Run | Operator question demonstrated |
| --- | --- |
| Checkout · alarm notification | What has been observed so far while a receiver capture and fault experiment are active? Replay advances through later evidence and finalization. |
| Orders · alarm notification | Can the operator trace passing criteria to the observed alarm transition, exact probe receipt and confirmed cleanup? |
| Payments · alarm notification | Why did the notification criterion fail even though execution and cleanup succeeded? The correlated receipt arrives outside the accepted deadline. |
| Inventory · alarm notification | What remains unresolved after a lost start response and cancellation? The external effect stays unknown and the protective hold remains visible. |
| Inventory · logged error budget | Why is a completed Logs Insights query insufficient to establish a passing assessment? The declared source scope lacks adequate coverage. |
| Fulfillment · alarm notification | Why was injection blocked before dispatch? A failed precondition leaves required criteria inconclusive. Diagnostic checks still run with explicitly unavailable observations, and cleanup proves that no injection was dispatched. |

Run names, IDs, accounts, resources, payloads, timestamps and operation results are synthetic. The clock uses fixed fixture timestamps in UTC. Future trace events are simulator instructions; they are excluded from the current observation and exported snapshot.

## Views and controls

**Overview** brings together independent outcomes, the main workflow, the finalization graph, remote effects and the observation timeline. **Steps & attempts** exposes scoped step identity, dependencies, technical outcomes, attempts and external operation references. **Criteria** separates preconditions from the frozen required-criterion denominator and shows actual, expected, reason and cited evidence. **Evidence** supports source and text filters, exact step associations and full provenance details. **Definition** shows the pinned revision, admitted inputs and bindings, dependency locks, source YAML and the three model diagrams.

Search and filters select runs. Replay can play, pause, advance or scrub; each run retains its cursor during navigation. Step and evidence details are available in keyboard-accessible dialogs. **Export snapshot** downloads the current observed projection, including its synthetic provenance, without the future event schedule.

**Simulate cancellation** changes only browser memory. It records local intent and prevents the original future trace from being presented as newly observed provider facts. It does not manufacture a successful stop, an empty result or a new receiver observation. Its labelled 45-second local budget is a demonstration boundary, separate from the pinned workflow's real finalization policy. Reset clears the intervention and restores the original fixture replay. Reload clears all local UI state.

## Implementation boundaries

The interface is buildless HTML/CSS/JavaScript. [fixtures.js](app/fixtures.js) contains synthetic traces and pinned example definitions; [model.js](app/model.js) projects those traces into observed snapshots; [app.js](app/app.js) renders the workspace. The exported snapshot is a presentation DTO for this demo; the proposed HTTP response contract has a separate specification. The [model tests](app/tests/model.test.cjs) cover consequential state and evidence distinctions. Current browser and test results are recorded in [VALIDATION.md](../VALIDATION.md).

The six domain entities are Scenario, ScenarioRevision, Run, StepRun, StepAttempt and Evidence. UI helpers and labels are presentation values. A native FIS experiment is an external operation of an attempt, with native action details belonging to the provider model. The UI does not offer fictional per-action control.

This demonstration does not execute the proposed API, compile CEL, verify real operation packages, authenticate a notification receiver or perform cloud actions. Fixture implementation digests are synthetic labels, as in the reviewed operation catalogue. Receipt evidence is scoped to the explicitly bound probe receiver; it does not establish production consumer processing. See the [model](../docs/suggested/model.md), [API](../docs/suggested/api.md) and [adapter contracts](../docs/suggested/adapters.md) for the full proposed semantics.

## Run the model checks

The test suite requires Node.js and Python 3 with `jsonschema`; Python validates recorded operation DTOs against the retained catalogue schemas. The browser application itself has no runtime dependencies. From the repository root:

```bash
node --test aws/fis/analysis/revised/suggested/app/tests/model.test.cjs
```

For local HTTP serving and the full package checks, follow the [package guide](../README.md).
