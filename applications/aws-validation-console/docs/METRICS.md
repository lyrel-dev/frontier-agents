# Metric graphs and the proposed Grafana dashboard

Version 0.2.1. The console can now display recorded metric samples. It still does **not** collect workload telemetry, execute a Prometheus/CloudWatch query, inject a fault, or establish operational readiness from a graph.

## What is graphed

Every catalogue metric and every metric found in imported evidence or scenario assertions receives a chart. The initial catalogue contains 32 metrics across customer impact, incident response/recovery, data/dependencies, capacity/saturation and operational evidence. Custom metric identifiers and units are discovered without modifying the chart code.

Graphs also appear beside workspace counts, in inventory, in numeric resource-fact details, and in scenario, execution, evidence, validation and report details. A count observed once is a **single point**, not a fabricated trend. Snapshot graphs are partitioned by connection, scope and simulation status; a reused connection name cannot combine accounts or relabel example observations as measured data. Numeric configuration facts are labelled as configuration/runtime observations, not performance measurements. A denied collection scope is missing data, not zero resources.

Controls: mouse hover, arrow-key sample inspection, Home/End, plus/minus zoom, horizontal drag-selection, reset range, legend isolation, sample tables and raw CSV export. Metric filters select group, text, scope, execution, deployment applicability, evidence presence and an absolute UTC interval. Independent scopes and runs are never averaged together. Deployment filtering uses the scenario's declared applicability, not inferred runtime identity.

The **Synthetic graph example** dataset is separate from the workspace. Viewing it does not import it or connect anything. Download and explicitly import `examples/metrics-series.json` to exercise persistence and evaluation with those fictional records. All records remain `simulated: true`.

## Optional evidence extension

The existing `evidence.data.value` remains the scalar evaluated against a scenario assertion. An evidence record may additionally contain:

```json
"series": {
  "description": "10-second request-error ratios; summary uses the full run population",
  "expected_interval_seconds": 10,
  "points": [
    {"at": "2026-10-21T10:00:00Z", "value": 0.002},
    {"at": "2026-10-21T10:00:10Z", "value": null},
    {"at": "2026-10-21T10:00:20Z", "value": 0.008}
  ],
  "events": [
    {"at": "2026-10-21T10:00:10Z", "kind": "fault_start", "label": "Confirmed fault start"}
  ]
}
```

This is a fragment inside a complete evidence record, not an importable bundle by itself. The build generates a complete example and an updated JSON schema.

Samples use the **same unit** as the evidence summary. Timestamps must be timezone-aware, strictly increasing and inside the evidence window. Values must be finite numeric values, booleans matching a boolean summary, or `null`. Duplicate timestamps, unknown fields, out-of-window events, invalid types and more than 20,000 points per record are rejected by the backend. The existing 5 MiB import limit remains.

`sample_count` still describes the scalar's measurement population; it is not the number of chart points. For example, 10,000 requests can produce ninety 10-second chart windows. The evaluator does not recompute a percentile, weighted ratio or recovery duration from the chart. A contradictory series and scalar require source reconciliation; visual appearance cannot override the scalar decision.

The extension is additive to the 1.0 bundle envelope. Version 0.1 clients do not accept it. Absent `series` fields are omitted on serialization, preserving legacy normalized records and hashes. To add samples to an existing immutable evidence record, create a **new revision** and explicitly recompute a validation using that revision. Do not overwrite a prior record or silently select the latest revision.

## Missing data, thresholds and provenance

A `null` point breaks the line. When an expected cadence is supplied, a gap exceeding 1.5 times that cadence also breaks it. Without a cadence, only explicitly supplied nulls establish gaps. Isolated summaries are never joined into a telemetry line. The last sample is labelled as recorded, not live; a trailing null remains “No sample”. The multi-series header reports the number of series rather than choosing a value from an arbitrary scope.

Long segments are visually reduced using bucket extrema and endpoints. No points are removed from storage or CSV; the on-screen table shows the first 200 rows. Zooming renders the selected range from the stored points. A scalar threshold overlay is labelled as a **whole-window requirement**, not a pointwise decision. The Metrics view suppresses threshold overlays when the visible metric spans different scenario revisions.

Validation and report graphs use only explicitly linked evidence whose stored digest matches the validation's pinned input hash. Missing or mismatched inputs are omitted. Hashes detect altered content; they do not authenticate the producer. Graphs cannot upgrade missing or imported evidence into a passing result.

The UI's **Download HTML report** produces a standalone interactive report with pinned charts, embedded data, a restrictive nonce-based CSP and no network calls. The existing backend HTML endpoint remains an inert summary for API consumers. Exported HTML includes the report origin and content hash, the validation origin, and a warning when the report or validation was imported or supplied as an example. Workspace bundles and report HTML can contain sensitive identifiers and source text; review them before sharing.

