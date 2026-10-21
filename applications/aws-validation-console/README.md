# Local Validation Console — 0.1.0

A local-first, single-page workspace for inspecting an AWS account and a local Docker, Podman or Kubernetes environment, then keeping scenario definitions, execution records, evidence, validation results and reports together.

**This release performs read-only metadata inspection. It does not inject faults, generate load, collect incident telemetry or certify operational readiness.** It provides a runnable foundation and the design for those next stages.

## Goal and current position

The original goal remains: measure customer impact, detection, response and recovery during controlled incidents across EC2/Auto Scaling, EKS on EC2, EKS on Fargate, ECS on EC2, ECS on Fargate and Lambda. A running resource, a completed FIS action or a successful inventory read is not proof of that outcome.

The earlier report supplied 36 research scenarios and six unexecuted FIS template starters. The 36 scenarios are retained here as **draft definitions**. This application adds persistent records and read-only collectors; it does not convert the earlier examples into approved executable tests.

The next acceptance milestone is one real AWS account plus one local runtime: verify identity, inspect bounded scope, retain denied/truncated reads, restart without losing data, and restore a backup with matching record hashes.

## Start with the interface

Open `static/console.html` directly in a browser. This **preview** uses marked synthetic fixtures in memory. It has no backend, credentials or persistent database. Export records before closing the page. Preview import checks are deliberately narrower than backend validation; preview results are not acceptance evidence.

For actual inspection and persistence, run the local service below. Its web interface starts locked and contains the draft catalogue, not synthetic deployment data. The console does not silently switch a failed live connection into a demonstration.

## Run the local service

### Native Python — simplest route to existing profiles and local sockets

Use Python 3.13, the version used for local tests. From the extracted project directory:

```sh
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export CONSOLE_CONFIG="$PWD/config.json"
export CONSOLE_DATA="$PWD/data"
python run.py
```

Open `http://127.0.0.1:8787`. Unlock with the token printed in the terminal. This token is **not** an AWS key. It is held only in browser memory. Reloading the page locks the interface. A new token is generated on service restart unless `CONSOLE_TOKEN` is set to a private value of at least 32 characters.

`config.json` initially has no connections. Copy the relevant entries from `config.example.json`, replace every placeholder, remove unused entries, and restart. Paths and profiles must be usable by the **service process**. Do not put access keys in connection JSON or imported records.

### Docker

```sh
docker compose up --build
```

The supplied Compose file exposes only loopback port 8787 and stores the database in the named `validation_data` volume. Read the startup token in the container logs. `docker compose down` preserves the volume; **`docker compose down -v` deletes it**. The image defaults to a non-root user, a read-only root filesystem and no added capabilities.

The default deployment intentionally mounts **no AWS credentials, engine socket or kubeconfig**. Configure required access explicitly using [the deployment runbook](docs/DEPLOYMENT.md). A containerized console cannot inspect its host engine merely because it runs inside that engine.

### Podman or a local Kubernetes cluster

The same image can run with a named Podman volume. `deploy/kubernetes.yaml` supplies a one-replica Deployment, namespace-scoped read permissions, a PVC and a ClusterIP Service. Neither deployment is claimed to have been exercised against a real runtime here. Exact commands, image loading, permissions and persistence checks are in [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## What works in this release

| Capability | Implemented behavior |
|---|---|
| AWS inspection | Check the effective account first; reject mismatch/root; read configured services and Regions; record partial coverage. |
| Local inspection | Fixed read endpoints for Docker/Podman Unix sockets; namespaced Kubernetes metadata reads. |
| Scenario catalogue | Six AWS deployment models, local models, search/filter, draft/specification status, JSON creation and revision. |
| Import/export | Versioned JSON bundles; backend schema checks; immutable revisions; atomic imports; dependency checks; hash manifests. |
| Execution records | Import or define observation/external run records. No command or fault execution. |
| Validation | Evaluate scalar assertions against explicitly linked evidence; keep failed and inconclusive checks distinct. |
| Reports | Freeze a validation summary; export JSON or inert standalone HTML. Imported reports remain unverified. |
| Storage | Local SQLite, additive audit events, consistent database backup, restart persistence. |
| Interface | Nine views, responsive navigation, searchable tables, detail drawers, import preview, visible provenance and synthetic labels. |

Missing incident evidence is never turned into a pass. A pass concerns only the assertions actually evaluated. Checksums detect changed content; they do not establish who supplied it.

## Files worth reading

- [Design and scope](docs/DESIGN.md): architecture, data model, evaluation semantics, deployment coverage and future execution design.
- [Value-ranked roadmap](docs/ROADMAP.md): acceptance gates rather than invented completion percentages.
- [Deployment and restore runbook](docs/DEPLOYMENT.md): local setup, credentials, socket risk, Kubernetes storage and first live acceptance.
- [API and data contract](docs/API.md): endpoints, import format, references and errors.
- [Security boundaries](docs/SECURITY.md): implemented controls and remaining risks.
- `schemas/validation-bundle.schema.json`: authoritative generated interchange schema.
- `examples/catalogue.json`: 36 research drafts plus the collection-coverage definition.
- `examples/synthetic-workflow.json`: deliberately failing and incomplete test fixtures.
- `VALIDATION.json`: what was tested, what was mocked and what remains unverified.

## Development checks

```sh
python -m pip install -r requirements-dev.txt
python build_ui.py
python -m pytest -q
```

`static/console.html` is generated from `static/shell.html`, `static/style.css`, `static/app.js` and `static/ui-data.json`. Do not edit the generated file without rebuilding the other deliverables. Frontend assets have no CDN dependency. Installing Python dependencies or building the image normally requires network access; inspecting AWS requires AWS connectivity.

## Boundaries

This is a single-operator local tool, not an internet-facing multi-tenant service. It has no scheduler, managed fault worker, arbitrary query executor, attachment/object store, user accounts, signed provenance, automatic retention or database encryption. All application records are local; AWS resources and AWS-side audit records remain in AWS. Source names and free-text imports can still contain sensitive information: review exports and protect the volume and backups.

For the optional browser and real-process HTTP checks:

```sh
# Use an installed Chromium via CHROMIUM_PATH, or Playwright's installed browser.
python tests/browser_checks.py
python tests/http_smoke.py
```

The browser harness uses injected page content and a TestClient bridge because native browser navigation was restricted in the delivery environment. The separate HTTP smoke test starts the real service on loopback, checks authentication/export/backup and verifies record hashes after process restart. Neither test connects to your AWS account or runtime.
