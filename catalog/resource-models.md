# Product resource models

Logical documentation model, not an AWS database schema, SDK payload or shared runtime. Green means AWS defines the concept; it does not mean every green item has an independent ARN, CRUD API or equal availability. Relationship multiplicities are qualified individually and are not service quotas.

The color classifies the definition of a concept, not who authors its content, pays for it or approves its use. IAM roles and EventBridge rules are AWS-defined dependencies outside the agent service.

Each relationship records targets per source and sources per target. 0..* means optional repeated association, not unlimited quota; ? means that exact multiplicity is not established by the reviewed guidance.

## AWS DevOps Agent

| Entity | Ownership / kind | Identity and scope | Meaning |
|---|---|---|---|
| Agent Space | aws / service resource | agentSpaceId; Agent Space ARN; Account and Region | Operational container for account access, integration associations, knowledge and executions. |
| Provider registration | aws / service configuration | serviceId in the association API; Account registration | Registered provider endpoint and authorization; registration alone does not select a space's tools. |
| Service association | aws / API resource | associationId, agentSpaceId, serviceId; One Agent Space | Provider-specific configuration selecting the service resources or tools usable in that space. |
| Selected tool | aws / configuration member | Tool identifier within its configured provider; Association and custom definition | An exposed operation selected for use; not an independently deployed tool resource. |
| Resource and operator IAM roles | aws / cross-service resource | IAM role ARN; Relevant AWS account | Separate roles govern service resource access and operator access; elevated action access is another role binding. |
| Custom-agent definition | aws / asset subtype | assetId; assetType custom_agent; One Agent Space | Stored prompt with selected tools, skill asset IDs and memory-store asset IDs; not an invocation. |
| Skill | aws / asset subtype | assetId; assetType skill; One Agent Space | Procedural instructions and references with applicability and agent-type scope. |
| Agent instructions | aws / asset subtype | assetId; assetType agents_md; Agent Space and agent type | Standing guidance loaded into new applicable work; content is not an IAM policy. |
| Memory store | aws / asset subtype | assetId; assetType memory_store; One Agent Space | Collection with a subject description; managed and custom stores have different write behavior. |
| Memory entry | aws / asset subtype | Memory asset identity within its store; One store | Synthesized informational content that can be selected and read for a task. |
| Memory content version | aws / version record | Memory identity plus displayed version; One memory entry | Immutable content revision; a version selector is not evidence of every possible restore or undelete operation. |
| Custom-agent trigger | aws / schedule configuration | Trigger shown on the custom-agent definition; One custom agent | Rate or cron schedule for future invocations; pausing it does not cancel existing work. |
| Custom-agent invocation | aws / execution record | Invocation selected in History; One custom agent | A particular execution with status, tool calls and outputs; its trajectory is execution detail. |
| Incident signal | aws / operational record | Signal linkage and displayed triage decision; One Agent Space | Incoming incident context can be linked, skipped or scheduled for independent investigation. |
| Investigation | aws / execution record | Investigation identifier and incident interval; One Agent Space | Evidence-gathering work and evolving incident conclusions; not the same record as a signal. |
| Investigation feedback | aws / operational record | Feedback associated with an investigation; Completed investigation | Operator verdict and verified correction. Do not assume a one-to-one mapping to every internal reflection entry. |
| Topology and environment understanding | aws / derived view | Space, selected view and applicable knowledge version; One Agent Space | Discovered and inferred relationships; not an independent access boundary or a complete authoritative inventory. |
| Prevention evaluation | aws / execution record | Evaluation shown in Improvements; One Agent Space | Analysis of investigation history for proposed improvements. |
| Prevention recommendation | aws / result record | Recommendation in the evaluation output; Agent Space | Proposed improvement with a review state, not an implemented resource change. |
| Directed-action approval | aws / authorization event | Approved operation, target and operator attribution; A particular requested action | Execution-time authorization separate from opt-in, role permissions and tool classification. |
| Chat conversation | aws / interaction record | Conversation in the space web app; One Agent Space | On-demand inquiry and supported configuration/action requests do not inherently require a custom-agent definition. |
| Release-readiness review | aws / preview execution | Review task and candidate source revision; Release management | Change analysis is distinct from active testing of a deployed application. |
| Release test profile | aws / asset subtype | assetId; assetType test_profile; One Agent Space | Reusable target and test-type configuration; not the documentation implementation profile. |
| Release test execution | aws / preview execution | Release Manager task or displayed test result; Authorized deployed target | Real requests and observed results; application data may change. |
| Telemetry or repository source | external / source system | Provider-native resource, revision and time range; External system of record | Original observations remain distinct from a copied summary or retained memory. |
| Deployed application | external / customer workload | Endpoint, deployed revision and test identity; Application owner authorization | The target receives requests; accepting a test profile is not blanket authorization. |
| Managed agent role | aws / platform-owned component | Agent type shown in Managed agents; One Agent Space | Platform-owned role; it is not a user-created custom_agent asset. Incident roles participate in investigations. Only Learning exposes its own run history and platform-owned triggers. |
| Learning execution | aws / execution record | Run selected in the Learning history; Managed Learning role | Observable synthesis and refresh execution; do not infer a separately runnable record for every managed incident role. |

