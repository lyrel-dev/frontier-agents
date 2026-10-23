---
id: record-mechanisms-MX-S-RUN
kind: record
collection: mechanisms
product: security
title: Saved assessment and independent execution
order: 18
frozen: true
data:
  id: MX-S-RUN
  platform: security
  title: Saved assessment and independent execution
  features:
  - FT-S-RUNS
  - FT-S-FINDINGS
  sections:
  - S-04
  trigger: Manual or supported recurring/external invocation
  state: Configuration, run and findings
  process:
    $markdown: field-0001
  effect: Active application assessment
  verification: Record actual revision, roles, exclusions, limit and incomplete areas.
  on_failure: Treat incomplete or failed execution as a coverage gap, not a pass.
  review:
    primary_section: S-04
    kind: Configuration-to-assessment workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Define
      - $markdown: field-0005
      - Reusable configuration
    - - Save or start
      - Choose the supported save-only or create-and-execute action.
      - Definition versus run
    - - Inspect
      - Open the run overview, preflight/logs and findings.
      - Execution evidence
    lifecycle:
    - - Configuration saved
      - Start execution
      - An independent run is created.
    - - Preflight fails
      - Resolve prerequisite and start a new run
      - No successful runtime coverage is established.
    - - Run completes
      - Review findings and coverage
      - Further execution uses a new run, not rewritten evidence.
    controls:
      $markdown: field-0006
    observable_output: Run identity, actual target context, logs, discovered/tested endpoints and findings.
    undocumented:
      $markdown: field-0007
    test:
    - Use a deliberately limited staging target and record its deployed revision.
    - Inspect actual reached paths and completed phases.
    - Make a required target unreachable; require a preflight failure or explicit coverage gap.
    claims:
    - source: SS404
      section: 'Penetration testing: reusable configurations with independent executions'
      assertion: One configuration supports separate runs and new findings.
    - source: SS418
      section: Create and execute; Review findings
      assertion: Saving, executing and preflight outcomes are different stages.
---

<!-- block: b-36b1579d45505a8b804e -->
## process

<!-- block: b-af5f0691f12e5727aeb8 -->
<!-- field: field-0001 -->
Execute against the current configured target and retain an independent result.
<!-- /field -->

<!-- block: b-7a35a7cbbe8b5388a95a -->
## review / inputs

<!-- block: b-0a49a704a20e5e0e8195 -->
<!-- field: field-0002 -->
Saved penetration-test configuration, current target deployment, credentials, exclusions and execution/work limit.
<!-- /field -->

<!-- block: b-f1df7115c04c5cbd967b -->
## review / narrative / 0

<!-- block: b-338906c7b06157bb90ba -->
<!-- field: field-0003 -->
A saved penetration-test configuration is reusable; each execution has its own record and findings. Saving the configuration does not freeze a deployment that continues to change. Identify the deployed revision and current credentials for every run.
<!-- /field -->

<!-- block: b-485811778e76578f85a9 -->
## review / narrative / 1

<!-- block: b-9b3cf65f8519545eac57 -->
<!-- field: field-0004 -->
Execution begins with prerequisite checks before assessment work. A preflight failure is neither a successful clean assessment nor evidence that the target contains no vulnerabilities. The assessment record should retain incomplete areas along with findings.
<!-- /field -->

<!-- block: b-6ae196b489005c0b9c2a -->
## review / configuration / 0 / 1

<!-- block: b-a61ad0ebda9553159806 -->
<!-- field: field-0005 -->
Penetration tests → create: configure target, role, credentials, network and source context.
<!-- /field -->

<!-- block: b-8e1098ae18985ac0aa41 -->
## review / controls

<!-- block: b-69ae3071b6b951b09637 -->
<!-- field: field-0006 -->
Work limits, test scope and owner authorization must remain explicit; budget limits do not guarantee a particular coverage level.
<!-- /field -->

<!-- block: b-0d82308262a5579e834f -->
## review / undocumented

<!-- block: b-a91498e6aa4555af9999 -->
<!-- field: field-0007 -->
The documented interface does not expose the complete assessment-planning or vulnerability-discovery algorithm.
<!-- /field -->
