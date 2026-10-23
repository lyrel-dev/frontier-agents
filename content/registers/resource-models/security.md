---
id: model-security
kind: record
collection: resource-models
product: security
title: security resource model
frozen: true
data:
  title: AWS Security Agent
  overview_section: S-01
  dictionary_section: S-10
  application_section: S-11
  entities:
  - id: S-Tenant
    name: Shared service scope
    owner: aws
    kind: documented scope
    identity: Tenant/organization scope used in the guide
    scope: Shared Security Agent configuration
    meaning:
      $markdown: field-0001
    sources:
    - SS50
  - id: S-Space
    name: Agent Space
    owner: aws
    kind: service resource
    identity: Application Agent Space identity
    scope: Application or project
    meaning: Groups application sources, settings, assignments and assessments.
    sources:
    - SS50
  - id: S-Registration
    name: Integration registration
    owner: aws
    kind: service configuration
    identity: Registered provider/account connection
    scope: Shared integration setup
    meaning: Authorization registered before particular sources are connected to an application.
    sources:
    - SS50
    - SS51
  - id: S-Connection
    name: Agent Space source connection
    owner: aws
    kind: configuration association
    identity: Space and selected source connection
    scope: One Agent Space
    meaning: Selects a repository or documentation source; per-capability settings decide its use.
    sources:
    - SS50
    - SS51
  - id: S-Repository
    name: Repository or design source
    owner: external
    kind: source artifact
    identity: Provider identity and immutable revision
    scope: Source system
    meaning: The original source can be reused across spaces without making every assessment identical.
    sources: []
  - id: S-Pack
    name: Security requirement pack
    owner: aws
    kind: service configuration
    identity: Pack identity and enabled state
    scope: Shared requirements
    meaning: Managed or custom collection governing subsequent eligible design and code reviews.
    sources:
    - SS53
  - id: S-Requirement
    name: Security requirement
    owner: aws
    kind: configuration item
    identity: Requirement within a pack
    scope: One pack
    meaning: Applicability and compliance criteria, not an assessment result or certification.
    sources:
    - SS53
  - id: S-Pentest
    name: Penetration-test configuration
    owner: aws
    kind: service configuration
    identity: Saved penetration-test identity
    scope: One Agent Space
    meaning: Reusable target, scope, authentication and execution settings.
    sources:
    - SS50
    - SS56
  - id: S-Rules
    name: Target and network rules
    owner: aws
    kind: configuration members
    identity: Rules within the selected test configuration
    scope: A penetration-test configuration
    meaning: Target, supporting access and excluded paths have different permitted effects.
    sources:
    - SS56
  - id: S-Credential
    name: Test credential definition
    owner: aws
    kind: configuration item
    identity: Named credential in test configuration
    scope: A penetration-test configuration
    meaning:
      $markdown: field-0002
    sources:
    - SS52
  - id: S-Login
    name: Retained login procedure
    owner: aws
    kind: managed procedural state
    identity: Procedure associated with the configured authentication flow
    scope: Login Optimization
    meaning: Reuse of successful navigation; no independent editable skill-resource API is asserted.
    sources:
    - SS52
  - id: S-Run
    name: Penetration-test run
    owner: aws
    kind: execution record
    identity: Run identity, target revision and observed credentials
    scope: One saved configuration
    meaning: Independent execution against the target as it exists at run time.
    sources:
    - SS50
    - SS56
  - id: S-Finding
    name: Penetration-test finding
    owner: aws
    kind: result record
    identity: Original finding identifier
    scope: Original assessment run
    meaning: Retains vulnerability evidence and identity through repair and repeated revalidation.
    sources:
    - SS54
    - SS55
  - id: S-Revalidation
    name: Revalidation job
    owner: aws
    kind: execution record
    identity: Job in run history with type Revalidation
    scope: Selected existing findings
    meaning:
      $markdown: field-0003
    sources:
    - SS54
  - id: S-SelectedResult
    name: Finding-to-revalidation result
    owner: documentation
    kind: normalized association
    identity: 'Our pair: original finding and revalidation job'
    scope: Documentation evidence model
    meaning:
      $markdown: field-0004
    sources:
    - SS54
  - id: S-CodeConfig
    name: Full-code review configuration
    owner: aws
    kind: service configuration
    identity: Selected source configuration and repository settings
    scope: One Agent Space
    meaning:
      $markdown: field-0005
    sources:
    - SS50
  - id: S-CodeRun
    name: Code review
    owner: aws
    kind: execution record
    identity: Review and exact source revision
    scope: Full or change-focused assessment
    meaning: A source assessment is not a running-application test.
    sources:
    - SS50
  - id: S-Design
    name: Design review
    owner: aws
    kind: one-off assessment
    identity: Individual review identity
    scope: One Agent Space
    meaning:
      $markdown: field-0006
    sources:
    - SS50
  - id: S-ThreatConfig
    name: Threat-model configuration
    owner: aws
    kind: service configuration
    identity: Saved threat-model identity
    scope: One Agent Space
    meaning: Reusable source and scope selection with on-demand runs.
    sources:
    - SS50
    - SS57
  - id: S-ThreatRun
    name: Threat-model run
    owner: aws
    kind: execution and result record
    identity: Run identity within a threat model
    scope: Selected source and scope documents
    meaning: Produces a system overview and threats for that run; inferred boundaries need review.
    sources:
    - SS57
  - id: S-Remediation
    name: Remediation attempt
    owner: aws
    kind: operation record
    identity: Finding-linked remediation state
    scope: Configured source repositories
    meaning:
      $markdown: field-0007
    sources:
    - SS55
  - id: S-Patch
    name: Patch or pull request
    owner: external
    kind: change artifact
    identity: Diff or provider-native pull request and revision
    scope: Engineering delivery process
    meaning: A proposal requires review, tests and deployment before a repair can be tested.
    sources: []
  - id: S-Target
    name: Deployed test application
    owner: external
    kind: customer workload
    identity: Endpoint, deployment revision and actual test role
    scope: Owner-authorized test boundary
    meaning: Actual application state may differ from the repository branch or earlier run.
    sources: []
  - id: S-Jira
    name: Jira integration and project connection
    owner: aws
    kind: service configuration
    identity: Selected integration and destination project
    scope: Configured finding publication
    meaning: Destination authorization is separate from source access and assessment execution.
    sources:
    - SS58
  - id: S-Issue
    name: Jira issue
    owner: external
    kind: external work record
    identity: Jira issue key
    scope: Selected project and audience
    meaning: External finding handoff; disconnecting an integration is not issue deletion.
    sources: []
  - id: S-CodeSettings
    name: Repository code-review settings
    owner: aws
    kind: service configuration
    identity: Settings on the connected repository
    scope: Agent Space source connection
    meaning:
      $markdown: field-0008
    sources:
    - SS50
  - id: S-RemediationSettings
    name: Remediation repository settings
    owner: aws
    kind: service configuration
    identity: Eligible source repositories and feature settings
    scope: Application Agent Space
    meaning:
      $markdown: field-0009
    sources:
    - SS50
    - SS55
  - id: S-CodeFinding
    name: Code-review finding
    owner: aws
    kind: result record
    identity: Review identity, source revision and finding location
    scope: Source-code review
    meaning:
      $markdown: field-0010
    sources:
    - SS50
  relationships:
  - id: SR01
    from: S-Tenant
    to: S-Space
    verb: organizes application scopes
    targets: 0..*
    sources_per_target: '1'
    basis: logical
    note: Scope hierarchy from the guide, not an AWS Organizations API schema.
    sources:
    - SS50
  - id: SR02
    from: S-Registration
    to: S-Connection
    verb: authorizes selection
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Provider-specific setup precedes selecting application sources.
    sources:
    - SS51
  - id: SR03
    from: S-Space
    to: S-Connection
    verb: selects sources
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Connection scope is application-specific.
    sources:
    - SS50
    - SS51
  - id: SR04
    from: S-Connection
    to: S-Repository
    verb: references source
    targets: '?'
    sources_per_target: 0..*
    basis: documented
    note:
      $markdown: field-0011
    sources:
    - SS50
  - id: SR05
    from: S-Tenant
    to: S-Pack
    verb: shares criteria
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Requirements affect future eligible reviews across spaces, not past results.
    sources:
    - SS50
    - SS53
  - id: SR06
    from: S-Pack
    to: S-Requirement
    verb: contains
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note:
      $markdown: field-0012
    sources:
    - SS53
  - id: SR07
    from: S-Space
    to: S-Pentest
    verb: contains configuration
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Different test targets or scopes can have separate definitions.
    sources:
    - SS50
  - id: SR08
    from: S-Pentest
    to: S-Run
    verb: is executed as
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Create once, execute repeatedly; runs are independent.
    sources:
    - SS50
  - id: SR09
    from: S-Pentest
    to: S-Credential
    verb: configures identities
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0013
    sources:
    - SS52
  - id: SR10
    from: S-Pentest
    to: S-Rules
    verb: sets target boundary
    targets: '?'
    sources_per_target: '1'
    basis: documented
    note: Rule collections are members of configuration, not independently authorized workloads.
    sources:
    - SS56
  - id: SR11
    from: S-Credential
    to: S-Login
    verb: supports learned navigation
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0014
    sources:
    - SS52
  - id: SR12
    from: S-Run
    to: S-Finding
    verb: produces evidence
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: An absence of findings does not establish complete authenticated coverage.
    sources:
    - SS50
    - SS54
  - id: SR13
    from: S-Finding
    to: S-SelectedResult
    verb: is evaluated in
    targets: 0..*
    sources_per_target: '1'
    basis: editorial
    note: Normalized lineage association; each pair records one finding's result for one job.
    sources:
    - SS54
  - id: SR14
    from: S-Revalidation
    to: S-SelectedResult
    verb: reports selected results
    targets: 1..*
    sources_per_target: '1'
    basis: editorial
    note:
      $markdown: field-0015
    sources:
    - SS54
  - id: SR15
    from: S-CodeConfig
    to: S-CodeRun
    verb: starts full-source scans
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0016
    sources:
    - SS50
  - id: SR16
    from: S-Design
    to: S-Design
    verb: clones to a new review
    targets: 0..*
    sources_per_target: 0..1
    basis: logical
    note:
      $markdown: field-0017
    sources:
    - SS50
  - id: SR17
    from: S-ThreatConfig
    to: S-ThreatRun
    verb: is executed as
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Reusable configuration is distinct from its system overview and threat results.
    sources:
    - SS50
    - SS57
  - id: SR18
    from: S-Pack
    to: S-CodeRun
    verb: supplies enabled criteria
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0018
    sources:
    - SS53
  - id: SR19
    from: S-Pack
    to: S-Design
    verb: supplies enabled criteria
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: Shared requirements do not imply a mutable result shared between applications.
    sources:
    - SS53
  - id: SR20
    from: S-Finding
    to: S-Remediation
    verb: initiates proposal work
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: Eligible automatic or manual remediation remains distinct from deployment.
    sources:
    - SS55
  - id: SR21
    from: S-Remediation
    to: S-Patch
    verb: produces proposed change
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note: The output depends on provider and repository support; not every attempt succeeds.
    sources:
    - SS55
  - id: SR22
    from: S-Run
    to: S-Target
    verb: assesses running system
    targets: '?'
    sources_per_target: 0..*
    basis: documented
    note: Target reachability, role and deployed revision must be recorded per run.
    sources:
    - SS56
  - id: SR23
    from: S-Revalidation
    to: S-Target
    verb: retests selected evidence
    targets: '?'
    sources_per_target: 0..*
    basis: documented
    note: Repair must reach the original environment; current authentication is used.
    sources:
    - SS54
  - id: SR24
    from: S-Finding
    to: S-Issue
    verb: may be linked
    targets: '?'
    sources_per_target: '?'
    basis: documented
    note:
      $markdown: field-0019
    sources:
    - SS54
    - SS58
  - id: SR25
    from: S-CodeSettings
    to: S-CodeRun
    verb: enables change-triggered reviews
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Provider-specific events and source revision identify the change-review path.
    sources:
    - SS50
  - id: SR26
    from: S-RemediationSettings
    to: S-Remediation
    verb: permits proposal generation
    targets: 0..*
    sources_per_target: '?'
    basis: documented
    note: Provider eligibility and the accepted finding remain required.
    sources:
    - SS55
  - id: SR27
    from: S-CodeRun
    to: S-CodeFinding
    verb: produces source findings
    targets: 0..*
    sources_per_target: '1'
    basis: documented
    note: Keep source-review results distinct from running-application findings.
    sources:
    - SS50
  feature_bindings:
    FT-S-SOURCES:
    - S-Space
    - S-Registration
    - S-Connection
    - S-Repository
    FT-S-TARGET:
    - S-Pentest
    - S-Rules
    - S-Target
    FT-S-AUTH:
    - S-Credential
    - S-Run
    FT-S-LOGIN:
    - S-Login
    - S-Credential
    FT-S-RUNS:
    - S-Pentest
    - S-Run
    FT-S-FINDINGS:
    - S-Finding
    - S-CodeFinding
    FT-S-FIX:
    - S-Remediation
    - S-Patch
    - S-RemediationSettings
    FT-S-REVALIDATION:
    - S-Revalidation
    - S-Finding
    - S-SelectedResult
    FT-S-REQUIREMENTS:
    - S-Pack
    - S-Requirement
    FT-S-CODE:
    - S-CodeConfig
    - S-CodeRun
    - S-CodeSettings
    FT-S-DESIGN:
    - S-Design
    - S-Repository
    FT-S-THREAT:
    - S-ThreatConfig
    - S-ThreatRun
    - S-Repository
    FT-S-PIPELINE:
    - S-Pentest
    - S-Run
    FT-S-JIRA:
    - S-Jira
    - S-Issue
    - S-Finding
  views:
  - key: er-security-scope
    title: 'Security Agent: shared configuration and application scope'
    sections:
    - S-01
    - S-10
    nodes:
    - S-Tenant
    - S-Space
    - S-Registration
    - S-Connection
    - S-Repository
    - S-Pack
    - S-Requirement
    - S-Pentest
    edges:
    - SR01
    - SR02
    - SR03
    - SR04
    - SR05
    - SR06
    - SR07
  - key: er-security-assessments
    title: 'Security Agent: assessment configurations and executions'
    sections:
    - S-10
    - S-06
    nodes:
    - S-Pentest
    - S-Run
    - S-CodeConfig
    - S-CodeRun
    - S-Design
    - S-ThreatConfig
    - S-ThreatRun
    - S-Pack
    edges:
    - SR08
    - SR15
    - SR16
    - SR17
    - SR18
    - SR19
  - key: er-security-lineage
    title: 'Security Agent: finding, repair and revalidation lineage'
    sections:
    - S-11
    - S-M05
    nodes:
    - S-Run
    - S-Finding
    - S-Revalidation
    - S-SelectedResult
    - S-Remediation
    - S-Patch
    - S-Target
    - S-Issue
    edges:
    - SR12
    - SR13
    - SR14
    - SR20
    - SR21
    - SR22
    - SR23
    - SR24
