---
id: register-mechanisms
kind: register
collection: mechanisms
title: mechanisms register
frozen: true
json_format:
  indent: 2
  ensure_ascii: false
  newline: true
data:
  schema_version: 2
  boundary:
    $markdown: field-0001
  entries:
  - $record: record-mechanisms-MX-D-READ
  - $record: record-mechanisms-MX-D-TOPOLOGY
  - $record: record-mechanisms-MX-D-RECALL
  - $record: record-mechanisms-MX-D-FEEDBACK
  - $record: record-mechanisms-MX-D-INSTRUCTIONS
  - $record: record-mechanisms-MX-D-SKILL
  - $record: record-mechanisms-MX-D-TRIAGE
  - $record: record-mechanisms-MX-D-INVESTIGATE
  - $record: record-mechanisms-MX-D-CUSTOM
  - $record: record-mechanisms-MX-D-SCHEDULE
  - $record: record-mechanisms-MX-D-PREVENT
  - $record: record-mechanisms-MX-D-ACTION
  - $record: record-mechanisms-MX-D-READINESS
  - $record: record-mechanisms-MX-D-TEST
  - $record: record-mechanisms-MX-S-CONTEXT
  - $record: record-mechanisms-MX-S-ACCESS
  - $record: record-mechanisms-MX-S-AUTH
  - $record: record-mechanisms-MX-S-LOGIN
  - $record: record-mechanisms-MX-S-RUN
  - $record: record-mechanisms-MX-S-FINDING
  - $record: record-mechanisms-MX-S-FIX
  - $record: record-mechanisms-MX-S-REVALIDATE
  - $record: record-mechanisms-MX-S-CRITERIA
  - $record: record-mechanisms-MX-S-GENERATE
  - $record: record-mechanisms-MX-S-CODE
  - $record: record-mechanisms-MX-S-DESIGN
  - $record: record-mechanisms-MX-S-THREAT
  - $record: record-mechanisms-MX-S-PIPELINE
  - $record: record-mechanisms-MX-S-JIRA
  - $record: record-mechanisms-MX-F-QUERY
  - $record: record-mechanisms-MX-F-FILES
  - $record: record-mechanisms-MX-F-MEMORY
  - $record: record-mechanisms-MX-F-COMPACT
  - $record: record-mechanisms-MX-F-TASK
  - $record: record-mechanisms-MX-F-SCHEDULE
  - $record: record-mechanisms-MX-F-EVENT
  - $record: record-mechanisms-MX-F-ARTIFACT
  - $record: record-mechanisms-MX-F-JIRA
  - $record: record-mechanisms-MX-F-SLACK
  - $record: record-mechanisms-MX-D-QUERY
  - $record: record-mechanisms-MX-S-PERSONALIZE
  review_sources:
    DS401:
      url:
        $markdown: field-0002
      scope: MCP registration, authentication, association and removal
      reviewed_on: '2026-10-22'
    DS402:
      url:
        $markdown: field-0003
      scope:
        $markdown: field-0004
      reviewed_on: '2026-10-22'
    DS403:
      url:
        $markdown: field-0005
      scope:
        $markdown: field-0006
      reviewed_on: '2026-10-22'
    DS404:
      url:
        $markdown: field-0007
      scope: Signal routing, investigation creation, steering and corrective feedback
      reviewed_on: '2026-10-22'
    DS405:
      url:
        $markdown: field-0008
      scope: Session-start loading and propagation; UI navigation differs between retrieved versions
      reviewed_on: '2026-10-22'
    DS406:
      url:
        $markdown: field-0009
      scope: Skill descriptions, targeting and document/code boundaries
      reviewed_on: '2026-10-22'
    DS407:
      url:
        $markdown: field-0010
      scope: Definition loading, selected tools and recorded invocation
      reviewed_on: '2026-10-22'
    DS408:
      url:
        $markdown: field-0011
      scope: Invocation, trigger creation, pause/delete and cancellation
      reviewed_on: '2026-10-22'
    DS409:
      url: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CronSchedule.html
      scope: Flexible window of up to 30 minutes; indexed API reference retrieved
      reviewed_on: '2026-10-22'
    DS410:
      url:
        $markdown: field-0012
      scope: Evaluation, recommendation disposition and recommendation lifecycle
      reviewed_on: '2026-10-22'
    DS411:
      url:
        $markdown: field-0013
      scope: Independent authorization gates, preference replacement and scoped approval
      reviewed_on: '2026-10-22'
    DS412:
      url:
        $markdown: field-0014
      scope: Candidate analysis, independent verification option and result categories
      reviewed_on: '2026-10-22'
    DS413:
      url:
        $markdown: field-0015
      scope:
        $markdown: field-0016
      reviewed_on: '2026-10-22'
    DS414:
      url:
        $markdown: field-0017
      scope: Custom definition creation and tool assignment
      reviewed_on: '2026-10-22'
    DS415:
      url:
        $markdown: field-0018
      scope: Feature-specific preview availability
      reviewed_on: '2026-10-22'
    SS401:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
      scope: Account registrations, space resource selection and separate write opt-ins
      reviewed_on: '2026-10-22'
    SS402:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
      scope: Target/access/exclusion distinction, credentials and saved assessment
      reviewed_on: '2026-10-22'
    SS403:
      url:
        $markdown: field-0019
      scope:
        $markdown: field-0020
      reviewed_on: '2026-10-22'
    SS404:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
      scope: Configuration/run models and one-off design reviews
      reviewed_on: '2026-10-22'
    SS405:
      url:
        $markdown: field-0021
      scope:
        $markdown: field-0022
      reviewed_on: '2026-10-22'
    SS406:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
      scope:
        $markdown: field-0023
      reviewed_on: '2026-10-22'
    SS407:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
      scope: Selected finding replay, Active/Resolved results and preserved lineage
      reviewed_on: '2026-10-22'
    SS408:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
      scope: Pack applicability, evaluation and future-review scope
      reviewed_on: '2026-10-22'
    SS409:
      url:
        $markdown: field-0024
      scope: Generation replaces pack contents including manual requirements
      reviewed_on: '2026-10-22'
    SS410:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html
      scope: Source selection, scan modes and preflight
      reviewed_on: '2026-10-22'
    SS411:
      url:
        $markdown: field-0025
      scope: Change triggers and repository filtering guidance
      reviewed_on: '2026-10-22'
    SS412:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html
      scope: Design statuses including Insufficient data and clone/new review behavior
      reviewed_on: '2026-10-22'
    SS413:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
      scope: Scope documents, source context, system overview and threat review
      reviewed_on: '2026-10-22'
    SS414:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html
      scope: Saved test prerequisite, CI/CD mode, OIDC, deployed-change scope and server-side execution
      reviewed_on: '2026-10-22'
    SS415:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
      scope: Project selection and separate issue/comment permissions
      reviewed_on: '2026-10-22'
    SS416:
      url:
        $markdown: field-0026
      scope: One issue per selected finding and Task issue-type prerequisite
      reviewed_on: '2026-10-22'
    SS417:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/remove-jira.html
      scope: Removal blocks future integration actions without deleting existing issues
      reviewed_on: '2026-10-22'
    SS418:
      url: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart.html
      scope: Save versus execute, preflight and result inspection
      reviewed_on: '2026-10-22'
    FS401:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
      scope: Source-service responsibilities for observed cost, forecasts, coverage and recommendations
      reviewed_on: '2026-10-22'
    FS402:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
      scope: Uploaded files, conversational memory and automatic compaction
      reviewed_on: '2026-10-22'
    FS403:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
      scope: Session runtime, instance isolation and object-specific removal
      reviewed_on: '2026-10-22'
    FS404:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
      scope: Explicit task requests, shared queue, schedules and event tasks
      reviewed_on: '2026-10-22'
    FS405:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
      scope: Monitor event, managed-rule permissions, automation and destination setup
      reviewed_on: '2026-10-22'
    FS406:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
      scope: Source query to report artifact and follow-up revision
      reviewed_on: '2026-10-22'
    FS407:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
      scope: Action/invocation-specific approval and analytical boundaries
      reviewed_on: '2026-10-22'
    FS408:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
      scope: Account registration, project connections and supported Jira operations
      reviewed_on: '2026-10-22'
    FS409:
      url: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
      scope: Workspace registration, channel binding, membership and one-way publication
      reviewed_on: '2026-10-22'
  reviewed_on: '2026-10-22'
  review_boundary:
    $markdown: field-0027
