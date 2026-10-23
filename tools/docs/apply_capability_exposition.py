"""One-time editorial migration. Frozen catalog and ER-model records are not written."""
from pathlib import Path
import hashlib
import json
import pprint
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from build import parse_source
from structure import CHAPTERS as OLD_CHAPTERS, DECK_CHAPTERS as OLD_DECK_CHAPTERS, TYPES, LABELS
from presentation import DECKS
BASELINE='d081eade643537905690c54c4968a2445489cf96'
FROZEN=('use-cases','mechanisms','features','profiles','aliases','resource-models')
before={n:hashlib.sha256((ROOT/f'catalog/{n}.json').read_bytes()).hexdigest() for n in FROZEN}
G={}
for p in ('devops','security','finops','architecture'):
    text=(ROOT/f'guides/{p}.md').read_text()
    text=re.sub(r'\n*<!-- mechanism-review:start [^>]+ -->.*?<!-- mechanism-review:end [^>]+ -->\n*','\n\n',text,flags=re.S)
    G[p]=parse_source(text)

def put(p,sid,title,body):
    G[p]['sections'][sid]={'id':sid,'title':title,'body':body.strip()}
    TYPES.setdefault(sid,'reference')

def ref(p,sid,path):
    base={'devops':'devopsagent','security':'securityagent','finops':'finops-agent'}[p]
    G[p]['refs'][sid]='https://docs.aws.amazon.com/'+base+'/latest/userguide/'+path+'.html'

for ident,path in {
'DS501':'working-with-devops-agent-managed-agents','DS502':'working-with-devops-agent-custom-agents-index',
'DS503':'custom-agents-executing-custom-agents','DS504':'about-aws-devops-agent-managing-assets',
'DS505':'about-aws-devops-agent-devops-agent-memories','DS506':'whats-new',
'DS507':'configuring-integrations-and-knowledge-connecting-remote-a2a-agents',
'DS508':'configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools',
'DS509':'accessing-devops-agent-connect-to-devops-agent-remote-servers',
'DS510':'configuring-integrations-and-knowledge-vended-logs-and-metrics',
'DS511':'about-aws-devops-agent-agent-instructions','DS512':'about-aws-devops-agent-devops-agent-skills',
'DS513':'custom-agents-managing-custom-agents','DS514':'configuring-integrations-and-knowledge-sandbox',
'DS515':'working-with-devops-agent-working-with-directed-actions'}.items():ref('devops',ident,path)
for ident,path in {'SS501':'understand-lifecycle','SS502':'how-it-works','SS503':'security-requirements',
'SS504':'provide-testing-credentials','SS505':'review-penetration-findings','SS506':'revalidate-findings',
'SS507':'data-protection','SS508':'customer-managed-keys'}.items():ref('security',ident,path)
for ident,path in {'FS501':'what-is','FS502':'creating-an-agent','FS503':'task-management',
'FS504':'context-files-and-memory','FS505':'data-protection','FS506':'agent-guardrail-control',
'FS507':'custom-cost-reporting','FS508':'cross-region-inference','FS509':'setting-up',
'FS510':'automated-anomaly-response'}.items():ref('finops',ident,path)

