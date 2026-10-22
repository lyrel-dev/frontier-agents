"""Curated presentation outlines. References resolve to canonical guide sections."""
def slide(title, minutes, refs, kind, data, message):
    return dict(title=title, seconds=int(minutes*60), refs=refs.split(), kind=kind, data=data, message=message)
def deck(title, subtitle, prefix, slides):
    return dict(title=title, subtitle=subtitle, prefix=prefix, slides=slides)
DECKS = {
'devops': deck('AWS DevOps Agent', 'Resources, context and controlled execution', 'D', [
slide('An Agent Space connects configuration to executions',2,'D-01','flow',[
['Account registrations','Providers and AWS account access'],['Agent Space','Associations, selected tools and operator access'],['Agent definition','Managed behavior or custom prompt and attachments'],['Execution','Investigation, invocation and observable tool results']], 'Configuration, execution and evidence are different objects.'),
slide('Two access paths need separate verification',2,'D-02','table',[
['Path','Purpose','Acceptance check'],['Resource role','Read authorized AWS sources','Known resource and identity are correct'],['Operator role','Let people use the space','Intended user—not only administrator—can enter'],['Connected provider','Access selected external tools','Arguments and returned source agree']], 'A created workspace is not proof that its data sources are readable.'),
slide('MCP setup has authentication-specific decisions',3,'D-03','table',[
['Method','Required decisions'],['OAuth','Token/authorization endpoints, client and scopes'],['API key / secret headers','Actual header names and supported rotation path'],['SigV4','Signing Region, service and role option'],['Association','Select tools in the Agent Space; verify there']], 'Role-less SigV4 validation is deferred to association.'),
slide('Private routing and provider identity are separate',2,'D-04','flow',[
['Agent service','Uses configured private connection'],['Resource gateway','ENIs in selected VPC subnets'],['Endpoint route','DNS, host and allowed port ranges'],['Authenticated tool','Provider authentication and selected operation']], 'Check the gateway path and target port before rotating a valid secret.'),
slide('Topology is a representation, not an access boundary',2,'D-05','columns',[
['Discovery','CloudFormation resources and enabled Resource Explorer supply inventory.'],['Relationships','Configuration, tags, pipeline mapping and observability supply evidence.'],['Verification','Compare one service/repository edge with the deployed configuration.']], 'A missing graph node does not establish that a direct resource read is denied.'),
slide('Past incidents become selected contextual evidence',3,'D-M01','flow',[
['Investigations','Earlier outcomes and evidence'],['Learning process','Synthesizes monitor-specific knowledge'],['Memory store','Descriptions, entries, versions and active state'],['New investigation','Selects relevant context and checks current evidence']], 'Retention, retrieval and diagnostic correctness require separate observations.'),
slide('Corrections and access attachments solve different problems',2,'D-M02 D-M07','columns',[
['Correct a diagnosis','Submit verified feedback; inspect the resulting lesson. AWS sharing is a separate choice.'],['Attach context','New custom agents start without stores. Attach only required stores; managed stores are read-only to them.']], 'Feedback changes contextual knowledge; attachment changes which context an agent may use.'),
slide('Instructions and skills enter the session differently',2,'D-M03 D-M04','table',[
['Control','Loading behavior','Configuration test'],['Instructions','Applicable text at session startup','Compare an existing and new session'],['Skill','Procedure selected by description and scope','Compare a matching and nonmatching request'],['Permissions','Enforced by the connected systems','Test an expected denial separately']], 'Prompt guidance does not grant or revoke IAM permissions.'),
slide('Inspect triage before diagnosing a missing investigation',2,'D-06','table',[
['Decision','Meaning','Operator response'],['Linked','Signal belongs to existing work','Inspect the primary investigation; unlink if wrong'],['Skipped','Configured criteria excluded it','Inspect rule/skill; unskip if wrong'],['Proceed','Independent work is scheduled','Inspect execution and evidence']], 'Routing correction and root-cause feedback are different operations.'),
slide('A trigger creates work; cancellation affects a run',2,'D-07','flow',[
['Definition','Prompt, selected tools, skills and stores'],['Trigger','Manual, rate or cron; inspect next run'],['Invocation','History shows status and tool trajectory'],['Stop controls','Pause future starts; cancel existing work separately']], 'In-flight calls may finish after cancellation; a schedule is not the data window.'),
slide('Sandbox and directed actions have different boundaries',3,'D-M05 D-M06','columns',[
['Sandbox','Fresh investigation-local environment; configured packages and outbound rules. Empty allowlist still permits AWS endpoints.'],['Directed actions','Space opt-in, eligible access and specific operation/resource approval. Inspect classification and final state.']], 'Application or tool effects must be reviewed; “read-only” is not a universal agent label.'),
slide('Update semantics are part of the operational contract',2,'D-08 D-M06','table',[
['Object','Update behavior','Avoid'],['Asset metadata','PATCH semantics','Assuming names can replace required asset IDs'],['Space preferences map','Replacement when supplied','Dropping existing values unintentionally'],['Memory entry','New immutable version','Treating edits as erased history']], 'Read current configuration first, then verify the saved result.'),
slide('Exercise: same alarm, different evidence',8,'D-U01 D-M01 D-M02','demo',[
['0–2 min','Inspect historical memory','Earlier database pool saturation'],['2–4 min','Compare new fixture','DB 34/100 connections; query p95 18 ms'],['4–6 min','Evaluate current lead','Inventory p95 2,900 ms; checkout 3,100 ms'],['6–8 min','Record the boundary','Upstream lead supported; internal cause unresolved']], 'Synthetic prepared-result exercise. Do not claim observed AWS recall or a proven deployment cause.'),
slide('Diagnose the failing layer, then retest',2,'D-10 D-11','columns',[
['Access and connectivity','Check operator identity, source role, provider association, route and endpoint port.'],['Context and execution','Check activation, descriptions, attachments, session start and concurrency.'],['Changes and coverage','Check exact approval and update semantics; consult current quotas and feature eligibility.']], 'Full remote-protocol and release-profile procedures remain linked scope, not completed live tests.')
]),
'security': deck('AWS Security Agent', 'Assessment resources, authentication and evidence lineage', 'S', [
slide('Application resources sit beneath shared account configuration',2,'S-01','flow',[
['Account resources','Integrations, identity and requirement packs'],['Agent Space','Application sources, users and settings'],['Configuration','Target, authentication, criteria and limits'],['Run and evidence','Assessment results and linked verification']], 'Requirements and integrations can have broader scope than a single application.'),
slide('Registration is not repository connection',2,'S-02','table',[
['Action','Establishes','Inspect'],['Register integration','Available source provider','Account type and authorization'],['Connect repository','Application source selection','Repository and branch identity'],['Enable feature','Selected assessment behavior','Modes, comments and remediation settings'],['Open as operator','Usable assessment access','Intended user rather than setup administrator']], 'Verify the deployed revision separately from the latest source branch.'),
slide('Network rules separate targets, dependencies and exclusions',2,'S-03','table',[
['Rule','Permitted purpose','Example'],['Target','Access and testing','Authorized staging application'],['Accessible','Supporting access; not attack target','Approved login dependency'],['Out of scope','No access; exclusion precedence','Production callback or payment path']], 'A verified domain is not authorization for every downstream effect.'),
slide('Obtaining a credential is not logging into the application',3,'S-M01','flow',[
['Credential source','Direct input, secret, role or Lambda'],['Service access','Required trust and read/invoke permissions'],['Login instructions','How credentials and MFA apply'],['Authenticated role','Observed identity and protected routes']], 'Save & Test verifies the configured flow; inspect where authentication fails.'),
slide('Learned login navigation is a specific reuse mechanism',2,'S-M02','flow',[
['First successful login','Navigation is discovered'],['Saved skill','Successful procedure is retained'],['Later session','Procedure can be reused'],['Setting / flow change','Toggle reuse; verify actual identity again']], 'Login Optimization is not a universal vulnerability-memory service.'),
slide('A reusable configuration produces distinct executions',2,'S-04','table',[
['Object','Meaning'],['Draft','Incomplete configuration, not a completed test'],['Saved configuration','Reusable target, credentials and execution choices'],['Run','Assessment against then-current target/configuration'],['Task-hour limit','Cumulative task work, not elapsed wall time']], 'A completed status does not establish exhaustive coverage.'),
slide('Requirement evaluation starts with applicability',2,'S-M03','columns',[
['Applicable and compliant','The required ownership check exists and supporting evidence is present.'],['Applicable and violating','A handler returns account-owned data without the required authorization.'],['Inapplicable','The requirement does not govern the evaluated component.']], 'Configure requirement evaluation explicitly; vulnerability analysis alone is different.'),
slide('Regeneration replaces requirements; it does not append',2,'S-M04','flow',[
['Source policy','Reviewed governing documents'],['Generate','Replace the pack contents'],['Review','Inspect generated and formerly manual rules'],['Enable','Use the reviewed replacement in later assessments']], 'Keep authoritative requirement source in Git and review replacement before enabling.'),
slide('A proposed repair is not a deployed repair',2,'S-05','flow',[
['Finding','Evidence and affected revision'],['Proposed change','Provider-specific patch or pull request'],['Engineering review','Tests and approval'],['Deployment','Known revision on the authorized target']], 'Use the finding ID to connect the records, not similarity of titles.'),
slide('Revalidation preserves the original finding',2,'S-M05','flow',[
['Selected finding','Original completed assessment'],['New job','Current credentials; repeat selected steps'],['Result','Reproduced or not reproduced'],['History','Original finding linked to new evidence']], 'A non-reproduction result is scoped; failed authentication can invalidate its interpretation.'),
slide('Earlier assessments use different resource lifecycles',2,'S-06','table',[
['Assessment','Configuration model','Result focus'],['Code','Full scan or supported change trigger','Locations, evidence and suggested fixes'],['Design','One-off review; clone for new work','Design findings against requirements'],['Threat model','Reusable configuration and runs','System boundary, flows and threats']], 'Review inferred system context before relying on individual findings.'),
slide('Encryption requires the correct identity and context',2,'S-M06','flow',[
['Customer KMS key','Protects resource branch keys'],['Branch key','Service-managed stored key material'],['Derived wrapping key','Protects data-encryption keys'],['Authorized request','Caller, action and encryption context must match']], 'Administrator, web-app role, assessment role and asynchronous service access are distinct.'),
slide('Exercise: verify the repaired account boundary',8,'S-U01 S-M05','demo',[
['0–2 min','Inspect the finding','User A received account B’s test invoice in demo-r1'],['2–4 min','Inspect the change','Ownership check reviewed; demo-r2 deployed'],['4–6 min','Inspect revalidation','Actual user A role and selected path reached'],['6–8 min','State the result scope','Prepared denial supports that path, not whole-app security']], 'Synthetic staging evidence only. No live penetration test or exploit execution.'),
slide('Troubleshooting follows the failed prerequisite',2,'S-07 S-08','columns',[
['Access','Separate repository connection, secret retrieval, application login and private routing.'],['Criteria','Check pack activation, applicability, regeneration and evaluation mode.'],['Evidence','Check deployment, actual identity, reachable path and linked job before closing a finding.']], 'Full provider/pipeline and GenAI exception setup remains explicitly linked coverage.')
]),
'finops': deck('AWS FinOps Agent', 'Source queries, retained context, tasks and publication', 'F', [
slide('Instance configuration and task execution are separate',2,'F-01','flow',[
['Access','Agent data role and operator entry'],['Context','Uploaded files, memory and conversation'],['Work','Automation or request creates a queued task'],['Output','Answer, artifact or configured external action']], 'Preview service; storage and inference geography must be reviewed separately.'),
slide('Four permission responsibilities are not one role',3,'F-02','table',[
['Responsibility','Purpose'],['Administrator','Create/configure service resources and permitted roles'],['Agent data role','Call authorized data services and manage required rules'],['Operator role','Supported web-app operations'],['User permission','Enter the configured agent as the intended person']], 'Test data access and team access independently.'),
slide('Numerical contribution and cause are different conclusions',2,'F-M01','table',[
['Source','What it can support'],['Cost query','Amount for fixed dates, metric and dimensions'],['Anomaly record','Detected deviation under the monitor'],['Recommendation','Upstream candidate and assumptions'],['Change event','Recorded operation at a time']], 'A nearby deployment alone does not explain the entire cost delta.'),
slide('Files are reviewed reference inputs',2,'F-M02','columns',[
['Preparation','Use actual account identifiers, owners and reporting basis. Keep the maintained source in Git.'],['Controls','Upload/soft-delete/restore in the workspace. The agent reads but does not conversationally rewrite the file.'],['Limits','Supported formats, 10 MB per file and total context quota matter.']], 'Everyone with access to the agent can see its context files.'),
slide('Memory and file retrieval need different tests',2,'F-M03','flow',[
['Remember','State a harmless preference'],['New session','Observe its application'],['Correct / forget','Change the retained memory'],['Retest','Check separately from uploaded source files']], 'Updating memory does not establish that a reference file changed.'),
slide('Compaction summarizes a conversation, not all persistent state',1,'F-M04','columns',[
['What changes','Older messages are summarized as the conversation context fills. Recent messages remain in full.'],['How to review','Restate the current cost contract and unresolved questions before another material calculation.']], 'Do not infer verbatim retention or a documented hidden precedence algorithm.'),
slide('A task runs; an automation creates future tasks',2,'F-03','flow',[
['Definition','Schedule or supported event condition'],['Task creation','A separate execution record'],['Shared queue','On-demand and automated work'],['Result','Status, source evidence and artifacts']], 'Removing an automation does not delete existing tasks or messages.'),
slide('Trace an anomaly through the complete event path',2,'F-M05','flow',[
['Monitor','Cost Anomaly Detection'],['Managed rule','EventBridge condition and permissions'],['Automation','COST_ANOMALY trigger creates task'],['Execution','Inspect result and destination separately']], 'No task and no delivered message are different failures.'),
slide('Integration registration precedes destination binding',2,'F-05','table',[
['Layer','Jira','Slack'],['Registration','Supported Cloud authorization','Workspace authorization'],['Agent connection','Selected project/space','Channel; app membership required'],['Boundary','No arbitrary workflow editing','One-way posting, not channel reading']], 'Inspect connection state and the actual destination.'),
slide('Approval rules depend on effect and invocation',2,'F-M06','table',[
['Effect','Interactive / on-demand','Automation'],['Jira issue or comment','Approval prompt','Pre-authorized during setup'],['Slack post','No approval prompt','No approval prompt']], 'Schedule setup can authorize publication; review content and audience at that point.'),
slide('Stop and delete mean different things for different objects',2,'F-M07 F-04','table',[
['Object','Control','What may remain'],['Context file','Soft delete / restore','Retained file content'],['Task','Cancel execution','Task record'],['Automation','Disable/delete future starts','Existing tasks'],['Artifact','Delete artifact','External published copies']], 'Whole-agent deletion is not an ordinary lifecycle demonstration.'),
slide('Exercise: reconcile the 41% increase before explaining it',8,'F-U01','demo',[
['0–2 min','Check comparison contract','Two complete windows, same scope and cost basis'],['2–4 min','Reconcile component totals','1,400 → 1,974; delta 574'],['4–6 min','Attribute arithmetic','Storage +200; requests +100; transfer +274'],['6–8 min','Evaluate prepared evidence','Extra export supports transfer only; other causes unresolved']], 'Synthetic quantities and rates—not AWS prices or a measured saving.'),
slide('Validate each layer rather than one fluent answer',2,'F-06 F-07','columns',[
['Data','Reproduce totals with identical metric, dates, filters and units.'],['State and execution','Test file retrieval, memory, event matching and queue status separately.'],['Effects','Inspect destination, approval path and retained records after a stop operation.']], 'Complete current policies and quotas remain the authoritative linked reference.')
]),
'architecture': deck('Shared architecture', 'Compare mechanisms without inventing a common runtime', 'A', [
slide('The three services expose different resource models',2,'A-01','table',[
['Layer','DevOps','Security','FinOps'],['Scope','Agent Space','Application + shared resources','Agent instance'],['Configuration','Agents, tools, knowledge','Assessment definitions','Context, automations, connections'],['Execution','Investigation / invocation','Run / revalidation job','Conversation / task']], 'Use platform-specific identifiers rather than a universal ambiguous agent ID.'),
slide('Retained context has different producers and lifecycles',2,'A-02','table',[
['Material','Producer','Consumer'],['Monitor knowledge','Managed investigation learning','Relevant later investigation'],['Login skill','Successful authentication navigation','Later login'],['Reference file','Operator upload','Agent task or conversation'],['Conversational memory','Preferences/corrections','Later session']], 'Do not reduce these to one “learning enabled” setting.'),
slide('Connectivity is not authorization',2,'A-03','flow',[
['Route','Can the endpoint be reached?'],['Identity','Who authenticated?'],['Permission','Which operation is allowed?'],['Behavior','What does prompt guidance request?']], 'Test each layer with observed results and an expected denial.'),
slide('The effect determines the relevant approval boundary',2,'A-04','table',[
['Effect','Control to inspect'],['Resource mutation','Specific directed-action authorization'],['Application testing','Targets, credentials, exclusions and permitted effects'],['Source change','Repository review and deployment controls'],['External publication','Destination and invocation-specific approval']], 'No universal “read-only” or “human-approved” label is sufficient.'),
slide('Configuration, runs and artifacts have separate lifecycles',2,'A-05','columns',[
['Future work','Pause a schedule or disable an automation.'],['Current work','Cancel the invocation/task using its supported control.'],['Retained evidence','Manage versions, findings, files and artifacts according to their own semantics.']], 'Stopping future starts does not reverse completed effects.'),
slide('A handoff transfers evidence—not credentials or authority',2,'A-06','flow',[
['Origin','Platform, configuration and execution IDs'],['Subject','Service, revision and UTC observation window'],['Request','Owner, question and permitted effect'],['Acceptance','Required evidence and unresolved questions']], 'The receiving team obtains its own access and makes its own authorization decision.'),
slide('Keep implementation unknowns visible',2,'A-07','columns',[
['Documented','Resource relationships, selected controls, retention and execution behavior.'],['Not established','Shared vector database, retrieval-ranking algorithm, cross-agent runtime or model-training pipeline.']], 'An attractive diagram is not evidence of undocumented internals.'),
slide('Tabletop: three observations, three evidence obligations',4,'A-U01','demo',[
['0–1 min','Identify the required inputs','Latency evidence, authorization identity and cost basis'],['1–3 min','Check consistency','Same intended revision, target and comparable windows'],['3–4 min','Assign unresolved questions','Do not invent a single shared root cause']], 'Synthetic comparison; no shared runtime or live execution assumed.'),
slide('Accept documents on operating usefulness',2,'A-07','columns',[
['Model','Resources and scope are clear before a scenario begins.'],['Procedure','Inputs, choices, confirmation and failure paths are described.'],['Evidence','Claims have sources; examples and live outcomes are not conflated.']], 'Link and layout checks are necessary but do not prove technical completeness.')
])}
