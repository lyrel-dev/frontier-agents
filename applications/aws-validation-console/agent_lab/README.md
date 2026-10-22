# AWS FIS · Agent response and prevention console

**0.5.1-dev — implementation delivery; live acceptance and remote publication are not complete.**

A local console for an authorized non-production AWS account set. It discovers existing FIS templates, prepares measured trials through forms, delegates target resolution and fault execution to FIS, observes AWS DevOps Agent, and produces source-pinned response and prevention assessments. AWS templates are not rewritten into local fault recipes.

The runtime starts empty. There are no accounts, credentials, incidents, measurements, recommendations or success records to demonstrate. Test fixtures are isolated under `tests/` and excluded from the runtime image.

## Start

Use Python 3.13 on Linux with a private local disk:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build_assets.py
python run.py --with-worker
```

Open `http://127.0.0.1:8787`. Use the local operator token printed by the process; keep the separate approval token private. Neither token is an AWS credential. Set distinct `LAB_OPERATOR_TOKEN` and `LAB_APPROVAL_TOKEN` environment values through your host secret mechanism for managed hosting.

## Operator workflow

Open **Guided setup** inside the AWS workspace. There is no application-JSON editing requirement for the guided path.

1. Select locally installed SDK profile names, expected AWS accounts and Regions. Test reads; approve the exact configuration proposal.
2. Discover the actual Agent Space and select its existing workload-account associations.
3. Discover FIS templates, inspect an AWS definition, and separately approve a real `skip-all` target preview.
4. Select observers for every target account. Define the business-path probe, typed resource checks, native incident correlation, response limits, independent recovery and optional business/collateral metrics in the forms. Add reviewed runbooks for intervention or prevention.
5. Review and approve the local plan revision. It becomes a selectable template/Agent Space contract in the FIS library.
6. Register a campaign, qualify and approve each exposure, inspect native response/diagnosis, and freeze the benchmark. Use **Response / prevention** for recommendation, implementation and paired replay.

Profiles, SSO sessions, AWS service roles and the existing incident integration must already exist on the host/in AWS. The console can identify access failures; it does not create cloud credentials, grant IAM permissions or fabricate an incident-delivery route. [Onboarding](docs/ONBOARDING.md) identifies each required input and the command it enables.

## Implemented changes in this delivery

| Component | Behavior |
|---|---|
| Account onboarding | Form-based account/Region/profile selection, identity/read checks, paginated Agent Space/association discovery, immutable configuration proposals and separate activation approval. |
| Native FIS planning | AWS-resolved target previews; dynamic tag/filter/parameter targets, AWS non-ARN resource identities and single/multi-account definitions are handled through FIS. |
| Guarded execution | Fresh pre-dispatch preview; exact/subset envelope policy; account-role fingerprints; per-account checks; original provider IDs; safety lever; independent cleanup. No local action-name allowlist on native definitions. |
| Guided instrumentation | SDK-shaped read parameters, resource-state predicates, HTTP probe, incident reference/receipt mapping, CloudWatch measurements, limits and reviewed Automation documents. |
| Agent benchmark | Qualified-exposure denominators, all attempts/exclusions, separate response/diagnosis/recovery/attribution, configured data-correctness and collateral verdicts, interactive graphs and exports. |
| Prevention | Actual evaluation task, pinned recommendation version, approved implementation, independently verified change and comparable replay. Required business failures cannot be hidden by availability recovery. |
| Local evidence | Configuration and plan revisions, captures, approvals, durable operations, charts, exports and consistent SQLite backup. |

A preview is a real AWS operation and requires separate authorization. It does **not** lock targets or prove permission to execute actions. Runtime drift detection cannot prevent the first effect on a newly selected resource; restrictive FIS execution roles remain essential. Stopping an experiment does not reverse completed actions. See [Native FIS execution](docs/NATIVE_FIS.md).

## Artifacts and routes

`/` is the AWS SPA with integrated Guided setup. `/setup` is the standalone setup surface. `/response` retains detailed diagnosis, intervention, recommendation and replay controls. API and one durable worker share the local workspace; closing the browser does not stop it.

`build_assets.py` produces ten JSON schemas, an empty main/response/setup preview, and the baseline Grafana dashboard. These offline previews cannot connect to AWS. The live application exports measurements and a dashboard through authenticated `/api/metrics` and `/api/grafana` routes; no series exists before evidence is collected.

[Onboarding](docs/ONBOARDING.md) · [Native FIS](docs/NATIVE_FIS.md) · [Campaign operation](docs/FIS_FLEET.md) · [Benchmark contract](docs/BENCHMARK_CONTRACT.md) · [Permissions](docs/PERMISSIONS.md) · [API](docs/API.md) · [Safety](docs/SAFETY.md) · [Deployment](docs/DEPLOYMENT.md) · [Acceptance](docs/DELIVERY_ACCEPTANCE.md)

## Verification and remaining acceptance

```sh
python -m pip install -r requirements-dev.txt
python build_assets.py
python -m pytest -q
python tests/browser_checks.py --native
python tests/fis_browser_checks.py --native
python tests/setup_browser_checks.py --native
python tests/worker_http_acceptance.py
# Requires Docker; no AWS credentials or connected configuration:
python tests/container_runtime_acceptance.py
```

`--native` fails when actual browser navigation is unavailable. The explicitly limited `--bridge` alternative uses DOM injection and a real local HTTP backend; it does not establish native navigation or CSP/fetch acceptance. SDK Stubber tests validate request/response shapes; provider doubles in workflow tests do not establish AWS behavior.

The live Definition of Done remains open until an authorized deployment passes the native account/incident/agent/intervention/prevention acceptance in [DELIVERY_ACCEPTANCE.md](docs/DELIVERY_ACCEPTANCE.md). This is not an independent security audit or production-readiness certificate. Current run-specific results accompany the delivery package; previous revision evidence remains in Git history and must not be used as results for this source.

The source is based on remote revision `b9dc53939611cc32904b49e2447dbb7fd5e2ab35`. The delivery includes a local commit and apply-ready patch; it does not claim a remote branch update.

## Integration review

See [RELEASE_0_5_1.md](docs/RELEASE_0_5_1.md) for the publication corrections and current-source acceptance procedure. Native browser, container and monitoring-server checks are required in repository CI; they do not establish live AWS or Agent Space efficacy.
