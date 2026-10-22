"""One-time reviewed source input; merged into the maintained mechanism registry."""
BASE='https://docs.aws.amazon.com/finops-agent/latest/userguide/'
SOURCES={
'FS401':(BASE+'what-is.html','Source-service responsibilities for observed cost, forecasts, coverage and recommendations'),
'FS402':(BASE+'context-files-and-memory.html','Uploaded files, conversational memory and automatic compaction'),
'FS403':(BASE+'data-protection.html','Session runtime, instance isolation and object-specific removal'),
'FS404':(BASE+'task-management.html','Explicit task requests, shared queue, schedules and event tasks'),
'FS405':(BASE+'automated-anomaly-response.html','Monitor event, managed-rule permissions, automation and destination setup'),
'FS406':(BASE+'custom-cost-reporting.html','Source query to report artifact and follow-up revision'),
'FS407':(BASE+'agent-guardrail-control.html','Action/invocation-specific approval and analytical boundaries'),
'FS408':(BASE+'jira-integration.html','Account registration, project connections and supported Jira operations'),
'FS409':(BASE+'slack-integration.html','Workspace registration, channel binding, membership and one-way publication'),
}
DETAILS={}
def add(id,section,kind,inputs,narrative,setup,lifecycle,controls,output,unknown,test,claims):
    DETAILS[id]={'primary_section':section,'kind':kind,'inputs':inputs,'narrative':narrative,'configuration':setup,'lifecycle':lifecycle,'controls':controls,'observable_output':output,'undocumented':unknown,'test':test,'claims':[{'source':s,'section':h,'assertion':a} for s,h,a in claims]}

add('MX-F-QUERY','F-M01','Source-backed analytical workflow',
'Question, dates, cost metric, scope, dimensions, currency and permissions to the relevant source service.',
['The agent queries the service that owns the requested evidence. Historical cost, forecasts, commitment coverage, anomaly records, optimization recommendations and change events are different inputs. Combining them in one conversation does not turn projected savings into observed spend.',
'The analytical result must preserve the query basis. First reconcile amounts, then examine operational evidence for an explanation. A nearby change event is a lead; numerical contribution and causal attribution remain different claims.'],
[['Source','Enable required upstream services and inspect the agent data role.','Permitted source evidence'],['Query','State complete periods, metric, filters and grouping.','Explicit analytical basis'],['Interpretation','Identify which source supplied a forecast, anomaly or recommendation.','Provenance of the returned value']],
[['Question submitted','Query upstream service','Source result or access failure returned.'],['Scope changed','Run a new query','New result is not comparable unless the basis is reconciled.'],['Recommendation retrieved','Contextualize for owner review','No infrastructure change is authorized by retrieval.']],
'The service summarizes recommendations from optimization services; it does not independently calculate its own underlying optimization analysis.',
'Returned figures, query basis and source/tool evidence.',
'Complete inference logic, causal accuracy and guaranteed agreement with differently scoped console queries are not established.',
['Use the supplied synthetic cost fixture or a harmless read-only account query.','Reconcile components to the total under identical periods and metric.','Change metric or period deliberately; identify why the totals are not comparable.'],
[('FS401','Related services','Cost Explorer, anomaly detection, optimization services and CloudTrail supply distinct evidence.'),('FS407','Generative AI accuracy considerations','Recommendations are upstream analysis; anomaly causality remains investigative.')])

add('MX-F-FILES','F-M02','Reference-file loading mechanism',
'Approved non-sensitive organization mapping or report convention in a supported active file.',
['Uploaded context is maintained outside the conversation. The agent can read the file but cannot rewrite or delete it by conversational instruction. A request to forget a preference therefore does not modify a conflicting account-owner mapping in an uploaded file.',
'Soft deletion removes a file from active context and Restore makes it active again. This is a documented reversible lifecycle for files, not a claim that every other retained object supports restoration.'],
[['Upload','Context files workspace: upload TXT, CSV, JSON, Markdown, HTML or YAML within documented size limits.','Instance-visible reference'],['Maintain','Update the governed source and intentionally replace the active uploaded representation.','Team-managed content'],['Deactivate/restore','Delete soft-deletes; Restore reactivates.','File availability']],
[['Active file','Delete','Soft-deleted; removed from active context.'],['Soft-deleted file','Restore','Available again.'],['Similar fact retained in memory','Edit file','Memory is a separate representation and may need separate correction.']],
'Files are visible to users with access to the agent. Do not upload credentials or sensitive personal information.',
'File state and correct application of a known identifier mapping.',
'File-versus-memory precedence and exact internal retrieval ranking are not specified.',
['Upload a harmless mapping for a fictitious account label.','Ask a question requiring that mapping and inspect attribution.','Soft-delete it and test again; restoring the file is distinct from remembering a new preference.'],
[('FS402','Supported file types; Manage context files','Files are agent-read-only, size-limited and support soft deletion/restoration.'),('FS403','Managing your data','File removal and other object lifecycles differ.')])