---

<!-- block: b-4692a9852b735155af7e -->
## boundary

<!-- block: b-a95232a575c45132b263 -->
<!-- field: field-0001 -->
This dependency index summarizes documented processes. Detailed explanations remain in the referenced guide sections. Verification and failure decisions are authored engineering checks, not executed tests.
<!-- /field -->

<!-- block: b-5f8b3236656e5864ad02 -->
## review sources / DS401 / url

<!-- block: b-db059af14e5054029386 -->
<!-- field: field-0002 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
<!-- /field -->

<!-- block: b-bbf386d12219598dbe48 -->
## review sources / DS402 / url

<!-- block: b-821d33ce7e2158cbb28a -->
<!-- field: field-0003 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
<!-- /field -->

<!-- block: b-c280beefed4a578cbbe3 -->
## review sources / DS402 / scope

<!-- block: b-9d9b638405de55dca951 -->
<!-- field: field-0004 -->
Memory production, progressive retrieval, versions and lifecycle; newer indexed text reviewed alongside older direct-page text
<!-- /field -->

<!-- block: b-f914a6019cf25cf9bf2c -->
## review sources / DS403 / url

<!-- block: b-3b9f6cf823ec54b99d0a -->
<!-- field: field-0005 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
<!-- /field -->

<!-- block: b-961703d0c4f35a3f94ad -->
## review sources / DS403 / scope

<!-- block: b-e09853c9a68c597e8386 -->
<!-- field: field-0006 -->
Discovery and topology representation; legacy learned-skill wording qualified by the current memory guide
<!-- /field -->

