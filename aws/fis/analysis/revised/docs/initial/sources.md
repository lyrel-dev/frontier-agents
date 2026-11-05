---
id: aws-fis-revised-docs-initial-sources
title: Official AWS FIS source register
type: source-register
service: aws-fis
status: reviewed
version: '1.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- source-register
aliases:
- Official AWS FIS source register
related:
- report.md
- sources.json
- ../review/quality-review.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/sources.json
---

# Official AWS FIS source register

This note presents the complete source register retained by the [initial report](report.md). The [machine-readable register](sources.json) is byte-for-byte identical to the reviewed baseline. Source IDs and citation links are stable.

**Research and baseline review date:** 2026-11-05. The second baseline review rechecked 22 central AWS pages; it did not claim a fresh exhaustive review of all 53. The current relocation to Obsidian does not add a new factual AWS recheck. See the [baseline quality review](../review/quality-review.md).

**Source policy:** Official AWS API Reference, User Guide, and EventBridge reference only. Product entity names, formulas, ingestion policy, and mock scenarios are engineering proposals.

| ID | Official source | Kind | Recorded access |
| --- | --- | --- | --- |
| S01 | [Experiment API shape](https://docs.aws.amazon.com/fis/latest/APIReference/API_Experiment.html) | api-reference | 2026-11-05 |
| S02 | [GetExperiment](https://docs.aws.amazon.com/fis/latest/APIReference/API_GetExperiment.html) | api-reference | 2026-11-05 |
| S03 | [ExperimentAction](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentAction.html) | api-reference | 2026-11-05 |
| S04 | [Action catalog shape](https://docs.aws.amazon.com/fis/latest/APIReference/API_Action.html) | api-reference | 2026-11-05 |
| S05 | [ActionParameter](https://docs.aws.amazon.com/fis/latest/APIReference/API_ActionParameter.html) | api-reference | 2026-11-05 |
| S06 | [ExperimentTemplateAction](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentTemplateAction.html) | api-reference | 2026-11-05 |
| S07 | [ExperimentTemplate](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentTemplate.html) | api-reference | 2026-11-05 |
| S08 | [Start from a template: snapshot semantics](https://docs.aws.amazon.com/fis/latest/userguide/start-experiment-from-template.html) | service-guide | 2026-11-05 |
| S09 | [Action sequence and duration semantics](https://docs.aws.amazon.com/fis/latest/userguide/action-sequence.html) | service-guide | 2026-11-05 |
| S10 | [ExperimentState](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentState.html) | api-reference | 2026-11-05 |
| S11 | [ExperimentActionState](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentActionState.html) | api-reference | 2026-11-05 |
| S12 | [ExperimentError](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentError.html) | api-reference | 2026-11-05 |
| S13 | [Lifecycle states and retention](https://docs.aws.amazon.com/fis/latest/userguide/view-experiment-progress.html) | service-guide | 2026-11-05 |
| S14 | [ExperimentOptions](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentOptions.html) | api-reference | 2026-11-05 |
| S15 | [Experiment options and previews](https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html) | service-guide | 2026-11-05 |
| S16 | [ExperimentTarget](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentTarget.html) | api-reference | 2026-11-05 |
| S17 | [Target selection semantics](https://docs.aws.amazon.com/fis/latest/userguide/targets.html) | service-guide | 2026-11-05 |
| S18 | [ResolvedTarget](https://docs.aws.amazon.com/fis/latest/APIReference/API_ResolvedTarget.html) | api-reference | 2026-11-05 |
| S19 | [ListExperimentResolvedTargets](https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentResolvedTargets.html) | api-reference | 2026-11-05 |
| S20 | [Resolved target availability](https://docs.aws.amazon.com/fis/latest/userguide/list-experiment-resolved-targets.html) | service-guide | 2026-11-05 |
| S21 | [Experiment target account configuration](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentTargetAccountConfiguration.html) | api-reference | 2026-11-05 |
| S22 | [ListExperimentTargetAccountConfigurations](https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentTargetAccountConfigurations.html) | api-reference | 2026-11-05 |
| S23 | [TargetResourceType](https://docs.aws.amazon.com/fis/latest/APIReference/API_TargetResourceType.html) | api-reference | 2026-11-05 |
| S24 | [ExperimentStopCondition](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentStopCondition.html) | api-reference | 2026-11-05 |
| S25 | [Stop conditions](https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html) | service-guide | 2026-11-05 |
| S26 | [SafetyLever](https://docs.aws.amazon.com/fis/latest/APIReference/API_SafetyLever.html) | api-reference | 2026-11-05 |
| S27 | [Safety lever behavior](https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html) | service-guide | 2026-11-05 |
| S28 | [UpdateSafetyLeverStateInput](https://docs.aws.amazon.com/fis/latest/APIReference/API_UpdateSafetyLeverStateInput.html) | api-reference | 2026-11-05 |
| S29 | [Multi-account safety and alarms](https://docs.aws.amazon.com/fis/latest/userguide/multi-account-prerequisites.html) | service-guide | 2026-11-05 |
| S30 | [ExperimentLogConfiguration](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentLogConfiguration.html) | api-reference | 2026-11-05 |
| S31 | [Experiment log schema and delivery](https://docs.aws.amazon.com/fis/latest/userguide/monitoring-logging.html) | service-guide | 2026-11-05 |
| S32 | [EventBridge notifications](https://docs.aws.amazon.com/fis/latest/userguide/monitoring-eventbridge.html) | service-guide | 2026-11-05 |
| S33 | [FIS EventBridge event catalog](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-fis.html) | service-guide | 2026-11-05 |
| S34 | [ExperimentReport](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentReport.html) | api-reference | 2026-11-05 |
| S35 | [ExperimentReportState](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentReportState.html) | api-reference | 2026-11-05 |
| S36 | [ExperimentReportS3Report](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentReportS3Report.html) | api-reference | 2026-11-05 |
| S37 | [ExperimentReportConfiguration](https://docs.aws.amazon.com/fis/latest/APIReference/API_ExperimentReportConfiguration.html) | api-reference | 2026-11-05 |
| S38 | [Report configuration and limitations](https://docs.aws.amazon.com/fis/latest/userguide/experiment-report-configuration.html) | service-guide | 2026-11-05 |
| S39 | [CloudWatch impact and usage metrics](https://docs.aws.amazon.com/fis/latest/userguide/monitoring-cloudwatch.html) | service-guide | 2026-11-05 |
| S40 | [CloudTrail audit records](https://docs.aws.amazon.com/fis/latest/userguide/logging-using-cloudtrail.html) | service-guide | 2026-11-05 |
| S41 | [Troubleshooting and error stability](https://docs.aws.amazon.com/fis/latest/userguide/troubleshooting.html) | service-guide | 2026-11-05 |
| S42 | [ListExperiments](https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperiments.html) | api-reference | 2026-11-05 |
| S43 | [StartExperiment](https://docs.aws.amazon.com/fis/latest/APIReference/API_StartExperiment.html) | api-reference | 2026-11-05 |
| S44 | [StopExperiment](https://docs.aws.amazon.com/fis/latest/APIReference/API_StopExperiment.html) | api-reference | 2026-11-05 |
| S45 | [Stop and post-action cleanup](https://docs.aws.amazon.com/fis/latest/userguide/stop-experiment.html) | service-guide | 2026-11-05 |
| S46 | [All FIS API operations](https://docs.aws.amazon.com/fis/latest/APIReference/API_Operations.html) | api-reference | 2026-11-05 |
| S47 | [UpdateExperimentTemplate](https://docs.aws.amazon.com/fis/latest/APIReference/API_UpdateExperimentTemplate.html) | api-reference | 2026-11-05 |
| S48 | [AWS FIS action-specific reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html) | service-guide | 2026-11-05 |
| S49 | [SafetyLeverState](https://docs.aws.amazon.com/fis/latest/APIReference/API_SafetyLeverState.html) | api-reference | 2026-11-05 |
| S50 | [ActionTarget](https://docs.aws.amazon.com/fis/latest/APIReference/API_ActionTarget.html) | api-reference | 2026-11-05 |
| S51 | [TargetAccountConfiguration](https://docs.aws.amazon.com/fis/latest/APIReference/API_TargetAccountConfiguration.html) | api-reference | 2026-11-05 |
| S52 | [UpdateExperimentTemplateExperimentOptionsInput](https://docs.aws.amazon.com/fis/latest/APIReference/API_UpdateExperimentTemplateExperimentOptionsInput.html) | api-reference | 2026-11-05 |
| S53 | [ListActions](https://docs.aws.amazon.com/fis/latest/APIReference/API_ListActions.html) | api-reference | 2026-11-05 |

The report includes the same full register and reference definitions. Each local diagram note points to the report section that explains its ownership and cardinality choices.
