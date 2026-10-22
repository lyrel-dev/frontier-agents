# Operational use-case catalog

Thirty outcome-oriented use cases linked through explicit workflow steps to mechanisms, platform features and configuration profiles.

[Mechanisms](mechanisms.html) · [Features](features.html) · [Implementation profiles](profiles.html) · [Former-record mapping](migration.md)

## UC-D01 — Triage incident signals

**Actor:** On-call engineer

**Objective:** Route a signal to the appropriate investigation or justified exclusion.

An on-call engineer receives several alerts for the same service. Before opening another investigation, the engineer needs to know whether the new signal belongs to work already in progress. Inspect the triage decision and its reason, then follow the primary investigation when the signal was linked. A skipped signal should identify the matching exclusion rather than disappear from the operating record.

When correlation is wrong, unlink the signal so it can be investigated separately. When a skip criterion excluded a relevant event, review that criterion and use the supported unskip operation. The result of this use case is correct routing and an identifiable investigation, not a root-cause conclusion. Root-cause analysis follows in the next use case.

### Completion criteria

- Decision and reason are visible.

- The resulting investigation or exclusion is identifiable.

### Workflow and dependencies

#### 1. Inspect routing

Determine whether this signal requires independent work.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-TRIAGE](mechanisms.html#MX-D-TRIAGE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-INCIDENT](features.html#FT-D-INCIDENT)

**Effect:** Investigation linkage

**Verification:** Inspect the routing decision, reason and resulting investigation identity.

**Failure handling:** Correct routing through the supported unlink or unskip operation.

### Implementation profiles

[PR-D-INCIDENT](profiles.html#PR-D-INCIDENT)

**Detailed guide:** [D-06](../guides/devops.html#D-06)

## UC-D02 — Investigate a service incident

**Actor:** Incident investigator

**Objective:** Establish an explanation supported by current incident evidence.

A service owner sees elevated errors after a deployment. The investigation begins with the affected service, incident time, and symptoms, not with an assumed deployment defect. Connect the available logs, metrics, traces, repository context, and deployment records, then inspect how the investigation relates the observations across those sources.

The useful result identifies the measurements that support each explanation and the sources that could not be read. A deployment timestamp may provide a lead, but its proximity to the error increase is not sufficient proof of cause. When evidence conflicts, preserve the competing explanations and supply the missing observation through investigation steering rather than turning a plausible summary into a confirmed diagnosis.

### Completion criteria

- Affected service and UTC interval are explicit.

- Competing explanations and unavailable sources are retained.

- The conclusion follows current observations or remains inconclusive.

### Workflow and dependencies

#### 1. Read current observations

Establish the present symptom and affected scope.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 2. Compare historical context

Treat prior causes as hypotheses, not predetermined answers.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-RECALL](mechanisms.html#MX-D-RECALL)

**Dependency:** optional — Relevant historical context is available.

**Configuration features:** [FT-D-MEMORY](features.html#FT-D-MEMORY)

**Effect:** Context read

**Verification:** Distinguish entry existence, observable retrieval and correctness against current evidence.

**Failure handling:** Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.

#### 3. Investigate and reconsider hypotheses

Use current evidence and relevant operator steering.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-INVESTIGATE](mechanisms.html#MX-D-INVESTIGATE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-INCIDENT](features.html#FT-D-INCIDENT), [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Investigation record

**Verification:** Check conclusions against current observations and identify missing evidence.

**Failure handling:** Retain competing hypotheses or an inconclusive result instead of inventing certainty.

#### 4. Record a verified correction

Preserve the actual cause when a completed diagnosis was wrong.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-FEEDBACK](mechanisms.html#MX-D-FEEDBACK)

**Dependency:** conditional — A completed investigation requires verified correction.

**Configuration features:** [FT-D-INCIDENT](features.html#FT-D-INCIDENT), [FT-D-MEMORY](features.html#FT-D-MEMORY)

**Effect:** Retained correction

**Verification:** Inspect saved feedback and any exposed corrective entry.

**Failure handling:** Keep the verified correction in the incident system when downstream use cannot be observed.

### Variant: New incident

Current evidence is sufficient to begin; prior history is not required.

Missing history never excuses missing current telemetry.

### Variant: Recurring alarm

Read relevant monitor context and compare it with new observations.

Record knowledge existence, observed retrieval and diagnosis correctness separately.

### Variant: Operator steering

Supply contrary evidence within the active investigation.

Steering does not authorize a production mutation.

### Implementation profiles

[PR-D-INCIDENT](profiles.html#PR-D-INCIDENT), [PR-EVIDENCE](profiles.html#PR-EVIDENCE)

**Detailed guide:** [D-01](../guides/devops.html#D-01), [D-06](../guides/devops.html#D-06), [D-M01](../guides/devops.html#D-M01), [D-03](../guides/devops.html#D-03), [D-12](../guides/devops.html#D-12), [D-M07](../guides/devops.html#D-M07), [D-M02](../guides/devops.html#D-M02)

## UC-D03 — Prepare a mitigation plan

**Actor:** Incident owner

**Objective:** Prepare a proposed change that a reviewer can approve, reject or revise.

Once the current evidence supports a likely failure mechanism, the incident owner needs a mitigation that can be reviewed. Ask for the proposed target, exact change, expected effect, risks, rollback, and recovery checks. Compare that proposal with the approved runbook and the evidence already collected, especially where the proposed action would affect another service.

The output is a decision document: it should make it possible to approve, reject, or revise the proposal without guessing its effect. A generated plan remains separate from execution. It can be carried out through the ordinary engineering process, or through an eligible directed-action path after the additional controls described in the next use case have been satisfied.

### Completion criteria

- Target and proposed effect are explicit.

- Risk, rollback and recovery checks are reviewable.

- Planning has not been represented as execution.

### Workflow and dependencies

#### 1. Review the incident explanation

Use evidence appropriate to the proposed mitigation.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-INVESTIGATE](mechanisms.html#MX-D-INVESTIGATE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-INCIDENT](features.html#FT-D-INCIDENT), [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Investigation record

**Verification:** Check conclusions against current observations and identify missing evidence.

**Failure handling:** Retain competing hypotheses or an inconclusive result instead of inventing certainty.

#### 2. Review the proposed mitigation

Compare target, effect, risk and rollback with the approved procedure.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-INCIDENT](profiles.html#PR-D-INCIDENT)

**Detailed guide:** [D-06](../guides/devops.html#D-06), [D-M06](../guides/devops.html#D-M06)

## UC-D04 — Execute an approved mitigation and verify recovery

**Actor:** Authorized incident operator

**Objective:** Carry out an eligible approved change and assess service recovery.

An incident owner has accepted a narrowly scoped mitigation and wants to use the documented action path. Confirm Agent Space enablement, the target-account role or connected-tool configuration, and the classification of the operation. Review the actual parameters presented for approval; a broadly named role is not the approval record.

After the operator approves the eligible action, inspect the resulting resource state and the available attribution evidence. Recovery must still be checked against service measurements. If execution is denied, locate the failed gate instead of widening all permissions. This workflow does not convert the earlier mitigation recommendation into standing authorization for subsequent changes.

### Completion criteria

- Exact operation and target were approved.

- Attributed resulting state is retained.

- Recovery is assessed against current service measurements.

### Workflow and dependencies

#### 1. Authorize and execute the eligible action

Apply the specific reviewed operation rather than standing authorization.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-ACTION](mechanisms.html#MX-D-ACTION)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-ACTIONS](features.html#FT-D-ACTIONS)

**Effect:** Resource or external-tool mutation

**Verification:** Inspect exact approval, attribution and resulting resource state.

**Failure handling:** Stop on a failed authorization gate; use the normal approved engineering process rather than bypassing it.

#### 2. Measure post-change service state

Determine whether the action had its intended effect.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 3. Decide whether recovery is established

Apply the declared recovery or rollback conditions.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-ACTION](profiles.html#PR-D-ACTION)

**Detailed guide:** [D-M06](../guides/devops.html#D-M06), [D-03](../guides/devops.html#D-03), [D-12](../guides/devops.html#D-12)

## UC-D05 — Prepare an incident-status bulletin

**Actor:** Incident commander

**Objective:** Explain what changed in an active incident during a short observation window.

During an active incident, the incident commander needs a brief update that explains what has changed since the preceding observation. Configure a specialist task with the incident identifier, selected telemetry tools, and a short explicit lookback window. Ask for changed measurements, the status of open hypotheses, missing reads, and the next check rather than a repetition of the whole incident history.

A report can analyze minute-resolution measurements without arriving every minute. The documented custom-agent schedule uses a flexible window of up to 30 minutes; execution time is additional. For time-critical updates, invoke the task on demand or use a separately tested triggering design. Record both the measurement window and report-generation time so a delayed bulletin is not mistaken for current telemetry.

### Completion criteria

- Incident and measurement window are identified.

- Changed facts, hypotheses and next check are stated.

- Generation time is distinguished from observation time.

### Workflow and dependencies

#### 1. Read the current incident signals

Obtain the measurements for the declared short window.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 2. Prepare a delta-focused bulletin

Use the configured reporting procedure and inspect its invocation.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-CUSTOM](mechanisms.html#MX-D-CUSTOM)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-CUSTOM](features.html#FT-D-CUSTOM), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Execution and output

**Verification:** Inspect tool arguments, failures and output against the task scope.

**Failure handling:** Mark incomplete output and resolve the failed prerequisite before repeating the run.

#### 3. Create recurring bulletin work

Repeat only within accepted timing constraints.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-SCHEDULE](mechanisms.html#MX-D-SCHEDULE)

**Dependency:** conditional — A non-real-time recurring profile is approved.

**Configuration features:** [FT-D-SCHEDULE](features.html#FT-D-SCHEDULE), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Future invocation

**Verification:** Inspect saved timing and actual start; record the observation window independently.

**Failure handling:** Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.

### Variant: On-demand bulletin

Invoke for a specific lookback period.

Execution may lag the measurement window.

### Variant: Recurring bulletin

Configure a supported trigger.

Flexible scheduling does not guarantee minute-by-minute delivery.

### Implementation profiles

[PR-D-REPORT](profiles.html#PR-D-REPORT)

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12)

## UC-D06 — Assess and report service health and trends

**Actor:** On-call or service engineer

**Objective:** Produce a sourced health assessment or comparable-period report.

The incoming engineer needs to know whether the service is healthy, what changed, and which observations are missing. Define the service scope and reporting period first. Retrieve the selected measurements, compare significant differences with a baseline when needed, and connect material observations to incident and deployment evidence. A recent snapshot and a multiweek trend are analytical profiles of the same reporting objective.

Review a material measurement against its source before relying on the report. Keep missing telemetry visible and consider workload changes before interpreting a trend. Recurrence preserves the agreed reporting basis; it does not create a different objective. An operational review can subsequently use this report to decide priorities and owners.

### Completion criteria

- Service dimensions and observation periods are explicit.

- Material measurements reconcile with source queries.

- Missing data and workload-mix changes are disclosed.

### Workflow and dependencies

#### 1. Retrieve comparable measurements

Read logs, metrics and incidents under one reporting basis.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 2. Answer a native health inquiry

Use the built-in query path for the native snapshot profile.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-QUERY](mechanisms.html#MX-D-QUERY)

**Dependency:** conditional — The built-in conversational snapshot profile is selected.

**Configuration features:** [FT-D-QUERY](features.html#FT-D-QUERY), [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read and conversational result

**Verification:** Inspect scope and reproduce a material observation from the same source query.

**Failure handling:** Name the missing source and qualify or withhold the answer; creating a custom agent does not by itself repair source access.

#### 3. Interpret retained service context

Resolve known mappings or relationships when relevant.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-RECALL](mechanisms.html#MX-D-RECALL)

**Dependency:** optional — The report uses maintained service context.

**Configuration features:** [FT-D-MEMORY](features.html#FT-D-MEMORY)

**Effect:** Context read

**Verification:** Distinguish entry existence, observable retrieval and correctness against current evidence.

**Failure handling:** Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.

#### 4. Run the reporting definition

Produce the configured snapshot, comparison or trend report.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-CUSTOM](mechanisms.html#MX-D-CUSTOM)

**Dependency:** conditional — A configured snapshot, comparison or recurring-report profile is selected.

**Configuration features:** [FT-D-CUSTOM](features.html#FT-D-CUSTOM), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Execution and output

**Verification:** Inspect tool arguments, failures and output against the task scope.

**Failure handling:** Mark incomplete output and resolve the failed prerequisite before repeating the run.

#### 5. Create recurring invocations

Repeat the reporting contract without changing its basis.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-SCHEDULE](mechanisms.html#MX-D-SCHEDULE)

**Dependency:** conditional — Recurring execution of the configured reporting profile is selected.

**Configuration features:** [FT-D-SCHEDULE](features.html#FT-D-SCHEDULE), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Future invocation

**Verification:** Inspect saved timing and actual start; record the observation window independently.

**Failure handling:** Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.

### Variant: Current snapshot

A bounded recent observation of the selected service.

An unavailable source is a gap, not a healthy measurement.

### Variant: Period or trend comparison

Compare complete periods under the same dimensions and aggregation.

Check denominator, traffic composition and source completeness.

### Variant: Recurring service report

Run a reviewed definition repeatedly.

Schedule, observation window and destination remain separate settings.

### Implementation profiles

[PR-D-QUERY](profiles.html#PR-D-QUERY), [PR-D-REPORT](profiles.html#PR-D-REPORT), [PR-EVIDENCE](profiles.html#PR-EVIDENCE)

**Detailed guide:** [D-01](../guides/devops.html#D-01), [D-05](../guides/devops.html#D-05), [D-12](../guides/devops.html#D-12), [D-07](../guides/devops.html#D-07), [D-M07](../guides/devops.html#D-M07), [D-03](../guides/devops.html#D-03), [D-M01](../guides/devops.html#D-M01)

## UC-D07 — Review deployment and change activity

**Actor:** Release engineer

**Objective:** Establish which deployments and rollbacks affected the selected services.

A release engineer wants to review the changes delivered during the previous week. The input is deployment history with service and revision identifiers, not simply merged pull requests. Configure the task to distinguish attempted, successful, failed, and rolled-back deployments using the states exposed by the connected delivery tools.

The result should make it possible to trace a reported deployment to its source record and compare it with incidents in the same service and period. Similar timestamps are useful for investigation but do not establish causality. Missing pipeline access or ambiguous status mappings should be listed explicitly so the report is not presented as a complete release history.

### Completion criteria

- Deployment states and immutable revisions are traceable.

- Source gaps are explicit.

- Temporal association is not presented as proven cause.

### Workflow and dependencies

#### 1. Read delivery evidence

Use actual deployment records rather than merged changes.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 2. Prepare the activity review

Normalize supported source states and expose unresolved mappings.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-CUSTOM](mechanisms.html#MX-D-CUSTOM)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-CUSTOM](features.html#FT-D-CUSTOM), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Execution and output

**Verification:** Inspect tool arguments, failures and output against the task scope.

**Failure handling:** Mark incomplete output and resolve the failed prerequisite before repeating the run.

#### 3. Repeat the activity review

Cover the declared complete period.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-SCHEDULE](mechanisms.html#MX-D-SCHEDULE)

**Dependency:** conditional — Recurring reporting is selected.

**Configuration features:** [FT-D-SCHEDULE](features.html#FT-D-SCHEDULE), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Future invocation

**Verification:** Inspect saved timing and actual start; record the observation window independently.

**Failure handling:** Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.

### Implementation profiles

[PR-D-REPORT](profiles.html#PR-D-REPORT), [PR-EVIDENCE](profiles.html#PR-EVIDENCE)

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12)

## UC-D08 — Identify recurring incident patterns

**Actor:** Reliability engineer

**Objective:** Identify cross-incident conditions supported by investigation evidence.

Several investigations may share an operational weakness even when they were triggered by different alarms. Review the relevant investigation history and ask which causes or contributing conditions recur. Group the evidence by the proposed pattern and retain the supporting investigation identifiers so the grouping can be challenged.

This analysis differs from retrieving the prior cause of one alarm: its purpose is to identify cross-incident themes worth prevention work. Similar symptoms without verified common causes should remain a candidate pattern. The next step is to review the prevention recommendations against those themes rather than assuming that a historical cluster explains the next incident.

### Completion criteria

- Supporting investigation identities are retained.

- Similar symptoms are distinguished from shared verified causes.

- Proposed groupings can be challenged and revised.

### Workflow and dependencies

#### 1. Inspect historical context

Locate recurring themes without assuming an identical cause.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-RECALL](mechanisms.html#MX-D-RECALL)

**Dependency:** optional — Relevant retained history is available.

**Configuration features:** [FT-D-MEMORY](features.html#FT-D-MEMORY)

**Effect:** Context read

**Verification:** Distinguish entry existence, observable retrieval and correctness against current evidence.

**Failure handling:** Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.

#### 2. Evaluate investigation history

Examine common weaknesses across investigations.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-PREVENT](mechanisms.html#MX-D-PREVENT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-PREVENTION](features.html#FT-D-PREVENTION)

**Effect:** Recommendation

**Verification:** Trace a proposed theme or improvement to supporting investigations.

**Failure handling:** Keep unsupported patterns as hypotheses and separate proposals from implemented changes.

#### 3. Review the pattern grouping

Check each grouping against the cited investigations.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-INCIDENT](profiles.html#PR-D-INCIDENT)

**Detailed guide:** [D-M01](../guides/devops.html#D-M01), [D-06](../guides/devops.html#D-06), [D-M07](../guides/devops.html#D-M07)

## UC-D09 — Prioritize incident-prevention work

**Actor:** Reliability owner

**Objective:** Turn evidence-backed improvement proposals into owned engineering work.

The reliability owner has identified recurring themes and needs a manageable prevention backlog. Run or inspect the documented prevention evaluation, then review each recommendation against the incidents it addresses. Separate observability improvements, infrastructure changes, governance work, and code changes because they have different owners and acceptance evidence.

Keep an accepted recommendation linked to its source evidence and normal change process. A recommendation’s priority or estimated effect is not proof that the change has been implemented. During the next operational review, inspect actual progress and post-change observations. This closes the team’s improvement loop without claiming autonomous implementation or measured benefit before either exists.

### Completion criteria

- Accepted proposals retain source incidents.

- An owner and acceptance criterion are assigned.

- Proposal status is distinct from implementation evidence.

### Workflow and dependencies

#### 1. Inspect the prevention evaluation

Identify proposals relevant to recurring weaknesses.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-PREVENT](mechanisms.html#MX-D-PREVENT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-PREVENTION](features.html#FT-D-PREVENTION)

**Effect:** Recommendation

**Verification:** Trace a proposed theme or improvement to supporting investigations.

**Failure handling:** Keep unsupported patterns as hypotheses and separate proposals from implemented changes.

#### 2. Prioritize and assign accepted work

Compare risk, dependencies and implementation effort through normal team review.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-INCIDENT](profiles.html#PR-D-INCIDENT)

**Detailed guide:** [D-06](../guides/devops.html#D-06)

## UC-D10 — Consolidate and maintain operational procedures

**Actor:** Runbook owner

**Objective:** Maintain one reviewed procedure for the intended operational situation.

A team has several overlapping timeout SOPs maintained by different owners. First reconcile their scope, resolve contradictory steps, remove stale tool names, and identify the approved procedure. Only then package that procedure as a skill with a description that states when it applies and which agent types may use it.

Keep the reviewed source in Git and test a request that should match the skill alongside one that should not. The supporting references should explain the expected observations and the point at which the procedure stops or escalates. Consolidation is authored team work; skill selection is the platform mechanism. A skill neither creates the referenced tools nor grants permission to use them.

### Completion criteria

- Conflicting or stale instructions are resolved.

- Actual tools and stop conditions are defined.

- Applicability tests include matching and nonmatching requests.

### Workflow and dependencies

#### 1. Reconcile authoritative procedures

Resolve conflicting scope, stale commands and ownership before packaging.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 2. Publish and test the procedural skill

Make the reviewed procedure available to the intended agent scope.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-SKILL](mechanisms.html#MX-D-SKILL)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SKILLS](features.html#FT-D-SKILLS)

**Effect:** Procedural context

**Verification:** Test matching and nonmatching requests and inspect exposed procedure or tool-use evidence.

**Failure handling:** Correct applicability or missing tools; stop unsupported steps without implicitly widening permissions.

### Implementation profiles

[PR-D-PROCEDURE](profiles.html#PR-D-PROCEDURE)

**Detailed guide:** [D-M04](../guides/devops.html#D-M04)

## UC-D11 — Document service topology and dependencies

**Actor:** Service owner

**Objective:** Produce a reviewed service and dependency description.

A service owner needs an architecture description before changing a dependency. Start from discovered resources and the topology’s service, repository, pipeline, and dependency relationships. Compare those relationships with the deployed configuration and source revision, distinguishing directly observed relationships from inferred ones.

Write the reviewed result as a maintained service description with identifiers, evidence links, and unresolved edges. The topology is useful input to that document, but it is not a guaranteed complete inventory or an automatic update to the team’s architecture repository. This use case produces owner-reviewed documentation; the following refresh use case checks whether the underlying environment model has changed.

### Completion criteria

- Observed and inferred relationships are distinguished.

- Deployed revision and evidence are recorded.

- Unresolved relationships have owners.

### Workflow and dependencies

#### 1. Inspect environment consolidation

Use discovery and the resulting retained representation.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-TOPOLOGY](mechanisms.html#MX-D-TOPOLOGY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-TOPOLOGY](features.html#FT-D-TOPOLOGY), [FT-D-MEMORY](features.html#FT-D-MEMORY)

**Effect:** Retained context update

**Verification:** Check a known changed resource and relationship in the resulting version.

**Failure handling:** Mark stale or inferred relationships; do not substitute the graph for current configuration.

#### 2. Check important source relationships

Compare graph edges with deployment and source evidence.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 3. Maintain the reviewed description

Record owner-verified relationships and unresolved discrepancies.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-KNOWLEDGE](profiles.html#PR-D-KNOWLEDGE), [PR-EVIDENCE](profiles.html#PR-EVIDENCE)

**Detailed guide:** [D-05](../guides/devops.html#D-05), [D-12](../guides/devops.html#D-12), [D-M08](../guides/devops.html#D-M08), [D-03](../guides/devops.html#D-03)

## UC-D12 — Audit resource configurations against approved standards

**Actor:** Platform engineer

**Objective:** Assess selected resource settings against an explicit operational standard.

An operations standard requires a small set of staging resources to have particular logging and access settings. Configure a custom task with read-only configuration tools, the explicit resource list, and the reviewed standard. Each reported finding should identify the resource, the applicable rule, and the actual value that was read.

Review a known conforming and a known nonconforming example before scheduling the task. An unavailable read is an unassessed resource, not a pass. The output is a scoped configuration audit for the chosen rules; it is not a built-in universal compliance engine or permission to repair findings automatically.

### Completion criteria

- Each finding identifies resource, rule and observed value.

- Unreadable resources remain unassessed.

- An audit result does not imply permission to repair it.

### Workflow and dependencies

#### 1. Load the reviewed audit procedure

Apply the scoped rules using actual tool references.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-SKILL](mechanisms.html#MX-D-SKILL)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SKILLS](features.html#FT-D-SKILLS)

**Effect:** Procedural context

**Verification:** Test matching and nonmatching requests and inspect exposed procedure or tool-use evidence.

**Failure handling:** Correct applicability or missing tools; stop unsupported steps without implicitly widening permissions.

#### 2. Read selected resource settings

Obtain the observations needed for each rule.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READ](mechanisms.html#MX-D-READ)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Source read

**Verification:** Compare returned identifiers and a material measurement with the original source.

**Failure handling:** Report the failed read and withhold conclusions that require that source.

#### 3. Run the configured audit

Produce findings and an explicit unassessed-resource record.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-CUSTOM](mechanisms.html#MX-D-CUSTOM)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-CUSTOM](features.html#FT-D-CUSTOM), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Execution and output

**Verification:** Inspect tool arguments, failures and output against the task scope.

**Failure handling:** Mark incomplete output and resolve the failed prerequisite before repeating the run.

### Implementation profiles

[PR-D-REPORT](profiles.html#PR-D-REPORT)

**Detailed guide:** [D-07](../guides/devops.html#D-07), [D-M04](../guides/devops.html#D-M04), [D-12](../guides/devops.html#D-12), [D-03](../guides/devops.html#D-03)

## UC-D13 — Assess release readiness

**Actor:** Release reviewer

**Objective:** Assess an eligible proposed revision for operational risk.

Before release, a team wants to examine a retry-policy change for operational risk. Use the eligible readiness-review path with the candidate revision, relevant repositories, topology, and release context. Review the findings against the intended dependency behavior and the service’s existing resilience assumptions.

A readiness review analyzes a proposed change; it does not prove that the deployed application behaves correctly. Retain unresolved dependencies and scope limitations and route accepted findings through engineering review. This feature is a separate preview path, so production-operations availability must not be used as evidence that the same review is available for every Region or repository.

### Completion criteria

- The candidate revision is unambiguous.

- Findings identify dependencies and limitations.

- Source analysis is not treated as deployed-behavior verification.

### Workflow and dependencies

#### 1. Analyze the eligible candidate

Review the proposed change with available operational context.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-READINESS](mechanisms.html#MX-D-READINESS)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-READINESS](features.html#FT-D-READINESS), [FT-D-SOURCES](features.html#FT-D-SOURCES)

**Effect:** Readiness result

**Verification:** Match findings to the exact candidate and unresolved dependencies.

**Failure handling:** Treat unsupported repository or feature access as an unmet prerequisite.

#### 2. Resolve the readiness decision

Evaluate findings and remaining dependencies under the normal release process.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-RELEASE](profiles.html#PR-D-RELEASE)

**Detailed guide:** [D-09](../guides/devops.html#D-09)

## UC-D14 — Test a deployed application release

**Actor:** Application test owner

**Objective:** Observe release behavior on an authorized disposable target.

A staging application is ready for an active release check. Prepare disposable test data, approved identities, explicit allowed operations, and disabled external side effects. The task exercises the deployed target, so the target revision and reachable endpoints matter more than the name of the branch that produced it.

Review the observed requests and results with the application owner. Active testing can create, modify, or delete application data; infrastructure read permissions do not make those requests harmless. The result describes the executed test and its uncovered areas, not blanket release approval. Unexpected effects require stopping and reviewing the configuration before further execution.

### Completion criteria

- Target revision, identities and permitted effects are explicit.

- Executed behavior and incomplete coverage are retained.

- Unexpected effects stop further testing.

### Workflow and dependencies

#### 1. Exercise the approved target

Test actual application behavior instead of inferring it from source review.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-TEST](mechanisms.html#MX-D-TEST)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-D-TEST](features.html#FT-D-TEST)

**Effect:** Application requests with possible writes

**Verification:** Inspect target revision, actual interactions, results and effects.

**Failure handling:** Stop unexpected effects and retain incomplete coverage.

#### 2. Interpret the observed behavior

Review results and uncovered areas with the application owner.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-D-RELEASE](profiles.html#PR-D-RELEASE)

**Detailed guide:** [D-09](../guides/devops.html#D-09)

## UC-S01 — Assess a running application for vulnerabilities

**Actor:** Application security engineer

**Objective:** Assess the explicitly authorized surface and record findings and coverage gaps.

An application owner authorizes assessment of a deployed release. Establish the target surface, permitted effects, source context and execution limit before starting. Public versus private access and authenticated versus unauthenticated testing are independent configuration choices: they determine which paths can be examined, not four independent operational objectives.

Review the saved configuration and follow the resulting run. Record actual revision, roles reached, exclusions, findings and incomplete areas. A recurring schedule or pipeline may initiate later runs, but cannot preserve credentials or target state that have since changed. Interpret an absence of findings only within the paths actually assessed.

### Completion criteria

- Target revision and owner authorization are retained.

- Reached roles and paths are known.

- Failures and exclusions remain coverage limitations.

### Workflow and dependencies

#### 1. Assemble application context

Select source evidence matching the application and intended revision.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CONTEXT](mechanisms.html#MX-S-CONTEXT)

**Dependency:** optional — Source code or documentation is selected to enrich application context.

**Configuration features:** [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Source read

**Verification:** Compare source revision and system boundary with the intended subject.

**Failure handling:** Exclude mismatched context and document the resulting assessment limitation.

#### 2. Configure target access

Define public or private reachability without widening authority.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-ACCESS](mechanisms.html#MX-S-ACCESS)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-TARGET](features.html#FT-S-TARGET)

**Effect:** Target connection

**Verification:** Confirm the permitted surface and exclusions in an authorized environment.

**Failure handling:** Stop when scope or owner authorization is unresolved.

#### 3. Authenticate the intended role

Reach the protected paths required by the profile.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-AUTH](mechanisms.html#MX-S-AUTH)

**Dependency:** conditional — The profile includes authenticated paths.

**Configuration features:** [FT-S-AUTH](features.html#FT-S-AUTH)

**Effect:** Authentication requests

**Verification:** Check the actual application identity and protected route, not only credential retrieval.

**Failure handling:** Mark protected paths unassessed when login fails.

#### 4. Reuse a successful login procedure

Use documented navigation reuse without assuming it proves coverage.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-LOGIN](mechanisms.html#MX-S-LOGIN)

**Dependency:** optional — A usable retained procedure and its reuse setting are available.

**Configuration features:** [FT-S-LOGIN](features.html#FT-S-LOGIN)

**Effect:** Authentication requests

**Verification:** Distinguish successful login from observable procedure reuse.

**Failure handling:** Retest a changed login flow; failed login is not a clean assessment.

#### 5. Execute and inspect the run

Retain actual findings, target state and unassessed areas.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-RUN](mechanisms.html#MX-S-RUN)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-RUNS](features.html#FT-S-RUNS), [FT-S-FINDINGS](features.html#FT-S-FINDINGS)

**Effect:** Active application assessment

**Verification:** Record actual revision, roles, exclusions, limit and incomplete areas.

**Failure handling:** Treat incomplete or failed execution as a coverage gap, not a pass.

### Variant: Public or private network

Choose the actual target route.

Private reachability does not extend authorized scope.

### Variant: Unauthenticated or selected roles

Choose the application identities to assess.

Login failure leaves protected paths unassessed.

### Variant: Manual, recurring or pipeline invocation

Choose a supported trigger.

Each run records its own target revision, identities, limits and coverage.

### Implementation profiles

[PR-S-ASSESS](profiles.html#PR-S-ASSESS), [PR-S-PIPELINE](profiles.html#PR-S-PIPELINE)

**Detailed guide:** [S-01](../guides/security.html#S-01), [S-03](../guides/security.html#S-03), [S-04](../guides/security.html#S-04), [S-M01](../guides/security.html#S-M01), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07), [S-M02](../guides/security.html#S-M02)

## UC-S02 — Review source code for security issues

**Actor:** Application security reviewer

**Objective:** Assess an identified source revision for vulnerabilities and selected requirements.

A team wants a baseline review of a repository or supported source package. Connect the intended source revision and select the eligible review modes. Vulnerability analysis and evaluation against enabled requirement packs answer related but different questions, so the requested criteria should be explicit.

Review findings in their code context and inspect preflight failures separately from completed analysis. The result applies to the selected source and modes; it is not a substitute for testing the deployed application. This preview workflow has provider and availability boundaries that must be checked before it becomes part of the delivery process.

### Completion criteria

- Review mode and exact revision are known.

- Findings retain source context.

- Preflight failure and stale results are explicit.

### Workflow and dependencies

#### 1. Read selected source context

Use the revision and repository intended for review.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CONTEXT](mechanisms.html#MX-S-CONTEXT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Source read

**Verification:** Compare source revision and system boundary with the intended subject.

**Failure handling:** Exclude mismatched context and document the resulting assessment limitation.

#### 2. Run the selected review mode

Review a baseline or supported change-focused source.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CODE](mechanisms.html#MX-S-CODE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-CODE](features.html#FT-S-CODE), [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Source analysis; optional comments separately configured

**Verification:** Match results to the revision and record unassessed scope.

**Failure handling:** Obtain a current result when revision or trigger behavior makes prior evidence stale.

#### 3. Evaluate applicable requirements

Apply reviewed organizational criteria.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CRITERIA](mechanisms.html#MX-S-CRITERIA)

**Dependency:** conditional — Requirement evaluation is selected.

**Configuration features:** [FT-S-REQUIREMENTS](features.html#FT-S-REQUIREMENTS)

**Effect:** Assessment result

**Verification:** Check compliant, violating and inapplicable examples.

**Failure handling:** Revise ambiguous applicability; do not treat a pack as a compliance certificate.

#### 4. Review returned evidence

Decide which findings require further work.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-FINDING](mechanisms.html#MX-S-FINDING)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-FINDINGS](features.html#FT-S-FINDINGS)

**Effect:** Finding review record

**Verification:** Give the finding a disposition using evidence, impact and application-owner context.

**Failure handling:** Preserve uncertainty and obtain missing evidence before closure.

### Variant: Full-source baseline

Analyze the selected full source scope.

The result does not test the deployed application.

### Variant: Change-focused review

Analyze an eligible change with surrounding context.

Further revisions require matching review evidence under provider-specific behavior.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-M03](../guides/security.html#S-M03), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07), [S-05](../guides/security.html#S-05)

## UC-S03 — Review a proposed application design

**Actor:** Architect and security reviewer

**Objective:** Evaluate a current design against applicable security requirements.

A team proposes a new payment-service design before implementation. Submit the current design material and relevant application context for the eligible review, and identify the enabled requirements that govern it. The assessment should expose assumptions about identity, data flows, and trust boundaries that need owner confirmation.

Review the findings with the architect and distinguish missing design evidence from a demonstrated violation. Design review has a one-off lifecycle, with cloning used for a new review; it should not be described as an automatically refreshed continuous model. The result informs design work rather than approving the future implementation.

### Completion criteria

- Design revision and assumptions are explicit.

- Missing evidence is separate from a demonstrated violation.

- Accepted findings have owners.

### Workflow and dependencies

#### 1. Select current design evidence

Identify the intended system and design revision.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CONTEXT](mechanisms.html#MX-S-CONTEXT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Source read

**Verification:** Compare source revision and system boundary with the intended subject.

**Failure handling:** Exclude mismatched context and document the resulting assessment limitation.

#### 2. Apply reviewed criteria

Evaluate the requirements applicable to the design.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CRITERIA](mechanisms.html#MX-S-CRITERIA)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-REQUIREMENTS](features.html#FT-S-REQUIREMENTS)

**Effect:** Assessment result

**Verification:** Check compliant, violating and inapplicable examples.

**Failure handling:** Revise ambiguous applicability; do not treat a pack as a compliance certificate.

#### 3. Inspect the point-in-time assessment

Record findings and unresolved architectural assumptions.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-DESIGN](mechanisms.html#MX-S-DESIGN)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-DESIGN](features.html#FT-S-DESIGN)

**Effect:** Review result

**Verification:** Separate missing evidence from demonstrated violation.

**Failure handling:** Use the documented new-review or clone path for changed design material.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07), [S-M03](../guides/security.html#S-M03)

## UC-S04 — Develop and review an application threat model

**Actor:** Threat-model reviewer

**Objective:** Produce a reviewed system representation and evidence-backed threats for a defined scope.

A service boundary has changed and the team needs an updated threat model. Supply explicit scope documents and the relevant architecture and source evidence. Review the inferred system overview, components, data flows, and trust boundaries before evaluating individual threats.

Correct an incorrect boundary at the model input rather than dismissing every threat that follows from it. Retain evidence for the accepted threats and identify inferred relationships that remain unverified. The result is a reviewed model for that scope and run, not proof that every possible threat has been discovered.

### Completion criteria

- Boundaries and flows are reviewed before threats.

- Source assumptions and inferred edges remain visible.

- Threat dispositions refer to the selected model run.

### Workflow and dependencies

#### 1. Assemble scope and source inputs

Separate analytical focus from implementation context.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CONTEXT](mechanisms.html#MX-S-CONTEXT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Source read

**Verification:** Compare source revision and system boundary with the intended subject.

**Failure handling:** Exclude mismatched context and document the resulting assessment limitation.

#### 2. Construct and review the model

Examine system boundaries before individual threats.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-THREAT](mechanisms.html#MX-S-THREAT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-THREAT](features.html#FT-S-THREAT), [FT-S-SOURCES](features.html#FT-S-SOURCES)

**Effect:** Model result

**Verification:** Review inferred boundaries before interpreting individual threats.

**Failure handling:** Correct input scope when the model represents the wrong system.

#### 3. Resolve model assumptions

Correct inputs and assign unresolved relationships to owners.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

## UC-S05 — Triage and prioritize security findings

**Actor:** Finding owner

**Objective:** Give findings an evidence-based disposition and accountable next action.

A completed assessment contains findings of different severity and evidential strength. Review each material finding in the context of the affected revision, reachable role, exposed data, and reproduction evidence. Add application-owner context before deciding which finding needs immediate repair and which requires more investigation.

The outcome is a disposition and an accountable next action, not merely a sorted severity list. Findings with incomplete evidence should retain that uncertainty. Link accepted work to the original finding identifier so remediation, deployment, and later verification remain traceable even if the issue title or owner changes.

### Completion criteria

- Impact and evidence are reviewed.

- Finding identity is preserved.

- Accepted work has an owner and acceptance test.

### Workflow and dependencies

#### 1. Review the finding in context

Evaluate the affected revision, application role and supporting evidence.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-FINDING](mechanisms.html#MX-S-FINDING)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-FINDINGS](features.html#FT-S-FINDINGS)

**Effect:** Finding review record

**Verification:** Give the finding a disposition using evidence, impact and application-owner context.

**Failure handling:** Preserve uncertainty and obtain missing evidence before closure.

#### 2. Assign priority and responsibility

Use application impact and evidence rather than severity alone.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 3. Publish accepted work to Jira

Preserve finding linkage in an appropriate project.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-JIRA](mechanisms.html#MX-S-JIRA)

**Dependency:** optional — A permitted destination and disclosure scope are configured.

**Configuration features:** [FT-S-JIRA](features.html#FT-S-JIRA)

**Effect:** External publication

**Verification:** Inspect actual project audience and original finding linkage.

**Failure handling:** Keep the finding owned locally while resolving publication failure.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-05](../guides/security.html#S-05), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

## UC-S06 — Prepare a code-remediation proposal

**Actor:** Developer and security reviewer

**Objective:** Produce a reviewable source change for an accepted finding.

A developer has accepted a finding and wants a repair proposal against the affected source. Confirm the repository and supported remediation settings, then inspect the proposed patch or pull request. The review should include the security change, regression tests, and any unrelated behavior introduced by the proposal.

Run the normal build and review process before deployment. A generated proposal that fails tests is unfinished work, and a merged revision that has not reached the target is not ready for revalidation. Preserve the finding identifier through the change and deployment records so the next test can evaluate the intended repair.

### Completion criteria

- The proposal matches the affected revision.

- Tests and unrelated changes are reviewed.

- Proposal, deployment and verification remain distinct.

### Workflow and dependencies

#### 1. Confirm the finding evidence

Identify the defect and affected source.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-FINDING](mechanisms.html#MX-S-FINDING)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-FINDINGS](features.html#FT-S-FINDINGS)

**Effect:** Finding review record

**Verification:** Give the finding a disposition using evidence, impact and application-owner context.

**Failure handling:** Preserve uncertainty and obtain missing evidence before closure.

#### 2. Create the supported repair proposal

Produce the configured patch or pull request.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-FIX](mechanisms.html#MX-S-FIX)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-FIX](features.html#FT-S-FIX)

**Effect:** Proposed repository change

**Verification:** Inspect revision, tests and unrelated changes before accepting the proposal.

**Failure handling:** Leave a failed or rejected proposal unfinished; merge is not deployment.

#### 3. Review and test the candidate

Use the normal build and review process; arrange deployment separately.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-05](../guides/security.html#S-05), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

## UC-S07 — Revalidate a finding after deployment of a repair

**Actor:** Verification owner

**Objective:** Determine whether a selected issue still reproduces under valid current test conditions.

The reviewed repair has been deployed to the original authorized environment. Select the existing finding for revalidation and inspect the new job, including the current authentication configuration and target revision. The job repeats the selected validation steps rather than conducting a broad new assessment.

Interpret the result within that scope. A reproduced finding remains active evidence of the issue; non-reproduction supports resolution only when the relevant identity and path were actually reached. Keep the original finding and the linked job history. A failed login or changed test environment must not be mistaken for a successful repair.

### Completion criteria

- The intended repair is deployed to the target.

- The relevant identity and path were reached.

- The linked job records reproduction, non-reproduction or an inconclusive result.

### Workflow and dependencies

#### 1. Confirm deployed repair and target

Match the finding, source change and actual deployed revision.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 2. Check current test authentication

Avoid interpreting an inaccessible path as repair.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-AUTH](mechanisms.html#MX-S-AUTH)

**Dependency:** conditional — The selected finding requires authenticated access.

**Configuration features:** [FT-S-AUTH](features.html#FT-S-AUTH)

**Effect:** Authentication requests

**Verification:** Check the actual application identity and protected route, not only credential retrieval.

**Failure handling:** Mark protected paths unassessed when login fails.

#### 3. Run selected revalidation

Retest the original finding and preserve its lineage.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-REVALIDATE](mechanisms.html#MX-S-REVALIDATE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-REVALIDATION](features.html#FT-S-REVALIDATION)

**Effect:** Targeted active test

**Verification:** Verify reached identity, deployed repair and linked result.

**Failure handling:** Record authentication or environment failure as inconclusive verification.

### Implementation profiles

[PR-S-ASSESS](profiles.html#PR-S-ASSESS)

**Detailed guide:** [S-M05](../guides/security.html#S-M05), [S-M01](../guides/security.html#S-M01)

## UC-S08 — Consolidate and maintain security requirements

**Actor:** Security policy owner

**Objective:** Maintain reviewed assessment criteria derived from authoritative policy.

Policy owners have revised several overlapping security standards. Reconcile the governing documents and identify the approved source before generating a replacement requirement pack. Compare the generated applicability and compliance statements with that source, including requirements that had previously been added manually.

Regeneration replaces the existing pack contents rather than appending to them. Review the proposed replacement before enabling it for subsequent assessments, and keep the policy and reviewed requirement source in Git. This is a controlled authoring workflow; it must not silently replace a working pack merely because new documents were uploaded.

### Completion criteria

- Conflicting policy sources are reconciled.

- The replacement is compared with prior manual requirements.

- Applicability and criteria are tested before enablement.

### Workflow and dependencies

#### 1. Reconcile governing policy

Identify approved source material and compare existing requirements.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 2. Generate the replacement pack

Treat regeneration as replacement rather than append.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-GENERATE](mechanisms.html#MX-S-GENERATE)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-REQUIREMENTS](features.html#FT-S-REQUIREMENTS)

**Effect:** Configuration replacement

**Verification:** Compare with approved policy and prior manually added requirements.

**Failure handling:** Do not enable an unreviewed replacement; keep authoritative source in Git.

#### 3. Test requirement applicability

Check compliant, violating and inapplicable examples.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-S-CRITERIA](mechanisms.html#MX-S-CRITERIA)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-S-REQUIREMENTS](features.html#FT-S-REQUIREMENTS)

**Effect:** Assessment result

**Verification:** Check compliant, violating and inapplicable examples.

**Failure handling:** Revise ambiguous applicability; do not treat a pack as a compliance certificate.

### Implementation profiles

[PR-S-REVIEW](profiles.html#PR-S-REVIEW)

**Detailed guide:** [S-M04](../guides/security.html#S-M04), [S-M03](../guides/security.html#S-M03)

## UC-F01 — Analyze historical cost and usage

**Actor:** Cost analyst or service engineer

**Objective:** Answer a bounded historical cost question using reproducible source queries.

A service owner asks how expenditure changed and which component requires investigation. Begin with the dates, cost metric, currency, scope and grouping. A total inquiry, owner breakdown and period comparison are analytical profiles of this bounded cost-analysis objective. Use reviewed ownership mappings only where the requested view needs them, and preserve unmapped values.

Reconcile totals and deltas against the same source basis before interpreting them. The largest monetary contribution identifies where to look next; it does not establish why the workload consumed that usage. Keep observed cost separate from forecasts and recommendation estimates, and retain unavailable evidence rather than inventing a single causal explanation.

### Completion criteria

- Dates, metric, currency and filters are explicit.

- Totals and component changes reconcile.

- Unmapped ownership and unexplained causes remain visible.

### Workflow and dependencies

#### 1. Retrieve defined cost evidence

Answer the total, breakdown or variance question under one basis.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 2. Apply ownership context

Use reviewed organization-specific mappings.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-FILES](mechanisms.html#MX-F-FILES)

**Dependency:** conditional — An ownership-enriched profile is selected.

**Configuration features:** [FT-F-FILES](features.html#FT-F-FILES)

**Effect:** Context read

**Verification:** Verify a known mapping and expose unmapped records.

**Failure handling:** Keep unassigned values visible and update the authoritative file deliberately.

#### 3. Reconcile and interpret the result

Check sums and distinguish monetary contribution from operational cause.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Variant: Total inquiry

Return a bounded historical amount.

The amount alone does not explain workload behavior.

### Variant: Dimensional breakdown

Group by supported source dimensions or reviewed ownership.

Keep ambiguous and unassigned records visible.

### Variant: Variance decomposition

Compare complete matched periods.

Contribution arithmetic is distinct from causal proof.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS)

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08), [F-U01](../guides/finops.html#F-U01), [F-M02](../guides/finops.html#F-M02)

## UC-F02 — Review a cost forecast

**Actor:** Cost planning owner

**Objective:** Review a projection for an explicit horizon and assumptions.

A planning owner needs a projection for a defined future period. Specify the horizon, cost basis and account scope, then obtain the supported source forecast. Retain its assumptions and source rather than put the projection in the same column as expenditure already observed.

Review the projection against known workload plans and record limits in the evidence. This outcome is distinct from assessing commitment coverage. A forecast does not authorize a purchase or establish what the next bill will be.

### Completion criteria

- Forecast horizon and source are identified.

- Projected values are separate from observed spending.

- Limitations relevant to planning are recorded.

### Workflow and dependencies

#### 1. Read forecast evidence

Use the supported forecast source and declared horizon.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 2. Review planning assumptions

Compare the projection with known workload plans and record uncertainty.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS)

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

## UC-F03 — Review commitment coverage

**Actor:** Commitment planning owner

**Objective:** Assess coverage of eligible usage by existing commitments.

A commitment planning owner needs to understand how existing commitments cover eligible usage. Specify the commitment type, workload scope and observation period. Inspect coverage directly instead of inferring it from a spending forecast or total account cost.

Review the observation with service owners and distinguish a coverage gap from an instruction to buy. A purchasing decision has separate assumptions and authority. The case ends with a reviewed coverage assessment, not a transaction.

### Completion criteria

- Commitment type, period and eligible scope are explicit.

- Coverage observations are distinct from forecasts.

- No purchasing authorization is implied.

### Workflow and dependencies

#### 1. Read commitment evidence

Inspect the supported commitment scope and period.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 2. Review coverage with service owners

Consider workload constraints before a separate purchasing decision.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS)

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

## UC-F04 — Prepare a periodic cost report

**Actor:** FinOps reporting owner

**Objective:** Produce a comparable report for the defined period and audience.

The team needs a recurring cost report with a stable comparison basis. Define the reporting period, sections, dimensions, audience, and output format before scheduling it. The task should distinguish observed spend, anomalies, and source recommendation estimates so unlike values are not added together.

Review a trial artifact against the source totals and inspect the saved automation separately from the generated task. A weekly schedule does not specify whether the report includes an incomplete current day. Preserve the task identifier and query basis with each report so changes in the template do not obscure what was actually compared.

### Completion criteria

- Period and cost basis remain consistent.

- Observed values, projections and estimates are separated.

- The artifact matches its reviewed task and source evidence.

### Workflow and dependencies

#### 1. Read report evidence

Retrieve the declared period and comparison dimensions.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 2. Apply approved reporting context

Use maintained mappings and template.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-FILES](mechanisms.html#MX-F-FILES)

**Dependency:** optional — Organization-specific reference material is selected.

**Configuration features:** [FT-F-FILES](features.html#FT-F-FILES)

**Effect:** Context read

**Verification:** Verify a known mapping and expose unmapped records.

**Failure handling:** Keep unassigned values visible and update the authoritative file deliberately.

#### 3. Run the report task

Retain a separate execution identity.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-TASK](mechanisms.html#MX-F-TASK)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-TASKS](features.html#FT-F-TASKS)

**Effect:** Execution and output

**Verification:** Match completed results to task identity and requested scope.

**Failure handling:** Distinguish absent, queued and failed tasks before retrying.

#### 4. Generate the reviewed artifact

Provide the requested supported output format.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-ARTIFACT](mechanisms.html#MX-F-ARTIFACT)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-ARTIFACTS](features.html#FT-F-ARTIFACTS)

**Effect:** Report artifact

**Verification:** Compare displayed figures and period with the reviewed source analysis.

**Failure handling:** Do not distribute an artifact that no longer matches its query basis.

#### 5. Repeat on a schedule

Create future reports under the same basis.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-SCHEDULE](mechanisms.html#MX-F-SCHEDULE)

**Dependency:** conditional — Recurring execution is enabled.

**Configuration features:** [FT-F-AUTOMATIONS](features.html#FT-F-AUTOMATIONS), [FT-F-TASKS](features.html#FT-F-TASKS)

**Effect:** Future tasks

**Verification:** Inspect trigger and the actual task's reporting window separately.

**Failure handling:** Disable future starts and control already-created work separately.

#### 6. Publish to the configured Jira destination

Create the supported report follow-up in the approved project.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-JIRA](mechanisms.html#MX-F-JIRA)

**Dependency:** optional — Jira distribution is selected and invocation-specific authorization is satisfied.

**Configuration features:** [FT-F-JIRA](features.html#FT-F-JIRA)

**Effect:** External publication

**Verification:** Inspect invocation type, action details, destination and resulting issue or comment.

**Failure handling:** Stop incorrect destinations. Do not expect an interactive prompt to protect an unattended automation.

#### 7. Publish to the configured Slack channel

Deliver the permitted report summary to its reviewed audience.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-SLACK](mechanisms.html#MX-F-SLACK)

**Dependency:** optional — Slack distribution is selected; audience review occurs before direct publication.

**Configuration features:** [FT-F-SLACK](features.html#FT-F-SLACK)

**Effect:** External publication

**Verification:** Review audience before invocation and inspect delivery afterward.

**Failure handling:** Keep analysis completion separate from delivery failure; posting does not establish channel-reading capability.

### Variant: On-demand period report

Create one report for a specified complete period.

No recurring automation is required.

### Variant: Recurring report

Select a supported schedule.

The schedule does not define the analytical time window.

### Variant: External distribution

Select an eligible configured destination.

Destination and invocation-specific authorization must be reviewed separately.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS), [PR-F-AUTOMATION](profiles.html#PR-F-AUTOMATION), [PR-F-PUBLICATION](profiles.html#PR-F-PUBLICATION)

**Detailed guide:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04), [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08), [F-M02](../guides/finops.html#F-M02), [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)

## UC-F05 — Investigate a cost anomaly

**Actor:** FinOps investigator

**Objective:** Quantify a cost anomaly and assess available evidence for an operational cause.

A cost monitor identifies an unexpected increase. Inspect the anomaly record and query the affected cost dimensions for the relevant period. Where permissions allow, use operational-change records to investigate whether a workload or configuration change explains the increased usage or rate.

Keep numerical attribution and causal evidence separate. A nearby CloudTrail event provides a lead but does not necessarily explain the whole deviation. The final explanation should identify affected costs, supporting observations, and missing inputs. If change evidence is unavailable, preserve the reconciled cost contribution without inventing an operational cause.

### Completion criteria

- Affected dimensions and monetary contributions reconcile.

- Change correlation is distinguished from causal evidence.

- Analysis completion and optional publication status remain separate.

### Workflow and dependencies

#### 1. Match a supported anomaly event

Create work for the approved monitor and condition.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-EVENT](mechanisms.html#MX-F-EVENT)

**Dependency:** conditional — The event-triggered profile is selected.

**Configuration features:** [FT-F-AUTOMATIONS](features.html#FT-F-AUTOMATIONS), [FT-F-TASKS](features.html#FT-F-TASKS)

**Effect:** Task creation; publication is a separate configured step

**Verification:** Trace event, automation, task, analysis and destination result independently.

**Failure handling:** Inspect monitor conditions and rule permissions before changing the analytical prompt.

#### 2. Create or inspect investigation work

Retain the execution independently of its trigger.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-TASK](mechanisms.html#MX-F-TASK)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-TASKS](features.html#FT-F-TASKS)

**Effect:** Execution and output

**Verification:** Match completed results to task identity and requested scope.

**Failure handling:** Distinguish absent, queued and failed tasks before retrying.

#### 3. Analyze cost and change evidence

Quantify contributions and assess the supported explanation.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 4. Publish to the reviewed channel

Deliver the permitted summary to the appropriate audience.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-SLACK](mechanisms.html#MX-F-SLACK)

**Dependency:** optional — A reviewed Slack destination is selected.

**Configuration features:** [FT-F-SLACK](features.html#FT-F-SLACK)

**Effect:** External publication

**Verification:** Review audience before invocation and inspect delivery afterward.

**Failure handling:** Keep analysis completion separate from delivery failure; posting does not establish channel-reading capability.

### Variant: On-demand investigation

Start from a chosen anomaly and explicit task.

No event automation is required.

### Variant: Event-triggered investigation

Use the supported anomaly event and managed rule.

Invocation, queue, analysis and publication are inspected separately.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS), [PR-F-AUTOMATION](profiles.html#PR-F-AUTOMATION), [PR-F-PUBLICATION](profiles.html#PR-F-PUBLICATION)

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08), [F-M05](../guides/finops.html#F-M05), [F-03](../guides/finops.html#F-03), [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)

## UC-F06 — Prioritize optimization recommendations

**Actor:** Service and cost owner

**Objective:** Select actionable upstream recommendations under workload constraints.

An optimization source proposes several changes for a service. Retrieve the original recommendations and inspect their assumptions, resource scope, and overlapping savings estimates. Add workload constraints such as latency, resilience, deployment risk, and ownership before prioritizing the candidates.

Record why each candidate is accepted, deferred, or rejected and identify the normal engineering process for an accepted change. The underlying recommendations originate in the documented optimization services. The agent’s explanation does not independently measure future savings or authorize an infrastructure change.

### Completion criteria

- Original source assumptions are retained.

- Overlapping savings estimates are not indiscriminately summed.

- Accepted, deferred and rejected work has explicit reasons.

### Workflow and dependencies

#### 1. Retrieve upstream recommendations

Read the original candidates, assumptions and resource scope.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 2. Apply workload-owner context

Use reviewed ownership and operating constraints.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-FILES](mechanisms.html#MX-F-FILES)

**Dependency:** optional — The recommendation depends on uploaded mappings.

**Configuration features:** [FT-F-FILES](features.html#FT-F-FILES)

**Effect:** Context read

**Verification:** Verify a known mapping and expose unmapped records.

**Failure handling:** Keep unassigned values visible and update the authoritative file deliberately.

#### 3. Review candidate changes

Compare reliability, performance and implementation risk with estimated benefit.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 4. Create an owned follow-up

Publish accepted work with evidence and acceptance criteria.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-JIRA](mechanisms.html#MX-F-JIRA)

**Dependency:** optional — The destination and invocation-specific authorization are satisfied.

**Configuration features:** [FT-F-JIRA](features.html#FT-F-JIRA)

**Effect:** External publication

**Verification:** Inspect invocation type, action details, destination and resulting issue or comment.

**Failure handling:** Stop incorrect destinations. Do not expect an interactive prompt to protect an unattended automation.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS), [PR-F-PUBLICATION](profiles.html#PR-F-PUBLICATION)

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08), [F-M02](../guides/finops.html#F-M02), [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)

## UC-F07 — Measure the outcome of an implemented optimization

**Actor:** Change owner

**Objective:** Measure post-change cost and service behavior within defensible attribution limits.

An approved optimization has been implemented, and the owner wants to know what changed. Select comparable before-and-after periods and record traffic, pricing, allocation, and service-health differences that could affect the result. Reconcile the costs using the same metric and scope.

Report the observed change together with its attribution limits. A lower bill is not sufficient evidence that the optimization caused the decrease when demand also fell. This is a team measurement workflow using source-backed analysis, not a service guarantee of savings. Unexplained differences remain part of the outcome rather than being removed from the report.

### Completion criteria

- Before and after periods are comparable.

- Demand, prices and allocation changes are disclosed.

- Observed change is not replaced with a prior savings estimate.

### Workflow and dependencies

#### 1. Establish the implemented change and baseline

Confirm deployment and select comparable observation periods.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 2. Read comparable cost evidence

Reconcile values under the same analytical basis.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-QUERY](mechanisms.html#MX-F-QUERY)

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** [FT-F-SOURCES](features.html#FT-F-SOURCES)

**Effect:** Source read

**Verification:** Reconcile a material result using the same dates, metric, scope and dimensions.

**Failure handling:** Withhold unsupported numerical or causal conclusions and identify missing sources.

#### 3. Assess the measured outcome

Account for other changes before attributing the difference.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Implementation profiles

[PR-F-ANALYSIS](profiles.html#PR-F-ANALYSIS)

**Detailed guide:** [F-U01](../guides/finops.html#F-U01), [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

## UC-G01 — Prepare an operational review

**Actor:** Operational review chair

**Objective:** Prepare evidence-backed decisions, owners and follow-up for an operational review.

An operational review starts with reviewed evidence and unresolved decisions, not with a request for another differently titled report. Select the reliability or cost-management profile, identify its period, and assemble relevant findings with the previous action list. Each input retains its source and execution identity so participants can question its interpretation.

Organize the meeting around decisions required, their supporting observations, accountable owners and the next verification date. Owners confirm progress and acceptance; silence is not completion. The profiles reuse this narrative while retaining their own data access and execution configuration. A combined meeting is a team-managed composition, not an AWS cross-agent orchestration feature.

### Completion criteria

- Reviewed inputs and prior actions retain source identity.

- Required decisions and accountable owners are explicit.

- Earlier actions are closed only with acceptance evidence.

### Workflow and dependencies

#### 1. Select review evidence

Choose reliability or cost-management results and the prior action list.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

#### 2. Prepare reliability evidence

Assemble selected service reports and incident themes.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-D-CUSTOM](mechanisms.html#MX-D-CUSTOM)

**Dependency:** conditional — The reliability review profile is selected.

**Configuration features:** [FT-D-CUSTOM](features.html#FT-D-CUSTOM), [FT-D-HISTORY](features.html#FT-D-HISTORY)

**Effect:** Execution and output

**Verification:** Inspect tool arguments, failures and output against the task scope.

**Failure handling:** Mark incomplete output and resolve the failed prerequisite before repeating the run.

#### 3. Prepare cost-management evidence

Assemble reconciled costs, anomalies and recommendation dispositions.

**Responsible actor:** Service execution; accountable engineer reviews the result

**Mechanism:** [MX-F-TASK](mechanisms.html#MX-F-TASK)

**Dependency:** conditional — The cost-management review profile is selected.

**Configuration features:** [FT-F-TASKS](features.html#FT-F-TASKS)

**Effect:** Execution and output

**Verification:** Match completed results to task identity and requested scope.

**Failure handling:** Distinguish absent, queued and failed tasks before retrying.

#### 4. Record decisions and follow-up

Have owners confirm status, priority and acceptance rather than infer completion from silence.

**Responsible actor:** Responsible engineer or reviewer

**Mechanism:** Team procedure; no native agent function asserted.

**Dependency:** required — Applies to the selected implementation.

**Configuration features:** 

**Effect:** Team decision; no implicit service action

**Verification:** Record the decision with the source identifiers and evidence needed for the case completion criteria.

**Failure handling:** Keep the result unresolved and assign the missing decision or evidence to an owner.

### Variant: Reliability review

Use health, deployments, incident patterns and prevention results.

Service measurements and engineering ownership remain authoritative.

### Variant: Cost-management review

Use reconciled costs, anomalies, recommendations and measured outcomes.

Potential savings remain estimates until independently measured.

### Variant: Combined team review

Use evidence from independently configured services.

No shared runtime, credentials or approval authority are implied.

### Implementation profiles

[PR-REVIEW](profiles.html#PR-REVIEW)

**Detailed guide:** [A-05](../guides/architecture.html#A-05), [A-06](../guides/architecture.html#A-06), [A-U01](../guides/architecture.html#A-U01)
