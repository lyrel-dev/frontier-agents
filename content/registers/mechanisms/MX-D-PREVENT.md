---
id: record-mechanisms-MX-D-PREVENT
kind: record
collection: mechanisms
product: devops
title: Cross-investigation prevention evaluation
order: 10
frozen: true
data:
  id: MX-D-PREVENT
  platform: devops
  title: Cross-investigation prevention evaluation
  features:
  - FT-D-PREVENTION
  sections:
  - D-06
  trigger: Manual or configured evaluation
  state: Investigation evidence and recommendations
  process:
    $markdown: field-0001
  effect: Recommendation
  verification: Trace a proposed theme or improvement to supporting investigations.
  on_failure: Keep unsupported patterns as hypotheses and separate proposals from implemented changes.
  review:
    primary_section: D-06
    kind: Cross-investigation analysis workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Evaluate
      - Improvements → Run Now; inspect linked investigations and proposed effect.
      - Evaluation and recommendations
    - - Control evaluation
      - Pause recurring evaluation or Stop Evaluation for current work as appropriate.
      - Different scheduling/execution controls
    - - Disposition
      - Use Keep, Discard or Implemented and supply relevant explanation.
      - Backlog state
    lifecycle:
    - - Proposal
      - Keep
      - Retained backlog candidate.
    - - Proposal
      - Discard with rationale
      - Removed from backlog; feedback informs later recommendations.
    - - Accepted proposal
      - Mark Implemented
      - Tracking status changes; actual implementation must be verified.
    controls: Priority and estimated effect do not authorize execution or measure realized improvement.
    observable_output: Recommendation, supporting investigation references, disposition and observed changes.
    undocumented:
      $markdown: field-0005
    test:
    - Review a candidate tied to several known investigations.
    - Trace the common weakness to its supporting evidence.
    - $markdown: field-0006
    claims:
    - source: DS410
      section: Controlling evaluations; Managing recommendations
      assertion:
        $markdown: field-0007
---

<!-- block: b-cb9ad4ff0ed75fae83a4 -->
## process

<!-- block: b-43ea8b25f9c35f22abb6 -->
<!-- field: field-0001 -->
Analyze recurring weaknesses and produce improvement proposals.
<!-- /field -->

<!-- block: b-55c049fef00052ce96a9 -->
## review / inputs

<!-- block: b-3751f3681e825a82a137 -->
<!-- field: field-0002 -->
Recent investigation evidence, existing recommendation backlog and operator disposition feedback.
<!-- /field -->

<!-- block: b-ac63c1fa9b935f11bbea -->
## review / narrative / 0

<!-- block: b-181cd06c678258f8b66a -->
<!-- field: field-0003 -->
Prevention compares incidents to propose changes rather than diagnosing one current alarm. An evaluation produces or updates recommendations; backlog controls describe what the team intends to do with those recommendations. The action that implements a recommendation remains a separate change.
<!-- /field -->

<!-- block: b-ae7a907940df51a8b345 -->
## review / narrative / 1

<!-- block: b-b6fe7c445a8258889e5a -->
<!-- field: field-0004 -->
A kept recommendation is not a deployed fix. A recommendation marked implemented is a tracking state, not independent proof of reduced incidents. Retain the implementation and post-change evidence in the normal change process.
<!-- /field -->

<!-- block: b-b14329d636605ef1bdda -->
## review / undocumented

<!-- block: b-31c75186dc30559e8eaf -->
<!-- field: field-0005 -->
Full ranking weights, exact feedback influence and causal benefit attribution are not specified.
<!-- /field -->

<!-- block: b-f02f262c3dbe51a6a99b -->
## review / test / 2

<!-- block: b-d6b667e7afed5ae39db7 -->
<!-- field: field-0006 -->
A change not deployed must not be reported as completed merely because the recommendation was kept.
<!-- /field -->

<!-- block: b-8487ff88a6d256c9853b -->
## review / claims / 0 / assertion

<!-- block: b-1521c3df0d62515b92e3 -->
<!-- field: field-0007 -->
Evaluation control and recommendation disposition are separate; unretained recommendations may age out.
<!-- /field -->
