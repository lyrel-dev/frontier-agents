# Execution boundary and recovery

This release is a single-operator, local, **non-production** experiment controller. Enabling execution can disrupt the configured workload and incur AWS charges. The distributed configuration has no bindings and disables AWS writes. No authoring or packaging test used an existing AWS account, Agent Space or workload.

## Authority separation

The browser can propose account/profile bindings, probe URLs/CIDRs, allowlisted typed read checks, measurements and fixed runbook parameters. Only a separate exact approval activates a configuration, and active/uncertain/restoration work blocks reconfiguration. AWS credentials, arbitrary SDK operations, shells, custom service endpoints and arbitrary agent prose are not executable inputs. The same local operator can possess both tokens; two bearer tokens are not enterprise separation of duties, authenticated reviewer identity, or a substitute for IAM.

| Credential | Account | Intended authority |
|---|---|---|
| Agent observer | A | STS identity; read the exact Agent Space/association, tasks, executions, journals, evaluation recommendations and configured lifecycle/receipt logs. |
| Workload observer | B | STS identity; selected metric alarms/history, selected CloudWatch metrics, explicit allowlisted resource-state verifiers. |
| Fault executor | B | Read the approved FIS template/experiments/actual targets; start the qualified template; stop the owned experiment. |
| Change executor | B | Read pinned Automation documents; start the exact version/fixed parameters; inspect/stop the resulting execution and read its tags. |
| Task requester | A | Create INVESTIGATION tasks only in assisted mode and EVALUATION tasks for approved prevention campaigns. |
| Automation assume role | B | Only the APIs and resources required by the reviewed implementation/cleanup/rollback document. |

Configure least-privilege policies and role trust separately. Some list APIs require `Resource: "*"`; scope supported resource actions to the actual ARNs. No policy is attached by this application. Successful STS/GET calls do not prove write permission. `aidevops` is the IAM prefix; boto3's service name is `devops-agent`. Do not substitute the Agent Space's own cross-account service role for console credentials. `iam:PassRole` may be required by the approved execution path; review exact roles rather than granting it broadly.

The exact API operations are in `lab/aws.py`. The provider write allowlist is limited to FIS start/stop, SSM Automation start/stop, and DevOps Agent task creation. It cannot create IAM policies or execute arbitrary agent-generated text. Administrator-controlled Automation documents can still perform powerful AWS changes through `aws:executeAwsApi`; the finite control-flow check is **not a semantic safety audit**. An administrator must review the actual APIs, parameters, role scope, secondary effects, cancellation behavior and recovery.

## Qualification and approval

Guided native FIS qualification requires the pinned AWS definition, actual skip-all target envelope, exact target-account role map, verified observers/associations and baseline/effect/cleanup checks for every account. It verifies the returned action IDs, exact stop alarms currently OK and the incident route. It uses AWS target resolution, not a local tag/pod selector. The original explicit-ARN finite-action restrictions remain only on legacy contracts. Native one-shot actions require action-specific review and independent recovery; a local runtime deadline does not guarantee reversal. See NATIVE_FIS.md for the preview/execution race and preventive IAM boundary.

Automation requires a positive numeric document version, exact content hash, a fixed account-B `AutomationAssumeRole`, fixed parameters, independent after-state checks, and finite step budgets. This executor accepts only linear `aws:executeAwsApi`, `aws:assertAwsResourceProperty`, `aws:waitForAwsResourceProperty` and `aws:sleep`. Scripts, nested execution, branch/jump control flow and custom cancellation branches are rejected. Configure an explicitly reviewed rollback where reversal is required.

Approvals bind the exact account/Agent Space/entity, instrument configuration, qualification, source recommendation/finding, runbook content and fixed parameters. The approver sees the subject and digest. An approval expires; a changed subject must be approved again. The worker rechecks it before first mutation. Setting `enable_aws_writes` false blocks new execution but does not disable reconciliation and stopping of already-owned operations. Configuration changes require API and worker restart.

## Unknown outcomes and restart

The worker commits an operation intent, request hash and idempotency token **before** dispatch. It persists provider IDs. A timeout, transport error or malformed successful response is not treated as proof that nothing happened. The operation enters `UNKNOWN_REMOTE_STATE`; the worker reconciles an exact provider identity, tags/parameters and request lineage. It does not blindly repeat an uncertain write. This is not a distributed transaction or an exactly-once guarantee.

SQLite and a local `flock` provide one worker owner on one local filesystem. A network filesystem, multiple hosts, multiple replicas, or bypassing that lock is unsupported. Only one trial/change may own the execution slot; unresolved restoration retains that slot. Closing the browser does not stop the worker. Long worker/probe gaps remain evidence gaps and block a clean assessment.

## Independent safety and abort

The local process is not the emergency safety boundary. Existing cloud-side FIS alarm stop conditions and independent recovery must remain operable without it. Where a fault has a finite duration, that duration does not establish restoration. Test their behavior before live acceptance. A successful stop does not guarantee reversal of every effect, data recovery, or completion of application cleanup.

An abort stops subsequent trial steps, stops the owned FIS experiment where possible, cancels undispatched interventions, and stops running Automation where supported. Interrupted changes require independently verified restoration or the exact approved rollback. `RESTORE_REQUIRED` is not a successful terminal state and blocks unrelated execution. After investigating provider state, use **Recheck restoration**. This reuses the original stop/cleanup authorization, not an arbitrary new command.

The console intentionally does not invoke the account/Region-wide FIS safety lever. An authorized operator must retain independent access to it and understand that it can affect other experiments in that scope. Also retain independent access to the approved rollback and workload controls.

## Data, network and credentials

The probe is a bounded GET against an administrator-approved HTTPS destination and CIDR allowlist; redirects and metadata/link-local destinations are rejected. DNS addresses are checked and the connection is pinned, while TLS validates the original hostname. It stores response hashes, status and timings, not response bodies. Only explicitly enabled loopback development targets may use HTTP. The probe path itself must be safe and authorized; GET does not prove a server endpoint has no side effects.

AWS SDK profiles stay in the backend. Browser tokens remain in memory, not local storage. Same-origin API access, explicit Host checks, separate approval authorization, request-size limits and an external-script CSP protect the local UI; these are not an internet-facing authentication design. Publish only on host loopback or use a private port-forward. No container-engine socket is needed.

SQLite, raw source captures, summaries, receipt logs, configuration snapshots and exported reports may contain sensitive resource names, investigation text and account identifiers. These records are not universally redacted or encrypted by the application. Protect local disks, credentials, backups and exports. Hashes detect consistency changes; they neither authenticate the upstream producer nor prevent an administrator from replacing the entire database. Retention, deletion, key management, independent audit and tamper-resistant signing are outside this release.

See `SOURCES.md` for the reviewed AWS contracts and `LIVE_ACCEPTANCE.md` for deployment-specific gates.
