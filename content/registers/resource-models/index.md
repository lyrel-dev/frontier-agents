---
id: register-resource-models
kind: register
collection: resource-models
title: resource-models register
frozen: true
json_format:
  indent: 2
  ensure_ascii: false
  newline: true
data:
  schema_version: 1
  reviewed_on: '2026-10-22'
  baseline: cd65b98e04e20e7a4bcf59165db7f98315417964
  scope:
    $markdown: field-0001
  boundary:
    $markdown: field-0002
  legend:
    documentation:
      label: Documentation-defined concept
      fill: '#DCEBFF'
      stroke: '#447AC2'
      tag: DOC
    aws:
      label: AWS-defined resource or documented concept
      fill: '#D9F2E5'
      stroke: '#348761'
      tag: AWS
    external:
      label: External system or engineering-owned artifact
      fill: '#FCE8D5'
      stroke: '#C78335'
      tag: EXT
  notation:
    range:
      $markdown: field-0003
    basis:
      $markdown: field-0004
    identity:
      $markdown: field-0005
    ownership:
      $markdown: field-0006
  concepts:
  - id: C-USECASE
    name: Use case
    owner: documentation
    definition:
      $markdown: field-0007
  - id: C-VARIANT
    name: Use-case variant
    owner: documentation
    definition:
      $markdown: field-0008
  - id: C-WORKFLOW
    name: Workflow
    owner: documentation
    definition:
      $markdown: field-0009
  - id: C-STEP
    name: Workflow step
    owner: documentation
    definition:
      $markdown: field-0010
  - id: C-CAPABILITY
    name: Capability group
    owner: documentation
    definition:
      $markdown: field-0011
  - id: C-MECHANISM
    name: Mechanism explanation
    owner: documentation
    definition:
      $markdown: field-0012
  - id: C-FEATURE
    name: Feature reference
    owner: documentation
    definition:
      $markdown: field-0013
  - id: C-PROFILE
    name: Implementation profile
    owner: documentation
    definition:
      $markdown: field-0014
  - id: C-BINDING
    name: Resource binding
    owner: documentation
    definition:
      $markdown: field-0015
  - id: X-EVIDENCE
    name: Source evidence
    owner: external
    definition:
      $markdown: field-0016
  - id: X-REVIEW
    name: Engineering review
    owner: external
    definition:
      $markdown: field-0017
  sources:
    DS50:
      url:
        $markdown: field-0018
      section: Agent Space scope and isolation
      basis: Retrieved official HTML
    DS51:
      url: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssociateService.html
      section: Request, Association response and replacement semantics
      basis: Retrieved official API reference
    DS52:
      url:
        $markdown: field-0019
      section: Asset types; custom_agent, memory_store, memory; metadata references
      basis: Updated official indexed text; cached HTML omits memory asset types
      qualification:
        $markdown: field-0020
    DS53:
      url:
        $markdown: field-0021
      section: Key concepts and execution; store attachment
      basis: Updated official indexed text; cached HTML omits memory attachment
    DS54:
      url:
        $markdown: field-0022
      section: Triggers, invocation history, cancellation and tool results
      basis: Retrieved official HTML
    DS55:
      url:
        $markdown: field-0023
      section: Store, memory, versions, retrieval and activation
      basis: Retrieved official HTML and indexed memory guidance
    DS56:
      url:
        $markdown: field-0024
      section: Incident triage, investigation and feedback
      basis: Retrieved official HTML
    DS57:
      url:
        $markdown: field-0025
      section: Opt-in, account role, tool category, per-action approval and attribution
      basis: Retrieved official HTML
    DS58:
      url:
        $markdown: field-0026
      section: Resource discovery, views and scope beyond topology
      basis: Retrieved official HTML
      qualification:
        $markdown: field-0027
    DS59:
      url:
        $markdown: field-0028
      section: Evaluations and recommendations
      basis: Retrieved official HTML; evaluation and recommendation relationship reviewed
    DS60:
      url:
        $markdown: field-0029
      section: Test profiles, executions and application effects
      basis: Retrieved official HTML
    DS61:
      url: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html
      section: Production operations, release review and on-demand inquiry
      basis: Retrieved official HTML
    DS62:
      url:
        $markdown: field-0030
      section: Account registration, space association, tool selection and authentication
      basis: Updated official indexed text
    SS50:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
      section: Tenant versus Agent Space scope; assessment lifecycles; repository reuse
      basis: Retrieved official HTML
    SS51:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
      section: Register once; connect selected sources; supported providers
      basis: Retrieved official HTML
    SS52:
      url:
        $markdown: field-0031
      section: Credential strategies, multiple credentials and Login Optimization
      basis: Retrieved official HTML; later indexed guidance retained for UI detail
    SS53:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
      section: Requirement membership, shared scope and activation
      basis: Retrieved official HTML
    SS54:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
      section: Selection of findings, job results and original-finding lineage
      basis: Retrieved official indexed text
    SS55:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
      section: Finding-linked remediation and provider-dependent output
      basis: Retrieved official HTML
    SS56:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
      section: Configuration, target rules, credentials and create versus execute
      basis: Retrieved official HTML; current guide retains newer wizard details
    SS57:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
      section: Scope documents, source context, configuration and run
      basis: Retrieved official HTML
    SS58:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
      section: Finding publication and project connection
      basis: Retrieved official indexed text; project selection and finding publication reviewed
    FS50:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
      section: Instance isolation; two roles; integration and connection setup
      basis: Retrieved official HTML
    FS51:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
      section:
        $markdown: field-0032
      basis: Retrieved official HTML
    FS52:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
      section: Conversation versus task; automations; queue; managed events
      basis: Retrieved official HTML
    FS53:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
      section: Files, persistent memory and conversation compaction
      basis: Retrieved official HTML
    FS54:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
      section: Session loading, retained records, isolation and deletion behavior
      basis: Retrieved official HTML
    FS55:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
      section: Account registration and agent-specific destination connection
      basis: Retrieved official HTML
    FS56:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
      section: Account registration, channel connection and one-way publication
      basis: Retrieved official HTML
    FS57:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
      section: Effect and invocation-specific approval; upstream evidence
      basis: Retrieved official HTML
    FS58:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
      section: Artifact production, revision and distribution
      basis: Retrieved official HTML
    DS63:
      url:
        $markdown: field-0033
      section: Platform-owned managed agents; Learning history and triggers versus incident roles
      basis: Retrieved current official indexed text; direct cached URL was unavailable
  products:
    devops:
      $record: model-devops
    security:
      $record: model-security
    finops:
      $record: model-finops
