# AWS DevOps Agent response and prevention lab

**0.3.0-rc1 — executable release candidate; live AWS acceptance is pending.**

This is a local experiment controller for an existing Agent Space in **account A** and an authorized **non-production service in account B**. It is not a scenario viewer and does not claim that merely retrieving an investigation validates the agent.

The worker drives a real baseline, a bounded AWS FIS exposure, the existing incident-delivery path, investigation collection, independent workload observation, cleanup, and a pinned assessment. A prevention campaign requests an actual agent `EVALUATION`, retrieves and pins a recommendation version, links it to an approved SSM Automation implementation, verifies the deployed state, and compares a qualified replay with the baseline.

**No account, experiment definition, incident, result or measurement is preloaded. AWS writes are disabled in `config.json`. Test fixtures live only under `tests/` and are not loaded by the application.** The offline preview is deliberately empty.

## What is implemented

| Operation | Implementation |
|---|---|
| Register before exposure | Immutable experiment and campaign definitions; trial exists before an investigation task ID. |
| Qualify and approve | STS identities, exact secondary-account association, pinned FIS/template and runbook content, resource-state checks, alarm state, exact digest and separate approval credential. |
| Execute | Durable single-worker phase machine, operation intent before dispatch, original idempotency tokens, actual provider IDs, unknown-outcome reconciliation. |
| Measure | Actual CIDR-restricted HTTPS GET probes, CloudWatch alarm history and configured metric queries, exact-reference task discovery, journals, optional lifecycle events and sender receipts. |
| Judge response | Separate delivery, response timing, challenge, measurement, cited diagnosis, intervention, recovery, attribution and cleanup outcomes. No aggregate readiness score. |
| Test prevention | Baseline → agent evaluation → versioned recommendation → exact approved linear Automation → independent changed-state checks → matched exposure. |
| Preserve evidence | Local SQLite, append-only source/event records, immutable probe captures, input hashes, dependency-inclusive JSON, interactive offline report, database backup. |
| Inspect metrics | Interactive SVG charts, keyboard/hover, zoom, series toggles, source samples and CSV. Actual derived Prometheus export and a generated Grafana dashboard. |

The product does **not** execute arbitrary agent prose, provide an unrestricted shell, infer successful incident delivery from timestamp overlap, infer correct diagnosis from summary presence, or credit recovery after fault expiry to the agent.

## Run the empty console

Python 3.13 and a local disk are required. No AWS connection is made by these commands with the distributed empty configuration.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python run.py --with-worker
```

Open `http://127.0.0.1:8787`. The process prints an **operator token** and a different **approval token**. Unlock using the operator token. The approval token is entered only for an exact action approval. Neither is an AWS credential. Keep both private; protect process logs. For a managed deployment, supply `LAB_OPERATOR_TOKEN` and `LAB_APPROVAL_TOKEN` through your local secret mechanism instead of printing generated credentials.

To run the API and worker independently, use two processes sharing the same local data directory:

```sh
python run.py --config config.local.json --data data
python worker.py --config config.local.json --data data
```

Only one worker may own a workspace. Browser closure does not stop it. A worker interruption does not extend a FIS action; long observation gaps block a clean result and request stopping/restoration when the worker returns. Independent cloud-side stop conditions and recovery remain mandatory.

## Configure the two-account test

1. Copy `config/binding.template.json` to `config.local.json` and replace its placeholders. Complete JSON-string `${ENV_NAME}` placeholders can also be supplied through process environment variables. The template describes a **bounded stop of one existing EC2 instance**, not a claimed universal fault recipe. Replace it with your actual reviewed instruments.
2. Keep observer profiles in A and B separate from the fault/change profiles in B and the task-creator profile in A. Do not reuse the Agent Space's own service access role. Confirm the exact existing secondary-account association.
3. Specify the real incident integration's `reference.system` / `reference.referenceId` contract. There is no universal alarm-to-task mapping. Register the service's business-path probe, resource verifiers, safety alarms, limits and cleanup.
4. Read the already-reviewed FIS template and Automation documents to obtain content fingerprints. These helper operations are read-only:

```sh
python configure.py --fingerprint-fis YOUR_TEMPLATE_ID \
  --profile workload-fault-executor --region YOUR_REGION --account YOUR_WORKLOAD_ACCOUNT
python configure.py --fingerprint-runbook YOUR_DOCUMENT_ARN --version YOUR_NUMERIC_VERSION \
  --profile workload-change-executor --region YOUR_REGION --account YOUR_WORKLOAD_ACCOUNT
python configure.py --check config.local.json
```

