---
id: record-mechanisms-MX-S-FIX
kind: record
collection: mechanisms
product: security
title: Repository repair proposal
order: 20
frozen: true
data:
  id: MX-S-FIX
  platform: security
  title: Repository repair proposal
  features:
  - FT-S-FIX
  sections:
  - S-05
  trigger: Accepted finding and configured source access
  state: Finding and proposed change
  process:
    $markdown: field-0001
  effect: Proposed repository change
  verification: Inspect revision, tests and unrelated changes before accepting the proposal.
  on_failure: Leave a failed or rejected proposal unfinished; merge is not deployment.
  review:
    primary_section: S-05
    kind: Remediation-proposal workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Enable
      - $markdown: field-0005
      - Optional source-write capability
    - - Start
      - From the finding, choose Remediate code or use the configured automatic proposal path.
      - Remediation attempt
    - - Review
      - Inspect proposal/diff and its tests before normal deployment.
      - Team acceptance
    lifecycle:
    - - Finding confirmed
      - Remediation requested
      - Attempt and proposed change are produced.
    - - Proposal created
      - Engineering review
      - Accept, revise or reject without implying deployment.
    - - Repair deployed
      - Revalidate finding separately
      - Test the actual target rather than the branch.
    controls:
      $markdown: field-0006
    observable_output: Remediation status, linked proposal/diff and original finding identity.
    undocumented:
      $markdown: field-0007
    test:
    - Use a known authorized fixture finding and isolated test repository.
    - Inspect intended diff, tests and unrelated changes.
    - A failing build or undeployed merge must keep verification incomplete.
    claims:
    - source: SS406
      section: Start and view code remediation
      assertion: Current guidance distinguishes private-repository proposals and S3 diffs.
    - source: SS401
      section: Write actions are opt-in
      assertion: Repository writes are separately configured and provider-limited.
---

<!-- block: b-907b6309f32b5fb6ad9d -->
## process

<!-- block: b-a4afa7ec330f576ea896 -->
<!-- field: field-0001 -->
Create a supported patch or pull request for engineering review.
<!-- /field -->

<!-- block: b-e86260dc9d755358b2e9 -->
## review / inputs

<!-- block: b-276f3585ec9753019414 -->
<!-- field: field-0002 -->
Finding, eligible connected repository or S3 source, configured remediation permission and selected source context.
<!-- /field -->

<!-- block: b-1bf57409874a57229107 -->
## review / narrative / 0

<!-- block: b-943dab54461d56018bb9 -->
<!-- field: field-0003 -->
Remediation produces a proposed source change. Current provider guidance describes pull/merge requests for eligible private repositories and a downloadable diff for S3 sources. Older retrieved text describes a narrower provider/public-repository path; do not generalize either wording to unsupported provider writes.
<!-- /field -->

<!-- block: b-fe21c8f1cd5e5e348329 -->
## review / narrative / 1

<!-- block: b-cd432734799e5bcd8151 -->
<!-- field: field-0004 -->
The proposal remains separate from review, merge, deployment and finding revalidation. Preserve the original finding relationship through those steps, including any linked Jira record.
<!-- /field -->

<!-- block: b-dd3ae9bf7a6c58838b05 -->
## review / configuration / 0 / 1

<!-- block: b-34c275fefc1c5a059909 -->
<!-- field: field-0005 -->
Enable remediation in the administrative configuration and select the appropriate repositories/source.
<!-- /field -->

<!-- block: b-83da02d8322e50aea2d2 -->
## review / controls

<!-- block: b-50f770ee74af59a9b44f -->
<!-- field: field-0006 -->
Read-only source access does not grant proposal-write permission. A pull request is not an automatically deployed fix.
<!-- /field -->

<!-- block: b-3ca6fe04c4145b82aee0 -->
## review / undocumented

<!-- block: b-6b0939eed86257eb888a -->
<!-- field: field-0007 -->
No universal guarantee of successful repair, regression coverage or automatic deployment is provided.
<!-- /field -->
