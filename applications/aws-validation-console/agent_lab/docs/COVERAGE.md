# Supported execution paths and unclosed scope

This delivery changes the FIS path from locally enumerated finite actions/explicit ARNs to **AWS-owned definition and target resolution** for guided native contracts. Legacy contracts retain their original validation rules. No deployment type has been live-accepted against the user's accounts in this delivery.

| Area | Implemented path | Boundary |
|---|---|---|
| Account set | Explicit connected accounts and Regions, installed SDK profiles, paginated catalogue, per-scope error reporting. | No automatic Organizations enrolment or discovery of unconfigured accounts/Regions. |
| FIS definitions | Existing single/multi-account templates, role-map pinning, dynamic selectors via actual skip-all, native Start/Stop and returned identities. | AWS service/Region/action prerequisites and restrictive IAM must be independently qualified. Preview is not a permissions test or target lock. |
| EC2, EKS, ECS, Lambda | Delegate selected FIS action and selector handling to AWS; verify effect/cleanup through configured account reads and service signals. | The console does not install Lambda extensions, ECS fault sidecars or Kubernetes access, or imply the same Fargate action support for EKS and ECS. |
| Shared data/network services | AWS FIS action execution plus configured state reads and CloudWatch business/collateral checks. | The selected verifiers and metric producers must establish effects and recovery. A namespace or metric name is not proof of data reconciliation. |
| Multi-account exposure | One orchestrator, all target observers/associations/role maps, per-account phase checks; distinct actual operation ID. | One FIS Region; commercial AWS partition; the console does not grant service-role permissions. |
| Local Docker/Podman/Kubernetes | Hosting of API/one worker/local evidence and access to authorized probe paths. | No local fault engine, engine-socket integration, parallel distributed worker or general command executor. |
| Instrumentation | Bounded HTTPS GET probe, configured CloudWatch series, source receipts/lifecycle logs, allowlisted read-verifier forms. | Not a production-scale or multi-step load generator; write/reconciliation producers remain service-owned. |
| Intervention/prevention | Exact approved restricted linear Automation, verified deployed state and matched replay. | No arbitrary scripts, automatically generated commands or general external-CI attribution. |
| Benchmarking | All attempts, separate dimensions, per-agent/per-cohort timing distributions, business checks and conservative comparison. | Sequential exposure, shared agent history, human semantic extraction; no automatic causal ranking or isolated agent reset. |

Dynamic/random targets are constrained to the approved captured envelope. A later sample outside it blocks the next fault or triggers stopping if already observed during execution. It is not silently authorized. New resource identities need new review; the prevention comparator does not infer replacement-resource equivalence.

Required business check aggregation supports maximum, minimum, sum and last across complete aligned metric buckets. No requirements yields not-assessed. Missing data is not zero. Complex transactional population reconciliation and semantic false-cause/harm assessment require independently accepted instrumentation/review; they are not solved merely by exposing a configurable threshold.

See [Native FIS](NATIVE_FIS.md), [Benchmark contract](BENCHMARK_CONTRACT.md) and [Delivery acceptance](DELIVERY_ACCEPTANCE.md). Do not present these boundaries as either universally supported capabilities or closed acceptance gates.
