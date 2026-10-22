# Instrument coverage: supported paths and explicit limits

The nine deployment-model labels describe the monitored service. They are **not** a claim that every FIS action, target resolver or local fault engine is implemented. No deployment model has been accepted against a real AWS workload during this delivery.

| Model | Executable path in this release | Limitation |
|---|---|---|
| EC2 / Auto Scaling | Existing duration-bounded stop template on exact EC2 ARNs, explicit state verifiers and an independent service probe. Other duration-bounded listed actions require their own approved template and checks. | Termination, Spot interruption and broad ASG/random selection are not qualified. Stopping an instance does not automatically prove replacement behavior. |
| EKS on EC2 | Exact EC2 host targets may use the EC2 path when the administrator proves workload mapping. | Kubernetes label/namespace/pod selectors and a pod-specific target resolver are not implemented. A managed-node-group label is not execution support. |
| EKS on Fargate | Observation of the monitored service and agent is representable. | No qualified direct pod fault executor in this release; selector targets are rejected. Do not attempt EC2-host faults or EKS pod-network actions against Fargate. |
| ECS on EC2 | Exact supported task ARNs and duration-bounded stress/network actions, with the required AWS-side preparation and independent checks. | SSM sidecar/fault-injection prerequisites, application mapping and platform behavior require live qualification. No container-host mutation is inferred from task metadata. |
| ECS on Fargate | Same explicit-task, finite-action path where the documented Fargate prerequisites and action are supported. | Not equivalent to EKS Fargate. No task termination/host-failure adapter is qualified here. |
| Lambda | Existing finite invocation delay/error/HTTP-integration-response template with exact function targets, required extension/configuration and independent service measurements. | Installation/prerequisite checks and actual invocation/side-effect correctness require live qualification. This GET probe does not reconcile writes. |
| Shared AWS services | Some finite EBS/network/API actions are structurally allowlisted. | Every target/result shape and verifier must be qualified. Database failover, regional disaster, replication recovery, data consistency and one-shot faults are not covered by the initial executor. |
| Docker / Podman | Hosts the local API/worker and SQLite. The probe can observe an authorized local service. | No Docker/Podman fault executor or engine-socket adapter in this release. |
| Local Kubernetes | Hosts the API and worker with one local persistent volume and port-forward access. | No local Kubernetes fault injector or distributed worker. No pod-selector execution support. |

The code intentionally rejects target `parameters`, tag filters and randomized selection. This means an action appearing in the duration allowlist is **not sufficient** to make a template usable. Expanding target support requires a resolver, actual-target comparison, fault confirmation, cleanup, tests and live acceptance—not removing the guard.

## Response measurements

The built-in workload instrument is a bounded single-path HTTPS GET probe, up to five scheduled requests/second and four concurrent requests. Scheduling shortfalls are recorded, not fabricated as service failures. It is not a production-scale load generator, multi-step user journey engine, write/idempotency test, or data-integrity oracle. Its path, expected status/JSON predicate, error/latency limits and load must be service-owned.

CloudWatch series are collected for inspection and graphs. The first response/prevention evaluator derives impact and recovery from captured probe requests; arbitrary CloudWatch expressions are not silently used as acceptance rules. CloudWatch missing/partial responses remain explicit. To make another business signal decisive, implement and test its evaluation contract.

The exact native reference join and optional sender receipt are specific to the existing incident integration. A receipt is attributable sender evidence, not an AWS attestation. Missing receipts produce an inconclusive delivery conclusion; an explicit correlated final rejection can establish a delivery-path failure. Lifecycle event timestamps are distinct from transport receipt time. No manual task fallback occurs in native mode.

## Prevention claims

Implemented comparisons are recurrence prevention, reduction of measured unhealthy-path duration, and earlier investigation with a qualified benign control. They require an actual recommendation version, reviewed exact implementation, verified changed state and comparable baseline/replay. Changed resource ARNs fail the automatic comparison: an equivalence resolver is not implemented.

The earlier-investigation claim is narrower than earlier autonomous detection. Its benign control requires a stable exact service-reference enumeration; integrations that generate a different reference per incident are not automatically eligible. False-positive semantic assessment across all agent activity is not implemented.

Sequential matched pairs are not randomized causal inference. Record history effects, prior investigations, trial order and confounders. An improved pair does not prove general prevention ability. Version-pinned recommendation lineage and verified deployment are necessary but do not prove that the recommendation alone caused the difference.
