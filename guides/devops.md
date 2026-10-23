# AWS DevOps Agent

Platform capabilities, configuration, and operating mechanisms

AWS DevOps Agent combines managed operational workflows with customer-configured agents, connected tools, and retained context. An Agent Space organizes access and configuration; an agent definition specifies behavior and available context; an invocation records one execution. These are different parts of the service. [DS501] [DS502] [DS504]

The chapters distinguish ten capability dimensions: workspace organization; agent definition; knowledge and behavioral context; invocation; integrations; network connectivity; execution and action control; managed workflows; interaction surfaces and outputs; and administration. The resource model explains how their objects relate. The separate use-case catalog applies those facilities to operational objectives.

**Reading conventions.** This chapter organization is editorial, not an AWS product hierarchy. Named facilities and behavior are linked to official guidance. DOC (blue), AWS (green), and EXT (orange) identify concept ownership in diagrams. Configuration advice and worked examples are labeled as team practice. No AWS execution is reported. Sources with differing retrieved representations are qualified in the source-review record.

## 01. Workspace and resource organization

Agent Spaces, AWS account connections, provider associations, and assets establish the objects available for configuration.

### D-01 — Agent Spaces and AWS account scope

An Agent Space is the configuration and access container for operational work. It associates the primary AWS account, optional secondary accounts, provider connections, and operator permissions. An investigation is work performed within that scope; creating an investigation does not create another Agent Space. [DS50] [DS56]

![Agent Space and provider relationships](../assets/diagrams/er-devops-scope.svg)

Multi-account access connects account-specific roles to the space. Secondary-account roles trust the service principal `aidevops.amazonaws.com` directly, with source-account and source-ARN conditions. The account-connection procedure also requires the documented `iam:PassRole` permission. The operator role and the roles used to inspect resources have different purposes; D-02 covers their configuration. [DS506] [DS19]

Provider registration and association are separate operations. Registration retains the provider endpoint and authentication configuration. Association selects that registration for an Agent Space. AWS documents multiple registrations of the same provider and multiple associations in one space. A team with two monitoring installations therefore does not need to describe them as two kinds of agent or two execution environments. [DS506]

The approved resource diagram is a logical view of these relationships. Its colors distinguish AWS resources from documentation concepts and external systems; its qualified multiplicities are not service quotas. The detailed entity definitions remain in the resource-model reference.

### D-13 — Assets, identities, and configuration references

The Asset API manages configuration and reference material inside an Agent Space. Its eight documented types are `skill`, `agents_md`, `attachment`, `custom_agent`, `memory_store`, `memory`, `test_profile`, and `feedback`. A trigger is a separate resource. These types identify what is stored; they are not eight agent types. [DS504]

![Configuration and knowledge references](../assets/diagrams/er-devops-knowledge.svg)

| Object | Identity and purpose |
|---|---|
| Agent Space | `agentSpaceId`; scope for accounts, integrations, assets, and operator access |
| Provider registration and association | A registered connection and the association selecting it for a space |
| Custom-agent asset | Prompt and references to selected tools, skills, and memory stores |
| Skill or instruction asset | Procedural or standing guidance, with its applicable agent scope |
| Memory store and memory | Container and informational entry; entry versions record content changes |
| Test profile | Native reusable configuration for release UI or API testing |
| Feedback | Feedback associated with an execution |
| Trigger | Start conditions for a custom-agent invocation, rather than reference content |

Use the identifier required by the relevant API field. Custom-agent references to skill and memory-store assets are not interchangeable with display labels. The memory entry's parent-store relationship also differs from an agent's attachment to that store. D-08 covers asset operations and the distinction between API edits and declarative management. [DS504]

An implementation recipe in the use-case catalog is authored setup guidance. It is not an additional AWS asset. In particular, it must not be confused with the native `test_profile` type above.

## 02. Agent definition and customization

Managed agents and custom-agent definitions expose different customization controls. Invocation is covered separately.

### D-15 — AWS-managed agents

AWS supplies managed agents for its built-in capabilities. The documented roster includes Chat, Incident triage, Incident RCA, Incident mitigation, Incident UI, Evaluation, Grader, Release testing, and Learning. Their responsibilities differ: Grader performs investigation Reviews, Incident UI generates investigation outputs, and Learning produces retained knowledge. The roster is not a set of customer-created custom agents. [DS501]

Open **Agents → Managed agents** and select a managed agent. **Agent definition** exposes global and agent-specific instructions; **Knowledge** exposes accessible knowledge. The system prompt, tool set, and skills of a managed agent remain platform-managed. The page does not provide an independent Run now control. [DS501]

The Learning agent additionally exposes **History** and **Triggers**. History identifies knowledge-production runs and their trajectories. Its scheduled tasks are platform-owned: they are not editable custom-agent schedules. The distinction matters when diagnosing stale knowledge: inspect the learning run and its inputs rather than creating a second custom schedule with the same name. [DS501]

Instructions are the supported customization point for managed behavior. Their loading mechanism is described in D-M03; it is separate from the managed agent's underlying system prompt.

### D-16 — Custom-agent definitions and configuration

A custom agent is a saved definition for customer-specified operational work. Its configuration determines the prompt, available tools, assigned procedures, and accessible informational context. A trigger determines when it runs; an invocation is the resulting execution. [DS502]

| Configuration element | What the customer selects | How it affects execution |
|---|---|---|
| System prompt | Markdown defining the objective, approach, and expected output | Loaded as the definition's instructions |
| Tools | Explicit operations from connected providers or custom MCP servers | The invocation uses the assigned tool set |
| Skills | Assigned instruction packages and supporting files | Their procedures are loaded for the invocation |
| Memory stores | Explicit store attachments | The agent can read attached stores and write to attached custom stores; managed stores are read-only to it |

A new custom agent starts without memory-store attachments. Connecting a provider to the Agent Space does not assign all its tools to every custom agent. Tool selection and store attachment are independent configuration decisions. [DS502]

Create or edit the definition on the custom-agent page, configure its prompt and referenced resources, then run a scoped invocation and inspect History. Configuration can also be managed as a `custom_agent` asset. A system prompt can be imported from a Markdown file in a supported GitHub repository and synchronized on demand. Synchronizing the prompt is not a continuous deployment of arbitrary repository changes. [DS504] [DS506] [DS513]

AWS also documents automatic continuation through a subagent when a long invocation approaches its context limit. The continuation receives the same tools and skills; no customer setting is required. This mechanism does not establish a customer-authored routing graph or permission to configure arbitrary inter-agent delegation. Invocation and cancellation are covered in D-07 and D-19. [DS502]