G['devops']['intro']='''# AWS DevOps Agent

Platform capabilities, configuration, and operating mechanisms

AWS DevOps Agent combines managed operational workflows with customer-configured agents, connected tools, and retained context. An Agent Space organizes access and configuration; an agent definition specifies behavior and available context; an invocation records one execution. These are different parts of the service. [DS501] [DS502] [DS504]

The chapters distinguish ten capability dimensions: workspace organization; agent definition; knowledge and behavioral context; invocation; integrations; network connectivity; execution and action control; managed workflows; interaction surfaces and outputs; and administration. The resource model explains how their objects relate. The separate use-case catalog applies those facilities to operational objectives.

**Reading conventions.** This chapter organization is editorial, not an AWS product hierarchy. Named facilities and behavior are linked to official guidance. DOC (blue), AWS (green), and EXT (orange) identify concept ownership in diagrams. Configuration advice and worked examples are labeled as team practice. No AWS execution is reported. Sources with differing retrieved representations are qualified in the source-review record.
'''
put('devops','D-01','Agent Spaces and AWS account scope','''An Agent Space is the configuration and access container for operational work. It associates the primary AWS account, optional secondary accounts, provider connections, and operator permissions. An investigation is work performed within that scope; creating an investigation does not create another Agent Space. [DS50] [DS56]

![Agent Space and provider relationships](../assets/diagrams/er-devops-scope.svg)

Multi-account access connects account-specific roles to the space. Secondary-account roles trust the service principal `aidevops.amazonaws.com` directly, with source-account and source-ARN conditions. The account-connection procedure also requires the documented `iam:PassRole` permission. The operator role and the roles used to inspect resources have different purposes; D-02 covers their configuration. [DS506] [DS19]

Provider registration and association are separate operations. Registration retains the provider endpoint and authentication configuration. Association selects that registration for an Agent Space. AWS documents multiple registrations of the same provider and multiple associations in one space. A team with two monitoring installations therefore does not need to describe them as two kinds of agent or two execution environments. [DS506]

The approved resource diagram is a logical view of these relationships. Its colors distinguish AWS resources from documentation concepts and external systems; its qualified multiplicities are not service quotas. The detailed entity definitions remain in the resource-model reference.''')
put('devops','D-13','Assets, identities, and configuration references','''The Asset API manages configuration and reference material inside an Agent Space. Its eight documented types are `skill`, `agents_md`, `attachment`, `custom_agent`, `memory_store`, `memory`, `test_profile`, and `feedback`. A trigger is a separate resource. These types identify what is stored; they are not eight agent types. [DS504]

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

An implementation recipe in the use-case catalog is authored setup guidance. It is not an additional AWS asset. In particular, it must not be confused with the native `test_profile` type above.''')
put('devops','D-15','AWS-managed agents','''AWS supplies managed agents for its built-in capabilities. The documented roster includes Chat, Incident triage, Incident RCA, Incident mitigation, Incident UI, Evaluation, Grader, Release testing, and Learning. Their responsibilities differ: Grader performs investigation Reviews, Incident UI generates investigation outputs, and Learning produces retained knowledge. The roster is not a set of customer-created custom agents. [DS501]

Open **Agents → Managed agents** and select a managed agent. **Agent definition** exposes global and agent-specific instructions; **Knowledge** exposes accessible knowledge. The system prompt, tool set, and skills of a managed agent remain platform-managed. The page does not provide an independent Run now control. [DS501]

The Learning agent additionally exposes **History** and **Triggers**. History identifies knowledge-production runs and their trajectories. Its scheduled tasks are platform-owned: they are not editable custom-agent schedules. The distinction matters when diagnosing stale knowledge: inspect the learning run and its inputs rather than creating a second custom schedule with the same name. [DS501]

Instructions are the supported customization point for managed behavior. Their loading mechanism is described in D-M03; it is separate from the managed agent's underlying system prompt.''')
put('devops','D-16','Custom-agent definitions and configuration','''A custom agent is a saved definition for customer-specified operational work. Its configuration determines the prompt, available tools, assigned procedures, and accessible informational context. A trigger determines when it runs; an invocation is the resulting execution. [DS502]

| Configuration element | What the customer selects | How it affects execution |
|---|---|---|
| System prompt | Markdown defining the objective, approach, and expected output | Loaded as the definition's instructions |
| Tools | Explicit operations from connected providers or custom MCP servers | The invocation uses the assigned tool set |
| Skills | Assigned instruction packages and supporting files | Their procedures are loaded for the invocation |
| Memory stores | Explicit store attachments | The agent can read attached stores and write to attached custom stores; managed stores are read-only to it |

A new custom agent starts without memory-store attachments. Connecting a provider to the Agent Space does not assign all its tools to every custom agent. Tool selection and store attachment are independent configuration decisions. [DS502]

Create or edit the definition on the custom-agent page, configure its prompt and referenced resources, then run a scoped invocation and inspect History. Configuration can also be managed as a `custom_agent` asset. A system prompt can be imported from a Markdown file in a supported GitHub repository and synchronized on demand. Synchronizing the prompt is not a continuous deployment of arbitrary repository changes. [DS504] [DS506] [DS513]

AWS also documents automatic continuation through a subagent when a long invocation approaches its context limit. The continuation receives the same tools and skills; no customer setting is required. This mechanism does not establish a customer-authored routing graph or permission to configure arbitrary inter-agent delegation. Invocation and cancellation are covered in D-07 and D-19. [DS502]''')
put('devops','D-M03','Standing instructions and session initialization','''Agent instructions are standing behavioral guidance stored as `AGENTS.md`. Global instructions apply across managed agents; agent-specific instructions apply to the selected managed agent. They are Markdown content, not a skill bundle with supporting files. [DS511]

The loading mechanism is unconditional session initialization: a new session receives the applicable global and agent-specific content. Editing the saved instructions affects subsequent sessions. A session already running retains the instructions with which it started. This differs from selecting a skill or memory according to relevance. [DS511]

Open **Agents → Managed agents → selected agent → Agent definition**. Edit the global or agent-specific instructions, save the change, and start a new session to observe its application. Changes to global instructions require confirmation because they affect more than one managed agent. The October 13 changelog records the move from the Knowledge page to these definition pages. [DS501] [DS506]

For example, a team can require an incident summary to state the resource identity and UTC measurement period. That is an output convention. Access to a resource still depends on the selected tool and its authorization; instruction text does not modify those controls.''')
put('devops','D-M04','Skills, applicability, and supporting files','''A skill packages a procedure in `SKILL.md`, optionally with reference or asset files. Its description states when the procedure is relevant, and agent-type targeting identifies eligible consumers. This is procedural context: it explains how to perform work, rather than retaining the result of an earlier investigation. [DS512] [DS504]

For managed agents, description matching determines whether the skill is relevant to the current task. An inactive skill is not loaded. Custom-agent definitions explicitly assign skill assets and load the assigned documents during invocation. These are different selection paths and should not be represented as unconditional loading of every skill in the space. [DS512] [DS502]

To author a skill, open **Knowledge → Skills**, supply `SKILL.md`, describe the circumstances in which it applies, and select the applicable agent types. Include required source operations in the procedure. A skill may specify supported tools through its metadata, but the surrounding tool integration and access controls still apply. Executable skill files require the supported Sandbox surface; storing code in an attachment does not create a runtime. [DS504] [DS514]

Repository import accepts a supported GitHub skill directory or `SKILL.md` source. On-demand synchronization replaces the imported content with the repository's current content. Review the repository revision before synchronization; the service does not describe this as continuous bidirectional editing. [DS506]''')
put('devops','D-M01','Memory construction and progressive retrieval','''A memory is retained informational content, represented as a Markdown file in a memory store. A store's description identifies its subject; an entry's description identifies the content within it. This structure supports selective retrieval rather than loading the entire store into every session. [DS505]

Retrieval proceeds from the available store names and descriptions. The agent selects a relevant store, lists its entries, and reads the files needed for the current task. Activation state and applicable agent access determine whether the content is available. Custom-agent attachments narrow that availability to the selected stores. The mechanism provides task context; it does not itself add a tool or train the model's weights. [DS505] [DS502]

![Incident-memory production and retrieval](../assets/diagrams/mechanism-devops-retrieval.svg)

The managed `monitors` store groups earlier causes by alarm or metric. When the Agent Space has investigations in the preceding two weeks, the documented learning process runs daily and synthesizes recent investigation evidence into these entries. Entries without updates for two weeks are removed; capacity pressure removes the oldest entry. Monitor memory is therefore bounded retained context, not the authoritative archive of every incident. [DS505]

Monitor memory is enabled by default. Inspect **Knowledge → Memories**, open the store and entry, and inspect its description, content, version, and activation state. A later investigation can use that content alongside current telemetry. Establishing that the entry exists, observing a read, and validating the resulting diagnosis are three separate checks. The worked example in D-U01 demonstrates a recurring alarm whose current cause differs from its earlier cause. [DS505] [DS506]''')
put('devops','D-M08','Managed knowledge production and refresh','''The Learning agent reviews the connected environment and past investigations and produces retained context for other agents. Its inputs include discovered topology, code dependencies, pipeline structure, and investigation history. Its output is synthesized knowledge rather than a copy of every tool response. [DS501] [DS505]

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

Knowledge production and retrieval are distinct. A completed learning run can update context without proving that a later investigation selected it. To examine stale understanding, inspect the relevant learning run, the retained entry, and the source material used to construct it. The topology and Summary report views described in D-05 are representations of this understanding; they are not separate memory-store types.''')
put('devops','D-M02','Corrective feedback and reflection memory','''Investigation feedback associates a verdict with a completed investigation and can provide the actual root cause when the diagnosis was wrong. It differs from steering a running investigation, which changes the current inquiry, and from monitor-history synthesis, which reviews prior occurrences. [DS08]

Submit the correction through **Add feedback** on the completed investigation or through the documented Chat route. Supply the corrected cause and the evidence that establishes it. The most recent submission replaces earlier feedback for that investigation. Sharing feedback with AWS requires a separate confirmation. [DS08]

AWS documents a `reflections` store for the lessons produced from corrective feedback. A subsequent relevant investigation may retrieve that retained context. The service guidance does not establish a guaranteed delay from submission to recall, so a saved correction and demonstrated later retrieval should not be reported as the same event. [DS506] [DS505]

The source incident record remains the place to retain the verified cause and supporting observations. Reflection memory supplies context to later work; it does not replace that record or establish that a repeated symptom has the same cause.''')
put('devops','D-17','Attachments and repository-backed authoring','''An attachment stores binary or text reference material, such as a diagram, log sample, or document. It is a reference asset. It becomes a skill only when authored as a supported procedural package, and it becomes memory only through a documented memory-writing or learning path. [DS504]

Repository-backed authoring supports different inputs. Skill import reads a directory or `SKILL.md` and its supported files. Custom-agent import reads a Markdown system prompt. Synchronization is an explicit pull of the repository's current content, not automatic two-way synchronization. [DS506]

Maintain the repository revision and the destination asset identity when updating either kind of content. For a skill, review procedural changes and referenced files. For a prompt, review the behavior and expected output. Re-run an applicable task after synchronization to inspect the saved configuration and its effect. These checks are a team procedure; the import feature itself does not validate operational correctness.''')
put('devops','D-07','On-demand invocation and scheduled triggers','''An invocation starts a custom-agent definition. From **Agents → selected custom agent**, choose **Run now**, or use **Run with prompt** to add invocation-specific context. Chat can also invoke an agent by name. The saved system prompt remains part of the definition; the extra prompt applies to that run. [DS503]

A schedule trigger starts future invocations. In the agent's **Triggers** tab, create a schedule using EventBridge-compatible `cron(...)` or `rate(...)` syntax. Inspect the saved expression, optional prompt, and next run information. Examples include `rate(1 hour)` and `cron(0 9 ? * MON-FRI *)`; the latter describes weekday starts at 09:00 UTC. [DS503]

Triggers can be paused, resumed, or deleted. These operations govern future starts. Cancellation of an existing invocation is a separate operation described in D-19. Observation interval, start time, and report-delivery time are also different: a scheduled report should state the period it queries rather than derive it silently from a delayed start. [DS503]

The detailed execution guide documents both schedule and webhook event triggers. Its custom-agent overview also contains schedule-only wording. This guide uses the detailed trigger procedure for invocation support and records that source discrepancy rather than treating the overview as an exhaustive list. D-18 describes event selection and payload handling. [DS503] [DS502]''')
put('devops','D-18','Webhook events, filtering, and payload projection','''An event trigger invokes a custom agent when an event arrives from a connected integration with an active webhook. The configured event source and filter determine whether to start an invocation and what event content to pass to it. This mechanism is separate from the managed incident-investigation path and from outbound lifecycle notifications. [DS503]

In **Agents → selected custom agent → Triggers**, create an **Event** trigger and choose an active webhook-enabled integration. Optionally enter a JMESPath expression. If no sources appear, check integration/webhook availability and the operator's `ListAssociations` and `ListWebhooks` permissions. [DS503]

| Expression result | Invocation behavior | Passed context |
|---|---|---|
| Null, false, empty string, empty array, or empty object | No invocation | None |
| Boolean true | Invoke | Original payload |
| Another truthy value | Invoke | Projected result |
| No expression | Invoke for each source event | Original payload |

The expression is limited to 4,096 characters; context supplied to the agent is truncated at 10,000 characters. `severity == 'critical'` filters by severity and passes the raw payload. `{sev: severity}` projects a field but does not filter on its value, because the resulting object contains a key. Validate against the actual integration payload rather than assuming common field names. [DS503]

An event trigger remains listed but does not run if its source integration or webhook is removed. The execution guide describes notices for unmatched events. Webhook authentication is a separate control: the changelog documents HMAC and API-key webhook options and credential rotation without changing the URL. [DS503] [DS506]''')
# Preserve the detailed integration inventory, adding omitted provider directions.
p=G['devops']['sections']['D-12']['body']
p=p.replace('| Incident coordination | ServiceNow, PagerDuty, Slack | Provider-specific incident initiation and communication | Configure each provider’s documented route and permitted destination |',
'''| Incident coordination | ServiceNow and PagerDuty | Provider-specific incident initiation and updates | Configure the incident route and destination |
| Collaboration | Slack and Microsoft Teams | Slack can support bidirectional private-channel conversations; Teams supplies one-way notifications | Enable the supported channel mode explicitly |
| AWS Support | AWS Support case creation | Open a case from an investigation with its context | Inspect the submitted case and support entitlement |''')
p += '''\n\nGrafana can query supported ClickHouse-backed data sources. This is functionality through the Grafana integration, not a separate native ClickHouse registration. Source-control support includes the documented GitHub enterprise variants and GitLab Self-Managed. Provider parity should be checked per operation: a registered repository connection does not establish that every provider supports the same event and write features. [DS506]\n\nGitHub registration can use the service's GitHub App, a customer-owned GitHub App, or a personal access token. A PAT-only registration does not supply webhook-based features such as automated code review. Choose the registration mode according to the required operations, not only whether a read succeeds. [DS506]'''
G['devops']['sections']['D-12']['body']=p
put('devops','D-20','Outbound A2A delegation','''Remote Agent-to-Agent (A2A) integration lets DevOps Agent call an external agent during an investigation or Chat. The external agent is a connected service, not a DevOps custom-agent definition. DevOps Agent discovers its interface through an agent card, invokes it through the supported protocol, and incorporates the returned result. [DS507]

Register **Capability Providers → Remote Agent** with the agent-card URL and supported authentication, then associate the registration with the intended Agent Space. The card supplies the remote interface and capability descriptions used for task selection. Authentication must work both when fetching the card and when invoking the agent. [DS507]

Private connectivity is documented for API key, bearer token, and OAuth client-credentials authentication, but not SigV4. This transport condition is specific to the A2A connection. It should not be copied from MCP configuration without checking the relevant provider guidance. [DS506]

AWS recommends read-only remote agents for investigation and gathering data. The external agent's own downstream access and effects require review: a connection to its endpoint does not transfer the DevOps Agent Space's IAM policies or approval model into that external system. [DS507]''')
put('devops','D-04','Private endpoints, routing, and DNS','''Private connectivity supplies a network path to a supported privately hosted integration. It is a transport capability, not an integration provider, and it does not place the entire DevOps Agent service inside the customer's VPC. [DS508]

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

For a shared VPC, follow the AWS RAM and self-managed connection procedure rather than selecting a service-managed gateway in the consumer account. The provider's supported authentication method also matters: a private A2A endpoint does not support all methods available for a public A2A endpoint. [DS506]''')
put('devops','D-19','Invocation state, trajectory, and continuation','''An invocation has its own execution state and trajectory. The trajectory records tool calls, returned results, and generated output. Use it to distinguish a failed source operation from a later interpretation of successfully retrieved data. Each individual custom agent supports only one invocation at a time. [DS503]

When a long invocation approaches its context limit, the documented continuation mechanism creates a subagent with the same tools and skills. This is automatic execution behavior. The guide does not infer a customer-configurable subagent graph, a new privilege grant, or additional customer-defined agent types from it. [DS502]

![Triggers and invocation cancellation](../assets/diagrams/mechanism-devops-cancellation.svg)

Cancel from the invocation trajectory or through Chat. Completed work remains in the trajectory, and tool calls already in progress may still finish. Pausing the trigger stops future starts; it does not cancel the running invocation. After either operation, inspect the relevant object and any external effect rather than assuming rollback. [DS503]

Failed tool results can lead the agent to retry, use another approach, or report a failure. The trajectory provides the evidence available for that invocation; it is not a guarantee that all upstream systems were reachable or all required observations were collected. [DS503]''')
put('devops','D-21','Investigation Reviews and conversational assistance','''Conversational assistance and investigation Reviews are managed product functions. Chat answers questions using connected environment context. It supports attachments and inline tables/charts, and the documented interface offers voice input and Smart, Balanced, or Fast model tiers. These are interaction and output capabilities, not additional knowledge-store types. [DS506]

A Review assesses a completed investigation and reports an overall helpful/not-helpful verdict with criterion-level results. The managed Grader agent performs this work. A Review is different from customer feedback that supplies a corrected root cause; the latter can feed reflection memory. [DS501] [DS506]

Within an investigation, live summaries and timeline messages support continuing the inquiry. The changelog also documents resuming completed work and forking from an agent or user message. A fork explores a separate inquiry while preserving the original investigation. These lifecycle operations are part of the managed investigation workflow rather than custom-agent creation. [DS506]''')
put('devops','D-22','Release-readiness review and release testing','''Release-readiness review examines a change, whereas release testing exercises a deployed application. These preview functions use different inputs and can have different permissions and effects. They belong to the managed workflow layer, not to the same category as a skill file or private connection. [DS60] [DS61]

| Function | Primary input | Configuration | Result |
|---|---|---|---|
| Release-readiness review | Repository change and relevant environment context | Supported repository integration, review settings, and applicable runtime roles | Review findings and supported verification results |
| Release UI testing | Deployed web endpoint and personas | Native UI test profile and credential references | Executed tests and results |
| Release API testing | Deployed API and its specification | Native API test profile, target, and credentials | Executed API tests and results |

Automated GitHub PR and GitLab MR review triggers are documented for private repositories. Public-repository reviews can be requested through supported interactive or remote workflows. Provider support for reading code does not itself enable automated change-review events. [DS506]

Native test profiles store endpoint, test type, personas, API specification where applicable, and secret references. The supplied source outline identifies TOTP and email-based UI authentication support; consult the linked release-testing procedure for the selected profile type and current availability. The reviewed product guide's preview scope must not be expanded to all Regions or all assessment interfaces. [DS504] [DS61]

Treat the code revision, deployed revision, test profile, and test result as separate identities. The approved release-readiness and release-test use cases retain distinct completion criteria.''')
put('devops','D-09','Console, web application, and inbound remote access','''The Management Console administers Agent Spaces, provider connections, access, and related settings. The operator web application provides Chat, investigations, managed/custom-agent pages, and operational views. Collaboration channels provide their documented interaction modes. These are ways to use the service, not execution environments owned by the customer. [DS18] [DS506]

Remote-server access allows IDEs, CLIs, or other clients to call DevOps Agent. The detailed setup guide documents dedicated MCP and A2A endpoints with scoped access tokens or SigV4 authentication. The overview also names ACP; do not infer the same endpoint or authentication procedure for every protocol from that overview alone. [DS509] [DS18]

| Direction | Caller | Target |
|---|---|---|
| Inbound remote access | External client | DevOps Agent's remote endpoint |
| Outbound MCP | DevOps Agent | Connected external tool server |
| Outbound A2A | DevOps Agent | Registered external agent |

Configure the relevant direction independently. For inbound access, select the remote endpoint and client authentication method and grant only the required scope. For outbound access, register the provider and associate it with the space. Reusing the term MCP for both paths does not make their credentials, operations, or permissions interchangeable. [DS509] [DS03] [DS507]''')
G['devops']['sections']['D-05']['title']='Topology, environment summaries, and export'
G['devops']['sections']['D-05']['body'] += '''\n\nThe topology interface includes application and pipeline views. Downloading PNG, JSON, or Mermaid exports the selected view. The Summary report is a versioned, read-only view derived from environment understanding and is available through the documented console and artifact surfaces. These outputs represent learned context; they are not independent knowledge-store types or access-control boundaries. [DS506]'''
put('devops','D-23','Artifacts, notifications, and outbound lifecycle events','''Custom agents can produce text, artifacts, and recommendations according to their instructions and assigned skills. Progress notifications can communicate intermediate findings through configured notification channels. Investigations and Chat also support the documented Markdown export; investigation PDF printing is an output operation, not a separate analysis capability. [DS502] [DS506]

Investigation and mitigation lifecycle events are delivered through EventBridge. A completion event can contain `summary_record_id`. The documented consumer procedure calls `ListJournalRecords` with the relevant event identifiers and locates that record in the returned journal data. Do not infer a Get-by-summary-ID operation from the presence of the identifier. [DS506]

These are outbound events: the service informs a downstream consumer that work changed state. A custom-agent webhook trigger is inbound: an external event starts work. Keep the source, destination, authentication, and resulting execution or notification record explicit for each direction.''')
G['devops']['sections']['D-08']['body'] += '''\n\n### Declarative management and file operations\n\n`AWS::DevOpsAgent::Asset` manages all eight asset types declaratively. `AWS::DevOpsAgent::Trigger` manages the documented schedule-trigger configuration. CDK constructs and Terraform `awscc` resources expose these types. Do not infer CloudFormation support for every event-trigger field merely because the UI can create that event trigger. [DS504] [DS506]\n\nCloudFormation owns an asset's complete metadata and file set. Per-file edits, content download, historical-version operations, and repository import/synchronization remain distinct Asset API operations. Plan which system owns the configuration: a later declarative deployment can replace content edited through another surface. [DS504]'''
# Nested Markdown headings must not be confused with canonical section headings.
G['devops']['sections']['D-08']['body']=G['devops']['sections']['D-08']['body'].replace('### Declarative management','#### Declarative management')
put('devops','D-24','Identity providers, credential maintenance, and service telemetry','''Operator access can use the documented OIDC identity-provider integrations, including Okta and Microsoft Entra ID. User/group assignment and revocation govern web-app access. These controls are separate from the AWS roles and external-provider credentials used by executions. [DS506]

Registered provider credentials can be rotated where the provider supports in-place updates, retaining associations. Webhook rotation retains the webhook URL. Multi-secret-header MCP registrations are an explicit exception to in-place update support. Authentication maintenance must therefore follow the provider-specific operation, not one assumed universal rotation API. [DS506]

CloudTrail records the documented asset operations, remote authentication activity, and directed-action attribution. Investigation timelines expose tool-call and safety-check information. Vended logs and CloudWatch metrics provide another inspection surface for the service's own operation. [DS506] [DS510]

| Metric | Accounting scope |
|---|---|
| `ConsumedOnDemandTime` | On-demand Chat sessions and custom-agent runs; measured in seconds |
| `ConsumedChatRequests` | Chat with investigation requests; not all on-demand Chat |
| `ConsumedInvestigationTime` | Investigation execution time |
| `ConsumedEvaluationTime` | Evaluation execution time |
| `TopologyCompletionCount` | Completion of topology processing |

Use the metric's documented dimensions and statistic when aggregating usage. A usage counter is not a measure of diagnostic correctness or incident resolution. [DS510]''')