### Relationships

| Source → relationship → target | Targets/source | Sources/target | Basis and qualification |
|---|---|---|---|
| Agent Space → contains → Service association | 0..* | 1 | documented. Association includes agentSpaceId. |
| Provider registration → is associated through → Service association | 0..* | 1 | documented. Do not assume unlimited associations. AssociateService replaces the existing association of the same service. |
| Service association → selects → Selected tool | 0..* | ? | documented. Provider-specific configuration; tools are members, not independently provisioned resources. |
| Agent Space → stores → Custom-agent definition | 0..* | 1 | documented. The custom definition is an asset in its space. |
| Custom-agent definition → selects subset → Selected tool | 0..* | ? | documented. Only assigned tools are available to the invocation. |
| Custom-agent definition → references asset IDs → Skill | 0..* | 0..* | documented. Existing skill assets in the same Agent Space; a name is not an asset ID. |
| Custom-agent definition → attaches asset IDs → Memory store | 0..* | 0..* | documented. Starts empty. Attached custom stores permit writes; managed stores are read-only to a custom agent. |
| Agent Space → scopes → Memory store | 0..* | 1 | documented. This is a space-local relationship, not organization-wide memory sharing. |
| Memory store → groups → Memory entry | 0..* | 1 | documented. Create the store before entries; content availability and selection remain distinct. |
| Memory entry → has content versions → Memory content version | 1..* | 1 | documented. Every update creates an immutable version. |
| Custom-agent definition → is executed as → Custom-agent invocation | 0..* | 1 | documented. Repeated runs are separate invocation records. |
| Custom-agent definition → has schedules → Custom-agent trigger | 0..* | 1 | documented. Trigger management belongs to the selected custom agent. |
| Custom-agent trigger → initiates → Custom-agent invocation | 0..* | 0..1 | logical. Optional origin because an invocation may be manual. This is not an asserted API foreign key. |
| Incident signal → links or starts → Investigation | 0..1 | 0..* | logical. Current routing view: skipped signals have no investigation, linked signals share one; manual investigations need no external signal. This is not immutable lifetime cardinality. |
| Investigation → receives correction → Investigation feedback | ? | 1 | documented. A feedback submission belongs to the investigation; feedback-to-memory entry counts are not specified. |
| Investigation → informs later synthesis → Memory entry | ? | ? | documented. A learning process mediates this relationship; the edge is not an immediate direct write or model retraining. |
| Prevention evaluation → produces → Prevention recommendation | 0..* | ? | documented. Evaluation and recommendation review are separate from implementation. |
| Agent Space → has derived views → Topology and environment understanding | ? | 1 | documented. View multiplicity is not an API inventory or authorization contract. |
| Selected tool → reads authorized evidence → Telemetry or repository source | ? | ? | logical. Actual provider operations and identity determine the readable scope. |
| Release test profile → supplies reusable configuration → Release test execution | 0..* | ? | documented. Profile-based execution is documented; do not require a saved profile for every supported initiation path. |
| Release test execution → sends real requests → Deployed application | ? | 0..* | documented. Application writes are distinct from directed AWS API actions. |
| Chat conversation → requests action authorization → Directed-action approval | 0..* | ? | documented. Approval applies to the operation and resource, not every subsequent message. |
| Directed-action approval → permits scoped use → Resource and operator IAM roles | ? | ? | documented. AWS-resource directed actions use the registered elevated role; permissions alone are not approval. |
| Agent Space → exposes managed roles → Managed agent role | ? | 1 | documented. Roles are platform-owned, not custom-agent definitions. |
| Managed agent role → Learning role has history → Learning execution | 0..* | 1 | documented. This edge applies to Learning only; other managed roles execute within investigations. |
| Learning execution → synthesizes retained context → Memory entry | ? | ? | documented. Completion and a resulting version must be inspected; this is not customer-controlled model training. |
## AWS Security Agent

