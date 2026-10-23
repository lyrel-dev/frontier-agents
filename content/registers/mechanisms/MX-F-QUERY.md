---
id: record-mechanisms-MX-F-QUERY
kind: record
collection: mechanisms
product: finops
title: Source-backed cost analysis
order: 29
frozen: true
data:
  id: MX-F-QUERY
  platform: finops
  title: Source-backed cost analysis
  features:
  - FT-F-SOURCES
  sections:
  - F-M01
  - F-08
  trigger: Bounded cost, forecast, coverage or recommendation question
  state: Query contract and source response
  process:
    $markdown: field-0001
  effect: Source read
  verification: Reconcile a material result using the same dates, metric, scope and dimensions.
  on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  review:
    primary_section: F-M01
    kind: Source-backed analytical workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Source
      - Enable required upstream services and inspect the agent data role.
      - Permitted source evidence
    - - Query
      - State complete periods, metric, filters and grouping.
      - Explicit analytical basis
    - - Interpretation
      - Identify which source supplied a forecast, anomaly or recommendation.
      - Provenance of the returned value
    lifecycle:
    - - Question submitted
      - Query upstream service
      - Source result or access failure returned.
    - - Scope changed
      - Run a new query
      - New result is not comparable unless the basis is reconciled.
    - - Recommendation retrieved
      - Contextualize for owner review
      - No infrastructure change is authorized by retrieval.
    controls:
      $markdown: field-0005
    observable_output: Returned figures, query basis and source/tool evidence.
    undocumented:
      $markdown: field-0006
    test:
    - Use the supplied synthetic cost fixture or a read-only query in an authorized account.
    - Reconcile components to the total under identical periods and metric.
    - Change metric or period deliberately; identify why the totals are not comparable.
    claims:
    - source: FS401
      section: Related services
      assertion:
        $markdown: field-0007
    - source: FS407
      section: Generative AI accuracy considerations
      assertion: Recommendations are upstream analysis; anomaly causality remains investigative.
---

<!-- block: b-d35b46cce7e358b5a7fa -->
## process

<!-- block: b-3c66267ef6f851939793 -->
<!-- field: field-0001 -->
Read the relevant upstream service and interpret its returned evidence.
<!-- /field -->

<!-- block: b-b41e3759aa5e51218b19 -->
## review / inputs

<!-- block: b-24579945092b5b1293c5 -->
<!-- field: field-0002 -->
Question, dates, cost metric, scope, dimensions, currency and permissions to the relevant source service.
<!-- /field -->

<!-- block: b-6ad4566ad7a754749fa6 -->
## review / narrative / 0

<!-- block: b-d3fb91cceff3529c91b8 -->
<!-- field: field-0003 -->
The agent queries the service that owns the requested evidence. Historical cost, forecasts, commitment coverage, anomaly records, optimization recommendations and change events are different inputs. Combining them in one conversation does not turn projected savings into observed spend.
<!-- /field -->

<!-- block: b-6d289be89f9a5d8eac2b -->
## review / narrative / 1

<!-- block: b-e9a9cb81a23f5c6fadde -->
<!-- field: field-0004 -->
The analytical result must preserve the query basis. First reconcile amounts, then examine operational evidence for an explanation. A nearby change event is a lead; numerical contribution and causal attribution remain different claims.
<!-- /field -->

<!-- block: b-b7f35c476e355ea4a619 -->
## review / controls

<!-- block: b-7743776361805a6a912b -->
<!-- field: field-0005 -->
The service summarizes recommendations from optimization services; it does not independently calculate its own underlying optimization analysis.
<!-- /field -->

<!-- block: b-2c7118f03be553898d13 -->
## review / undocumented

<!-- block: b-fd9e86f1d226590aa496 -->
<!-- field: field-0006 -->
The source guides do not specify the query-planning algorithm. Queries with different dates, metrics or filters are not directly comparable.
<!-- /field -->

<!-- block: b-4fd5b4ac1a6a5decb0bb -->
## review / claims / 0 / assertion

<!-- block: b-813eacbf2f4b5fadb268 -->
<!-- field: field-0007 -->
Cost Explorer, anomaly detection, optimization services and CloudTrail supply distinct evidence.
<!-- /field -->
