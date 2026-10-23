# AWS FIS agent benchmark console — 0.5.1-dev

This revision publishes the guided account/native FIS implementation and adds
restricted telemetry access plus exact-source operational acceptance. It is a
development build: a passing software run is not evidence that a real AWS agent
responded correctly or that the product's live Definition of Done is closed.

The application starts empty with AWS writes disabled. No runtime seed/imported
successes or credentials are supplied. Test fixtures are under `tests/` only.

## Start

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build_assets.py
python run.py --with-worker
```

Open `http://127.0.0.1:8787`. Use the printed local operator token, not an AWS key.
The separate approval token is required for exact configuration and execution
approvals. Production credentials, SSO and role trust remain host/administrator
configuration. The main console's **Guided setup** selects installed profiles,
verifies account identities, discovers Agent Spaces and associations, prepares
existing FIS templates and defines the response measurements through forms.

## Workflows

- [Guided onboarding](docs/ONBOARDING.md): account scopes, exact approvals,
  typed AWS verifier fields, incident correlation and requirement setup.
- [Native FIS](docs/NATIVE_FIS.md): single- and multi-account templates,
  target previews, fresh scope checks, actual execution and restoration.
- [Campaigns and benchmarks](docs/FIS_FLEET.md): discovery, queue control,
  denominator/exclusion handling, pinned results and comparison limits.
- [Response/prevention operations](docs/OPERATIONS.md): native delivery,
  grounded diagnosis, approved interventions and recommendation/change/replay.

The new hosting/telemetry work is described in
[OPERABILITY.md](docs/OPERABILITY.md). `GET /healthz` checks the API process;
`GET /readyz` requires a recent running worker heartbeat. Neither tests AWS.

## Prometheus and Grafana

Set a distinct `LAB_METRICS_TOKEN` or `LAB_METRICS_TOKEN_FILE`. That credential
permits **GET /api/metrics only**; it cannot read configuration, evidence or
backups, and cannot start/approve a cloud action. Never give Prometheus an
operator or approval credential. Exact internal hostnames can be supplied through
`LAB_ALLOWED_HOSTS`; wildcard hosts and arbitrary endpoint changes are rejected.

Metrics carry the frozen assessment, Agent Space, service, workload account,
Region, template revision and native/assisted mode. They are trial summaries,
not live service telemetry; every scrape re-exposes frozen values. Observation
age remains visible. Missing measurements are absent, never zero-filled.

Download the configured dashboard from `/api/grafana` with the operator
credential. The dashboard includes observed business requirements and an Agent
Space filter. No Prometheus or Grafana server is bundled inside the application.

## Checks

```sh
python -m pip install -r requirements-dev.txt
python build_assets.py
python -m pytest -q
python tests/browser_checks.py --native
python tests/fis_browser_checks.py --native
python tests/setup_browser_checks.py --native
python tests/worker_http_acceptance.py
python tests/container_runtime_acceptance.py
python tests/observability_acceptance.py
```

The final two scripts require Docker and fail rather than skip when it is absent.
The observability check runs the real console, Prometheus and Grafana on an
internal-only network. It checks actual scraping, missing data, label retention,
dashboard import/readback and execution of generated PromQL. Its positive
measurement is real loopback HTTP latency; account, agent and business labels
are explicit test fixtures in a disposable workspace, not AWS results.

CI uses native HTTP browser navigation, not the authoring environment's bridge.
Each run clears prior generated evidence, then records its exact source and
artifact hashes in `validation/software-acceptance.json`. Inspect that run's
result; do not reuse counts from earlier revisions as acceptance of this one.

## Status and boundaries

The implementation has a durable single-host worker, independent probes, actual
FIS execution adapters, native incident observation, grounded human diagnosis
review, approved Automation changes and matched prevention replay. It does not
create credentials, remove required approvals, validate unknown business-metric
producers or execute arbitrary agent prose. Preview is neither a target lock nor
an action-permission test. Independent cloud-side recovery remains mandatory.

The current target is `feat/aws-fis-console-acceptance`, based on remote
`b9dc53939611cc32904b49e2447dbb7fd5e2ab35`. No main-branch merge is implied.
[DELIVERY_ACCEPTANCE.md](docs/DELIVERY_ACCEPTANCE.md) retains the open live gates:
real account/IAM access, incident delivery, agent findings, multi-account cleanup,
recommendation efficacy, intended-host credentials and independent business
measurement acceptance. **The full Definition of Done remains open.**
