# Deployment, connection and restore runbook

These recipes configure a **local, single-operator read-only console**. They are not proof that the image, credentials or volumes work in your environment. Perform the acceptance procedure at the end before treating the workspace as an evidence repository.

## 1. Select the host and persistence boundary

Run on an operator workstation, a dedicated local host or a local Kubernetes cluster. The workspace must not be an ephemeral container filesystem. Keep a separate backup outside the runtime you intend to disrupt. Do not expose the API through an Ingress, public port, tunnel or reverse proxy in this release.

The default data directory is `./data` for a native process and `/data` in the image. The database is `workspace.sqlite3`. Configuration is read once at startup; changing `config.json` requires restart. There is no automatic discovery of host credentials or sockets from inside a container.

## 2. Native process

Follow the Python commands in the README. Run as a non-root operator who can read the chosen SDK profile and, where approved, the local socket. Keep `CONSOLE_BIND` at its default `127.0.0.1`.

Use `config.json` with only the required connections. This example permits one AWS account; replace the placeholder and use your own approved Region:

```json
{
  "connections": [{
    "id": "aws-staging",
    "name": "Staging account",
    "kind": "aws",
    "profile": "readiness-readonly",
    "expected_account_id": "123456789012",
    "regions": ["eu-central-1"],
    "services": ["ec2", "autoscaling", "eks", "ecs", "lambda", "rds", "elbv2", "cloudwatch", "fis"]
  }]
}
```

### AWS authentication and permission checks

Prepare the profile outside this application using your organization's IAM Identity Center or assumed-role process. Boto3 uses its credential providers; the application does not implement login or store a credential document. For an already configured Identity Center profile, authenticate using your approved CLI workflow before inspection. Credential refresh failures remain collection/authentication errors, not empty inventories. [AWS credential documentation](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html)

`deploy/inspection-policy.json` is a policy **starter**, restricted to the implemented reads and an example Region. An administrator must review its Region condition, resource scope, trust policy, permission boundaries and organizational controls. It is not attached automatically. Source-identity permissions needed to assume a role are a separate concern. Do not use root credentials; the inspector rejects a root principal.

The inspector calls STS before listing resources and requires an exact expected account match. STS success establishes identity only, not permission for EC2, EKS or other reads. The coverage table shows denied operations. [STS reference](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)

## 3. Docker service

From the project directory:

```sh
docker compose up --build
```

Open `http://127.0.0.1:8787`, then read the token from the foreground logs. A detached deployment can use `docker compose logs console`; treat those logs as private. The named volume persists across normal stop/start. Never use `down -v` as a routine restart.

To access an AWS profile from the image, add a private Compose override mounting only the required credential/config directory into `/home/console/.aws:ro`. Verify UID 10001 can read it. A complete `~/.aws` mount can include unrelated credentials; a dedicated credential directory is preferable. A read-only token cache cannot always refresh expired sessions; refresh outside the container and repeat inspection. Do not loosen permissions to make the directory world-readable. No AWS CLI or external credential plugin is installed in the image.

### Inspecting a Docker engine

The administrator must explicitly configure a Unix socket path accessible to the process. A native process avoids container socket ownership complications. Container mounting requires a matching path and approved group/ACL mapping; it does not become safe merely by adding `:ro`.