---

<!-- block: b-2d32f70141e25006a804 -->
## entities / 0 / meaning

<!-- block: b-00e9428bdb145f6cbf38 -->
<!-- field: field-0001 -->
The documented shared layer; do not equate it with a new AWS Organizations resource or infer cross-account policy propagation.
<!-- /field -->

<!-- block: b-223ae6e1f2c45b85a186 -->
## entities / 9 / meaning

<!-- block: b-5c16b838d0225cd982ba -->
<!-- field: field-0002 -->
Credential strategy and login instructions; obtaining a secret is distinct from authentication.
<!-- /field -->

<!-- block: b-2f1f0116e60b539b9c02 -->
## entities / 13 / meaning

<!-- block: b-15f0a4be16b05f55a0a9 -->
<!-- field: field-0003 -->
Retests selected evidence; it neither replaces the original finding nor performs broad discovery.
<!-- /field -->

<!-- block: b-58e4ba44e4df5df2b207 -->
## entities / 14 / meaning

<!-- block: b-08b9534ba5765c6a803f -->
<!-- field: field-0004 -->
Captures the reported result for a selected finding. This is not asserted to be a separate AWS API resource.
<!-- /field -->

<!-- block: b-b034f1a5640e5d90b1a6 -->
## entities / 15 / meaning

