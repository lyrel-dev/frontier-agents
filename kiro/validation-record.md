# Kiro — documentation-validation record and presentation transcript

**Day-to-day engineering with the frontier coding agent**

Documentation reviewed: **20 October 2026**. Independent synthesis of official AWS/Kiro sources; not an AWS publication.

**Scope:** Cloud autonomous delivery, repository collaboration, and the IDE/CLI capabilities that support the same engineering workflow. No production deployment authority is assumed.

**Overview:** Use Kiro for bounded engineering outcomes: understand a repository, specify a change, implement and test it, and hand a reviewable pull request to a person. Cloud delivery is the central frontier-agent workflow; local-only controls are labeled separately.

**Read before adoption:** Kiro Web requires an eligible paid plan and is documented in us-east-1 only. It does not automatically merge changes. Local permission prompts, hooks, and file restore behavior must not be assumed to exist in a cloud session. [S02] [S18] [S17] [S21]

## Validation method and outcome

21 capability entries; eight presentation sections; 24 official references.

| Verdict | Entries | Meaning |
|---|---:|---|
| Confirmed | 6 | Core behavior directly documented. |
| Qualified | 14 | Documented behavior with material setup, access, or safety restrictions. |
| Workflow example | 1 | Author-proposed use of documented tools, not a separately established native feature. |

Verdicts are not maturity labels. A confirmed claim can still be preview. Every feature’s availability is recorded separately.

**Validation boundary:** Documentation review only. No AWS account, repository, application, permission policy, prompt, or agent workflow was exercised. Demonstrations and acceptance checks are proposed. No productivity, diagnostic-accuracy, detection-rate, or savings outcome was measured.

**Excluded from this first pass:** Mobile preview, personal-assistant/Crew scenarios, legacy client migration, experimental features, detailed model comparisons, and autonomous production deployment are outside this first pass. Optional workflow orchestration is included only where the account exposes it.

## Recommended starting workflow

1. Confirm the target client, paid Web access, region, and Cloud Sessions policy.

2. Connect a trusted repository and define a small task with evidence-based completion criteria.

3. Review the diff and fresh checks; let the normal human process decide merge and deployment.

## Capability register

### C01 — Understand a repository before editing

**Area:** Coding and specifications  
**Verdict:** Confirmed  
**Availability:** Web · interactive mode  
**Delivery model:** Native; connected repository

**Documented capability:** Inspect connected code, discuss implementation choices, and iterate on a change in a selected branch. [S03] [S09]

**Boundary:** The accessible repository is the evidence base. A plausible explanation is not proof that the runtime behaves as described.

**Prerequisites:** Connect GitHub or GitLab and select the relevant repository and branch. Start with a narrowly scoped question.

**Example task or prompt — author-created, not executed:**

> Explain how request IDs pass through this service. Cite files and symbols, identify gaps, and make no changes yet.

**Engineering acceptance check — recommendation:** Follow the cited call path yourself and compare it with a known request or test trace.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C02 — Plan a feature with requirements, design, and tasks

**Area:** Coding and specifications  
**Verdict:** Confirmed  
**Availability:** IDE / CLI / Web · specifications  
**Delivery model:** Native structured workflow

**Documented capability:** Feature specifications separate requirements, technical design, and implementation tasks before execution. [S08]

**Boundary:** Spec capabilities vary by interface. Requirements analysis and correctness/property-based tooling are not uniformly available in Web.

**Prerequisites:** Provide the desired outcome, constraints, non-goals, and acceptance evidence; select the appropriate specification workflow.

**Example task or prompt — author-created, not executed:**

> Plan request-ID propagation. Preserve public APIs, identify affected components, and propose tests before implementation.

**Engineering acceptance check — recommendation:** Review requirements and design against actual service contracts; reject tasks that expand the agreed scope.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C03 — Specify a bug fix without changing unrelated behavior

**Area:** Coding and specifications  
**Verdict:** Confirmed  
**Availability:** IDE / CLI / Web · bugfix specifications  
**Delivery model:** Native structured workflow

**Documented capability:** Bugfix specifications distinguish current behavior, expected behavior, and behavior that must remain unchanged. [S08]

**Boundary:** The specification is not evidence that the bug is reproduced or the fix is correct.

**Prerequisites:** Provide a minimal reproduction, relevant input, expected output, and regression constraints.

**Example task or prompt — author-created, not executed:**

> Create a bugfix spec for duplicate webhook handling. Define the failing case and the successful flows that must remain unchanged.