The implemented adapter issues only `GET /version`, `GET /containers/json?all=true`, `GET /volumes` and `GET /networks`. However, a compromised process with the raw socket can use wider engine authority. A read-only filesystem mount does not enforce read-only HTTP methods. Prefer an administrator-enforced proxy that permits only the required methods and paths when stronger isolation is necessary. The application does not ship or configure that proxy. [Docker daemon protection](https://docs.docker.com/engine/security/protect-access/)

Do not set `privileged: true`, expose the socket over an unauthenticated network port, or grant cluster/host administration solely to make this inspector work.

## 4. Podman service

Build and run the image using a named local volume:

```sh
podman build -t localhost/validation-console:0.2.1 .
podman volume create validation_data
podman run --name validation-console --rm \
  -p 127.0.0.1:8787:8787 \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop ALL --security-opt no-new-privileges \
  -v validation_data:/data \
  -v "$PWD/config.json:/config/config.json:ro" \
  localhost/validation-console:0.2.1
```

On SELinux hosts, use an administrator-approved file label for the configuration mount; adding `:Z` relabels the source and must not be applied casually to shared home directories or sockets. Verify that the named volume is writable by the image's UID. Do not solve ownership problems by switching the whole service to privileged/root mode.

For rootless Linux Podman inspection, the API socket is normally under the operator's runtime directory. Starting the user socket through systemd is an administrative setup action, not performed by this app. Configure its actual absolute path, not the literal `$XDG_RUNTIME_DIR` variable. The adapter uses the Docker-compatible routes; real engine-version testing is required. macOS/Windows Podman commonly involves a VM or forwarded socket and is not claimed as accepted by this recipe. The Podman API grants the authority of its service user, not merely read access. [Podman service reference](https://docs.podman.io/en/latest/markdown/podman-system-service.1.html)

## 5. Local Kubernetes service

Before applying `deploy/kubernetes.yaml`, confirm the current `kubectl` context is your intended **local** cluster. Inspect the default StorageClass and verify that its backing storage is local, durable and suitable for SQLite. A PVC alone does not establish these facts. Keep one replica; do not scale this deployment horizontally. [Persistent-volume documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

Build the image and load it into that cluster using the cluster distribution's supported image-loading command. The manifest expects `localhost/validation-console:0.2.1`. It does not contact an image registry to publish the image.

```sh
kubectl config current-context
kubectl get storageclass
# Load the built image into the selected local cluster before proceeding.
kubectl apply -f deploy/kubernetes.yaml
kubectl -n validation-console rollout status deployment/console
kubectl -n validation-console logs deployment/console
kubectl -n validation-console port-forward service/console 8787:8787 --address 127.0.0.1
```

The supplied configuration inspects only the `validation-console` namespace. Its Role allows get/list for pods, Services, PVCs, Deployments, StatefulSets and DaemonSets. No Secrets, ConfigMaps, pod logs, exec or cluster-wide reads are granted. To inspect another namespace, an administrator must create a corresponding scoped RoleBinding and add the namespace to configuration; no wildcard expansion occurs. [RBAC guidance](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)

For a console running outside the cluster, specify a trusted kubeconfig, explicit context and namespaces. Kubeconfig may invoke an authentication program; review that file before granting it to the backend. TLS verification is required. The image does not include `kubectl`, AWS CLI or arbitrary exec-credential plugins. [Kubeconfig guidance](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

The manifest intentionally has no Ingress, external LoadBalancer, hostPath, engine socket or AWS credential mount. AWS inspection from this pod requires separately approved credential configuration; it is not implied by the Kubernetes service account.

## 6. Backup and restore

Use **Data & security → Download SQLite backup** while the service is running. This uses SQLite's backup API, not a raw copy of an active database. Save the file outside the volume under test and protect it like the source database. A JSON workspace export is also useful, but does not retain the complete database audit/provenance history or administrator connection configuration. [SQLite backup API](https://www.sqlite.org/backup.html)

To restore, stop the single writer first. Preserve the damaged/current database for investigation. Place the downloaded file as `workspace.sqlite3` in the intended data directory, restore the service UID's ownership and mode 0600, and restart. For a container volume, use your engine's approved offline volume-copy procedure; for Kubernetes, stop the Deployment before mounting the PVC in a restore job. There is deliberately no web endpoint that accepts an arbitrary database file.

After restore, export JSON and compare the record-hash manifest with the saved pre-incident manifest. Confirm that record counts, scenario revisions, validation inputs and recent audit entries are present. Test database integrity with `PRAGMA integrity_check` on an offline copy. Credentials and `config.json` must be restored separately; they are not in the workspace backup.

## 7. First live acceptance gate

Use a non-production account with a known resource set and one chosen local runtime. Record actual engine/cluster/API versions and the console source version.

| Check | Required evidence |
|---|---|
| Identity | Effective account and principal match the approved connection; a wrong expected account blocks all inventory calls. |
| Permissions | An intentionally denied read appears as denied, not zero resources or a pass. |
| Scope | Requested Regions/services/namespaces are visible; capped or failed reads are explicit. |
| Classification | Known examples of each applicable deployment model are correctly distinguished; unknown mappings remain unknown. |
| Secret minimization | Collected records contain no credential values, container environments, kubeconfig contents or function code. Review free text separately. |
| Observation validation | Complete requested collection passes only the collection assertion; a denied scope fails it. Neither report claims resilience. |
| Persistence | The same snapshot and hash exist after an ordinary service restart. |
| Recovery | A backup restored into a separate workspace has matching hashes and usable reports. |
| Access boundary | Loopback-only browser access; locked API rejects requests; untrusted origins and unsupported endpoints fail. |
| Connection refresh | Expired/revoked credentials produce an error; no synthetic fallback appears. |

Do not start fault execution as part of this gate: this release has no such endpoint. Keep the resulting acceptance record with the workspace and only then begin service-specific scenario specification.
