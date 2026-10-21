# Changes

## 0.2.0 — 21 October 2026

Added interactive metric charts across evidence, scenarios, executions, validations, reports, workspace counts and numeric inspection facts. Added an optional, bounded timestamped-sample extension that preserves legacy evidence hashes and does not alter scalar evaluation. Added explicit gaps, event markers, per-series provenance, keyboard inspection, zoom, CSV export and standalone interactive report export.

Added a 32-metric catalogue, reproducible synthetic examples, a proposed Grafana dashboard with 33 graph panels, provisioning examples and sample Prometheus recording rules. These are not live telemetry integrations. Generated UI/schema/dashboard files are built from tracked sources; release bundles include the outputs.

The next acceptance gate is unchanged: connect an approved real AWS account and local runtime, verify bounded inspection and persistence, then implement and qualify incident telemetry collection. No fault execution or operational-readiness certification was added.
