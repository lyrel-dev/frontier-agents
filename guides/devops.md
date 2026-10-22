# AWS DevOps Agent

Architecture, integrations, knowledge, and operational workflows

An incident rarely arrives with all of its evidence in one place. The alarm identifies a symptom; logs describe individual failures; a deployment system records changes; and a runbook explains the service’s expected behavior. AWS DevOps Agent works across the sources made available to an Agent Space to investigate that operational question. The service also supports operational inquiries, prevention analysis, and custom-agent work. Release-assurance features have separate availability and effects. [DS18] [DS08]

This guide begins with the objects an operator configures, then follows the evidence into an execution and into retained knowledge. After the integration and knowledge chapters, it explains incident handling, custom reports, and controlled actions. The worked example shows why an earlier root cause is useful context but cannot replace present measurements. The grouped use-case catalog applies these mechanisms to daily work; it is not a second list of platform capabilities.

Product behavior is linked to official AWS documentation. Diagrams are logical explanations of documented resources and flows, not disclosures of AWS’s internal implementation. Procedures marked as engineering guidance and synthetic examples describe proposed team practice. No live AWS execution is claimed.



## 01. Resource model and scope

Begin with the product-specific entities, their scope and their relationships. Configuration, executions, knowledge and external evidence are distinct objects with different lifecycles.



### D-01 — Agent Space, configuration and execution

AWS DevOps Agent uses an Agent Space to scope operational work. The space brings together the AWS account access, selected external services and retained context needed to investigate an application. It is not an individual investigation and it is not the running application being observed. A new investigation creates a record of work within that configured environment; it does not create another Agent Space. [DS50] [DS56]

The resource model has three layers. Provider registration establishes an integration and its authentication. Association then selects how that registered service is used by an Agent Space. Executions use the available operations and applicable context to collect evidence or produce a result. A connection error belongs to the first two layers; an unsupported diagnosis belongs to the execution and evidence layer. These faults require different corrective actions. [DS51] [DS62]

![DevOps Agent scope, providers and execution](../assets/diagrams/er-devops-scope.svg)

Green boxes are AWS-defined objects or documented concepts. The label beneath each name distinguishes an independently addressable resource from a configuration member or derived view. Orange boxes identify external source systems. The blue concepts used by this collection, such as a use case or implementation profile, organize the explanation but are not resources created in the service. The complete ownership convention is described in the shared guide A-10.

Managed and custom agents have different administrative models. Managed roles belong to the platform; the incident roles operate as part of an investigation. Learning has its own history and platform-owned triggers. A custom agent is instead a saved definition whose prompt, selected tools, skills and memory access the team configures. Running that definition creates an invocation with a separate status and trajectory. [DS63] [DS53] [DS54]

These distinctions connect the service to the approved outcomes. Incident triage and investigation use the built-in operational path. A native health inquiry can use Chat. A repeatable report with a prescribed structure may use a custom definition and optional trigger. A mitigation proposal is an output; carrying out a directed action introduces additional authorization. Release-readiness review and deployed-application testing are separate preview paths with different subjects and effects. [DS56] [DS57] [DS60] [DS61]

The following section explains identities and relationships. Subsequent chapters follow the same model through integration setup, knowledge production, execution and the approved use cases. The [resource index](../catalog/resource-models.html#model-devops) provides the entity dictionary and individually qualified relationship multiplicities; it is not an inventory of resources in your account.

<!-- mechanism-review:start D-01 -->

#### MX-D-QUERY — Built-in operational inquiry

**Classification:** Built-in inquiry workflow. **Inputs:** Explicit question, service/account scope, observation interval and connected evidence.

The built-in inquiry path answers an operational question without requiring a separately created custom agent. It still depends on the Agent Space sources and permissions. A custom definition is useful for a recurring or specialized procedure, not a repair for missing read access. [DS407] [DS401]

The response is scoped to evidence actually available to that request. Record the queried period and reproduce a material observation before treating a health summary as an operational fact. [DS407] [DS401]

**Configuration and enablement**

1. **Scope.** Open Chat in the intended Agent Space and state service identifiers and UTC interval. Applies to: Current request.
2. **Evidence.** Check relevant source associations and permission scope. Applies to: Underlying read access.

[DS407] [DS401]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Question submitted | Read available evidence | Response or source gap is produced. |
| Question needs recurring execution | Define a custom task separately | A new configuration path, not automatic conversion. |

[DS407] [DS401]

**Controls.** A conversational request is not permission for a state-changing operation.

**Observable output.** Scoped answer and available supporting tool observations.

**Not established by the reviewed sources.** No universal source-completeness or exact query-planning guarantee is provided.

**Proposed verification — not executed**

1. Ask for one known staging service measurement in a complete interval.
2. Compare it with the monitoring source.
3. An unavailable metric must be listed as missing rather than inferred as healthy.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS407] | Custom agents compared to built-in capabilities | On-demand queries are a built-in path; custom agents are separately configured. |
| [DS401] | Configuring MCP tools in an Agent Space | Connected evidence remains subject to selected source tools. |

<!-- mechanism-review:end D-01 -->

### D-13 — Configuration identities and knowledge relationships

A resource name is useful to a person, but it does not necessarily identify a valid relationship in an API. An Agent Space has an `agentSpaceId`. A service association records the space, `serviceId` and `associationId`, together with provider-specific configuration. Registering a provider and associating it are therefore different operations. The association API also documents replacement of an existing association of the same service; adding an association is not an unrestricted append operation. [DS51]

The asset model provides another identity layer. A custom-agent definition, skill, instruction file, memory store or memory entry can be represented through its documented asset type. References between these assets use the expected identifiers. In particular, the `skills` and `memory_stores` arrays of a custom-agent definition refer to existing asset IDs in the same Agent Space, not display names. A memory entry identifies its parent store. These are concrete relationships that can be inspected and configured, rather than abstract claims that an agent has access to all organizational knowledge. [DS52]

![Stored knowledge and configuration references](../assets/diagrams/er-devops-knowledge.svg)

Knowledge has both a production path and a use path. Managed learning synthesizes environment or investigation information into retained context. A later execution selects relevant available stores and entries rather than receiving every file indiscriminately. Versions describe changes to an entry; active state and custom-agent attachment describe availability. None of those observations alone proves that a particular investigation used the information correctly. D-M08 describes consolidation, D-M01 retrieval, and D-M07 access and lifecycle in detail. [DS55] [DS63]

A custom definition begins without attached stores. An attached managed store is read-only to that custom agent, while attached custom stores support the documented write behavior. Managed-agent knowledge access and custom-agent attachment should consequently not be represented by one universal permission rule. Standing instructions and applicable skills are other kinds of context: they are not memory entries and do not grant source-system permissions. [DS53] [DS55]

| Object or relationship | What changes | What remains a separate concern |
|---|---|---|
| Provider association | Selected provider-specific configuration | Authentication, target routing and actual tool result |
| Custom-agent definition | Prompt and references to available tools, skills and stores | Each invocation and its output |
| Memory entry version | Retained content | Activation, attachment and observed retrieval |
| Learning execution | A particular knowledge-production run | Correctness and freshness of the resulting representation |
| Custom trigger | Future start conditions | Existing invocation cancellation and observation window |
| Directed-action approval | Authorization for the requested operation and target | Permission ceiling, actual resource state and service recovery |

