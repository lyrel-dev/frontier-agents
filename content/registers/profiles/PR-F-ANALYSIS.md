---
id: record-profiles-PR-F-ANALYSIS
kind: record
collection: profiles
product: ''
title: Cost-analysis and report configuration
order: 7
frozen: true
data:
  id: PR-F-ANALYSIS
  title: Cost-analysis and report configuration
  platforms:
  - finops
  mechanisms:
  - MX-F-QUERY
  - MX-F-FILES
  - MX-F-MEMORY
  - MX-F-COMPACT
  - MX-F-TASK
  - MX-F-ARTIFACT
  parameters:
  - - Query basis
    - Dates, metric, currency, scope, dimensions and granularity
    - Complete comparable periods and explicitly chosen cost metric
  - - Analysis type
    - Observed cost, forecast, coverage or recommendation
    - Select the required upstream evidence
  - - Organization context
    - Optional reviewed ownership mapping
    - Active non-sensitive reference file
  - - Output
    - Result or supported report artifact
    - HTML report retaining source basis
  setup:
  - $markdown: field-0001
  - $markdown: field-0002
  - $markdown: field-0003
  tests:
  - $markdown: field-0004
  - $markdown: field-0005
  - $markdown: field-0006
  stop_behavior:
    $markdown: field-0007
---

<!-- block: b-11b6e70eec8c59eb831c -->
## setup / 0

<!-- block: b-aefa8181c2835296a815 -->
<!-- field: field-0001 -->
Verify the agent data role and relevant upstream service.
<!-- /field -->

<!-- block: b-b7ce87e317cd50b4b7d8 -->
## setup / 1

<!-- block: b-1867fbac9044542f97f4 -->
<!-- field: field-0002 -->
State material query choices even when preferences are retained.
<!-- /field -->

<!-- block: b-912daf4af16452bf8386 -->
## setup / 2

<!-- block: b-0ba214ebe4895b6299ed -->
<!-- field: field-0003 -->
Reconcile a material result independently and inspect task or artifact identity.
<!-- /field -->

<!-- block: b-850aae5776585af4a8b9 -->
## tests / 0

<!-- block: b-3fbf999e348159ed833c -->
<!-- field: field-0004 -->
Different filters invalidate a direct numerical comparison.
<!-- /field -->

<!-- block: b-0a66b54e1d92564a8c7f -->
## tests / 1

<!-- block: b-3235dcb810d55b98af64 -->
<!-- field: field-0005 -->
Forecasts and recommendation estimates are not added to observed costs.
<!-- /field -->

<!-- block: b-6a4a8f56ccf95c6fbde4 -->
## tests / 2

<!-- block: b-b50fb64cfa34563290f4 -->
<!-- field: field-0006 -->
Missing change evidence leaves causal attribution unresolved.
<!-- /field -->

<!-- block: b-d4aba3a2bc525018a5af -->
## stop behavior

<!-- block: b-014d486d873c5596aa00 -->
<!-- field: field-0007 -->
Cancel tasks and manage artifacts separately. This recipe authorizes neither infrastructure changes nor commitment purchases.
<!-- /field -->
