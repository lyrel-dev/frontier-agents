# Use cases

Use the [searchable index](index.html) to browse by product and operational task. Each linked page includes its configuration and direct procedure references.

## AWS DevOps Agent — Incident response

Incident response moves from signal routing to investigation, then to mitigation planning and separately authorized execution. A status bulletin communicates progress without becoming a new diagnosis.

### [Triage incident signals](UC-D01.html)

Route a signal to the appropriate investigation or justified exclusion.

An on-call engineer receives several alerts for the same service. Before opening another investigation, the engineer needs to know whether the new signal belongs to work already in progress. Inspect the triage decision and its reason, then follow the primary investigation when the signal was linked. A skipped signal should identify the matching exclusion rather than disappear from the operating record.
When correlation is wrong, unlink the signal so it can be investigated separately. When a skip criterion excluded a relevant event, review that criterion and use the supported unskip operation. The result of this use case is correct routing and an identifiable investigation, not a root-cause conclusion. Root-cause analysis follows in the next use case.

### [Investigate a service incident](UC-D02.html)

Establish an explanation supported by current incident evidence.

A service owner sees elevated errors after a deployment. The investigation begins with the affected service, incident time, and symptoms, not with an assumed deployment defect. Connect the available logs, metrics, traces, repository context, and deployment records, then inspect how the investigation relates the observations across those sources.
The useful result identifies the measurements that support each explanation and the sources that could not be read. A deployment timestamp may provide a lead, but its proximity to the error increase is not sufficient proof of cause. When evidence conflicts, preserve the competing explanations and supply the missing observation through investigation steering rather than turning a plausible summary into a confirmed diagnosis.

### [Prepare a mitigation plan](UC-D03.html)

Prepare a proposed change that a reviewer can approve, reject or revise.

Once the current evidence supports a likely failure mechanism, the incident owner needs a mitigation that can be reviewed. Ask for the proposed target, exact change, expected effect, risks, rollback, and recovery checks. Compare that proposal with the approved runbook and the evidence already collected, especially where the proposed action would affect another service.
The output is a decision document: it should make it possible to approve, reject, or revise the proposal without guessing its effect. A generated plan remains separate from execution. It can be carried out through the ordinary engineering process, or through an eligible directed-action path after the additional controls described in the next use case have been satisfied.

### [Execute an approved mitigation and verify recovery](UC-D04.html)

Carry out an eligible approved change and assess service recovery.

An incident owner has accepted a narrowly scoped mitigation and wants to use the documented action path. Confirm Agent Space enablement, the target-account role or connected-tool configuration, and the classification of the operation. Review the actual parameters presented for approval; a broadly named role is not the approval record.
After the operator approves the eligible action, inspect the resulting resource state and the available attribution evidence. Recovery must still be checked against service measurements. If execution is denied, locate the failed gate instead of widening all permissions. This workflow does not convert the earlier mitigation recommendation into standing authorization for subsequent changes.

### [Prepare an incident-status bulletin](UC-D05.html)

Explain what changed in an active incident during a short observation window.

During an active incident, the incident commander needs a brief update that explains what has changed since the preceding observation. Configure a specialist task with the incident identifier, selected telemetry tools, and a short explicit lookback window. Ask for changed measurements, the status of open hypotheses, missing reads, and the next check rather than a repetition of the whole incident history.
A report can analyze minute-resolution measurements without arriving every minute. The documented custom-agent schedule uses a flexible window of up to 30 minutes; execution time is additional. For time-critical updates, invoke the task on demand or use a separately tested triggering design. Record both the measurement window and report-generation time so a delayed bulletin is not mistaken for current telemetry.

## AWS DevOps Agent — Operational reporting

Health reports and change-activity reviews produce comparable observations. Their cadence and presentation format are choices within a defined objective; a later operational review uses the results for decisions.

### [Assess and report service health and trends](UC-D06.html)

Produce a sourced health assessment or comparable-period report.