**Engineering acceptance check — recommendation:** Require a failing regression test before the change and the same test passing afterward.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C04 — Delegate a bounded outcome through to a pull request

**Area:** Cloud delivery  
**Verdict:** Qualified  
**Availability:** Web / cloud sessions · autonomous mode  
**Delivery model:** Native autonomous execution

**Documented capability:** Autonomous mode can plan work, delegate sub-agents, implement, verify, and open a pull request or merge request. [S04] [S02] [S12]

**Boundary:** It is off by default, can pause for input, and may return an answer instead of a code change. It does not merge into the default branch.

**Prerequisites:** Use an eligible plan, connected repositories, a functioning sandbox, explicit acceptance criteria, and a named human reviewer.

**Example task or prompt — author-created, not executed:**

> Fix this reproducible retry defect, add focused tests, and open a small PR explaining evidence and remaining risks. Do not deploy.

**Engineering acceptance check — recommendation:** Inspect the full diff and actual test output; apply ordinary review and branch-protection rules.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C05 — Coordinate a change across repositories

**Area:** Cloud delivery  
**Verdict:** Qualified  
**Availability:** Web · GitHub and GitLab  
**Delivery model:** Native; provider connections required

**Documented capability:** A task can span multiple repositories, including mixed GitHub and GitLab projects, with a separate PR or MR for each. [S05] [S07]

**Boundary:** Provider access is not implied by the repository picker. GitLab token scope and network reachability matter; VPC-only private GitLab is not supported.

**Prerequisites:** Connect only trusted repositories; validate tokens, write access, default branches, and cross-repository dependency order.

**Example task or prompt — author-created, not executed:**

> Update the shared client and its consuming service for the new optional header. Open linked changes and describe the safe merge order.

**Engineering acceptance check — recommendation:** Run consumer compatibility checks and review whether either change can be deployed independently.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C06 — Assign a GitHub issue to the agent

**Area:** Repository collaboration  
**Verdict:** Confirmed  
**Availability:** Web · GitHub integration  
**Delivery model:** Native issue trigger

**Documented capability:** The documented GitHub flow delegates an issue using the kiro label or a /kiro comment. [S06]

**Boundary:** The app must have repository access and the assigning user needs suitable write access. Multiple assignments can create duplicate tasks.

**Prerequisites:** Install the Kiro GitHub app on selected repositories; give the issue a reproduction and completion criteria.

**Example task or prompt — author-created, not executed:**

> Prepare a small bug issue with expected behavior and test criteria, then assign it using the documented Kiro trigger.

**Engineering acceptance check — recommendation:** Confirm one task owns the issue and that its resulting PR addresses the issue rather than unrelated cleanup.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C07 — Iterate on review feedback and supplied CI failures

**Area:** Repository collaboration  
**Verdict:** Qualified  
**Availability:** Web · GitHub feedback flow  
**Delivery model:** Native PR interaction; trigger restrictions

**Documented capability:** Kiro can address explicit PR feedback through documented commands, including /kiro all or /kiro fix for a thread. [S06]

**Boundary:** The GitHub flow responds to the task creator’s instructions. Automated CI feedback is addressed when user feedback triggers work; do not assume every failed build causes an autonomous retry.

**Prerequisites:** Keep the task creator responsible for feedback and attach the failing job, commit, and test output.

**Example task or prompt — author-created, not executed:**

> Address this review thread and the linked CI failure. Preserve the test intent; report the exact check you reran.

**Engineering acceptance check — recommendation:** Confirm a fresh CI run validates the new commit rather than relying on a previous green result.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C08 — Write tests and verify a UI in the sandbox

**Area:** Coding and specifications  
**Verdict:** Qualified  
**Availability:** Cloud sandbox; local tools where configured  
**Delivery model:** Native tools; project test setup required

**Documented capability:** Code and shell tools support test-writing workflows; the cloud sandbox includes browser tooling for UI inspection and verification. [S09] [S10]

**Boundary:** Available tools do not guarantee adequate coverage, reliable assertions, or access to every test dependency.

**Prerequisites:** Provide reproducible fixtures, test commands, dependency access, and a non-production application endpoint when required.

**Example task or prompt — author-created, not executed:**

> Add a regression test for the empty-state bug, run the affected tests, and inspect the page at a mobile viewport. Report failures honestly.

**Engineering acceptance check — recommendation:** Review assertions, fixture realism, screenshots where relevant, and captured command exit status.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C09 — Schedule small repository-maintenance jobs

**Area:** Cloud delivery  
**Verdict:** Qualified  
**Availability:** Web · paid-plan automations  
**Delivery model:** Native recurring autonomous tasks