## 03. Knowledge and behavioral context management

Instructions, skills, memories, and attachments differ in purpose, production, loading, and lifecycle.

### D-M03 — Standing instructions and session initialization

Agent instructions are standing behavioral guidance stored as `AGENTS.md`. Global instructions apply across managed agents; agent-specific instructions apply to the selected managed agent. They are Markdown content, not a skill bundle with supporting files. [DS511]

The loading mechanism is unconditional session initialization: a new session receives the applicable global and agent-specific content. Editing the saved instructions affects subsequent sessions. A session already running retains the instructions with which it started. This differs from selecting a skill or memory according to relevance. [DS511]

Open **Agents → Managed agents → selected agent → Agent definition**. Edit the global or agent-specific instructions, save the change, and start a new session to observe its application. Changes to global instructions require confirmation because they affect more than one managed agent. The October 13 changelog records the move from the Knowledge page to these definition pages. [DS501] [DS506]

For example, a team can require an incident summary to state the resource identity and UTC measurement period. That is an output convention. Access to a resource still depends on the selected tool and its authorization; instruction text does not modify those controls.

### D-M04 — Skills, applicability, and supporting files

A skill packages a procedure in `SKILL.md`, optionally with reference or asset files. Its description states when the procedure is relevant, and agent-type targeting identifies eligible consumers. This is procedural context: it explains how to perform work, rather than retaining the result of an earlier investigation. [DS512] [DS504]

For managed agents, description matching determines whether the skill is relevant to the current task. An inactive skill is not loaded. Custom-agent definitions explicitly assign skill assets and load the assigned documents during invocation. These are different selection paths and should not be represented as unconditional loading of every skill in the space. [DS512] [DS502]

To author a skill, open **Knowledge → Skills**, supply `SKILL.md`, describe the circumstances in which it applies, and select the applicable agent types. Include required source operations in the procedure. A skill may specify supported tools through its metadata, but the surrounding tool integration and access controls still apply. Executable skill files require the supported Sandbox surface; storing code in an attachment does not create a runtime. [DS504] [DS514]

Repository import accepts a supported GitHub skill directory or `SKILL.md` source. On-demand synchronization replaces the imported content with the repository's current content. Review the repository revision before synchronization; the service does not describe this as continuous bidirectional editing. [DS506]

### D-M01 — Memory construction and progressive retrieval

A memory is retained informational content, represented as a Markdown file in a memory store. A store's description identifies its subject; an entry's description identifies the content within it. This structure supports selective retrieval rather than loading the entire store into every session. [DS505]

Retrieval proceeds from the available store names and descriptions. The agent selects a relevant store, lists its entries, and reads the files needed for the current task. Activation state and applicable agent access determine whether the content is available. Custom-agent attachments narrow that availability to the selected stores. The mechanism provides task context; it does not itself add a tool or train the model's weights. [DS505] [DS502]

![Incident-memory production and retrieval](../assets/diagrams/mechanism-devops-retrieval.svg)

The managed `monitors` store groups earlier causes by alarm or metric. When the Agent Space has investigations in the preceding two weeks, the documented learning process runs daily and synthesizes recent investigation evidence into these entries. Entries without updates for two weeks are removed; capacity pressure removes the oldest entry. Monitor memory is therefore bounded retained context, not the authoritative archive of every incident. [DS505]

Monitor memory is enabled by default. Inspect **Knowledge → Memories**, open the store and entry, and inspect its description, content, version, and activation state. A later investigation can use that content alongside current telemetry. Establishing that the entry exists, observing a read, and validating the resulting diagnosis are three separate checks. The worked example in D-U01 demonstrates a recurring alarm whose current cause differs from its earlier cause. [DS505] [DS506]

### D-M08 — Managed knowledge production and refresh

The Learning agent reviews the connected environment and past investigations and produces retained context for other agents. Its inputs include discovered topology, code dependencies, pipeline structure, and investigation history. Its output is synthesized knowledge rather than a copy of every tool response. [DS501] [DS505]

| Retained knowledge | Subject |
|---|---|
| `monitors` | Cause history organized by alarm or metric |
| `directives` | User-authored context and preferences |
| `reflections` | Lessons derived from corrective investigation feedback |
| Agent Space Understanding | Resources, environments, request paths, observability coverage, and code-to-deployment mappings |
| Understanding Code Dependencies | Service and package relationships |
| Understanding Pipeline Topology | Pipeline stages and environment promotion |
| Tool Use Best Practices | Tool parameters, recurring errors, and handling of results |

The August 27 changelog states that the knowledge previously described as learned skills is maintained as memory. This historical label does not introduce another customer-authored skill type. The managed-agent page identifies Learning as the producer and exposes its run history and platform-owned triggers. [DS506] [DS501]

Knowledge production and retrieval are distinct. A completed learning run can update context without proving that a later investigation selected it. To examine stale understanding, inspect the relevant learning run, the retained entry, and the source material used to construct it. The topology and Summary report views described in D-05 are representations of this understanding; they are not separate memory-store types.

### D-M02 — Corrective feedback and reflection memory

Investigation feedback associates a verdict with a completed investigation and can provide the actual root cause when the diagnosis was wrong. It differs from steering a running investigation, which changes the current inquiry, and from monitor-history synthesis, which reviews prior occurrences. [DS08]

Submit the correction through **Add feedback** on the completed investigation or through the documented Chat route. Supply the corrected cause and the evidence that establishes it. The most recent submission replaces earlier feedback for that investigation. Sharing feedback with AWS requires a separate confirmation. [DS08]

AWS documents a `reflections` store for the lessons produced from corrective feedback. A subsequent relevant investigation may retrieve that retained context. The service guidance does not establish a guaranteed delay from submission to recall, so a saved correction and demonstrated later retrieval should not be reported as the same event. [DS506] [DS505]

The source incident record remains the place to retain the verified cause and supporting observations. Reflection memory supplies context to later work; it does not replace that record or establish that a repeated symptom has the same cause.

### D-M07 — Memory-store access, versions, and retention

A stored entry must be available to the particular execution before retrieval is possible. Availability depends on activation and, for custom agents, explicit store attachment. Versions then describe how the retained content has changed; they do not change which agent is allowed to access it.

A new custom agent has no store attachments. Its definition selects accessible stores; it can write to attached custom stores, while managed stores are read-only to it. This is narrower than the managed Chat agent's documented memory editing behavior. [DS10]