The table summarizes different lifecycles; it is not an instruction to apply the same update or delete operation to every object. Custom-agent execution and cancellation are documented under D-07. Directed actions have a separate control sequence under D-M06. Topology is a derived representation of discovered and inferred relationships; its visible boundary is not the full IAM access boundary. [DS54] [DS57] [DS58]

In the diagrams, `0..*` means an optional repeated logical association, not an unlimited service quota. `?` means that the reviewed documentation does not establish exact multiplicity. Dashed edges mark logical or editorial associations rather than asserted service foreign keys. Each qualification and its supporting source is retained in the [relationship register](../catalog/resource-models.html#model-devops).



## 02. Data sources and integration configuration

An investigation can use only the evidence exposed through its configured access paths. Start with the supported connection families, then distinguish operator roles, provider authorization, selected tools, and private routing.



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
| Incident coordination | ServiceNow, PagerDuty, Slack | Provider-specific incident initiation and communication | Configure each provider’s documented route and permitted destination |
| Additional tools | Compatible remote or private MCP servers | The tools explicitly selected for the Agent Space | MCP authentication, tool selection, effect classification, and networking |
| External initiation | Authenticated webhooks | Incoming incident information | Caller authentication and request format; not a telemetry-read grant |
| Lifecycle delivery | Amazon EventBridge | Investigation and mitigation lifecycle events sent to configured targets | Event routing and destination permissions; not an arbitrary custom-agent trigger claim |

The named built-in providers above come from the integration overview and provider guidance. A Prometheus or proprietary source can be exposed through the bring-your-own MCP/webhook route; that is not the same claim as a maintained native connector. The three-way distinction between built-in two-way telemetry, built-in one-way telemetry, and bring-your-own sources is documented by AWS. [DS30] [DS31]

![Provider registration and Agent Space association](../assets/diagrams/devops-integrations.svg)

Registration establishes an account-level provider connection. Association makes selected resources or tools available in a particular Agent Space. Authentication is then exercised when the agent invokes the tool. An engineer can therefore diagnose a missing result in sequence: confirm registration, confirm association and tool selection, confirm the route, then inspect the actual call and returned identity. The MCP-specific choices are described in D-03; private routing is described in D-04.

Azure adds another scope decision. Azure Resources and Azure DevOps are independently registered capabilities. The former associates subscriptions; the latter associates projects. The documented registration options include administrator consent and a customer-managed Entra application with federation. Connecting a pipeline whose code lives elsewhere does not automatically provide that repository’s contents. [DS32]

For a first operational deployment, choose the smallest useful evidence chain: the affected AWS service, one telemetry source, and the repository or pipeline that deploys it. Add incident coordination after confirming a read with known service and revision identifiers. This staged verification is an engineering recommendation, not an additional service requirement.



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

<!-- mechanism-review:start D-03 -->

#### MX-D-READ — Evidence retrieval through selected tools

**Classification:** Tool-access mechanism. **Inputs:** Registered provider endpoint and authentication; space association; selected operation; resource identifiers and observation interval.

A successful provider registration establishes a connection, not the result of a particular query. The Agent Space association selects the available tool surface. A custom definition can further restrict that surface. At execution time the source still evaluates the actual credentials and request arguments. This is why a missing metric can be a selection, identity, scope or time-window problem rather than an analytical failure. [DS401] [DS407]

The mechanism ends with a tool response or an explicit error. Interpreting the response is subsequent work. Keep the source identity and observation interval with the response so that a later summary can be checked against the same measurement. [DS401] [DS407]

**Configuration and enablement**

1. **Registration.** Capability Providers → MCP Server → Register; provide HTTPS endpoint and supported authentication. Applies to: Account-level registration.
2. **Association.** Agent Space → Capabilities → MCP Servers → Add; select the registered provider and required tools. Applies to: Space-level tool selection.
3. **Custom execution.** Assign the actual tools to the custom definition. Applies to: Additional definition-level selection.

[DS401] [DS407]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Registered | Associate selected tools | Tools become available to the space, not necessarily every custom definition. |
| Associated | Remove connection | Future access through that association is removed. |
| Registered credential changes | Follow provider re-registration procedure | Review dependent associations before replacing the registration. |

[DS401] [DS407]

**Controls.** Network reachability, authentication, resource permissions and tool selection are separate gates. Use read credentials for this evidence path; mutating tools belong to the directed-action explanation.

**Observable output.** Provider/association configuration and an actual tool result or error; a connection-valid status alone does not prove the intended source query works.

**Not established by the reviewed sources.** The platform does not document a universal query planner, response-completeness guarantee or retry/deduplication contract for every connected tool.

**Proposed verification — not executed**

1. Use a permitted staging read with a known resource and time interval.
2. Reproduce one returned measurement with the same source query.
3. Select an unavailable operation or out-of-scope fixture; require an explicit gap, not a healthy result.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS401] | Registering an MCP server; Configuring MCP tools; Managing connections | Registration, association and tool selection are separate; removal and credential replacement have dependent-connection consequences. |
| [DS407] | How custom agents work | A custom agent accesses only its assigned tools. |

<!-- mechanism-review:end D-03 -->

### D-04 — Private network connections

A private integration requires a working route as well as valid credentials. The endpoint address identifies the service, whereas the private connection provides the network path to it. Authentication changes cannot repair a missing route or a blocked port.

AWS uses VPC Lattice and a service-managed resource gateway whose ENIs are placed in selected subnets. Traffic reaches the target from those ENIs, not from the public integration IP list. The private connection and the provider's endpoint URL are separate configuration objects. [DS05]

**Configuration procedure:** select a VPC, suitable subnets and security groups; specify a routable host and required port ranges; create the connection; associate it with the provider. For OAuth, account for both the MCP endpoint and token endpoint. On failure, inspect `failureMessage`, DNS, routing, port ranges and target-side rules before modifying credentials. The newer guidance states that omitted port ranges allow only 443. [DS05] [DS19]

**Illustrative configuration review:** an endpoint `https://metrics.example.internal:8443/mcp` needs a route and port range covering 8443. A successful HTTPS check on port 443 is not evidence that this endpoint works. A firewall rule should identify the selected gateway network path. It should not be copied from an unrelated public-service allowlist. This example is a review checklist, not a deployable AWS resource definition.



## 03. Knowledge and execution context

Current observations and retained information play different roles in a diagnosis. Discovery builds an environment model; learning produces memories; instructions and skills supply guidance. The following sections explain their producers and retrieval paths.



### D-05 — Resource discovery and topology construction

Topology is assembled from discovered resources and evidence of their relationships. It helps the agent connect a service to its deployment, repository, and dependencies. It is a representation of the environment, not the environment itself: an inferred edge can be wrong and an undiscovered resource can still be readable through an authorized tool.

Discovery collects CloudFormation resources and, for tagged resources outside CloudFormation deployments, uses enabled Resource Explorer. Relationship evidence can include configuration, tags, deployment mapping and observability. Learned topology/pipeline views summarize that evidence; raw-resource views expose different levels of granularity. A missing graph node does not prove the agent cannot investigate the resource. [DS04]

The managed Learning agent maintains environment knowledge. Its page provides knowledge, run history and scheduled-trigger inspection. Its schedules belong to the platform, unlike custom-agent triggers. Newer documentation moves learned topology, dependency, pipeline and tool-use knowledge into memory; older pages still call these learned skills. [DS06] [DS19]

**Engineering verification:** choose one service, identify its actual deployed resources and repository revision, and compare them with the graph. Record missing or incorrectly inferred edges separately. Inspect a learning run and the output's version after refresh; clicking a refresh control is not the completion evidence. Do not enable additional account writes to repair a read/discovery gap.