**Documented capability:** Automations run a stored prompt against connected repositories on a schedule and can produce reviewable changes. [S11]

**Boundary:** Schedules use UTC and cannot run more often than hourly. Repeated runs still need output review and consumption monitoring.

**Prerequisites:** Define a narrow prompt, repository selection, recurrence, and responsible reviewer; inspect the schedule before activating it.

**Example task or prompt — author-created, not executed:**

> Once a week, identify outdated internal API examples and propose corrections only when a concrete mismatch is found. Avoid empty PRs.

**Engineering acceptance check — recommendation:** Check the UTC-to-local conversion, inspect the first run, and disable the automation when ownership or usefulness lapses.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C10 — Continue cloud work from another client

**Area:** Cloud delivery  
**Verdict:** Confirmed  
**Availability:** IDE / CLI / Web · cloud sessions  
**Delivery model:** Native session continuity

**Documented capability:** Cloud sessions run in a managed environment and can be resumed or steered from supported Kiro clients. [S12]

**Boundary:** The service clones repository content server-side. Unsaved or unpushed local working-copy changes are not automatically uploaded.

**Prerequisites:** Enable Cloud Sessions where required and ensure the intended branch and commit are available to the cloud session.

**Example task or prompt — author-created, not executed:**

> Resume the cloud task for this branch. Summarize completed checks and ask before changing the agreed acceptance criteria.

**Engineering acceptance check — recommendation:** Compare the cloud commit with the intended local change before continuing or reviewing output.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C11 — Apply team conventions through steering

**Area:** Team configuration  
**Verdict:** Qualified  
**Availability:** Documented · interface and access requirements apply  
**Delivery model:** Native context configuration

**Documented capability:** Workspace steering and AGENTS.md can carry repository conventions, architecture guidance, and expected engineering practices. [S13]

**Boundary:** Steering is instruction context, not an access-control boundary. Custom agents do not automatically inherit all steering resources.

**Prerequisites:** Commit concise project guidance and explicitly load necessary resources for custom agents; handle personal cloud context through supported sync.

**Example task or prompt — author-created, not executed:**

> Follow the repository’s API-compatibility and testing guidance. Identify conflicts in those instructions before editing.

**Engineering acceptance check — recommendation:** Check which instructions actually loaded and verify compliance in the resulting diff.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C12 — Reuse learned context without treating it as truth

**Area:** Team configuration  
**Verdict:** Qualified  
**Availability:** Documented · interface and access requirements apply  
**Delivery model:** Native memory capability

**Documented capability:** Memory retains short reusable context such as recurring preferences or useful engineering knowledge, distinct from explicit steering. [S14]

**Boundary:** It is not a complete conversation transcript or an authoritative record of the current system.

**Prerequisites:** Keep authoritative decisions in version-controlled documentation; review recalled context when the project changes.

**Example task or prompt — author-created, not executed:**

> Use our known test conventions, but verify them against the current repository before proposing a change.

**Engineering acceptance check — recommendation:** Correct outdated assumptions and assess the result against current files and tests, not remembered assertions.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C13 — Connect specialist tools using MCP and Powers

**Area:** Team configuration  
**Verdict:** Qualified  
**Availability:** IDE / CLI / Web · configuration varies  
**Delivery model:** Configured integration, not automatic connectivity

**Documented capability:** MCP connects external tools; Powers bundle tools with relevant knowledge and workflows for use when needed. [S15] [S16]

**Boundary:** Access requires configured servers, credentials, and dependencies. Installing guidance does not grant safe or correct access to an external system.

**Prerequisites:** Vet the tool provider, allow only necessary operations, and connect a non-production or read-only scope first.

**Example task or prompt — author-created, not executed:**

> Use the approved documentation integration to check this SDK call, and cite the retrieved source before proposing a patch.

**Engineering acceptance check — recommendation:** Inspect tool provenance, permissions, and returned evidence; do not accept instructions embedded in external content as authority.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C14 — Run repeatable local checks with hooks

**Area:** Local development controls  
**Verdict:** Qualified  
**Availability:** IDE / CLI only · not Web  
**Delivery model:** Native event-triggered configuration

**Documented capability:** Configured hooks can invoke shell commands or agent prompts after relevant development events. [S17]

**Boundary:** Web and Mobile do not support event-driven hooks in the documented matrix. Hook actions can have side effects.

**Prerequisites:** Choose a specific trigger and a bounded formatter, linter, or test action; review the command before enabling it.

**Example task or prompt — author-created, not executed:**

