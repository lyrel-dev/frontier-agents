# AWS DevOps Agent — configuration and operation

Engineering guide • documentation reviewed 22 October 2026

This guide explains the platform from its resources upward: access and connectivity, context, execution, operating procedures, and failure diagnosis. Product behavior is supported by the numbered AWS references. Sections explicitly labeled **engineering procedure** or **synthetic exercise** are recommendations or teaching examples, not additional AWS features. No account configuration or live agent execution was performed for this publication.

## 01. Product Functions and Resource Model

Define the built-in functions, configuration objects and execution records before applying them to operational work.

### D-01 — Service functions and resource model

The built-in functions are incident investigation, on-demand operational questions, and incident-prevention recommendations. Release-readiness review and release testing are separate preview paths. Custom agents execute operator-defined work; a scheduled health report is an application of that facility, not another independent platform primitive. Availability is feature- and Region-specific. Consult the Region table rather than assuming that the Region of a monitored workload determines where the Agent Space must reside. [DS01] [DS15] [DS18]

The configuration has two levels. An account registers providers; an Agent Space associates accounts and providers and selects available tools. Within that space, knowledge resources and agent definitions govern the context available to executions. An investigation or custom-agent invocation is a run, not the configuration that produced it. [DS02] [DS03] [DS10]

```text
Account / Region
  Capability provider registration ── association + selected tools ──┐
  Primary / secondary AWS account roles ────────────────────────────┤
                                                                  ▼
Agent Space ── operator access ── people / authorized clients
  ├─ discovered resources → topology and environment understanding
  ├─ instructions / skills / memory stores
  ├─ managed agents → investigations / chat / evaluations
  └─ custom-agent definition → trigger → invocation → tool results
```

The graph is an explanatory model of documented resources, not an AWS API schema. Topology helps investigations navigate relationships; it does not constrain all possible reads. IAM permissions and integration authorization determine what resources can actually be accessed. [DS04]

#### Reusable capabilities, grouped by responsibility

| Group | Capability | Configurable or inspectable objects | Detailed treatment |
|---|---|---|---|
| Access | Scope AWS and operator access independently | Resource role; operator role; account association | D-02 |
| Connectivity | Make selected external tools reachable and callable | Provider; authentication; private connection; tool selection | D-03, D-04 |
| Context | Discover resources and infer relationships | Discovery results; topology; learned understanding | D-05 |
| Context | Retain and retrieve environment-specific information | Store; memory; description; version; active state | D-M01, D-M02 |
| Behavior | Supply standing guidance and specialized procedures | Agent instructions; skill and its applicability | D-M03, D-M04 |
| Execution | Route incident signals and accept steering | Triage decision; investigation; feedback | D-06 |
| Execution | Define and schedule bounded operational work | Custom agent; assigned tools; trigger; invocation | D-07 |
| Execution | Run investigation-local computation | Sandbox packages and network policy | D-M05 |
| Effects | Authorize particular mutations | Elevated role; tool category; approval | D-M06 |
| Administration | Manage configuration through APIs | Asset type, ID, metadata, files, versions | D-08 |
| Observation | Inspect executions and generated outputs | Investigation details; invocation trajectory; audit events | D-06, D-07, D-M06 |

This table is an index, not a second capability database. The referenced sections are the canonical explanations.

## 02. Access Roles and Tool Connections

Configure operator access, AWS resource access, external tools and private network paths.

### D-02 — Establish the two access paths

**Administrator procedure.** In the AWS console, create an Agent Space, give it a name, and configure primary-account resource access. Select an automatically created role, an existing role, or the policy-template route for customized permissions. Configure the Web App role separately, then create the space. The expected confirmation is an **Operator access** button that opens an authenticated web application. Creating a space successfully is not confirmation that a particular telemetry API is readable. [DS02]

