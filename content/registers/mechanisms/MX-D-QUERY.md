---
id: record-mechanisms-MX-D-QUERY
kind: record
collection: mechanisms
product: devops
title: Built-in operational inquiry
order: 39
frozen: true
data:
  id: MX-D-QUERY
  platform: devops
  title: Built-in operational inquiry
  features:
  - FT-D-QUERY
  - FT-D-SOURCES
  sections:
  - D-01
  - D-12
  - D-07
  trigger: A scoped conversational question
  state: Request context and connected source evidence
  process:
    $markdown: field-0001
  effect: Source read and conversational result
  verification: Inspect scope and reproduce a material observation from the same source query.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-07
    kind: Built-in inquiry workflow
    inputs: Explicit question, service/account scope, observation interval and connected evidence.
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Scope
      - Open Chat in the intended Agent Space and state service identifiers and UTC interval.
      - Current request
    - - Evidence
      - Check relevant source associations and permission scope.
      - Underlying read access
    lifecycle:
    - - Question submitted
      - Read available evidence
      - Response or source gap is produced.
    - - Question needs recurring execution
      - Define a custom task separately
      - A new configuration path, not automatic conversion.
    controls: A conversational request is not permission for a state-changing operation.
    observable_output: Scoped answer and available supporting tool observations.
    undocumented:
      $markdown: field-0005
    test:
    - Ask for one known staging service measurement in a complete interval.
    - Compare it with the monitoring source.
    - An unavailable metric must be listed as missing rather than inferred as healthy.
    claims:
    - source: DS407
      section: Custom agents compared to built-in capabilities
      assertion: On-demand queries are a built-in path; custom agents are separately configured.
    - source: DS401
      section: Configuring MCP tools in an Agent Space
      assertion: Connected evidence remains subject to selected source tools.
---

<!-- block: b-c824a48ccddb5a3ea9fe -->
## process

<!-- block: b-31a3730c368050178a5d -->
<!-- field: field-0001 -->
Use the built-in on-demand inquiry path to answer the operational question using available authorized evidence.
<!-- /field -->

<!-- block: b-7936c8f31d1f57a696c9 -->
## on failure

<!-- block: b-7bfad706d376565d946c -->
<!-- field: field-0002 -->
Name the missing source and qualify or withhold the answer; creating a custom agent does not by itself repair source access.
<!-- /field -->

<!-- block: b-6e8955252c525fb8a236 -->
## review / narrative / 0

<!-- block: b-b7ae7e10f91356548735 -->
<!-- field: field-0003 -->
The built-in inquiry path answers an operational question without requiring a separately created custom agent. It still depends on the Agent Space sources and permissions. Use a custom definition for a recurring or specialized procedure; configure source access independently.
<!-- /field -->

<!-- block: b-a793c02b18f8560681f6 -->
## review / narrative / 1

<!-- block: b-33fc9e34d22f56d7918c -->
<!-- field: field-0004 -->
The response is scoped to evidence actually available to that request. Record the queried period and reproduce a material observation before treating a health summary as an operational fact.
<!-- /field -->

<!-- block: b-a56da033eff95b829950 -->
## review / undocumented

<!-- block: b-644197fefdc65569b0b6 -->
<!-- field: field-0005 -->
The cited guide does not specify the query-selection algorithm. Inspect the sources and query parameters used by the execution.
<!-- /field -->