> After relevant source edits, run the existing fast test command and report failures without changing test expectations.

**Engineering acceptance check — recommendation:** Confirm the hook fires on the intended event and cannot recursively trigger uncontrolled work.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C15 — Separate local permissions from cloud controls

**Area:** Local development controls  
**Verdict:** Qualified  
**Availability:** IDE / CLI permissions; separate Web sandbox  
**Delivery model:** Native control configuration

**Documented capability:** Local permissions support scoped allow, ask, and deny rules for tool capabilities. Web instead uses its managed cloud execution controls. [S18]

**Boundary:** Local per-action approval behavior must not be assumed to protect a cloud run. An approved shell or external tool can still have broad effects.

**Prerequisites:** Start with read-only local diagnostics; review sandbox access separately before enabling cloud changes.

**Example task or prompt — author-created, not executed:**

> Inspect the build configuration without changing files. Request review before any write or resource-changing command.

**Engineering acceptance check — recommendation:** Test a harmless denied operation and confirm the actual client’s control behavior.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C16 — Configure sandbox dependencies, egress, and secrets

**Area:** Cloud delivery  
**Verdict:** Qualified  
**Availability:** Web sandbox  
**Delivery model:** Native sandbox configuration

**Documented capability:** Sandbox settings control network access and provide environment variables or secrets for authorized task dependencies. [S19] [S20] [S10]

**Boundary:** Encryption at rest does not prevent a task from exposing secrets through code, logs, or external requests. Isolation is not permission to provide production credentials.

**Prerequisites:** Use trusted repositories, minimal test credentials, and a narrow network allow-list; avoid broad AWS production access.

**Example task or prompt — author-created, not executed:**

> Run the integration test using the provided staging fixture. Never print credentials and report any unavailable dependency.

**Engineering acceptance check — recommendation:** Review allowed endpoints and logs, rotate temporary credentials, and inspect changes for accidental disclosure.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C17 — Recover local work with the correct restore mechanism

**Area:** Local development controls  
**Verdict:** Qualified  
**Availability:** IDE file checkpoints; CLI conversation rewind  
**Delivery model:** Native; different semantics by client

**Documented capability:** IDE checkpoints can restore files and conversation context. CLI rewind forks conversation context but does not revert files. [S21]

**Boundary:** Neither capability is available as a Web file-rollback mechanism; neither reverses changes to external infrastructure.

**Prerequisites:** Use version control alongside the client feature and record the commit before a change.

**Example task or prompt — author-created, not executed:**

> Return to the pre-change discussion, then show the working-tree diff so I can decide which edits to restore.

**Engineering acceptance check — recommendation:** Inspect git status and external side effects explicitly; do not infer restored files from a rewound conversation.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C18 — Diagnose IaC or pipeline failures using supplied evidence

**Area:** Engineering workflow examples  
**Verdict:** Workflow example  
**Availability:** Use supported coding tools; environment setup required  
**Delivery model:** Application of documented file and shell tools

**Documented capability:** A practical workflow is to provide Terraform, CloudFormation, CDK, or pipeline files plus a failure log and request a minimal proposed fix. [S09] [S18]

**Boundary:** This is not a separately documented universal IaC validator, a connected CI monitoring service, or authorization to deploy.

**Prerequisites:** Provide redacted logs, the exact tool version, relevant files, and safe validation commands.

**Example task or prompt — author-created, not executed:**

> Explain the earliest causal error in this failed infrastructure plan. Propose the smallest correction and do not apply changes.

**Engineering acceptance check — recommendation:** Rerun the organization’s existing plan, lint, and policy checks in the intended environment and review all resource changes.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C19 — Reuse a specialist custom agent

**Area:** Team configuration  
**Verdict:** Qualified  
**Availability:** IDE / CLI primary agents; Web sub-agent delegation  
**Delivery model:** Native configuration; client-specific behavior

**Documented capability:** Custom agents define focused instructions, tools, and context. Web can delegate to project-level agents committed in .kiro/agents/. [S22] [S13]

**Boundary:** A custom agent cannot be selected as the primary Web session agent. Local profiles and cloud-loaded configurations have different scope.

**Prerequisites:** Version-control the agent configuration and include only the tools and resources needed for its task.

**Example task or prompt — author-created, not executed:**

> Ask our test-review agent to inspect missing regression coverage and return findings without implementing changes.

**Engineering acceptance check — recommendation:** Check the effective tool list and confirm the reviewer’s evidence is independent of the implementation summary.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C20 — Package a repeatable team procedure as a skill