---

<!-- block: b-6804fabfb16c5515b54b -->
## scope

<!-- block: b-ea7ed4efb8575ecc8e25 -->
<!-- field: field-0001 -->
Product-specific specialization of the approved conceptual ER model. The thirty approved use cases and their identifiers remain unchanged.
<!-- /field -->

<!-- block: b-227562e4d71a5769b502 -->
## boundary

<!-- block: b-54cca204f4e557d195df -->
<!-- field: field-0002 -->
Logical documentation model, not an AWS database schema, SDK payload or shared runtime. Green means AWS defines the concept; it does not mean every green item has an independent ARN, CRUD API or equal availability. Relationship multiplicities are qualified individually and are not service quotas.
<!-- /field -->

<!-- block: b-7a80fa9f1a485d27b947 -->
## notation / range

<!-- block: b-be8f95a8f702504c8c24 -->
<!-- field: field-0003 -->
Each relationship records targets per source and sources per target. 0..* means optional repeated association, not unlimited quota; ? means that exact multiplicity is not established by the reviewed guidance.
<!-- /field -->

<!-- block: b-b5b9ecfebffb51628676 -->
## notation / basis

<!-- block: b-b754bc3c52d952738a2e -->
<!-- field: field-0004 -->
documented = relationship stated in the source; logical = useful documentation association inferred from described behavior, not a service foreign key; editorial = relationship introduced by this collection.
<!-- /field -->

<!-- block: b-2c3069dc6cdf53959cce -->
## notation / identity

<!-- block: b-4a836058ef9b57a5a115 -->
<!-- field: field-0005 -->
Only documented identifiers are named as API fields. Other identities are described by their console or application context. Composite identity descriptions in this file are documentation keys, not invented API parameters.
<!-- /field -->

<!-- block: b-2e77b732283d5ffcadf0 -->
## notation / ownership

<!-- block: b-1373195efd1654959eb2 -->
<!-- field: field-0006 -->
The color classifies the definition of a concept, not who authors its content, pays for it or approves its use. IAM roles and EventBridge rules are AWS-defined dependencies outside the agent service.
<!-- /field -->

<!-- block: b-931ab328bb4a54dda211 -->
## concepts / 0 / definition

<!-- block: b-95cae6ba622751c0b64d -->
<!-- field: field-0007 -->
An actor's operational objective and completion criteria; the approved catalog is authoritative.
<!-- /field -->

<!-- block: b-93677fb1d9cb5a44a3b0 -->
## concepts / 1 / definition

<!-- block: b-2804c6f26baa5029a208 -->
<!-- field: field-0008 -->
A scope or delivery variation that preserves the operational objective.
<!-- /field -->

<!-- block: b-8aec052d7ba25ec2b080 -->
## concepts / 2 / definition

<!-- block: b-eeef2b0602d457aebf1f -->
<!-- field: field-0009 -->
An authored ordered sequence of work and decisions; not a universal AWS Workflow resource.
<!-- /field -->

<!-- block: b-c727da64ab5f5419bedf -->
## concepts / 3 / definition

<!-- block: b-277ca13e2f89545585db -->
<!-- field: field-0010 -->
A bounded operation or team decision with dependencies, effects and failure handling.
<!-- /field -->

<!-- block: b-d11b6fa22e4959b69fe4 -->
## concepts / 4 / definition

<!-- block: b-b627c8675030506386bc -->
<!-- field: field-0011 -->
A grouping of reusable abilities, such as context reuse or controlled execution.
<!-- /field -->

<!-- block: b-3c4b33f951415dedacdf -->
## concepts / 5 / definition