### D-M08 — Environment-knowledge consolidation and refresh

Knowledge consolidation is the step between collecting source material and retaining a useful explanation. In DevOps Agent, managed learning produces several kinds of environment knowledge: the application and resource model, code dependencies, pipeline relationships, and effective tool-use patterns. Those stores support different questions. A service map helps locate evidence, whereas a tool-use lesson helps construct an appropriate query. [DS06] [DS07] [DS19]

| Managed store | Retained subject | Operational use |
|---|---|---|
| `understanding-agent-space` | Logical services, components, request paths, source-to-resource relationships, and observability context | Orient an investigation or review a dependency description |
| `understanding-dependencies` | Service and package dependencies | Examine upstream/downstream relationships and change scope |
| `understanding-pipeline-topology` | Pipeline steps, environments, and promotions | Interpret a deployment or release context |
| `tool-use-best-practices` | Query patterns, recurring tool errors, and output-management guidance | Avoid previously observed invocation problems |

These are informational memories, not extra permissions or a replacement for the original systems. The memory guidance describes a browsable file structure: names can represent paths, and an index leads to relevant files. This arrangement supports progressive disclosure instead of placing the entire environment model into every task. [DS07]

![Environment-knowledge consolidation](../assets/diagrams/devops-knowledge.svg)

Refresh is not one universal timer. The environment understanding begins after discovery and can be regenerated when connected repositories, pipelines, or observability integrations change. The guidance separately describes scheduled refresh for active spaces, with account changes appearing on a scheduled refresh rather than immediately. Tool-use guidance is refreshed after enough new completed investigations and is rate-limited; monitor history follows its own daily rule. Consult the current thresholds in the memory guidance before assigning freshness expectations to an operational report. [DS07]

To inspect the result, follow the learning execution and examine the resulting memory version. The summary report is a versioned, read-only representation of the environment understanding; the topology visualizes its resource relationships. A successful connection or submitted regeneration request is not yet evidence that those views have incorporated the change. [DS04] [DS06] [DS07]

For example, after adding an inventory service, identify its deployed resources, repository, and critical request path. Compare them with the updated understanding and note any inferred or missing relationships. If a query repeatedly fails because it uses an obsolete namespace, inspect the relevant tool guidance as well as the source configuration. Correct the representation that is wrong rather than adding unrelated permissions.

A custom store serves a different authoring need. It can hold reviewed facts, service conventions, and reporting context supplied by the team. Give it a subject-specific description and keep each entry focused on information that remains useful across tasks. Raw tool output for one investigation belongs in that execution record; copying it into memory is not a documented same-run cache or a substitute for the original logs. Attach the store explicitly to a custom agent that needs it, then verify retrieval against a known fact. [DS07] [DS10]

<!-- mechanism-review:start D-M08 -->

#### MX-D-TOPOLOGY — Environment-knowledge construction and refresh

**Classification:** Knowledge-production mechanism. **Inputs:** Discovered resources, configuration and observability relationships, connected repository/pipeline context and completed operational work.

Environment learning turns source evidence into a retained representation. Discovery identifies resources; relationship analysis connects them; learned context describes services and request paths for later work. These products are derived information. They neither replace the deployed configuration nor widen the permission boundary. [DS403] [DS402]

Environment understanding, tool-use guidance and monitor history have different refresh conditions. The current memory guide is authoritative for those conditions; the older topology page still uses learned-skill terminology. Requesting regeneration is therefore followed by inspecting the learning result and its version, not by assuming that every dependent view has already changed. [DS403] [DS402]

**Configuration and enablement**

1. **Discovery.** Connect the relevant accounts and sources; enable Resource Explorer for its documented discovery path. Applies to: Resource and relationship inputs.
2. **Refresh.** Use Topology → Regenerate or request the supported update through Chat. Applies to: Managed learning request.
3. **Inspection.** Inspect the resulting environment memory and summary/topology representation. Applies to: Version and changed relationships.

[DS403] [DS402]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Source changed | Run applicable managed refresh | New derived understanding may be written. |
| Refresh requested | Observe completion and inspect a known changed relationship | Request acceptance is not completion. |
| Derived view stale | Correct source/discovery configuration and refresh | The graph is not repaired by granting unrelated write access. |

[DS403] [DS402]

**Controls.** Authorization belongs to account roles and tool access. A graph omission does not prove a resource is unreadable, and a graph edge does not prove source completeness.

**Observable output.** Updated context version and a reviewed topology/summary with known changed relationships.

**Not established by the reviewed sources.** No universal freshness SLA, complete relationship-detection algorithm or consistency guarantee across all derived views is documented.

**Proposed verification — not executed**

1. Identify a harmless staging dependency change with authoritative before/after evidence.
2. Find that change in the refreshed representation and record the version.
3. Leave an input unavailable; require the resulting missing or inferred relationship to remain qualified.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS403] | How topology graphs are created; Resource discovery; Investigation scope beyond topology | Discovery and relationship inference produce a representation that does not bound investigation permissions. |
| [DS402] | How memory is built and refreshed | Managed stores have distinct refresh conditions and can be inspected after regeneration. |

<!-- mechanism-review:end D-M08 -->

### D-M01 — Incident-memory construction and retrieval

Incident memory has a producer and a consumer. The producer synthesizes information from earlier work; the consumer is a later execution deciding which retained information is relevant. The managed monitors store records recurring-cause history for an alarm or metric, with evidence associated with earlier investigations. AWS describes a daily learning pass when the Agent Space has had investigations during the previous two weeks. Its retention and eviction behavior makes this a working operational memory, not an incident archive. [DS07]

At the beginning of a session, the agent receives store names and descriptions, rather than every stored file. It can select a relevant store, list its entries, evaluate their descriptions, and read the content it needs. A description is therefore part of the retrieval interface: an entry about inventory timeouts hidden behind an uninformative description may be available without being selected. The reviewed guidance describes progressive disclosure; it does not document a universal vector index, ranking algorithm, or customer-controlled model-training pipeline. [DS07]

Corrections provide a different input. Investigation feedback supplies the actual cause when a conclusion was wrong; the change guidance identifies reflections for that corrective context. The distinction is important operationally. Repeated appearances in history can establish a recurring theme, while a verified correction can explain why an earlier conclusion should not be repeated. Neither removes the need to read current telemetry. The feedback operation is described in D-M02. [DS08] [DS19]

To inspect the mechanism, open Knowledge, select Memories, and examine the relevant store and entry. Record its description, active state, version, and modification time. The monitor store is documented as enabled by default; individual availability still depends on activation, and custom-agent access additionally depends on attachment. The latter is configured in the custom-agent definition and is described in D-M07. [DS07] [DS10] [DS19]

For a recurring alarm, a useful response compares the previous cause with evidence from the new incident. In the worked example D-U01, healthy database metrics weaken the old database hypothesis while new upstream latency provides a different lead. A historical match should change where the investigation looks, not predetermine its conclusion.

There are also two meanings of recovery. Retrieving knowledge means making a relevant stored entry available to a current task. Restoring knowledge means recovering content after a change or loss. Versions allow inspection of earlier content and supported editing can create a corrected version; activation can make retained content available again. These controls are not evidence of an undocumented backup, undelete, or disaster-recovery service. Keep authoritative SOPs and configuration source in Git and keep incident evidence in its system of record. [DS07]

<!-- mechanism-review:start D-M01 -->

#### MX-D-RECALL — Selective incident-context retrieval