<!-- block: b-2127724e191158748219 -->
## review sources / DS404 / url

<!-- block: b-bd65395a5af4566a8d92 -->
<!-- field: field-0007 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html
<!-- /field -->

<!-- block: b-b0250eb3e49f50598bdb -->
## review sources / DS405 / url

<!-- block: b-b990381d39525aaaa826 -->
<!-- field: field-0008 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html
<!-- /field -->

<!-- block: b-357b985f3ec6578cb47d -->
## review sources / DS406 / url

<!-- block: b-59fd96a6030a594c8348 -->
<!-- field: field-0009 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html
<!-- /field -->

<!-- block: b-5f31b617d7845016aafd -->
## review sources / DS407 / url

<!-- block: b-7bfdaac1b3c85ea0b967 -->
<!-- field: field-0010 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
<!-- /field -->

<!-- block: b-a640bc4e808f5c999470 -->
## review sources / DS408 / url

<!-- block: b-21d6e2120617558582f6 -->
<!-- field: field-0011 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
<!-- /field -->

<!-- block: b-a24c77b071ac5223b1fa -->
## review sources / DS410 / url

<!-- block: b-252e22d01c32595abd01 -->
<!-- field: field-0012 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html
<!-- /field -->

<!-- block: b-ba9f5149cf075b569a00 -->
## review sources / DS411 / url

<!-- block: b-11672786640252d88c7d -->
<!-- field: field-0013 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
<!-- /field -->

<!-- block: b-b5cebfcf46585fb59010 -->
## review sources / DS412 / url

<!-- block: b-8ac2170e000c518580cd -->
<!-- field: field-0014 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html
<!-- /field -->

<!-- block: b-aea44fb3dbd251b1a229 -->
## review sources / DS413 / url

<!-- block: b-6ad77806500f5137a1c0 -->
<!-- field: field-0015 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html
<!-- /field -->

<!-- block: b-bf4775bd8cce5a7fb76b -->
## review sources / DS413 / scope

<!-- block: b-00642385ca515c77bc44 -->
<!-- field: field-0016 -->
Test profiles, real application requests and results; conflicting action names in the page are not copied
<!-- /field -->

<!-- block: b-679bf278bd2059e1ab0c -->
## review sources / DS414 / url

<!-- block: b-5a05952f49155aa5acb0 -->
<!-- field: field-0017 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html
<!-- /field -->

<!-- block: b-3b9e330f502d5524a293 -->
## review sources / DS415 / url

<!-- block: b-2078fe88f0cf57b8b5ed -->
<!-- field: field-0018 -->
https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html
<!-- /field -->

<!-- block: b-b69c4b661b095761a9da -->
## review sources / SS403 / url

<!-- block: b-9cb61c2a36705d928bb9 -->
<!-- field: field-0019 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
<!-- /field -->

<!-- block: b-474da891e8845a73bccd -->
## review sources / SS403 / scope

<!-- block: b-7319eb1b06225f49a5bd -->
<!-- field: field-0020 -->
Credential resolution and retained login procedure; navigation/authentication coverage differs across retrieved page versions
<!-- /field -->

<!-- block: b-1bac02fde9bf5865a48d -->
## review sources / SS405 / url

<!-- block: b-d89c84967ad9592c8d90 -->
<!-- field: field-0021 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html
<!-- /field -->

<!-- block: b-c5e1d9c0a9015606b7a0 -->
## review sources / SS405 / scope

<!-- block: b-29bb7d471ada527889a1 -->
<!-- field: field-0022 -->
Findings, confidence filter, original/latest edits and Findings Personalization; newer indexed official page reviewed
<!-- /field -->

<!-- block: b-560b1c3b035b55caba56 -->
## review sources / SS406 / scope

<!-- block: b-8ded2d2228695275b576 -->
<!-- field: field-0023 -->
Private repository proposals and S3 diffs; newer indexed provider wording supersedes older GitHub-only description
<!-- /field -->

<!-- block: b-90238fe2c8855126ab79 -->
## review sources / SS409 / url

<!-- block: b-5e16091aab69561faefc -->
<!-- field: field-0024 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html
<!-- /field -->

<!-- block: b-5d10d82cc80a5b368e2c -->
## review sources / SS411 / url

<!-- block: b-1bc2e318a6e15544a8b2 -->
<!-- field: field-0025 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html
<!-- /field -->

<!-- block: b-386ed71e3dc25f5b9e10 -->
## review sources / SS416 / url

<!-- block: b-f539d4b0b0e954ff9368 -->
<!-- field: field-0026 -->
https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html
<!-- /field -->

<!-- block: b-d55f9fa730e15a3d83de -->
## review boundary

<!-- block: b-4209066a63255c91a4f6 -->
<!-- field: field-0027 -->
Detailed mechanism prose is maintained here and rendered into delimited guide sections. Tests and failure decisions are proposed engineering guidance, not live results.
<!-- /field -->