| Decision | Resource-access path | Operator-access path |
|---|---|---|
| Purpose | Allow the service to inspect authorized AWS resources | Allow personnel to interact with the space |
| Review | Target accounts, actions, resource scope and trust | Which users can enter and what operations they can perform |
| Proposed test | Read one known non-sensitive resource and inspect its identity | Sign in as the intended operator, not only the setup administrator |
| Failure interpretation | Missing data can be an API or role problem | An unavailable app can be an identity/access problem |

**Engineering procedure:** record the space ID, Region, role ARNs and one tested resource. Keep policy source in Git. Do not publish account secrets or copy broad policy examples without adapting their resource scope. For secondary-account trust and exact IAM statements, use the linked current AWS procedure; this guide does not invent a universal trust policy. [DS19]

### D-03 — Connect an external MCP tool provider

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

### D-04 — Private connectivity is a network mechanism

AWS uses VPC Lattice and a service-managed resource gateway whose ENIs are placed in selected subnets. Traffic reaches the target from those ENIs, not from the public integration IP list. The private connection and the provider's endpoint URL are separate configuration objects. [DS05]

**Configuration procedure:** select a VPC, suitable subnets and security groups; specify a routable host and required port ranges; create the connection; associate it with the provider. For OAuth, account for both the MCP endpoint and token endpoint. On failure, inspect `failureMessage`, DNS, routing, port ranges and target-side rules before modifying credentials. The newer guidance states that omitted port ranges allow only 443. [DS05] [DS19]

**Illustrative configuration review:** an endpoint `https://metrics.example.internal:8443/mcp` needs a route and port range covering 8443. A successful HTTPS check on port 443 is not evidence that this endpoint works. A firewall rule should identify the selected gateway network path. It should not be copied from an unrelated public-service allowlist. This example is a review checklist, not a deployable AWS resource definition.

## 03. Knowledge, Memory and Operational Procedures

Separate discovery, recurring-cause memory, corrections, attachments, instructions and skills.

### D-05 — Discovery, topology and learned understanding

Discovery collects CloudFormation resources and, for tagged resources outside CloudFormation deployments, uses enabled Resource Explorer. Relationship evidence can include configuration, tags, deployment mapping and observability. Learned topology/pipeline views summarize that evidence; raw-resource views expose different levels of granularity. A missing graph node does not prove the agent cannot investigate the resource. [DS04]

The managed Learning agent maintains environment knowledge. Its page provides knowledge, run history and scheduled-trigger inspection. Its schedules belong to the platform, unlike custom-agent triggers. Newer documentation moves learned topology, dependency, pipeline and tool-use knowledge into memory; older pages still call these learned skills. [DS06] [DS19]

**Engineering verification:** choose one service, identify its actual deployed resources and repository revision, and compare them with the graph. Record missing or incorrectly inferred edges separately. Inspect a learning run and the output's version after refresh; clicking a refresh control is not the completion evidence. Do not enable additional account writes to repair a read/discovery gap.

### D-M01 — How previous incidents become reusable context

**Production and retrieval are distinct.** The managed `monitors` store associates recurring causes and investigation evidence with an alarm or metric. AWS describes a daily learning pass when the space has investigations in the preceding two weeks; entries without updates for two weeks can be removed and full stores evict the oldest item. This is operational context, not permanent incident retention. [DS07]

At session start, an agent sees store descriptions. It opens relevant stores, evaluates entry descriptions, and reads selected content. Updates create immutable versions. A store may exist without being selected. The public documentation does not identify a customer-controlled model-training process or disclose a retrieval-ranking implementation. [DS07]

```text
Past investigations → learning process → monitor-specific memory
                                             ↓
New signal → store relevance → entry relevance → selected context
                                             ↓
                              diagnosis using current evidence
```

**Operator procedure:** open **Knowledge → Memories**, inspect the monitor store, open the relevant entry, and inspect version and modification time. Confirm that the store and entry are active. Inactive entries are excluded; the monitor store is documented as enabled by default. Use Chat to request a correction to retained information and inspect the resulting content. [DS07] [DS19]

