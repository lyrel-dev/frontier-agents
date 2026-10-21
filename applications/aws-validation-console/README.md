# Local Validation Console — 0.2.0

A local single-page workspace for AWS, Docker, Podman and Kubernetes inspection, versioned scenarios, execution records, evidence, validation results and reports.

**Collectors are read-only. This release does not inject faults, generate load, collect incident telemetry, query Prometheus or certify operational readiness.** It can now graph supplied evidence, including timestamped samples, and generate a proposed Grafana dashboard.

## Build and run

Use Python 3.13, the version used for local tests:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build_ui.py
python run.py
```

Open `http://127.0.0.1:8787` and unlock with the private startup token. `config.json` starts with no connections. Configure approved AWS profiles, expected account identity, local socket paths or Kubernetes context in the administrator configuration before inspection. The browser accepts no AWS access keys or connection paths.

To inspect the UI without a backend, open the generated `static/console.html`. It is self-contained and works offline. Preview records and the separate graph demonstration are explicitly synthetic. Preview changes stay in memory unless exported.

```sh
# Build and run in Docker; only loopback port 8787 is published.
docker compose up --build
```

The Docker build generates the UI from source. The default image mounts no credentials, engine socket or kubeconfig. The database resides in a persistent local volume. `docker compose down -v` deletes that volume. See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for Docker/Podman/Kubernetes access, storage and restore procedures.

## Metrics and Grafana

The **Metrics** view gives every catalogue/imported metric an interactive graph, including explicit missing-data states. Charts also appear beside overview counts, inventory counts, numeric resource facts and scenario/run/evidence/validation/report details. Hover or use arrow keys to inspect samples; drag or use zoom controls to select a range; toggle series, inspect provenance and export CSV.

The **Grafana design** view includes the 32-metric measurement catalogue and a downloadable dashboard proposal. Build outputs:

| Output | Purpose |
|---|---|
| `static/console.html` | Offline preview and served SPA. |
| `grafana/operational-readiness.json` | Importable proposed Grafana dashboard: 32 metric panels plus observation age. |
| `grafana/metric-catalogue.json` | Units, definitions and proposed queries. |
| `examples/metrics-series.json` | Explicitly synthetic, importable timeline examples. |
| `schemas/validation-bundle.schema.json` | Interchange schema, including optional chart samples. |

Generated outputs are built from tracked sources rather than committed as stale copies. Distribution bundles include them. `python run.py` builds missing outputs automatically; rebuild explicitly after source edits. No network is used by the build.

Read [METRICS.md](docs/METRICS.md) for sample semantics, source labels, Grafana setup, proposed recording rules and limitations. **The `readiness_*` Prometheus names are a proposed contract, not metrics already emitted by AWS FIS or this console.** A real source adapter remains necessary.

## Evidence and decisions

The requirement, execution, evidence, validation and report are separate immutable records. Import review precedes atomic commit. Existing revisions cannot be overwritten. Scalar values remain the evaluator inputs: an attractive graph cannot turn missing evidence into a pass. Optional chart samples are stored in local SQLite with their evidence record; report charts use only pinned inputs with matching hashes.

A successful inventory read is not resilience validation. All nine deployment models remain in scope: EC2/Auto Scaling, EKS on EC2/Fargate, ECS on EC2/Fargate, Lambda, Docker, Podman and Kubernetes. Live collector acceptance, controlled workload telemetry and supervised fault execution remain outstanding.

## Checks

```sh
python -m pip install -r requirements-dev.txt
python build_ui.py
python -m pytest -q
python tests/browser_checks.py
python tests/metrics_browser_checks.py
python tests/http_smoke.py
```

Chromium is required for browser checks; set `CHROMIUM_PATH` when necessary. The execution environment blocks browser navigation, so browser checks use DOM injection. The metrics harness supplies SHA-256 for its insecure test page and bridges UI API calls to real loopback HTTP. It checks served script/style hashes through meta CSP; native browser navigation, fetch/CORS and `connect-src` are not established by that harness. See `validation/metrics-validation.json` for measured results.

## Documentation and boundaries

[Metric design](docs/METRICS.md), [deployment](docs/DEPLOYMENT.md), [API](docs/API.md), [security](docs/SECURITY.md), [value-ranked roadmap](docs/ROADMAP.md). The version 0.1 [design baseline](docs/DESIGN.md) remains historical context; the metrics document specifies the 0.2 additions.

This is a single-operator local tool, not an internet-facing multi-tenant service. It has no scheduler, fault worker, general command executor, signed provenance or encrypted database. Protect local volumes and exports. Engine-socket access remains powerful even when the application chooses read endpoints. No live AWS/runtime or Grafana acceptance is claimed.
