---
id: record-mechanisms-MX-D-INVESTIGATE
kind: record
collection: mechanisms
product: devops
title: Investigation and operator steering
order: 7
frozen: true
data:
  id: MX-D-INVESTIGATE
  platform: devops
  title: Investigation and operator steering
  features:
  - FT-D-INCIDENT
  - FT-D-SOURCES
  sections:
  - D-06
  trigger: Selected incident or manual investigation
  state: Current evidence and evolving conclusions
  process:
    $markdown: field-0001
  effect: Investigation record
  verification: Check conclusions against current observations and identify missing evidence.
  on_failure: Retain competing hypotheses or an inconclusive result instead of inventing certainty.
  review:
    primary_section: D-06
    kind: Documented service workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Start
      - $markdown: field-0005
      - Investigation identity
    - - Steer
      - Supply contrary observations within the active investigation.
      - Current execution context
    - - Conclude
      - Review findings and cause; request a mitigation proposal separately.
      - Analysis before effects
    lifecycle:
    - - Investigation started
      - Read connected evidence
      - Observations and gaps accumulate.
    - - Hypothesis present
      - Operator supplies contrary evidence
      - Analysis can be reconsidered in context.
    - - Investigation completed
      - Review or submit feedback
      - Later correction is separate from active steering.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Use the repository recurring-alarm fixture as a tabletop, not as service telemetry.
    - Require the explanation to follow the current dependency measurements.
    - $markdown: field-0009
    claims:
    - source: DS404
      section: Starting Investigations; Incident triage
      assertion: Manual scope and operator context drive a separate investigation record.
    - source: DS407
      section: Custom agents compared to built-in capabilities
      assertion: Incident response is a built-in path, not a mandatory custom-agent task.
---

<!-- block: b-5420cab5b66157a3bda8 -->
## process

<!-- block: b-95aa9390109053749b78 -->
<!-- field: field-0001 -->
Read observations, examine hypotheses and accept relevant operator steering in the investigation context.
<!-- /field -->

<!-- block: b-f8adc530e1d45a889afe -->
## review / inputs

<!-- block: b-05036a8090985ca19bf7 -->
<!-- field: field-0002 -->
Incident description, start evidence, actual incident time, service scope and connected source access.
<!-- /field -->

<!-- block: b-f771f5f6f3e05103bb27 -->
## review / narrative / 0

<!-- block: b-91b762566f095120b42f -->
<!-- field: field-0003 -->
An investigation has its own scope and evidence record. The service gathers observations and develops an explanation; operator steering can add missing or contrary evidence within that record. This describes the observable workflow, not an undisclosed hypothesis-ranking algorithm.
<!-- /field -->

<!-- block: b-537e323c0a9a58dea455 -->
## review / narrative / 1

<!-- block: b-cd2e26f65974571e93c5 -->
<!-- field: field-0004 -->
Use the incident timestamp rather than the time the operator happened to open the form. Preserve observations that weaken the leading explanation. A revised analysis is useful only when the supporting evidence also changes.
<!-- /field -->

<!-- block: b-0d80fb2ea8d350869eed -->
## review / configuration / 0 / 1

<!-- block: b-ca88cfc557f751a38dc6 -->
<!-- field: field-0005 -->
Incident Response → start a manual investigation; review details, starting point, UTC incident time, name and priority.
<!-- /field -->

<!-- block: b-db6a3190a3ad5fd392d7 -->
## review / controls

<!-- block: b-8e9aae2983ee5d5cb024 -->
<!-- field: field-0006 -->
Steering is not approval for a resource mutation. Missing evidence constrains the conclusion.
<!-- /field -->

<!-- block: b-853e8ae5cb8753c0a889 -->
## review / observable output

<!-- block: b-e86af500ff5a573aa3f0 -->
<!-- field: field-0007 -->
Investigation findings, source observations and any revised conclusion available in the service record.
<!-- /field -->

<!-- block: b-750dec3f78695b848d0e -->
## review / undocumented

<!-- block: b-b5a4f93d52c655539ca8 -->
<!-- field: field-0008 -->
No deterministic root-cause accuracy guarantee or complete inference algorithm is published.
<!-- /field -->

<!-- block: b-3e74310b621f5db5a216 -->
## review / test / 2

<!-- block: b-46637b7558af5924a26d -->
<!-- field: field-0009 -->
Remove the decisive observation; an inconclusive result is preferable to a fabricated cause.
<!-- /field -->