| Object/action | Documented consequence | Practical inspection |
|---|---|---|
| Deactivate a store or entry | Stop active access without deleting content | Check the active state and rerun a harmless read test |
| Edit memory | New immutable version | Compare content and timestamp |
| Remove custom-agent attachment | Remove that agent's access to the store | Inspect the saved definition |
| Delete a custom store through Chat | Contents must be removed first | Confirm store and entries separately |
| Delete a custom store in console | Deletes its contents; not reversible | Review the selected store before confirmation |
| Delete a managed store | Not supported | Use supported activation/content controls instead |

The last two deletion behaviors and the description-selection model are documented in the indexed memory guidance retrieved for the source review. See the evidence notes for the retrieved-page discrepancy. [DS07]

Memories can be organized by `/`-separated paths within a store. Store and entry descriptions guide selection. The documented limits are 50 stores per Agent Space, 200 memories per store, and 100 KB per memory. Historical viewing, deactivation, and custom-store deletion are different operations; retention of versions is not a claim that a deleted custom store can be restored. [DS505]

### D-17 — Attachments and repository-backed authoring

An attachment stores binary or text reference material, such as a diagram, log sample, or document. It is a reference asset. It becomes a skill only when authored as a supported procedural package, and it becomes memory only through a documented memory-writing or learning path. [DS504]

Repository-backed authoring supports different inputs. Skill import reads a directory or `SKILL.md` and its supported files. Custom-agent import reads a Markdown system prompt. Synchronization is an explicit pull of the repository's current content, not automatic two-way synchronization. [DS506]

Maintain the repository revision and the destination asset identity when updating either kind of content. For a skill, review procedural changes and referenced files. For a prompt, review the behavior and expected output. Re-run an applicable task after synchronization to inspect the saved configuration and its effect. These checks are a team procedure; the import feature itself does not validate operational correctness.

## 04. Invocation and triggers

On-demand requests, schedules, and webhook events start work. Filtering decides whether to start an invocation and what payload it receives.

### D-07 — On-demand invocation and scheduled triggers

An invocation starts a custom-agent definition. From **Agents → selected custom agent**, choose **Run now**, or use **Run with prompt** to add invocation-specific context. Chat can also invoke an agent by name. The saved system prompt remains part of the definition; the extra prompt applies to that run. [DS503]

A schedule trigger starts future invocations. In the agent's **Triggers** tab, create a schedule using EventBridge-compatible `cron(...)` or `rate(...)` syntax. Inspect the saved expression, optional prompt, and next run information. Examples include `rate(1 hour)` and `cron(0 9 ? * MON-FRI *)`; the latter describes weekday starts at 09:00 UTC. [DS503]

Triggers can be paused, resumed, or deleted. These operations govern future starts. Cancellation of an existing invocation is a separate operation described in D-19. Observation interval, start time, and report-delivery time are also different: a scheduled report should state the period it queries rather than derive it silently from a delayed start. [DS503]

The detailed execution guide documents both schedule and webhook event triggers. Its custom-agent overview also contains schedule-only wording. This guide uses the detailed trigger procedure for invocation support and records that source discrepancy rather than treating the overview as an exhaustive list. D-18 describes event selection and payload handling. [DS503] [DS502]

### D-18 — Webhook events, filtering, and payload projection

An event trigger invokes a custom agent when an event arrives from a connected integration with an active webhook. The configured event source and filter determine whether to start an invocation and what event content to pass to it. This mechanism is separate from the managed incident-investigation path and from outbound lifecycle notifications. [DS503]

In **Agents → selected custom agent → Triggers**, create an **Event** trigger and choose an active webhook-enabled integration. Optionally enter a JMESPath expression. If no sources appear, check integration/webhook availability and the operator's `ListAssociations` and `ListWebhooks` permissions. [DS503]

| Expression result | Invocation behavior | Passed context |
|---|---|---|
| Null, false, empty string, empty array, or empty object | No invocation | None |
| Boolean true | Invoke | Original payload |
| Another truthy value | Invoke | Projected result |
| No expression | Invoke for each source event | Original payload |

The expression is limited to 4,096 characters; context supplied to the agent is truncated at 10,000 characters. `severity == 'critical'` filters by severity and passes the raw payload. `{sev: severity}` projects a field but does not filter on its value, because the resulting object contains a key. Validate against the actual integration payload rather than assuming common field names. [DS503]

An event trigger remains listed but does not run if its source integration or webhook is removed. The execution guide describes notices for unmatched events. Webhook authentication is a separate control: the changelog documents HMAC and API-key webhook options and credential rotation without changing the URL. [DS503] [DS506]

## 05. External system integrations

Native providers, outbound MCP tools, and outbound A2A agents expose different external operations.

### D-12 — Supported integrations and connection directions

An integration answers two separate questions: which system can supply evidence, and which system can receive an action or update? Those directions matter. A telemetry connection may permit reading metrics without posting findings back. A webhook may start an investigation without granting any permission to query the originating monitoring system. The following inventory separates these paths rather than treating every connected brand as an equivalent connector. [DS30] [DS31]

| Connection family | Documented systems | Information or effect | Setup boundary |
|---|---|---|---|
| AWS resource and telemetry access | Primary and secondary AWS accounts; CloudWatch | Authorized resource inspection and telemetry queries | Account roles and selected account associations |
| Object-based evidence | Amazon S3 | Read logs, configuration, and other objects | Scope ListBucket and GetObject to required buckets and objects |
| Kubernetes inspection | Amazon EKS | Cluster, pod-log, and event inspection | EKS access setup and network reachability are additional prerequisites |
| Two-way observability | Dynatrace | Telemetry/topology reads; configured problem initiation; investigation updates | Provider setup and the Dynatrace workflow determine the actual paths |
| One-way telemetry access | Datadog, Grafana, New Relic, Splunk | Telemetry reads through the documented provider path | Source authorization; event initiation is separately configured through webhooks |
| Code and delivery context | GitHub, GitLab | Repository and pipeline evidence for operational investigations | Connect the relevant sources and deployment mapping |
| Azure infrastructure | Azure Resources | Subscription-scoped discovery and investigation | Register the tenant connection, then associate subscriptions |
| Azure delivery context | Azure DevOps | Selected project and pipeline-history context | Separate registration and project association; pipeline history does not imply access to externally hosted code |
| Incident coordination | ServiceNow and PagerDuty | Provider-specific incident initiation and updates | Configure the incident route and destination |
| Collaboration | Slack and Microsoft Teams | Slack can support bidirectional private-channel conversations; Teams supplies one-way notifications | Enable the supported channel mode explicitly |
| AWS Support | AWS Support case creation | Open a case from an investigation with its context | Inspect the submitted case and support entitlement |
| Additional tools | Compatible remote or private MCP servers | The tools explicitly selected for the Agent Space | MCP authentication, tool selection, effect classification, and networking |
| External initiation | Authenticated webhooks | Incoming incident information | Caller authentication and request format; not a telemetry-read grant |
| Lifecycle delivery | Amazon EventBridge | Investigation and mitigation lifecycle events sent to configured targets | Event routing and destination permissions; not an arbitrary custom-agent trigger claim |