| Entity | Ownership / kind | Identity and scope | Meaning |
|---|---|---|---|
| Shared service scope | aws / documented scope | Tenant/organization scope used in the guide; Shared Security Agent configuration | The documented shared layer; do not equate it with a new AWS Organizations resource or infer cross-account policy propagation. |
| Agent Space | aws / service resource | Application Agent Space identity; Application or project | Groups application sources, settings, assignments and assessments. |
| Integration registration | aws / service configuration | Registered provider/account connection; Shared integration setup | Authorization registered before particular sources are connected to an application. |
| Agent Space source connection | aws / configuration association | Space and selected source connection; One Agent Space | Selects a repository or documentation source; per-capability settings decide its use. |
| Repository or design source | external / source artifact | Provider identity and immutable revision; Source system | The original source can be reused across spaces without making every assessment identical. |
| Security requirement pack | aws / service configuration | Pack identity and enabled state; Shared requirements | Managed or custom collection governing subsequent eligible design and code reviews. |
| Security requirement | aws / configuration item | Requirement within a pack; One pack | Applicability and compliance criteria, not an assessment result or certification. |
| Penetration-test configuration | aws / service configuration | Saved penetration-test identity; One Agent Space | Reusable target, scope, authentication and execution settings. |
| Target and network rules | aws / configuration members | Rules within the selected test configuration; A penetration-test configuration | Target, supporting access and excluded paths have different permitted effects. |
| Test credential definition | aws / configuration item | Named credential in test configuration; A penetration-test configuration | Credential strategy and login instructions; obtaining a secret is distinct from authentication. |
| Retained login procedure | aws / managed procedural state | Procedure associated with the configured authentication flow; Login Optimization | Reuse of successful navigation; no independent editable skill-resource API is asserted. |
| Penetration-test run | aws / execution record | Run identity, target revision and observed credentials; One saved configuration | Independent execution against the target as it exists at run time. |
| Penetration-test finding | aws / result record | Original finding identifier; Original assessment run | Retains vulnerability evidence and identity through repair and repeated revalidation. |
| Revalidation job | aws / execution record | Job in run history with type Revalidation; Selected existing findings | Retests selected evidence; it neither replaces the original finding nor performs broad discovery. |
| Finding-to-revalidation result | documentation / normalized association | Our pair: original finding and revalidation job; Documentation evidence model | Captures the reported result for a selected finding. This is not asserted to be a separate AWS API resource. |
| Full-code review configuration | aws / service configuration | Selected source configuration and repository settings; One Agent Space | Reusable selection of repositories or S3 sources for full scans; repository-event review settings are modeled separately. |
| Code review | aws / execution record | Review and exact source revision; Full or change-focused assessment | A source assessment is not a running-application test. |
| Design review | aws / one-off assessment | Individual review identity; One Agent Space | Analyze submitted design material once; clone creates a new review rather than rerunning the same object. |
| Threat-model configuration | aws / service configuration | Saved threat-model identity; One Agent Space | Reusable source and scope selection with on-demand runs. |
| Threat-model run | aws / execution and result record | Run identity within a threat model; Selected source and scope documents | Produces a system overview and threats for that run; inferred boundaries need review. |
| Remediation attempt | aws / operation record | Finding-linked remediation state; Configured source repositories | Finding-linked attempt to produce a code proposal; it is not the repository settings or the resulting deployment. |
| Patch or pull request | external / change artifact | Diff or provider-native pull request and revision; Engineering delivery process | A proposal requires review, tests and deployment before a repair can be tested. |
| Deployed test application | external / customer workload | Endpoint, deployment revision and actual test role; Owner-authorized test boundary | Actual application state may differ from the repository branch or earlier run. |
| Jira integration and project connection | aws / service configuration | Selected integration and destination project; Configured finding publication | Destination authorization is separate from source access and assessment execution. |
| Jira issue | external / external work record | Jira issue key; Selected project and audience | External finding handoff; disconnecting an integration is not issue deletion. |
| Repository code-review settings | aws / service configuration | Settings on the connected repository; Agent Space source connection | Controls eligible change review, selected analysis modes and comments. These settings are not the full-scan configuration. |
| Remediation repository settings | aws / service configuration | Eligible source repositories and feature settings; Application Agent Space | Determines where supported fix proposals can be created. Settings alone do not represent a remediation attempt. |
| Code-review finding | aws / result record | Review identity, source revision and finding location; Source-code review | Static-analysis result with source evidence. Penetration-test revalidation is not inferred for this result type. |