**Area:** Team configuration  
**Verdict:** Confirmed  
**Availability:** IDE / CLI / Web · workspace skills  
**Delivery model:** Native reusable instruction package

**Documented capability:** Skills package instructions, reference material, and optional scripts for relevant tasks, with workspace scope suitable for shared procedures. [S23]

**Boundary:** A skill is not inherently a security sandbox. Scripts and instructions must be reviewed before the agent uses them.

**Prerequisites:** Create a focused SKILL.md under .kiro/skills/ and commit reviewed supporting material.

**Example task or prompt — author-created, not executed:**

> Use the team’s release-note skill to draft a changelog from merged commits. Do not publish or change the release tag.

**Engineering acceptance check — recommendation:** Validate the included changes, excluded work, and output format against the intended release.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C21 — Orchestrate a repeatable multi-step engineering workflow

**Area:** Team configuration  
**Verdict:** Qualified  
**Availability:** Opt-in · account rollout and client controls vary  
**Delivery model:** Native workflow graph; optional advanced setup

**Documented capability:** Workflows define steps, handoffs, parallel branches, loops, and completion conditions; recipes can be saved for reuse. [S24]

**Boundary:** This is distinct from autonomous mode. Workflows require opt-in; an absent setting can mean the account lacks access. Multi-agent work can consume more tokens.

**Prerequisites:** Enable the feature where available, cap loops, name required evidence, and keep a human merge decision.

**Example task or prompt — author-created, not executed:**

> Create a bounded workflow: investigate, propose a fix, independently review, and rerun the regression test. Stop after two unsuccessful repair cycles.

**Engineering acceptance check — recommendation:** Inspect handoff artifacts and each step’s result. A completed graph is not proof of a correct release.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

## Cross-cutting validation record

### G01 — Availability is not one universal GA label

This report uses the current documented feature matrices rather than claiming every Kiro feature is generally available everywhere. Web access is paid-plan and us-east-1 scoped; organizational Cloud Sessions can require administrator enablement. [S02]

### G02 — Frontier core versus developer companions

Autonomous cloud delivery is the central subject. Hooks, local permission rules, and checkpoint behavior are included because teams use them alongside that workflow, not because they are all Web capabilities. [S04] [S17] [S18] [S21]

### G03 — Repository access and human merge

Keep repository app installation and token access narrow. Kiro’s documented no-auto-merge boundary does not replace branch protections, review responsibility, or deployment controls. [S02] [S06] [S07]

### G04 — Instruction files are not security controls

Steering, skills, and memory affect behavior; permissions and external-system access are separate. Custom agents need explicit context, and third-party instruction packages require review. [S13] [S23] [S14] [S22]

### G05 — Automation and workflow availability

Recurring automations use UTC and are distinct from reusable workflow graphs. Opt-in workflow availability and control surfaces vary; do not promise unattended delivery solely because scheduling exists. [S11] [S24]

### G06 — Secrets and untrusted input

Limit egress and use disposable test credentials. A cloud sandbox does not eliminate malicious repository instructions or the risk of a task exposing injected secrets. [S05] [S20] [S19]

## Structured presentation transcript

Eight sections. Speaking notes are ready to present; demonstrations remain proposed and unexecuted.

### 01 — Start with a reviewable engineering outcome

**On-screen message:** Delegate a bounded change, not an unlimited mandate.

**Speaker transcript:**

The useful starting point is one engineering outcome with observable completion criteria: explain a code path, fix a reproduced defect, or update an interface without breaking consumers. Kiro’s cloud autonomous mode can carry work through implementation and reviewable repository changes. It is not an automatic production-release authority. Our recommended boundary is simple: an engineer owns the task, the evidence, and the merge decision. The local development features in this report support that same workflow, but they are not all available in the browser. Keep those interfaces distinct when planning a team rollout.

**Proposed demonstration — not executed:** Select one small issue, identify the affected repository and reviewer, and write a measurable acceptance check before assigning it.

**Official evidence:** [S04] [S02]

### 02 — Specify success and preserve behavior

**On-screen message:** Requirements and regression evidence precede implementation.

**Speaker transcript:**

Use a feature specification when the desired behavior needs design discussion. Use a bugfix specification when there is a concrete defect and existing behavior to preserve. The important team habit is to make non-goals explicit. In our proposed example, request IDs must propagate correctly without changing existing response contracts. A specification should expose unresolved decisions before code is accepted; it is not itself a successful test. Review generated acceptance criteria for missing negative cases, and use the project’s real build and test commands to establish evidence.

**Proposed demonstration — not executed:** Prepare a feature spec and a bugfix spec for the same service, then compare their scope and required regression checks.