The named built-in providers above come from the integration overview and provider guidance. A Prometheus or proprietary source can be exposed through the bring-your-own MCP/webhook route; that is not the same claim as a maintained native connector. The three-way distinction between built-in two-way telemetry, built-in one-way telemetry, and bring-your-own sources is documented by AWS. [DS30] [DS31]

![Provider registration and Agent Space association](../assets/diagrams/devops-integrations.svg)

Registration establishes an account-level provider connection. Association makes selected resources or tools available in a particular Agent Space. Authentication is then exercised when the agent invokes the tool. An engineer can therefore diagnose a missing result in sequence: confirm registration, confirm association and tool selection, confirm the route, then inspect the actual call and returned identity. The MCP-specific choices are described in D-03; private routing is described in D-04.

Azure adds another scope decision. Azure Resources and Azure DevOps are independently registered capabilities. The former associates subscriptions; the latter associates projects. The documented registration options include administrator consent and a customer-managed Entra application with federation. Connecting a pipeline whose code lives elsewhere does not automatically provide that repository’s contents. [DS32]

For a first operational deployment, choose the smallest useful evidence chain: the affected AWS service, one telemetry source, and the repository or pipeline that deploys it. Add incident coordination after confirming a read with known service and revision identifiers. This staged verification is an engineering recommendation, not an additional service requirement.

Grafana can query supported ClickHouse-backed data sources. This is functionality through the Grafana integration, not a separate native ClickHouse registration. Source-control support includes the documented GitHub enterprise variants and GitLab Self-Managed. Provider parity should be checked per operation: a registered repository connection does not establish that every provider supports the same event and write features. [DS506]

GitHub registration can use the service's GitHub App, a customer-owned GitHub App, or a personal access token. A PAT-only registration does not supply webhook-based features such as automated code review. Choose the registration mode according to the required operations, not only whether a read succeeds. [DS506]

### D-03 — MCP provider registration and tool selection

MCP connects the agent to a tool interface exposed by another system. The provider supplies the tool behavior; the Agent Space selects which tools the agent may call. Authentication establishes the calling identity, while the selected tool set constrains the available operations.

**Inbound versus outbound:** this section concerns DevOps Agent calling an external MCP server. A client calling DevOps Agent's own remote endpoint is the opposite integration direction; see D-09.

In **Capability Providers → MCP Server → Register**, enter a name and HTTPS endpoint, choose authentication, and supply the relevant fields. The documented transport is Streamable HTTP. After registration, associate the provider under the Agent Space's **Capabilities → MCP Servers** and select the required tools. [DS03]

| Authentication choice | Configuration to prepare |
|---|---|
| OAuth client credentials | Client ID/secret, token exchange URL, parameters and scopes |
| OAuth three-legged flow | Client details, exchange and authorization URLs, scopes |
| API key | Secret value and the actual HTTP header name |
| Multiple secret headers | Explicit secret/header pairs; registration-only credential updates |
| SigV4 | Signing Region, AWS service name, and dedicated role or documented role-less option |

In the role-less SigV4 option, validation is deferred until association and uses the primary account role. Registration alone is therefore not a successful connectivity test. Removal of a provider registration requires removing its associations first. Authentication update support differs by method. [DS03]

**Engineering verification:** register a staging provider exposing only a non-mutating `service_status` tool. Ask for a known service identifier, inspect the returned tool arguments/result, and compare the result with the source. Then request a deliberately unselected tool; the test is whether it is unavailable, not whether the model verbally promises restraint. Tool-effect classification is a separate decision under D-M06.

### D-20 — Outbound A2A delegation

Remote Agent-to-Agent (A2A) integration lets DevOps Agent call an external agent during an investigation or Chat. The external agent is a connected service, not a DevOps custom-agent definition. DevOps Agent discovers its interface through an agent card, invokes it through the supported protocol, and incorporates the returned result. [DS507]

Register **Capability Providers → Remote Agent** with the agent-card URL and supported authentication, then associate the registration with the intended Agent Space. The card supplies the remote interface and capability descriptions used for task selection. Authentication must work both when fetching the card and when invoking the agent. [DS507]

Private connectivity is documented for API key, bearer token, and OAuth client-credentials authentication, but not SigV4. This transport condition is specific to the A2A connection. It should not be copied from MCP configuration without checking the relevant provider guidance. [DS506]

AWS recommends read-only remote agents for investigation and gathering data. The external agent's own downstream access and effects require review: a connection to its endpoint does not transfer the DevOps Agent Space's IAM policies or approval model into that external system. [DS507]

## 06. Network connectivity

Private connections supply transport to endpoints; they are separate from provider identity and tool authorization.

### D-04 — Private endpoints, routing, and DNS

Private connectivity supplies a network path to a supported privately hosted integration. It is a transport capability, not an integration provider, and it does not place the entire DevOps Agent service inside the customer's VPC. [DS508]

The path uses a VPC Lattice resource configuration and a resource gateway with network interfaces in customer subnets. Traffic reaching the target originates from those gateway interfaces. Public integration endpoints instead use the published regional source addresses. Firewall rules must match the selected path. [DS508]

| Configuration decision | What to specify |
|---|---|
| Managed or self-managed connection | Whether the service creates the supported gateway resources or uses existing resources |
| Target host | Reachable private address or hostname, distinct from the provider's complete endpoint URL |
| DNS resolution | Public resolution or in-VPC resolution for private hostnames |
| Port ranges | Required ports; a connection created without ranges permits only 443 |
| OAuth paths | Tool endpoint and token-exchange endpoint can select different private connections |
| Shared VPC | Network account creates/shares the required resources; consuming account uses the documented self-managed arrangement |
| Cross-account or on-premises target | Customer-managed reachability from the gateway subnets to the target |

Create the connection, inspect its status or `failureMessage`, associate it with the relevant provider endpoint, and test an authenticated operation. Network success and application authentication are different checks. Existing gateway/subnet routing, DNS, TLS trust, and endpoint ports remain prerequisites. [DS508] [DS506]

For a shared VPC, follow the AWS RAM and self-managed connection procedure rather than selecting a service-managed gateway in the consumer account. The provider's supported authentication method also matters: a private A2A endpoint does not support all methods available for a public A2A endpoint. [DS506]

## 07. Execution runtime and action control

