---
id: record-use-cases-UC-F04
kind: record
collection: use-cases
product: finops
title: Prepare a periodic cost report
order: 25
frozen: true
data:
  id: UC-F04
  platform: finops
  group: Cost reporting
  title: Prepare a periodic cost report
  summary: Produce a comparable report for the defined period and audience.
  delivery: Configured recurring task
  cadence: Scheduled
  availability: Preview
  inputs: Report contract, schedule, source scope, context and recipients.
  output: HTML, PDF or editable presentation artifact.
  sections:
  - F-03
  - F-04
  - F-M01
  - F-08
  - F-M02
  - F-05
  - F-M06
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - recurring report
  - daily report
  - weekly report
  - monthly report
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: FinOps reporting owner
  objective: Produce a comparable report for the defined period and audience.
  completion:
  - Period and cost basis remain consistent.
  - Observed values, projections and estimates are separated.
  - The artifact matches its reviewed task and source evidence.
  profiles:
  - PR-F-ANALYSIS
  - PR-F-AUTOMATION
  - PR-F-PUBLICATION
  variants:
  - name: On-demand period report
    changes: Create one report for a specified complete period.
    controls: No recurring automation is required.
  - name: Recurring report
    changes: Select a supported schedule.
    controls: The schedule does not define the analytical time window.
  - name: External distribution
    changes: Select an eligible configured destination.
    controls: Destination and invocation-specific authorization must be reviewed separately.
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC05
  aliases:
  - Daily, weekly or monthly cost report
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Read report evidence
    purpose:
      $markdown: field-0006
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Apply approved reporting context
    purpose:
      $markdown: field-0007
    mechanism: MX-F-FILES
    dependency: optional
    condition: Organization-specific reference material is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-FILES
    effect: Context read
    verification: Verify a known mapping and expose unmapped records.
    on_failure: Keep unassigned values visible and update the authoritative file deliberately.
  - title: Run the report task
    purpose:
      $markdown: field-0008
    mechanism: MX-F-TASK
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-TASKS
    effect: Execution and output
    verification: Match completed results to task identity and requested scope.
    on_failure: Distinguish absent, queued and failed tasks before retrying.
  - title: Generate the reviewed artifact
    purpose:
      $markdown: field-0009
    mechanism: MX-F-ARTIFACT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-ARTIFACTS
    effect: Report artifact
    verification: Compare displayed figures and period with the reviewed source analysis.
    on_failure: Do not distribute an artifact that no longer matches its query basis.
  - title: Repeat on a schedule
    purpose:
      $markdown: field-0010
    mechanism: MX-F-SCHEDULE
    dependency: conditional
    condition: Recurring execution is enabled.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-AUTOMATIONS
    - FT-F-TASKS
    effect: Future tasks
    verification: Inspect trigger and the actual task's reporting window separately.
    on_failure: Disable future starts and control already-created work separately.
  - title: Publish to the configured Jira destination
    actor: Service execution; accountable engineer reviews the result
    purpose:
      $markdown: field-0011
    mechanism: MX-F-JIRA
    dependency: optional
    condition: Jira distribution is selected and invocation-specific authorization is satisfied.
    configuration_features:
    - FT-F-JIRA
    effect: External publication
    verification: Inspect invocation type, action details, destination and resulting issue or comment.
    on_failure:
      $markdown: field-0012
  - title: Publish to the configured Slack channel
    actor: Service execution; accountable engineer reviews the result
    purpose:
      $markdown: field-0013
    mechanism: MX-F-SLACK
    dependency: optional
    condition: Slack distribution is selected; audience review occurs before direct publication.
    configuration_features:
    - FT-F-SLACK
    effect: External publication
    verification: Review audience before invocation and inspect delivery afterward.
    on_failure:
      $markdown: field-0014
---

<!-- block: b-3545caf01cab5d1c8173 -->
## constraints

<!-- block: b-1d99608fe74552d38843 -->
<!-- field: field-0001 -->
Schedule, source window and audience are separate settings. Report values still require reconciliation.
<!-- /field -->

<!-- block: b-237d5dc660a25dd59e19 -->
## example

<!-- block: b-d9c358dc3f1757e88b9e -->
<!-- field: field-0002 -->
Create a weekly cost report with service totals, anomalies, recommendations, owners and unresolved gaps.
<!-- /field -->

<!-- block: b-6c9df9a2799a5c26bb14 -->
## narrative / 0

<!-- block: b-c58aa0dae70d53a28c19 -->
<!-- field: field-0003 -->
The team needs a recurring cost report with a stable comparison basis. Define the reporting period, sections, dimensions, audience, and output format before scheduling it. The task should distinguish observed spend, anomalies, and source recommendation estimates so unlike values are not added together.
<!-- /field -->

<!-- block: b-9932fd27f7755b09b0a5 -->
## narrative / 1

<!-- block: b-8fa30dd658125b1c8595 -->
<!-- field: field-0004 -->
Review a trial artifact against the source totals and inspect the saved automation separately from the generated task. A weekly schedule does not specify whether the report includes an incomplete current day. Preserve the task identifier and query basis with each report so changes in the template do not obscure what was actually compared.
<!-- /field -->

<!-- block: b-cd279592f7885c198353 -->
## steps basis

<!-- block: b-9016955d28bb5a2088a3 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-46a52b87d09455b8aed4 -->
## workflow / 0 / purpose

<!-- block: b-8bc189c89c665df1b8df -->
<!-- field: field-0006 -->
Retrieve the declared period and comparison dimensions.
<!-- /field -->

<!-- block: b-5eceace085c155f5955a -->
## workflow / 1 / purpose

<!-- block: b-ce01bf21c79d5975b627 -->
<!-- field: field-0007 -->
Use maintained mappings and template.
<!-- /field -->

<!-- block: b-395daf6b5ea35c7abb3b -->
## workflow / 2 / purpose

<!-- block: b-550b857408fd52e99ab6 -->
<!-- field: field-0008 -->
Retain a separate execution identity.
<!-- /field -->

<!-- block: b-e320ca8f67b75ee9890d -->
## workflow / 3 / purpose

<!-- block: b-b25cab77cd295bce83dc -->
<!-- field: field-0009 -->
Provide the requested supported output format.
<!-- /field -->

<!-- block: b-edffa2c99c8e58a4a208 -->
## workflow / 4 / purpose

<!-- block: b-bb18f4f6fa6a5d08a5a8 -->
<!-- field: field-0010 -->
Create future reports under the same basis.
<!-- /field -->

<!-- block: b-e06d83fe9bf55e6eb15b -->
## workflow / 5 / purpose

<!-- block: b-b9609fee9ca5599e8dff -->
<!-- field: field-0011 -->
Create the supported report follow-up in the approved project.
<!-- /field -->

<!-- block: b-8aaac1d26a7e501bb416 -->
## workflow / 5 / on failure

<!-- block: b-8a41feac5e2757cdb6c9 -->
<!-- field: field-0012 -->
Stop incorrect destinations. Do not expect an interactive prompt to protect an unattended automation.
<!-- /field -->

<!-- block: b-6bb0612a67975843b7ef -->
## workflow / 6 / purpose

<!-- block: b-4396e882cc1b5e7c8990 -->
<!-- field: field-0013 -->
Deliver the permitted report summary to its reviewed audience.
<!-- /field -->

<!-- block: b-a134664264005b4d97ca -->
## workflow / 6 / on failure

<!-- block: b-c7ce82e1b38b51729b66 -->
<!-- field: field-0014 -->
Keep analysis completion separate from delivery failure; posting does not establish channel-reading capability.
<!-- /field -->