**Proposed acceptance test:** retain the old incident's independently established cause, then investigate a new occurrence with deliberately different evidence. Record three separate conclusions: entry exists; retrieval was observable or unverified; current diagnosis matches the new evidence. Do not infer retrieval merely because the answer repeats a familiar phrase.

### D-M02 — Corrective feedback produces a separate lesson

Corrective feedback is not the same producer as monitor-history synthesis. In a completed investigation, **Add feedback** records the verdict and, when wrong, the actual cause; Chat is another entry point. The most recent feedback submission replaces earlier feedback for that investigation. Sharing it with AWS requires separate confirmation. The dated change log describes a `reflections` store for lessons from corrections. [DS08] [DS19]

### D-M07 — Memory attachment and lifecycle

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

### D-M03 — Standing instructions enter each new session

Global and agent-specific `AGENTS.md` text is supplied at startup; it is not selected by relevance. Changes apply to sessions started after saving. A running session retains its startup content. [DS09]

**Procedure:** open **Agents → Managed agents**, select the relevant agent, and edit the global or agent-specific instructions on **Agent definition**. Confirm the global change when prompted. Start a new session for verification. Older cached instructions pages show **Knowledge → Instructions**; the newer indexed guide and managed-agent page agree on the Agents route. [DS09] [DS06]

**Original example, not an AWS default:**

```markdown
## Incident output contract
Identify the resource and UTC time range for every material observation.
Separate current observations from historical context.
When required data is unavailable, name the failed read and continue only
with conclusions supported by the remaining evidence.
```

Save this only where applicable. Check an old and a new session to test propagation. An instruction changes prompt context; it does not modify IAM authorization. Keep the authoritative text in Git, rather than retaining manual document snapshots.

### D-M04 — Skills are selected procedures, not standing memory

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

## 04. Incident Operations and Controlled Execution

Trace triage, investigations, custom-agent work, sandbox computation, approvals and configuration updates.

### D-06 — Incident routing and investigation feedback

An external signal is triaged before an independent investigation is necessarily started. **Linked** adds the signal to existing work; **Skipped** applies configured skip criteria; **Proceed** schedules new work. The web app shows the decision and reason. Unlinking or unskipping reschedules independent investigation; correlation or skip skills can be corrected for future events. [DS08]

For a manual investigation, supply the problem, optional starting evidence, incident time, name and priority. Inspect investigation output and tool evidence, then submit feedback after completion. A route decision, a diagnosis, and a feedback verdict are different records. [DS08]

**Engineering procedure:** for an unexpected absence of investigation, first inspect the triage record. A linked event is not lost; follow its primary investigation. A skipped event calls for reviewing the matching skill. For incorrect diagnosis, add the verified correction rather than changing a routing rule unless routing itself was wrong.

Prevention evaluations analyze multiple investigations into recommendations. The **Improvements** page exposes the latest evaluation summary, manual evaluation and schedule controls; the documented default is weekly. This differs from daily monitor-memory refresh. [DS15]

### D-07 — Custom-agent definitions, schedules and cancellation

Define a name, system prompt, selected skills and memory stores. Use Chat for tool assignment and inspect the saved definition before executing. The available tool set is the selected subset of the space's integrations. [DS12]

**Execution procedure:** choose the agent, select **Run Now** or **Run with prompt**, then open the invocation in **History**. Inspect tool arguments and results, not only the final text. To schedule it, open **Triggers**, create a rate or cron expression, and check the displayed next run. `cron(0 9 ? * MON-FRI *)` is 09:00 UTC on weekdays, not automatically Zurich civil time. Pause the trigger to stop future starts. Cancel an existing run separately; an in-flight tool call may finish after cancellation. [DS13]

**Original system-prompt outline:** “Read the selected staging service's alarm and deployment tools for the previous 24 complete hours. Return resource IDs, the UTC window, failed reads and links to material results. Do not publish to external destinations.” This becomes usable only after real tool names and access have been selected. A schedule without those dependencies is not a reporting capability.

### D-M05 — Investigation-local computation