**Official evidence:** [S08] [S09]

### 03 — Move from a task to linked repository changes

**On-screen message:** One outcome can produce several independently reviewed PRs or MRs.

**Speaker transcript:**

For a cross-repository change, identify both the producer and consumer and agree on a safe sequence. Kiro can work across connected repositories, including GitHub and GitLab. That makes consistency work practical, but access and provider limitations still apply. The GitHub issue flow gives teams a familiar assignment point. Avoid duplicate ownership: a second independent assignment can create competing work rather than useful coordination. Our acceptance rule is that each resulting change must explain its dependency on the others and demonstrate compatibility before any merge.

**Proposed demonstration — not executed:** Describe a shared-client change, show the repository selections, and define what evidence each resulting PR or MR must contain.

**Official evidence:** [S05] [S07] [S06]

### 04 — Treat tests and review feedback as evidence

**On-screen message:** A green claim is weaker than a fresh check on the current commit.

**Speaker transcript:**

Ask for test changes and execution evidence together. Browser tooling can help inspect a UI in the sandbox, while project commands provide repeatable checks. The reviewer still needs to examine assertions and failure output. For GitHub feedback, use the documented explicit interaction path rather than assuming the agent watches every failed job independently. Our proposed review checks three things: the reproduced bug disappears, preserved behavior still passes, and the new commit—not an older one—has the expected CI result. Do not accept weakened tests as a repair.

**Proposed demonstration — not executed:** Walk through a proposed regression test, its command output, a review comment, and the evidence required after a follow-up change.

**Official evidence:** [S10] [S09] [S06]

### 05 — Make team knowledge reusable and inspectable

**On-screen message:** Steering, memory, skills, and tools serve different purposes.

**Speaker transcript:**

Steering expresses deliberate project guidance. Memory carries reusable learned context. Skills package procedures, while MCP and Powers provide configured tool access and associated guidance. Keep these concepts separate: an instruction to follow a process does not grant permission, and a connected tool does not establish the truth of its output. Our recommendation is to keep authoritative standards in version control and use a small number of reviewed packages. Introduce specialist agents only when a focused role improves the review process; check their actual context and tools rather than assuming they inherit everything.

**Proposed demonstration — not executed:** Show one steering file, one narrowly scoped skill, and the effective tool list for a proposed test-review agent.

**Official evidence:** [S13] [S14] [S23] [S15] [S16] [S22]

### 06 — Automate the repetitive work, not the approval decision

**On-screen message:** Schedules and workflow graphs require different controls.

**Speaker transcript:**

A scheduled automation is useful for a recurring bounded job such as checking documentation drift. A workflow graph is useful when work needs explicit handoffs and independent checks. Neither should become an unowned source of repository churn. Our pilot starts with one recurrence and an instruction to produce no change when nothing is wrong. Check UTC schedule interpretation, consumption, and reviewer workload. For workflows, confirm account availability, limit retries, and specify the artifacts required to conclude each step. Keep small tasks in a normal session when orchestration adds more work than it removes.

**Proposed demonstration — not executed:** Draft one weekly maintenance automation and one two-stage review workflow; leave both disabled until their owner approves the configuration.

**Official evidence:** [S11] [S24]

### 07 — Apply controls in the interface where work actually runs

**On-screen message:** Local approvals are not cloud approvals; rewind is not infrastructure rollback.

**Speaker transcript:**

A developer may begin in the IDE and continue in a cloud session, but that does not carry every local control into the cloud. Local hooks and permission rules have their own support boundaries. Cloud execution needs separate network, credential, and repository review. Similarly, an IDE checkpoint and a CLI conversation rewind do different things. The safe engineering practice is to know the exact branch and commit, limit external access, and retain normal version-control and recovery procedures. Never supply production credentials merely because a task runs in an isolated environment.

**Proposed demonstration — not executed:** Compare a local read-only diagnostic setup with a cloud sandbox configuration; inspect the git diff after a conversation rewind.

**Official evidence:** [S12] [S18] [S17] [S19] [S20] [S21]

### 08 — Measure accepted work, not generated volume

**On-screen message:** A successful pilot improves delivery without lowering the quality bar.

**Speaker transcript:**

Our proposed thirty-day pilot uses a small, representative issue set and records outcomes before and after assistance. Measure accepted changes, reviewer corrections, escaped regressions, and total human effort, including setup and supervision. These are evaluation recommendations, not published product guarantees. Keep failed or abandoned tasks in the results so the team does not confuse impressive examples with reliable performance. Expand only when the same review standard holds across repeated tasks. Defer production-changing tool access and complex orchestration until the simpler workflow has demonstrated value in your environment.

