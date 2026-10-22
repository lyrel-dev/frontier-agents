# Operational use-case catalog



Operational use cases for AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent. Read each workflow as a situation, an evidence-gathering process, and an outcome to interpret. The linked guides explain the underlying capabilities and mechanisms.



## AWS DevOps Agent



### Incident operations

Incident work proceeds from routing to investigation, then to mitigation review and any separately authorized action. These use cases describe those decisions independently so that a correctly routed signal is not mistaken for a confirmed diagnosis or an approved change.



#### D-UC01 — Incident signal triage

**Delivery:** Built-in function. **Availability:** GA production operations.

An on-call engineer receives several alerts for the same service. Before opening another investigation, the engineer needs to know whether the new signal belongs to work already in progress. Inspect the triage decision and its reason, then follow the primary investigation when the signal was linked. A skipped signal should identify the matching exclusion rather than disappear from the operating record.

When correlation is wrong, unlink the signal so it can be investigated separately. When a skip criterion excluded a relevant event, review that criterion and use the supported unskip operation. The result of this use case is correct routing and an identifiable investigation, not a root-cause conclusion. Root-cause analysis follows in the next use case.

**Inputs:** Incident identity, correlation evidence, skip criteria and active investigations.

**Output:** Triage decision, reason and resulting investigation linkage.

**Limits:** A triage decision is not a diagnosis. Incorrect linking or skipping requires a routing correction.

**Example request:** Explain why this alert was linked, skipped or scheduled for a new investigation.

**Detailed guide:** [D-06](../guides/devops.html#D-06)

**Official references:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)



#### D-UC02 — Root-cause investigation

**Delivery:** Built-in function. **Availability:** GA production operations.

A service owner sees elevated errors after a deployment. The investigation begins with the affected service, incident time, and symptoms, not with an assumed deployment defect. Connect the available logs, metrics, traces, repository context, and deployment records, then inspect how the investigation relates the observations across those sources.

The useful result identifies the measurements that support each explanation and the sources that could not be read. A deployment timestamp may provide a lead, but its proximity to the error increase is not sufficient proof of cause. When evidence conflicts, preserve the competing explanations and supply the missing observation through investigation steering rather than turning a plausible summary into a confirmed diagnosis.

**Inputs:** Incident signal, service scope, UTC window, connected telemetry and deployment context.

**Output:** Investigation record with observations, hypotheses, root-cause versions and evidence.

**Limits:** The output remains an investigation result to verify against current source data.

**Example request:** Investigate the checkout 5xx increase for the stated service and UTC window; separate observations, hypotheses and missing data.

