---
id: record-mechanisms-MX-F-ARTIFACT
kind: record
collection: mechanisms
product: finops
title: Report generation and revision
order: 36
frozen: true
data:
  id: MX-F-ARTIFACT
  platform: finops
  title: Report generation and revision
  features:
  - FT-F-ARTIFACTS
  sections:
  - F-04
  trigger: Analysis requires a report artifact
  state: Report artifact, originating conversation or task, and query basis
  process:
    $markdown: field-0001
  effect: Report artifact
  verification: Compare displayed figures and period with the reviewed source analysis.
  on_failure: Do not distribute an artifact that no longer matches its query basis.
  review:
    primary_section: F-04
    kind: Analysis-to-artifact mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Request
      - $markdown: field-0005
      - Artifact instruction
    - - Inspect
      - Open/download from Artifacts and compare figures to source results.
      - Output review
    - - Revise
      - Reference the existing report in a follow-up and state whether the query basis may change.
      - Revision intent
    lifecycle:
    - - Analysis available
      - Generate report
      - Artifact delivered.
    - - Artifact exists
      - Request revision
      - Updated presentation can be produced.
    - - Service artifact removed
      - External copies remain
      - Downloaded or published copies require separate handling.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Generate a report from the small supplied synthetic cost fixture.
    - Reconcile displayed components and totals to the fixture.
    - Revise layout only and verify that period, metric and numbers did not change.
    claims:
    - source: FS406
      section: Generating cost reports
      assertion: Reports are artifacts, default to HTML and can be revised through follow-up.
    - source: FS403
      section: Managing your data
      assertion: Artifacts and other retained objects have distinct controls.
---

<!-- block: b-041c3093cd3456679d2c -->
## process

<!-- block: b-b6494eff2bbc5127af6e -->
<!-- field: field-0001 -->
Format supported output and revise it without silently changing analytical scope.
<!-- /field -->

<!-- block: b-4fe0cc26e7b95f95a94a -->
## review / inputs

<!-- block: b-1ea3743b9f4c56efbfd5 -->
<!-- field: field-0002 -->
Cost-report request, authorized source access, query parameters, output format and optional report template.
<!-- /field -->

<!-- block: b-cc147a336cd551a4a1e6 -->
## review / narrative / 0

<!-- block: b-77325da786265852bdbd -->
<!-- field: field-0003 -->
Report generation retrieves source data, builds the requested presentation and returns an artifact. A visual quality pass concerns presentation defects; it is not an independent reconciliation of the underlying financial interpretation.
<!-- /field -->

<!-- block: b-f09aaf763c635fd39c86 -->
## review / narrative / 1

<!-- block: b-2f0b63b0746e5b40bf45 -->
<!-- field: field-0004 -->
A follow-up can revise the artifact. Keep the analytical basis explicit when revising it: changing a title or chart layout should not silently change period, cost metric or grouping.
<!-- /field -->

<!-- block: b-956ffeb1e83b57f5b304 -->
## review / configuration / 0 / 1

<!-- block: b-309937f9c1df5881b78a -->
<!-- field: field-0005 -->
Specify report audience, source period, metric, required sections and supported format; default is HTML.
<!-- /field -->

<!-- block: b-6a98d3d726515d32b1e4 -->
## review / controls

<!-- block: b-08ce8805567d5c1789aa -->
<!-- field: field-0006 -->
Formatting and completion status do not establish numerical accuracy; distribution is a separate effect.
<!-- /field -->

<!-- block: b-57bc911edd3f59019e5a -->
## review / observable output

<!-- block: b-55becf7dbb025e049c46 -->
<!-- field: field-0007 -->
Report artifact and its source conversation or task. Record the query parameters and output identity used for reconciliation.
<!-- /field -->

<!-- block: b-9916d49bc705501a9fb9 -->
## review / undocumented

<!-- block: b-d70c7ecfa25152228ff8 -->
<!-- field: field-0008 -->
An immutable artifact-version API and universal external-copy deletion are not established by the report guide.
<!-- /field -->