**Proposed demonstration — not executed:** Review the pilot scorecard and classify each task as accepted, reworked, abandoned, or blocked by setup; retain the underlying evidence.

**Official evidence:** [S02] [S04]

## Recommended 30-day pilot

This is an adoption experiment, not a product feature or a vendor performance promise.

### Days 1–3 — Scope and access

Choose two trusted repositories, an eligible account, and one reviewer per task. Record branch protections, cloud enablement, and prohibited actions.

### Days 4–7 — Small reproducible fixes

Try code comprehension and two bounded bug fixes. Record the reproduction, human effort, test results, and reasons for rejected output.

### Days 8–14 — Structured changes

Use specs for one feature and one cross-repository change. Review compatibility, merge ordering, and current-commit CI evidence.

### Days 15–21 — Reusable team context

Version-control a steering file and a reviewed skill. Trial one disabled-by-default automation; activate only after ownership and schedule checks.

### Days 22–30 — Evaluate and constrain

Compare accepted outcomes with the baseline. Retain useful patterns, remove noisy automations, and review tool/secret access before expansion.

### Recommended measures

Recommended measures: accepted-task ratio; reviewer rework; human minutes including setup; regression rate; actual task consumption; and changes rejected for access or evidence gaps. No baseline, savings, or accuracy results have been measured.

## Official source register

All sources checked on 20 October 2026. Recheck current documentation before enabling a workflow.

### S01 — AWS frontier agents

**Type:** Official product page  
**Relevant sections:** Meet the frontier agents

Establishes Kiro as part of the AWS frontier-agent portfolio.

