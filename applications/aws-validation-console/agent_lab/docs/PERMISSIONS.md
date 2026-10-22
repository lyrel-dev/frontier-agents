# Permission inventory and credential boundary

This is an operation inventory, not a policy granting every listed action on `*`. Resource-level support and condition keys vary by AWS action. An administrator must construct and review account-specific IAM policies and execution-role trust relationships. No policy is attached by the application.

| Identity | Required operation families for selected features |
|---|---|
| Every selected observer/executor | `sts:GetCallerIdentity`; actual expected account checked; root rejected. |
| FIS catalogue observer | `fis:ListExperimentTemplates`, `GetExperimentTemplate`, `ListTargetAccountConfigurations`, `ListExperiments`. |
| Agent observer | `aidevops:ListAgentSpaces`, `GetAgentSpace`, `ListAssociations`, `GetAssociation`, task/execution/journal read operations and recommendation reads. |
| Native FIS executor/orchestrator | `fis:GetAction`, template/target-account reads, `GetSafetyLever`, `StartExperiment`, `GetExperiment`, `ListExperiments`, `ListExperimentResolvedTargets`, `ListExperimentTargetAccountConfigurations`, `StopExperiment`; reads of its configured CloudWatch stop alarms. |
| Workload observers in every target account | Selected resource verifier reads, `cloudwatch:DescribeAlarms`, `DescribeAlarmHistory`, `GetMetricData`, and `logs:FilterLogEvents` where the incident receipt source is located. Only configured services/reads are called. |
| Optional agent task creator | `aidevops:CreateBacklogTask` for an explicitly approved assisted investigation or prevention evaluation. Native incident observation uses no substitute task. |
| Optional change executor | Pinned Automation document/execution reads, `ssm:StartAutomationExecution`, `StopAutomationExecution` and associated role-pass permissions where needed for the fixed document. |

The FIS service execution roles in the orchestrator/target accounts are **different** from console observer credentials. They need the selected actions' resource permissions and appropriate trust/role assumption. Preview success does not validate those action permissions. The Agent Space's own workload access is also a separate AWS service relationship.

The existing `deploy/fis-discovery-policy.json` is only a discovery starter. It does not authorize the native execution path. Review `lab/aws.py`, `lab/native_fis.py`, the chosen AWS action documentation, and your account policies together; a read capability report is not an IAM simulator.

The console accepts names of profiles already installed on the host. The SDK handles their ordinary SSO/role refresh. No browser-supplied keys, arbitrary credential paths, endpoint overrides or session credentials are accepted. Installing a profile or satisfying MFA remains an external credential-management responsibility.

Local API requests require the operator token. Exact approval routes require the separate approval token. The same person may possess both: this is not authenticated separation of organizational duties. Reviewer names are attributed input, not cryptographically authenticated identities.

Source captures can contain operational metadata and configured read results. Restrict observer permissions, avoid secret-bearing verifier queries, protect the SQLite directory/backups and encrypt the underlying storage as required. The application does not provide database encryption or signed source provenance. Do not publish live captures in CI artifacts.