<!-- block: b-6fe1102c189553078136 -->
<!-- field: field-0005 -->
Reusable selection of repositories or S3 sources for full scans; repository-event review settings are modeled separately.
<!-- /field -->

<!-- block: b-1c8fd555866a5323b81c -->
## entities / 17 / meaning

<!-- block: b-1b45fdb96fad559fb040 -->
<!-- field: field-0006 -->
Analyze submitted design material once; clone creates a new review rather than rerunning the same object.
<!-- /field -->

<!-- block: b-bbdfb400e7855208a798 -->
## entities / 20 / meaning

<!-- block: b-e9474b6bc550580b96e5 -->
<!-- field: field-0007 -->
Finding-linked attempt to produce a code proposal; it is not the repository settings or the resulting deployment.
<!-- /field -->

<!-- block: b-04a9d40097635e2e9dc0 -->
## entities / 25 / meaning

<!-- block: b-8d9345457d075bdb8abf -->
<!-- field: field-0008 -->
Controls eligible change review, selected analysis modes and comments. These settings are not the full-scan configuration.
<!-- /field -->

<!-- block: b-c3f13763d3d458eaad77 -->
## entities / 26 / meaning

<!-- block: b-abb6b2182c1959b489e7 -->
<!-- field: field-0009 -->
Determines where supported fix proposals can be created. Settings alone do not represent a remediation attempt.
<!-- /field -->