# Other products use the same dimensions only where their own documentation provides a facility.
G['security']['intro']='''# AWS Security Agent

Application scope, assessment capabilities, and execution mechanisms

AWS Security Agent exposes application-scoped assessments and the configuration needed to supply source context, criteria, target access, and credentials. Penetration testing, code review, design review, and threat modeling have different configuration and execution lifecycles. They are managed product functions, not interchangeable customer-defined agents. [SS501] [SS502]

The guide separates workspace organization, assessment definition, context, invocation, provider integration, network access, execution controls, managed assessment workflows, outputs, and administration. The approved resource model introduces the objects; the use-case catalog explains their application to operational objectives.

**Reading conventions.** These capability dimensions are editorial. The DevOps custom-agent, skill, memory-store, and trigger types are not assumed to exist here. Official sources identify Security Agent's own facilities. DOC/AWS/EXT colors retain the approved ownership convention. Worked examples and verification instructions are team guidance, not executed assessments.
'''
put('security','S-12','Assessment definitions and customization','''The configurable unit is the selected assessment. A penetration-test definition specifies targets, credentials, and test parameters. Full-code review selects source material and review modes. Threat modeling selects source and scope documents. Design review creates a one-off assessment of the submitted documents. These are the product's exposed configuration choices; this guide does not substitute the DevOps custom-agent prompt/tool/store schema for them. [SS501]

| Configuration | Main customer choices |
|---|---|
| Penetration test | Application targets, network access, credentials, scope exclusions, and relevant context |
| Full-code review | Repository or supported source input, revision, and vulnerability/requirement review modes |
| Repository-event review | Supported event integration, review settings, and comment/remediation permission |
| Design review | Design documents and applicable organizational requirements |
| Threat model | Source code and/or scope documents describing the system to analyze |

A saved configuration is not a run. Changes to it govern subsequent work, while an earlier run retains its own findings. Design reviews use cloning rather than rerunning one reusable configuration. S-10 describes these resource relationships; S-04 covers execution. [SS501]''')
put('security','S-13','Finding-edit personalization','''Findings Personalization retains eligible operator edits and applies them to similar findings on later penetration-test runs. Its input is finding-review activity, not a code change. The learned preference can alter a finding's displayed attributes without changing the application under test. [SS505]

AWS describes learning from the most recent completed run when personalization was enabled at test start. For status edits, marking a finding `FALSE_POSITIVE` is the documented learnable signal. Other status transitions must not be treated as equivalent feedback. Inspect original values and the Personalization changes explanation when reviewing an affected finding. [SS505]

This is separate from Login Optimization: one reuses finding preferences; the other reuses successful authentication navigation. Disabling reuse or personalization does not itself repair the application or prove a finding no longer reproduces. Revalidation is the separate execution described in S-M05. [SS504] [SS505] [SS506]

![Login reuse and finding personalization](../assets/diagrams/mechanism-security-learning.svg)''')
put('security','S-14','Assessment invocation and repository events','''An assessment starts through the interface supported for that function. Reusable penetration-test, full-code-review, and threat-model configurations can be run on demand. A design review is submitted as an individual assessment; cloning creates a new assessment with reusable inputs rather than rerunning the same object. [SS501]

Connected repositories can invoke configured review behavior on supported change events. Repository authorization, selection by the Agent Space, and enabling review/comments are separate setup steps. The source revision and event identify the reviewed change. [SS501]

A CI/CD caller invokes the configured assessment through the documented integration. The service executes the assessment; the pipeline does not become its testing engine. Keep the assessment identifier and inspect the returned execution status before interpreting findings. Defining a release-blocking policy from those findings is a team decision, not an automatic consequence of connecting a repository. [SS502]

The reviewed resource lifecycle does not establish one generic trigger object shared by all assessment types. Use the function-specific invocation procedure and keep scheduled or repository-triggered behavior distinct from the saved assessment definition.''')
put('security','S-15','Private source access and application connectivity','''Source connectivity and target connectivity are separate paths. Reaching a private repository supplies source context. Reaching a private application permits the test runner to send requests to that application. Neither connection supplies application-login credentials. [SS30] [SS07]

For a private assessment target, configure the documented VPC access and the necessary subnets, routing, DNS resolution, security groups, and application allowlisting. For a self-hosted source provider, configure that provider's reachability and authentication independently. A successful source read therefore says nothing about whether the target is reachable. [SS07] [SS06]

The target list also has scope semantics. A supporting login or content endpoint may need access without becoming a test target. The Target, Accessible, and Out-of-scope rules in S-03 describe that distinction. Network troubleshooting should preserve the authorized test surface rather than remove exclusions to obtain a successful connection. [SS08]''')
put('security','S-16','Interfaces, findings, and assessment outputs','''The Management Console provides administrative configuration and access management. The operator web application is the working interface for assessments and findings. Repository comments and Jira issues are outputs in external systems, with their own permissions and lifecycle. [SS502] [SS30]

| Function | Reviewable output |
|---|---|
| Penetration testing | Run-specific findings and supporting validation evidence |
| Code review | Source findings associated with the analyzed revision; supported repository comments |
| Design review | Findings against the submitted design and applicable requirements |
| Threat modeling | System overview, trust boundaries, threats, and supporting evidence |
| Code remediation | A proposed source change through the supported provider path |
| Revalidation | A separate job linked to selected existing findings |

A generated remediation proposal is not a deployed revision. A repository comment is not a penetration-test execution. A linked Jira issue tracks work in another system. Preserve the originating assessment and finding identifiers across those surfaces. S-05 and S-11 provide the detailed result lifecycle. [SS501] [SS502]''')
# Keep reviewed assessment procedures, but integrate publication in the integration chapter.
G['security']['sections']['S-09']['body'] += '''\n\nPublishing a finding to Jira is a destination operation. The site registration supplies authorization, the Agent Space selects a project and allowed create/comment actions, and publication creates an external record. Removing an integration does not remove the already-created issue. This configuration is different from attaching a source repository for analysis. [SS415] [SS416] [SS417]'''
G['security']['sections']['S-05']['body'] += '''\n\nFinding edits can also supply input to the personalization mechanism described in S-13. Review the original and current values before interpreting a changed severity or status. A preferred classification and successful revalidation of a deployed repair are different observations. [SS505]'''

