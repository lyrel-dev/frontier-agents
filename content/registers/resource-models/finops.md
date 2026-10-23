---
id: model-finops
kind: record
collection: resource-models
product: finops
title: finops resource model
frozen: true
data:
  title: AWS FinOps Agent
  overview_section: F-01
  dictionary_section: F-09
  application_section: F-10
  entities:
  - id: F-Agent
    name: FinOps agent instance
    owner: aws
    kind: service resource
    identity: finops-agent AgentSpace actions and agentspace ARN in IAM
    scope: AWS account and Region
    meaning:
      $markdown: field-0001
    sources:
    - FS50
    - FS51
  - id: F-DataRole
    name: Agent data role
    owner: aws
    kind: cross-service resource
    identity: IAM role ARN trusted by finops-agent.amazonaws.com
    scope: Configured AWS account access
    meaning:
      $markdown: field-0002
    sources:
    - FS50
    - FS51
  - id: F-OperatorRole
    name: Operator role
    owner: aws
    kind: cross-service resource
    identity: Configured IAM role ARN
    scope: Agent web-application operations
    meaning: Distinct from the agent data role and from the end user's own entry permissions.
    sources:
    - FS50
    - FS51
  - id: F-Integration
    name: Integration registration
    owner: aws
    kind: service resource
    identity: Account-level Jira or Slack integration
    scope: AWS account
    meaning: Registers authorization before an instance is connected to a project or channel.
    sources:
    - FS50
    - FS55
    - FS56
  - id: F-Connection
    name: Agent connection
    owner: aws
    kind: service resource
    identity: Connection to selected integration and destination
    scope: One agent instance
    meaning: Binds the registered integration to the selected Jira project or Slack channel.
    sources:
    - FS50
    - FS55
    - FS56
  - id: F-Conversation
    name: Conversation
    owner: aws
    kind: interaction record
    identity: Conversation in the agent workspace
    scope: One agent instance
    meaning: Can answer directly. A conversation is not automatically a task.
    sources:
    - FS52
    - FS54
  - id: F-Task
    name: Task
    owner: aws
    kind: execution record
    identity: Task in the Tasks workspace
    scope: One agent instance
    meaning: On-demand, scheduled or event-created execution with recorded results.
    sources:
    - FS52
    - FS54
  - id: F-Automation
    name: Automation
    owner: aws
    kind: service configuration
    identity: Saved automation in the Automations workspace
    scope: One agent instance
    meaning: Schedule or supported event condition that creates new tasks.
    sources:
    - FS52
  - id: F-Rule
    name: EventBridge managed rule
    owner: aws
    kind: cross-service resource
    identity: Service-managed EventBridge rule
    scope: Supported event automation
    meaning:
      $markdown: field-0003
    sources:
    - FS51
    - FS52
  - id: F-Source
    name: AWS cost and operational evidence
    owner: documentation
    kind: normalized evidence family
    identity: Original query basis, anomaly or recommendation identifier
    scope: Underlying cost and operational services
    meaning:
      $markdown: field-0004
    sources:
    - FS51
    - FS57
  - id: F-File
    name: Context file
    owner: aws
    kind: retained input
    identity: Uploaded file and active state
    scope: One agent instance
    meaning:
      $markdown: field-0005
    sources:
    - FS53
    - FS54
  - id: F-Memory
    name: Persistent memory
    owner: aws
    kind: managed retained state
    identity: Preference, fact or correction addressed in conversation
    scope: One agent instance
    meaning:
      $markdown: field-0006
    sources:
    - FS53
    - FS54
  - id: F-Runtime
    name: Session runtime
    owner: aws
    kind: ephemeral execution component
    identity: Current session context, not an asserted public resource ID
    scope: One session
    meaning:
      $markdown: field-0007
    sources:
    - FS54
  - id: F-Summary
    name: Conversation summary
    owner: aws
    kind: derived context
    identity: Older-message summary within the current conversation context
    scope: Conversation context window
    meaning: Compaction is distinct from persistent memory and does not promise verbatim retention.
    sources:
    - FS53
  - id: F-Artifact
    name: Report artifact
    owner: aws
    kind: output record
    identity: Artifact in the Artifacts workspace
    scope: One agent instance
    meaning:
      $markdown: field-0008
    sources:
    - FS54
    - FS58
  - id: F-Approval
    name: Jira approval decision
    owner: aws
    kind: authorization interaction
    identity: Requested Jira action and invocation context
    scope: Interactive or on-demand Jira action
    meaning: Not required per action for pre-authorized automations; Slack does not use this prompt.
    sources:
    - FS57
  - id: F-Destination
    name: Jira project or Slack channel
    owner: external
    kind: external destination
    identity: Provider-native project or channel identity
    scope: Destination audience
    meaning: Publication has its own authorization, membership and retention rules.
    sources: []
  - id: F-Message
    name: Published issue, comment or message
    owner: external
    kind: external artifact
    identity: Provider-native issue, comment or message identity
    scope: Destination system
    meaning:
      $markdown: field-0009
    sources: []
  relationships:
  - id: FR01
    from: F-Agent
    to: F-DataRole
    verb: uses data access role
    targets: '1'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0010
    sources:
    - FS50
  - id: FR02
    from: F-Agent
    to: F-OperatorRole
    verb: uses operator role
    targets: '1'
    sources_per_target: '?'
    basis: documented
    note: Separate permission responsibility from data access and end-user entry.
    sources:
    - FS50
    - FS51
  - id: FR03
    from: F-Agent
    to: F-Connection
    verb: has destination connections
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Actual supported connection quotas are separate from logical multiplicity.
    sources:
    - FS50
    - FS55
    - FS56
  - id: FR04
    from: F-Integration
    to: F-Connection
    verb: authorizes connections
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Registration is at account level; connection is at instance level.
    sources:
    - FS55
    - FS56
  - id: FR05
    from: F-Connection
    to: F-Destination
    verb: selects destination
    targets: '1'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0011
    sources:
    - FS55
    - FS56
  - id: FR06
    from: F-Agent
    to: F-Conversation
    verb: retains
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Conversation history is instance-local.
    sources:
    - FS50
    - FS54
  - id: FR07
    from: F-Agent
    to: F-Task
    verb: queues and retains
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: The shared task queue belongs to this instance, not to all agents in the organization.
    sources:
    - FS50
    - FS52
  - id: FR08
    from: F-Agent
    to: F-Automation
    verb: contains future-work rules
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: An automation is not an already-created task.
    sources:
    - FS52
  - id: FR09
    from: F-Automation
    to: F-Task
    verb: creates on each match
    targets: 0..*
    sources_per_target: 0..1
    basis: logical
    note:
      $markdown: field-0012
    sources:
    - FS52
  - id: FR10
    from: F-Conversation
    to: F-Task
    verb: may explicitly request
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Direct answers do not require a task, and Tasks workspace is another initiation path.
    sources:
    - FS52
  - id: FR11
    from: F-Rule
    to: F-Automation
    verb: delivers supported events
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0013
    sources:
    - FS52
  - id: FR12
    from: F-Agent
    to: F-File
    verb: retains reference inputs
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Files are visible to users with agent access, and soft deletion changes active context.
    sources:
    - FS53
    - FS54
  - id: FR13
    from: F-Agent
    to: F-Memory
    verb: retains contextual state
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note: No independent customer-managed memory-store schema is documented here.
    sources:
    - FS53
    - FS54
  - id: FR14
    from: F-File
    to: F-Runtime
    verb: is loaded for a session
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: Runtime isolation is not deletion of the retained input.
    sources:
    - FS54
  - id: FR15
    from: F-Memory
    to: F-Runtime
    verb: is loaded for a session
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: No cross-instance shared memory is inferred.
    sources:
    - FS54
  - id: FR16
    from: F-Conversation
    to: F-Summary
    verb: compacts older messages
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note:
      $markdown: field-0014
    sources:
    - FS53
  - id: FR17
    from: F-Task
    to: F-Artifact
    verb: can produce reports
    targets: 0..*
    sources_per_target: '?'
    basis: logical
    note:
      $markdown: field-0015
    sources:
    - FS52
    - FS58
  - id: FR18
    from: F-Connection
    to: F-Message
    verb: permits supported publication
    targets: 0..*
    sources_per_target: '?'
    basis: logical
    note:
      $markdown: field-0016
    sources:
    - FS55
    - FS56
    - FS57
  - id: FR19
    from: F-Task
    to: F-Source
    verb: queries authorized evidence
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: Query dimensions, time basis and source identity govern the meaning of returned values.
    sources:
    - FS51
    - FS57
  feature_bindings:
    FT-F-SOURCES:
    - F-Agent
    - F-DataRole
    - F-Source
    FT-F-FILES:
    - F-File
    - F-Runtime
    FT-F-MEMORY:
    - F-Memory
    - F-Runtime
    FT-F-CONTEXT:
    - F-Conversation
    - F-Summary
    - F-Runtime
    FT-F-TASKS:
    - F-Task
    - F-Agent
    FT-F-AUTOMATIONS:
    - F-Automation
    - F-Rule
    - F-Task
    FT-F-JIRA:
    - F-Integration
    - F-Connection
    - F-Approval
    - F-Destination
    - F-Message
    FT-F-SLACK:
    - F-Integration
    - F-Connection
    - F-Destination
    - F-Message
    FT-F-ARTIFACTS:
    - F-Artifact
    - F-Task
  views:
  - key: er-finops-scope
    title: 'FinOps Agent: instance access and integration connections'
    sections:
    - F-01
    - F-09
    nodes:
    - F-Agent
    - F-DataRole
    - F-OperatorRole
    - F-Integration
    - F-Connection
    - F-Destination
    edges:
    - FR01
    - FR02
    - FR03
    - FR04
    - FR05
  - key: er-finops-work
    title: 'FinOps Agent: conversation, automation and task records'
    sections:
    - F-09
    - F-03
    nodes:
    - F-Agent
    - F-Conversation
    - F-Automation
    - F-Rule
    - F-Task
    - F-Artifact
    - F-Source
    edges:
    - FR06
    - FR07
    - FR08
    - FR09
    - FR10
    - FR11
    - FR17
    - FR19
  - key: er-finops-context
    title: 'FinOps Agent: retained inputs and session context'
    sections:
    - F-10
    - F-M02
    - F-M03
    - F-M04
    nodes:
    - F-Agent
    - F-File
    - F-Memory
    - F-Conversation
    - F-Summary
    - F-Runtime
    edges:
    - FR06
    - FR12
    - FR13
    - FR14
    - FR15
    - FR16