add('MX-F-MEMORY','F-M03','Cross-session retained-context mechanism',
'Preference or correction supplied through conversation; instance-local persistent memory.',
['Conversational memory retains preferences and corrections for later work in the same instance. It is not the current conversation transcript and is not an uploaded file. An explicit remember, update or forget instruction targets this retained representation.',
'Test it across sessions rather than immediately repeating the fact in the same conversation. Also inspect whether an active reference file supplies the same information; otherwise successful file use can be mistaken for memory recall.'],
[['Write/update','Ask the agent to remember or update one non-sensitive preference.','Persistent conversational context'],['Remove','Ask it to forget the specific retained fact.','Memory update, not history deletion'],['Verify','Use a later session without restating the test fact.','Cross-session behavior']],
[['Preference supplied','Remember/update','Retained context can influence later work.'],['Preference retained','Forget','Memory is updated in place.'],['Session ends','Start later session','Persistent instance data is separate from ephemeral runtime.']],
'Each instance isolates its retained content; no shared organization-wide memory is inferred.',
'Observed later use of a controlled fact, qualified when no direct memory-inspection evidence is exposed.',
'Internal schema, selection precedence and complete deletion of historical conversation occurrences are not established by a forget request.',
['Use a fictitious reporting preference absent from uploaded files.','Test a later session, then change the preference and test again.','Forget it; do not claim that earlier reports or conversation history were erased.'],
[('FS402','Agent memory across sessions','Remember, update and forget govern retained preferences/corrections.'),('FS403','Data isolation; Managing your data','Instance isolation and memory updates differ from conversation retention.')])

add('MX-F-COMPACT','F-M04','Session-context compaction mechanism',
'Growing conversation approaching the model context window.',
['Compaction changes the context supplied to continued conversation. Older material is summarized while recent messages remain in full. It preserves a working representation of key decisions, not a verbatim copy of every earlier turn.',
'Keep a material cost question explicit after a long exchange: period, metric, filters and unresolved assumptions. Restating those choices is an engineering safeguard, not a control that changes the undocumented compaction algorithm.'],
[['Enablement','Automatic; no administrator threshold or manual compaction switch is established by the cited guide.','Service-managed context handling'],['Operational practice','Restate critical query constraints and reference authoritative outputs.','Team verification procedure']],
[['Context grows','Approaches context limit','Older portions summarized.'],['Compacted context','Conversation continues','Recent messages and summary guide subsequent work.'],['Detail missing','Reconstruct from authoritative record','Do not infer verbatim recall from a fluent answer.']],
'Compaction is not durable preference management or deletion of stored conversation history.',
'Continued conversation and the constraints it actually applies; a direct compaction event may not be exposed.',
'Thresholds, summary-selection rules and lossless retention are not documented.',
['Use a non-sensitive long conversation with a recorded query contract.','Check whether later analysis retains the period and metric.','Where detail is missing, restore it explicitly and label compaction itself unobserved if no service signal exists.'],
[('FS402','Long conversation handling','Automatic summarization replaces older context while recent messages remain in full.')])

add('MX-F-TASK','F-03','Explicit request-to-task mechanism',
'Explicit task request or automation invocation, prompt and permitted data/context.',
['An ordinary question can be answered in the conversation. A task is created when explicitly requested or through an automation. The task has its own queue position, execution and output, so a chat acknowledgement is not completion evidence.',
'All documented task types share a queue. Inspect whether work was never created, remains queued, failed during analysis or completed but failed to publish. Those failures require different actions.'],
[['Create','Ask explicitly to create a task, or Tasks → Create tasks.','Separate execution record'],['Observe','Inspect Tasks/history and actual tool results.','Work status and evidence'],['Stop','Use supported cancellation for current work; control recurring automation separately.','Execution versus definition']],
[['Task requested','Create record','Work enters the shared queue.'],['Queued work','Execute','Tool results and output accumulate.'],['Task cancelled','Inspect retained record','Cancellation does not delete task history.']],
'Cancelling work is not rollback of prior external publication.',
'Task identity, execution status, source calls, outputs and separate delivery outcome.',
'Queue order, fairness, exactly-once processing and guaranteed cancellation of every in-flight action are not specified.',
['Create a harmless report task with an explicit date range.','Trace its identity from request to resulting output.','Cancel controlled work and distinguish preserved history from a deleted task.'],
[('FS404','On-demand tasks','Tasks are explicit and run through a shared queue rather than blocking the conversation.'),('FS403','Managing your data','Cancellation and record removal are different lifecycle operations.')])