G['finops']['intro']='''# AWS FinOps Agent

Instance configuration, cost analysis, context, and automation

AWS FinOps Agent is documented as a preview service for cost inquiry, reporting, anomaly investigation, and interpretation of upstream recommendations. Its instance retains organizational context and contains task automations and destination connections. A conversation, a queued task, and an automation are different objects. [FS501] [FS502] [FS503]

This guide separates those configuration facilities from their mechanisms: contextual reuse, conversation compaction, scheduled task creation, anomaly-event matching, and publication authorization. It then describes the managed analytical functions and their outputs. The use-case catalog supplies the approved operational objectives rather than another list of platform features.

**Reading conventions.** The dimensions below organize documented FinOps facilities; they do not imply a DevOps-style custom-agent API, arbitrary MCP tool registry, or shared cross-service memory. Official sources support product behavior. DOC/AWS/EXT colors identify ownership. Financial examples use synthetic values; verification procedures are proposed, not live account results.
'''
put('finops','F-11','Instance configuration and task instructions','''The instance is configured with data access, operator access, retained context, and supported integration connections. These settings determine which sources can be read and where results can be published. Instructions supplied for a task or automation specify the work; they are not a documented custom-agent system-prompt asset with a customer-selected MCP tool list. [FS502] [FS509]

| Customer control | Configuration surface | Applies to |
|---|---|---|
| Data role | Instance setup and IAM policy | Authorized AWS source calls |
| Operator access | Operator role and user permissions | Use of the instance's web application |
| Uploaded instructions or mappings | Context files workspace | Reusable organizational context |
| Request or task instructions | Conversation or task creation | The selected analysis or report |
| Recurring/event instructions | Automation configuration | Work created by future matching occurrences |
| Publication destination | Agent connection | Selected Jira project or Slack channel |

Create the instance through the wizard, configure the two role paths, and test entry as the intended operator. Then exercise a small source query under the actual data role. The context and task chapters describe the remaining controls. This configuration model should be read on its own terms rather than populated with facilities available in another AWS service. [FS502] [FS509]''')
put('finops','F-12','Service access, storage location, and inference','''FinOps Agent accesses the AWS sources and supported collaboration services described in F-08. The source-service permissions and destination connection establish the available interfaces. The reviewed guide does not expose the DevOps private-tool resource-gateway configuration, so this chapter does not invent a VPC connection object for FinOps Agent. [FS501] [FS509]

During the documented preview, persistent agent data is stored in `us-east-1`. Bedrock inference can take place in other US Regions. Storage location and inference location are separate properties and must both be considered when evaluating organizational data-location requirements. [FS505] [FS508]

Review the permitted input content before uploading it. Anyone with access to the agent can see its context files. An account-to-owner mapping is reference data, not an integration credential; credential values belong in the provider's supported authorization configuration. [FS504]''')
put('finops','F-13','Queued execution and session runtime','''A direct question can be answered in the conversation. An explicit task request creates separately recorded work in the shared queue. Scheduled and event automations also create tasks. Queueing is the execution mechanism; the saved automation defines when and with which instructions that work is created. [FS503]

Persistent files and memory are separate from the ephemeral session runtime into which context is loaded. Instances do not share files, memory, or task queues. Session termination is therefore not the deletion operation for the persistent context. F-M07 describes object-specific removal and retention. [FS505]

Inspect task history for the requested source calls, results, and supported publication actions. Distinguish work that was not created, work waiting in the queue, analysis failure, and publication failure. These are diagnostic observations rather than an invented API status enumeration. [FS503]

Cancel current work through the supported control, and disable or remove the automation separately to prevent future work. Cancellation does not withdraw an external message that has already been published. [FS503] [FS505]''')
put('finops','F-14','Cost inquiry, anomaly investigation, and recommendation analysis','''The managed analytical functions consume different source-service results. Cost Explorer answers historical cost/usage, forecast, and commitment-coverage questions. Cost Anomaly Detection identifies a deviation for investigation. Cost Optimization Hub and Compute Optimizer supply optimization recommendations. CloudTrail records API activity that can help evaluate a possible explanation. [FS501]

| Analytical function | Result to interpret |
|---|---|
| Historical cost and usage | Amounts under specified dates, metric, filters, and dimensions |
| Forecast review | A source forecast with a stated horizon and assumptions |
| Commitment coverage | Coverage under the selected commitment type and eligible usage scope |
| Anomaly investigation | Reconciled cost drivers and evidence for candidate causes |
| Recommendation analysis | Upstream candidates and savings estimates interpreted against workload context |

These are supported analytical functions. A weekly cost report or a team optimization review is a use case that combines them with retained context, automation, or publication. Retrieving a savings estimate is not applying a resource change or measuring realized savings. [FS501] [FS06]

The causal inquiry starts after reconciling the numerical comparison. A matching CloudTrail event can support a hypothesis, but the query basis and workload evidence must establish how much of the movement it explains. F-M01 gives the source-query procedure, and F-U01 supplies the synthetic decomposition example.''')
put('finops','F-15','Conversation, task history, and artifact interfaces','''The web application exposes conversation, Tasks, Automations, Context files, and Artifacts as different working areas. A conversation supports immediate questions. Tasks expose separately executed work. Automations define future starts. Artifacts retain generated reports. The administrative console configures the instance and access. [FS502] [FS503] [FS504] [FS507]

Report artifacts can originate in a conversation or a task. A follow-up request can revise a report; preserve the period, metric, and source scope when the requested revision concerns only format. F-04 describes report generation and supported output forms. [FS507]

Jira and Slack are external publication surfaces, not a shared conversation store. Their permitted operations and approval rules differ. A completed source analysis and successful external publication should be inspected separately through the available task record and the destination. [FS506]''')

