---
id: model-devops
kind: record
collection: resource-models
product: devops
title: devops resource model
frozen: true
data:
  title: AWS DevOps Agent
  overview_section: D-01
  dictionary_section: D-13
  application_section: D-14
  entities:
  - id: D-Space
    name: Agent Space
    owner: aws
    kind: service resource
    identity: agentSpaceId; Agent Space ARN
    scope: Account and Region
    meaning:
      $markdown: field-0001
    sources:
    - DS50
    - DS51
  - id: D-Registration
    name: Provider registration
    owner: aws
    kind: service configuration
    identity: serviceId in the association API
    scope: Account registration
    meaning:
      $markdown: field-0002
    sources:
    - DS51
    - DS62
  - id: D-Association
    name: Service association
    owner: aws
    kind: API resource
    identity: associationId, agentSpaceId, serviceId
    scope: One Agent Space
    meaning:
      $markdown: field-0003
    sources:
    - DS51
  - id: D-Tool
    name: Selected tool
    owner: aws
    kind: configuration member
    identity: Tool identifier within its configured provider
    scope: Association and custom definition
    meaning: An exposed operation selected for use; not an independently deployed tool resource.
    sources:
    - DS52
    - DS53
    - DS62
  - id: D-Role
    name: Resource and operator IAM roles
    owner: aws
    kind: cross-service resource
    identity: IAM role ARN
    scope: Relevant AWS account
    meaning:
      $markdown: field-0004
    sources:
    - DS50
    - DS57
  - id: D-Custom
    name: Custom-agent definition
    owner: aws
    kind: asset subtype
    identity: assetId; assetType custom_agent
    scope: One Agent Space
    meaning:
      $markdown: field-0005
    sources:
    - DS52
    - DS53
  - id: D-Skill
    name: Skill
    owner: aws
    kind: asset subtype
    identity: assetId; assetType skill
    scope: One Agent Space
    meaning: Procedural instructions and references with applicability and agent-type scope.
    sources:
    - DS52
  - id: D-Instructions
    name: Agent instructions
    owner: aws
    kind: asset subtype
    identity: assetId; assetType agents_md
    scope: Agent Space and agent type
    meaning: Standing guidance loaded into new applicable work; content is not an IAM policy.
    sources:
    - DS52
    - DS55
  - id: D-Store
    name: Memory store
    owner: aws
    kind: asset subtype
    identity: assetId; assetType memory_store
    scope: One Agent Space
    meaning:
      $markdown: field-0006
    sources:
    - DS52
    - DS53
    - DS55
  - id: D-Memory
    name: Memory entry
    owner: aws
    kind: asset subtype
    identity: Memory asset identity within its store
    scope: One store
    meaning: Synthesized informational content that can be selected and read for a task.
    sources:
    - DS52
    - DS55
  - id: D-Version
    name: Memory content version
    owner: aws
    kind: version record
    identity: Memory identity plus displayed version
    scope: One memory entry
    meaning:
      $markdown: field-0007
    sources:
    - DS55
  - id: D-Trigger
    name: Custom-agent trigger
    owner: aws
    kind: schedule configuration
    identity: Trigger shown on the custom-agent definition
    scope: One custom agent
    meaning: Rate or cron schedule for future invocations; pausing it does not cancel existing work.
    sources:
    - DS53
    - DS54
  - id: D-Invocation
    name: Custom-agent invocation
    owner: aws
    kind: execution record
    identity: Invocation selected in History
    scope: One custom agent
    meaning:
      $markdown: field-0008
    sources:
    - DS53
    - DS54
  - id: D-Signal
    name: Incident signal
    owner: aws
    kind: operational record
    identity: Signal linkage and displayed triage decision
    scope: One Agent Space
    meaning:
      $markdown: field-0009
    sources:
    - DS56
  - id: D-Investigation
    name: Investigation
    owner: aws
    kind: execution record
    identity: Investigation identifier and incident interval
    scope: One Agent Space
    meaning:
      $markdown: field-0010
    sources:
    - DS56
  - id: D-Feedback
    name: Investigation feedback
    owner: aws
    kind: operational record
    identity: Feedback associated with an investigation
    scope: Completed investigation
    meaning:
      $markdown: field-0011
    sources:
    - DS56
    - DS52
  - id: D-Topology
    name: Topology and environment understanding
    owner: aws
    kind: derived view
    identity: Space, selected view and applicable knowledge version
    scope: One Agent Space
    meaning:
      $markdown: field-0012
    sources:
    - DS58
  - id: D-Evaluation
    name: Prevention evaluation
    owner: aws
    kind: execution record
    identity: Evaluation shown in Improvements
    scope: One Agent Space
    meaning: Analysis of investigation history for proposed improvements.
    sources:
    - DS59
  - id: D-Recommendation
    name: Prevention recommendation
    owner: aws
    kind: result record
    identity: Recommendation in the evaluation output
    scope: Agent Space
    meaning: Proposed improvement with a review state, not an implemented resource change.
    sources:
    - DS59
  - id: D-Approval
    name: Directed-action approval
    owner: aws
    kind: authorization event
    identity: Approved operation, target and operator attribution
    scope: A particular requested action
    meaning:
      $markdown: field-0013
    sources:
    - DS57
  - id: D-Chat
    name: Chat conversation
    owner: aws
    kind: interaction record
    identity: Conversation in the space web app
    scope: One Agent Space
    meaning:
      $markdown: field-0014
    sources:
    - DS50
    - DS61
  - id: D-Readiness
    name: Release-readiness review
    owner: aws
    kind: preview execution
    identity: Review task and candidate source revision
    scope: Release management
    meaning: Change analysis is distinct from active testing of a deployed application.
    sources:
    - DS61
  - id: D-TestProfile
    name: Release test profile
    owner: aws
    kind: asset subtype
    identity: assetId; assetType test_profile
    scope: One Agent Space
    meaning: Reusable target and test-type configuration; not the documentation implementation profile.
    sources:
    - DS52
    - DS60
  - id: D-TestRun
    name: Release test execution
    owner: aws
    kind: preview execution
    identity: Release Manager task or displayed test result
    scope: Authorized deployed target
    meaning: Real requests and observed results; application data may change.
    sources:
    - DS60
  - id: D-Source
    name: Telemetry or repository source
    owner: external
    kind: source system
    identity: Provider-native resource, revision and time range
    scope: External system of record
    meaning: Original observations remain distinct from a copied summary or retained memory.
    sources: []
  - id: D-Target
    name: Deployed application
    owner: external
    kind: customer workload
    identity: Endpoint, deployed revision and test identity
    scope: Application owner authorization
    meaning: The target receives requests; accepting a test profile is not blanket authorization.
    sources: []
  - id: D-Managed
    name: Managed agent role
    owner: aws
    kind: platform-owned component
    identity: Agent type shown in Managed agents
    scope: One Agent Space
    meaning:
      $markdown: field-0015
    sources:
    - DS63
  - id: D-LearningRun
    name: Learning execution
    owner: aws
    kind: execution record
    identity: Run selected in the Learning history
    scope: Managed Learning role
    meaning:
      $markdown: field-0016
    sources:
    - DS63
    - DS55
  relationships:
  - id: DR01
    from: D-Space
    to: D-Association
    verb: contains
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Association includes agentSpaceId.
    sources:
    - DS51
  - id: DR02
    from: D-Registration
    to: D-Association
    verb: is associated through
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note:
      $markdown: field-0017
    sources:
    - DS51
    - DS62
  - id: DR03
    from: D-Association
    to: D-Tool
    verb: selects
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0018
    sources:
    - DS62
  - id: DR04
    from: D-Space
    to: D-Custom
    verb: stores
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: The custom definition is an asset in its space.
    sources:
    - DS52
  - id: DR05
    from: D-Custom
    to: D-Tool
    verb: selects subset
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Only assigned tools are available to the invocation.
    sources:
    - DS53
  - id: DR06
    from: D-Custom
    to: D-Skill
    verb: references asset IDs
    targets: 0..*
    sources_per_target: 0..*
    basis: documented
    note: Existing skill assets in the same Agent Space; a name is not an asset ID.
    sources:
    - DS52
  - id: DR07
    from: D-Custom
    to: D-Store
    verb: attaches asset IDs
    targets: 0..*
    sources_per_target: 0..*
    basis: documented
    note:
      $markdown: field-0019
    sources:
    - DS52
    - DS53
  - id: DR08
    from: D-Space
    to: D-Store
    verb: scopes
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: This is a space-local relationship, not organization-wide memory sharing.
    sources:
    - DS52
    - DS55
  - id: DR09
    from: D-Store
    to: D-Memory
    verb: groups
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Create the store before entries; content availability and selection remain distinct.
    sources:
    - DS52
    - DS55
  - id: DR10
    from: D-Memory
    to: D-Version
    verb: has content versions
    targets: 1..*
    sources_per_target: '1'
    basis: documented
    note: Every update creates an immutable version.
    sources:
    - DS55
  - id: DR11
    from: D-Custom
    to: D-Invocation
    verb: is executed as
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Repeated runs are separate invocation records.
    sources:
    - DS53
    - DS54
  - id: DR12
    from: D-Custom
    to: D-Trigger
    verb: has schedules
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Trigger management belongs to the selected custom agent.
    sources:
    - DS54
  - id: DR13
    from: D-Trigger
    to: D-Invocation
    verb: initiates
    targets: 0..*
    sources_per_target: 0..1
    basis: logical
    note:
      $markdown: field-0020
    sources:
    - DS54
  - id: DR14
    from: D-Signal
    to: D-Investigation
    verb: links or starts
    targets: 0..1
    sources_per_target: 0..*
    basis: logical
    note:
      $markdown: field-0021
    sources:
    - DS56
  - id: DR15
    from: D-Investigation
    to: D-Feedback
    verb: receives correction
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note:
      $markdown: field-0022
    sources:
    - DS56
  - id: DR16
    from: D-Investigation
    to: D-Memory
    verb: informs later synthesis
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0023
    sources:
    - DS55
  - id: DR17
    from: D-Evaluation
    to: D-Recommendation
    verb: produces
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Evaluation and recommendation review are separate from implementation.
    sources:
    - DS59
  - id: DR18
    from: D-Space
    to: D-Topology
    verb: has derived views
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note: View multiplicity is not an API inventory or authorization contract.
    sources:
    - DS58
  - id: DR19
    from: D-Tool
    to: D-Source
    verb: reads authorized evidence
    targets: '?'
    sources_per_target: '?'
    basis: logical
    note: Actual provider operations and identity determine the readable scope.
    sources:
    - DS62
  - id: DR20
    from: D-TestProfile
    to: D-TestRun
    verb: supplies reusable configuration
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0024
    sources:
    - DS60
  - id: DR21
    from: D-TestRun
    to: D-Target
    verb: sends real requests
    targets: '?'
    sources_per_target: 0..*
    basis: documented
    note: Application writes are distinct from directed AWS API actions.
    sources:
    - DS60
  - id: DR22
    from: D-Chat
    to: D-Approval
    verb: requests action authorization
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Approval applies to the operation and resource, not every subsequent message.
    sources:
    - DS57
  - id: DR23
    from: D-Approval
    to: D-Role
    verb: permits scoped use
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0025
    sources:
    - DS57
  - id: DR24
    from: D-Space
    to: D-Managed
    verb: exposes managed roles
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note: Roles are platform-owned, not custom-agent definitions.
    sources:
    - DS63
  - id: DR25
    from: D-Managed
    to: D-LearningRun
    verb: Learning role has history
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: This edge applies to Learning only; other managed roles execute within investigations.
    sources:
    - DS63
  - id: DR26
    from: D-LearningRun
    to: D-Memory
    verb: synthesizes retained context
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0026
    sources:
    - DS63
    - DS55
  feature_bindings:
    FT-D-SOURCES:
    - D-Registration
    - D-Association
    - D-Tool
    - D-Role
    - D-Source
    FT-D-TOPOLOGY:
    - D-Topology
    - D-Space
    - D-Managed
    - D-LearningRun
    FT-D-MEMORY:
    - D-Store
    - D-Memory
    - D-Version
    - D-Custom
    - D-LearningRun
    FT-D-INSTRUCTIONS:
    - D-Instructions
    FT-D-SKILLS:
    - D-Skill
    FT-D-CUSTOM:
    - D-Custom
    - D-Invocation
    FT-D-SCHEDULE:
    - D-Trigger
    - D-Invocation
    FT-D-HISTORY:
    - D-Invocation
    FT-D-INCIDENT:
    - D-Signal
    - D-Investigation
    - D-Feedback
    FT-D-PREVENTION:
    - D-Evaluation
    - D-Recommendation
    FT-D-ACTIONS:
    - D-Approval
    - D-Role
    - D-Tool
    FT-D-READINESS:
    - D-Readiness
    - D-Source
    FT-D-TEST:
    - D-TestProfile
    - D-TestRun
    - D-Target
    FT-D-QUERY:
    - D-Space
    - D-Chat
    - D-Tool
  views:
  - key: er-devops-scope
    title: 'DevOps Agent: scope, providers and execution'
    sections:
    - D-01
    - D-13
    nodes:
    - D-Space
    - D-Registration
    - D-Association
    - D-Tool
    - D-Custom
    - D-Trigger
    - D-Invocation
    - D-Source
    edges:
    - DR01
    - DR02
    - DR03
    - DR04
    - DR05
    - DR11
    - DR12
    - DR13
    - DR19
  - key: er-devops-knowledge
    title: 'DevOps Agent: stored knowledge and configuration references'
    sections:
    - D-13
    - D-M07
    nodes:
    - D-Space
    - D-Custom
    - D-Skill
    - D-Store
    - D-Memory
    - D-Version
    - D-Investigation
    edges:
    - DR04
    - DR06
    - DR07
    - DR08
    - DR09
    - DR10
    - DR16
  - key: er-devops-incidents
    title: 'DevOps Agent: incident records and directed-action boundary'
    sections:
    - D-14
    - D-06
    - D-M06
    nodes:
    - D-Signal
    - D-Investigation
    - D-Feedback
    - D-Memory
    - D-Chat
    - D-Approval
    - D-Role
    edges:
    - DR14
    - DR15
    - DR16
    - DR22
    - DR23