<!-- block: b-bb8f5707ede65c89b47e -->
## entities / 27 / meaning

<!-- block: b-9d971655c47a543bb95e -->
<!-- field: field-0010 -->
Static-analysis result with source evidence. Penetration-test revalidation is not inferred for this result type.
<!-- /field -->

<!-- block: b-1a515d5a03835f409f53 -->
## relationships / 3 / note

<!-- block: b-95ca41b52d515b6abf1a -->
<!-- field: field-0011 -->
A repository can be connected to multiple spaces. Provider-level connection grouping is not forced to one repository.
<!-- /field -->

<!-- block: b-8e9b88ac9c395fb78dd8 -->
## relationships / 5 / note

<!-- block: b-8dffedfc722d5a93877a -->
<!-- field: field-0012 -->
Each requirement belongs to a pack; custom packs may be created before adding requirements.
<!-- /field -->

<!-- block: b-e5a6df0a6cc45a08a77d -->
## relationships / 8 / note

<!-- block: b-8d3ef7aab8b85cdbb862 -->
<!-- field: field-0013 -->
Multiple credentials can represent different application roles; reuse constraints are not generalized.
<!-- /field -->

<!-- block: b-b6e04c7e4e4150e681fb -->
## relationships / 10 / note

<!-- block: b-d64b7d7e80525cf898b9 -->
<!-- field: field-0014 -->
The guide documents reuse, not an exact procedure-to-credential schema or separate skill management API.
<!-- /field -->