---

<!-- block: b-94773aea9e2454939768 -->
## entities / 0 / meaning

<!-- block: b-3ce555de56275dd6a78d -->
<!-- field: field-0001 -->
Independent instance in the UI. Its AgentSpace API/IAM name does not make it a DevOps Agent Space.
<!-- /field -->

<!-- block: b-3121c22bc0ce5c539a9d -->
## entities / 1 / meaning

<!-- block: b-8550e8768ece55feb419 -->
<!-- field: field-0002 -->
Permits cost and operational reads and the managed-rule operations required for event automations.
<!-- /field -->

<!-- block: b-ca20f509b5055633ad18 -->
## entities / 8 / meaning

<!-- block: b-b396817ba2e25df3bf4a -->
<!-- field: field-0003 -->
Delivers matching Cost Anomaly Detection events; it is not a general customer event orchestration API.
<!-- /field -->

<!-- block: b-9bc9e844d38c57dd9c73 -->
## entities / 9 / meaning

<!-- block: b-93c22c8fdbfb5f308f6f -->
<!-- field: field-0004 -->
Our grouping of distinct AWS-source results: cost query, forecast, coverage, anomaly, recommendation and change event. It is not one FinOps resource type or a shared evidence API.
<!-- /field -->

<!-- block: b-0a597d2945f85bffa11b -->
## entities / 10 / meaning

