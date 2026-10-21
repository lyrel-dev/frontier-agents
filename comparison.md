# Platform comparison

No shared runtime, memory or authorization model is asserted.

| Dimension | AWS DevOps Agent | AWS Security Agent | AWS FinOps Agent |
|---|---|---|---|
| Primary evidence | Current telemetry, topology and change context for an incident. [D05](devops/validated-report.html#D05) | Design/source assessments and executed target-test evidence. [S03](security/report.html#S03) | Billing-tool results and source optimization recommendations. [F01](finops/report.html#F01) |
| Historical context | Managed monitor memories and corrective reflections; explicit store lifecycle. [DM3](devops/validated-report.html#DM3) | Requirements, source context and linked retest history; no general incident-memory claim. [SM4](security/report.html#SM4) | User context files and retained reporting preferences; no changes to billing truth. [FM2](finops/report.html#FM2) |
| Change proposal | Mitigation proposal or prevention recommendation. [D07](devops/validated-report.html#D07) | Proposed code repair, followed by developer tests and deployment. [S08](security/report.html#S08) | Source recommendation summarized for workload-owner review. [F06](finops/report.html#F06) |
| Resource/application effects | Approved directed actions; preview Sandbox and release testing have separate boundaries. [DM5](devops/validated-report.html#DM5) | Authorized penetration-test traffic against a configured target. [S06](security/report.html#S06) | Documented external publishing, not resource resizing or commitment purchase. [FM4](finops/report.html#FM4) |
| Recurring work | Custom-agent definition, selected tools/context and triggers. [DM4](devops/validated-report.html#DM4) | Source-review trigger rules and assessment jobs; no universal scheduler assumed. [SM2](security/report.html#SM2) | Scheduled tasks or supported cost-anomaly event automations. [FM3](finops/report.html#FM3) |
| Meaning of success | Diagnosis supported by current evidence; recovery verified separately. [DU1](devops/validated-report.html#DU1) | Specific finding retested under valid conditions; regressions independently checked. [SU2](security/report.html#SU2) | Matched totals reconcile; explanation and estimates remain qualified. [FU1](finops/report.html#FU1) |

The shared work-record fields are a proposed team practice, not a native common schema.