---

<!-- block: b-546c17115c0e53d6873e -->
## entities / 0 / meaning

<!-- block: b-8cab9b7e0958503c9377 -->
<!-- field: field-0001 -->
Operational container for account access, integration associations, knowledge and executions.
<!-- /field -->

<!-- block: b-1ce77c62b0bc59619816 -->
## entities / 1 / meaning

<!-- block: b-dce2d8f70aa55a7f9206 -->
<!-- field: field-0002 -->
Registered provider endpoint and authorization; registration alone does not select a space's tools.
<!-- /field -->

<!-- block: b-3a4ff279d9805d49bfc8 -->
## entities / 2 / meaning

<!-- block: b-a2ec64e3eb9a54cab5fb -->
<!-- field: field-0003 -->
Provider-specific configuration selecting the service resources or tools usable in that space.
<!-- /field -->

<!-- block: b-e8a865f579325f4f8a8e -->
## entities / 4 / meaning

<!-- block: b-ccfb8b089a405e158b97 -->
<!-- field: field-0004 -->
Separate roles govern service resource access and operator access; elevated action access is another role binding.
<!-- /field -->

<!-- block: b-5437be64b9f256c592c3 -->
## entities / 5 / meaning

<!-- block: b-bef6934db8165e939dc3 -->
<!-- field: field-0005 -->
Stored prompt with selected tools, skill asset IDs and memory-store asset IDs; not an invocation.
<!-- /field -->