**Classification:** Knowledge-retrieval mechanism. **Inputs:** Current task; available store and entry descriptions; active memory content; applicable custom-agent store attachment.

Retrieval is a selection process, not automatic loading of all history. The agent first sees available store descriptions, then inspects a relevant store and selects entries before reading their content. A useful description exposes the subject and conditions under which an entry matters. A relevant fact hidden behind an unrelated description may never be read. [DS402]

Operationally, distinguish content production, availability to this execution, selection and diagnostic influence. A previous cause is contextual evidence for a new incident. Current measurements can contradict it. Viewing an old version is also different from restoring a deleted store; the current guide does not establish a general backup or undelete service. [DS402]

![Selective incident-context retrieval: state and control paths](../assets/diagrams/mechanism-devops-retrieval.svg)

**Configuration and enablement**

1. **Content.** Knowledge → Memories → select store → View entry; inspect description and version. Applies to: Stored informational context.
2. **Availability.** Inspect store and entry activation; inspect custom-agent attachments where applicable. Applies to: Access to retained material.
3. **Description maintenance.** Refine the store/entry description and retest a relevant request. Applies to: Retrieval metadata, not permissions.

[DS402]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Entry retained | Deactivate entry or store | Content remains but active retrieval is suppressed. |
| Entry edited | Save updated content | A new immutable version is created. |
| Custom store deleted in console | Confirm deletion | Store contents are removed; the documented deletion is not reversible. |

[DS402]

**Controls.** Keep raw incident evidence in its source system. Store access, relevance and answer correctness are separate; memory is not a same-investigation raw-tool cache.

**Observable output.** Entry content/version and, where exposed, a memory read in execution evidence. Output similarity alone does not establish retrieval.

**Not established by the reviewed sources.** Embedding model, ranking thresholds, hidden selection policy and model-weight training are not documented by this mechanism.

**Proposed verification — not executed**

1. Prepare a harmless known fact and a current observation that contradicts a historical cause.
2. Record existence, observable retrieval and supported conclusion separately.
3. Deactivate the entry or remove the applicable attachment and verify that unsupported historical claims are not asserted.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS402] | How memories work; Activating and deactivating; Deleting a memory store | Description-led retrieval, immutable versions and activation differ from irreversible custom-store deletion. |

<!-- mechanism-review:end D-M01 -->

### D-M02 — Investigation feedback and corrective memory

A correction becomes useful only when it identifies what the original investigation got wrong and supplies the verified alternative. That is a different input from simply collecting another similar incident. The feedback path records that distinction so later work can treat a prior conclusion as corrected context.

Corrective feedback is not the same producer as monitor-history synthesis. In a completed investigation, **Add feedback** records the verdict and, when wrong, the actual cause; Chat is another entry point. The most recent feedback submission replaces earlier feedback for that investigation. Sharing it with AWS requires separate confirmation. The dated change log describes a `reflections` store for lessons from corrections. [DS08] [DS19]

<!-- mechanism-review:start D-M02 -->

#### MX-D-FEEDBACK — Corrective investigation feedback

**Classification:** Corrective-context mechanism. **Inputs:** Completed investigation identifier, operator verdict and verified actual cause.

Feedback supplies a verified correction to a particular investigation. It is not the same input as another occurrence of the alarm and is not the same operation as steering an active investigation. The correction can produce reflection context explaining the discrepancy between the earlier diagnosis and the established cause. [DS404] [DS402]

The operator should preserve the evidence for the actual cause independently. Submitting feedback confirms an input was recorded; it does not prove that a later task selected the resulting context. Sharing the feedback with AWS is a separate confirmation decision. [DS404] [DS402]

**Configuration and enablement**

1. **Feedback.** Completed investigation → Add feedback; supply verdict and actual cause when incorrect, or use the documented Chat path. Applies to: Investigation-specific correction.
2. **Inspection.** Inspect saved feedback and any exposed reflection in Knowledge → Memories. Applies to: Correction versus derived context.
3. **External sharing.** Review the separate AWS-sharing confirmation. Applies to: Separate disclosure decision.

[DS404] [DS402]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Completed diagnosis | Submit correction | Feedback describes the verified alternative. |
| Feedback already present | Submit replacement | Inspect the saved latest feedback rather than assuming additive history. |
| Reflection available | Later relevant investigation reads it | Later use must be evaluated independently. |

[DS404] [DS402]

**Controls.** Do not infer production-change authority from a corrective message. Operator evidence, retained correction and optional external sharing are different records.

**Observable output.** Saved feedback and any visible corrective memory; later retrieval is an additional observation.

**Not established by the reviewed sources.** The exact latency from submission to reflection availability and a guaranteed recall rate are not established.

**Proposed verification — not executed**

1. Use a completed non-production example with a known corrected cause.
2. Confirm saved correction, then inspect later use only if the execution exposes it.
3. Supply a different current cause on recurrence; repeating the previous answer is not success.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS404] | Provide feedback on investigations | Feedback records the actual cause; latest feedback and separate sharing confirmation have distinct effects. |
| [DS402] | reflections | Corrective lessons are retained for future relevant investigations. |

<!-- mechanism-review:end D-M02 -->

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

The last two deletion behaviors and the description-selection model are documented in the newer indexed memory guidance. See the evidence notes for the older/newer-page discrepancy. [DS07]



### D-M03 — Global and agent-specific instructions

Some guidance belongs in every new session, such as the format of an incident finding or the conventions used to name services. Standing instructions provide that context at startup. They are appropriate for persistent behavioral guidance rather than a procedure relevant only to one symptom.

Global and agent-specific `AGENTS.md` text is supplied at startup; it is not selected by relevance. Changes apply to sessions started after saving. A running session retains its startup content. [DS09]

**Procedure:** open **Agents → Managed agents**, select the relevant agent, and edit the global or agent-specific instructions on **Agent definition**. Confirm the global change when prompted. Start a new session for verification. Older cached instructions pages show **Knowledge → Instructions**; the newer indexed guide and managed-agent page agree on the Agents route. [DS09] [DS06]

**Original example, not an AWS default:**

```markdown
## Incident reporting instructions
Identify the resource and UTC time range for every material observation.
Separate current observations from historical context.
When required data is unavailable, name the failed read and continue only
with conclusions supported by the remaining evidence.
```

Save this only where applicable. Check an old and a new session to test propagation. An instruction changes prompt context; it does not modify IAM authorization. Keep the authoritative text in Git, rather than retaining manual document snapshots.

<!-- mechanism-review:start D-M03 -->

#### MX-D-INSTRUCTIONS — Standing instruction loading

**Classification:** Session-initialization mechanism. **Inputs:** Saved global and applicable agent-specific AGENTS.md text and a newly starting session.

Standing instructions are loaded at session initialization. The service includes applicable global and agent-specific content without relying on task-relevance selection. Saving a change affects newly started sessions, not the content already loaded by an existing session. [DS405]

This makes instructions suitable for persistent reporting conventions. It does not make their content an IAM policy. Use an ordinary output convention as a propagation test and verify actual permissions separately. [DS405]

**Configuration and enablement**

1. **Scope.** Edit global or relevant managed-agent instructions using the instruction editor exposed by the operator app. Applies to: Applicable AGENTS.md content.
2. **Propagation.** Save, then start a new session. Applies to: Startup-loaded content.
3. **UI version.** Retrieved guidance shows both Knowledge → Instructions and Agents → Managed agents → Agent definition. Use the editor present in the deployed interface. Applies to: Navigation qualification.