add('MX-F-SCHEDULE','F-03','Automation-to-task mechanism',
'Recurring prompt, explicit schedule and timezone, observation-window rule and optional destination.',
['A recurring request creates an automation. Each eligible occurrence creates separate work; the automation is not the historical report. Keep the schedule and reporting basis distinct so a delayed task still queries the intended complete period.',
'Disabling an automation controls future starts. Existing tasks and distributed artifacts retain their own lifecycle. When replacing recurring work, inspect old automations to avoid running both definitions unintentionally.'],
[['Create','Describe the recurring work and schedule in conversation.','Saved automation'],['Inspect','Open Automations and confirm the actual saved schedule and prompt.','Configuration confirmation'],['Disable/delete','Stop future occurrences through the automation control.','Not cancellation/deletion of prior tasks']],
[['Automation active','Scheduled occurrence','A new task is created.'],['Automation active','Disable','Future starts stop.'],['Automation deleted','Inspect existing tasks/artifacts','Historical work remains independently retained.']],
'Unattended publication has destination-specific authorization; recurrence is not a universal approval bypass for unrelated actions.',
'Automation configuration and individual task histories with their queried periods.',
'Exact missed-run and timezone-resolution behavior must be inspected; the guide does not establish a universal timing SLA.',
['Create a non-sensitive recurring report only after an on-demand trial.','Inspect saved timing and the first task observation window.','Disable the automation and confirm future creation stops without assuming prior artifacts disappear.'],
[('FS404','Scheduled tasks','Schedules create automations and new tasks; disabling/deleting stops recurring work.'),('FS403','Managing your data','Automations and task records have distinct lifecycles.')])

add('MX-F-EVENT','F-M05','Anomaly-event matching mechanism',
'Cost Anomaly Detection monitor, required managed EventBridge permissions, condition, response prompt and optional destination.',
['The event path begins in Cost Anomaly Detection. The service creates a managed rule, matches the configured condition and creates a task using the saved prompt. Analysis and delivery occur after task creation; they are not evidence that matching itself was correct.',
'Trace the chain one object at a time. A monitor event with no task points toward rule or condition configuration. A completed analysis with no message points toward destination publication. Changing the analytical prompt does not repair an absent event subscription.'],
[['Prerequisites','Configure a monitor and the agent-role EventBridge permissions.','Event source and managed-rule authority'],['Automation','Describe monitor/scope, threshold and desired response in Chat.','COST_ANOMALY trigger and prompt'],['Verification','Inspect automation status, last-triggered information, created task and destination result.','End-to-end observation']],
[['Matching event arrives','Automation matches','Task created in the queue.'],['Task completes','Optional publication','Delivery has its own outcome.'],['Automation disabled/deleted','Future event arrives','No future task from that automation; old records remain.']],
'The documented preview event source is Cost Anomaly Detection, not arbitrary events. External publication requires its configured destination.',
'Monitor/event identity, automation, task, source analysis and any actual message.',
'Event deduplication keys, ordering and universal delivery/retry guarantees are not established.',
['Use a controlled event fixture for tabletop tracing; do not manufacture production spend.','Verify all chain identities against available service records during an authorized test.','A missing message must be localized to absent task, failed analysis or failed delivery rather than reported as one undifferentiated error.'],
[('FS405','Prerequisites; Verify and manage the automation','Monitor, managed-rule permissions and saved condition create a traceable automation/task path.'),('FS404','Event-based tasks','The supported preview trigger is a cost-anomaly event.')])

