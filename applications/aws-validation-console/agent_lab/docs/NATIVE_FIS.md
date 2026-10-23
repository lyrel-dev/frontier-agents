# Native FIS execution and multi-account scope

## AWS is the executor

For guided contracts (`native_fis: true`), the console submits the existing FIS template unchanged. AWS resolves tags, filters, target parameters and service-specific target forms. The controller checks `GetAction` in the selected Region rather than imposing the legacy action-name whitelist. It does not implement a Kubernetes selector engine or emulate a managed-service failure.

The original explicit-ARN finite-action path remains for old contracts. Its original restrictions and recorded results are preserved. Guided native contracts use the new path; the application does not silently upgrade a legacy definition or result.

## Template owner, agent account and target accounts

The template-owner account is the FIS orchestrator. It may differ from the Agent Space account and the primary monitored-service account. Native multi-account contracts pin the complete target-account ID/role map from AWS. Every affected account needs an approved observer profile and an existing association with the selected Agent Space. The selected accounts must equal the FIS target-account set; merely adding a profile for the orchestrator is insufficient.

One native FIS experiment spans target accounts within the template Region. The agent may be in another configured Region. Account-role map changes invalidate the plan. Every target has baseline, fault-effect and cleanup checks. Captured responses retain observer account and Region, rather than being flattened into a generic “account B”.

## Two preview stages, separate authority

The onboarding preview is a real `StartExperiment` call with `actionsMode=skip-all`, a persisted idempotency token, fresh safety-lever check, provider identity and exact local approval. Its complete target records and account-role configuration form the reviewable envelope.

An approved response trial establishes its measured healthy baseline, rereads the AWS template and runs a **fresh dispatch preview**. If the new targets/configuration violate the approved policy, it does not dispatch the actual fault. Otherwise it starts a separate `run-all` experiment with its own persisted operation identity. The lifecycle of both operations is retained.

Preview does not verify action permissions and does not lock target selection. Targets can change or be sampled differently. Approval therefore never establishes that a future tag match is safe. The actual execution's returned target records are checked while running and at completion. A resource outside the approved envelope requests stop and restoration; that is **detective**, not a guarantee that the resource was never affected. Restrictive AWS execution-role permissions are the preventive blast-radius boundary.

## Identity and matching

A target consists of AWS `targetName`, `resourceType` and complete `targetInformation`. ARNs are retained where returned. Other resource identities receive a local `fis-resource:<digest>` key while retaining the original AWS fields; this is not represented as an AWS ARN.

`exact` requires equality with the captured preview. `subset` allows only members of that captured envelope, at least the registered count, and representation of every approved named target group. It does not authorize an arbitrary later sample from all tag-matching resources. FIS random selection may therefore require a new preview/review when the sample differs. Empty or incomplete target data cannot qualify exposure.

Required action skips/failures and incomplete effects remain failed or unqualified exposures even when AWS reports an experiment terminal state. Independent application probes and account-specific reads establish intended effects; a provider status alone does not.

## Time and stopping

Native definitions are not rejected simply because an action is one-shot or lacks a duration parameter. Instead the administrator supplies a reviewed runtime deadline, cloud stop alarms and an independent recovery procedure. The deadline is a local observation/stop budget, **not** an upper bound on lasting effects. A stopped/rebooted/terminated resource or completed database failover is not reversed by `StopExperiment`.

Fresh safety-lever reads, exact approvals, approved alarm states, content fingerprints, account checks, durable dispatch intents and cleanup remain mandatory. A native template without suitable CloudWatch stop conditions must be corrected in AWS and rediscovered; this console does not edit it. The independent recovery plan must remain operable if the local host disappears. Test that plan on the authorized service before relying on this controller.

Original uncertain operation IDs are reconciled rather than replaced. Stop/reconciliation of an owned operation is not blocked by a start-only safety check. A failed restoration remains `RESTORE_REQUIRED`, preventing unrelated exposure.

## Coverage boundaries

The adapter supports AWS-owned target resolution and target-account configuration; this is not an assertion that every FIS action has been run against a real resource. Availability, service prerequisites, IAM efficacy, failure effects and independent checks remain action/account-specific acceptance requirements. Service-specialized setup (for example agent extensions or container instrumentation) is not installed by the console.

The AWS partition currently accepted by identity/ARN contracts is the commercial `aws` partition. Additional partitions require explicit tests and contract changes. AWS Organizations-wide account enrolment, multi-Region single experiments, parallel fault exposure and local Docker/Podman/Kubernetes fault execution are not implemented.

## Primary contracts reviewed on 22 October 2026

- https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html
- https://docs.aws.amazon.com/fis/latest/userguide/multi-account.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentResolvedTargets.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentTargetAccountConfigurations.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetSafetyLever.html