<!-- block: b-61626566aeb05db1850e -->
## relationships / 13 / note

<!-- block: b-3c57ef710bb151998630 -->
<!-- field: field-0015 -->
A job selects one or more findings. Pending or failed work may not yet have a conclusive result value.
<!-- /field -->

<!-- block: b-79ee85d878755417a2bf -->
## relationships / 14 / note

<!-- block: b-1cd205a6427e53ae9d84 -->
<!-- field: field-0016 -->
This relationship describes full scans. Repository-event reviews originate through their own connected-source settings.
<!-- /field -->

<!-- block: b-7146d2c18e4b5de5a6c8 -->
## relationships / 15 / note

<!-- block: b-53c2fa4b8e475085922d -->
<!-- field: field-0017 -->
New reviews may originate without a clone. This is a logical derivation, not a claimed clone-parent API field.
<!-- /field -->

<!-- block: b-59b0ef36af6954dd863e -->
## relationships / 17 / note

<!-- block: b-97f7d6078af358fdbce6 -->
<!-- field: field-0018 -->
Selected review modes and current pack enablement matter; existing reviews do not change retrospectively.
<!-- /field -->

<!-- block: b-906129db143850c79f61 -->
## relationships / 23 / note

<!-- block: b-3680a97fbb49591d849c -->
<!-- field: field-0019 -->
When linked, revalidation can add a result comment. No universal one-issue-per-finding rule is asserted.
<!-- /field -->