5. Add reviewed implementation/rollback runbooks and their **actual deployed-state verifiers** before using prevention. A parameter claiming “deployed” is not a sufficient independent verifier unless it is independently maintained and justified. `config/runbook.template.json` defines the required shape; it is not an executable runbook.
6. Review [safety](docs/SAFETY.md), [the operation guide](docs/OPERATIONS.md) and [instrument coverage](docs/COVERAGE.md). Set `enable_aws_writes` true only after the administrator approves the instrument configuration. Restart both local processes after configuration changes; they do not hot-reload credentials or instruments from the browser.

## Execute a response trial

In **Instruments & access**, inspect the configured accounts and instruments. In **Response trials**, register your actual hypothesis, measurement limits, independent ground truth and diagnosis rubric. Registering creates no observations. Create a trial, **Qualify**, inspect the qualification evidence, approve the exact target/action digest, then **Start**.

The worker must observe a healthy real-traffic baseline before exposure. It starts only an approved finite FIS template; records actual resolved targets; verifies the fault's effect with independent AWS reads; discovers the native investigation using the configured external reference; collects findings and workload evidence; and verifies restoration. Native mode never creates a replacement investigation when incident delivery fails. Assisted mode is explicitly distinct and cannot validate native triggering.

Review a real investigation summary against the captured ground-truth records. The structured claim form requires exact quotations and independent source citations. This remains attributed human semantic extraction, not an objective automated language judge.

An optional mitigation must quote an actual mitigation summary and map to a pre-registered runbook. A separate exact approval starts that implementation. The UI shows proposal, provider execution, verification and rollback separately. Recovery is not labelled causal: at most it is temporally associated with an intervention while the fault remained active.

## Execute a prevention campaign

Create **Prevention campaign** before the baseline. Choose recurrence prevention, impact reduction or earlier investigation; register the tolerances and the Agent Space history/carryover note. Run all untreated baseline attempts first.

Request and approve the agent evaluation. Pin one returned recommendation version. Map it to a reviewed implementation artifact, runbook content/version, fixed parameters, and before/after verifiers. Approve the exact change. Only a verified deployment opens **Create matched replay**.

The replay uses the same experiment revision, instrument configuration and exact target set; checks the changed state before and after exposure; and compares actual delivered traffic and actual fault duration. Non-comparable and incomplete attempts are excluded with reasons, not deleted. Additional attempts remain visible. One successful pair proves only that specific measured challenge—not general incident prevention or randomized causal efficacy.

Earlier-investigation comparison uses **impact-to-task time**, not a claim that the agent itself detected the fault. It requires a healthy, fault-free post-change benign control with complete exact service-reference enumeration. Dynamic source-event-ID joins are not automatically qualified for that negative control. No invented zero false-alert rate is emitted.

## Graphs, reports and Grafana

The application graphs actual probes, configured CloudWatch series, derived timings and matched comparisons. A duration observed once is one point, not an invented trend. Missing values are missing. Each report pins its source hashes and a frozen probe capture. Historical reports are not silently updated when delayed samples arrive.

`GET /api/metrics` is an authenticated Prometheus text endpoint for measured derived gauges. `GET /api/grafana` downloads the dashboard. A present gauge does not prove freshness; the dashboard includes source observation age. See `grafana/README.md`. The console does not provide a Prometheus server or claim that the Grafana import/query path was tested in this environment.

## Tests and acceptance

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
python tests/worker_http_acceptance.py
CHROMIUM_PATH=/path/to/chromium python tests/browser_checks.py --native
```

`--native` must use actual browser HTTP navigation and fails if navigation is blocked. The alternative `--bridge` harness injects the DOM and bridges fetch to a real loopback API; it does not establish native CSP/fetch/CORS behavior. The recorded authoring-environment checks identify which method ran.

AWS operation contracts are checked with botocore Stubber; response/prevention state machines use test-only provider fixtures. Local HTTP probe tests perform actual loopback requests. **No AWS account or live Agent Space has been tested.** Docker/Podman/Kubernetes hosting, actual IAM efficacy, native incident-route correlation and a real recommendation/change/replay remain release acceptance gates. The implementation is a release candidate, not a validated claim about your agent.

See `validation/review.json` for measured results and `docs/LIVE_ACCEPTANCE.md` for the exact live gate. Legacy 0.2.1 workbench records are neither loaded nor upgraded to stronger verdicts.

## Source integration

The supplied patch adds this isolated application under `applications/aws-validation-console/agent_lab/` relative to the published repository baseline `83f65fc50d2f2a39c705356f71715ef1e33ef774`. It does not replace or import the legacy 0.2.1 workspace. No repository commit or merge was performed for this delivery. Test fixtures are shipped for reproducibility, not as runtime data.