## Grafana import

Run `python build_ui.py`, then import `grafana/operational-readiness.json` in your Grafana installation. Select a Prometheus data source using the dashboard's **Prometheus** variable. The file uses Grafana's Classic JSON model, 32 time-series metric panels and an additional source-observation-age panel. It includes no universal passing thresholds or alert rules.

The dashboard filters are `environment`, `service`, `deployment_model`, `scenario`, `run_id`, and `data_kind`. The provenance selector defaults to **measured**; use **synthetic** only with an explicitly separate demonstration source. Metric panels preserve series labels rather than aggregating across selected runs. Every panel legend retains all six scope/provenance labels. Grafana supplies zoom, shared crosshair, query inspection, legend isolation and panel-data export.

The datasource and dashboard provisioning examples are under `grafana/provisioning/`. Set `READINESS_PROMETHEUS_URL` to the endpoint reachable **from Grafana**, and mount the generated JSON under `/var/lib/grafana/dashboards/readiness`. Set the datasource scrape interval to the actual interval. Keep service authentication, TLS, volume retention and access controls in your deployment configuration; no credentials are included here. The console neither embeds Grafana nor opens a new unauthenticated metrics endpoint.

## Required instrumentation contract

All `readiness_*` names are **proposed normalized metrics**, not AWS/FIS built-ins or existing console exports. Your collector/recording rules must produce them. Each measurement family must have these labels:

| Label | Contract |
|---|---|
| `environment`, `service` | Stable, non-secret scope identifiers. |
| `deployment_model` | `ec2`, `eks-ec2`, `eks-fargate`, `ecs-ec2`, `ecs-fargate`, `lambda`, `docker`, `podman` or `kubernetes`. |
| `scenario` | Versioned scenario identity used for the measurement. |
| `run_id` | Bounded test-execution identity, not a user/session/request ID. |
| `data_kind` | Exactly `measured` or `synthetic`; never silently relabel examples. |

Emit `readiness_run_info{...} 1` for variable discovery. Each catalogue entry supplies its exact gauge name, unit, description and PromQL selector in `grafana/metric-catalogue.json`. Emit `readiness_observed_timestamp_seconds{...,metric="request_error_ratio"}` containing the **source measurement-window end**, not scrape time. The observation-age panel detects a recent scrape of an old measurement. Retire obsolete gauges and use an explicit stale-data policy; a present time series is not proof of fresh evidence.

Do not apply `rate()` to the normalized gauges. `grafana/recording-rules.example.yaml` shows reset-aware request rates, matching-population error ratios and p95/p99 calculations from histogram buckets. It is an **instrumentation example** and requires the named source counters/histogram. A 5-minute rule window must be chosen deliberately for the incident duration and scrape interval; it can smooth a short outage. Use Grafana's `$__rate_interval` for ad hoc counter queries. Do not average per-instance percentiles, replace absent data with zero, or create a success ratio from a zero denominator.

Resource metrics may originate in CloudWatch, Container Insights or local exporters, but their denominators must be normalized explicitly. Incident durations require attributable event pairs; FIS completion cannot establish detection, acknowledgement, mitigation or stable recovery. Data-loss and duplicate-effect metrics require transaction reconciliation. Automatic recovery success is a defined **cohort** ratio, not a one-run latency graph.

`run_id` increases cardinality. Limit retention and active runs, avoid customer identifiers in labels, and retain long-term raw evidence in the local workspace instead of expanding production application label sets indefinitely. A collector adapter must be accepted for each deployment model; labelling a scenario as applicable does not implement that adapter.

## Verification boundary and references

The 0.2.0 baseline is retained in `validation/metrics-validation.json`. Publication acceptance adds native loopback/file browser navigation, an unprivileged container build with persistence across replacement, and Grafana JSON import/readback. Measured results and the tested Grafana version are in `validation/publication-review.json`.

These checks do not inspect an actual AWS account or Docker/Podman/Kubernetes target, execute proposed PromQL, test datasource provisioning against real telemetry, or validate incident recovery. The container test exercises hosting and storage, not runtime inspection. Native navigation is unavailable in the local authoring sandbox; that suite runs without a bridge in GitHub Actions.


Primary documentation reviewed on 21 October 2026:

- [Grafana time-series panels](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/time-series/)
- [Grafana JSON models](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/view-dashboard-json-model/)
- [Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Prometheus template variables](https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/)
- [PromQL functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [Histogram aggregation](https://prometheus.io/docs/practices/histograms/)