<!-- block: b-7da368497565526d9486 -->
<!-- field: field-0012 -->
Our explanation of a documented process; its claims link to AWS sources and product features.
<!-- /field -->

<!-- block: b-b62434b050e05aada1be -->
## concepts / 6 / definition

<!-- block: b-0d7b18be2e7f5680be23 -->
<!-- field: field-0013 -->
An index record for a documented facility; it can map to several resources or behaviors.
<!-- /field -->

<!-- block: b-0fe20d939b5055a1889c -->
## concepts / 7 / definition

<!-- block: b-6c7d89d30c4c5908b079 -->
<!-- field: field-0014 -->
A reviewed configuration recipe, not a deployed AWS resource or API schema.
<!-- /field -->

<!-- block: b-48a91a9e3f3950d6a384 -->
## concepts / 8 / definition

<!-- block: b-98d7b4c9773f57b8adb6 -->
<!-- field: field-0015 -->
The explicit mapping from a feature reference to named product objects and external dependencies.
<!-- /field -->

<!-- block: b-a575bddc9a925858a546 -->
## concepts / 9 / definition

<!-- block: b-b3bd82c8ae365cf7a02c -->
<!-- field: field-0016 -->
Measurements, revisions and records retained by their source systems.
<!-- /field -->

<!-- block: b-5811f1b4a3cf5463912e -->
## concepts / 10 / definition

<!-- block: b-0867c33b60b558f39463 -->
<!-- field: field-0017 -->
The team's decision on the adequacy of evidence and acceptance of an outcome.
<!-- /field -->

<!-- block: b-7f19b7d62238538c987a -->
## sources / DS50 / url

<!-- block: b-251fd5e4733854a990be -->
<!-- field: field-0018 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html
<!-- /field -->

<!-- block: b-dc0b5bdd72365dba81ab -->
## sources / DS52 / url

<!-- block: b-96dc94a2e6765acdb35d -->
<!-- field: field-0019 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html
<!-- /field -->

<!-- block: b-503292a7ce805046ae30 -->
## sources / DS52 / qualification

<!-- block: b-0d4403b6f59a55b1a30a -->
<!-- field: field-0020 -->
Use the indexed eight-type list and asset-ID references, not the older six-type cached page. ListAssetTypes remains the runtime discovery operation.
<!-- /field -->

<!-- block: b-eee17c31049d5d629408 -->
## sources / DS53 / url

<!-- block: b-08cbf943c47b5f57ac38 -->
<!-- field: field-0021 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
<!-- /field -->

<!-- block: b-c95aa563dbe4588ea2f4 -->
## sources / DS54 / url

<!-- block: b-9dadb5bd3c975bdda3d9 -->
<!-- field: field-0022 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
<!-- /field -->

<!-- block: b-093271055c5c5cc6a510 -->
## sources / DS55 / url

<!-- block: b-87c3120516635882a7f2 -->
<!-- field: field-0023 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
<!-- /field -->

<!-- block: b-c97a3f4e45df5a45a3ee -->
## sources / DS56 / url

<!-- block: b-53faad1f2b0f5c2d8ff6 -->
<!-- field: field-0024 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html
<!-- /field -->

<!-- block: b-756fb0ff2ccb50529d07 -->
## sources / DS57 / url

<!-- block: b-07a3d556da58535186f8 -->
<!-- field: field-0025 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
<!-- /field -->

<!-- block: b-0de2e8e42553507c8ef6 -->
## sources / DS58 / url

<!-- block: b-0bcfac987d345c75a9f5 -->
<!-- field: field-0026 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
<!-- /field -->

<!-- block: b-e807ab78d93056b28316 -->
## sources / DS58 / qualification

<!-- block: b-3bf68eafa57554bb87e9 -->
<!-- field: field-0027 -->
Older topology prose calls learned knowledge skills. The model treats topology as a derived view without asserting a new independent storage API.
<!-- /field -->

<!-- block: b-644371abcaef53519afe -->
## sources / DS59 / url

<!-- block: b-661b52dda73753488079 -->
<!-- field: field-0028 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html
<!-- /field -->

<!-- block: b-dc8e044881ac534c84be -->
## sources / DS60 / url

<!-- block: b-a357319b796d597a8015 -->
<!-- field: field-0029 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
<!-- /field -->

<!-- block: b-ce7cce5f35225c56a222 -->
## sources / DS62 / url

<!-- block: b-045b22f6d7795b93839f -->
<!-- field: field-0030 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
<!-- /field -->

<!-- block: b-da66992a03d95938aeda -->
## sources / SS52 / url

<!-- block: b-0fa42a10abc6525bab4c -->
<!-- field: field-0031 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
<!-- /field -->

<!-- block: b-5dbee0a42d4d5d4abfeb -->
## sources / FS51 / section

<!-- block: b-b5eb3bea9dfe551285d2 -->
<!-- field: field-0032 -->
IAM responsibilities; finops-agent AgentSpace action and ARN names; managed-rule permissions
<!-- /field -->

<!-- block: b-fe34eb04c923501ebf98 -->
## sources / DS63 / url

<!-- block: b-3c50bc2d57415a61b1aa -->
<!-- field: field-0033 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html
<!-- /field -->
