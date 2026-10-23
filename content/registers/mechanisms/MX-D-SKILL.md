---
id: record-mechanisms-MX-D-SKILL
kind: record
collection: mechanisms
product: devops
title: Runbook applicability and procedural loading
order: 5
frozen: true
data:
  id: MX-D-SKILL
  platform: devops
  title: Runbook applicability and procedural loading
  features:
  - FT-D-SKILLS
  sections:
  - D-M04
  trigger: Applicable task or assigned procedural configuration
  state: Skill content, description and agent scope
  process:
    $markdown: field-0001
  effect: Procedural context
  verification: Test matching and nonmatching requests and inspect exposed procedure or tool-use evidence.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-M04
    kind: Procedural-context mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Package
      - Knowledge → Skills → add a skill with SKILL.md and a concrete applicability description.
      - Reusable procedure
    - - Target
      - Select relevant agent types or assign the skill to the custom definition.
      - Consumer scope
    - - Tool dependencies
      - Name real selected operations and expected observations.
      - External prerequisites
    lifecycle:
    - - Skill available
      - Matching task or assigned custom invocation
      - Procedure becomes context.
    - - Procedure updated
      - Run a new applicable test
      - Check the saved content and actual selection.
    - - Skill disabled or unassigned
      - Start subsequent work
      - Do not assume the procedure remains available.
    controls: Skill text is guidance, not authorization; executable-code support is feature-specific.
    observable_output: Saved skill configuration and exposed execution evidence of procedure/tool use.
    undocumented:
      $markdown: field-0006
    test:
    - Provide one request that matches the described symptom and another that does not.
    - Inspect exposed skill/tool-use evidence and the resulting procedure.
    - $markdown: field-0007
    claims:
    - source: DS406
      section: Frontmatter; Creating Skills; Managing Skills
      assertion: Description, target scope and supported content determine applicability.
    - source: DS407
      section: How custom agents work
      assertion: Custom definitions load assigned skill documents.
---

<!-- block: b-d681754a9ba850b0ac3b -->
## process

<!-- block: b-aa483f97511058f8a983 -->
<!-- field: field-0001 -->
Make the reviewed procedure and its references available to the intended execution.
<!-- /field -->

<!-- block: b-155ef196405e5911a080 -->
## on failure

<!-- block: b-0723cb85fd3c5401b051 -->
<!-- field: field-0002 -->
Correct applicability or missing tools; stop unsupported steps without implicitly widening permissions.
<!-- /field -->

<!-- block: b-1e0a5dcba46a52128dca -->
## review / inputs

<!-- block: b-767e622a8c9357068543 -->
<!-- field: field-0003 -->
SKILL.md, applicability description, agent-type targeting and any supporting files; actual tools required by the procedure.
<!-- /field -->

<!-- block: b-9e598b969f045777ae9b -->
## review / narrative / 0

<!-- block: b-99980f42765c5377b0c7 -->
<!-- field: field-0004 -->
A skill packages procedural guidance. Its description tells the built-in agent when to select it; targeting limits which agent types can use it. Assigned skills in a custom definition are loaded through that definition, so built-in relevance selection and explicit custom assignment should not be described as identical entry paths.
<!-- /field -->

<!-- block: b-b0a5bce4ef6b5a338746 -->
## review / narrative / 1

<!-- block: b-a743c21beb8c5ca08c10 -->
<!-- field: field-0005 -->
The procedure still depends on tools that exist and are authorized. Document-only skills do not create a shell. Executable content requires the separately configured Sandbox surface where supported.
<!-- /field -->

<!-- block: b-228d77837d8655c9abce -->
## review / undocumented

<!-- block: b-d851295d064d56748489 -->
<!-- field: field-0006 -->
The cited guide does not specify relevance thresholds or guarantee a skill-selection event in every execution trace.
<!-- /field -->

<!-- block: b-8c4779dff64552318d0a -->
## review / test / 2

<!-- block: b-c8f410a70a535f30a8ee -->
<!-- field: field-0007 -->
Remove a necessary tool; the task must report the blocked step rather than invent its observation.
<!-- /field -->
