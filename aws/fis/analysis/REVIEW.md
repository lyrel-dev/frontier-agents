# AWS FIS model review

**Reviewed:** 5 November 2026

**Status:** complete; suitable as the initial logical model for a mock operator UI

**Reviewed source:** the original 21-page analysis, its five Mermaid sources, current official AWS response/operation documentation, and repository authoring guidance

**Maintained repository source:** [report.md](report.md) and [diagrams/](diagrams/)

## Review conclusion

The initial model correctly separates catalog Action, named template step, and named action execution. It preserves the run configuration snapshot and differentiates selected resources, execution state, workload assessment, and report readiness. No blocking API-semantic defect was found in those core choices.

The reviewed source makes the following refinements explicit. These are model/provenance clarifications, not claims that AWS changed its service behavior.

| ID | Finding | Resolution |
| --- | --- | --- |
| R01 | The original evidence diagram represented the scope lever as optional while also saying cardinalities described the logical domain. An unloaded cache row is not resource nonexistence. | The diagram now uses one SafetyLever per AWS_SCOPE. Unknown/unloaded lever state stays an observation condition. AWS documents one lever per account/Region. |
| R02 | Directly attaching AlarmObservation to StopCondition could imply a condition owns alarm state or prevent one alarm from being shared across runs. | Added the external CloudWatchAlarm identity. A condition may reference an alarm; an alarm has timestamped observations. `source=none` has no alarm relation. |
| R03 | Broad “coverage” terminology can conceal different guarantees. | Explicitly distinguish configured actions, selected memberships, observed starts/completions, verified fault effects, and verified recovery. |
| R04 | A terminal-step fraction needs a complete denominator and unknown-state policy. | Compute only with sufficient detail; keep unknown states, handle zero/absent denominators, and never force a terminal run's missing steps to completed. |
| R05 | A conditional path-duration estimate could be misread as a guaranteed lower bound or ETA. | State duration-adapter and normal-execution assumptions; skips, early stops, timeouts, preparation, and post actions qualify it. |
| R06 | A hash or separately fetched description could be mistaken for an AWS template revision/snapshot field. | Label fingerprints as application metadata and separately captured template metadata with observation time. Keep mutable tags distinct where history matters. |
| R07 | Returned experiment options are broader than update inputs. | Document that UpdateExperimentTemplate's current options input exposes emptyTargetResolutionMode; accountTargeting must not be offered as that update operation's field. |
| R08 | Report completion, artifact access, and experiment completion can be conflated. | Preserve report state separately, keep artifacts as a collection, retain open reportType strings, and avoid invented report times/download URLs. |
| R09 | Source examples do not all list the newest statuses. | Use current API vocabularies as known values and retain unknown raw strings; examples are not treated as a closed schema. |
| R10 | Retention wording specifically enumerates stopped/completed/failed runs. | Preserve that exact scope; recommend archiving all run types without asserting undocumented cancelled-run retention. |

Primary sources for the refinements are the [safety lever guide](https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html), [stop-condition shape](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentStopCondition.html), [action sequencing guide](https://docs.aws.amazon.com/fis/latest/userguide/action-sequence.html), [update-options shape](https://docs.aws.amazon.com/fis/latest/APIReference/API_UpdateExperimentTemplateExperimentOptionsInput.html), [report state](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentReportState.html), and [lifecycle/retention guide](https://docs.aws.amazon.com/fis/latest/userguide/view-experiment-progress.html). The complete source register is [sources.json](sources.json).

## Confirmed API boundaries

- ExperimentAction has no independent execution ID/ARN, structured error object, generic result payload, percentage complete, or universal per-resource result.
- The action map key is the execution name. `actionId` selects the catalog capability, and dependencies reference names.
- Resolved target records provide a resource type and generic information map; canonical resource identity is optional application normalization.
- List summaries require GetExperiment hydration. Missing summary fields must not erase known detail.
- EventBridge is an experiment-state notification source; it is not a generic action-state stream.
- The FIS log `id` is the experiment ID. Event deduplication needs source record identity/location.
- The runtime response is current state. Exact historical transitions require appropriate evidence; poll time is observation time.
- StopExperiment is a stop request despite using HTTP DELETE. There is no individual runtime-action retry/pause/stop/update API.
- Experiment-level error can represent only the first failed action. Reasons and most error codes must not be parsed as stable automation contracts.
- A preview does not validate fault permissions or prove the selected set will match a subsequent run.

## Repository boundaries

No AGENTS.md was present in the inspected checkout. README.md, SCOPE.md, AUTHORING.md, and EDITORIAL_STANDARD.md describe the existing agent-guide compiler and frozen registry boundaries. The user explicitly requested the new FIS analysis path. This package therefore remains self-contained there, with a source Markdown report and no edits to generated guide content or approved records.

## Documentation validation

- Compared the complete Experiment and ExperimentAction inventories to the official shapes.
- Checked action metadata, target-account fields, safety-lever vocabulary, list/detail differences, and the template update-options restriction.
- Reviewed identity, relationship multiplicity, missing-data handling, evidence time semantics, and derived-measure assumptions.
- Synchronized all five embedded Mermaid blocks with their standalone `.mmd` files byte-for-byte.
- Verified the source register has unique IDs/URLs and that all citations in the report resolve to it.

These checks establish documentation/model consistency. Browser interactions and application tests are a separate verification activity. No live AWS experiment was run, stopped, or modified during the model review.

## Rendered report and diagrams

The reviewed report is delivered as self-contained Markdown and a matching 27-page PDF. All five diagrams are embedded in both forms and have standalone Mermaid and accessible SVG sources. The SVG/PDF renderer parses the canonical entity attributes, relationships, and cardinalities; the rendered multiplicities use `1`, `0..1`, `1..N`, and `0..N` labels.

All 27 PDF pages were rendered for layout review. Detailed inspection covered every diagram and the Experiment field inventory, including the revised CloudWatchAlarm relationship and the scope's one SafetyLever. Checks verified diagram parity, source-reference resolution, SVG XML validity, and PDF text extraction. [`tools/README.md`](tools/README.md) documents regeneration and validation, and [`tools/render-manifest.json`](tools/render-manifest.json) records input/output hashes. The renderer fails on stale embedded diagram content or a divergent source register.