### Relationships

| Source → relationship → target | Targets/source | Sources/target | Basis and qualification |
|---|---|---|---|
| Shared service scope → organizes application scopes → Agent Space | 0..* | 1 | logical. Scope hierarchy from the guide, not an AWS Organizations API schema. |
| Integration registration → authorizes selection → Agent Space source connection | 0..* | ? | documented. Provider-specific setup precedes selecting application sources. |
| Agent Space → selects sources → Agent Space source connection | 0..* | 1 | documented. Connection scope is application-specific. |
| Agent Space source connection → references source → Repository or design source | ? | 0..* | documented. A repository can be connected to multiple spaces. Provider-level connection grouping is not forced to one repository. |
| Shared service scope → shares criteria → Security requirement pack | 0..* | 1 | documented. Requirements affect future eligible reviews across spaces, not past results. |
| Security requirement pack → contains → Security requirement | 0..* | 1 | documented. Each requirement belongs to a pack; custom packs may be created before adding requirements. |
| Agent Space → contains configuration → Penetration-test configuration | 0..* | 1 | documented. Different test targets or scopes can have separate definitions. |
| Penetration-test configuration → is executed as → Penetration-test run | 0..* | 1 | documented. Create once, execute repeatedly; runs are independent. |
| Penetration-test configuration → configures identities → Test credential definition | 0..* | ? | documented. Multiple credentials can represent different application roles; reuse constraints are not generalized. |
| Penetration-test configuration → sets target boundary → Target and network rules | ? | 1 | documented. Rule collections are members of configuration, not independently authorized workloads. |
| Test credential definition → supports learned navigation → Retained login procedure | ? | ? | documented. The guide documents reuse, not an exact procedure-to-credential schema or separate skill management API. |
| Penetration-test run → produces evidence → Penetration-test finding | 0..* | 1 | documented. An absence of findings does not establish complete authenticated coverage. |
| Penetration-test finding → is evaluated in → Finding-to-revalidation result | 0..* | 1 | editorial. Normalized lineage association; each pair records one finding's result for one job. |
| Revalidation job → reports selected results → Finding-to-revalidation result | 1..* | 1 | editorial. A job selects one or more findings. Pending or failed work may not yet have a conclusive result value. |
| Full-code review configuration → starts full-source scans → Code review | 0..* | ? | documented. This relationship describes full scans. Repository-event reviews originate through their own connected-source settings. |
| Design review → clones to a new review → Design review | 0..* | 0..1 | logical. New reviews may originate without a clone. This is a logical derivation, not a claimed clone-parent API field. |
| Threat-model configuration → is executed as → Threat-model run | 0..* | 1 | documented. Reusable configuration is distinct from its system overview and threat results. |
| Security requirement pack → supplies enabled criteria → Code review | ? | ? | documented. Selected review modes and current pack enablement matter; existing reviews do not change retrospectively. |
| Security requirement pack → supplies enabled criteria → Design review | ? | ? | documented. Shared requirements do not imply a mutable result shared between applications. |
| Penetration-test finding → initiates proposal work → Remediation attempt | ? | ? | documented. Eligible automatic or manual remediation remains distinct from deployment. |
| Remediation attempt → produces proposed change → Patch or pull request | ? | ? | documented. The output depends on provider and repository support; not every attempt succeeds. |
| Penetration-test run → assesses running system → Deployed test application | ? | 0..* | documented. Target reachability, role and deployed revision must be recorded per run. |
| Revalidation job → retests selected evidence → Deployed test application | ? | 0..* | documented. Repair must reach the original environment; current authentication is used. |
| Penetration-test finding → may be linked → Jira issue | ? | ? | documented. When linked, revalidation can add a result comment. No universal one-issue-per-finding rule is asserted. |
| Repository code-review settings → enables change-triggered reviews → Code review | 0..* | ? | documented. Provider-specific events and source revision identify the change-review path. |
| Remediation repository settings → permits proposal generation → Remediation attempt | 0..* | ? | documented. Provider eligibility and the accepted finding remain required. |
| Code review → produces source findings → Code-review finding | 0..* | 1 | documented. Keep source-review results distinct from running-application findings. |
## AWS FinOps Agent

