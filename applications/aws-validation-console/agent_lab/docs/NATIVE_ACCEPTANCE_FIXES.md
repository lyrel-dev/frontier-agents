# Native acceptance corrections — 23 October 2026

This record describes corrections discovered by hosted acceptance of 0.5.1-dev. It does not assert a passing final run; the current commit's generated `validation/software-acceptance.json` is the source for measured results.

## Catalogue refresh

A pending refresh could recreate blank search/scope inputs after returning from guided setup. The SPA now retains these filters in memory, restores the active input's keyboard focus, and does not remount an active setup workflow when an earlier catalogue request returns. Locking clears this state. Delayed-response regressions exercise the actual native page.

## Guided setup

Changing a stage used to leave its old editable form present while asynchronous account/contract reads were in progress. A user could fill the old form, then lose those values when the response rendered a new form. Navigation now clears stale controls immediately, renders a loading state, and uses a navigation generation to reject obsolete responses. Delayed-read tests assert both unavailable stale fields and the loaded current form. Browser test polling uses automation-protocol evaluation without enabling `unsafe-eval`; the served CSP is unchanged.

## Telemetry integration harness

The telemetry suite uses real console, Prometheus and Grafana containers on an isolated Docker network. Its control HTTP requests now originate inside that network instead of assuming a host route through an internal-only Docker network. They exercise the actual HTTP servers, bearer authentication, Prometheus scrape/query and Grafana datasource/query APIs, not mocked responses. The separate container suite verifies host loopback publication.

The only workload sample fixture is constructed by this test in a disposable volume from actual loopback request timings. Its cloud/agent identities and business requirement are explicitly test-only. It is not distributed runtime data and cannot establish AWS agent effectiveness. Failure diagnostics retain bounded, token-redacted container logs before removing only resources owned by the harness.

## Publication and limits

Temporary write-enabled source-integration workflows have been removed. The retained acceptance workflow has read-only repository permissions and no AWS credentials. It independently runs all suites, retains failures, and requires current-run evidence; a failure cannot be hidden by an older report. Source acceptance does not close live AWS, IAM, incident-delivery, diagnosis, prevention or production-safety requirements.
