---
id: record-mechanisms-MX-D-READ
kind: record
collection: mechanisms
product: devops
title: Evidence retrieval through selected tools
order: 0
frozen: true
data:
  id: MX-D-READ
  platform: devops
  title: Evidence retrieval through selected tools
  features:
  - FT-D-SOURCES
  sections:
  - D-03
  - D-12
  trigger: Scoped operational request
  state: Provider association and selected tools
  process:
    $markdown: field-0001
  effect: Source read
  verification: Compare returned identifiers and a material measurement with the original source.
  on_failure: Report the failed read and withhold conclusions that require that source.
  review:
    primary_section: D-03
    kind: Tool-access mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Registration
      - $markdown: field-0005
      - Account-level registration
    - - Association
      - $markdown: field-0006
      - Space-level tool selection
    - - Custom execution
      - Assign the actual tools to the custom definition.
      - Additional definition-level selection
    lifecycle:
    - - Registered
      - Associate selected tools
      - Tools become available to the space, not necessarily every custom definition.
    - - Associated
      - Remove connection
      - Future access through that association is removed.
    - - Registered credential changes
      - Follow provider re-registration procedure
      - Review dependent associations before replacing the registration.
    controls:
      $markdown: field-0007
    observable_output:
      $markdown: field-0008
    undocumented:
      $markdown: field-0009
    test:
    - Use a permitted staging read with a known resource and time interval.
    - Reproduce one returned measurement with the same source query.
    - $markdown: field-0010
    claims:
    - source: DS401
      section: Registering an MCP server; Configuring MCP tools; Managing connections
      assertion:
        $markdown: field-0011
    - source: DS407
      section: How custom agents work
      assertion: A custom agent accesses only its assigned tools.
---

<!-- block: b-b95529a1d84f5321841d -->
## process

<!-- block: b-7c3a196cbc8956bca3af -->
<!-- field: field-0001 -->
Invoke the authorized source with the intended identity, resource and observation period.
<!-- /field -->

<!-- block: b-d1ff1d58fabb544d97cf -->
## review / inputs

<!-- block: b-96d1686bd4d451339838 -->
<!-- field: field-0002 -->
Registered provider endpoint and authentication; space association; selected operation; resource identifiers and observation interval.
<!-- /field -->

<!-- block: b-6178fe0049ce522d86fa -->
## review / narrative / 0

<!-- block: b-a37daf8764435bc884e1 -->
<!-- field: field-0003 -->
A successful provider registration establishes a connection, not the result of a particular query. The Agent Space association selects the available tool surface. A custom definition can further restrict that surface. At execution time the source still evaluates the actual credentials and request arguments. This is why a missing metric can be a selection, identity, scope or time-window problem rather than an analytical failure.
<!-- /field -->

<!-- block: b-e396ec23baf35a71ab1b -->
## review / narrative / 1

<!-- block: b-469a493085355c948e80 -->
<!-- field: field-0004 -->
The mechanism ends with a tool response or an explicit error. Interpreting the response is subsequent work. Keep the source identity and observation interval with the response so that a later summary can be checked against the same measurement.
<!-- /field -->

<!-- block: b-6cd5ae5dac165285ade1 -->
## review / configuration / 0 / 1

<!-- block: b-9dd00ed5171057f2acc7 -->
<!-- field: field-0005 -->
Capability Providers → MCP Server → Register; provide HTTPS endpoint and supported authentication.
<!-- /field -->

<!-- block: b-8ea3c8bde9de55c7ab6f -->
## review / configuration / 1 / 1

<!-- block: b-91a7197ef6a45a74905a -->
<!-- field: field-0006 -->
Agent Space → Capabilities → MCP Servers → Add; select the registered provider and required tools.
<!-- /field -->

<!-- block: b-ecf21f65693b567499fb -->
## review / controls

<!-- block: b-a42825efe2b85a479141 -->
<!-- field: field-0007 -->
Network reachability, authentication, resource permissions and tool selection are separate gates. Use read credentials for this evidence path; mutating tools belong to the directed-action explanation.
<!-- /field -->

<!-- block: b-79470260c726544caf8d -->
## review / observable output

<!-- block: b-ef730340d3c5594ea20e -->
<!-- field: field-0008 -->
Provider/association configuration and an actual tool result or error; a connection-valid status alone does not prove the intended source query works.
<!-- /field -->

<!-- block: b-fc00b28d8079577fb7b3 -->
## review / undocumented

<!-- block: b-ccda2b4c1d96529c9a26 -->
<!-- field: field-0009 -->
The platform does not document a universal query planner, response-completeness guarantee or retry/deduplication contract for every connected tool.
<!-- /field -->

<!-- block: b-4f7b2cba99ff579fa3a0 -->
## review / test / 2

<!-- block: b-45fb482753785ac78fee -->
<!-- field: field-0010 -->
Select an unavailable operation or out-of-scope fixture; require an explicit gap, not a healthy result.
<!-- /field -->

<!-- block: b-a95f609523ec550f977d -->
## review / claims / 0 / assertion

<!-- block: b-99e102d252c75384a99b -->
<!-- field: field-0011 -->
Registration, association and tool selection are separate; removal and credential replacement have dependent-connection consequences.
<!-- /field -->