| Entity | Ownership / kind | Identity and scope | Meaning |
|---|---|---|---|
| FinOps agent instance | aws / service resource | finops-agent AgentSpace actions and agentspace ARN in IAM; AWS account and Region | Independent instance in the UI. Its AgentSpace API/IAM name does not make it a DevOps Agent Space. |
| Agent data role | aws / cross-service resource | IAM role ARN trusted by finops-agent.amazonaws.com; Configured AWS account access | Permits cost and operational reads and the managed-rule operations required for event automations. |
| Operator role | aws / cross-service resource | Configured IAM role ARN; Agent web-application operations | Distinct from the agent data role and from the end user's own entry permissions. |
| Integration registration | aws / service resource | Account-level Jira or Slack integration; AWS account | Registers authorization before an instance is connected to a project or channel. |
| Agent connection | aws / service resource | Connection to selected integration and destination; One agent instance | Binds the registered integration to the selected Jira project or Slack channel. |
| Conversation | aws / interaction record | Conversation in the agent workspace; One agent instance | Can answer directly. A conversation is not automatically a task. |
| Task | aws / execution record | Task in the Tasks workspace; One agent instance | On-demand, scheduled or event-created execution with recorded results. |
| Automation | aws / service configuration | Saved automation in the Automations workspace; One agent instance | Schedule or supported event condition that creates new tasks. |
| EventBridge managed rule | aws / cross-service resource | Service-managed EventBridge rule; Supported event automation | Delivers matching Cost Anomaly Detection events; it is not a general customer event orchestration API. |
| AWS cost and operational evidence | documentation / normalized evidence family | Original query basis, anomaly or recommendation identifier; Underlying cost and operational services | Our grouping of distinct AWS-source results: cost query, forecast, coverage, anomaly, recommendation and change event. It is not one FinOps resource type or a shared evidence API. |
| Context file | aws / retained input | Uploaded file and active state; One agent instance | Operator-maintained reference; the agent can read but not rewrite or delete it conversationally. |
| Persistent memory | aws / managed retained state | Preference, fact or correction addressed in conversation; One agent instance | Supports remember, update and forget; no DevOps-style attachment or version API is inferred. |
| Session runtime | aws / ephemeral execution component | Current session context, not an asserted public resource ID; One session | Loads retained files into an isolated runtime. Ending a session does not delete persistent records. |
| Conversation summary | aws / derived context | Older-message summary within the current conversation context; Conversation context window | Compaction is distinct from persistent memory and does not promise verbatim retention. |
| Report artifact | aws / output record | Artifact in the Artifacts workspace; One agent instance | Generated report that can be inspected, revised, downloaded or deleted independently of external copies. |
| Jira approval decision | aws / authorization interaction | Requested Jira action and invocation context; Interactive or on-demand Jira action | Not required per action for pre-authorized automations; Slack does not use this prompt. |
| Jira project or Slack channel | external / external destination | Provider-native project or channel identity; Destination audience | Publication has its own authorization, membership and retention rules. |
| Published issue, comment or message | external / external artifact | Provider-native issue, comment or message identity; Destination system | A service result copied externally has a lifecycle separate from the originating task or artifact. |