The incoming engineer needs to know whether the service is healthy, what changed, and which observations are missing. Define the service scope and reporting period first. Retrieve the selected measurements, compare significant differences with a baseline when needed, and connect material observations to incident and deployment evidence. A recent snapshot and a multiweek trend are analytical profiles of the same reporting objective.
Review a material measurement against its source before relying on the report. Keep missing telemetry visible and consider workload changes before interpreting a trend. Recurrence preserves the agreed reporting basis; it does not create a different objective. An operational review can subsequently use this report to decide priorities and owners.

### [Review deployment and change activity](UC-D07.html)

Establish which deployments and rollbacks affected the selected services.

A release engineer wants to review the changes delivered during the previous week. The input is deployment history with service and revision identifiers, not simply merged pull requests. Configure the task to distinguish attempted, successful, failed, and rolled-back deployments using the states exposed by the connected delivery tools.
The result should make it possible to trace a reported deployment to its source record and compare it with incidents in the same service and period. Similar timestamps are useful for investigation but do not establish causality. Missing pipeline access or ambiguous status mappings should be listed explicitly so the report is not presented as a complete release history.

## AWS DevOps Agent — Reliability improvement

Pattern identification establishes recurring evidence. Prevention prioritization decides which proposals deserve owned implementation. These are related but independently reviewable outcomes.

### [Identify recurring incident patterns](UC-D08.html)

Identify cross-incident conditions supported by investigation evidence.

Several investigations may share an operational weakness even when they were triggered by different alarms. Review the relevant investigation history and ask which causes or contributing conditions recur. Group the evidence by the proposed pattern and retain the supporting investigation identifiers so the grouping can be challenged.
This analysis differs from retrieving the prior cause of one alarm: its purpose is to identify cross-incident themes worth prevention work. Similar symptoms without verified common causes should remain a candidate pattern. The next step is to review the prevention recommendations against those themes rather than assuming that a historical cluster explains the next incident.

### [Prioritize incident-prevention work](UC-D09.html)

Turn evidence-backed improvement proposals into owned engineering work.

The reliability owner has identified recurring themes and needs a manageable prevention backlog. Run or inspect the documented prevention evaluation, then review each recommendation against the incidents it addresses. Separate observability improvements, infrastructure changes, governance work, and code changes because they have different owners and acceptance evidence.
Keep an accepted recommendation linked to its source evidence and normal change process. A recommendation’s priority or estimated effect is not proof that the change has been implemented. During the next operational review, inspect actual progress and post-change observations. This closes the team’s improvement loop without claiming autonomous implementation or measured benefit before either exists.

## AWS DevOps Agent — Operational knowledge

Procedure consolidation produces reviewed instructions; topology documentation produces an owner-reviewed system description. Both use source evidence, but their maintained outputs differ.

### [Consolidate and maintain operational procedures](UC-D10.html)

Maintain one reviewed procedure for the intended operational situation.

A team has several overlapping timeout SOPs maintained by different owners. First reconcile their scope, resolve contradictory steps, remove stale tool names, and identify the approved procedure. Only then package that procedure as a skill with a description that states when it applies and which agent types may use it.
Keep the reviewed source in Git and test a request that should match the skill alongside one that should not. The supporting references should explain the expected observations and the point at which the procedure stops or escalates. Consolidation is authored team work; skill selection is the platform mechanism. A skill neither creates the referenced tools nor grants permission to use them.

### [Document service topology and dependencies](UC-D11.html)

Produce a reviewed service and dependency description.

A service owner needs an architecture description before changing a dependency. Start from discovered resources and the topology’s service, repository, pipeline, and dependency relationships. Compare those relationships with the deployed configuration and source revision, distinguishing directly observed relationships from inferred ones.
Write the reviewed result as a maintained service description with identifiers, evidence links, and unresolved edges. The topology is useful input to that document, but it is not a guaranteed complete inventory or an automatic update to the team’s architecture repository. This use case produces owner-reviewed documentation; the following refresh use case checks whether the underlying environment model has changed.

## AWS DevOps Agent — Configuration assurance

A scoped audit compares actual resource settings with approved rules and retains unassessed resources as gaps rather than passes.

### [Audit resource configurations against approved standards](UC-D12.html)

Assess selected resource settings against an explicit operational standard.