[Open official source](https://aws.amazon.com/ai/frontier-agents/)

### S02 — Kiro Web

**Type:** Product documentation  
**Relevant sections:** Prerequisites; ways to work

Paid-plan access, administrator enablement, region, and human merge boundary.

[Open official source](https://kiro.dev/docs/web/)

### S03 — Working with the agent

**Type:** Product documentation  
**Relevant sections:** Start a session

Interactive collaboration and repository/branch selection.

[Open official source](https://kiro.dev/docs/web/using-the-agent/)

### S04 — Autonomous mode

**Type:** Product documentation  
**Relevant sections:** How autonomous mode works; task outcomes

Plans, delegated implementation, verification, and PR/MR delivery.

[Open official source](https://kiro.dev/docs/web/autonomous-mode/)

### S05 — Creating tasks

**Type:** Product documentation  
**Relevant sections:** From app.kiro.dev; multi-repository tasks

Cross-provider changes and trusted-repository warning.

[Open official source](https://kiro.dev/docs/web/using-the-agent/creating-tasks/)

### S06 — GitHub integration

**Type:** Product documentation  
**Relevant sections:** Installation; issue tasks; pull-request feedback

Provider-specific triggers and feedback behavior.

[Open official source](https://kiro.dev/docs/web/github/)

### S07 — GitLab integration

**Type:** Product documentation  
**Relevant sections:** Connection; access requirements

Token scope and private-network limitations.

[Open official source](https://kiro.dev/docs/web/gitlab/)

### S08 — Specifications

**Type:** Product documentation  
**Relevant sections:** Capability matrix; feature and bugfix specifications

Feature planning, preservation requirements, and interface differences.

[Open official source](https://kiro.dev/docs/specs/)

### S09 — Built-in tools

**Type:** Product documentation  
**Relevant sections:** File, search, and shell tools

Engineering primitives, not a universal CI or infrastructure connector.

[Open official source](https://kiro.dev/docs/tools/)

### S10 — Cloud sandbox

**Type:** Product documentation  
**Relevant sections:** Sandbox environment; browser tools

Isolated execution and browser verification tools.

[Open official source](https://kiro.dev/docs/web/sandbox/)

### S11 — Automations

**Type:** Product documentation  
**Relevant sections:** Create and manage automations; schedules

Recurring cloud tasks, UTC scheduling, and enable/disable controls.

[Open official source](https://kiro.dev/docs/web/automations/)

### S12 — Cloud sessions

**Type:** Product documentation  
**Relevant sections:** Client capabilities; repositories

Session continuity and server-side repository cloning.

[Open official source](https://kiro.dev/docs/cloud-sessions/)

### S13 — Steering

**Type:** Product documentation  
**Relevant sections:** Locations; custom agents

Explicit project guidance and loading boundaries.

[Open official source](https://kiro.dev/docs/steering/)

### S14 — Memory

**Type:** Product documentation  
**Relevant sections:** What memory is; relation to steering

Reusable learned context is not a complete transcript or a permission policy.

[Open official source](https://kiro.dev/docs/memory/)

### S15 — Model Context Protocol

**Type:** Product documentation  
**Relevant sections:** Capability matrix; server configuration

Tool connection prerequisites and interface support.

[Open official source](https://kiro.dev/docs/mcp/)

### S16 — Powers

**Type:** Product documentation  
**Relevant sections:** Capability matrix; activation

Tools bundled with guidance; authoring and usage differ by interface.

[Open official source](https://kiro.dev/docs/powers/)

### S17 — Hooks

**Type:** Product documentation  
**Relevant sections:** Capability matrix; trigger/action examples

Event-driven hooks are IDE/CLI features, not Web features.

[Open official source](https://kiro.dev/docs/hooks/)

### S18 — Permissions

**Type:** Product documentation  
**Relevant sections:** Capability matrix; permission rules

Local allow/ask/deny controls versus managed Web sandbox.

[Open official source](https://kiro.dev/docs/permissions/)

### S19 — Sandbox internet access

**Type:** Product documentation  
**Relevant sections:** Network access levels

Network allow-list options.

[Open official source](https://kiro.dev/docs/web/sandbox/internet-access/)

### S20 — Environment variables and secrets

**Type:** Product documentation  
**Relevant sections:** Secrets; security considerations

Encryption does not prevent disclosure through code, logs, or network requests.

[Open official source](https://kiro.dev/docs/web/sandbox/environment-variables/)

### S21 — Checkpoints and rewind

**Type:** Product documentation  
**Relevant sections:** Capability matrix; restore behavior

IDE file restore, CLI conversation rewind, and Web exclusions.

[Open official source](https://kiro.dev/docs/checkpoints/)

### S22 — Custom agents

**Type:** Product documentation  
**Relevant sections:** Surface behavior; configuration files

Web project agents are delegated sub-agents, not selectable primary session agents.

[Open official source](https://kiro.dev/docs/custom-agents/)

### S23 — Agent Skills

**Type:** Product documentation  
**Relevant sections:** Skill scope; activation; custom agents

Reusable instruction packages; workspace and global scope differ.

[Open official source](https://kiro.dev/docs/skills/)

### S24 — Workflows

**Type:** Product documentation  
**Relevant sections:** Turn it on; client support; workflow graph

Opt-in workflow orchestration; account rollout and client controls vary.

[Open official source](https://kiro.dev/docs/workflows/)

---

### Reference links

[S01]: https://aws.amazon.com/ai/frontier-agents/ "AWS frontier agents"

[S02]: https://kiro.dev/docs/web/ "Kiro Web"

[S03]: https://kiro.dev/docs/web/using-the-agent/ "Working with the agent"

[S04]: https://kiro.dev/docs/web/autonomous-mode/ "Autonomous mode"

[S05]: https://kiro.dev/docs/web/using-the-agent/creating-tasks/ "Creating tasks"

[S06]: https://kiro.dev/docs/web/github/ "GitHub integration"

[S07]: https://kiro.dev/docs/web/gitlab/ "GitLab integration"

[S08]: https://kiro.dev/docs/specs/ "Specifications"

[S09]: https://kiro.dev/docs/tools/ "Built-in tools"

[S10]: https://kiro.dev/docs/web/sandbox/ "Cloud sandbox"

[S11]: https://kiro.dev/docs/web/automations/ "Automations"

[S12]: https://kiro.dev/docs/cloud-sessions/ "Cloud sessions"

[S13]: https://kiro.dev/docs/steering/ "Steering"

[S14]: https://kiro.dev/docs/memory/ "Memory"

[S15]: https://kiro.dev/docs/mcp/ "Model Context Protocol"

[S16]: https://kiro.dev/docs/powers/ "Powers"

[S17]: https://kiro.dev/docs/hooks/ "Hooks"

[S18]: https://kiro.dev/docs/permissions/ "Permissions"

[S19]: https://kiro.dev/docs/web/sandbox/internet-access/ "Sandbox internet access"

[S20]: https://kiro.dev/docs/web/sandbox/environment-variables/ "Environment variables and secrets"

[S21]: https://kiro.dev/docs/checkpoints/ "Checkpoints and rewind"

[S22]: https://kiro.dev/docs/custom-agents/ "Custom agents"

[S23]: https://kiro.dev/docs/skills/ "Agent Skills"

[S24]: https://kiro.dev/docs/workflows/ "Workflows"