### Relationships

| Source → relationship → target | Targets/source | Sources/target | Basis and qualification |
|---|---|---|---|
| FinOps agent instance → uses data access role → Agent data role | 1 | ? | documented. One configured role responsibility; do not infer that customer-managed roles cannot be referenced elsewhere. |
| FinOps agent instance → uses operator role → Operator role | 1 | ? | documented. Separate permission responsibility from data access and end-user entry. |
| FinOps agent instance → has destination connections → Agent connection | 0..* | 1 | documented. Actual supported connection quotas are separate from logical multiplicity. |
| Integration registration → authorizes connections → Agent connection | 0..* | 1 | documented. Registration is at account level; connection is at instance level. |
| Agent connection → selects destination → Jira project or Slack channel | 1 | ? | documented. Connection binds the intended project or channel. This is not evidence of reading all destination content. |
| FinOps agent instance → retains → Conversation | 0..* | 1 | documented. Conversation history is instance-local. |
| FinOps agent instance → queues and retains → Task | 0..* | 1 | documented. The shared task queue belongs to this instance, not to all agents in the organization. |
| FinOps agent instance → contains future-work rules → Automation | 0..* | 1 | documented. An automation is not an already-created task. |
| Automation → creates on each match → Task | 0..* | 0..1 | logical. A task may instead be on demand. No universal automation ID field is asserted by this logical relationship. |
| Conversation → may explicitly request → Task | 0..* | ? | documented. Direct answers do not require a task, and Tasks workspace is another initiation path. |
| EventBridge managed rule → delivers supported events → Automation | ? | ? | documented. Exact rule-to-automation cardinality is not specified; do not assert one rule per automation. |
| FinOps agent instance → retains reference inputs → Context file | 0..* | 1 | documented. Files are visible to users with agent access, and soft deletion changes active context. |
| FinOps agent instance → retains contextual state → Persistent memory | ? | 1 | documented. No independent customer-managed memory-store schema is documented here. |
| Context file → is loaded for a session → Session runtime | ? | ? | documented. Runtime isolation is not deletion of the retained input. |
| Persistent memory → is loaded for a session → Session runtime | ? | ? | documented. No cross-instance shared memory is inferred. |
| Conversation → compacts older messages → Conversation summary | ? | 1 | documented. Summary representation and revision count are not exposed as a customer-managed resource model. |
| Task → can produce reports → Report artifact | 0..* | ? | logical. Artifacts can also originate from direct conversations. Do not force every artifact to have exactly one task parent. |
| Agent connection → permits supported publication → Published issue, comment or message | 0..* | ? | logical. Jira and Slack actions have different approval behavior; delivery success must be inspected separately. |
| Task → queries authorized evidence → AWS cost and operational evidence | ? | ? | documented. Query dimensions, time basis and source identity govern the meaning of returned values. |

