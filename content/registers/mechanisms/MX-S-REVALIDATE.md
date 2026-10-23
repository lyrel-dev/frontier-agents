---
id: record-mechanisms-MX-S-REVALIDATE
kind: record
collection: mechanisms
product: security
title: Selected finding replay and lineage
order: 21
frozen: true
data:
  id: MX-S-REVALIDATE
  platform: security
  title: Selected finding replay and lineage
  features:
  - FT-S-REVALIDATION
  sections:
  - S-M05
  trigger: Repair deployed to the authorized target
  state: Original finding and separate revalidation job
  process:
    $markdown: field-0001
  effect: Targeted active test
  verification: Verify reached identity, deployed repair and linked result.
  on_failure: Record authentication or environment failure as inconclusive verification.
  review:
    primary_section: S-M05
    kind: Targeted replay and lineage mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Prepare
      - Deploy the reviewed repair to the environment originally tested.
      - Current target state
    - - Select
      - $markdown: field-0005
      - Selected replay scope
    - - Inspect
      - Open the job, original finding and revalidation history.
      - Evidence lineage
    lifecycle:
    - - Original finding
      - Start revalidation
      - Separate job created.
    - - Validation reproduced
      - Active result
      - Further remediation remains necessary.
    - - Validation not reproduced
      - Resolved result
      - Interpret within reached identity and scope.
    - - Another repair deployed
      - Repeat selected replay
      - A further linked job records a new attempt.
    controls:
      $markdown: field-0006
    observable_output: Linked job and per-finding replay result; linked Jira issues can receive result comments.
    undocumented:
      $markdown: field-0007
    test:
    - Use a deployed repair with a known test identity and retained original finding.
    - Check the reached identity and link to the replay result.
    - $markdown: field-0008
    claims:
    - source: SS407
      section: Select findings; Interpret results; Trace history
      assertion: Replay has separate job identity, selected scope and preserved original finding.
    diagram: mechanism-security-replay
---

<!-- block: b-2b26c5f79fa05c428acc -->
## process

<!-- block: b-45fb5c214f365790af01 -->
<!-- field: field-0001 -->
Repeat selected finding-validation steps under current test conditions.
<!-- /field -->

<!-- block: b-bc73190ff34a5d409448 -->
## review / inputs

<!-- block: b-512d54ee416152728de5 -->
<!-- field: field-0002 -->
Completed test findings, deployed repair on the original target and current authentication configuration.
<!-- /field -->

<!-- block: b-2d5a109011a35170b66f -->
## review / narrative / 0

<!-- block: b-b9b9fc68296050e2b5f2 -->
<!-- field: field-0003 -->
Revalidation repeats validation steps for selected existing findings and creates a separate job. The original finding remains available and the result links back to it. This is targeted replay, not new vulnerability discovery.
<!-- /field -->

<!-- block: b-59d57866a9e55e14abd2 -->
## review / narrative / 1

<!-- block: b-d5f6f1a3da7d53b487aa -->
<!-- field: field-0004 -->
An Active result means reproduction succeeded. Resolved means the service could not reproduce the issue during this replay. The engineering review must still confirm that the intended identity and path were reached; a failed login cannot demonstrate a repaired authorization check.
<!-- /field -->

<!-- block: b-488d352adbf3546a81b4 -->
## review / configuration / 1 / 1

<!-- block: b-3c7c0b31ceee5147a66b -->
<!-- field: field-0005 -->
Completed run → Multiselect findings for revalidation → select findings → Revalidate findings.
<!-- /field -->

<!-- block: b-d565776e16655315acdb -->
## review / controls

<!-- block: b-836922442ad65b54b92a -->
<!-- field: field-0006 -->
Full assessments remain necessary for broader changes; replay does not certify whole-application security.
<!-- /field -->

<!-- block: b-b849a680d84353bb8e6c -->
## review / undocumented

<!-- block: b-852a9da9d97c5cf683fd -->
<!-- field: field-0007 -->
No exactly-once callback or universal guarantee distinguishing every environmental failure from non-reproduction is established.
<!-- /field -->

<!-- block: b-e3032611223c50bf847d -->
## review / test / 2

<!-- block: b-9265c8d8af2f5748872d -->
<!-- field: field-0008 -->
Break authentication in a controlled test; record verification as inconclusive rather than celebrating non-reproduction.
<!-- /field -->
