# Security boundary and unresolved risks

## Intended deployment

One trusted operator, on a trusted local host, through loopback or a local Kubernetes port-forward. The application is not designed for exposure to the internet, shared-user operation or adversarial multi-tenancy.

## Implemented controls

The API requires a private token of at least 32 characters. The launcher generates one when it is not configured. Browser memory holds it until lock/reload; it is not placed in URLs or browser persistent storage. Startup logs contain it and therefore require protection. The health endpoint exposes no workspace or credential information.

The backend checks Host and Origin, rejects cross-site requests, does not enable CORS, and serves a Content Security Policy with exact inline-script/style hashes. UI imports are rendered as escaped text. JSON schema and reference checks run server-side. Duplicate property names, non-finite values, unknown fields and immutable-revision conflicts are rejected. Imports are atomic and bounded to 5 MiB.

Connections are allowlisted in administrator configuration. The browser can request a named connection, not a new endpoint or arbitrary command. AWS checks the effective account before inventory and rejects root. Kubernetes requires explicit scope and TLS verification. Docker/Podman routes are fixed GETs. No write, shell, fault-start or container-exec API is implemented.

Resource summaries are whitelisted. The inspector does not collect cloud keys, function code, container environment variables, secrets, volume contents or kubeconfig contents. This is minimization, not universal secret detection: resource names, imported JSON and free text may contain sensitive information.

## Limits that remain

| Risk | Present boundary | Required treatment before wider use |
|---|---|---|
| Raw Docker/Podman socket | Adapter uses GET only; process still has engine authority | Enforced proxy or separate restricted inspection process; review host impact |
| Malicious kubeconfig | Administrator must supply a trusted file; plugins may run | Review config/plugin executables and credential isolation |
| Compromised local administrator | Can read or alter data, token and audit log | OS controls, encrypted storage, signed/independent evidence where needed |
| Token leakage | Single bearer secret; no user identity or revocation list | Keep local; restart/rotate; add real authentication before multi-user deployment |
| Source forgery | Imported records visibly unverified; checksums are not signatures | Trusted collectors, signed bundles and source attestation |
| Data loss | Manual backup and one persistent database writer | Restore drills, volume monitoring, retention and independent backups |
| Process crash during inspection | No durable job journal for an unfinished collection | Durable worker state before remote fault execution |
| Large histories | Bounded imports but whole-workspace reads | Pagination, quotas, archival and load acceptance |
| Shared failure domain | Console may run in the environment being inspected | Separate controller/evidence backup/stop path before injecting failures |
| Dependency vulnerabilities | Versions pinned; no security-scan acceptance claimed | Review SBOM/CVEs, image provenance and patch policy before deployment |

A Docker bind mount marked `:ro` is not an HTTP read-only security policy. Podman's service documentation explicitly describes broad engine authority; Docker also requires protection of daemon access. Trusted kubeconfig and least-privilege namespaced RBAC are separate requirements. See the primary sources in `sources.json`.

## Future execution permissions

Do not add FIS execution permissions to the inspection role. A future executor must be a separate worker and identity, with bounded targets, durable remote IDs, approval tied to a plan hash, independent stop controls, cleanup verification and a non-production acceptance gate. This release grants no such authorization.