An operations standard requires a small set of staging resources to have particular logging and access settings. Configure a custom task with read-only configuration tools, the explicit resource list, and the reviewed standard. Each reported finding should identify the resource, the applicable rule, and the actual value that was read.
Review a known conforming and a known nonconforming example before scheduling the task. An unavailable read is an unassessed resource, not a pass. The output is a scoped configuration audit for the chosen rules; it is not a built-in universal compliance engine or permission to repair findings automatically.

## AWS DevOps Agent — Release assurance

Readiness analysis examines a proposed revision, while active testing exercises a deployed target. Source evidence, application effects and completion criteria are different.

### [Assess release readiness](UC-D13.html)

Assess an eligible proposed revision for operational risk.

Before release, a team wants to examine a retry-policy change for operational risk. Use the eligible readiness-review path with the candidate revision, relevant repositories, topology, and release context. Review the findings against the intended dependency behavior and the service’s existing resilience assumptions.
A readiness review analyzes a proposed change; it does not prove that the deployed application behaves correctly. Retain unresolved dependencies and scope limitations and route accepted findings through engineering review. This feature is a separate preview path, so production-operations availability must not be used as evidence that the same review is available for every Region or repository.

### [Test a deployed application release](UC-D14.html)

Observe release behavior on an authorized disposable target.

A staging application is ready for an active release check. Prepare disposable test data, approved identities, explicit allowed operations, and disabled external side effects. The task exercises the deployed target, so the target revision and reachable endpoints matter more than the name of the branch that produced it.
Review the observed requests and results with the application owner. Active testing can create, modify, or delete application data; infrastructure read permissions do not make those requests harmless. The result describes the executed test and its uncovered areas, not blanket release approval. Unexpected effects require stopping and reviewing the configuration before further execution.

## AWS Security Agent — Application assessment

The assessment objective remains stable while network path, application identities and invocation mode vary. Each combination must preserve authorized scope and record actual coverage.

### [Assess a running application for vulnerabilities](UC-S01.html)

Assess the explicitly authorized surface and record findings and coverage gaps.

An application owner authorizes assessment of a deployed release. Establish the target surface, permitted effects, source context and execution limit before starting. Public versus private access and authenticated versus unauthenticated testing are independent configuration choices: they determine which paths can be examined, not four independent operational objectives.
Review the saved configuration and follow the resulting run. Record actual revision, roles reached, exclusions, findings and incomplete areas. A recurring schedule or pipeline may initiate later runs, but cannot preserve credentials or target state that have since changed. Interpret an absence of findings only within the paths actually assessed.

## AWS Security Agent — Source and design assessment

Code review, design review and threat modeling examine different evidence and produce different review objects. Variants within an assessment must not erase its resource lifecycle.

### [Review source code for security issues](UC-S02.html)

Assess an identified source revision for vulnerabilities and selected requirements.

A team wants a baseline review of a repository or supported source package. Connect the intended source revision and select the eligible review modes. Vulnerability analysis and evaluation against enabled requirement packs answer related but different questions, so the requested criteria should be explicit.
Review findings in their code context and inspect preflight failures separately from completed analysis. The result applies to the selected source and modes; it is not a substitute for testing the deployed application. This preview workflow has provider and availability boundaries that must be checked before it becomes part of the delivery process.

### [Review a proposed application design](UC-S03.html)

Evaluate a current design against applicable security requirements.

A team proposes a new payment-service design before implementation. Submit the current design material and relevant application context for the eligible review, and identify the enabled requirements that govern it. The assessment should expose assumptions about identity, data flows, and trust boundaries that need owner confirmation.
Review the findings with the architect and distinguish missing design evidence from a demonstrated violation. Design review has a one-off lifecycle, with cloning used for a new review; it should not be described as an automatically refreshed continuous model. The result informs design work rather than approving the future implementation.

### [Develop and review an application threat model](UC-S04.html)

Produce a reviewed system representation and evidence-backed threats for a defined scope.

A service boundary has changed and the team needs an updated threat model. Supply explicit scope documents and the relevant architecture and source evidence. Review the inferred system overview, components, data flows, and trust boundaries before evaluating individual threats.
Correct an incorrect boundary at the model input rather than dismissing every threat that follows from it. Retain evidence for the accepted threats and identify inferred relationships that remain unverified. The result is a reviewed model for that scope and run, not proof that every possible threat has been discovered.

