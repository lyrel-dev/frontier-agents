# Runtime safeguards and hosting acceptance

This increment hardens the executable controller before live two-account acceptance. It does not configure an AWS account, authorize a target, run an incident, or declare the agent effective.

## FIS dispatch guard

Every first `StartExperiment` dispatch now reads the workload account/Region's `default` safety lever using the separately verified fault identity. Only `disengaged` permits that dispatch. `engaged`, `engaging`, malformed responses, denied reads, and unavailable reads block it. The console never changes the lever.

Add `fis:GetSafetyLever` to the reviewed fault profile's read permissions. This permission was previously needed only by the optional preflight command; it is now required by execution too. Review the account and Region scope with the administrator.

The source response and an `execution_guard` record are retained before the operation intent is dispatched. A guard record describes that instant, not a claim that no subsequent operation occurred. It does not replace exact approval, template fingerprints, target checks, stop alarms, independent restoration, or AWS's own enforcement. A concurrent administrator change remains possible between the read and the service request.

An existing confirmed start returns its recorded provider identity. An uncertain start is reconciled against its original identity rather than repeated. Neither that reconciliation nor stopping an owned experiment depends on the start-only guard. This avoids a new local guard preventing emergency recovery.

Official contract: https://docs.aws.amazon.com/fis/latest/APIReference/API_GetSafetyLever.html

## Worker ownership and process supervision

`python run.py --with-worker` now acquires the workspace lock synchronously and waits for the worker to start before it serves HTTP. A second combined process using that workspace exits instead of presenting an apparently operational console whose worker failed in a daemon thread.

The combined process watches its worker. An engine or probe-scheduler failure records a failed heartbeat, stops the HTTP server, and produces a nonzero process exit. Normal shutdown stops scheduling and waits for in-flight local probe work before releasing ownership. The process applies a 30-second drain budget; exceeding it terminates the process unsuccessfully even if executor threads remain, and leaves durable operation intents for reconciliation after restart. Shutdown is not automatic cloud rollback.

Separate API/worker deployments remain supported. The API can serve evidence when its separate worker is stopped, but starting a trial still requires the worker heartbeat. The combined-process supervisor does not manage an external worker process.

## Reproducible checks

```sh
python -m pytest -q
python tests/browser_checks.py --native
python tests/worker_http_acceptance.py
# Requires a local Docker engine; no AWS credentials or account configuration:
python tests/container_runtime_acceptance.py
```

The new Docker check builds the actual image with its empty runtime configuration. It verifies non-root/read-only hosting, loopback publication, dropped capabilities, no credential or engine-socket mounts, API authentication, no seeded trials or metric samples, rejection of a duplicate combined worker, SQLite backup integrity, preservation of a local storage marker across abrupt idle-container replacement, and graceful shutdown.

The storage marker is created only by the test harness in a disposable volume. It is not workload telemetry, is never part of the distributed configuration, and is not used by the evaluator. The harness removes only its uniquely named containers, image and volume. It fails rather than silently skipping when Docker is unavailable.

The workflow retains `validation/container-runtime.json` with the built image ID and individual results as an artifact. The image ID identifies the tested build; upstream base images and transitive dependencies are not fully locked. Repeat review and image scanning before an actual deployment.

## What these checks do not establish

Container replacement is tested while idle, not during an actual AWS mutation. Unit and worker-HTTP tests use explicitly isolated provider doubles. No account A/Agent Space or account B service is accessed by CI. Podman, Kubernetes, external IAM/credential refresh, live incident delivery, real diagnosis, prevention effectiveness and production safety remain separate acceptance obligations.

Continue with [the live acceptance gate](ACCEPTANCE_GATE.md). A passing software or hosting check is not execution approval or an agent performance result.
