---
id: record-mechanisms-MX-D-FEEDBACK
kind: record
collection: mechanisms
product: devops
title: Corrective investigation feedback
order: 3
frozen: true
data:
  id: MX-D-FEEDBACK
  platform: devops
  title: Corrective investigation feedback
  features:
  - FT-D-INCIDENT
  - FT-D-MEMORY
  sections:
  - D-M02
  trigger: Operator supplies a verified correction
  state: Investigation feedback and documented corrective context
  process:
    $markdown: field-0001
  effect: Retained correction
  verification: Inspect saved feedback and any exposed corrective entry.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-M02
    kind: Corrective-context mechanism
    inputs: Completed investigation identifier, operator verdict and verified actual cause.
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Feedback
      - $markdown: field-0005
      - Investigation-specific correction
    - - Inspection
      - Inspect saved feedback and any exposed reflection in Knowledge → Memories.
      - Correction versus derived context
    - - External sharing
      - Review the separate AWS-sharing confirmation.
      - Separate disclosure decision
    lifecycle:
    - - Completed diagnosis
      - Submit correction
      - Feedback describes the verified alternative.
    - - Feedback already present
      - Submit replacement
      - Inspect the saved latest feedback rather than assuming additive history.
    - - Reflection available
      - Later relevant investigation reads it
      - Later use must be evaluated independently.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Use a completed non-production example with a known corrected cause.
    - Confirm saved correction, then inspect later use only if the execution exposes it.
    - $markdown: field-0009
    claims:
    - source: DS404
      section: Provide feedback on investigations
      assertion:
        $markdown: field-0010
    - source: DS402
      section: reflections
      assertion: Corrective lessons are retained for future relevant investigations.
---

<!-- block: b-7230b9e420655faeb249 -->
## process

<!-- block: b-7675f8f9049358bc9b10 -->
<!-- field: field-0001 -->
Record the actual cause separately from routine synthesis of incident history.
<!-- /field -->

<!-- block: b-1d083eda9c1b50f5b9e2 -->
## on failure

<!-- block: b-22624fc92ed6593591cd -->
<!-- field: field-0002 -->
Keep the verified correction in the incident system when downstream use cannot be observed.
<!-- /field -->

<!-- block: b-a6f008b6d9d25770a0c8 -->
## review / narrative / 0

<!-- block: b-319d76b87ff65ff686df -->
<!-- field: field-0003 -->
Feedback supplies a verified correction to a particular investigation. It is not the same input as another occurrence of the alarm and is not the same operation as steering an active investigation. The correction can produce reflection context explaining the discrepancy between the earlier diagnosis and the established cause.
<!-- /field -->

<!-- block: b-94d40ead32d1532d821e -->
## review / narrative / 1

<!-- block: b-5a468c5ac3eb51e5b834 -->
<!-- field: field-0004 -->
The operator should preserve the evidence for the actual cause independently. Submitting feedback confirms an input was recorded; it does not prove that a later task selected the resulting context. Sharing the feedback with AWS is a separate confirmation decision.
<!-- /field -->

<!-- block: b-f05c0921b7b1552ead82 -->
## review / configuration / 0 / 1

<!-- block: b-6c3f047121dd5cdda941 -->
<!-- field: field-0005 -->
Completed investigation → Add feedback; supply verdict and actual cause when incorrect, or use the documented Chat path.
<!-- /field -->

<!-- block: b-2a7a0953897556e185ae -->
## review / controls

<!-- block: b-07a04bd839f853519980 -->
<!-- field: field-0006 -->
Do not infer production-change authority from a corrective message. Operator evidence, retained correction and optional external sharing are different records.
<!-- /field -->

<!-- block: b-11b6b6e1822551fdada8 -->
## review / observable output

<!-- block: b-8192cc036bb5513a9b25 -->
<!-- field: field-0007 -->
Saved feedback and any visible corrective memory; later retrieval is an additional observation.
<!-- /field -->

<!-- block: b-863cea68bfd65b4f9ba5 -->
## review / undocumented

<!-- block: b-85cc4b8b540d5b72b9a2 -->
<!-- field: field-0008 -->
The exact latency from submission to reflection availability and a guaranteed recall rate are not established.
<!-- /field -->

<!-- block: b-d921fab72c435565803c -->
## review / test / 2

<!-- block: b-5915b299d28d5304808e -->
<!-- field: field-0009 -->
Supply a different current cause on recurrence; repeating the previous answer is not success.
<!-- /field -->

<!-- block: b-cc796c86a16d5fe1add8 -->
## review / claims / 0 / assertion

<!-- block: b-a21570f8570c5746b8cf -->
<!-- field: field-0010 -->
Feedback records the actual cause; latest feedback and separate sharing confirmation have distinct effects.
<!-- /field -->