# Clarify the model's role without changing its definitions or introducing another taxonomy.
put('architecture','A-12','Capabilities, product features, and mechanisms','''The model relates operational objectives to documented implementation facilities. It is not the table of contents of every product guide. Organizing a book into one chapter per entity would put a network route, a prompt, a review result, and a use case at the same explanatory level.

A capability dimension groups a kind of customer control: workspace organization, definition, context, invocation, integrations, connectivity, execution, managed workflows, outputs, or administration. Within a dimension, a feature names a concrete service facility. A mechanism explains how that facility operates. The approved use cases remain separate descriptions of operational objectives. [AS01] [AS02] [AS03]

| Product facility | Mechanism to explain | Application in the existing catalog |
|---|---|---|
| DevOps memory stores | Description-led store/entry selection and retained-version lifecycle | Historical context during incident investigation |
| DevOps event trigger | Webhook event matching, JMESPath condition/projection, then invocation | Event-driven execution where the chosen implementation permits it |
| Security Login Optimization | Retain successful navigation and reuse it for subsequent authentication | Authenticated application assessment |
| Security requirement pack | Select applicable criteria during an eligible review | Design or source review against organizational requirements |
| FinOps automation | Match a schedule or supported anomaly event and create a task | Periodic reporting or anomaly investigation |
| FinOps conversation context | Summarize older messages near the context limit | Continued analysis within a conversation |

An implementation profile in the approved model means an authored grouping of configuration choices. In the reading edition it appears as configuration instructions for the relevant use case. It is not an AWS agent type or service resource. The native DevOps release-testing `test_profile` is a different, explicitly documented resource. The model and the catalog are retained unchanged; product explanations identify what AWS exposes and what the team supplies. [AS01]''')
# Resolve shared references to existing official sources rather than inventing placeholders.
if 'AS01' not in G['architecture']['refs']:
    G['architecture']['refs']['AS01']=G['devops']['refs']['DS502']
