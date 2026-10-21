# Changelog

## 0.2.1 — publication review

- Fixed in-cluster Kubernetes identity serialization after configuration normalization.
- Removed argument-spread limits from chart extent/range calculations; added a 200,000-sample regression.
- Separated snapshot graphs by connection, scope and simulation status; retained each point reference in CSV.
- Preserved report/validation origin and content hashes in standalone HTML, with imported/example warnings.
- Preserved required-check failures when execution gates remain. Gates still prevent a pass. Evaluators are `scalar-1.1` and `browser-preview-1.1`; saved results are not rewritten.
- Included all scope/provenance labels in Grafana legends and corrected the recovery-point-loss definition.
- Updated image tags and added native-browser, container-persistence and Grafana-import publication checks. See `validation/publication-review.json`.

# Changes

## 0.2.0 — 21 October 2026

Added interactive metric charts across evidence, scenarios, executions, validations, reports, workspace counts and numeric inspection facts. Added an optional, bounded timestamped-sample extension that preserves legacy evidence hashes and does not alter scalar evaluation. Added explicit gaps, event markers, per-series provenance, keyboard inspection, zoom, CSV export and standalone interactive report export.

Added a 32-metric catalogue, reproducible synthetic examples, a proposed Grafana dashboard with 33 graph panels, provisioning examples and sample Prometheus recording rules. These are not live telemetry integrations. Generated UI/schema/dashboard files are built from tracked sources; release bundles include the outputs.

The next acceptance gate is unchanged: connect an approved real AWS account and local runtime, verify bounded inspection and persistence, then implement and qualify incident telemetry collection. No fault execution or operational-readiness certification was added.
