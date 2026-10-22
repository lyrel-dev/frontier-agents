# AWS FIS account orchestration and agent benchmarks

**0.4.0-rc1 — live AWS and agent-performance acceptance pending.**

The default `/` view discovers existing FIS templates across a configured set of AWS accounts and Regions, maps them to approved agent-response measurement contracts, and sequences qualified FIS trials through the durable executor. Frozen benchmarks retain unsuccessful and unstarted attempts and separate incomparable service/template/agent cohorts. The detailed response and prevention workspace remains at `/response`.

Start with [the AWS/FIS operating guide](docs/FIS_FLEET.md). Account discovery needs only read permissions and is independent of execution configuration. No account, incident, experiment or measurement is preloaded.

The local controller tests an existing Agent Space in account A against an authorized non-production service in account B. It drives a measured baseline, an approved finite FIS exposure, native incident correlation, investigation collection, independent workload observation and verified cleanup. Prevention links an actual evaluation and versioned recommendation to an approved implementation and comparable replay.

The installation is empty. `config.json` disables AWS writes. No account, incident, result or measurement is seeded. Test providers exist only under `tests/` and are not loaded by the application. Legacy workbench results are not imported or upgraded.

## Run

Use Python 3.13:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build_assets.py
python run.py --with-worker
```

Open `http://127.0.0.1:8787`. Unlock using the local operator token. The separate approval token authorizes an exact displayed action; neither token is an AWS credential. In managed operation, supply `LAB_OPERATOR_TOKEN` and `LAB_APPROVAL_TOKEN` through the local secret mechanism. Protect logs and data volumes.

The API and worker can also run separately against the same local directory:

```sh
python run.py --config config.local.json --data data
python worker.py --config config.local.json --data data
```

Only one worker can own the workspace. Closing the browser does not stop a trial. Independent cloud-side stop conditions and recovery procedures are mandatory.

## Connect the actual environment

Complete `config/binding.template.json` locally. It describes one finite, explicit-target EC2 stop example, not a universal fault recipe. Supply the real account IDs, regions, profiles, Agent Space/association, exact native incident-reference contract, approved targets, pinned instruments, verifiers, business-path probe and service-owned limits. Keep observation, fault execution, change execution and optional task creation identities separate from the agent's own cross-account role.

```sh
python configure.py --check config.local.json
python acceptance.py preflight --config config.local.json \
  --experiment experiment.local.json --data data --read-aws \
  --output local-acceptance/read-checks.json
```

Without `--read-aws`, preflight is an offline plan. Add `--probe` only to send one explicit business-path GET. Preflight never starts a fault, runbook, investigation or evaluation. A successful read check is not execution approval or evidence that the agent can handle an incident. See [ACCEPTANCE_GATE.md](docs/ACCEPTANCE_GATE.md) for report semantics and the required live gates.

## Execute and evaluate

Register the actual experiment before a task exists. Create a response trial, qualify it, inspect the captured prerequisites, approve the exact subject and start. Native mode never creates a substitute investigation when delivery fails. Assisted mode cannot validate native triggering.

The worker persists operation intent and idempotency identity before dispatch. Uncertain outcomes require reconciliation; unresolved restoration blocks further unrelated execution. It never executes arbitrary agent prose. A mitigation must map to a registered, version-pinned runbook with separate approval and independent state verification.

Results separate challenge, measurement, native delivery, response, cited diagnosis, intervention, recovery, attribution and cleanup. Diagnosis uses attributed human extraction against the frozen oracle. Recovery following a change is not automatically a causal effect of the agent.

For prevention, register the comparison before baseline, request an approved agent evaluation, pin a recommendation version, verify its approved implementation and run a matched replay. Failed, aborted, excluded and incomplete attempts remain visible. Earlier-investigation claims require a qualified post-change benign control. One pair does not establish general prevention competence.

## Evidence, graphs and acceptance

SQLite retains source records, observations, approvals, provider identities and frozen assessments. Graphs support inspection, zoom, series selection, source tables and CSV without filling missing data. `/api/metrics` and `/api/grafana` expose measured derived gauges and a dashboard proposal behind authentication. Configuration and report exports may contain sensitive resource identifiers.

```sh
python acceptance.py audit --data data --trial "$BASELINE_TRIAL_ID" \
  --campaign "$CAMPAIGN_ID" --output local-acceptance/evidence-audit.json
```

The audit reads a consistent database snapshot. `reviewable` means local completeness and hash consistency, not live certification or an agent pass. Source authenticity and the authorized live experiment remain independent obligations.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python build_assets.py
python -m pytest -q
python tests/browser_checks.py --native
python tests/worker_http_acceptance.py
```

Set `CHROMIUM_PATH` as needed. `--native` requires real browser HTTP navigation and does not fall back to a bridge. `--bridge` is an explicitly limited authoring-sandbox harness. Browser tests delay the workspace HTTP response to cover unlock/load ordering. Unit and worker tests use test-only AWS/agent providers; loopback probes make real local requests. Neither validates an AWS account.

## Documents and repository

[Operations](docs/OPERATIONS.md) · [Safety](docs/SAFETY.md) · [Coverage](docs/COVERAGE.md) · [Deployment](docs/DEPLOYMENT.md) · [API](docs/API.md) · [Live acceptance](docs/LIVE_ACCEPTANCE.md) · [Acceptance commands](docs/ACCEPTANCE_GATE.md)

Source is committed on `feat/devops-agent-response-lab` in `lyrel-dev/frontier-agents`, under `applications/aws-validation-console/agent_lab/`. This branch is not merged by the acceptance-tool work. Generated preview, schemas and dashboard are rebuilt with `build_assets.py`; local configuration, credentials and acceptance exports must not be committed.