<!-- block: b-3b819bd64c92540c9448 -->
## entities / 8 / meaning

<!-- block: b-b40f74c92bba50fe9103 -->
<!-- field: field-0006 -->
Collection with a subject description; managed and custom stores have different write behavior.
<!-- /field -->

<!-- block: b-8580e04d8b23564d9b62 -->
## entities / 10 / meaning

<!-- block: b-b32e43c37afe509e8c2b -->
<!-- field: field-0007 -->
Immutable content revision; a version selector is not evidence of every possible restore or undelete operation.
<!-- /field -->

<!-- block: b-4f1418dc7eb258aa8ad7 -->
## entities / 12 / meaning

<!-- block: b-c61f75e6ffa558f6983b -->
<!-- field: field-0008 -->
A particular execution with status, tool calls and outputs; its trajectory is execution detail.
<!-- /field -->

<!-- block: b-011a12615703563faff0 -->
## entities / 13 / meaning

<!-- block: b-a3a2c72bc370577e8ed9 -->
<!-- field: field-0009 -->
Incoming incident context can be linked, skipped or scheduled for independent investigation.
<!-- /field -->

<!-- block: b-1b9e34fb181d5a3eadd4 -->
## entities / 14 / meaning

<!-- block: b-5d6e64ed9e0c5cf29e7a -->
<!-- field: field-0010 -->
Evidence-gathering work and evolving incident conclusions; not the same record as a signal.
<!-- /field -->