[DS405]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Saved guidance | Start session | Applicable content is loaded. |
| Session active | Edit saved guidance | Active session retains its startup content. |
| Updated guidance | Start another session | New content becomes applicable. |

[DS405]

**Controls.** An instruction cannot grant a tool, change a trust policy or substitute for action approval.

**Observable output.** Saved instruction content and observable behavior in a newly started session.

**Not established by the reviewed sources.** Conflict precedence for contradictory global, agent-specific and task instructions is not fully specified; do not invent it.

**Proposed verification — not executed**

1. Add a harmless required heading to a scoped test instruction.
2. Compare a new session with one started before the change.
3. A denied tool must remain denied even when the instruction asks to use it.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS405] | How agent instructions work; Agent type scoping | Instructions are loaded at session start; existing sessions retain the original content. |

<!-- mechanism-review:end D-M03 -->

### D-M04 — Runbook skills and applicability rules

A runbook describes a procedure for a recognizable situation. A skill packages that procedure with an applicability description so an agent can select it when the task matches. Consolidating SOPs therefore starts with resolving contradictory or stale procedures, not merely concatenating documents into a larger prompt.

A skill requires `SKILL.md`; its name, description and agent-type targeting determine applicability. Additional references or data can accompany it. Without Sandbox, the supported material is non-executable; Sandbox adds a code-execution surface for applicable investigations. [DS11]

**Procedure:** add a skill from **Knowledge → Skills**, write a description naming the relevant symptoms and services, choose agent scope, and supply the procedure. Test a matching request and a nonmatching request. Inspect available run evidence for selection and tool use; document an unavailable signal as unverified rather than asserting selection.

**Original example:**

```markdown
---
name: checkout-upstream-timeout
description: Investigate checkout timeouts involving the inventory dependency.
---
```

Add a procedure that compares upstream response time, connection errors and deployment timestamps using the actually connected tools. Record failed reads and distinguish observations from hypotheses. The example frontmatter illustrates applicability; it is not a complete environment-specific runbook. A procedure cannot confer missing tool permissions.

<!-- mechanism-review:start D-M04 -->

#### MX-D-SKILL — Runbook applicability and procedural loading

**Classification:** Procedural-context mechanism. **Inputs:** SKILL.md, applicability description, agent-type targeting and any supporting files; actual tools required by the procedure.

A skill packages procedural guidance. Its description tells the built-in agent when to select it; targeting limits which agent types can use it. Assigned skills in a custom definition are loaded through that definition, so built-in relevance selection and explicit custom assignment should not be described as identical entry paths. [DS406] [DS407]

The procedure still depends on tools that exist and are authorized. Document-only skills do not create a shell. Executable content requires the separately configured Sandbox surface where supported. [DS406] [DS407]

**Configuration and enablement**

1. **Package.** Knowledge → Skills → add a skill with SKILL.md and a concrete applicability description. Applies to: Reusable procedure.
2. **Target.** Select relevant agent types or assign the skill to the custom definition. Applies to: Consumer scope.
3. **Tool dependencies.** Name real selected operations and expected observations. Applies to: External prerequisites.

[DS406] [DS407]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Skill available | Matching task or assigned custom invocation | Procedure becomes context. |
| Procedure updated | Run a new applicable test | Check the saved content and actual selection. |
| Skill disabled or unassigned | Start subsequent work | Do not assume the procedure remains available. |

[DS406] [DS407]

**Controls.** Skill text is guidance, not authorization; executable-code support is feature-specific.

**Observable output.** Saved skill configuration and exposed execution evidence of procedure/tool use.

**Not established by the reviewed sources.** Exact relevance thresholds and a universal selection trace are not guaranteed; unavailable observability remains unverified.

**Proposed verification — not executed**

1. Provide one request that matches the described symptom and another that does not.
2. Inspect exposed skill/tool-use evidence and the resulting procedure.
3. Remove a necessary tool; the task must report the blocked step rather than invent its observation.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS406] | Frontmatter; Creating Skills; Managing Skills | Description, target scope and supported content determine applicability. |
| [DS407] | How custom agents work | Custom definitions load assigned skill documents. |

<!-- mechanism-review:end D-M04 -->

## 04. Incident response and operational work

With access and context configured, a signal can be routed into an investigation or a defined operational task. This chapter follows execution, observation, and the additional controls required for computation or state-changing actions.



### D-06 — Incident triage, investigation, and prevention

![Workflow: Incident triage, investigation, and prevention](../assets/diagrams/devops-incident.svg)

The first operational decision is whether a signal needs new work. Correlation can attach it to an existing investigation, and configured criteria can exclude it. Only after that routing decision should the operator interpret the investigation itself. A correction to routing is consequently different from feedback on a root-cause conclusion.

An external signal is triaged before an independent investigation is necessarily started. **Linked** adds the signal to existing work; **Skipped** applies configured skip criteria; **Proceed** schedules new work. The web app shows the decision and reason. Unlinking or unskipping reschedules independent investigation; correlation or skip skills can be corrected for future events. [DS08]

For a manual investigation, supply the problem, optional starting evidence, incident time, name and priority. Inspect investigation output and tool evidence, then submit feedback after completion. A route decision, a diagnosis, and a feedback verdict are different records. [DS08]

**Engineering procedure:** for an unexpected absence of investigation, first inspect the triage record. A linked event is not lost; follow its primary investigation. A skipped event calls for reviewing the matching skill. For incorrect diagnosis, add the verified correction rather than changing a routing rule unless routing itself was wrong.

Prevention evaluations analyze multiple investigations into recommendations. The **Improvements** page exposes the latest evaluation summary, manual evaluation and schedule controls; the documented default is weekly. This differs from daily monitor-memory refresh. [DS15]

<!-- mechanism-review:start D-06 -->

#### MX-D-TRIAGE — Incident routing

**Classification:** Incident-routing mechanism. **Inputs:** Incoming external signal, active investigations and configured correlation/skip guidance.

Triage changes the relationship between a signal and investigation work. Linked signals contribute context to an existing investigation; skipped signals match exclusion criteria; proceed decisions schedule independent work. Routing is therefore not the root-cause result. [DS404]

Correct a bad relationship at the routing layer. Unlinking or unskipping reschedules independent investigation; changing a hypothesis inside the primary investigation does not repair the original routing decision. [DS404]

**Configuration and enablement**

1. **Signal path.** Connect a supported incident source or webhook and inspect the received event. Applies to: Incident initiation.
2. **Routing criteria.** Review the relevant correlation or skip skill. Applies to: Routing guidance.
3. **Correction.** Inspect the triage record and use supported unlink/unskip controls. Applies to: Signal relationship.

[DS404]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Received signal | Linked | Existing investigation receives signal context. |
| Received signal | Skipped | Reason is retained without a new investigation. |
| Received signal | Proceed | Independent investigation is scheduled. |
| Linked or skipped | Unlink or unskip | Independent work is rescheduled. |

[DS404]

**Controls.** Do not interpret a linked signal as missing work or a skipped signal as proof that the service is healthy.

**Observable output.** Triage outcome, reason and investigation linkage.

**Not established by the reviewed sources.** The exact correlation model and an absolute timing guarantee are not specified; a typical lookback is not a universal contract.

**Proposed verification — not executed**

1. Submit related and unrelated authorized test events.
2. Check linkage and reason against known service/time identity.
3. Deliberately review an incorrect skip criterion and verify the correction changes routing, not resource state.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS404] | Incident triage | Linked, Skipped and Proceed are routing outcomes; supported corrections reschedule independent work. |


