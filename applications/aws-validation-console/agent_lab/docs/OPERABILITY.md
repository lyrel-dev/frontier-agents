# Exact-source hosting and telemetry acceptance

## What this iteration changes

`0.5.1-dev` adds a dedicated scrape authorization boundary, worker-aware readiness,
frozen scope labels and an executable console/Prometheus/Grafana integration test.
It does not fabricate an AWS run or close the real response/prevention gates.

### Credential separation

Configure `LAB_METRICS_TOKEN` **or** `LAB_METRICS_TOKEN_FILE` at startup. The value
must differ from both local operational tokens. It authorizes GET `/api/metrics`
and nothing else: no workspace, account setup, backup, dashboard download,
approval, fault start or write route. The secret is never written into SQLite.
A missing scrape token does not create a default credential. Operator access
continues to work for interactive metrics/dashboard exports, but must not be
shared with a monitoring server.

`LAB_ALLOWED_HOSTS` is a comma-separated exact-host list for administrator-approved
internal service names. It rejects wildcards, URLs and ports. The default remains
loopback/local testing names. Proxy headers are not trusted by the launcher.
This setting does not make an internet-facing deployment safe; the application
remains a protected single-operator local service. Use TLS and an independently
reviewed access boundary for traffic beyond a trusted local network.

### Readiness and shutdown

`/healthz` reports process liveness. `/readyz` reports a recently running worker
heartbeat, with a minimum 60-second freshness window (or three poll intervals).
It does not contact AWS or certify the queue/credentials. A stopped, future-dated,
malformed or stale heartbeat returns 503 without account metadata. Evidence can
still be inspected while the worker is stopped. Kubernetes readiness uses this
endpoint; Docker's default image expects the combined worker mode. Host shutdown
grace is 45 seconds, exceeding the launcher's 30-second worker drain budget.

### Frozen measurements

New assessments directly pin the immutable account/Agent Space configuration.
Exports check ownership and these hashes, then label the frozen workload account,
Region/service, Agent Space, template revision, mode, trial and assessment. Changing
current setup cannot relabel earlier results. Invalid scope makes the scrape fail
rather than emit a metric with guessed identity. Older assessments without a direct
binding pin are not rewritten; review and explicitly create a new assessment before
exporting them through this stricter path.

Each Prometheus scrape re-exposes a frozen outcome. It is not a live request counter
or a workload time series. Observation age is a separate metric. A new assessment
has a distinct identity; dashboards must not average unrelated revisions, agents or
workloads. Missing response values are absent, not zero. Business measurements retain
their declared unit and measured account. Labels are intentionally trial-level;
control experiment retention and Prometheus retention for long-running workspaces.

### Acceptance scripts

The permanent read-only CI workflow clears previous generated results and runs:

1. Python/SDK regression tests.
2. Three native HTTP browser suites, with no bridge fallback.
3. Actual loopback HTTP and worker-restart checks.
4. Container isolation, separate configuration approval, replacement persistence,
   backup and graceful shutdown checks.
5. Real console -> Prometheus -> Grafana scrape/query integration on an internal-only
   Docker network, including a dashboard import and a generated PromQL query.

The integration's positive HTTP latency is actually measured. Account/agent/business
metadata is deliberately isolated test-fixture data in a temporary workspace, not
an AWS observation. Runtime images exclude test fixtures and contain no seed route.
The script removes only containers, network and image names it created.

`tests/summarize_acceptance.py` rejects stale artifacts, bridge-browser evidence,
skipped Python tests and missing PromQL execution. It records exact source hashes,
run identifiers, image identities and evidence hashes. `software_acceptance=passed`
never changes `live_aws_acceptance=not_run` or closes the Definition of Done.

## Primary interfaces used

- https://prometheus.io/docs/prometheus/latest/configuration/configuration/
- https://prometheus.io/docs/prometheus/latest/querying/basics/
- https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/api-legacy/data_source/
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-docker/

Legacy Grafana `/api` endpoints are used for the pinned test server and remain
operative while deprecated. Compatibility is measured by the integration run,
not inferred from a dashboard JSON parse. No independent security certification
or live AWS agent-effectiveness claim follows from these tests.