## Official evidence

- [DS50](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html): Agent Space scope and isolation. Retrieved official HTML. 
- [DS51](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssociateService.html): Request, Association response and replacement semantics. Retrieved official API reference. 
- [DS52](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html): Asset types; custom_agent, memory_store, memory; metadata references. Updated official indexed text; cached HTML omits memory asset types. Use the indexed eight-type list and asset-ID references, not the older six-type cached page. ListAssetTypes remains the runtime discovery operation.
- [DS53](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html): Key concepts and execution; store attachment. Updated official indexed text; cached HTML omits memory attachment. 
- [DS54](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html): Triggers, invocation history, cancellation and tool results. Retrieved official HTML. 
- [DS55](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html): Store, memory, versions, retrieval and activation. Retrieved official HTML and indexed memory guidance. 
- [DS56](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html): Incident triage, investigation and feedback. Retrieved official HTML. 
- [DS57](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html): Opt-in, account role, tool category, per-action approval and attribution. Retrieved official HTML. 
- [DS58](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html): Resource discovery, views and scope beyond topology. Retrieved official HTML. Older topology prose calls learned knowledge skills. The model treats topology as a derived view without asserting a new independent storage API.
- [DS59](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html): Evaluations and recommendations. Retrieved official HTML; evaluation and recommendation relationship reviewed. 
- [DS60](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html): Test profiles, executions and application effects. Retrieved official HTML. 
- [DS61](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html): Production operations, release review and on-demand inquiry. Retrieved official HTML. 
- [DS62](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html): Account registration, space association, tool selection and authentication. Updated official indexed text. 
- [SS50](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html): Tenant versus Agent Space scope; assessment lifecycles; repository reuse. Retrieved official HTML. 
- [SS51](https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html): Register once; connect selected sources; supported providers. Retrieved official HTML. 
- [SS52](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html): Credential strategies, multiple credentials and Login Optimization. Retrieved official HTML; later indexed guidance retained for UI detail. 
- [SS53](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html): Requirement membership, shared scope and activation. Retrieved official HTML. 
- [SS54](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html): Selection of findings, job results and original-finding lineage. Retrieved official indexed text. 
- [SS55](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html): Finding-linked remediation and provider-dependent output. Retrieved official HTML. 
- [SS56](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html): Configuration, target rules, credentials and create versus execute. Retrieved official HTML; current guide retains newer wizard details. 
- [SS57](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html): Scope documents, source context, configuration and run. Retrieved official HTML. 
- [SS58](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html): Finding publication and project connection. Retrieved official indexed text; project selection and finding publication reviewed. 
- [FS50](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html): Instance isolation; two roles; integration and connection setup. Retrieved official HTML. 
- [FS51](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html): IAM responsibilities; finops-agent AgentSpace action and ARN names; managed-rule permissions. Retrieved official HTML. 
- [FS52](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html): Conversation versus task; automations; queue; managed events. Retrieved official HTML. 
- [FS53](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html): Files, persistent memory and conversation compaction. Retrieved official HTML. 
- [FS54](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html): Session loading, retained records, isolation and deletion behavior. Retrieved official HTML. 
- [FS55](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html): Account registration and agent-specific destination connection. Retrieved official HTML. 
- [FS56](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html): Account registration, channel connection and one-way publication. Retrieved official HTML. 
- [FS57](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html): Effect and invocation-specific approval; upstream evidence. Retrieved official HTML. 
- [FS58](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html): Artifact production, revision and distribution. Retrieved official HTML. 
- [DS63](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html): Platform-owned managed agents; Learning history and triggers versus incident roles. Retrieved current official indexed text; direct cached URL was unavailable.