<!-- block: b-44cc2505dff850d792ba -->
<!-- field: field-0005 -->
Operator-maintained reference; the agent can read but not rewrite or delete it conversationally.
<!-- /field -->

<!-- block: b-4a021ae0fb6650fcbc6f -->
## entities / 11 / meaning

<!-- block: b-fa2c098f890a54fb8463 -->
<!-- field: field-0006 -->
Supports remember, update and forget; no DevOps-style attachment or version API is inferred.
<!-- /field -->

<!-- block: b-91449e2bab8d5058ab2c -->
## entities / 12 / meaning

<!-- block: b-2b127bc322ca548eb4ba -->
<!-- field: field-0007 -->
Loads retained files into an isolated runtime. Ending a session does not delete persistent records.
<!-- /field -->

<!-- block: b-6cee6873245f57c6aecb -->
## entities / 14 / meaning

<!-- block: b-5662800c5be9594c9aa8 -->
<!-- field: field-0008 -->
Generated report that can be inspected, revised, downloaded or deleted independently of external copies.
<!-- /field -->

<!-- block: b-14a861cb2cba5524a704 -->
## entities / 17 / meaning

<!-- block: b-233d0bd4581552618544 -->
<!-- field: field-0009 -->
A service result copied externally has a lifecycle separate from the originating task or artifact.
<!-- /field -->

<!-- block: b-818e14ffd6a4547f8007 -->
## relationships / 0 / note

<!-- block: b-0266a6d1a20c5e74b900 -->
<!-- field: field-0010 -->
One configured role responsibility; do not infer that customer-managed roles cannot be referenced elsewhere.
<!-- /field -->

<!-- block: b-841eedbfd8e0565d8e2d -->
## relationships / 4 / note

<!-- block: b-407a111bd1c95c5eb14c -->
<!-- field: field-0011 -->
Connection binds the intended project or channel. This is not evidence of reading all destination content.
<!-- /field -->

<!-- block: b-429abbe758ad59f4a64f -->
## relationships / 8 / note

<!-- block: b-951bfcba841e5326b379 -->
<!-- field: field-0012 -->
A task may instead be on demand. No universal automation ID field is asserted by this logical relationship.
<!-- /field -->

<!-- block: b-f89ba149c09651fc8a7b -->
## relationships / 10 / note

<!-- block: b-1dffa48e120d515fab3e -->
<!-- field: field-0013 -->
Exact rule-to-automation cardinality is not specified; do not assert one rule per automation.
<!-- /field -->

<!-- block: b-eec603111d0455679665 -->
## relationships / 15 / note

<!-- block: b-4f2f29384cee535e87a9 -->
<!-- field: field-0014 -->
Summary representation and revision count are not exposed as a customer-managed resource model.
<!-- /field -->

<!-- block: b-46fdffa6d64357448097 -->
## relationships / 16 / note

<!-- block: b-c49f095b738150c4ab5a -->
<!-- field: field-0015 -->
Artifacts can also originate from direct conversations. Do not force every artifact to have exactly one task parent.
<!-- /field -->

<!-- block: b-0111f546da385a2fa1a6 -->
## relationships / 17 / note

<!-- block: b-5d0f810d6dc35b8a8eab -->
<!-- field: field-0016 -->
Jira and Slack actions have different approval behavior; delivery success must be inspected separately.
<!-- /field -->
