---
id: record-mechanisms-MX-S-THREAT
kind: record
collection: mechanisms
product: security
title: System-model construction and threat analysis
order: 26
frozen: true
data:
  id: MX-S-THREAT
  platform: security
  title: System-model construction and threat analysis
  features:
  - FT-S-THREAT
  - FT-S-SOURCES
  sections:
  - S-06
  trigger: Scoped threat-model run
  state: Scope, system representation and threats
  process:
    $markdown: field-0001
  effect: Model result
  verification: Review inferred boundaries before interpreting individual threats.
  on_failure: Correct input scope when the model represents the wrong system.
  review:
    primary_section: S-06
    kind: System-model and threat-analysis workflow
    inputs: Scope documents, selected sources or both, application boundary and service role.
    narrative:
    - $markdown: field-0002
    - $markdown: field-0003
    configuration:
    - - Create
      - $markdown: field-0004
      - Reusable model configuration
    - - Execute
      - Start run; inspect Preflight and Logs.
      - Independent run
    - - Review
      - Inspect Overview before Threats; review evidence and recommendations.
      - System representation and threat records
    lifecycle:
    - - Configuration saved
      - Start run
      - Preflight and analysis create a system model.
    - - Model produced
      - Review boundaries and threats
      - Accept, resolve or dismiss findings with rationale.
    - - Scope changes
      - Rerun with corrected input
      - New result reflects the intended subject.
    controls:
      $markdown: field-0005
    observable_output: System overview, threat statements, classifications, evidence and recommendations.
    undocumented:
      $markdown: field-0006
    test:
    - Provide a small design with a known trust boundary and supporting source.
    - Check that the overview reflects the known boundary.
    - $markdown: field-0007
    claims:
    - source: SS413
      section: Create and run a threat model; Review threats
      assertion:
        $markdown: field-0008
---

<!-- block: b-e7c5dfe679355ed9b640 -->
## process

<!-- block: b-6bd22021446d57038a73 -->
<!-- field: field-0001 -->
Construct the system model and examine threats to its flows and boundaries.
<!-- /field -->

<!-- block: b-ea90ace245d857f0aa13 -->
## review / narrative / 0

<!-- block: b-f71f414a3def570cb2cb -->
<!-- field: field-0002 -->
Scope documents express what should be modeled; source code supplies context for the current system. The output includes a system overview and threats derived for that representation. Review the system boundary and flows before accepting the threats built on them.
<!-- /field -->

<!-- block: b-fad61aeea6fd592ebb7b -->
## review / narrative / 1

<!-- block: b-fa4e0a8947f45362aae2 -->
<!-- field: field-0003 -->
A model of the wrong system can produce plausible but irrelevant threats. Correct the scope or source mismatch and run again rather than dismissing every downstream item individually.
<!-- /field -->

<!-- block: b-d5fd2838f2055c4bbbf4 -->
## review / configuration / 0 / 1

<!-- block: b-3f962ae82b655026a10f -->
<!-- field: field-0004 -->
Threat models → Create threat model: title, scope documents and/or sources, service role and optional log group.
<!-- /field -->

<!-- block: b-a487b1c4977e54e0ba4e -->
## review / controls

<!-- block: b-589414a4bbb2565dbb1c -->
<!-- field: field-0005 -->
Inferred relationships require owner review; threat status is not proof that a mitigation is deployed.
<!-- /field -->

<!-- block: b-9ce0be514ecf54009bc7 -->
## review / undocumented

<!-- block: b-e72edfe5dcbc5faf86e4 -->
<!-- field: field-0006 -->
The exhaustive threat-generation strategy and completeness of inferred flows are not published.
<!-- /field -->

<!-- block: b-ab0c31ac60925eee9891 -->
## review / test / 2

<!-- block: b-17278b2d6a285cc9bd16 -->
<!-- field: field-0007 -->
Use a deliberately stale scope document; identify the mismatch before interpreting threat counts.
<!-- /field -->

<!-- block: b-d030477d5713582f8194 -->
## review / claims / 0 / assertion

<!-- block: b-c1fb2ec7681952e7b5c8 -->
<!-- field: field-0008 -->
Scope documents and source context have distinct roles; overview and threats are reviewable.
<!-- /field -->