#### MX-D-INVESTIGATE — Investigation and operator steering

**Classification:** Documented service workflow. **Inputs:** Incident description, start evidence, actual incident time, service scope and connected source access.

An investigation has its own scope and evidence record. The service gathers observations and develops an explanation; operator steering can add missing or contrary evidence within that record. This describes the observable workflow, not an undisclosed hypothesis-ranking algorithm. [DS404] [DS407]

Use the incident timestamp rather than the time the operator happened to open the form. Preserve observations that weaken the leading explanation. A revised analysis is useful only when the supporting evidence also changes. [DS404] [DS407]

**Configuration and enablement**

1. **Start.** Incident Response → start a manual investigation; review details, starting point, UTC incident time, name and priority. Applies to: Investigation identity.
2. **Steer.** Supply contrary observations within the active investigation. Applies to: Current execution context.
3. **Conclude.** Review findings and cause; request a mitigation proposal separately. Applies to: Analysis before effects.

[DS404] [DS407]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Investigation started | Read connected evidence | Observations and gaps accumulate. |
| Hypothesis present | Operator supplies contrary evidence | Analysis can be reconsidered in context. |
| Investigation completed | Review or submit feedback | Later correction is separate from active steering. |

[DS404] [DS407]

**Controls.** Steering is not approval for a resource mutation. Missing evidence constrains the conclusion.

**Observable output.** Investigation findings, source observations and any revised conclusion available in the service record.

**Not established by the reviewed sources.** No deterministic root-cause accuracy guarantee or complete inference algorithm is published.

**Proposed verification — not executed**

1. Use the repository recurring-alarm fixture as a tabletop, not as service telemetry.
2. Require the explanation to follow the current dependency measurements.
3. Remove the decisive observation; an inconclusive result is preferable to a fabricated cause.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS404] | Starting Investigations; Incident triage | Manual scope and operator context drive a separate investigation record. |
| [DS407] | Custom agents compared to built-in capabilities | Incident response is a built-in path, not a mandatory custom-agent task. |


#### MX-D-PREVENT — Cross-investigation prevention evaluation

**Classification:** Cross-investigation analysis workflow. **Inputs:** Recent investigation evidence, existing recommendation backlog and operator disposition feedback.

Prevention compares incidents to propose changes rather than diagnosing one current alarm. An evaluation produces or updates recommendations; backlog controls describe what the team intends to do with those recommendations. The action that implements a recommendation remains a separate change. [DS410]

A kept recommendation is not a deployed fix. A recommendation marked implemented is a tracking state, not independent proof of reduced incidents. Retain the implementation and post-change evidence in the normal change process. [DS410]

**Configuration and enablement**

1. **Evaluate.** Improvements → Run Now; inspect linked investigations and proposed effect. Applies to: Evaluation and recommendations.
2. **Control evaluation.** Pause recurring evaluation or Stop Evaluation for current work as appropriate. Applies to: Different scheduling/execution controls.
3. **Disposition.** Use Keep, Discard or Implemented and supply relevant explanation. Applies to: Backlog state.

[DS410]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Proposal | Keep | Retained backlog candidate. |
| Proposal | Discard with rationale | Removed from backlog; feedback informs later recommendations. |
| Accepted proposal | Mark Implemented | Tracking status changes; actual implementation must be verified. |

[DS410]

**Controls.** Priority and estimated effect do not authorize execution or measure realized improvement.

**Observable output.** Recommendation, supporting investigation references, disposition and observed changes.

**Not established by the reviewed sources.** Full ranking weights, exact feedback influence and causal benefit attribution are not specified.

**Proposed verification — not executed**

1. Review a candidate tied to several known investigations.
2. Trace the common weakness to its supporting evidence.
3. A change not deployed must not be reported as completed merely because the recommendation was kept.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS410] | Controlling evaluations; Managing recommendations | Evaluation control and recommendation disposition are separate; unretained recommendations may age out. |

<!-- mechanism-review:end D-06 -->

### D-07 — Custom-agent configuration and invocation

![Workflow: Custom-agent configuration and invocation](../assets/diagrams/devops-reporting.svg)

A custom agent is a saved definition of specialist work. Its system prompt states the task, its selected tools provide the evidence or actions it can use, and its skills and store attachments supply procedures and context. An invocation executes that definition once; a trigger arranges future invocations.

Define a name, system prompt, selected skills and memory stores. Use Chat for tool assignment and inspect the saved definition before executing. The available tool set is the selected subset of the space's integrations. [DS12]

**Execution procedure:** choose the agent, select **Run Now** or **Run with prompt**, then open the invocation in **History**. Inspect tool arguments and results, not only the final text. To schedule it, open **Triggers**, create a rate or cron expression, and check the displayed next run. `cron(0 9 ? * MON-FRI *)` is 09:00 UTC on weekdays, not automatically Zurich civil time. Pause the trigger to stop future starts. Cancel an existing run separately; an in-flight tool call may finish after cancellation. [DS13]

**Original system-prompt outline:** “Read the selected staging service's alarm and deployment tools for the previous 24 complete hours. Return resource IDs, the UTC window, failed reads and links to material results. Do not publish to external destinations.” This becomes usable only after real tool names and access have been selected. A schedule without those dependencies is not a reporting capability.

The CronSchedule API reference specifies a flexible scheduling window of up to 30 minutes for trigger-created custom-agent schedules. A cron expression anchors that window; it is not a guarantee of exact-minute start or completion. Keep telemetry resolution, report lookback window, trigger window, and execution duration separate. For a time-critical incident bulletin, use an explicit on-demand request or a separately engineered trigger path whose latency you test. [DS33]

<!-- mechanism-review:start D-07 -->

#### MX-D-CUSTOM — Configured custom-agent invocation

**Classification:** Definition-to-execution mechanism. **Inputs:** Custom definition with system prompt, selected tools, assigned skills and applicable memory access; optional per-run prompt.

A custom definition persists across executions. Run Now creates a new invocation; an additional prompt supplies context for that run without replacing the system prompt. The execution loads its configured resources, calls available tools and records results in a trajectory. [DS407] [DS408] [DS414]

A definition is not a running job. Likewise, an output artifact is not the invocation itself. Diagnose these objects separately when a report is missing: was an invocation created, did its tools complete, and was the requested output produced? [DS407] [DS408] [DS414]

![Configured custom-agent invocation: state and control paths](../assets/diagrams/mechanism-devops-cancellation.svg)

**Configuration and enablement**

1. **Define.** Agents → Custom Agents → Create agent; provide goal, approach, constraints and output. Applies to: Reusable definition.
2. **Select.** Assign actual tools through the supported configuration path and applicable skills/stores. Applies to: Scoped execution resources.
3. **Run.** Run Now or Run with prompt; open the invocation in History. Applies to: Independent execution.

[DS407] [DS408] [DS414]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Definition saved | Run Now | An invocation starts or is pending. |
| Invocation active | Cancel in trajectory or Chat | Completed evidence is retained; in-flight calls may still finish. |
| No invocation active | Invoke again | A new record is created; do not assume prior transient context is inherited. |

[DS407] [DS408] [DS414]

**Controls.** Only assigned tools are available. The documented execution page permits one invocation at a time per custom agent.

**Observable output.** Invocation identity, status, tool arguments/results/errors and requested output.

**Not established by the reviewed sources.** Exactly-once effects and universal rollback after cancellation are not documented.

