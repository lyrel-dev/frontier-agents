# Local deployment and storage

Run the API and worker from the same source revision and shared workspace. The bootstrap configuration supplies only initial settings; both processes refresh the separately approved active configuration stored in SQLite. The API writes intent/approval records; the worker owns AWS mutation dispatch. Both use one local SQLite directory. The default configuration is empty and cannot execute an experiment.

## Native Linux

Use the README commands. Either `python run.py --with-worker`, or separate `run.py` and `worker.py` processes. Set `LAB_OPERATOR_TOKEN` and `LAB_APPROVAL_TOKEN` to distinct high-entropy values of at least 24 characters. Use a local secret manager or protected environment file. Export only selected credential/header variables. `LAB_BIND` defaults to loopback. This implementation uses Unix `flock`; Windows is not qualified.

A role/profile refresh is performed by the AWS SDK. Actual SSO expiration, refresh and cross-account behavior must be tested in your environment. The console never accepts access keys in the browser. Keep profiles for A/B observers, B fault/change execution and A task creation separate.

## Docker or Podman

```sh
cp .env.example .env
# Replace both token placeholders locally before starting; chmod 600 .env.
docker compose up --build
# Or, with a locally installed compatible Compose provider:
podman compose up --build
```

The API is published only on `127.0.0.1:8787`. The image runs as UID/GID 10001, drops capabilities, uses a read-only root filesystem and a writable named data volume. The default image contains no AWS credentials, runtime socket, connected configuration or result data. `docker compose down -v` deletes that data volume; do not use it as routine shutdown.

After administrator review, make **only required** AWS profile/config/cache files available to UID 10001. Use Guided setup to create the account/measurement configuration in SQLite. A read-only `/app/config.json` mount remains an optional bootstrap path, not a prerequisite for the GUI workflow. Configure any role/SSO cache write requirements explicitly rather than assuming a read-only credential mount supports refresh. Do not mount the entire home directory or Docker/Podman socket. Populate the approved probe header variables through a protected environment mechanism. These mounts are deliberately not present in the distributed Compose file.

The image uses a pinned application dependency list but an upstream `python:3.13-slim` tag and transitive dependencies are not digest-locked. The credential-free Docker hosting harness is included in CI. The current delivery has not run it locally because no Docker engine is available; historical CI successes apply only to their own revisions. This is not a supply-chain audit or live AWS acceptance. Scan the image, pin a reviewed digest, and validate volume ownership and credential refresh before executing an AWS trial.

## Kubernetes

`deploy/kubernetes.yaml` is a single-replica, Recreate deployment with API and worker containers sharing a PVC. It starts with the empty configuration and no service-account token. Replace the image with your reviewed built digest. Create the `agent-lab-auth` Secret separately with keys `operator-token` and `approval-token`; do not commit it. An example command can be generated from your local secret manager; no secret value is supplied in the manifest.

The PVC intentionally has no storage class selected. Set a reviewed local/block storage provisioner and confirm actual backing location, locking and SQLite durability. A PVC alone does not prove data is local. Do not use a shared network filesystem or scale the replicas. No ingress or public LoadBalancer is included. Access with:

```sh
kubectl -n agent-validation port-forward service/agent-lab 8787:8787
```

Set up account profiles/workload identities and network access as an explicit deployment task. The supplied `automountServiceAccountToken: false` manifest does not claim automatic IRSA/EKS Pod Identity configuration. Kubernetes scheduling, storage, native credential integration and Podman operation have not been accepted in this delivery.

## Backup and restore

`GET /api/backup` with the operator token returns a SQLite online backup. Export a dependency-inclusive trial/campaign JSON as review material, not as a database restore.

Before restoring: stop API and worker; preserve the existing data directory; verify the backup file with `PRAGMA integrity_check`; replace only the workspace database using the configured filename, correct UID and mode; and ensure no stale SQLite WAL/SHM sidecars are reused. Restart in observation-only mode first. A restored operation intent may still represent an active AWS operation: reconcile IDs and verify actual resource state before enabling new work. Do not erase uncertain operation history to force a retry.

## Runtime safeguard follow-up

The branch now includes a Docker hosting acceptance harness and combined-process worker supervision. See [Runtime safeguards and hosting acceptance](RUNTIME_ACCEPTANCE.md) for the commands, evidence artifact, new mandatory FIS safety-lever read, and remaining live-environment limits. Use the exact commit's CI artifact to determine whether its image was built and exercised. This does not qualify Podman or Kubernetes automatically.
