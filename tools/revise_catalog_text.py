#!/usr/bin/env python3
"""Apply the catalog's authored narrative edition once, then remove this script."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
NARRATIVES={
'D-UC01':[
'An on-call engineer receives several alerts for the same service. Before opening another investigation, the engineer needs to know whether the new signal belongs to work already in progress. Inspect the triage decision and its reason, then follow the primary investigation when the signal was linked. A skipped signal should identify the matching exclusion rather than disappear from the operating record.',
'When correlation is wrong, unlink the signal so it can be investigated separately. When a skip criterion excluded a relevant event, review that criterion and use the supported unskip operation. The result of this use case is correct routing and an identifiable investigation, not a root-cause conclusion. Root-cause analysis follows in the next use case.'
],
'D-UC02':[
'A service owner sees elevated errors after a deployment. The investigation begins with the affected service, incident time, and symptoms, not with an assumed deployment defect. Connect the available logs, metrics, traces, repository context, and deployment records, then inspect how the investigation relates the observations across those sources.',
'The useful result identifies the measurements that support each explanation and the sources that could not be read. A deployment timestamp may provide a lead, but its proximity to the error increase is not sufficient proof of cause. When evidence conflicts, preserve the competing explanations and supply the missing observation through investigation steering rather than turning a plausible summary into a confirmed diagnosis.'
],
'D-UC03':[
'During an investigation, the engineer establishes that the database is healthy even though the current hypothesis blames connection exhaustion. Supply the contrary measurements and their time window to the active investigation. Ask the agent to reconsider the hypothesis and examine the upstream dependency rather than starting an unrelated conversation with no investigation context.',
'Review the revised analysis for an actual change in reasoning and supporting evidence. If the new evidence cannot be accessed, retain that limitation. Steering affects the current investigation; completed-investigation feedback is the separate path for recording a verified correction for later work. Neither operation authorizes a production change.'
],
'D-UC04':[
'Once the current evidence supports a likely failure mechanism, the incident owner needs a mitigation that can be reviewed. Ask for the proposed target, exact change, expected effect, risks, rollback, and recovery checks. Compare that proposal with the approved runbook and the evidence already collected, especially where the proposed action would affect another service.',
'The output is a decision document: it should make it possible to approve, reject, or revise the proposal without guessing its effect. A generated plan remains separate from execution. It can be carried out through the ordinary engineering process, or through an eligible directed-action path after the additional controls described in the next use case have been satisfied.'
],
'D-UC05':[
'An incident owner has accepted a narrowly scoped mitigation and wants to use the documented action path. Confirm Agent Space enablement, the target-account role or connected-tool configuration, and the classification of the operation. Review the actual parameters presented for approval; a broadly named role is not the approval record.',
'After the operator approves the eligible action, inspect the resulting resource state and the available attribution evidence. Recovery must still be checked against service measurements. If execution is denied, locate the failed gate instead of widening all permissions. This workflow does not convert the earlier mitigation recommendation into standing authorization for subsequent changes.'
],
'D-UC06':[
'Before an on-call handover, the engineer needs a current view of one service. Define the service identity and a bounded period, such as the previous complete hour, and ask for error rate, latency, saturation, active alarms, and recent changes from the connected sources. A health answer is more useful when it identifies its observation time and any unavailable signal.',
'Compare one material figure with the underlying monitoring query, using the same aggregation and dimensions. An absent log source should appear as a data gap rather than as an absence of errors. The answer supports a handover or investigation decision; it does not replace the monitoring system or create a complete continuous health assessment.'
],
'D-UC07':[
'During an active incident, the incident commander needs a brief update that explains what has changed since the preceding observation. Configure a specialist task with the incident identifier, selected telemetry tools, and a short explicit lookback window. Ask for changed measurements, the status of open hypotheses, missing reads, and the next check rather than a repetition of the whole incident history.',
'A report can analyze minute-resolution measurements without arriving every minute. The documented custom-agent schedule uses a flexible window of up to 30 minutes; execution time is additional. For time-critical updates, invoke the task on demand or use a separately tested triggering design. Record both the measurement window and report-generation time so a delayed bulletin is not mistaken for current telemetry.'
],
'D-UC08':[
'A platform team wants the same service-health report each week. Define the covered services, complete reporting period, metric aggregation, comparison period, and sections before creating the custom agent. Select the real telemetry and incident tools and attach only the knowledge required to interpret service names, owners, and reporting conventions.',
'Inspect a trial invocation before enabling recurring execution. The report should connect significant changes to source observations, identify incomplete data, and distinguish incident counts from ongoing problems. Its purpose is a repeatable health record. Decisions about priorities and ownership belong to the operational review that consumes this report, rather than being inferred from a formatted health table.'
],
'D-UC09':[
'A release engineer wants to review the changes delivered during the previous week. The input is deployment history with service and revision identifiers, not simply merged pull requests. Configure the task to distinguish attempted, successful, failed, and rolled-back deployments using the states exposed by the connected delivery tools.',
'The result should make it possible to trace a reported deployment to its source record and compare it with incidents in the same service and period. Similar timestamps are useful for investigation but do not establish causality. Missing pipeline access or ambiguous status mappings should be listed explicitly so the report is not presented as a complete release history.'
],
'D-UC10':[
'An operational review turns measurements into decisions. Start with the reviewed service-health and deployment reports, incident themes, prevention recommendations, and the previous meeting’s action list. The task is to assemble the evidence relevant to unresolved decisions, not to create another differently titled copy of the weekly health report.',
'Organize the review around decisions required, their supporting observations, the accountable owner, and the next verification date. Ask owners to confirm status rather than treating silence as completion. This is a team-designed workflow built from configured evidence access and reporting; the meeting, prioritization, and acceptance of actions remain engineering responsibilities.'
],
'D-UC11':[
'Several investigations may share an operational weakness even when they were triggered by different alarms. Review the relevant investigation history and ask which causes or contributing conditions recur. Group the evidence by the proposed pattern and retain the supporting investigation identifiers so the grouping can be challenged.',
'This analysis differs from retrieving the prior cause of one alarm: its purpose is to identify cross-incident themes worth prevention work. Similar symptoms without verified common causes should remain a candidate pattern. The next step is to review the prevention recommendations against those themes rather than assuming that a historical cluster explains the next incident.'
],
'D-UC12':[
'The reliability owner has identified recurring themes and needs a manageable prevention backlog. Run or inspect the documented prevention evaluation, then review each recommendation against the incidents it addresses. Separate observability improvements, infrastructure changes, governance work, and code changes because they have different owners and acceptance evidence.',
'Keep an accepted recommendation linked to its source evidence and normal change process. A recommendation’s priority or estimated effect is not proof that the change has been implemented. During the next operational review, inspect actual progress and post-change observations. This closes the team’s improvement loop without claiming autonomous implementation or measured benefit before either exists.'
],
'D-UC13':[
'The same alarm fires again, and the previous investigation has a known cause. Inspect the relevant retained context and make it available to the current investigation. Then compare the earlier explanation with the new measurements. The historical entry is a lead that can shorten the list of questions; it is not a substitute for the new time window’s evidence.',
'Record whether a relevant entry existed, whether its retrieval was observable, and whether the new diagnosis was correct. Those are three separate results. If current evidence contradicts the old cause, preserve the contradiction and provide a verified correction when appropriate. The worked recurring-alarm example in the guide illustrates this distinction with synthetic measurements.'
],
'D-UC14':[
'A team has several overlapping timeout SOPs maintained by different owners. First reconcile their scope, resolve contradictory steps, remove stale tool names, and identify the approved procedure. Only then package that procedure as a skill with a description that states when it applies and which agent types may use it.',
'Keep the reviewed source in Git and test a request that should match the skill alongside one that should not. The supporting references should explain the expected observations and the point at which the procedure stops or escalates. Consolidation is authored team work; skill selection is the platform mechanism. A skill neither creates the referenced tools nor grants permission to use them.'
],
'D-UC15':[
'The operations team requires every incident answer to identify its service, UTC window, evidence sources, and unresolved questions. Put these standing conventions in the appropriate global or agent-specific instructions rather than duplicating them in every task. Save the change and start a new session to inspect the resulting behavior.',
'An existing session retains its startup instructions, so it is not a valid test of the updated text. Compare old and new sessions deliberately and retain the instruction source in Git. These conventions improve the readability of operational records; access control and authorization remain enforced by the connected systems rather than by the wording of the instructions.'
],
'D-UC16':[
'A service owner needs an architecture description before changing a dependency. Start from discovered resources and the topology’s service, repository, pipeline, and dependency relationships. Compare those relationships with the deployed configuration and source revision, distinguishing directly observed relationships from inferred ones.',
'Write the reviewed result as a maintained service description with identifiers, evidence links, and unresolved edges. The topology is useful input to that document, but it is not a guaranteed complete inventory or an automatic update to the team’s architecture repository. This use case produces owner-reviewed documentation; the following refresh use case checks whether the underlying environment model has changed.'
],
'D-UC17':[
'After a new integration or infrastructure change, the previously learned environment summary may be incomplete. Request or inspect the supported refresh and follow the managed learning run to its resulting knowledge. Compare one known changed resource or relationship with the new output rather than accepting a submitted refresh request as evidence of completion.',
'Record the observed version and the discrepancies that remain. A missing topology node can reflect discovery limitations and does not by itself establish denied resource access. Refreshing the environment model supports later investigations; it does not replace source-controlled architecture documentation or grant a custom agent access to every retained store.'
],
'D-UC18':[
'An operations standard requires a small set of staging resources to have particular logging and access settings. Configure a custom task with read-only configuration tools, the explicit resource list, and the reviewed standard. Each reported finding should identify the resource, the applicable rule, and the actual value that was read.',
'Review a known conforming and a known nonconforming example before scheduling the task. An unavailable read is an unassessed resource, not a pass. The output is a scoped configuration audit for the chosen rules; it is not a built-in universal compliance engine or permission to repair findings automatically.'
],
'D-UC19':[
'A service has gradually become slower without a single clear incident. Define complete comparison periods, metric dimensions, aggregation, and the relevant traffic denominator. Ask the configured task to compare latency, errors, and capacity indicators and to identify the periods where the behavior materially changed.',
'Inspect the underlying series for gaps and changes in traffic composition before attributing the trend to a release. A change in a percentile or absolute error count can reflect a different workload mix. The result is a sourced trend analysis with candidate explanations and missing evidence, providing a starting point for focused investigation rather than a causal verdict.'
],
'D-UC20':[
'An incident spans a monitoring alert, a deployment, and a service ticket that use different names for the same application. Supply the identity mapping and a bounded question to a custom task with the required tools. Ask it to build an evidence table that preserves source identifiers and timestamps instead of merging records merely because their descriptions look similar.',
'Review unmatched records and contradictory revision information explicitly. A connected tool that returns no data may have the wrong scope or permissions. The useful result identifies which observations refer to the same service and change, and which relationships remain hypotheses. Those distinctions make the subsequent investigation reproducible.'
],
'D-UC21':[
'Before release, a team wants to examine a retry-policy change for operational risk. Use the eligible readiness-review path with the candidate revision, relevant repositories, topology, and release context. Review the findings against the intended dependency behavior and the service’s existing resilience assumptions.',
'A readiness review analyzes a proposed change; it does not prove that the deployed application behaves correctly. Retain unresolved dependencies and scope limitations and route accepted findings through engineering review. This feature is a separate preview path, so production-operations availability must not be used as evidence that the same review is available for every Region or repository.'
],
'D-UC22':[
'A staging application is ready for an active release check. Prepare disposable test data, approved identities, explicit allowed operations, and disabled external side effects. The task exercises the deployed target, so the target revision and reachable endpoints matter more than the name of the branch that produced it.',
'Review the observed requests and results with the application owner. Active testing can create, modify, or delete application data; infrastructure read permissions do not make those requests harmless. The result describes the executed test and its uncovered areas, not blanket release approval. Unexpected effects require stopping and reviewing the configuration before further execution.'
],
'S-UC01':[
'An application owner has authorized a staging assessment for a specific release. Create the test configuration with the verified target, permitted network surface, source context, test identities, and work limit. Save the configuration separately from starting a run so another reviewer can inspect the intended scope before execution.',
'Follow the resulting run and retain its target revision, exclusions, and observed coverage. Findings need review against their evidence, while failed authentication or unreachable paths remain assessment gaps. The test sends real requests and can change application state; technical domain verification does not replace the application owner’s authorization.'
],
'S-UC02':[
'The application’s most important functions are behind authentication, and an unauthenticated scan would not reach them. Configure representative test roles and login instructions, then use authentication preflight to determine whether the credentials are obtained and successfully applied. Inspect the actual application identity rather than only a successful secret read.',
'Assess the protected workflow under the intended role and retain the routes reached. A successful login as an administrator cannot substitute for coverage of an ordinary customer’s authorization boundary. If MFA, navigation, or application permissions fail, record the missing coverage before interpreting an absence of findings.'
],
'S-UC03':[
'A staging service is reachable only from a private network. Configure the documented private path, DNS, subnets, and security groups together with the target and exclusion rules. Source-control reachability and application-target reachability are separate paths, so test the one the assessment actually requires.',
'Once the target is reachable, authenticate with the approved test identity and inspect the resulting run. Do not widen the authorized surface simply because a supporting dependency is private. An unreachable production callback should remain excluded, while an approved login dependency may require supporting access without becoming an attack target.'
],
'S-UC04':[
'The security team wants separate assessments of a stable staging application at regular intervals. Reuse a saved configuration and configure the supported schedule, but identify the target revision and credential state for each run. A reusable definition does not freeze an application that continues to be deployed.',
'Compare the successive run records and investigate incomplete authentication or coverage before interpreting a reduction in findings. Review the continuing authorization and work limits as the application changes. The schedule creates assessment opportunities; it does not guarantee that every scheduled run successfully exercises the same application surface.'
],
'S-UC05':[
'Repeated assessment runs spend time navigating the same login flow. After a successful authentication, inspect the Login Optimization setting and the documented reuse behavior. Keep the configuration enabled where appropriate, while still verifying the actual application role and protected routes on each run.',
'When the staging login flow changes, test the new flow rather than assuming the retained procedure remains sufficient. Disabling reuse preserves the learned procedure according to the guidance, so a toggle is not a deletion operation. This use case concerns repeated authenticated access, not a general vulnerability-memory or model-training capability.'
],
'S-UC06':[
'A completed assessment contains findings of different severity and evidential strength. Review each material finding in the context of the affected revision, reachable role, exposed data, and reproduction evidence. Add application-owner context before deciding which finding needs immediate repair and which requires more investigation.',
'The outcome is a disposition and an accountable next action, not merely a sorted severity list. Findings with incomplete evidence should retain that uncertainty. Link accepted work to the original finding identifier so remediation, deployment, and later verification remain traceable even if the issue title or owner changes.'
],
'S-UC07':[
'An accepted finding needs an owned remediation ticket. Connect the permitted Jira Cloud project and review whether issue creation and comments are enabled for that project. Before publication, check that the project audience is appropriate for the finding’s sensitive technical details.',
'Create the issue with a reference to the finding, affected revision, proposed work, and acceptance evidence. Later updates should preserve that finding relationship. Jira is the external work-tracking record; disconnecting the integration does not delete existing issues. The team’s prioritization and closure decisions remain separate from the publication action.'
],
'S-UC08':[
'A developer has accepted a finding and wants a repair proposal against the affected source. Confirm the repository and supported remediation settings, then inspect the proposed patch or pull request. The review should include the security change, regression tests, and any unrelated behavior introduced by the proposal.',
'Run the normal build and review process before deployment. A generated proposal that fails tests is unfinished work, and a merged revision that has not reached the target is not ready for revalidation. Preserve the finding identifier through the change and deployment records so the next test can evaluate the intended repair.'
],
'S-UC09':[
'The reviewed repair has been deployed to the original authorized environment. Select the existing finding for revalidation and inspect the new job, including the current authentication configuration and target revision. The job repeats the selected validation steps rather than conducting a broad new assessment.',
'Interpret the result within that scope. A reproduced finding remains active evidence of the issue; non-reproduction supports resolution only when the relevant identity and path were actually reached. Keep the original finding and the linked job history. A failed login or changed test environment must not be mistaken for a successful repair.'
],
'S-UC10':[
'A team wants a baseline review of a repository or supported source package. Connect the intended source revision and select the eligible review modes. Vulnerability analysis and evaluation against enabled requirement packs answer related but different questions, so the requested criteria should be explicit.',
'Review findings in their code context and inspect preflight failures separately from completed analysis. The result applies to the selected source and modes; it is not a substitute for testing the deployed application. This preview workflow has provider and availability boundaries that must be checked before it becomes part of the delivery process.'
],
'S-UC11':[
'A pull request changes an authorization handler. Use the supported change-focused review path and identify the exact revision being assessed. Provide the repository context and enabled criteria needed to evaluate the change rather than treating an isolated diff as a complete description of the system.',
'When further commits arrive, confirm whether another review is required for that provider and trigger path. Retain revision-specific findings and distinguish a stale result from a finding that still applies. Optional comments or remediation depend on the configured write features; read access alone does not authorize those repository effects.'
],
'S-UC12':[
'The organization has an explicit requirement for access to account-owned invoices. Configure its applicability and compliance criteria in an enabled pack, then run an eligible design or code review with requirement evaluation selected. Inspect why the requirement applied before interpreting its compliance result.',
'Use a known compliant handler, a violating handler, and an inapplicable public resource as review examples. These expose different mistakes in the criteria. A framework label or a generated pack does not certify compliance; the result is an assessment against the selected requirements and supplied evidence.'
],
'S-UC13':[
'Policy owners have revised several overlapping security standards. Reconcile the governing documents and identify the approved source before generating a replacement requirement pack. Compare the generated applicability and compliance statements with that source, including requirements that had previously been added manually.',
'Regeneration replaces the existing pack contents rather than appending to them. Review the proposed replacement before enabling it for subsequent assessments, and keep the policy and reviewed requirement source in Git. This is a controlled authoring workflow; it must not silently replace a working pack merely because new documents were uploaded.'
],
'S-UC14':[
'A team proposes a new payment-service design before implementation. Submit the current design material and relevant application context for the eligible review, and identify the enabled requirements that govern it. The assessment should expose assumptions about identity, data flows, and trust boundaries that need owner confirmation.',
'Review the findings with the architect and distinguish missing design evidence from a demonstrated violation. Design review has a one-off lifecycle, with cloning used for a new review; it should not be described as an automatically refreshed continuous model. The result informs design work rather than approving the future implementation.'
],
'S-UC15':[
'A service boundary has changed and the team needs an updated threat model. Supply explicit scope documents and the relevant architecture and source evidence. Review the inferred system overview, components, data flows, and trust boundaries before evaluating individual threats.',
'Correct an incorrect boundary at the model input rather than dismissing every threat that follows from it. Retain evidence for the accepted threats and identify inferred relationships that remain unverified. The result is a reviewed model for that scope and run, not proof that every possible threat has been discovered.'
],
'S-UC16':[
'The delivery team wants an assessment result before a staging release proceeds. Prepare the saved assessment configuration and the pipeline’s authorized invocation path. The pipeline starts and observes a server-side assessment; it does not become the assessment engine itself.',
'Define the gate policy for failed invocation, incomplete assessment, inconclusive evidence, and accepted findings before enabling the workflow. Retain the run identifier and target revision with the delivery decision. This preview integration should not turn a missing result into a pass or claim synchronous completion when the underlying assessment is still running.'
],
'F-UC01':[
'An engineer wants to know how much a service cost during the last complete week. State the cost metric, dates, account scope, currency, and grouping dimension in the question. Those choices define the query; a similar-sounding question with a different metric can legitimately return a different total.',
'Inspect the returned scope and reproduce a material figure with the same source query before using the answer in a decision. Missing accounts or incomplete dates should be visible. The result is a bounded cost answer, not a general explanation of why the workload consumed that usage.'
],
'F-UC02':[
'A service’s bill increased between two complete periods. Hold the cost basis and scope constant, then decompose the monetary delta by service, usage type, quantity, and rate where the available source data supports those dimensions. Reconcile the components back to the total before ranking contributors.',
'The largest contributor is the part of the arithmetic to investigate first, not automatically the operational cause. The guide’s synthetic example attributes a 574-unit increase across three components and uses additional job evidence to explain only one of them. Preserve unexplained components rather than forcing the whole change into one causal story.'
],
'F-UC03':[
'A platform cost report needs to be understood by the teams that own the accounts. Supply the reviewed account-to-team mapping and the intended grouping or allocation basis, then ask for the cost breakdown using those identifiers. Keep unassigned or ambiguous costs visible instead of distributing them silently.',
'Check both the arithmetic and the mapping. A correctly summed result can still be assigned to the wrong team when the reference file is stale. This workflow produces an organizational view of source costs; it does not change billing tags or establish a new authoritative chargeback policy by itself.'
],
'F-UC04':[
'Planning requires both an estimate of future spend and an understanding of existing commitment coverage. Ask these as distinct questions with an explicit forecast horizon, cost basis, and commitment scope. Retain the source and assumptions for each result rather than combining them into one observed-spend figure.',
'Review uncertainty and workload constraints with the accountable financial and service owners. A projected value is not a realized amount, and a coverage observation is not an instruction to purchase a commitment. The agent supports analysis of the available data; purchasing decisions and their authorization remain outside this narrated workflow.'
],
'F-UC05':[
'The team needs a recurring cost report with a stable comparison basis. Define the reporting period, sections, dimensions, audience, and output format before scheduling it. The task should distinguish observed spend, anomalies, and source recommendation estimates so unlike values are not added together.',
'Review a trial artifact against the source totals and inspect the saved automation separately from the generated task. A weekly schedule does not specify whether the report includes an incomplete current day. Preserve the task identifier and query basis with each report so changes in the template do not obscure what was actually compared.'
],
'F-UC06':[
'A monthly FinOps review needs decisions, not another copy of the cost table. Start from the reconciled report, anomaly investigations, recommendation dispositions, owner mapping, and the previous action list. Organize the discussion around decisions required and evidence that previous actions had the intended effect.',
'The result is a review agenda and owned follow-up with explicit unresolved questions. Recommendation savings remain estimates until independently authorized changes and comparable observations support a measured outcome. The meeting process is team-composed; the service supplies analysis, tasks, context, and artifacts that support it.'
],
'F-UC07':[
'A cost monitor identifies an unexpected increase. Inspect the anomaly record and query the affected cost dimensions for the relevant period. Where permissions allow, use operational-change records to investigate whether a workload or configuration change explains the increased usage or rate.',
'Keep numerical attribution and causal evidence separate. A nearby CloudTrail event provides a lead but does not necessarily explain the whole deviation. The final explanation should identify affected costs, supporting observations, and missing inputs. If change evidence is unavailable, preserve the reconciled cost contribution without inventing an operational cause.'
],
'F-UC08':[
'The team wants qualifying cost anomalies to create investigation work without a manual request. Configure the relevant anomaly monitor, the agent’s required managed-rule permissions, and the automation condition. Select an appropriate destination before authorizing unattended publication.',
'Trace a matching event into the automation, queued task, result, and optional message. No task indicates a different failure from a completed task whose publication failed. Disabling or deleting the automation stops future task creation; it does not remove existing task records or external messages. The documented event source is Cost Anomaly Detection, not arbitrary business events.'
],
'F-UC09':[
'An optimization source proposes several changes for a service. Retrieve the original recommendations and inspect their assumptions, resource scope, and overlapping savings estimates. Add workload constraints such as latency, resilience, deployment risk, and ownership before prioritizing the candidates.',
'Record why each candidate is accepted, deferred, or rejected and identify the normal engineering process for an accepted change. The underlying recommendations originate in the documented optimization services. The agent’s explanation does not independently measure future savings or authorize an infrastructure change.'
],
'F-UC10':[
'An approved optimization has been implemented, and the owner wants to know what changed. Select comparable before-and-after periods and record traffic, pricing, allocation, and service-health differences that could affect the result. Reconcile the costs using the same metric and scope.',
'Report the observed change together with its attribution limits. A lower bill is not sufficient evidence that the optimization caused the decrease when demand also fell. This is a team measurement workflow using source-backed analysis, not a service guarantee of savings. Unexplained differences remain part of the outcome rather than being removed from the report.'
],
'F-UC11':[
'Cost inquiries repeatedly require an explanation of which team owns each account. Maintain that mapping in a focused reference file with the identifiers actually returned by the cost source. Review it with the responsible owners, upload the approved revision, and test a question whose answer depends on one known mapping.',
'When ownership changes, update the authoritative source and the active uploaded file deliberately. Context files are visible to users with agent access and cannot be rewritten by the agent through conversation. The mapping helps interpretation and routing; a statement in it does not grant permission to publish to a destination.'
],
'F-UC12':[
'A team wants future reports to use a consistent view and presentation order. Supply the non-sensitive preference through an explicit remember request, then open another conversation and inspect whether it is applied. Keep the requested cost basis explicit in material analyses even when the preference has been retained.',
'When the convention changes, update or forget the preference and test again. This does not modify a reference file containing similar instructions or rewrite an earlier report. Persistent memory is instance-local; a successful preference test in one agent does not establish that another instance shares it.'
],
'F-UC13':[
'A weekly optimization review should create a new execution record each time it runs. Define the schedule, the comparison period, and the desired output separately, then inspect the saved automation. Review the first created task in the shared queue and verify that its result corresponds to the intended period.',
'Pausing or deleting the schedule concerns future work. A task already running needs its own control, and an existing report remains a historical artifact. These distinctions are important when a recurring job is replaced: avoid leaving two active automations merely because the new one has a clearer name.'
],
'F-UC14':[
'A cost analysis has produced an accepted action and an owner. Confirm the connected Jira project and the content appropriate for its audience, then request the supported issue or comment operation. Include the source evidence and acceptance criteria rather than only an estimated savings figure.',
'Interactive and on-demand Jira actions request approval, while scheduled or event-driven actions use authorization established during automation setup. Inspect the actual issue or comment and retain its relationship to the task. Do not assume that this integration can perform arbitrary field changes, workflow transitions, or deletion.'
],
'F-UC15':[
'The incident or FinOps channel needs a reviewed cost summary. Confirm the workspace registration, agent-specific channel connection, and application membership before publication. Limit the message to information appropriate for that channel and link the underlying analysis where suitable.',
'Slack posting has no approval prompt in the documented behavior, including interactive requests. The destination and message scope therefore need review before invocation rather than at an expected confirmation step. Inspect delivery separately from task completion. Posting does not establish that the agent can read channel conversations or process replies.'
],
'F-UC16':[
'A reviewer needs an artifact that can be read outside the conversation. Specify the report audience, query basis, required tables, and supported output format. Inspect the generated artifact against the task’s source results and request revisions that preserve the comparison basis unless a change is intentional.',
'The artifact is a version of the analysis, not independent evidence that its totals are correct. Retain its relationship to the task and reviewed period when sharing it. Deleting the service artifact does not necessarily remove copies already distributed to collaboration systems or downloaded by recipients.'
]}
GROUPS={
'Incident operations':'Incident work proceeds from routing to investigation, then to mitigation review and any separately authorized action. These use cases describe those decisions independently so that a correctly routed signal is not mistaken for a confirmed diagnosis or an approved change.',
'Health reporting and reviews':'A health query answers an immediate operational question. A bulletin records change during an incident, a recurring report preserves a comparable period, and an operational review turns those records into decisions. Their inputs overlap, but their purposes and acceptance evidence differ.',
'Pattern analysis and improvement':'An incident explains one occurrence. Pattern analysis compares occurrences, and prevention review turns recurring evidence into proposed improvements. Keep the historical evidence attached to the pattern so that its interpretation can be revised.',
'Knowledge and documentation':'Operational knowledge moves from source evidence and approved procedures into representations an agent can retrieve or apply. The following workflows distinguish historical context, standing instructions, selected runbook skills, topology observations, and owner-reviewed documentation.',
'Custom operational work':'Custom agents apply selected tools and explicit instructions to specialist tasks. The team supplies the resource scope, standards, identifiers, and expected output. These workflows are configurable applications, not additional universal audit or correlation engines.',
'Release and change assurance':'Reviewing a proposed change and exercising a deployed application answer different questions. Both require explicit scope, and active testing introduces application effects that source review does not. Availability must be checked for the particular preview path.',
'Application assessment':'Application testing begins with an authorized target and a reproducible configuration. Public access, authenticated workflows, private reachability, and recurring execution introduce different prerequisites. Each run retains its own scope and evidence.',
'Authentication and access':'Authentication enables a test to reach protected behavior. Reusing a successful login procedure can support repeated runs, but actual role and route coverage still need verification when the application changes.',
'Findings and remediation':'A finding is evidence to review, not an automatically completed engineering task. The following workflows retain the relationship between the accepted finding, the proposed repair, the deployed revision, and the verification result.',
'Shift-left review':'Source, design, and threat-model assessments examine different representations of the same application. Requirements supply explicit criteria, while scope and source revisions define what is actually evaluated. Generated criteria require review before they govern later work.',
'Program operations':'Delivery integration connects a saved assessment to a team decision. The team must define how missing, incomplete, or adverse evidence affects the release rather than treating any returned status as approval.',
'Cost inquiry and reporting':'Cost work starts with a precise query basis. Comparisons, ownership views, forecasts, recurring reports, and operational reviews reuse that basis for different decisions. Observed amounts, projections, and recommendation estimates remain distinct.',
'Anomaly and optimization':'An anomaly calls for explanation; a recommendation proposes a possible change. Neither is a measured outcome. These workflows connect source evidence to reviewed action and, separately, to post-change measurement.',
'Context and governance':'Organizational context makes financial data interpretable. Files hold operator-maintained reference material; memory retains preferences and corrections. Their update and visibility rules differ, so the authoritative representation should be explicit.',
'Automation and collaboration':'Automation creates future tasks, tasks produce results, and integrations publish supported effects. These separate objects explain where to inspect failure, which approval behavior applies, and what remains after execution is stopped.'}

def apply():
    path=ROOT/'catalog/use-cases.json';catalog=json.loads(path.read_text())
    assert {e['id'] for e in catalog['entries']}==set(NARRATIVES)
    for e in catalog['entries']:
        e['narrative']=NARRATIVES[e['id']]
        e['narrative_status']='Authored engineering workflow based on the linked documented mechanisms; not an executed service result.'
        if e['id']=='D-UC07':
            e.update(title='Incident status bulletin',summary='Prepare a short, timestamped update from current incident evidence without implying a guaranteed minute-by-minute delivery schedule.',cadence='On demand; scheduling is not exact-minute',constraints='Telemetry resolution, lookback period, schedule window, and execution time are different. The documented custom-agent schedule has a flexible window of up to 30 minutes.',example='Report what changed in the active incident during the previous five complete minutes, including the observation window, generation time, and missing sources.')
        if e['id']=='D-UC13':e['title']='Recurring-alarm investigation with historical context';e['delivery']='Built-in function with retained context'
        if e['id']=='D-UC15':e['title']='Applying incident reporting conventions'
        if e['id']=='S-UC05':e['title']='Repeated assessment with retained login procedure'
        if e['id']=='F-UC07':e['summary']='Investigate a detected cost anomaly, quantify contributing dimensions, and evaluate the available evidence for an operational explanation.'
        if e['platform']=='devops' and any(s in e['sections'] for s in ('D-03','D-05','D-07')):e['sections']=list(dict.fromkeys(e['sections']+['D-12']))
        if e['platform']=='security' and e['id'] in ('S-UC07','S-UC08','S-UC10','S-UC11','S-UC14','S-UC15','S-UC16'):e['sections']=list(dict.fromkeys(e['sections']+['S-09','S-M07']))
        if e['platform']=='finops' and any(s in e['sections'] for s in ('F-M01','F-05')):e['sections']=list(dict.fromkeys(e['sections']+['F-08']))
    catalog['revision']='2026-10-22-narrative-guides'
    catalog['group_introductions']=GROUPS
    catalog['description']='Operational use cases for AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent. Read each workflow as a situation, an evidence-gathering process, and an outcome to interpret. The linked guides explain the underlying capabilities and mechanisms.'
    path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    Path(__file__).unlink()
if __name__=='__main__':apply()
