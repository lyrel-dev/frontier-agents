---
id: record-mechanisms-MX-D-TRIAGE
kind: record
collection: mechanisms
product: devops
title: Incident routing
order: 6
frozen: true
data:
  id: MX-D-TRIAGE
  platform: devops
  title: Incident routing
  features:
  - FT-D-INCIDENT
  sections:
  - D-06
  trigger: Incoming incident signal
  state: Signal and investigation relationships
  process:
    $markdown: field-0001
  effect: Investigation linkage
  verification: Inspect the routing decision, reason and resulting investigation identity.
  on_failure: Correct routing through the supported unlink or unskip operation.
  review:
    primary_section: D-06
    kind: Incident-routing mechanism
    inputs: Incoming external signal, active investigations and configured correlation/skip guidance.
    narrative:
    - $markdown: field-0002
    - $markdown: field-0003
    configuration:
    - - Signal path
      - Connect a supported incident source or webhook and inspect the received event.
      - Incident initiation
    - - Routing criteria
      - Review the relevant correlation or skip skill.
      - Routing guidance
    - - Correction
      - Inspect the triage record and use supported unlink/unskip controls.
      - Signal relationship
    lifecycle:
    - - Received signal
      - Linked
      - Existing investigation receives signal context.
    - - Received signal
      - Skipped
      - Reason is retained without a new investigation.
    - - Received signal
      - Proceed
      - Independent investigation is scheduled.
    - - Linked or skipped
      - Unlink or unskip
      - Independent work is rescheduled.
    controls:
      $markdown: field-0004
    observable_output: Triage outcome, reason and investigation linkage.
    undocumented:
      $markdown: field-0005
    test:
    - Submit related and unrelated authorized test events.
    - Check linkage and reason against known service/time identity.
    - $markdown: field-0006
    claims:
    - source: DS404
      section: Incident triage
      assertion:
        $markdown: field-0007
---

<!-- block: b-907a80e944a55b42b4c6 -->
## process

<!-- block: b-2c7848c54f9159449d3d -->
<!-- field: field-0001 -->
Link the signal, skip it under configured criteria or proceed with independent investigation.
<!-- /field -->

<!-- block: b-fa4d269d7e425b698429 -->
## review / narrative / 0

<!-- block: b-db718c059dbe546e9e8b -->
<!-- field: field-0002 -->
Triage changes the relationship between a signal and investigation work. Linked signals contribute context to an existing investigation; skipped signals match exclusion criteria; proceed decisions schedule independent work. Routing is therefore not the root-cause result.
<!-- /field -->

<!-- block: b-67991f99cd275c67a4a9 -->
## review / narrative / 1

<!-- block: b-fbed7f56ef5a55508b43 -->
<!-- field: field-0003 -->
Correct a bad relationship at the routing layer. Unlinking or unskipping reschedules independent investigation; changing a hypothesis inside the primary investigation does not repair the original routing decision.
<!-- /field -->

<!-- block: b-d42d9d2a4bf957b08397 -->
## review / controls

<!-- block: b-82bc2c056d4c521b94ac -->
<!-- field: field-0004 -->
Do not interpret a linked signal as missing work or a skipped signal as proof that the service is healthy.
<!-- /field -->

<!-- block: b-a9361c87ff275f38a476 -->
## review / undocumented

<!-- block: b-fc39f1dce8775a71aa48 -->
<!-- field: field-0005 -->
The exact correlation model and an absolute timing guarantee are not specified; a typical lookback is not a universal contract.
<!-- /field -->

<!-- block: b-9fecd7a8988153f4ad94 -->
## review / test / 2

<!-- block: b-acb47cda406254d687da -->
<!-- field: field-0006 -->
Deliberately review an incorrect skip criterion and verify the correction changes routing, not resource state.
<!-- /field -->

<!-- block: b-63ddea38dfeb5b27a175 -->
## review / claims / 0 / assertion

<!-- block: b-ffd719fb14e657f5ae3c -->
<!-- field: field-0007 -->
Linked, Skipped and Proceed are routing outcomes; supported corrections reschedule independent work.
<!-- /field -->