## AWS Security Agent — Findings and repair

Disposition, a proposed source repair and verification of a deployed repair are distinct outcomes linked by finding identity.

### [Triage and prioritize security findings](UC-S05.html)

Give findings an evidence-based disposition and accountable next action.

A completed assessment contains findings of different severity and evidential strength. Review each material finding in the context of the affected revision, reachable role, exposed data, and reproduction evidence. Add application-owner context before deciding which finding needs immediate repair and which requires more investigation.
The outcome is a disposition and an accountable next action, not merely a sorted severity list. Findings with incomplete evidence should retain that uncertainty. Link accepted work to the original finding identifier so remediation, deployment, and later verification remain traceable even if the issue title or owner changes.

### [Prepare a code-remediation proposal](UC-S06.html)

Produce a reviewable source change for an accepted finding.

A developer has accepted a finding and wants a repair proposal against the affected source. Confirm the repository and supported remediation settings, then inspect the proposed patch or pull request. The review should include the security change, regression tests, and any unrelated behavior introduced by the proposal.
Run the normal build and review process before deployment. A generated proposal that fails tests is unfinished work, and a merged revision that has not reached the target is not ready for revalidation. Preserve the finding identifier through the change and deployment records so the next test can evaluate the intended repair.

### [Revalidate a finding after deployment of a repair](UC-S07.html)

Determine whether a selected issue still reproduces under valid current test conditions.

The reviewed repair has been deployed to the original authorized environment. Select the existing finding for revalidation and inspect the new job, including the current authentication configuration and target revision. The job repeats the selected validation steps rather than conducting a broad new assessment.
Interpret the result within that scope. A reproduced finding remains active evidence of the issue; non-reproduction supports resolution only when the relevant identity and path were actually reached. Keep the original finding and the linked job history. A failed login or changed test environment must not be mistaken for a successful repair.

## AWS Security Agent — Assessment governance

Maintaining requirements is controlled authoring work. Applying those requirements during an assessment is a supporting mechanism, not another duplicate case.

### [Consolidate and maintain security requirements](UC-S08.html)

Maintain reviewed assessment criteria derived from authoritative policy.

Policy owners have revised several overlapping security standards. Reconcile the governing documents and identify the approved source before generating a replacement requirement pack. Compare the generated applicability and compliance statements with that source, including requirements that had previously been added manually.
Regeneration replaces the existing pack contents rather than appending to them. Review the proposed replacement before enabling it for subsequent assessments, and keep the policy and reviewed requirement source in Git. This is a controlled authoring workflow; it must not silently replace a working pack merely because new documents were uploaded.

## AWS FinOps Agent — Cost analysis

Historical analysis starts with a reproducible query. Totals, dimensional breakdowns and variance are analytical profiles; monetary attribution is not automatically operational causality.

### [Analyze historical cost and usage](UC-F01.html)

Answer a bounded historical cost question using reproducible source queries.

A service owner asks how expenditure changed and which component requires investigation. Begin with the dates, cost metric, currency, scope and grouping. A total inquiry, owner breakdown and period comparison are analytical profiles of this bounded cost-analysis objective. Use reviewed ownership mappings only where the requested view needs them, and preserve unmapped values.
Reconcile totals and deltas against the same source basis before interpreting them. The largest monetary contribution identifies where to look next; it does not establish why the workload consumed that usage. Keep observed cost separate from forecasts and recommendation estimates, and retain unavailable evidence rather than inventing a single causal explanation.

## AWS FinOps Agent — Planning and commitments

A forecast projects expenditure. Commitment coverage describes eligible usage covered by existing commitments. Their evidence and completion criteria remain separate.

### [Review a cost forecast](UC-F02.html)

Review a projection for an explicit horizon and assumptions.

A planning owner needs a projection for a defined future period. Specify the horizon, cost basis and account scope, then obtain the supported source forecast. Retain its assumptions and source rather than put the projection in the same column as expenditure already observed.
Review the projection against known workload plans and record limits in the evidence. This outcome is distinct from assessing commitment coverage. A forecast does not authorize a purchase or establish what the next bill will be.