Invocations, continuation, Sandbox code execution, and directed actions have different runtime and control boundaries.

### D-19 — Invocation state, trajectory, and continuation

An invocation has its own execution state and trajectory. The trajectory records tool calls, returned results, and generated output. Use it to distinguish a failed source operation from a later interpretation of successfully retrieved data. Each individual custom agent supports only one invocation at a time. [DS503]

When a long invocation approaches its context limit, the documented continuation mechanism creates a subagent with the same tools and skills. This is automatic execution behavior. The guide does not infer a customer-configurable subagent graph, a new privilege grant, or additional customer-defined agent types from it. [DS502]

![Triggers and invocation cancellation](../assets/diagrams/mechanism-devops-cancellation.svg)

Cancel from the invocation trajectory or through Chat. Completed work remains in the trajectory, and tool calls already in progress may still finish. Pausing the trigger stops future starts; it does not cancel the running invocation. After either operation, inspect the relevant object and any external effect rather than assuming rollback. [DS503]

Failed tool results can lead the agent to retry, use another approach, or report a failure. The trajectory provides the evidence available for that invocation; it is not a guarantee that all upstream systems were reachable or all required observations were collected. [DS503]

### D-M05 — Sandbox computation and network policy

Some investigations need computation on retrieved material rather than another prose response. Sandbox supplies an investigation-local environment for that purpose. Its package and network configuration governs what code can use, while the underlying source permissions remain separate.

Sandbox provisions a fresh Linux environment per investigation. It can execute code, access configured packages and use account profiles within existing permissions. Its default outbound policy permits AWS service endpoints; other destinations require allowlisting. The reviewed preview does not extend this environment to all chat or custom-agent paths. [DS14]

**Procedure:** in the console, select the space, open **Capabilities → Sandbox → Configure**, select packages and add required host/method/path rules, then save. An empty allowlist is not total network isolation. Remove the Sandbox configuration to stop future use; do not assume that changing configuration rewinds already executed code. [DS14]

**Proposed check:** process a harmless supplied dataset, inspect code and numerical results, and test that an unlisted non-AWS endpoint is unavailable. Do not use production mutation as a connectivity test. Network filtering, AWS permissions and directed-action approvals are distinct controls.

### D-M06 — Directed actions and approval scope

An investigation can recommend a change before anyone authorizes it. Directed actions add an execution path for eligible changes, with enablement, access, tool classification, and approval as separate gates. The operator should be able to identify the exact operation and resource before the change is attempted.

Directed actions require space opt-in, eligible target-account elevated access or integration configuration, and specific operator approval. The approval binds the operation and resource; AWS calls are attributed through CloudTrail. A saved role is a permission ceiling, not a standing approval. [DS16]

**Procedure:** enable the space setting; register the target account's `agentElevatedRoleArn`; review tool categories for connected services; ask for the particular change; review or adjust parameters; approve or reject; then compare resulting state with the approved operation. Programmatically registered tools without `toolDetails` default to read-only. Incorrect classification can bypass the expected approval prompt. [DS16]

When using `UpdateAgentSpace`, supplying `preferences` replaces that complete map; omitted preferences revert to defaults. Read current settings first and verify them afterward. A denied mutation should lead to inspection of enablement, role trust, permission policy, tool category and approval scope—not unconditional elevation. [DS16]

## 08. Built-in managed workflows

AWS-managed investigation, prevention, review, and release-assurance functions apply the platform facilities to defined work.

### D-06 — Incident triage, investigation, and prevention

![Workflow: Incident triage, investigation, and prevention](../assets/diagrams/devops-incident.svg)

The first operational decision is whether a signal needs new work. Correlation can attach it to an existing investigation, and configured criteria can exclude it. Only after that routing decision should the operator interpret the investigation itself. A correction to routing is consequently different from feedback on a root-cause conclusion.

An external signal is triaged before an independent investigation is necessarily started. **Linked** adds the signal to existing work; **Skipped** applies configured skip criteria; **Proceed** schedules new work. The web app shows the decision and reason. Unlinking or unskipping reschedules independent investigation; correlation or skip skills can be corrected for future events. [DS08]

For a manual investigation, supply the problem, optional starting evidence, incident time, name and priority. Inspect investigation output and tool evidence, then submit feedback after completion. A route decision, a diagnosis, and a feedback verdict are different records. [DS08]

**Engineering procedure:** for an unexpected absence of investigation, first inspect the triage record. A linked event is not lost; follow its primary investigation. A skipped event calls for reviewing the matching skill. For incorrect diagnosis, add the verified correction rather than changing a routing rule unless routing itself was wrong.

Prevention evaluations analyze multiple investigations into recommendations. The **Improvements** page exposes the latest evaluation summary, manual evaluation and schedule controls; the documented default is weekly. This differs from daily monitor-memory refresh. [DS15]

### D-21 — Investigation Reviews and conversational assistance

Conversational assistance and investigation Reviews are managed product functions. Chat answers questions using connected environment context. It supports attachments and inline tables/charts, and the documented interface offers voice input and Smart, Balanced, or Fast model tiers. These are interaction and output capabilities, not additional knowledge-store types. [DS506]

A Review assesses a completed investigation and reports an overall helpful/not-helpful verdict with criterion-level results. The managed Grader agent performs this work. A Review is different from customer feedback that supplies a corrected root cause; the latter can feed reflection memory. [DS501] [DS506]

Within an investigation, live summaries and timeline messages support continuing the inquiry. The changelog also documents resuming completed work and forking from an agent or user message. A fork explores a separate inquiry while preserving the original investigation. These lifecycle operations are part of the managed investigation workflow rather than custom-agent creation. [DS506]

### D-22 — Release-readiness review and release testing

Release-readiness review examines a change, whereas release testing exercises a deployed application. These preview functions use different inputs and can have different permissions and effects. They belong to the managed workflow layer, not to the same category as a skill file or private connection. [DS60] [DS61]

| Function | Primary input | Configuration | Result |
|---|---|---|---|
| Release-readiness review | Repository change and relevant environment context | Supported repository integration, review settings, and applicable runtime roles | Review findings and supported verification results |
| Release UI testing | Deployed web endpoint and personas | Native UI test profile and credential references | Executed tests and results |
| Release API testing | Deployed API and its specification | Native API test profile, target, and credentials | Executed API tests and results |

Automated GitHub PR and GitLab MR review triggers are documented for private repositories. Public-repository reviews can be requested through supported interactive or remote workflows. Provider support for reading code does not itself enable automated change-review events. [DS506]