if 'AS02' not in G['architecture']['refs']:
    G['architecture']['refs']['AS02']=G['security']['refs']['SS501']
if 'AS03' not in G['architecture']['refs']:
    G['architecture']['refs']['AS03']=G['finops']['refs']['FS503']
G['architecture']['refs']['AS501']=G['devops']['refs']['DS503']
G['architecture']['refs']['AS502']=G['security']['refs']['SS504']
G['architecture']['refs']['AS503']=G['finops']['refs']['FS504']
G['architecture']['sections']['A-12']['body'] += '\n\nThe concrete retrieval, event-processing, authentication-reuse, and compaction behaviors are documented separately by their products; the table is an editorial comparison, not a shared implementation. [AS501] [AS502] [AS503]'


def chapter(slug,title,purpose,sections,appendix=False):
    d={'slug':slug,'title':title,'purpose':purpose,'sections':sections}
    if appendix:d['appendix']=True
    return d
C={}
C['devops']=[
chapter('workspace','Workspace and resource organization','Agent Spaces, AWS account connections, provider associations, and assets establish the objects available for configuration.',['D-01','D-13']),
chapter('definition','Agent definition and customization','Managed agents and custom-agent definitions expose different customization controls. Invocation is covered separately.',['D-15','D-16']),
chapter('knowledge','Knowledge and behavioral context management','Instructions, skills, memories, and attachments differ in purpose, production, loading, and lifecycle.',['D-M03','D-M04','D-M01','D-M08','D-M02','D-M07','D-17']),
chapter('invocation','Invocation and triggers','On-demand requests, schedules, and webhook events start work. Filtering decides whether to start an invocation and what payload it receives.',['D-07','D-18']),
chapter('integrations','External system integrations','Native providers, outbound MCP tools, and outbound A2A agents expose different external operations.',['D-12','D-03','D-20']),
chapter('network','Network connectivity','Private connections supply transport to endpoints; they are separate from provider identity and tool authorization.',['D-04']),
chapter('runtime','Execution runtime and action control','Invocations, continuation, Sandbox code execution, and directed actions have different runtime and control boundaries.',['D-19','D-M05','D-M06']),
chapter('managed-workflows','Built-in managed workflows','AWS-managed investigation, prevention, review, and release-assurance functions apply the platform facilities to defined work.',['D-06','D-21','D-22']),
chapter('interfaces','Interaction surfaces, outputs, and outbound events','Interfaces expose the service; artifacts and views represent its results; lifecycle events notify external consumers.',['D-09','D-05','D-23']),
chapter('administration','Administration, security, and automation','IAM and operator access, Asset APIs, infrastructure as code, credential maintenance, and service telemetry support administration.',['D-02','D-08','D-24','D-10']),
chapter('examples','Worked example and reference material','The approved operational objectives and prepared example remain separate from the platform-capability explanation.',['D-14','D-U01','D-11'],True)]
C['security']=[
chapter('workspace','Workspace and resource organization','Shared settings, application Agent Spaces, and assessment records have distinct scopes.',['S-01','S-10']),
chapter('definition','Assessment definition and customization','Assessment-specific settings select targets, sources, criteria, and effects; they are not custom-agent definitions.',['S-12']),
chapter('knowledge','Application knowledge and assessment criteria','Application context, requirements, retained login procedures, and finding preferences have distinct producers and consumers.',['S-M07','S-M03','S-M04','S-M02','S-13']),
chapter('invocation','Assessment invocation','Manual assessment requests, supported repository events, and pipeline callers initiate the appropriate function.',['S-14']),
chapter('integrations','External system integrations','Source-provider authorization, application-source selection, and publication permissions are separate settings.',['S-09']),
chapter('network','Network connectivity','Private source access and private application access are independent network paths.',['S-15']),
chapter('runtime','Execution and assessment controls','Target rules, credential resolution, and run state determine the scope and conditions of a dynamic assessment.',['S-03','S-M01','S-04']),
chapter('managed-workflows','Managed assessment and remediation workflows','Code/design review, threat modeling, finding handling, repair proposals, and revalidation produce different records.',['S-06','S-05','S-M05']),
chapter('interfaces','Interaction surfaces and outputs','Console administration, assessment workspaces, source comments, findings, and external issues are distinct surfaces.',['S-16']),
chapter('administration','Administration, security, and limits','User access, encryption identities, and execution limits require product-specific configuration.',['S-02','S-M06','S-07']),
chapter('examples','Worked example and reference material','Follow the approved finding workflow and inspect the prepared evidence without changing the use-case catalog.',['S-11','S-U01','S-08'],True)]
C['finops']=[
chapter('workspace','Workspace and resource organization','The agent instance, connections, conversations, automations, tasks, and artifacts have different identities.',['F-01','F-09']),
chapter('definition','Instance configuration and task definition','Instance settings control access and context; requests and automations define the work.',['F-11']),
chapter('knowledge','Organizational knowledge and conversation context','Uploaded files, retained preferences, and compaction are three different context mechanisms.',['F-M02','F-M03','F-M04']),
chapter('invocation','Task invocation and automation','Explicit requests, schedules, and supported anomaly events create work through different start conditions.',['F-03','F-M05']),
chapter('integrations','Data-source and collaboration integrations','AWS evidence sources and Jira/Slack destinations are configured for different operations.',['F-08','F-05']),
chapter('network','Service access and data location','The service's interfaces, persistent storage location, and inference geography are distinct properties.',['F-12']),
chapter('runtime','Execution runtime and publication control','Task queueing and session execution precede destination-specific publication controls.',['F-13','F-M06']),
chapter('managed-workflows','Managed analytical functions','Historical analysis, forecasting, coverage, anomaly inquiry, and recommendation analysis use different source results.',['F-14','F-M01']),
chapter('interfaces','Interaction surfaces and report artifacts','Conversations, task history, report generation, and external publication expose different outputs.',['F-15','F-04']),
chapter('administration','Administration, retention, and limits','Role permissions, retained-data operations, and failure diagnosis must be applied to the correct object.',['F-02','F-M07','F-06']),
chapter('examples','Worked example and reference material','The approved reporting and investigation cases are illustrated with a synthetic, reconcilable cost comparison.',['F-10','F-U01','F-07'],True)]
C['architecture']=[dict(c) for c in OLD_CHAPTERS['architecture']]
C['architecture'][0]=dict(C['architecture'][0],sections=['A-00','A-10','A-12','A-11','A-09','A-01','A-02'],purpose='Use the entity model to distinguish responsibilities, then compare the product capability dimensions. The model is not a product feature inventory.')

# Each prior section remains an addressable destination. Remove only schema-shaped generated blocks.
for product,g in G.items():
    expected=[sid for c in C[product] for sid in c['sections']]
    if len(expected)!=len(set(expected)) or set(expected)!=set(g['sections']):
        raise ValueError((product,'chapter membership',set(expected)^set(g['sections'])))
    blocks=[g['intro'].strip()]
    for i,c in enumerate(C[product],1):
        blocks.extend([f'## {i:02d}. '+c['title'],c['purpose']])
        for sid in c['sections']:
            s=g['sections'][sid]
            body=s['body'].strip()
            body=re.sub(r'\n{3,}','\n\n',body)
            blocks.extend(['### '+sid+' — '+s['title'],body])
    used=set(re.findall(r'\b[DSFA]S\d+\b','\n'.join(blocks)))
    missing=used-set(g['refs'])
    if missing:raise ValueError((product,'undefined sources',missing))
    definitions='\n'.join('['+r+']: '+g['refs'][r] for r in sorted(g['refs']))
    (ROOT/f'guides/{product}.md').write_text('\n\n'.join(blocks)+'\n\n'+definitions+'\n')

# The curriculum follows capability dimensions. Preserve existing useful figures, tables, and exercises.
# Move supplied exercise/reference material after the platform exposition.
def slide(title,refs,rows,message,seconds=180):
    return {'title':title,'refs':refs,'data':rows,'message':message,'seconds':seconds,'kind':'table'}
DECKS['devops']['slides'].extend([
slide('Managed agents and customer-defined agents',['D-15','D-16'],[['Control','Managed agent','Custom-agent definition'],['Lifecycle','Provided by AWS','Created and maintained by the customer'],['Behavior','Global and agent-specific instructions','Customer system prompt'],['Tools and skills','Platform-managed','Explicitly selected and assigned'],['Memory access','Applicable managed access','Explicit store attachments'],['Invocation','Managed workflow entry point','On demand, schedule, or webhook trigger']],'Agent definition specifies behavior and available resources. Trigger configuration specifies when the definition runs.'),
slide('Webhook triggers: condition and payload projection',['D-18'],[['Input or result','Service behavior'],['Active webhook integration','Available event source'],['False, null, or empty expression result','No invocation'],['Boolean true','Invocation receives the original payload'],['Another truthy result','Invocation receives the projected value'],['Limits','4,096-character expression; 10,000-character invocation context'],['Removed source','Trigger remains listed but cannot run']],'A JMESPath predicate selects an event. A projection also changes the context passed to the invocation. Neither is an outbound EventBridge notification.'),
slide('Outbound tools and remote-agent delegation',['D-03','D-20','D-09'],[['Path','Caller and target','Configuration'],['Outbound MCP','DevOps Agent calls a tool server','Provider authentication and selected tools'],['Outbound A2A','DevOps Agent calls an external agent','Agent-card endpoint and supported authentication'],['Inbound MCP/A2A','External client calls DevOps Agent','Remote-server endpoint and scoped caller credentials'],['Custom agent','Definition executes inside DevOps Agent','System prompt, assigned tools, skills, stores']],'Integration direction determines which endpoint, identity, and operation must be configured.'),
slide('Private connectivity: gateway, DNS, and endpoint routes',['D-04'],[['Property','Configuration consequence'],['VPC Lattice resource gateway','Private traffic arrives through gateway interfaces in selected subnets'],['Shared VPC','Use the documented self-managed connection arrangement'],['DNS','Select public or in-VPC resolution for the target hostname'],['Port ranges','Explicitly include nonstandard ports; omitted ranges allow 443'],['OAuth endpoint','Can use a different private route from the tool endpoint'],['Scope','Network transport does not relocate the agent service into the VPC']],'Provider authentication and private routing are configured independently.'),
slide('Asset APIs, declarative management, and audit',['D-08','D-24'],[['Facility','Supported role','Distinct operation'],['Asset API','Manage eight asset types','Triggers remain separate resources'],['CloudFormation Asset','Complete metadata and file set','Per-file edits and historical content operations remain API calls'],['CloudFormation Trigger','Documented scheduled starts','Do not infer event-trigger properties from UI support'],['CloudTrail','Attribution of documented service operations','Not a correctness score'],['CloudWatch usage metrics','Execution time and request counts','Accounting scopes differ by metric']],'The source of configuration and the audit of its use are separate administrative responsibilities.')])
DECKS['security']['slides'].append(slide('Assessment configuration rather than custom-agent configuration',['S-12','S-14'],[['Facility','Customer-controlled input'],['Penetration test','Targets, network path, credentials, and scope'],['Code review','Source revision and vulnerability/requirement settings'],['Design review','Documents for a one-off assessment'],['Threat model','Source and scope documents'],['Repository event','Selected integration and supported review settings']],'The reviewed Security Agent model exposes assessment-specific settings, not the DevOps custom-agent prompt, tool, and memory-store schema.'))
DECKS['finops']['slides'].append(slide('Instance settings, task instructions, and automations',['F-11','F-12'],[['Control','What it configures'],['Data role','Authorized AWS data-source operations'],['Operator access','Entry and web-application operations'],['Context files and memory','Organization-specific reference and retained preferences'],['Task request','Instructions for one separately recorded execution'],['Automation','Future task creation on schedule or supported event'],['Destination connection','Agent-specific Jira project or Slack channel']],'The instance exposes these facilities independently. A task instruction is not a DevOps custom-agent definition.'))

DC={}
for product,deck in DECKS.items():
    positions={sid:i for i,c in enumerate(C[product]) for sid in c['sections']}
    buckets={i:[] for i in range(len(C[product]))}
    for s in deck['slides']:
        # A diagram/table stays with its main technical reference, rather than with a generic record class.
        idx=positions[s['refs'][0]]
        buckets[idx].append(s)
    ordered=[];groups=[]
    for i,c in enumerate(C[product]):
        values=buckets[i]
        if not values:continue
        start=len(ordered);ordered.extend(values)
        groups.append((c['title'],list(range(start,len(ordered)))))
    deck['slides']=ordered
    DC[product]=groups
(HERE/'presentation.py').write_text('"""HTML presentation outlines, organized by product capability dimensions."""\nDECKS='+pprint.pformat(DECKS,width=105,sort_dicts=False)+'\n')
(HERE/'structure.py').write_text('"""Capability-oriented reading structure; does not redefine frozen entities or use cases."""\nREVISION="2026-10-23-capability-exposition"\nBASELINE="75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9"\nCHAPTERS='+pprint.pformat(C,width=105,sort_dicts=False)+'\nDECK_CHAPTERS='+pprint.pformat(DC,width=105,sort_dicts=False)+'\nTYPES='+repr(TYPES)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else TYPES.get(sid,"reference")\n')

# Do not regenerate exposition from the frozen, heterogeneous dependency registry.
build=HERE/'build.py';text=build.read_text()
text=text.replace('    mechanism_detail.sync_guides()\n','')
text=text.replace('renderer preserves authored prose and regenerates delimited mechanism-detail blocks from the registry.','renderer preserves authored capability explanations; frozen registries supply links, not chapter prose.')
build.write_text(text)

# Preserve identifier routes without presenting each registry row as an AWS mechanism or feature.
p=HERE/'reader.py';text=p.read_text()
text=text.replace("                subnav = '<ul>'+''.join('<li><a href=\"#'+m['id']+'\">'+esc(m['title'])+'</a></li>' for m in mechanisms)+'</ul>' if mechanisms else ''", "                subnav = ''")
old="                for heading in prose.select('h4[id^=\"MX-\"]'):\n                    heading.string = re.sub(r'^MX-[A-Z]-[A-Z]+\\s+[—-]\\s+','',heading.get_text())"
new="""                # Compatibility anchors resolve frozen workflow references to their technical explanation.
                # They are references, not declarations that every old registry label is a mechanism.
                for m in mechanisms:
                    node=prose.new_tag('span',id=m['id'])
                    node['class']='technical-reference-anchor'
                    node['aria-label']='Technical reference: '+section['title']
                    node.string=''
                    prose.insert(0,node)"""
if old not in text:raise ValueError('reader anchor patch not found')
text=text.replace(old,new)
# Replace feature-card repetition with references to the actual authored explanation and frozen resource model.
start=text.index('    def feature_detail(');end=text.index('    def guide(',start)
text=text[:start]+'''    def feature_detail(self, feature, current):
        product=self.model['products'][feature['platform']]
        entities={e['id']:e for e in product['entities']}
        ids=product['feature_bindings'][feature['id']]
        uses=[c for c in self.cases if any(feature['id'] in s['configuration_features'] for s in c['workflow'])]
        result='<details class="feature-reference" id="'+feature['id']+'"><summary>Resource and use-case references: '+esc(feature['title'])+'</summary>'
        result+='<p>Read the configuration explanation in '+ ' · '.join(self.section_link(s,current) for s in feature['sections'])+'.</p>'
        result+='<p>Resource definitions: '+' · '.join(anchor('catalog/resource-models.html#'+i,entities[i]['name'],current) for i in ids)+'</p>'
        if uses:result+='<p>Applicable use cases: '+' · '.join(self.link(c['id'],c['title'],current) for c in uses)+'</p>'
        return result+'</details>'

'''+text[end:]
text=text.replace("            nav_sections, content = [], []", "            nav_sections, content = [], []\n            display_number = 'A' if chapter.get('appendix') else f'{number:02d}'")
text=text.replace("str(number)+'.'+str(j)","display_number+'.'+str(j)")
text=text.replace("f'{number:02d}. '+esc(chapter['title'])", "display_number+'. '+esc(chapter['title'])")
text=text.replace("<p class=\"chapter-label\">Chapter '+f'{number:02d}'", "<p class=\"chapter-label\">'+('Appendix' if chapter.get('appendix') else 'Chapter '+f'{number:02d}')")
p.write_text(text)
# Anchors occupy a small scroll target; they are not extra headings or content cards.
p=HERE/'reading.css';p.write_text(p.read_text()+'\n.technical-reference-anchor{display:block;min-height:1px;scroll-margin-top:5rem}.report-section>h3{margin-bottom:1rem}\n')

p=HERE/'mechanism_detail.py';text=p.read_text()
text=text.replace("if not node or node.name!='h4':errors.append(e['id']+': detailed guide anchor missing')", "if not node or not node.find_parent(class_='report-section'):errors.append(e['id']+': technical reference destination missing')")
# Remove obsolete prose renderers. Keep the frozen-register validation and source records.
for a,b in [('def markdown_table(', 'def load(')]:
    pass
for name,next_name in [('markdown_table','block'),('block','section_boundaries'),('section_boundaries','sync_guides'),('sync_guides','index_summary'),('index_summary','source_record')]:
    start=text.find('def '+name+'(');end=text.find('def '+next_name+'(',start+1)
    if start>=0 and end>start:text=text[:start]+text[end:]
p.write_text(text)

# Audit source basis and retain all frozen records byte-for-byte.
review={'date':'2026-10-23','baseline':BASELINE,
 'basis':'User-supplied ten-part capability outline; retained guide procedures; targeted official-documentation corroboration.',
 'scope':'Platform exposition and chapter/curriculum composition. Entity model and use-case semantics remain frozen.',
 'frozen_sources':{n:hashlib.sha256((ROOT/f'catalog/{n}.json').read_bytes()).hexdigest()==before[n] for n in FROZEN},
 'conceptual_corrections':[
 'Capabilities organize customer controls; they are not outcome labels.',
 'Concrete product facilities are described within capability dimensions, not a homogeneous feature-record index.',
 'Mechanisms describe selection, loading, event evaluation, routing, continuation, or lifecycle behavior; assessment and reporting remain functions/workflows.',
 'Implementation profiles are authored configuration recipes, not native platform resources; native release test profiles remain distinct.',
 'Provider integration, network transport, inbound invocation, and outbound event delivery are separate dimensions.',
 'Frozen dependency registers are retained for identifiers and relationships, not rendered as an authoritative product taxonomy.'],
 'official_rechecks':[
 {'url':G['devops']['refs']['DS503'],'supports':'Event and schedule triggers; JMESPath predicate/projection; context limits; invocation concurrency and cancellation','qualification':'The directly retrieved representation was schedule-only; the indexed detailed page includes event triggers.'},
 {'url':G['devops']['refs']['DS502'],'supports':'Explicit tool/skill/store selection and automatic continuation subagents','qualification':'Overview retains schedule-only wording; use execution procedure for trigger coverage.'},
 {'url':G['devops']['refs']['DS501'],'supports':'Managed roster, editable instructions, Learning history and platform-owned triggers'},
 {'url':G['devops']['refs']['DS504'],'supports':'Eight asset types, CloudFormation support, API and declarative distinctions','qualification':'Directly retrieved representation lists six types; indexed page and dated change log include memory types.'},
 {'url':G['devops']['refs']['DS506'],'supports':'Dated additions including Teams, OIDC administration, source import, shared-VPC routing, knowledge conversion, outputs, and metrics','qualification':'The indexed changelog contains October entries; the direct representation ended in July. No relative age is inferred solely from retrieval order.'},
 {'url':G['security']['refs']['SS501'],'supports':'Assessment-specific resource and execution lifecycles'},
 {'url':G['security']['refs']['SS504'],'supports':'Credential resolution and retained login procedure'},
 {'url':G['finops']['refs']['FS503'],'supports':'Conversation versus task; schedule/event creation; approval by invocation type'},
 {'url':G['finops']['refs']['FS504'],'supports':'Files, memory, and compaction have different loading and lifecycle behavior'}],
 'boundary':'No live AWS execution; retained statements keep their previous sources. The supplied document governs structure, not a claim that AWS publishes this taxonomy.'}
if not all(review['frozen_sources'].values()):raise ValueError('Frozen source changed')
(ROOT/'qa/exposition-review.json').write_text(json.dumps(review,indent=2)+'\n')
p=ROOT/'EDITORIAL_STANDARD.md';p.write_text(p.read_text()+'''\n## Capability exposition\n\nThe approved entity model is a semantic reference, not a chapter template. Organize platform explanation by the exposed configuration dimensions: scope, definition, context, invocation, integration, connectivity, execution, managed functions, interfaces/outputs, and administration. A feature names a concrete product facility; a mechanism explains its operation. Do not render every dependency-register row as an equivalent mechanism or feature. Implementation recipes remain team-authored setup instructions within use cases; distinguish them from native test-profile resources.\n\nGuide prose is authored in Markdown. Frozen registry records provide relationships and compatibility identifiers, not automatic chapter prose. The supplied DevOps outline is the editorial basis; other product guides use only their documented facilities rather than inheriting DevOps resource types.\n''')
p=ROOT/'CHANGELOG.md';p.write_text(p.read_text()+'\n## 2026-10-23 — Capability exposition\n\nReorganized product guides by capability dimension using the supplied DevOps outline. Removed automatic registry-shaped prose, retained frozen model/use-case sources, added omitted DevOps facilities and explicit source-version qualifications, and aligned the HTML curriculum with the revised books.\n')
Path(__file__).unlink()
print(json.dumps({'frozen_sources_unchanged':True,'guide_sections':{p:len(g['sections']) for p,g in G.items()},'primary_capability_chapters':10,'appendix_separate':True}))