**Proposed verification — not executed**

1. Create a harmless read-only report over a known staging signal.
2. Inspect the actual arguments and reconcile a figure in the output.
3. Cancel a controlled long read; distinguish cancellation from completion of an already-started external call.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS407] | How custom agents work | Prompt, selected tools and assigned skills are loaded per invocation. |
| [DS408] | Running; Canceling an invocation; Tool call results | Runs have history; cancellation preserves completed evidence and may not interrupt in-flight calls. |
| [DS414] | Creating a custom agent using the form | Creation and tool assignment are separate setup concerns. |


#### MX-D-SCHEDULE — Schedule-to-invocation creation

**Classification:** Trigger-to-execution mechanism. **Inputs:** Saved custom agent and valid rate/cron trigger; explicit reporting-window rules in task instructions.

A trigger schedules future invocation opportunities. It does not specify the observation interval used by a report. The API reference further qualifies the timing: custom-agent schedules use a flexible start window of up to 30 minutes. An expression therefore cannot be presented as an exact delivery deadline. [DS408] [DS409]

Pausing the trigger prevents subsequent starts but does not cancel a running invocation. These are two independent control operations and should be inspected separately when retiring recurring work. [DS408] [DS409]

**Configuration and enablement**

1. **Create.** Agents → selected custom agent → Triggers → create; enter a valid rate or cron expression. Applies to: Recurring trigger.
2. **Inspect.** Confirm saved expression, next run and actual start. Applies to: Timing evidence.
3. **Stop.** Pause/delete trigger and, if needed, cancel the current invocation separately. Applies to: Future versus current work.

[DS408] [DS409]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Trigger active | Schedule due | Eligible future invocation under timing/concurrency constraints. |
| Trigger active | Pause | Future starts disabled until resumed. |
| Trigger paused | Resume | Future schedule becomes active. |
| Trigger exists | Delete | Trigger is removed; existing execution evidence is separate. |

[DS408] [DS409]

**Controls.** Schedule variability, one-at-a-time custom execution and external-call completion are independent constraints.

**Observable output.** Trigger configuration plus actual invocation timing and observation interval.

**Not established by the reviewed sources.** Missed-occurrence, overlap queueing and exactly-once delivery behavior are not established by the cited schedule pages.

**Proposed verification — not executed**

1. Choose a non-time-critical test report and explicit UTC reporting period.
2. Compare due time, actual start and the period queried.
3. Run longer than the interval in an approved test and record actual behavior rather than assuming queued catch-up.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS408] | Scheduling custom agents; Managing triggers | Rate/cron triggers can be paused or deleted separately from invocations. |
| [DS409] | CronSchedule | The schedule anchors a flexible window of up to 30 minutes. |

<!-- mechanism-review:end D-07 -->

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

<!-- mechanism-review:start D-M06 -->

#### MX-D-ACTION — Operation-specific directed authorization

**Classification:** Effect-specific authorization mechanism. **Inputs:** Eligible exact operation and resource; Agent Space opt-in; target-account elevated role or selected classified tool; operator approval.

The requested effect passes several gates. Enabling directed actions opens the capability; the target role supplies a permission ceiling; the approval constrains the specific operation and resource. For AWS calls, the service uses scoped credentials and records attribution. None of these steps is replaced by a mitigation recommendation. [DS411]

External-tool classification is part of the control boundary. A tool marked read-only but implemented as mutating can defeat the intended approval path. Review classification against its real effects and permissions rather than its display name. [DS411]

**Configuration and enablement**

1. **Enable.** Agent Space settings: enable directed actions; preserve the full preferences map when updating through the API. Applies to: Primary opt-in.
2. **Authorize account.** Register the elevated role with documented trust including source-identity/session tagging support. Applies to: Permission ceiling.
3. **Review exact action.** Inspect target and parameters in Chat approval; reject or narrow as needed. Applies to: Specific execution grant.

[DS411]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Disabled | Enable and configure eligible access | Requests can reach the approval path. |
| Proposal awaiting decision | Approve exact operation | Scoped execution is permitted. |
| Approval granted | Different target or operation requested | Previous approval is not reusable. |
| Action executed | Inspect resource and service signals | Action success and recovery are separate observations. |

[DS411]

**Controls.** API preference replacement can reset omitted settings. IAM and service guardrails still apply after approval; tool effects require correct classification.

**Observable output.** Approval details, execution attribution and independently inspected resulting state.

**Not established by the reviewed sources.** No universal transactional rollback is documented; approved calls can have effects that outlive the conversation.

**Proposed verification — not executed**

1. Use an eligible reversible staging operation under narrow permissions.
2. Match approval, attribution and target state.
3. Request a different target or denied operation; it must not inherit the earlier approval.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS411] | Enabling; Registering elevated role; Categorizing tools; Approving directed actions | Independent opt-ins, operation-specific approval, preference replacement and classification govern mutation. |

<!-- mechanism-review:end D-M06 -->

### D-08 — Configuration APIs and update semantics

Programmatic configuration makes agent settings maintainable alongside other infrastructure definitions. It also requires attention to the resource being updated: changing asset metadata and replacing a preference map have different semantics. Reading the current state is therefore part of preparing a safe update.

Asset management uses the `devops-agent` CLI/SDK client but `aidevops:` IAM actions. `ListAssetTypes` discovers supported types; other asset operations generally authorize against the Agent Space ARN. Metadata keys use snake_case, while top-level request keys use camelCase. Metadata updates use PATCH semantics; asset type cannot be changed. Custom-agent skill/store references require asset IDs, not names. [DS17]

**Read-only inspection pattern:**

```bash
aws devops-agent list-asset-types --region "$AWS_REGION"
aws devops-agent list-assets --agent-space-id "$AGENT_SPACE_ID" --region "$AWS_REGION"
```

Set both variables to your approved environment; these commands were not executed here. Inspect returned metadata before changing it. Asset PATCH behavior must not be generalized to the replacement behavior of the directed-action preference map. For content upload/file operations and deployment templates, follow the type-specific official examples rather than constructing an undocumented payload. [DS17]



### D-09 — Remote access and release-assurance workflows

There are several directions of access around the service. An external client can call the agent, the agent can call an external tool, and an incident system can deliver a webhook. Release assurance adds another distinction between reviewing a proposed change and actively exercising a deployed application.

| Path | Caller → recipient | What it connects |
|---|---|---|
| External-tool MCP | DevOps Agent → your tool server | Tool/data access; D-03 |
| Remote service endpoint | Authorized client → DevOps Agent | MCP or agent-protocol access to service capabilities |
| Webhook | Incident system → Agent Space | Incident initiation |
| Asset/service APIs | Administrator or automation → AWS API | Configuration and supported service operations |

Each path has its own authentication and permissions. Connecting a tool server does not grant a client access to the agent. The access guide links the remote endpoint, webhook and API procedures. Their complete protocol setup is linked, not reproduced in this edition. [DS20]

Release testing interacts with a deployed application and can create, modify or delete application data. A test profile supplies reusable context; the execution produces evidence about that run. Treat it separately from code/readiness analysis. Use a disposable target and disabled external side effects before trying the preview. [DS21]

<!-- mechanism-review:start D-09 -->

#### MX-D-READINESS — Candidate release analysis

**Classification:** Preview analysis and verification workflow. **Inputs:** Candidate branch/commit and connected repository context; optional managed verification environment.

Readiness analysis examines a proposed code change. Optional verification builds and exercises the code in a managed environment; it is not a test of whichever production revision happens to be running. A report must therefore identify the candidate and whether verification actually ran. [DS412] [DS415]