add('MX-F-ARTIFACT','F-04','Analysis-to-artifact mechanism',
'Reviewed cost query/results, report instructions, output format and optional sample template.',
['Report generation retrieves source data, builds the requested presentation and returns an artifact. A visual quality pass concerns presentation defects; it is not an independent reconciliation of the underlying financial interpretation.',
'A follow-up can revise the artifact. Keep the analytical basis explicit when revising it: changing a title or chart layout should not silently change period, cost metric or grouping.'],
[['Request','Specify report audience, source period, metric, required sections and supported format; default is HTML.','Artifact instruction'],['Inspect','Open/download from Artifacts and compare figures to source results.','Output review'],['Revise','Reference the existing report in a follow-up and state whether the query basis may change.','Revision intent']],
[['Analysis available','Generate report','Artifact delivered.'],['Artifact exists','Request revision','Updated presentation can be produced.'],['Service artifact removed','External copies remain','Downloaded or published copies require separate handling.']],
'Formatting and completion status do not establish numerical accuracy; distribution is a separate effect.',
'Reportable artifact tied by the team to task/query identity and reviewed scope.',
'An immutable artifact-version API and universal external-copy deletion are not established by the report guide.',
['Generate a report from the small supplied synthetic cost fixture.','Reconcile displayed components and totals to the fixture.','Revise layout only and verify that period, metric and numbers did not change.'],
[('FS406','Generating cost reports','Reports are artifacts, default to HTML and can be revised through follow-up.'),('FS403','Managing your data','Artifacts and other retained objects have distinct controls.')])

add('MX-F-JIRA','F-M06','Invocation-dependent publication mechanism',
'Account Jira registration, per-instance project connection, supported action, payload and invocation mode.',
['Jira approval depends on how the action starts. Chat and on-demand tasks present issue/comment details for confirmation; a scheduled or event automation uses authorization established during setup. The same destination does not imply the same per-run approval behavior.',
'After approval or preauthorization, inspect the actual external record. A successful analysis is not a successful issue creation, and a retry after an uncertain response can create duplicates unless the operator checks the existing project records.'],
[['Connect','Authorize the Jira Cloud integration, then bind the approved project to this instance.','Project scope'],['Interactive action','Review project, issue/comment body and target shown for approval.','Per-action decision'],['Automation action','Review action and audience before enabling recurrence/event handling.','Setup-time authorization']],
[['Interactive request','Confirm/revise action','Supported publication can execute.'],['Automation configured','Matching invocation','Publication executes without a per-run approval prompt.'],['Publication uncertain','Inspect destination before retry','Avoid assuming an unobserved response means no issue exists.']],
'Supported actions do not include arbitrary issue-field changes, deletion or Jira workflow management.',
'Actual issue/comment, intended project and task action history.',
'Exactly-once external publication and automatic duplicate suppression are not documented.',
['Use a restricted Jira Cloud test project and non-sensitive payload.','Compare interactive approval with a separately reviewed automation test.','Deny project access and verify a publication failure does not erase or falsely complete the analysis record.'],
[('FS407','Jira issue creation and comment addition','Approval differs between interactive/on-demand and automated invocation.'),('FS408','Integration model; Capabilities','Project connections and supported actions limit the effect.')])

add('MX-F-SLACK','F-M06','One-way destination-publication mechanism',
'Account workspace registration, instance channel connection, app membership and reviewed message/artifact.',
['Slack publication is one-way in the documented preview. Registration authorizes the workspace; the instance connection selects a channel; channel membership permits delivery. Posting does not establish channel reading, command handling or thread interaction.',
'There is no per-message approval prompt, including interactive requests. Review the intended channel and content before invocation, then inspect actual delivery. Disconnecting the channel is not a mechanism for deleting previously posted messages.'],
[['Register','Authorize the workspace integration.','Account-level registration'],['Connect','Add the app to the channel; instance → Add connection → Slack; select integration and channel ID.','Instance-specific destination'],['Publish','Use the reviewed destination and verify the resulting post.','External effect']],
[['Connection active','Post requested','Message may be sent without an approval prompt.'],['App absent from channel','Post attempted','Delivery fails despite registration.'],['Connection removed','Future request','Future access changes; existing posts remain externally managed.']],
'Review audience before sending. The integration does not provide general edit/delete, channel administration or conversation reading.',
'Actual channel post and recorded action/delivery result.',
'Deduplicated retries, universal rollback and guaranteed post deletion are not provided by the documented interface.',
['Use a restricted test channel containing the installed app.','Verify destination and content without expecting a confirmation prompt.','Remove app membership for an authorized negative test and distinguish delivery failure from task failure.'],
[('FS409','Integration and connection model; Capabilities','Connections are per-instance/channel and one-way; membership is required.'),('FS407','Slack messages','Posting does not prompt for approval even in interactive invocation.')])