<!-- block: b-b1de7eb7721652cf92c8 -->
## entities / 15 / meaning

<!-- block: b-bee08d099492528ea4e4 -->
<!-- field: field-0011 -->
Operator verdict and verified correction. Do not assume a one-to-one mapping to every internal reflection entry.
<!-- /field -->

<!-- block: b-0a6dfbb839415ca08b65 -->
## entities / 16 / meaning

<!-- block: b-1bfc567da4be56038106 -->
<!-- field: field-0012 -->
Discovered and inferred relationships; not an independent access boundary or a complete authoritative inventory.
<!-- /field -->

<!-- block: b-cde89b6261825110bbd3 -->
## entities / 19 / meaning

<!-- block: b-71e6c2984f1559e69062 -->
<!-- field: field-0013 -->
Execution-time authorization separate from opt-in, role permissions and tool classification.
<!-- /field -->

<!-- block: b-cbba841abcab5caca78f -->
## entities / 20 / meaning

<!-- block: b-43171c2a26ab5075a387 -->
<!-- field: field-0014 -->
On-demand inquiry and supported configuration/action requests do not inherently require a custom-agent definition.
<!-- /field -->

<!-- block: b-81cf9c75cb9a50d2bca1 -->
## entities / 26 / meaning

<!-- block: b-becf28c27d875cca881d -->
<!-- field: field-0015 -->
Platform-owned role; it is not a user-created custom_agent asset. Incident roles participate in investigations. Only Learning exposes its own run history and platform-owned triggers.
<!-- /field -->