Insufficient data or permissions are unresolved outcomes, not favorable release decisions. Automated triggers and verification are independently configured, so the presence of a review does not prove that a build/test environment was used. [DS412] [DS415]

**Configuration and enablement**

1. **Eligibility.** Check current release-management Region and repository support. Applies to: Feature-specific preview boundary.
2. **Repository settings.** Configure change-review triggering and automatic verification independently. Applies to: Two separate options.
3. **Private verification.** Select a verification environment with the required private route and runtime role when needed. Applies to: Build dependencies, not unrestricted network access.

[DS412] [DS415]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Candidate selected | Start review | Analysis record is associated with the candidate. |
| Verification enabled | Build and execute tests | Test evidence is added when execution succeeds. |
| Access or context missing | Review reports gaps | Resolve the prerequisite and rerun; do not interpret as clean review. |

[DS412] [DS415]

**Controls.** Code verification and active deployed-application testing have different subjects and effects.

**Observable output.** Readiness report, candidate identity, findings and any Tests-tab results.

**Not established by the reviewed sources.** Exact risk-scoring thresholds and guaranteed test coverage are not published; feature availability must be checked.

**Proposed verification — not executed**

1. Use a non-production candidate with one known behavior change.
2. Compare findings and executed tests with that revision.
3. Omit a required build dependency and require an incomplete or failed verification, not a pass.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS412] | Getting started; Performing a code review; Automatic verification testing | Review and verification settings are independent; candidate and verification results are inspectable. |
| [DS415] | Feature availability by Region | Release-management eligibility differs from production operations. |


#### MX-D-TEST — Active deployed-application testing

**Classification:** Preview active-test workflow. **Inputs:** Test profile, deployed URL, UI/API type, test intent and authorized disposable application data.

Release testing generates a plan from change context or a stated intent and exercises a running application. Its requests can modify data. The relevant identity is therefore the deployed target and its test account, not just the repository branch. [DS413] [DS415]

Inspect the actual interactions and results. A generated plan is not executed coverage. This guide uses the documented profile and web-app path rather than copying inconsistent action names from different parts of the retrieved pipeline example. [DS413] [DS415]

**Configuration and enablement**

1. **Profile.** Release Manager → Test profiles → Add test profile: name, target URL and UI/API type. Applies to: Saved target definition.
2. **Execution.** Start testing and provide a bounded test intent. Applies to: Active run.
3. **Environment.** Use disposable staging data and suppress unintended downstream effects. Applies to: Team safety prerequisite.

[DS413] [DS415]

**Lifecycle and state changes**

The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.

| Starting condition | Operation or event | Consequence |
|---|---|---|
| Profile saved | Start testing | Plan generation and active requests begin. |
| Requests executed | Review results | Failures, reproductions and observed behavior become available. |
| Unexpected effect observed | Stop further authorized test activity and inspect target | No automatic undo of prior requests is asserted. |

[DS413] [DS415]

**Controls.** Infrastructure read permissions do not make application POST/PUT/DELETE requests harmless.

**Observable output.** Test run, actual target, observed interactions and reproduction details.

**Not established by the reviewed sources.** The documentation does not promise exhaustive coverage or transactional rollback of application writes.

**Proposed verification — not executed**

1. Prepare a sandboxed checkout endpoint with synthetic records and disabled notifications.
2. Inspect expected request effects and one known validation error.
3. An unexpected payment/notification path ends the exercise; do not treat later cancellation as rollback.

The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.

**Official evidence for the product assertions**

| Reference | Reviewed section | Supported assertion |
|---|---|---|
| [DS413] | How release testing works; Defining test profiles; Reviewing results | Testing sends real requests including writes and reports observed results. |
| [DS415] | Feature availability by Region | Release testing is a feature-specific preview path. |

<!-- mechanism-review:end D-09 -->

## 05. Applying the model to operational outcomes

Trace the approved use cases through their concrete configuration and execution objects, then examine the prepared evidence. The examples remain synthetic, not live AWS results.



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



## 06. Troubleshooting and operating limits

Failures can occur before analysis begins: identity, routing, tool selection, and quotas all matter. Diagnose the first failed prerequisite before changing the investigation hypothesis.



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



## 07. Documentation coverage

The references identify the documented behaviors used in this guide and the procedures that remain linked rather than reproduced.



### D-11 — Documentation coverage and references

The preceding chapters explain the resource model, integration setup, retained knowledge, and execution paths needed for day-to-day operation. The coverage table distinguishes procedures described here from subjects that remain linked reference material. In particular, a source link for a remote protocol or preview release feature is not a claim that its entire configuration has been reproduced or exercised.

The reference register identifies the official pages supporting product-specific statements. New integration and scheduling material and selected knowledge mechanisms were rechecked on 22 October 2026. Other retained explanations keep their existing sources and review boundaries. Authored diagrams show logical relationships; the worked incident and proposed acceptance checks are not records of live AWS execution.

| AWS subject | Treatment here | Deliberate boundary |
|---|---|---|
| Workspace, roles, topology | Configuration and diagnostic model | Exact organization IAM policy remains in official reference |
| MCP/private connectivity | Authentication decisions and operational sequence | No customer network topology assumed |
| Knowledge and learning | Producer, retrieval, feedback, activation, attachment, lifecycle | No claims about hidden ranking or model training |
| Managed/custom execution | Routing, manual runs, schedules, cancellation, observation | Not every external incident provider reproduced |
| Assets and directed actions | Distinct update semantics and authorization | Full SDK schemas and denial lists linked |
| Sandbox/release preview | Configuration and effect boundaries | Full release-profile authoring is deferred |
| Quotas | Selected day-to-day constraints | Complete current quota/Region tables remain authoritative |

**Source-version decisions:** older cached pages and newer indexed AWS content differed for instruction navigation, custom-store attachment and learned-knowledge storage. This edition uses the newer indexed managed-agent, memory, asset and dated-change guidance for those points. The Region table was not reproduced as a complete regional inventory. A retrieval date is not a claim that AWS published the page on that date.

#### Official sources and reviewed sections

- [DS01] Service/feature eligibility; Supported Regions and Feature availability.
- [DS02] Space creation; primary account and Web App roles; verification.
- [DS03] MCP requirements; registration, association, authentication, rotation and role-less validation. Newer indexed content used.
- [DS04] Topology views, discovery and scope beyond the graph.
- [DS05] Private gateway operation, firewall rules and connection verification.
- [DS06] Managed agents; Learning history and platform-owned triggers. Indexed content used.
- [DS07] Memory production, retrieval, versions, activation, custom-store deletion. Older HTML reconciled with newer indexed content.
- [DS08] Investigation initiation, triage decisions/corrections and feedback.
- [DS09] Instruction scoping and new-session behavior; newer indexed navigation used.
- [DS10] Custom-agent tool/store scope and invocation model. Newer indexed content used.
- [DS11] Skill applicability, format and authoring.
- [DS12] Custom-agent creation and store selection. Indexed content used.
- [DS13] Manual execution, schedules, cancellation and trajectories.
- [DS14] Sandbox execution, network defaults, configuration and preview limits.
- [DS15] Prevention evaluations and controls.
- [DS16] Directed-action enablement, preferences replacement, categories, approval and audit.
- [DS17] Asset operation/permission map, IDs and PATCH metadata. Newer indexed content used.
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

[DS50]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html

[DS51]: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssociateService.html

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