Native test profiles store the target endpoint, test type, applicable personas and API specification, and credential configuration. TOTP authentication is supported for UI and API profiles; email-based 2FA applies to UI profiles only. The email option supplies a profile-specific forwarding address and an optional sender filter. Release testing sends real application requests, including writes, so its target and credentials must be suitable for the intended test effects. [DS516]

Treat the code revision, deployed revision, test profile, and test result as separate identities. The approved release-readiness and release-test use cases retain distinct completion criteria.

## 09. Interaction surfaces, outputs, and outbound events

Interfaces expose the service; artifacts and views represent its results; lifecycle events notify external consumers.

### D-09 — Console, web application, and inbound remote access

The Management Console administers Agent Spaces, provider connections, access, and related settings. The operator web application provides Chat, investigations, managed/custom-agent pages, and operational views. Collaboration channels provide their documented interaction modes. These are ways to use the service, not execution environments owned by the customer. [DS18] [DS506]

Remote-server access allows IDEs, CLIs, or other clients to call DevOps Agent. The detailed setup guide documents dedicated MCP and A2A endpoints with scoped access tokens or SigV4 authentication. The overview also names ACP; do not infer the same endpoint or authentication procedure for every protocol from that overview alone. [DS509] [DS18]

| Direction | Caller | Target |
|---|---|---|
| Inbound remote access | External client | DevOps Agent's remote endpoint |
| Outbound MCP | DevOps Agent | Connected external tool server |
| Outbound A2A | DevOps Agent | Registered external agent |

Configure the relevant direction independently. For inbound access, select the remote endpoint and client authentication method and grant only the required scope. For outbound access, register the provider and associate it with the space. Reusing the term MCP for both paths does not make their credentials, operations, or permissions interchangeable. [DS509] [DS03] [DS507]

### D-05 — Topology, environment summaries, and export

Topology is assembled from discovered resources and evidence of their relationships. It helps the agent connect a service to its deployment, repository, and dependencies. It is a representation of the environment, not the environment itself: an inferred edge can be wrong and an undiscovered resource can still be readable through an authorized tool.

Discovery collects CloudFormation resources and, for tagged resources outside CloudFormation deployments, uses enabled Resource Explorer. Relationship evidence can include configuration, tags, deployment mapping and observability. Learned topology/pipeline views summarize that evidence; raw-resource views expose different levels of granularity. A missing graph node does not prove the agent cannot investigate the resource. [DS04]

The managed Learning agent maintains environment knowledge. Its page provides knowledge, run history and scheduled-trigger inspection. Its schedules belong to the platform, unlike custom-agent triggers. The August 27 changelog records the move of learned topology, dependency, pipeline, and tool-use knowledge into memory. Some retrieved pages retain the earlier learned-skills terminology. [DS06] [DS19]

**Engineering verification:** choose one service, identify its actual deployed resources and repository revision, and compare them with the graph. Record missing or incorrectly inferred edges separately. Inspect a learning run and the output's version after refresh; clicking a refresh control is not the completion evidence. Do not enable additional account writes to repair a read/discovery gap.

The topology interface includes application and pipeline views. Downloading PNG, JSON, or Mermaid exports the selected view. The Summary report is a versioned, read-only view derived from environment understanding and is available through the documented console and artifact surfaces. These outputs represent learned context; they are not independent knowledge-store types or access-control boundaries. [DS506]

### D-23 — Artifacts, notifications, and outbound lifecycle events

Custom agents can produce text, artifacts, and recommendations according to their instructions and assigned skills. Progress notifications can communicate intermediate findings through configured notification channels. Investigations and Chat also support the documented Markdown export; investigation PDF printing is an output operation, not a separate analysis capability. [DS502] [DS506]

Investigation and mitigation lifecycle events are delivered through EventBridge. A completion event can contain `summary_record_id`. The documented consumer procedure calls `ListJournalRecords` with the relevant event identifiers and locates that record in the returned journal data. Do not infer a Get-by-summary-ID operation from the presence of the identifier. [DS506]

These are outbound events: the service informs a downstream consumer that work changed state. A custom-agent webhook trigger is inbound: an external event starts work. Keep the source, destination, authentication, and resulting execution or notification record explicit for each direction.

## 10. Administration, security, and automation

IAM and operator access, Asset APIs, infrastructure as code, credential maintenance, and service telemetry support administration.

### D-02 — Resource roles and operator roles

Resource access lets an execution inspect infrastructure; operator access lets a person use the space. These paths are configured together during setup but fail independently. Establishing the distinction first makes a missing data result easier to diagnose than treating every failure as an agent problem.

**Administrator procedure.** In the AWS console, create an Agent Space, give it a name, and configure primary-account resource access. Select an automatically created role, an existing role, or the policy-template route for customized permissions. Configure the Web App role separately, then create the space. The expected confirmation is an **Operator access** button that opens an authenticated web application. Creating a space successfully is not confirmation that a particular telemetry API is readable. [DS02]

| Decision | Resource-access path | Operator-access path |
|---|---|---|
| Purpose | Allow the service to inspect authorized AWS resources | Allow personnel to interact with the space |
| Review | Target accounts, actions, resource scope and trust | Which users can enter and what operations they can perform |
| Proposed test | Read one known non-sensitive resource and inspect its identity | Sign in as the intended operator, not only the setup administrator |
| Failure interpretation | Missing data can be an API or role problem | An unavailable app can be an identity/access problem |

**Engineering procedure:** record the space ID, Region, role ARNs and one tested resource. Keep policy source in Git. Do not publish account secrets or copy broad policy examples without adapting their resource scope. For secondary-account trust and exact IAM statements, use the linked current AWS procedure; this guide does not invent a universal trust policy. [DS19]

### D-08 — Configuration APIs and update semantics

Programmatic configuration makes agent settings maintainable alongside other infrastructure definitions. It also requires attention to the resource being updated: changing asset metadata and replacing a preference map have different semantics. Reading the current state is therefore part of preparing a safe update.

Asset management uses the `devops-agent` CLI/SDK client but `aidevops:` IAM actions. `ListAssetTypes` discovers supported types; other asset operations generally authorize against the Agent Space ARN. Metadata keys use snake_case, while top-level request keys use camelCase. Metadata updates use PATCH semantics; asset type cannot be changed. Custom-agent skill/store references require asset IDs, not names. [DS17]

**Read-only inspection pattern:**

```bash
aws devops-agent list-asset-types --region "$AWS_REGION"
aws devops-agent list-assets --agent-space-id "$AGENT_SPACE_ID" --region "$AWS_REGION"
```

Set both variables to your approved environment; these commands were not executed here. Inspect returned metadata before changing it. Asset PATCH behavior must not be generalized to the replacement behavior of the directed-action preference map. For content upload/file operations and deployment templates, follow the type-specific official examples rather than constructing an undocumented payload. [DS17]