<!-- block: b-19ce367bf4105b598e6d -->
## entities / 27 / meaning

<!-- block: b-f699ad8eaa465d47b982 -->
<!-- field: field-0016 -->
Observable synthesis and refresh execution; do not infer a separately runnable record for every managed incident role.
<!-- /field -->

<!-- block: b-434ae3a2accc5fd9b628 -->
## relationships / 1 / note

<!-- block: b-5020725df12b5a3db8db -->
<!-- field: field-0017 -->
Do not assume unlimited associations. AssociateService replaces the existing association of the same service.
<!-- /field -->

<!-- block: b-c38b3f77b27c5a6c90d0 -->
## relationships / 2 / note

<!-- block: b-7c7f360a391355ad8b24 -->
<!-- field: field-0018 -->
Provider-specific configuration; tools are members, not independently provisioned resources.
<!-- /field -->

<!-- block: b-2cf005d16b5059728555 -->
## relationships / 6 / note

<!-- block: b-d5fab32f3e17557283b7 -->
<!-- field: field-0019 -->
Starts empty. Attached custom stores permit writes; managed stores are read-only to a custom agent.
<!-- /field -->

<!-- block: b-1f082bdb28fa5e348a85 -->
## relationships / 12 / note

<!-- block: b-272abe5765925efdbdf7 -->
<!-- field: field-0020 -->
Optional origin because an invocation may be manual. This is not an asserted API foreign key.
<!-- /field -->

<!-- block: b-ba2342bbce015ec19098 -->
## relationships / 13 / note

<!-- block: b-956736bd46465de58bd0 -->
<!-- field: field-0021 -->
Current routing view: skipped signals have no investigation, linked signals share one; manual investigations need no external signal. This is not immutable lifetime cardinality.
<!-- /field -->

<!-- block: b-181b4356bd125da7a31e -->
## relationships / 14 / note

<!-- block: b-90eff6fe2f545294bd14 -->
<!-- field: field-0022 -->
A feedback submission belongs to the investigation; feedback-to-memory entry counts are not specified.
<!-- /field -->

<!-- block: b-ab0cd7b0e3ce56a39a2c -->
## relationships / 15 / note

<!-- block: b-413e018fe1e85b61a4cc -->
<!-- field: field-0023 -->
A learning process mediates this relationship; the edge is not an immediate direct write or model retraining.
<!-- /field -->

<!-- block: b-37e0edce4b0a5df8b6a5 -->
## relationships / 19 / note

<!-- block: b-5bba190cfdfd591aba98 -->
<!-- field: field-0024 -->
Profile-based execution is documented; do not require a saved profile for every supported initiation path.
<!-- /field -->

<!-- block: b-e272445ecc1d53788144 -->
## relationships / 22 / note

<!-- block: b-82395fd657925a9fb823 -->
<!-- field: field-0025 -->
AWS-resource directed actions use the registered elevated role; permissions alone are not approval.
<!-- /field -->

<!-- block: b-d0e48f068a7658918e16 -->
## relationships / 25 / note

<!-- block: b-b4602b70dc7a5862bb4a -->
<!-- field: field-0026 -->
Completion and a resulting version must be inspected; this is not customer-controlled model training.
<!-- /field -->