**Detailed guide:** [D-01](../guides/devops.html#D-01), [D-06](../guides/devops.html#D-06)

**Official references:** [DS01](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html), [DS02](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS18](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)



#### D-UC03 — Investigation steering and hypothesis review

**Delivery:** Built-in function. **Availability:** GA production operations.

During an investigation, the engineer establishes that the database is healthy even though the current hypothesis blames connection exhaustion. Supply the contrary measurements and their time window to the active investigation. Ask the agent to reconsider the hypothesis and examine the upstream dependency rather than starting an unrelated conversation with no investigation context.

Review the revised analysis for an actual change in reasoning and supporting evidence. If the new evidence cannot be accessed, retain that limitation. Steering affects the current investigation; completed-investigation feedback is the separate path for recording a verified correction for later work. Neither operation authorizes a production change.

**Inputs:** Active investigation, operator question, new evidence or rejected hypothesis.

**Output:** Updated investigation or root-cause version that records the steering input.

**Limits:** Steering changes analysis; it does not authorize a production action.

**Example request:** The database pool is healthy. Re-evaluate the upstream dependency hypothesis and cite the current evidence.

**Detailed guide:** [D-06](../guides/devops.html#D-06)

**Official references:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)



#### D-UC04 — Mitigation plan preparation

**Delivery:** Built-in function. **Availability:** GA production operations.

Once the current evidence supports a likely failure mechanism, the incident owner needs a mitigation that can be reviewed. Ask for the proposed target, exact change, expected effect, risks, rollback, and recovery checks. Compare that proposal with the approved runbook and the evidence already collected, especially where the proposed action would affect another service.

The output is a decision document: it should make it possible to approve, reject, or revise the proposal without guessing its effect. A generated plan remains separate from execution. It can be carried out through the ordinary engineering process, or through an eligible directed-action path after the additional controls described in the next use case have been satisfied.

**Inputs:** Reviewed incident evidence and a specific operational objective.

**Output:** Mitigation proposal suitable for operator approval or normal runbook execution.

**Limits:** A proposal is not permission to execute. Unsupported or high-risk actions remain outside the action path.

**Example request:** Propose the lowest-risk mitigation, including blast radius, rollback and recovery checks.

**Detailed guide:** [D-06](../guides/devops.html#D-06), [D-M06](../guides/devops.html#D-M06)

**Official references:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html), [DS16](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)



#### D-UC05 — Approved directed mitigation

**Delivery:** Controlled action. **Availability:** GA operations; directed actions require opt-in.

An incident owner has accepted a narrowly scoped mitigation and wants to use the documented action path. Confirm Agent Space enablement, the target-account role or connected-tool configuration, and the classification of the operation. Review the actual parameters presented for approval; a broadly named role is not the approval record.

After the operator approves the eligible action, inspect the resulting resource state and the available attribution evidence. Recovery must still be checked against service measurements. If execution is denied, locate the failed gate instead of widening all permissions. This workflow does not convert the earlier mitigation recommendation into standing authorization for subsequent changes.

**Inputs:** Directed-action enablement, eligible role or integration, correct tool classification and exact operation/resource approval.

**Output:** Attributed action record and independently checked resulting state.

**Limits:** Approval is scoped to a particular operation and resource. Tool misclassification can change expected approval behavior.

**Example request:** After showing the exact target and parameters, request approval for the narrowly scoped change.

**Detailed guide:** [D-M06](../guides/devops.html#D-M06)

**Official references:** [DS16](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)



### Health reporting and reviews

A health query answers an immediate operational question. A bulletin records change during an incident, a recurring report preserves a comparable period, and an operational review turns those records into decisions. Their inputs overlap, but their purposes and acceptance evidence differ.



#### D-UC06 — On-demand service health query

**Delivery:** Built-in function. **Availability:** GA production operations.

Before an on-call handover, the engineer needs a current view of one service. Define the service identity and a bounded period, such as the previous complete hour, and ask for error rate, latency, saturation, active alarms, and recent changes from the connected sources. A health answer is more useful when it identifies its observation time and any unavailable signal.

Compare one material figure with the underlying monitoring query, using the same aggregation and dimensions. An absent log source should appear as a data gap rather than as an absence of errors. The answer supports a handover or investigation decision; it does not replace the monitoring system or create a complete continuous health assessment.

**Inputs:** Service identity, reporting window and connected metrics/logs/alarms/deployment sources.

**Output:** Timestamped health answer with source scope and missing signals.

**Limits:** A conversational health answer does not replace monitoring or prove complete signal coverage.

**Example request:** Summarize checkout health for the previous 60 minutes and state every unavailable signal.

**Detailed guide:** [D-01](../guides/devops.html#D-01), [D-05](../guides/devops.html#D-05), [D-12](../guides/devops.html#D-12)

**Official references:** [DS01](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html), [DS02](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS18](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC07 — Incident status bulletin

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

During an active incident, the incident commander needs a brief update that explains what has changed since the preceding observation. Configure a specialist task with the incident identifier, selected telemetry tools, and a short explicit lookback window. Ask for changed measurements, the status of open hypotheses, missing reads, and the next check rather than a repetition of the whole incident history.

A report can analyze minute-resolution measurements without arriving every minute. The documented custom-agent schedule uses a flexible window of up to 30 minutes; execution time is additional. For time-critical updates, invoke the task on demand or use a separately tested triggering design. Record both the measurement window and report-generation time so a delayed bulletin is not mistaken for current telemetry.

**Inputs:** Custom agent, selected telemetry and incident tools, explicit five- or ten-minute window and output contract.

**Output:** Delta-focused status update: changed observations, open hypotheses, owner and next check.

**Limits:** Telemetry resolution, lookback period, schedule window, and execution time are different. The documented custom-agent schedule has a flexible window of up to 30 minutes.

**Example request:** Report what changed in the active incident during the previous five complete minutes, including the observation window, generation time, and missing sources.

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12)

**Official references:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC08 — Daily or weekly service health report

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

A platform team wants the same service-health report each week. Define the covered services, complete reporting period, metric aggregation, comparison period, and sections before creating the custom agent. Select the real telemetry and incident tools and attach only the knowledge required to interpret service names, owners, and reporting conventions.

Inspect a trial invocation before enabling recurring execution. The report should connect significant changes to source observations, identify incomplete data, and distinguish incident counts from ongoing problems. Its purpose is a repeatable health record. Decisions about priorities and ownership belong to the operational review that consumes this report, rather than being inferred from a formatted health table.

**Inputs:** Named services, reporting period, selected tools, reporting standard and recipients.

**Output:** Structured health report or artifact with evidence links and data-quality notes.

**Limits:** The agent can report only from attached memory and selected tools. A schedule does not define report scope by itself.

**Example request:** Generate the weekly payments health report for complete UTC days, including error, latency, incidents, deployments and data gaps.

**Detailed guide:** [D-07](../guides/devops.html#D-07), [D-M07](../guides/devops.html#D-M07), [D-12](../guides/devops.html#D-12)

**Official references:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC09 — Deployment and change activity report

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

A release engineer wants to review the changes delivered during the previous week. The input is deployment history with service and revision identifiers, not simply merged pull requests. Configure the task to distinguish attempted, successful, failed, and rolled-back deployments using the states exposed by the connected delivery tools.

The result should make it possible to trace a reported deployment to its source record and compare it with incidents in the same service and period. Similar timestamps are useful for investigation but do not establish causality. Missing pipeline access or ambiguous status mappings should be listed explicitly so the report is not presented as a complete release history.

**Inputs:** CI/CD integration, service ownership, revision identifiers and complete reporting window.

**Output:** Deployment report with revisions, outcomes, affected services and unresolved follow-up.

**Limits:** Requires connected pipeline tools and explicit interpretation of deployment states.

**Example request:** List production deployments in the last seven complete days, including failed changes and linked incidents.

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12)

**Official references:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC10 — Operational review pack

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

An operational review turns measurements into decisions. Start with the reviewed service-health and deployment reports, incident themes, prevention recommendations, and the previous meeting’s action list. The task is to assemble the evidence relevant to unresolved decisions, not to create another differently titled copy of the weekly health report.

Organize the review around decisions required, their supporting observations, the accountable owner, and the next verification date. Ask owners to confirm status rather than treating silence as completion. This is a team-designed workflow built from configured evidence access and reporting; the meeting, prioritization, and acceptance of actions remain engineering responsibilities.

**Inputs:** Review template, selected data sources, attached reporting context and named audience.

**Output:** Review agenda, evidence summary, decisions required and owned follow-up.

**Limits:** This is a team-defined workflow. The report contract, recipients and stop owner must be configured.

**Example request:** Prepare the weekly operational review pack with health, incidents, improvements, deployments, decisions and owners.

**Detailed guide:** [D-07](../guides/devops.html#D-07), [D-M07](../guides/devops.html#D-M07), [D-12](../guides/devops.html#D-12)

**Official references:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



### Pattern analysis and improvement

An incident explains one occurrence. Pattern analysis compares occurrences, and prevention review turns recurring evidence into proposed improvements. Keep the historical evidence attached to the pattern so that its interpretation can be revised.



#### D-UC11 — Incident pattern identification

**Delivery:** Built-in function. **Availability:** GA production operations.

Several investigations may share an operational weakness even when they were triggered by different alarms. Review the relevant investigation history and ask which causes or contributing conditions recur. Group the evidence by the proposed pattern and retain the supporting investigation identifiers so the grouping can be challenged.

This analysis differs from retrieving the prior cause of one alarm: its purpose is to identify cross-incident themes worth prevention work. Similar symptoms without verified common causes should remain a candidate pattern. The next step is to review the prevention recommendations against those themes rather than assuming that a historical cluster explains the next incident.

**Inputs:** Recent investigation history and managed learning context.

**Output:** Pattern summary, recurring-cause context and candidate prevention themes.

**Limits:** Historical similarity does not establish the cause of a new incident.

**Example request:** Identify recurring checkout incident patterns and cite the investigations that support each pattern.

**Detailed guide:** [D-M01](../guides/devops.html#D-M01), [D-06](../guides/devops.html#D-06)

**Official references:** [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)



#### D-UC12 — Prevention recommendation backlog

**Delivery:** Built-in function. **Availability:** GA production operations.

The reliability owner has identified recurring themes and needs a manageable prevention backlog. Run or inspect the documented prevention evaluation, then review each recommendation against the incidents it addresses. Separate observability improvements, infrastructure changes, governance work, and code changes because they have different owners and acceptance evidence.

Keep an accepted recommendation linked to its source evidence and normal change process. A recommendation’s priority or estimated effect is not proof that the change has been implemented. During the next operational review, inspect actual progress and post-change observations. This closes the team’s improvement loop without claiming autonomous implementation or measured benefit before either exists.

**Inputs:** Multiple incident investigations, team priorities and recommendation evaluation.

**Output:** Ranked recommendations with source incidents, expected effect and backlog state.

**Limits:** Recommendations are not automatically implemented and may age out when not kept or implemented.

**Example request:** Run a prevention evaluation and return the highest-priority recommendations with affected incidents and owners.

**Detailed guide:** [D-06](../guides/devops.html#D-06)

**Official references:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)



### Knowledge and documentation

Operational knowledge moves from source evidence and approved procedures into representations an agent can retrieve or apply. The following workflows distinguish historical context, standing instructions, selected runbook skills, topology observations, and owner-reviewed documentation.



#### D-UC13 — Recurring-alarm investigation with historical context

**Delivery:** Built-in function with retained context. **Availability:** GA managed memory.

The same alarm fires again, and the previous investigation has a known cause. Inspect the relevant retained context and make it available to the current investigation. Then compare the earlier explanation with the new measurements. The historical entry is a lead that can shorten the list of questions; it is not a substitute for the new time window’s evidence.

Record whether a relevant entry existed, whether its retrieval was observable, and whether the new diagnosis was correct. Those are three separate results. If current evidence contradicts the old cause, preserve the contradiction and provide a verified correction when appropriate. The worked recurring-alarm example in the guide illustrates this distinction with synthetic measurements.

**Inputs:** Prior completed investigations, active monitor memory and current incident evidence.

**Output:** Retrieved historical context considered alongside current telemetry.

**Limits:** Memory existence, retrieval and diagnostic correctness are separate observations.

**Example request:** Compare this alarm with relevant prior causes, then list the current evidence that supports or contradicts each one.

**Detailed guide:** [D-M01](../guides/devops.html#D-M01)

**Official references:** [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)



#### D-UC14 — SOP consolidation into reusable skills

**Delivery:** Composed workflow. **Availability:** GA skills.

A team has several overlapping timeout SOPs maintained by different owners. First reconcile their scope, resolve contradictory steps, remove stale tool names, and identify the approved procedure. Only then package that procedure as a skill with a description that states when it applies and which agent types may use it.

Keep the reviewed source in Git and test a request that should match the skill alongside one that should not. The supporting references should explain the expected observations and the point at which the procedure stops or escalates. Consolidation is authored team work; skill selection is the platform mechanism. A skill neither creates the referenced tools nor grants permission to use them.

**Inputs:** Reviewed SOP, target agent types, actual tool names and expected evidence.

**Output:** Version-controlled SKILL.md bundle and a matching/nonmatching selection test.

**Limits:** Consolidation and review are team work. A skill supplies procedure; it does not grant tools or permissions.

**Example request:** Create a skill from the approved checkout timeout SOP and state when it should and should not load.

**Detailed guide:** [D-M04](../guides/devops.html#D-M04)

**Official references:** [DS11](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)



#### D-UC15 — Applying incident reporting conventions

**Delivery:** Configured knowledge. **Availability:** GA instructions.

The operations team requires every incident answer to identify its service, UTC window, evidence sources, and unresolved questions. Put these standing conventions in the appropriate global or agent-specific instructions rather than duplicating them in every task. Save the change and start a new session to inspect the resulting behavior.

An existing session retains its startup instructions, so it is not a valid test of the updated text. Compare old and new sessions deliberately and retain the instruction source in Git. These conventions improve the readability of operational records; access control and authorization remain enforced by the connected systems rather than by the wording of the instructions.

**Inputs:** Reviewed global or agent-specific AGENTS.md content.

**Output:** New sessions that include the standing guidance.

**Limits:** Instructions guide behavior but do not enforce IAM authorization. Existing sessions retain their startup content.

**Example request:** Apply the evidence-output contract to new incident RCA sessions and compare with an existing session.

**Detailed guide:** [D-M03](../guides/devops.html#D-M03)

**Official references:** [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS09](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)



#### D-UC16 — Topology documentation and dependency map

**Delivery:** Built-in function with composed documentation. **Availability:** GA production operations.

A service owner needs an architecture description before changing a dependency. Start from discovered resources and the topology’s service, repository, pipeline, and dependency relationships. Compare those relationships with the deployed configuration and source revision, distinguishing directly observed relationships from inferred ones.

Write the reviewed result as a maintained service description with identifiers, evidence links, and unresolved edges. The topology is useful input to that document, but it is not a guaranteed complete inventory or an automatic update to the team’s architecture repository. This use case produces owner-reviewed documentation; the following refresh use case checks whether the underlying environment model has changed.

**Inputs:** Connected accounts, discovery, Resource Explorer where applicable and relevant integrations.

**Output:** Topology view and environment summary that can support architecture documentation.

**Limits:** Topology is a representation, not an authorization boundary or guaranteed complete inventory.

**Example request:** Document the payments service containers, downstream dependencies, repositories and deployment boundaries; mark inferred relationships.

**Detailed guide:** [D-05](../guides/devops.html#D-05), [D-12](../guides/devops.html#D-12), [D-M08](../guides/devops.html#D-M08)

**Official references:** [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)



#### D-UC17 — Environment summary and topology refresh

**Delivery:** Built-in mechanism. **Availability:** GA production operations.

After a new integration or infrastructure change, the previously learned environment summary may be incomplete. Request or inspect the supported refresh and follow the managed learning run to its resulting knowledge. Compare one known changed resource or relationship with the new output rather than accepting a submitted refresh request as evidence of completion.

Record the observed version and the discrepancies that remain. A missing topology node can reflect discovery limitations and does not by itself establish denied resource access. Refreshing the environment model supports later investigations; it does not replace source-controlled architecture documentation or grant a custom agent access to every retained store.

**Inputs:** Changed resources or integrations and managed learning capability.

**Output:** Updated environment summary, topology and versioned knowledge.

**Limits:** A refresh request is not completion evidence. Managed learning schedules are platform-owned.

**Example request:** Refresh the environment understanding after the new inventory integration and report the resulting version and changed relationships.

**Detailed guide:** [D-05](../guides/devops.html#D-05), [D-12](../guides/devops.html#D-12), [D-M08](../guides/devops.html#D-M08)

**Official references:** [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)



### Custom operational work

Custom agents apply selected tools and explicit instructions to specialist tasks. The team supplies the resource scope, standards, identifiers, and expected output. These workflows are configurable applications, not additional universal audit or correlation engines.



#### D-UC18 — Configuration audit

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

An operations standard requires a small set of staging resources to have particular logging and access settings. Configure a custom task with read-only configuration tools, the explicit resource list, and the reviewed standard. Each reported finding should identify the resource, the applicable rule, and the actual value that was read.

Review a known conforming and a known nonconforming example before scheduling the task. An unavailable read is an unassessed resource, not a pass. The output is a scoped configuration audit for the chosen rules; it is not a built-in universal compliance engine or permission to repair findings automatically.

**Inputs:** Read-only configuration tools, approved standard, selected resource scope and report format.

**Output:** Audit findings with resource identifiers, rule and observed value.

**Limits:** Requires explicit tools and standards. It is not a built-in universal compliance engine.

**Example request:** Audit staging security-group and logging settings against the attached operations standard; do not change resources.

**Detailed guide:** [D-07](../guides/devops.html#D-07), [D-M04](../guides/devops.html#D-M04), [D-12](../guides/devops.html#D-12)

**Official references:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS11](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC19 — Metrics and error trend analysis

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

A service has gradually become slower without a single clear incident. Define complete comparison periods, metric dimensions, aggregation, and the relevant traffic denominator. Ask the configured task to compare latency, errors, and capacity indicators and to identify the periods where the behavior materially changed.

Inspect the underlying series for gaps and changes in traffic composition before attributing the trend to a release. A change in a percentile or absolute error count can reflect a different workload mix. The result is a sourced trend analysis with candidate explanations and missing evidence, providing a starting point for focused investigation rather than a causal verdict.

**Inputs:** Selected metric/log tools, complete time range, aggregation and comparison basis.

**Output:** Trend report with material changes, possible explanations and missing evidence.

**Limits:** The workflow must define aggregation and avoid treating correlation as cause.

**Example request:** Analyze checkout latency and error trends for the last four complete weeks and identify material changes.

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12)

**Official references:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html)



#### D-UC20 — Cross-tool operational correlation

**Delivery:** Configured custom agent. **Availability:** GA custom agents.

An incident spans a monitoring alert, a deployment, and a service ticket that use different names for the same application. Supply the identity mapping and a bounded question to a custom task with the required tools. Ask it to build an evidence table that preserves source identifiers and timestamps instead of merging records merely because their descriptions look similar.

Review unmatched records and contradictory revision information explicitly. A connected tool that returns no data may have the wrong scope or permissions. The useful result identifies which observations refer to the same service and change, and which relationships remain hypotheses. Those distinctions make the subsequent investigation reproducible.

**Inputs:** Selected tools from multiple providers, shared identifiers and explicit question.

**Output:** Evidence table linking signals across systems and unresolved mismatches.

**Limits:** Tool availability and identity mapping must be explicit; similar timestamps do not prove causality.

**Example request:** Correlate the error increase with deployments, alerts and tickets using service and revision identifiers.

**Detailed guide:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07), [D-12](../guides/devops.html#D-12), [D-M08](../guides/devops.html#D-M08)

**Official references:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS33](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html), [DS30](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html), [DS31](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html), [DS32](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html), [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)



### Release and change assurance

Reviewing a proposed change and exercising a deployed application answer different questions. Both require explicit scope, and active testing introduces application effects that source review does not. Availability must be checked for the particular preview path.



#### D-UC21 — Release readiness review

**Delivery:** Preview function. **Availability:** Preview; feature and repository eligibility specific.

Before release, a team wants to examine a retry-policy change for operational risk. Use the eligible readiness-review path with the candidate revision, relevant repositories, topology, and release context. Review the findings against the intended dependency behavior and the service’s existing resilience assumptions.

A readiness review analyzes a proposed change; it does not prove that the deployed application behaves correctly. Retain unresolved dependencies and scope limitations and route accepted findings through engineering review. This feature is a separate preview path, so production-operations availability must not be used as evidence that the same review is available for every Region or repository.

**Inputs:** Candidate revision, repositories, topology and release context.

**Output:** Readiness findings, risk explanations and recommended actions.

**Limits:** Do not apply production-operations GA status to this preview path.

**Example request:** Review the retry-policy change for dependency, IAM, resilience and operational risks.

**Detailed guide:** [D-09](../guides/devops.html#D-09)

**Official references:** [DS20](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html), [DS21](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)



#### D-UC22 — Active release testing

**Delivery:** Preview function. **Availability:** Preview.

A staging application is ready for an active release check. Prepare disposable test data, approved identities, explicit allowed operations, and disabled external side effects. The task exercises the deployed target, so the target revision and reachable endpoints matter more than the name of the branch that produced it.

Review the observed requests and results with the application owner. Active testing can create, modify, or delete application data; infrastructure read permissions do not make those requests harmless. The result describes the executed test and its uncovered areas, not blanket release approval. Unexpected effects require stopping and reviewing the configuration before further execution.

**Inputs:** Disposable staging target, test identities, disabled external effects and explicit allowed operations.

**Output:** Test results, reproduction detail and residual risk.

**Limits:** Requests can create, modify or delete application data. Infrastructure write controls do not make application testing read-only.

**Example request:** Test the staging checkout API with synthetic data; avoid production endpoints and external notifications.

**Detailed guide:** [D-09](../guides/devops.html#D-09)

**Official references:** [DS20](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html), [DS21](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)



## AWS Security Agent



### Application assessment

Application testing begins with an authorized target and a reproducible configuration. Public access, authenticated workflows, private reachability, and recurring execution introduce different prerequisites. Each run retains its own scope and evidence.



#### S-UC01 — On-demand application penetration test

**Delivery:** Native assessment. **Availability:** GA on-demand penetration testing.

An application owner has authorized a staging assessment for a specific release. Create the test configuration with the verified target, permitted network surface, source context, test identities, and work limit. Save the configuration separately from starting a run so another reviewer can inspect the intended scope before execution.

Follow the resulting run and retain its target revision, exclusions, and observed coverage. Findings need review against their evidence, while failed authentication or unreachable paths remain assessment gaps. The test sends real requests and can change application state; technical domain verification does not replace the application owner’s authorization.

**Inputs:** Agent Space, verified target, written authority, test data and stop owner.

**Output:** Assessment run with findings, evidence and coverage record.

**Limits:** Testing sends real requests and can change application state. Domain verification is not sufficient authorization.

**Example request:** Run the authorized staging penetration test with the stated target, exclusions and test identities.

**Detailed guide:** [S-01](../guides/security.html#S-01), [S-03](../guides/security.html#S-03), [S-04](../guides/security.html#S-04)

**Official references:** [SS01](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html), [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS10](https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html), [SS11](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)



#### S-UC02 — Authenticated workflow assessment

**Delivery:** Configured assessment. **Availability:** GA penetration testing.

The application’s most important functions are behind authentication, and an unauthenticated scan would not reach them. Configure representative test roles and login instructions, then use authentication preflight to determine whether the credentials are obtained and successfully applied. Inspect the actual application identity rather than only a successful secret read.

Assess the protected workflow under the intended role and retain the routes reached. A successful login as an administrator cannot substitute for coverage of an ordinary customer’s authorization boundary. If MFA, navigation, or application permissions fail, record the missing coverage before interpreting an absence of findings.

**Inputs:** Credential strategy, login instructions, protected routes and representative roles.

**Output:** Findings and coverage tied to the actual authenticated identity.

**Limits:** Credential retrieval and application authentication are separate steps.

**Example request:** Assess the invoice workflow as the test customer role and record the identity and routes reached.

**Detailed guide:** [S-M01](../guides/security.html#S-M01), [S-03](../guides/security.html#S-03)

**Official references:** [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html)



#### S-UC03 — Private application assessment

**Delivery:** Configured assessment. **Availability:** GA penetration testing.

A staging service is reachable only from a private network. Configure the documented private path, DNS, subnets, and security groups together with the target and exclusion rules. Source-control reachability and application-target reachability are separate paths, so test the one the assessment actually requires.

Once the target is reachable, authenticate with the approved test identity and inspect the resulting run. Do not widen the authorized surface simply because a supporting dependency is private. An unreachable production callback should remain excluded, while an approved login dependency may require supporting access without becoming an attack target.

**Inputs:** Target rules, VPC route, DNS, security groups and application credentials.

**Output:** Reachability record and assessment findings for the private target.

**Limits:** Private reachability does not broaden the authorized target list or credential scope.

**Example request:** Assess the private staging endpoint and confirm that the production callback remains out of scope.

**Detailed guide:** [S-03](../guides/security.html#S-03), [S-M01](../guides/security.html#S-M01)

**Official references:** [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)



#### S-UC04 — Recurring penetration test

**Delivery:** Configured assessment. **Availability:** Feature-specific; verify current availability.

The security team wants separate assessments of a stable staging application at regular intervals. Reuse a saved configuration and configure the supported schedule, but identify the target revision and credential state for each run. A reusable definition does not freeze an application that continues to be deployed.

Compare the successive run records and investigate incomplete authentication or coverage before interpreting a reduction in findings. Review the continuing authorization and work limits as the application changes. The schedule creates assessment opportunities; it does not guarantee that every scheduled run successfully exercises the same application surface.

**Inputs:** Stable saved configuration, current test credentials, authorized target and schedule.

**Output:** Separate scheduled run records and findings.

**Limits:** Each run reflects the then-current target and credentials; a schedule does not guarantee successful authentication.

**Example request:** Schedule the staging penetration test weekly and retain each run as a separate evidence record.

**Detailed guide:** [S-04](../guides/security.html#S-04)

**Official references:** [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS10](https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html), [SS11](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)



### Authentication and access

Authentication enables a test to reach protected behavior. Reusing a successful login procedure can support repeated runs, but actual role and route coverage still need verification when the application changes.



#### S-UC05 — Repeated assessment with retained login procedure

**Delivery:** Native mechanism. **Availability:** GA penetration testing.

Repeated assessment runs spend time navigating the same login flow. After a successful authentication, inspect the Login Optimization setting and the documented reuse behavior. Keep the configuration enabled where appropriate, while still verifying the actual application role and protected routes on each run.

When the staging login flow changes, test the new flow rather than assuming the retained procedure remains sufficient. Disabling reuse preserves the learned procedure according to the guidance, so a toggle is not a deletion operation. This use case concerns repeated authenticated access, not a general vulnerability-memory or model-training capability.

**Inputs:** At least one successful login, saved penetration-test configuration and Login Optimization enabled.

**Output:** Reused login skill and observed authenticated identity.

**Limits:** The learned procedure concerns login navigation, not general vulnerability learning.

**Example request:** Compare first-run and later login behavior, then verify the actual application role.

**Detailed guide:** [S-M02](../guides/security.html#S-M02)

**Official references:** [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)



### Findings and remediation

A finding is evidence to review, not an automatically completed engineering task. The following workflows retain the relationship between the accepted finding, the proposed repair, the deployed revision, and the verification result.



#### S-UC06 — Finding review and prioritization

**Delivery:** Native operation. **Availability:** Feature-specific.

A completed assessment contains findings of different severity and evidential strength. Review each material finding in the context of the affected revision, reachable role, exposed data, and reproduction evidence. Add application-owner context before deciding which finding needs immediate repair and which requires more investigation.

The outcome is a disposition and an accountable next action, not merely a sorted severity list. Findings with incomplete evidence should retain that uncertainty. Link accepted work to the original finding identifier so remediation, deployment, and later verification remain traceable even if the issue title or owner changes.

**Inputs:** Completed assessment findings and application-owner context.

**Output:** Prioritized finding with owner, disposition and remediation plan.

**Limits:** Finding count or severity alone is not an adequate risk decision.

**Example request:** Prioritize the findings using impact, confidence, affected role and reproduction evidence.

**Detailed guide:** [S-05](../guides/security.html#S-05)

**Official references:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)



#### S-UC07 — Jira remediation tracking

**Delivery:** Configured integration. **Availability:** Feature-specific.

An accepted finding needs an owned remediation ticket. Connect the permitted Jira Cloud project and review whether issue creation and comments are enabled for that project. Before publication, check that the project audience is appropriate for the finding’s sensitive technical details.

Create the issue with a reference to the finding, affected revision, proposed work, and acceptance evidence. Later updates should preserve that finding relationship. Jira is the external work-tracking record; disconnecting the integration does not delete existing issues. The team’s prioritization and closure decisions remain separate from the publication action.

**Inputs:** Finding, connected Jira project and approved disclosure scope.

**Output:** Jira issue linked to the finding, with later revalidation comments when supported.

**Limits:** Sensitive assessment details should not be published to an inappropriate project or audience.

**Example request:** Create a Jira issue for this accepted finding with the evidence, affected revision and acceptance test.

**Detailed guide:** [S-05](../guides/security.html#S-05), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



#### S-UC08 — Proposed code remediation

**Delivery:** Configured remediation. **Availability:** Feature-specific; provider support applies.

A developer has accepted a finding and wants a repair proposal against the affected source. Confirm the repository and supported remediation settings, then inspect the proposed patch or pull request. The review should include the security change, regression tests, and any unrelated behavior introduced by the proposal.

Run the normal build and review process before deployment. A generated proposal that fails tests is unfinished work, and a merged revision that has not reached the target is not ready for revalidation. Preserve the finding identifier through the change and deployment records so the next test can evaluate the intended repair.

**Inputs:** Accepted finding, repository access and remediation configuration.

**Output:** Patch or pull request linked to the finding.

**Limits:** A proposed patch is not a reviewed, deployed or verified repair.

**Example request:** Prepare a remediation change for the authorization finding and include tests; do not merge automatically.

**Detailed guide:** [S-05](../guides/security.html#S-05), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



#### S-UC09 — Finding revalidation

**Delivery:** Native operation. **Availability:** GA penetration testing.

The reviewed repair has been deployed to the original authorized environment. Select the existing finding for revalidation and inspect the new job, including the current authentication configuration and target revision. The job repeats the selected validation steps rather than conducting a broad new assessment.

Interpret the result within that scope. A reproduced finding remains active evidence of the issue; non-reproduction supports resolution only when the relevant identity and path were actually reached. Keep the original finding and the linked job history. A failed login or changed test environment must not be mistaken for a successful repair.

**Inputs:** Completed original finding, deployed repair and current authentication configuration.

**Output:** Separate revalidation job linked to the original finding with Active or Resolved result.

**Limits:** Revalidation does not rediscover unrelated vulnerabilities or establish whole-application security.

**Example request:** Revalidate the selected finding against the deployed revision and record the actual test identity.

**Detailed guide:** [S-M05](../guides/security.html#S-M05)

**Official references:** [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)



### Shift-left review

Source, design, and threat-model assessments examine different representations of the same application. Requirements supply explicit criteria, while scope and source revisions define what is actually evaluated. Generated criteria require review before they govern later work.



#### S-UC10 — Repository code review

**Delivery:** Preview assessment. **Availability:** Preview.

A team wants a baseline review of a repository or supported source package. Connect the intended source revision and select the eligible review modes. Vulnerability analysis and evaluation against enabled requirement packs answer related but different questions, so the requested criteria should be explicit.

Review findings in their code context and inspect preflight failures separately from completed analysis. The result applies to the selected source and modes; it is not a substitute for testing the deployed application. This preview workflow has provider and availability boundaries that must be checked before it becomes part of the delivery process.

**Inputs:** Connected repository or S3 source, review mode and applicable requirement packs.

**Output:** Code findings with evidence, location and possible remediation.

**Limits:** Provider, source and availability limits apply. Completed review is not complete application coverage.

**Example request:** Review the repository for vulnerability findings and the enabled authorization requirements.

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-M03](../guides/security.html#S-M03), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



#### S-UC11 — Change-focused code review

**Delivery:** Preview assessment. **Availability:** Preview.

A pull request changes an authorization handler. Use the supported change-focused review path and identify the exact revision being assessed. Provide the repository context and enabled criteria needed to evaluate the change rather than treating an isolated diff as a complete description of the system.

When further commits arrive, confirm whether another review is required for that provider and trigger path. Retain revision-specific findings and distinguish a stale result from a finding that still applies. Optional comments or remediation depend on the configured write features; read access alone does not authorize those repository effects.

**Inputs:** Supported change event or differential source, repository context and criteria.

**Output:** Revision-specific findings and optional remediation path.

**Limits:** Subsequent changes may require a new review; support differs by provider and trigger path.

**Example request:** Review this change for security findings and enabled requirements; identify the exact revision.

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



#### S-UC12 — Security requirement evaluation

**Delivery:** Configured criteria. **Availability:** Preview workflows.

The organization has an explicit requirement for access to account-owned invoices. Configure its applicability and compliance criteria in an enabled pack, then run an eligible design or code review with requirement evaluation selected. Inspect why the requirement applied before interpreting its compliance result.

Use a known compliant handler, a violating handler, and an inapplicable public resource as review examples. These expose different mistakes in the criteria. A framework label or a generated pack does not certify compliance; the result is an assessment against the selected requirements and supplied evidence.

**Inputs:** Enabled requirement pack and eligible assessment configured for requirement evaluation.

**Output:** Requirement-level compliant, violating or inapplicable result.

**Limits:** A framework or generated pack is not a compliance certification.

**Example request:** Evaluate the ownership-check requirement and show why it is applicable, compliant or violated.

**Detailed guide:** [S-M03](../guides/security.html#S-M03)

**Official references:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)



#### S-UC13 — Security requirement consolidation

**Delivery:** Composed workflow. **Availability:** Preview workflows.

Policy owners have revised several overlapping security standards. Reconcile the governing documents and identify the approved source before generating a replacement requirement pack. Compare the generated applicability and compliance statements with that source, including requirements that had previously been added manually.

Regeneration replaces the existing pack contents rather than appending to them. Review the proposed replacement before enabling it for subsequent assessments, and keep the policy and reviewed requirement source in Git. This is a controlled authoring workflow; it must not silently replace a working pack merely because new documents were uploaded.

**Inputs:** Governed policy sources, existing pack and reviewer.

**Output:** Reviewed replacement requirement pack and external change record.

**Limits:** Regeneration replaces existing requirements, including manual entries. Keep the authoritative source outside the generated pack.

**Example request:** Regenerate the pack from the approved policy documents and identify which existing requirements would be replaced.

**Detailed guide:** [S-M04](../guides/security.html#S-M04)

**Official references:** [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS15](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)



#### S-UC14 — Design review

**Delivery:** Preview assessment. **Availability:** Preview.

A team proposes a new payment-service design before implementation. Submit the current design material and relevant application context for the eligible review, and identify the enabled requirements that govern it. The assessment should expose assumptions about identity, data flows, and trust boundaries that need owner confirmation.

Review the findings with the architect and distinguish missing design evidence from a demonstrated violation. Design review has a one-off lifecycle, with cloning used for a new review; it should not be described as an automatically refreshed continuous model. The result informs design work rather than approving the future implementation.

**Inputs:** Current design material, application context and enabled requirement packs.

**Output:** Design findings and reviewed assumptions.

**Limits:** Design review uses a different one-off lifecycle from reusable run configurations.

**Example request:** Review the new payment design against the enabled security requirements and list unsupported assumptions.

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



#### S-UC15 — Threat modeling

**Delivery:** Preview assessment. **Availability:** Preview.

A service boundary has changed and the team needs an updated threat model. Supply explicit scope documents and the relevant architecture and source evidence. Review the inferred system overview, components, data flows, and trust boundaries before evaluating individual threats.

Correct an incorrect boundary at the model input rather than dismissing every threat that follows from it. Retain evidence for the accepted threats and identify inferred relationships that remain unverified. The result is a reviewed model for that scope and run, not proof that every possible threat has been discovered.

**Inputs:** Architecture documents, code/context sources and explicit system boundary.

**Output:** Assets, trust boundaries, flows, threats and model findings.

**Limits:** Inferred system context requires review; the model is not a complete guarantee of threat coverage.

**Example request:** Create a threat model for the checkout service and mark inferred flows that require owner confirmation.

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



### Program operations

Delivery integration connects a saved assessment to a team decision. The team must define how missing, incomplete, or adverse evidence affects the release rather than treating any returned status as approval.



#### S-UC16 — CI/CD assessment integration

**Delivery:** Configured integration. **Availability:** Preview.

The delivery team wants an assessment result before a staging release proceeds. Prepare the saved assessment configuration and the pipeline’s authorized invocation path. The pipeline starts and observes a server-side assessment; it does not become the assessment engine itself.

Define the gate policy for failed invocation, incomplete assessment, inconclusive evidence, and accepted findings before enabling the workflow. Retain the run identifier and target revision with the delivery decision. This preview integration should not turn a missing result into a pass or claim synchronous completion when the underlying assessment is still running.

**Inputs:** Saved assessment configuration, pipeline credentials and explicit pass/fail policy.

**Output:** Assessment job and auditable delivery decision.

**Limits:** The pipeline runner is not the assessment engine. Missing or inconclusive evidence needs an explicit gate policy.

**Example request:** Start the configured staging assessment from the release pipeline and fail safely on missing evidence.

**Detailed guide:** [S-06](../guides/security.html#S-06), [S-09](../guides/security.html#S-09), [S-M07](../guides/security.html#S-M07)

**Official references:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS30](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html), [SS31](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html), [SS32](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html), [SS33](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS34](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)



## AWS FinOps Agent



### Cost inquiry and reporting

Cost work starts with a precise query basis. Comparisons, ownership views, forecasts, recurring reports, and operational reviews reuse that basis for different decisions. Observed amounts, projections, and recommendation estimates remain distinct.



#### F-UC01 — Natural-language cost inquiry

**Delivery:** Native function. **Availability:** Preview.

An engineer wants to know how much a service cost during the last complete week. State the cost metric, dates, account scope, currency, and grouping dimension in the question. Those choices define the query; a similar-sounding question with a different metric can legitimately return a different total.

Inspect the returned scope and reproduce a material figure with the same source query before using the answer in a decision. Missing accounts or incomplete dates should be visible. The result is a bounded cost answer, not a general explanation of why the workload consumed that usage.

**Inputs:** Dates, cost metric, currency, account scope and requested dimension.

**Output:** Answer with figures, filters and source context.

**Limits:** A fluent answer is not a substitute for a reproducible source query.

**Example request:** Show production storage cost for the last complete week by account and Region; state the metric and filters.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC02 — Cost variance decomposition

**Delivery:** Native function. **Availability:** Preview.

A service’s bill increased between two complete periods. Hold the cost basis and scope constant, then decompose the monetary delta by service, usage type, quantity, and rate where the available source data supports those dimensions. Reconcile the components back to the total before ranking contributors.

The largest contributor is the part of the arithmetic to investigate first, not automatically the operational cause. The guide’s synthetic example attributes a 574-unit increase across three components and uses additional job evidence to explain only one of them. Preserve unexplained components rather than forcing the whole change into one causal story.

**Inputs:** Comparable windows, same cost basis, grouping dimensions and source permissions.

**Output:** Reconciled delta and ranked contributors.

**Limits:** Contribution arithmetic does not by itself establish the operational cause.

**Example request:** Compare the last two complete weeks and decompose the cost delta into usage and rate changes.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-U01](../guides/finops.html#F-U01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC03 — Cost breakdown by ownership dimension

**Delivery:** Native function with context. **Availability:** Preview.

A platform cost report needs to be understood by the teams that own the accounts. Supply the reviewed account-to-team mapping and the intended grouping or allocation basis, then ask for the cost breakdown using those identifiers. Keep unassigned or ambiguous costs visible instead of distributing them silently.

Check both the arithmetic and the mapping. A correctly summed result can still be assigned to the wrong team when the reference file is stale. This workflow produces an organizational view of source costs; it does not change billing tags or establish a new authoritative chargeback policy by itself.

**Inputs:** Authorized cost data, grouping dimension and optional context file mapping.

**Output:** Dimensioned totals and unmapped items.

**Limits:** Owner mappings require maintained context; tags and account metadata may be incomplete.

**Example request:** Break down this cost by service owner and list every unmapped account or tag.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-M02](../guides/finops.html#F-M02), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC04 — Forecast and commitment coverage review

**Delivery:** Native function. **Availability:** Preview.

Planning requires both an estimate of future spend and an understanding of existing commitment coverage. Ask these as distinct questions with an explicit forecast horizon, cost basis, and commitment scope. Retain the source and assumptions for each result rather than combining them into one observed-spend figure.

Review uncertainty and workload constraints with the accountable financial and service owners. A projected value is not a realized amount, and a coverage observation is not an instruction to purchase a commitment. The agent supports analysis of the available data; purchasing decisions and their authorization remain outside this narrated workflow.

**Inputs:** Forecast horizon, commitment scope and relevant upstream source.

**Output:** Forecast or coverage summary with assumptions.

**Limits:** Forecast and recommendation values are not observed spend and should not be combined without qualification.

**Example request:** Summarize the next-month forecast and current commitment coverage; separate observed and projected values.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC05 — Daily, weekly or monthly cost report

**Delivery:** Configured recurring task. **Availability:** Preview.

The team needs a recurring cost report with a stable comparison basis. Define the reporting period, sections, dimensions, audience, and output format before scheduling it. The task should distinguish observed spend, anomalies, and source recommendation estimates so unlike values are not added together.

Review a trial artifact against the source totals and inspect the saved automation separately from the generated task. A weekly schedule does not specify whether the report includes an incomplete current day. Preserve the task identifier and query basis with each report so changes in the template do not obscure what was actually compared.

**Inputs:** Report contract, schedule, source scope, context and recipients.

**Output:** HTML, PDF or editable presentation artifact.

**Limits:** Schedule, source window and audience are separate settings. Report values still require reconciliation.

**Example request:** Create a weekly cost report with service totals, anomalies, recommendations, owners and unresolved gaps.

**Detailed guide:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04)

**Official references:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)



#### F-UC06 — FinOps operational review pack

**Delivery:** Composed workflow. **Availability:** Preview.

A monthly FinOps review needs decisions, not another copy of the cost table. Start from the reconciled report, anomaly investigations, recommendation dispositions, owner mapping, and the previous action list. Organize the discussion around decisions required and evidence that previous actions had the intended effect.

The result is a review agenda and owned follow-up with explicit unresolved questions. Recommendation savings remain estimates until independently authorized changes and comparable observations support a measured outcome. The meeting process is team-composed; the service supplies analysis, tasks, context, and artifacts that support it.

**Inputs:** Recurring report, owner mappings, recommendation status and review template.

**Output:** Review agenda, decision log and owner/action table.

**Limits:** The review process and acceptance criteria are team-defined, not a separate native feature.

**Example request:** Prepare the monthly FinOps review pack with decisions required, owners and prior action outcomes.

**Detailed guide:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04), [F-M02](../guides/finops.html#F-M02)

**Official references:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html), [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)



### Anomaly and optimization

An anomaly calls for explanation; a recommendation proposes a possible change. Neither is a measured outcome. These workflows connect source evidence to reviewed action and, separately, to post-change measurement.



#### F-UC07 — On-demand cost anomaly investigation

**Delivery:** Native function. **Availability:** Preview.

A cost monitor identifies an unexpected increase. Inspect the anomaly record and query the affected cost dimensions for the relevant period. Where permissions allow, use operational-change records to investigate whether a workload or configuration change explains the increased usage or rate.

Keep numerical attribution and causal evidence separate. A nearby CloudTrail event provides a lead but does not necessarily explain the whole deviation. The final explanation should identify affected costs, supporting observations, and missing inputs. If change evidence is unavailable, preserve the reconciled cost contribution without inventing an operational cause.

**Inputs:** Cost Anomaly Detection record, Cost Explorer access and optional CloudTrail permission.

**Output:** Anomaly explanation with affected services, usage/rate analysis and correlated changes.

**Limits:** CloudTrail events are correlated activity, not automatic proof of cause.

**Example request:** Investigate the MemoryDB anomaly and separate usage, rate and correlated change evidence.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC08 — Event-triggered anomaly response

**Delivery:** Configured automation. **Availability:** Preview.

The team wants qualifying cost anomalies to create investigation work without a manual request. Configure the relevant anomaly monitor, the agent’s required managed-rule permissions, and the automation condition. Select an appropriate destination before authorizing unattended publication.

Trace a matching event into the automation, queued task, result, and optional message. No task indicates a different failure from a completed task whose publication failed. Disabling or deleting the automation stops future task creation; it does not remove existing task records or external messages. The documented event source is Cost Anomaly Detection, not arbitrary business events.

**Inputs:** Anomaly monitor, event-rule permission, automation condition and optional destination.

**Output:** Task history, investigation result and delivery status.

**Limits:** The documented event source is Cost Anomaly Detection. Removing the automation stops future tasks, not existing records.

**Example request:** When a production anomaly exceeds the threshold, investigate it and post the result to the approved channel.

**Detailed guide:** [F-M05](../guides/finops.html#F-M05), [F-03](../guides/finops.html#F-03)

**Official references:** [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS07](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)



#### F-UC09 — Optimization recommendation triage

**Delivery:** Native function with team review. **Availability:** Preview.

An optimization source proposes several changes for a service. Retrieve the original recommendations and inspect their assumptions, resource scope, and overlapping savings estimates. Add workload constraints such as latency, resilience, deployment risk, and ownership before prioritizing the candidates.

Record why each candidate is accepted, deferred, or rejected and identify the normal engineering process for an accepted change. The underlying recommendations originate in the documented optimization services. The agent’s explanation does not independently measure future savings or authorize an infrastructure change.

**Inputs:** Cost Optimization Hub or Compute Optimizer recommendation, workload evidence and owner constraints.

**Output:** Prioritized candidate, rejected/deferred reason and accepted next step.

**Limits:** The agent contextualizes upstream recommendations; it does not independently calculate or authorize the change.

**Example request:** Review the storage recommendations, identify overlapping savings and list the reliability constraints.

**Detailed guide:** [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



#### F-UC10 — Post-change savings measurement

**Delivery:** Composed workflow. **Availability:** Preview service; team process.

An approved optimization has been implemented, and the owner wants to know what changed. Select comparable before-and-after periods and record traffic, pricing, allocation, and service-health differences that could affect the result. Reconcile the costs using the same metric and scope.

Report the observed change together with its attribution limits. A lower bill is not sufficient evidence that the optimization caused the decrease when demand also fell. This is a team measurement workflow using source-backed analysis, not a service guarantee of savings. Unexplained differences remain part of the outcome rather than being removed from the report.

**Inputs:** Implemented change record, comparable periods and service indicators.

**Output:** Measured outcome with attribution limits.

**Limits:** A lower bill does not prove the change caused the decrease; traffic, prices and allocation may differ.

**Example request:** Compare the post-change period with a matched baseline and state what cannot be attributed to the change.

**Detailed guide:** [F-U01](../guides/finops.html#F-U01), [F-M01](../guides/finops.html#F-M01), [F-08](../guides/finops.html#F-08)

**Official references:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)



### Context and governance

Organizational context makes financial data interpretable. Files hold operator-maintained reference material; memory retains preferences and corrections. Their update and visibility rules differ, so the authoritative representation should be explicit.



#### F-UC11 — Cost ownership and allocation context

**Delivery:** Configured context. **Availability:** Preview.

Cost inquiries repeatedly require an explanation of which team owns each account. Maintain that mapping in a focused reference file with the identifiers actually returned by the cost source. Review it with the responsible owners, upload the approved revision, and test a question whose answer depends on one known mapping.

When ownership changes, update the authoritative source and the active uploaded file deliberately. Context files are visible to users with agent access and cannot be rewritten by the agent through conversation. The mapping helps interpretation and routing; a statement in it does not grant permission to publish to a destination.

**Inputs:** Supported context file with non-sensitive ownership and allocation data.

**Output:** Context available to relevant tasks and conversations.

**Limits:** Files are visible to agent users, cannot be conversationally rewritten and have file/total size limits.

**Example request:** Use the approved account-owner mapping and list every cost item that lacks an owner.

**Detailed guide:** [F-M02](../guides/finops.html#F-M02)

**Official references:** [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)



#### F-UC12 — Persistent reporting preferences

**Delivery:** Native memory. **Availability:** Preview.

A team wants future reports to use a consistent view and presentation order. Supply the non-sensitive preference through an explicit remember request, then open another conversation and inspect whether it is applied. Keep the requested cost basis explicit in material analyses even when the preference has been retained.

When the convention changes, update or forget the preference and test again. This does not modify a reference file containing similar instructions or rewrite an earlier report. Persistent memory is instance-local; a successful preference test in one agent does not establish that another instance shares it.

**Inputs:** Explicit remember, update or forget request.

**Output:** Agent-instance memory applied in later sessions.

**Limits:** Memory is distinct from reference files and should be tested independently.

**Example request:** Remember that executive reports use amortized cost and update the preference when the policy changes.

**Detailed guide:** [F-M03](../guides/finops.html#F-M03)

**Official references:** [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)



### Automation and collaboration

Automation creates future tasks, tasks produce results, and integrations publish supported effects. These separate objects explain where to inspect failure, which approval behavior applies, and what remains after execution is stopped.



#### F-UC13 — Scheduled recurring task

**Delivery:** Configured automation. **Availability:** Preview.

A weekly optimization review should create a new execution record each time it runs. Define the schedule, the comparison period, and the desired output separately, then inspect the saved automation. Review the first created task in the shared queue and verify that its result corresponds to the intended period.

Pausing or deleting the schedule concerns future work. A task already running needs its own control, and an existing report remains a historical artifact. These distinctions are important when a recurring job is replaced: avoid leaving two active automations merely because the new one has a clearer name.

**Inputs:** Prompt, schedule, tools/data permissions and output expectations.

**Output:** Automation record and separate task history.

**Limits:** Deleting an automation stops future starts but does not delete existing tasks or messages.

**Example request:** Run the weekly optimization review every Monday at the stated UTC time.

**Detailed guide:** [F-03](../guides/finops.html#F-03)

**Official references:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)



#### F-UC14 — Jira follow-up creation

**Delivery:** Configured integration. **Availability:** Preview.

A cost analysis has produced an accepted action and an owner. Confirm the connected Jira project and the content appropriate for its audience, then request the supported issue or comment operation. Include the source evidence and acceptance criteria rather than only an estimated savings figure.

Interactive and on-demand Jira actions request approval, while scheduled or event-driven actions use authorization established during automation setup. Inspect the actual issue or comment and retain its relationship to the task. Do not assume that this integration can perform arbitrary field changes, workflow transitions, or deletion.

**Inputs:** Connected Jira project, reviewed content and owner.

**Output:** Jira issue/comment and task history.

**Limits:** Interactive and on-demand Jira actions require approval; automation actions are pre-authorized at setup.

**Example request:** Create a Jira issue for the accepted storage optimization with evidence, owner and acceptance criteria.

**Detailed guide:** [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06), [F-08](../guides/finops.html#F-08)

**Official references:** [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)



#### F-UC15 — Slack publication

**Delivery:** Configured integration. **Availability:** Preview.

The incident or FinOps channel needs a reviewed cost summary. Confirm the workspace registration, agent-specific channel connection, and application membership before publication. Limit the message to information appropriate for that channel and link the underlying analysis where suitable.

Slack posting has no approval prompt in the documented behavior, including interactive requests. The destination and message scope therefore need review before invocation rather than at an expected confirmation step. Inspect delivery separately from task completion. Posting does not establish that the agent can read channel conversations or process replies.

**Inputs:** Registered workspace, agent connection, channel and reviewed message scope.

**Output:** Slack post and delivery result.

**Limits:** Slack posting has no approval prompt, including interactive use; channel membership and sensitive content must be reviewed.

**Example request:** Post the approved anomaly summary to the FinOps incident channel.

**Detailed guide:** [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06), [F-08](../guides/finops.html#F-08)

**Official references:** [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)



#### F-UC16 — Downloadable report artifact

**Delivery:** Native output. **Availability:** Preview.

A reviewer needs an artifact that can be read outside the conversation. Specify the report audience, query basis, required tables, and supported output format. Inspect the generated artifact against the task’s source results and request revisions that preserve the comparison basis unless a change is intentional.

The artifact is a version of the analysis, not independent evidence that its totals are correct. Retain its relationship to the task and reviewed period when sharing it. Deleting the service artifact does not necessarily remove copies already distributed to collaboration systems or downloaded by recipients.

**Inputs:** Source query, report instructions and desired format.

**Output:** HTML, PDF or editable presentation artifact.

**Limits:** Formatting quality does not establish numerical or causal accuracy; external copies have their own lifecycle.

**Example request:** Generate an editable monthly cost report and include the query basis for every chart.

**Detailed guide:** [F-04](../guides/finops.html#F-04)

**Official references:** [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)