#### Declarative management and file operations

`AWS::DevOpsAgent::Asset` manages all eight asset types declaratively. `AWS::DevOpsAgent::Trigger` manages the documented schedule-trigger configuration. CDK constructs and Terraform `awscc` resources expose these types. Do not infer CloudFormation support for every event-trigger field merely because the UI can create that event trigger. [DS504] [DS506]

CloudFormation owns an asset's complete metadata and file set. Per-file edits, content download, historical-version operations, and repository import/synchronization remain distinct Asset API operations. Plan which system owns the configuration: a later declarative deployment can replace content edited through another surface. [DS504]

### D-24 — Identity providers, credential maintenance, and service telemetry

Operator access can use the documented OIDC identity-provider integrations, including Okta and Microsoft Entra ID. User/group assignment and revocation govern web-app access. These controls are separate from the AWS roles and external-provider credentials used by executions. [DS506]

Registered provider credentials can be rotated where the provider supports in-place updates, retaining associations. Webhook rotation retains the webhook URL. Multi-secret-header MCP registrations are an explicit exception to in-place update support. Authentication maintenance must therefore follow the provider-specific operation, not one assumed universal rotation API. [DS506]

CloudTrail records the documented asset operations, remote authentication activity, and directed-action attribution. Investigation timelines expose tool-call and safety-check information. Vended logs and CloudWatch metrics provide another inspection surface for the service's own operation. [DS506] [DS510]

| Metric | Accounting scope |
|---|---|
| `ConsumedOnDemandTime` | On-demand Chat sessions and custom-agent runs; measured in seconds |
| `ConsumedChatRequests` | Chat with investigation requests; not all on-demand Chat |
| `ConsumedInvestigationTime` | Investigation execution time |
| `ConsumedEvaluationTime` | Evaluation execution time |
| `TopologyCompletionCount` | Completion of topology processing |

Use the metric's documented dimensions and statistic when aggregating usage. A usage counter is not a measure of diagnostic correctness or incident resolution. [DS510]

### D-10 — Execution limits and diagnostic procedures

Selected defaults in the reviewed quota guide: three concurrent investigations per space; five concurrent custom invocations per space but one per custom agent; one-hour custom invocation timeout; 500 allowlisted MCP tools; 50 memory stores, 200 entries per store and 100 KB per entry. Some concurrency quotas are adjustable; the custom-agent and memory limits shown are not. Confirm the effective quota before rollout. [DS22]

| Symptom | Inspect first | Corrective decision / expected evidence |
|---|---|---|
| Web app unavailable | Operator identity and role | Repair entry permissions; opening as administrator is not the end-user test |
| Missing topology resource | CloudFormation/Resource Explorer and readable metadata | Distinguish discovery absence from denied direct access |
| Provider registers but no tool works | Space association, selected tools, auth mode | For role-less SigV4, verify primary-account validation and invoke permission |
| Private endpoint times out | Connection failureMessage, DNS, port ranges, gateway ENIs | Correct the network path before rotating a valid secret |
| Memory is ignored | Store/entry activation, descriptions, agent attachments | Compare availability and observed retrieval separately |
| Instruction change has no effect | Session start time and instruction scope | Retest in a newly started session |
| Custom run cannot start | Existing invocation and per-agent concurrency | Cancel or inspect current work; do not duplicate definitions |
| Mutation is rejected | Opt-in, role, category, approval | Repair the failing layer; preserve the narrow target scope |

This diagnostic ordering is an engineering synthesis of D-02 through D-M06, not an additional AWS troubleshooting API.

## 11. Appendix: worked example and reference material

The approved operational objectives and prepared example remain separate from the platform-capability explanation.

### D-14 — Incident and reporting use cases in the resource model

The approved incident-investigation case begins with an operational objective: explain the current incident using current evidence. Its first objects are the incident signal, any triage decision and the resulting investigation. A signal may join existing work or be skipped; an investigation can also begin manually. The signal and investigation must therefore remain separate records. A correction to routing changes their relationship, while steering changes the investigation analysis. [DS56]

![Incident records and action authorization](../assets/diagrams/er-devops-incidents.svg)