Sandbox provisions a fresh Linux environment per investigation. It can execute code, access configured packages and use account profiles within existing permissions. Its default outbound policy permits AWS service endpoints; other destinations require allowlisting. The reviewed preview does not extend this environment to all chat or custom-agent paths. [DS14]

**Procedure:** in the console, select the space, open **Capabilities → Sandbox → Configure**, select packages and add required host/method/path rules, then save. An empty allowlist is not total network isolation. Remove the Sandbox configuration to stop future use; do not assume that changing configuration rewinds already executed code. [DS14]

**Proposed check:** process a harmless supplied dataset, inspect code and numerical results, and test that an unlisted non-AWS endpoint is unavailable. Do not use production mutation as a connectivity test. Network filtering, AWS permissions and directed-action approvals are distinct controls.

### D-M06 — Directed-action authorization

Directed actions require space opt-in, eligible target-account elevated access or integration configuration, and specific operator approval. The approval binds the operation and resource; AWS calls are attributed through CloudTrail. A saved role is a permission ceiling, not a standing approval. [DS16]

**Procedure:** enable the space setting; register the target account's `agentElevatedRoleArn`; review tool categories for connected services; ask for the particular change; review or adjust parameters; approve or reject; then compare resulting state with the approved operation. Programmatically registered tools without `toolDetails` default to read-only. Incorrect classification can bypass the expected approval prompt. [DS16]

When using `UpdateAgentSpace`, supplying `preferences` replaces that complete map; omitted preferences revert to defaults. Read current settings first and verify them afterward. A denied mutation should lead to inspection of enablement, role trust, permission policy, tool category and approval scope—not unconditional elevation. [DS16]

### D-08 — Configuration APIs and update semantics

Asset management uses the `devops-agent` CLI/SDK client but `aidevops:` IAM actions. `ListAssetTypes` discovers supported types; other asset operations generally authorize against the Agent Space ARN. Metadata keys use snake_case, while top-level request keys use camelCase. Metadata updates use PATCH semantics; asset type cannot be changed. Custom-agent skill/store references require asset IDs, not names. [DS17]

**Read-only inspection pattern:**

```bash
aws devops-agent list-asset-types --region "$AWS_REGION"
aws devops-agent list-assets --agent-space-id "$AGENT_SPACE_ID" --region "$AWS_REGION"
```

Set both variables to your approved environment; these commands were not executed here. Inspect returned metadata before changing it. Asset PATCH behavior must not be generalized to the replacement behavior of the directed-action preference map. For content upload/file operations and deployment templates, follow the type-specific official examples rather than constructing an undocumented payload. [DS17]

### D-09 — Access direction and preview release paths

| Path | Caller → recipient | What it connects |
|---|---|---|
| External-tool MCP | DevOps Agent → your tool server | Tool/data access; D-03 |
| Remote service endpoint | Authorized client → DevOps Agent | MCP or agent-protocol access to service capabilities |
| Webhook | Incident system → Agent Space | Incident initiation |
| Asset/service APIs | Administrator or automation → AWS API | Configuration and supported service operations |

Each path has its own authentication and permissions. Connecting a tool server does not grant a client access to the agent. The access guide links the remote endpoint, webhook and API procedures. Their complete protocol setup is linked, not reproduced in this edition. [DS20]

Release testing interacts with a deployed application and can create, modify or delete application data. A test profile supplies reusable context; the execution produces evidence about that run. Treat it separately from code/readiness analysis. Use a disposable target and disabled external side effects before trying the preview. [DS21]

## 05. Worked Incident Analysis

Use prepared evidence to examine a recurring alarm without assuming the previous cause has returned.

### D-U01 — Worked example: recurring alarm, different cause

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

## 06. Troubleshooting, Limits and Failure Modes

Locate the first failed prerequisite and distinguish limits from missing access, context or approval.

### D-10 — Limits and diagnostic decisions

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

## 07. Coverage and Source Notes

Identify detailed coverage, linked subjects, deferred procedures and source-version qualifications.

### D-11 — Coverage and evidence notes

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
