---
id: record-mechanisms-MX-S-CONTEXT
kind: record
collection: mechanisms
product: security
title: Application-context assembly
order: 14
frozen: true
data:
  id: MX-S-CONTEXT
  platform: security
  title: Application-context assembly
  features:
  - FT-S-SOURCES
  sections:
  - S-09
  - S-M07
  trigger: Assessment setup or execution
  state: Selected sources and application scope
  process:
    $markdown: field-0001
  effect: Source read
  verification: Compare source revision and system boundary with the intended subject.
  on_failure: Exclude mismatched context and document the resulting assessment limitation.
  review:
    primary_section: S-M07
    kind: Assessment-context mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Register
      - 'Integrations: authorize the supported provider account.'
      - Account-level registration
    - - Connect
      - Within the intended Agent Space, select repositories or documentation resources.
      - Application-scoped evidence
    - - Configure effects
      - Review per-repository write options separately from source reads.
      - Optional repository effects
    lifecycle:
    - - Provider registered
      - Connect resource to space
      - Read context becomes available through that association.
    - - Application changes
      - Start assessment against intended sources
      - A previous result remains tied to its earlier evidence.
    - - Write option disabled
      - Run eligible read analysis
      - Read context does not imply comment or repair permission.
    controls:
      $markdown: field-0005
    observable_output: Selected resource identity and assessment source/preflight evidence.
    undocumented:
      $markdown: field-0006
    test:
    - Select a repository and design document that describe one known staging application.
    - Check that a run identifies that application and revision.
    - $markdown: field-0007
    claims:
    - source: SS401
      section: Register once, reuse everywhere; One connection, shared across capabilities
      assertion: Registration, resource association and write opt-ins are distinct.
---

<!-- block: b-1b05965e0d1755488a7a -->
## process

<!-- block: b-52c9db4676165a43b33c -->
<!-- field: field-0001 -->
Read the connected source and documentation relevant to the selected assessment.
<!-- /field -->

<!-- block: b-f9afc7e9d7125d34a47d -->
## review / inputs

<!-- block: b-4dcbc0ddc2d75a5b8dd6 -->
<!-- field: field-0002 -->
Connected source/document resources, selected revision or design scope, service-role access and assessment configuration.
<!-- /field -->

<!-- block: b-6177f3e7b9c25e6589c0 -->
## review / narrative / 0

<!-- block: b-697b27cfda945fe2b631 -->
<!-- field: field-0003 -->
Registration authorizes a provider account; connecting particular resources supplies application-specific evidence. A selected repository can support several assessment types without being independently registered for each. Context assembly must nevertheless use the correct application and revision.
<!-- /field -->

<!-- block: b-2b102dd9147c5adc92b3 -->
## review / narrative / 1

<!-- block: b-87d62aef315154e293e2 -->
<!-- field: field-0004 -->
Read access and publication of comments or proposed changes are separate. A context read can help interpret an application without creating a permission to change its repository. The service documentation describes the evidence inputs but not a universal persistent knowledge store or retrieval algorithm for every assessment.
<!-- /field -->

<!-- block: b-736c2c42736058a18992 -->
## review / controls

<!-- block: b-e94420eefb85509aa981 -->
<!-- field: field-0005 -->
Keep application boundary and revision explicit. Private source-control access is separate from private target access.
<!-- /field -->

<!-- block: b-4735385e3f265c989890 -->
## review / undocumented

<!-- block: b-3c682c145dcf5393a08e -->
<!-- field: field-0006 -->
Cross-assessment cache freshness, internal ranking and automatic refresh guarantees are not established.
<!-- /field -->

<!-- block: b-4a10c9b19e545d10b00d -->
## review / test / 2

<!-- block: b-d52e3638e9495e978fb6 -->
<!-- field: field-0007 -->
Supply a mismatched design revision and require an explicit mismatch rather than a merged invented architecture.
<!-- /field -->