### [Review commitment coverage](UC-F03.html)

Assess coverage of eligible usage by existing commitments.

A commitment planning owner needs to understand how existing commitments cover eligible usage. Specify the commitment type, workload scope and observation period. Inspect coverage directly instead of inferring it from a spending forecast or total account cost.
Review the observation with service owners and distinguish a coverage gap from an instruction to buy. A purchasing decision has separate assumptions and authority. The case ends with a reviewed coverage assessment, not a transaction.

## AWS FinOps Agent — Cost reporting

A report retains a comparable period and analytical basis for a defined audience. Recurrence and external publication are separately configured choices.

### [Prepare a periodic cost report](UC-F04.html)

Produce a comparable report for the defined period and audience.

The team needs a recurring cost report with a stable comparison basis. Define the reporting period, sections, dimensions, audience, and output format before scheduling it. The task should distinguish observed spend, anomalies, and source recommendation estimates so unlike values are not added together.
Review a trial artifact against the source totals and inspect the saved automation separately from the generated task. A weekly schedule does not specify whether the report includes an incomplete current day. Preserve the task identifier and query basis with each report so changes in the template do not obscure what was actually compared.

## AWS FinOps Agent — Anomalies and optimization

Anomaly investigation explains a deviation, recommendation review prioritizes proposed work, and post-change measurement evaluates observed outcomes. Estimates do not replace measurements.

### [Investigate a cost anomaly](UC-F05.html)

Quantify a cost anomaly and assess available evidence for an operational cause.

A cost monitor identifies an unexpected increase. Inspect the anomaly record and query the affected cost dimensions for the relevant period. Where permissions allow, use operational-change records to investigate whether a workload or configuration change explains the increased usage or rate.
Keep numerical attribution and causal evidence separate. A nearby CloudTrail event provides a lead but does not necessarily explain the whole deviation. The final explanation should identify affected costs, supporting observations, and missing inputs. If change evidence is unavailable, preserve the reconciled cost contribution without inventing an operational cause.

### [Prioritize optimization recommendations](UC-F06.html)

Select actionable upstream recommendations under workload constraints.

An optimization source proposes several changes for a service. Retrieve the original recommendations and inspect their assumptions, resource scope, and overlapping savings estimates. Add workload constraints such as latency, resilience, deployment risk, and ownership before prioritizing the candidates.
Record why each candidate is accepted, deferred, or rejected and identify the normal engineering process for an accepted change. The underlying recommendations originate in the documented optimization services. The agent’s explanation does not independently measure future savings or authorize an infrastructure change.

### [Measure the outcome of an implemented optimization](UC-F07.html)

Measure post-change cost and service behavior within defensible attribution limits.

An approved optimization has been implemented, and the owner wants to know what changed. Select comparable before-and-after periods and record traffic, pricing, allocation, and service-health differences that could affect the result. Reconcile the costs using the same metric and scope.
Report the observed change together with its attribution limits. A lower bill is not sufficient evidence that the optimization caused the decrease when demand also fell. This is a team measurement workflow using source-backed analysis, not a service guarantee of savings. Unexplained differences remain part of the outcome rather than being removed from the report.

## Cross-service architecture — Operational governance

An operational review assembles reviewed results into decisions and owned follow-up. Reliability and cost-management profiles share a meeting narrative, not credentials or an execution runtime.

### [Prepare an operational review](UC-G01.html)

Prepare evidence-backed decisions, owners and follow-up for an operational review.

An operational review starts with reviewed evidence and unresolved decisions, not with a request for another differently titled report. Select the reliability or cost-management profile, identify its period, and assemble relevant findings with the previous action list. Each input retains its source and execution identity so participants can question its interpretation.
Organize the meeting around decisions required, their supporting observations, accountable owners and the next verification date. Owners confirm progress and acceptance; silence is not completion. The profiles reuse this narrative while retaining their own data access and execution configuration. A combined meeting is a team-managed composition, not an AWS cross-agent orchestration feature.