For [UC-D02, investigate a service incident](../catalog/index.html#UC-D02), evidence retrieval traverses the space's selected source operations. Historical context is optional: the investigation may examine a relevant memory entry, but its conclusion still depends on observations from the current interval. After completion, verified corrective feedback can record what the original conclusion got wrong. The feedback operation and later retained corrective context are connected, but the public material does not establish a universal one-feedback-to-one-memory cardinality. [DS55] [DS56]

[UC-D06, service health and trends](../catalog/index.html#UC-D06), uses the same source-access layer for a different result. A native snapshot may be answered in Chat. The configured reporting profile instead uses a custom definition, selected telemetry tools and any required service mappings. Its invocation records the actual reads and failures. A trigger adds recurring starts without redefining the observation period or turning the result into continuous monitoring. [DS53] [DS54] [DS61]

| Approved outcome | Objects to configure or inspect | Record used to evaluate completion |
|---|---|---|
| Investigate an incident | Space, source association, signal, investigation, applicable memory | Current observations, hypotheses and conclusion |
| Report service health | Chat or custom definition, selected tools, optional store and trigger | Observation window, source measurements, failed reads and report |
| Document topology | Discovery inputs, learning execution, derived topology and knowledge version | Owner-reviewed relationships and unresolved edges |
| Consolidate SOPs | Reviewed procedure, skill asset, applicability and selected tools | Matching and nonmatching procedure tests |
| Execute approved mitigation | Opt-in, role binding, classified tool and exact approval | Action attribution, resulting state and recovery measurements |

The table is a map of the existing cases, not additional native functionality. In particular, the engineering team owns SOP reconciliation and architecture-document acceptance. The service supplies the documented skills, discovery and execution facilities those processes use. A report does not automatically publish itself to an external destination, and a mitigation recommendation does not authorize a change. [DS52] [DS57] [DS58]

To troubleshoot a case, locate the first missing relationship. A registered provider with no usable association is different from an invocation that queried the wrong interval. A stored memory with no attachment is different from a retrieved entry that conflicts with current data. The detailed case dependencies identify whether to stop, continue with a qualification or transfer work to an engineer. Those failure decisions are authored operating guidance; they are not an additional AWS workflow engine.

### D-U01 — Recurring-alarm investigation: worked example

**Synthetic exercise, not an AWS execution.** The same checkout latency alarm fired in two incidents. In the first, connection exhaustion was verified. The new fixture contains the evidence below; values are invented and are not performance claims.

| Observation | Earlier incident | New incident |
|---|---:|---:|
| Database connections / configured limit | 100 / 100 | 34 / 100 |
| Database query p95 | 900 ms | 18 ms |
| Inventory upstream p95 | 40 ms | 2,900 ms |
| Checkout p95 | 3,200 ms | 3,100 ms |
| Known change | Database pool configuration | Inventory deployment at 10:02 UTC |

**Walkthrough:** inspect the old monitor entry; start a separately identified investigation with the new UTC window and evidence; ask for competing explanations; locate observable memory/tool access; compare the result to the table. The prior database hypothesis is weakened by current connection and query figures. The inventory path is the stronger lead, but a nearby deployment alone does not establish its internal cause.

**Expected output:** a current-evidence explanation identifying upstream latency as the supported direction, the old cause as historical context, and missing upstream logs as an unresolved dependency. No deployment action is justified solely by this fixture. A wrong repeated database diagnosis should receive corrective feedback with the contrary evidence.

**Failure branch:** when no retrieval evidence is exposed, record memory use as unverified. When current telemetry is inaccessible, report insufficient evidence; do not substitute the old memory for current measurements. This exercise tests the distinction between retention, retrieval and diagnosis, not whether a memorized sentence appears.

### D-11 — Documentation coverage and references

The preceding chapters explain the resource model, integration setup, retained knowledge, and execution paths needed for day-to-day operation. The coverage table distinguishes procedures described here from subjects that remain linked reference material. In particular, a source link for a remote protocol or preview release feature is not a claim that its entire configuration has been reproduced or exercised.

The reference register identifies the official pages supporting product-specific statements. The capability exposition follows the supplied outline. Agent definitions, triggers, assets, integration directions, release authentication, and selected knowledge behavior were checked for the 23 October 2026 revision. Retained procedures keep their existing references and review boundaries. Authored diagrams show logical relationships; the worked incident and proposed acceptance checks are not records of live AWS execution.

| AWS subject | Treatment here | Deliberate boundary |
|---|---|---|
| Workspace, roles, topology | Configuration and diagnostic model | Exact organization IAM policy remains in official reference |
| MCP/private connectivity | Authentication decisions and operational sequence | No customer network topology assumed |
| Knowledge and learning | Producer, retrieval, feedback, activation, attachment, lifecycle | No claims about hidden ranking or model training |
| Managed/custom execution | Definitions, routing, on-demand/scheduled/event invocation, continuation, cancellation | Provider-specific event payloads and full protocol schemas remain linked |
| Assets and directed actions | Distinct update semantics and authorization | Full SDK schemas and denial lists linked |
| Sandbox/release preview | Runtime scope, test-profile fields, authentication, and effect boundaries | Complete environment and deployment procedures remain linked |
| Quotas | Selected day-to-day constraints | Complete current quota/Region tables remain authoritative |

**Source-version qualifications:** retrieved representations differ for instruction navigation, asset types, trigger coverage, custom-store access, and learned-knowledge storage. The dated change entries and topic-specific procedures support the selected descriptions; the differing representations are recorded in `qa/exposition-review.json`. The guide does not infer publication order from retrieval order or provide a complete regional inventory.

#### Official sources and reviewed sections

- [DS01] Service/feature eligibility; Supported Regions and Feature availability.
- [DS02] Space creation; primary account and Web App roles; verification.
- [DS03] MCP requirements; registration, association, authentication, rotation and role-less validation. Retrieved-source qualifications are recorded in the review notes.
- [DS04] Topology views, discovery and scope beyond the graph.
- [DS05] Private gateway operation, firewall rules and connection verification.
- [DS06] Managed agents; Learning history and platform-owned triggers. Indexed content used.
- [DS07] Memory production, retrieval, versions, activation, custom-store deletion. Older HTML reconciled with newer indexed content.
- [DS08] Investigation initiation, triage decisions/corrections and feedback.
- [DS09] Instruction scoping and new-session behavior; newer indexed navigation used.
- [DS10] Custom-agent tool/store scope and invocation model. Retrieved-source qualifications are recorded in the review notes.
- [DS11] Skill applicability, format and authoring.
- [DS12] Custom-agent creation and store selection. Indexed content used.
- [DS13] Manual execution, schedules, cancellation and trajectories.
- [DS14] Sandbox execution, network defaults, configuration and preview limits.
- [DS15] Prevention evaluations and controls.
- [DS16] Directed-action enablement, preferences replacement, categories, approval and audit.
- [DS17] Asset operation/permission map, IDs and PATCH metadata. Retrieved-source qualifications are recorded in the review notes.
- [DS18] Built-in versus custom capabilities.
- [DS19] Dated changes: monitor default, memory migration, reflections, private ports.
- [DS20] Access methods and direction; client-specific setup not reproduced.
- [DS21] Release testing operation and application-write warning.
- [DS22] Selected quota defaults and adjustability; newer indexed table used.

[DS01]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html
[DS02]: https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html
[DS03]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
[DS04]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
[DS05]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html
[DS06]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html
[DS07]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
[DS08]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html
[DS09]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html
[DS10]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
[DS11]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html
[DS12]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html
[DS13]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
[DS14]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html
[DS15]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html
[DS16]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
[DS17]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html
[DS18]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
[DS19]: https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html
[DS20]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html
[DS21]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
[DS22]: https://docs.aws.amazon.com/devopsagent/latest/userguide/quotas.html
[DS30]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html
[DS31]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-telemetry-sources-index.html
[DS32]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-azure-index.html
[DS33]: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html
[DS401]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
[DS402]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
[DS403]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
[DS404]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html
[DS405]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html
[DS406]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html
[DS407]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
[DS408]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
[DS409]: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html
[DS410]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html
[DS411]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
[DS412]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html
[DS413]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
[DS414]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html
[DS415]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html
[DS50]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html
[DS501]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html
[DS502]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
[DS503]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
[DS504]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html
[DS505]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
[DS506]: https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html
[DS507]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html
[DS508]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html
[DS509]: https://docs.aws.amazon.com/devopsagent/latest/userguide/accessing-devops-agent-connect-to-devops-agent-remote-servers.html
[DS51]: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssociateService.html
[DS510]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-vended-logs-and-metrics.html
[DS511]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html
[DS512]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html
[DS513]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-managing-custom-agents.html
[DS514]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html
[DS515]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
[DS52]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html
[DS53]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
[DS54]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
[DS55]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
[DS56]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html
[DS57]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
[DS58]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
[DS59]: https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html
[DS60]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
[DS61]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html
[DS62]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
[DS63]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html

[DS516]: https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
