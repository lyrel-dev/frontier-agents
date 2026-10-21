# Kiro

Repository-scoped planning, implementation, testing and review workflows.


Revision: 21 October 2026. Independent engineering field guide.


**Audience:** Software engineers, technical leads and developer-platform teams

**Availability:** Kiro Web is preview, requires eligible paid access, and has documented Region and administrator controls. IDE, CLI and Web features are not interchangeable.

**Recommended starting decision:** Delegate a small reviewable change with a concrete regression test. Keep merge, release and production credentials outside the task.


## Decision brief

A useful coding agent does more than generate lines of code. It turns an understood requirement into a reviewable change, with enough implementation and test evidence for another engineer to decide whether to accept it. That requires a bounded repository context, clear behavior and an environment that can run the relevant checks.

The running example adds request-ID propagation to checkout-api without changing public behavior elsewhere. It begins with repository understanding, uses specifications when the expected behavior needs agreement, and ends at a pull request. A second example schedules a tightly scoped maintenance task. Web autonomy, local hooks and cloud sandbox controls are kept separate throughout.


## Running use case

**Name:** Propagate request IDs through checkout-api

**Trigger:** A developer cannot correlate an incoming checkout request with its downstream calls.

**Scope:** Selected repository and branch; no schema change, production access or unrelated dependency upgrades.

**Deliverable:** A PR/MR containing the change, meaningful tests and a review explanation.

**Not Done:** Code was generated, but the relevant tests were not run or the diff exceeds the agreed scope.

**Done:** A reviewer verifies propagation and failure behavior, confirms the tests, and makes the merge decision.


## 1. Understand the code before choosing the mode

Use an interactive session while the problem is still ambiguous. Ask for the request path, the relevant symbols and the boundaries where request IDs disappear. The repository gives the agent evidence about the implementation; it does not prove how a deployed service behaves.

Move to autonomous work only after the desired outcome and exclusions are clear. Web sessions, local IDE/CLI work and cloud-session continuation have different entry points and controls. Verify the plan, client and administrator configuration rather than assuming a feature described for one surface exists on every other surface.

**Capability crosswalk:** C01, C04, C10

**Responsible role (team recommendation):** Developer/repository owner

**Input:** Repository, branch, reproduced problem and a named reviewer.

**Artifact:** A cited code-path explanation and a bounded task statement.

**Gate:** The owner can describe the intended behavior and what must not change.

**Fallback:** Stay interactive and investigate missing runtime evidence instead of delegating an ambiguous outcome.


## 2. Make the intended behavior inspectable

For the request-ID change, define what happens when the header is present, absent or invalid, which outbound calls receive it, and which logging fields must not contain sensitive data. Specifications make requirements, design choices and implementation tasks reviewable before the patch grows.

Steering can carry coding conventions; memory can retain useful working context. Neither changes authorization or turns a remembered assumption into verified fact. Keep the task's acceptance criteria explicit and correct stale context before it influences implementation.

**Capability crosswalk:** C02, C03, C11, C12

**Responsible role (team recommendation):** Developer and reviewer

**Input:** Observed gap, compatibility constraints, team conventions and expected failure cases.

**Artifact:** An agreed feature or bug-fix specification with tests linked to behavior.

**Gate:** A reviewer can tell an acceptable implementation from a plausible but incompatible one.

**Fallback:** Reduce the task to one contract boundary and resolve open questions before adding more repositories.


## 3. Configure the environment that will execute the work

The sandbox needs the dependencies and access required to run the chosen checks. Configure setup commands, permitted network access and narrowly scoped test secrets deliberately. A failed test caused by a missing dependency is not evidence that the implementation itself is wrong or right.

MCP and Powers extend the tools available to the agent. Review their credential scope and side effects. Local permissions and hooks do not automatically govern Web execution; local file-save checks and cloud recurring jobs are different mechanisms. Keep production credentials out of the coding task.

**Capability crosswalk:** C08, C13, C14, C15, C16

**Responsible role (team recommendation):** Platform or repository administrator

**Input:** Known setup commands, test configuration, approved tools and minimal test credentials.

**Artifact:** An executable task environment with documented access and known limitations.

**Gate:** The same meaningful checks can run under the intended execution surface.

**Fallback:** Record the environment failure and move verification to approved CI; do not mark an unexecuted test as passed.


## 4. Implement within the contract and inspect the evidence

A bounded autonomous task can plan the change, edit code and open a reviewable PR. When several repositories are involved, identify each affected contract and the evidence required in each repository. The issue or prompt should name the target branch and exclude unrelated refactoring.

For the example, inspect the request-header handling, downstream propagation and tests for both existing and generated IDs. Generated tests only help when their assertions exercise the requirement and their execution result is available. A screenshot or passing command is not a substitute for reviewing what was actually checked.

**Capability crosswalk:** C04, C05, C06, C08

**Responsible role (team recommendation):** Implementing engineer and reviewer

**Input:** Approved task, repository scope and runnable verification commands.

**Artifact:** A focused diff with test source, execution results and residual limitations.

**Gate:** Every changed area can be justified by the stated outcome.

**Fallback:** Split an oversized change into reviewable units rather than accepting a cross-repository patch on faith.


## 5. Treat review feedback as new constrained work

The PR is the start of independent acceptance, not the end of responsibility. Check the diff, test meaningful negative cases and provide precise feedback. Supplied CI failures can guide another iteration, but a coding workflow is not automatically a connected CI-monitoring service.

Use the correct recovery mechanism for the client. Local file checkpoints and conversation rewind are not general production rollback. IaC drafts, pipeline diagnosis and runbook writing are composed uses of coding tools; validate them with the relevant provider tooling, CI job or safe rehearsal.

**Capability crosswalk:** C07, C17, C18

**Responsible role (team recommendation):** PR reviewer

**Input:** PR/MR, review comments and the actual failing check where applicable.

**Artifact:** An updated change and a documented reviewer decision.

**Gate:** The reviewer, not the agent, decides whether the change meets the contract and can merge.

**Fallback:** Reject or revert the branch change using normal source-control practice when acceptance fails.


## 6. Automate only the maintenance that is already understood

A recurring dependency-maintenance job should define allowed version changes, prohibited packages, required tests and the reviewer. Kiro automations can run recurring repository tasks and propose changes; the schedule does not authorize an automatic production release.

Custom agents, skills and workflows can package repeated procedures, but their surface support and rollout conditions differ. Start with one job whose result is easy to inspect. Measure accepted changes, review effort and escaped defects before expanding the task or repository scope.

**Capability crosswalk:** C09, C19, C20, C21

**Responsible role (team recommendation):** Maintenance workflow owner

**Input:** A repeatable procedure, precise schedule, repository boundary and stop owner.

**Artifact:** A recurring reviewable change with an audit trail and test evidence.

**Gate:** Every run remains bounded, independently reviewed and easy to pause.

**Fallback:** Disable or narrow the automation when it produces noisy, unreviewed or out-of-scope changes.


## Detailed capability reference


### C01 — Understand a repository before editing

**Claim:** Inspect connected code, discuss implementation choices, and iterate on a change in a selected branch.

**Availability:** Web · interactive mode

**Delivery:** Native; connected repository

**Setup:** Connect GitHub or GitLab and select the relevant repository and branch. Start with a narrowly scoped question.

**Limit:** The accessible repository is the evidence base. A plausible explanation is not proof that the runtime behaves as described.

**Check:** Follow the cited call path yourself and compare it with a known request or test trace.

**Prompt:** Explain how request IDs pass through this service. Cite files and symbols, identify gaps, and make no changes yet.

**Review record to retain (team recommendation):** Repository map and file/symbol references for the investigated path.

Official documentation references: S03, S09


### C02 — Plan a feature with requirements, design, and tasks

**Claim:** Feature specifications separate requirements, technical design, and implementation tasks before execution.

**Availability:** IDE / CLI / Web · specifications

**Delivery:** Native structured workflow

**Setup:** Provide the desired outcome, constraints, non-goals, and acceptance evidence; select the appropriate specification workflow.

**Limit:** Spec capabilities vary by interface. Requirements analysis and correctness/property-based tooling are not uniformly available in Web.

**Check:** Review requirements and design against actual service contracts; reject tasks that expand the agreed scope.

**Prompt:** Plan request-ID propagation. Preserve public APIs, identify affected components, and propose tests before implementation.

**Review record to retain (team recommendation):** Versioned requirements, design decisions, implementation tasks, and open questions.

Official documentation references: S08


### C03 — Specify a bug fix without changing unrelated behavior

**Claim:** Bugfix specifications distinguish current behavior, expected behavior, and behavior that must remain unchanged.

**Availability:** IDE / CLI / Web · bugfix specifications

**Delivery:** Native structured workflow

**Setup:** Provide a minimal reproduction, relevant input, expected output, and regression constraints.

**Limit:** The specification is not evidence that the bug is reproduced or the fix is correct.

**Check:** Require a failing regression test before the change and the same test passing afterward.

**Prompt:** Create a bugfix spec for duplicate webhook handling. Define the failing case and the successful flows that must remain unchanged.

**Review record to retain (team recommendation):** Current/expected behavior specification with preservation constraints and regression cases.

Official documentation references: S08


### C04 — Delegate a bounded outcome through to a pull request

**Claim:** Autonomous mode can plan work, delegate sub-agents, implement, verify, and open a pull request or merge request.

**Availability:** Web / cloud sessions · autonomous mode

**Delivery:** Native autonomous execution

**Setup:** Use an eligible plan, connected repositories, a functioning sandbox, explicit acceptance criteria, and a named human reviewer.

**Limit:** It is off by default, can pause for input, and may return an answer instead of a code change. It does not merge into the default branch.

**Check:** Inspect the full diff and actual test output; apply ordinary review and branch-protection rules.

**Prompt:** Fix this reproducible retry defect, add focused tests, and open a small PR explaining evidence and remaining risks. Do not deploy.

**Review record to retain (team recommendation):** Pull request with scoped diff, execution output, and unresolved review points.

Official documentation references: S04, S02, S12


### C05 — Coordinate a change across repositories

**Claim:** A task can span multiple repositories, including mixed GitHub and GitLab projects, with a separate PR or MR for each.

**Availability:** Web · GitHub and GitLab

**Delivery:** Native; provider connections required

**Setup:** Connect only trusted repositories; validate tokens, write access, default branches, and cross-repository dependency order.

**Limit:** Provider access is not implied by the repository picker. GitLab token scope and network reachability matter; VPC-only private GitLab is not supported.

**Check:** Run consumer compatibility checks and review whether either change can be deployed independently.

**Prompt:** Update the shared client and its consuming service for the new optional header. Open linked changes and describe the safe merge order.

**Review record to retain (team recommendation):** Repository-specific diffs with a cross-repository dependency and review checklist.

Official documentation references: S05, S07


### C06 — Assign a GitHub issue to the agent

**Claim:** The documented GitHub flow delegates an issue using the kiro label or a /kiro comment.

**Availability:** Web · GitHub integration

**Delivery:** Native issue trigger

**Setup:** Install the Kiro GitHub app on selected repositories; give the issue a reproduction and completion criteria.

**Limit:** The app must have repository access and the assigning user needs suitable write access. Multiple assignments can create duplicate tasks.

**Check:** Confirm one task owns the issue and that its resulting PR addresses the issue rather than unrelated cleanup.

**Prompt:** Prepare a small bug issue with expected behavior and test criteria, then assign it using the documented Kiro trigger.

**Review record to retain (team recommendation):** GitHub issue, delegated task, resulting change proposal, and reviewer decision.

Official documentation references: S06


### C07 — Iterate on review feedback and supplied CI failures

**Claim:** Kiro can address explicit PR feedback through documented commands, including /kiro all or /kiro fix for a thread.

**Availability:** Web · GitHub feedback flow

**Delivery:** Native PR interaction; trigger restrictions

**Setup:** Keep the task creator responsible for feedback and attach the failing job, commit, and test output.

**Limit:** The GitHub flow responds to the task creator’s instructions. Automated CI feedback is addressed when user feedback triggers work; do not assume every failed build causes an autonomous retry.

**Check:** Confirm a fresh CI run validates the new commit rather than relying on a previous green result.

**Prompt:** Address this review thread and the linked CI failure. Preserve the test intent; report the exact check you reran.

**Review record to retain (team recommendation):** Updated PR diff with link to comments, failing checks, and verification reruns.

Official documentation references: S06


### C08 — Write tests and verify a UI in the sandbox

**Claim:** Code and shell tools support test-writing workflows; the cloud sandbox includes browser tooling for UI inspection and verification.

**Availability:** Cloud sandbox; local tools where configured

**Delivery:** Native tools; project test setup required

**Setup:** Provide reproducible fixtures, test commands, dependency access, and a non-production application endpoint when required.

**Limit:** Available tools do not guarantee adequate coverage, reliable assertions, or access to every test dependency.

**Check:** Review assertions, fixture realism, screenshots where relevant, and captured command exit status.

**Prompt:** Add a regression test for the empty-state bug, run the affected tests, and inspect the page at a mobile viewport. Report failures honestly.

**Review record to retain (team recommendation):** Test source, runner output, and UI/browser evidence when applicable.

Official documentation references: S09, S10


### C09 — Schedule small repository-maintenance jobs

**Claim:** Automations run a stored prompt against connected repositories on a schedule and can produce reviewable changes.

**Availability:** Web · paid-plan automations

**Delivery:** Native recurring autonomous tasks

**Setup:** Define a narrow prompt, repository selection, recurrence, and responsible reviewer; inspect the schedule before activating it.

**Limit:** Schedules use UTC and cannot run more often than hourly. Repeated runs still need output review and consumption monitoring.

**Check:** Check the UTC-to-local conversion, inspect the first run, and disable the automation when ownership or usefulness lapses.

**Prompt:** Once a week, identify outdated internal API examples and propose corrections only when a concrete mismatch is found. Avoid empty PRs.

**Review record to retain (team recommendation):** Scheduled task record, proposed maintenance diff, and assigned reviewer.

Official documentation references: S11


### C10 — Continue cloud work from another client

**Claim:** Cloud sessions run in a managed environment and can be resumed or steered from supported Kiro clients.

**Availability:** IDE / CLI / Web · cloud sessions

**Delivery:** Native session continuity

**Setup:** Enable Cloud Sessions where required and ensure the intended branch and commit are available to the cloud session.

**Limit:** The service clones repository content server-side. Unsaved or unpushed local working-copy changes are not automatically uploaded.

**Check:** Compare the cloud commit with the intended local change before continuing or reviewing output.

**Prompt:** Resume the cloud task for this branch. Summarize completed checks and ask before changing the agreed acceptance criteria.

**Review record to retain (team recommendation):** Cloud-session record, applied changes, and the final reviewed artifact.

Official documentation references: S12


### C11 — Apply team conventions through steering

**Claim:** Workspace steering and AGENTS.md can carry repository conventions, architecture guidance, and expected engineering practices.

**Availability:** Documented · interface and access requirements apply

**Delivery:** Native context configuration

**Setup:** Commit concise project guidance and explicitly load necessary resources for custom agents; handle personal cloud context through supported sync.

**Limit:** Steering is instruction context, not an access-control boundary. Custom agents do not automatically inherit all steering resources.

**Check:** Check which instructions actually loaded and verify compliance in the resulting diff.

**Prompt:** Follow the repository’s API-compatibility and testing guidance. Identify conflicts in those instructions before editing.

**Review record to retain (team recommendation):** Versioned steering file with documented conventions and a change-review record.

Official documentation references: S13


### C12 — Reuse learned context without treating it as truth

**Claim:** Memory retains short reusable context such as recurring preferences or useful engineering knowledge, distinct from explicit steering.

**Availability:** Documented · interface and access requirements apply

**Delivery:** Native memory capability

**Setup:** Keep authoritative decisions in version-controlled documentation; review recalled context when the project changes.

**Limit:** It is not a complete conversation transcript or an authoritative record of the current system.

**Check:** Correct outdated assumptions and assess the result against current files and tests, not remembered assertions.

**Prompt:** Use our known test conventions, but verify them against the current repository before proposing a change.

**Review record to retain (team recommendation):** Inspectable stored context and a correction record when recalled information is wrong.

Official documentation references: S14


### C13 — Connect specialist tools using MCP and Powers

**Claim:** MCP connects external tools; Powers bundle tools with relevant knowledge and workflows for use when needed.

**Availability:** IDE / CLI / Web · configuration varies

**Delivery:** Configured integration, not automatic connectivity

**Setup:** Vet the tool provider, allow only necessary operations, and connect a non-production or read-only scope first.

**Limit:** Access requires configured servers, credentials, and dependencies. Installing guidance does not grant safe or correct access to an external system.

**Check:** Inspect tool provenance, permissions, and returned evidence; do not accept instructions embedded in external content as authority.

**Prompt:** Use the approved documentation integration to check this SDK call, and cite the retrieved source before proposing a patch.

**Review record to retain (team recommendation):** Named MCP/Powers integration scope and records of calls affecting external systems.

Official documentation references: S15, S16


### C14 — Run repeatable local checks with hooks

**Claim:** Configured hooks can invoke shell commands or agent prompts after relevant development events.

**Availability:** IDE / CLI only · not Web

**Delivery:** Native event-triggered configuration

**Setup:** Choose a specific trigger and a bounded formatter, linter, or test action; review the command before enabling it.

**Limit:** Web and Mobile do not support event-driven hooks in the documented matrix. Hook actions can have side effects.

**Check:** Confirm the hook fires on the intended event and cannot recursively trigger uncontrolled work.

**Prompt:** After relevant source edits, run the existing fast test command and report failures without changing test expectations.

**Review record to retain (team recommendation):** Hook configuration, invoked commands, exit status, and repository changes.

Official documentation references: S17


### C15 — Separate local permissions from cloud controls

**Claim:** Local permissions support scoped allow, ask, and deny rules for tool capabilities. Web instead uses its managed cloud execution controls.

**Availability:** IDE / CLI permissions; separate Web sandbox

**Delivery:** Native control configuration

**Setup:** Start with read-only local diagnostics; review sandbox access separately before enabling cloud changes.

**Limit:** Local per-action approval behavior must not be assumed to protect a cloud run. An approved shell or external tool can still have broad effects.

**Check:** Test a harmless denied operation and confirm the actual client’s control behavior.

**Prompt:** Inspect the build configuration without changing files. Request review before any write or resource-changing command.

**Review record to retain (team recommendation):** Permission rules and negative test showing blocked out-of-scope operations.

Official documentation references: S18


### C16 — Configure sandbox dependencies, egress, and secrets

**Claim:** Sandbox settings control network access and provide environment variables or secrets for authorized task dependencies.

**Availability:** Web sandbox

**Delivery:** Native sandbox configuration

**Setup:** Use trusted repositories, minimal test credentials, and a narrow network allow-list; avoid broad AWS production access.

**Limit:** Encryption at rest does not prevent a task from exposing secrets through code, logs, or external requests. Isolation is not permission to provide production credentials.

**Check:** Review allowed endpoints and logs, rotate temporary credentials, and inspect changes for accidental disclosure.

**Prompt:** Run the integration test using the provided staging fixture. Never print credentials and report any unavailable dependency.

**Review record to retain (team recommendation):** Sandbox configuration including approved egress, injected settings, and secret-handling checks.

Official documentation references: S19, S20, S10


### C17 — Recover local work with the correct restore mechanism

**Claim:** IDE checkpoints can restore files and conversation context. CLI rewind forks conversation context but does not revert files.

**Availability:** IDE file checkpoints; CLI conversation rewind

**Delivery:** Native; different semantics by client

**Setup:** Use version control alongside the client feature and record the commit before a change.

**Limit:** Neither capability is available as a Web file-rollback mechanism; neither reverses changes to external infrastructure.

**Check:** Inspect git status and external side effects explicitly; do not infer restored files from a rewound conversation.

**Prompt:** Return to the pre-change discussion, then show the working-tree diff so I can decide which edits to restore.

**Review record to retain (team recommendation):** Restoration record or new branch/fork demonstrating which work state was recovered.

Official documentation references: S21


### C18 — Diagnose IaC or pipeline failures using supplied evidence

**Claim:** A practical workflow is to provide Terraform, CloudFormation, CDK, or pipeline files plus a failure log and request a minimal proposed fix.

**Availability:** Use supported coding tools; environment setup required

**Delivery:** Application of documented file and shell tools

**Setup:** Provide redacted logs, the exact tool version, relevant files, and safe validation commands.

**Limit:** This is not a separately documented universal IaC validator, a connected CI monitoring service, or authorization to deploy.

**Check:** Rerun the organization’s existing plan, lint, and policy checks in the intended environment and review all resource changes.

**Prompt:** Explain the earliest causal error in this failed infrastructure plan. Propose the smallest correction and do not apply changes.

**Review record to retain (team recommendation):** Evidence-backed failure analysis, proposed file change, and independent command output.

Official documentation references: S09, S18


### C19 — Reuse a specialist custom agent

**Claim:** Custom agents define focused instructions, tools, and context. Web can delegate to project-level agents committed in .kiro/agents/.

**Availability:** IDE / CLI primary agents; Web sub-agent delegation

**Delivery:** Native configuration; client-specific behavior

**Setup:** Version-control the agent configuration and include only the tools and resources needed for its task.

**Limit:** A custom agent cannot be selected as the primary Web session agent. Local profiles and cloud-loaded configurations have different scope.

**Check:** Check the effective tool list and confirm the reviewer’s evidence is independent of the implementation summary.

**Prompt:** Ask our test-review agent to inspect missing regression coverage and return findings without implementing changes.

**Review record to retain (team recommendation):** Custom-agent configuration, scoped task result, and approval of its output.

Official documentation references: S22, S13


### C20 — Package a repeatable team procedure as a skill

**Claim:** Skills package instructions, reference material, and optional scripts for relevant tasks, with workspace scope suitable for shared procedures.

**Availability:** IDE / CLI / Web · workspace skills

**Delivery:** Native reusable instruction package

**Setup:** Create a focused SKILL.md under .kiro/skills/ and commit reviewed supporting material.

**Limit:** A skill is not inherently a security sandbox. Scripts and instructions must be reviewed before the agent uses them.

**Check:** Validate the included changes, excluded work, and output format against the intended release.

**Prompt:** Use the team’s release-note skill to draft a changelog from merged commits. Do not publish or change the release tag.

**Review record to retain (team recommendation):** Versioned skill instructions and a reproducibility review for included scripts.

Official documentation references: S23


### C21 — Orchestrate a repeatable multi-step engineering workflow

**Claim:** Workflows define steps, handoffs, parallel branches, loops, and completion conditions; recipes can be saved for reuse.

**Availability:** Opt-in · account rollout and client controls vary

**Delivery:** Native workflow graph; optional advanced setup

**Setup:** Enable the feature where available, cap loops, name required evidence, and keep a human merge decision.

**Limit:** This is distinct from autonomous mode. Workflows require opt-in; an absent setting can mean the account lacks access. Multi-agent work can consume more tokens.

**Check:** Inspect handoff artifacts and each step’s result. A completed graph is not proof of a correct release.

**Prompt:** Create a bounded workflow: investigate, propose a fix, independently review, and rerun the regression test. Stop after two unsuccessful repair cycles.

**Review record to retain (team recommendation):** Workflow definition, per-step artifacts, failures, handoffs, and completion status.

Official documentation references: S24


## Illustrative handoff

```yaml

task: request-id-propagation
repository: checkout-api
branch: feature/request-id-demo
allowed_effects: [read-code, edit-branch, run-test-suite, propose-pr]
constraints: [no-schema-change, no-production-access]
acceptance: [existing-id-preserved, missing-id-created, outbound-id-propagated]
reviewer: service-maintainer
merge: human-decision

```


## Readiness checklist

- [ ] Target client, paid access and administrator enablement are confirmed.

- [ ] Repository and branch are explicitly selected.

- [ ] Behavior, exclusions and regression tests are written down.

- [ ] Sandbox tools, egress and secrets have been reviewed.

- [ ] The diff and actual test execution are independently checked.

- [ ] Merge and deployment remain separate team decisions.


## Sources

- S01: [AWS frontier agents](https://aws.amazon.com/ai/frontier-agents/)

- S02: [Kiro Web](https://kiro.dev/docs/web/)

- S03: [Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

- S04: [Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

- S05: [Creating tasks](https://kiro.dev/docs/web/using-the-agent/creating-tasks/)

- S06: [GitHub integration](https://kiro.dev/docs/web/github/)

- S07: [GitLab integration](https://kiro.dev/docs/web/gitlab/)

- S08: [Specifications](https://kiro.dev/docs/specs/)

- S09: [Built-in tools](https://kiro.dev/docs/tools/)

- S10: [Cloud sandbox](https://kiro.dev/docs/web/sandbox/)

- S11: [Automations](https://kiro.dev/docs/web/automations/)

- S12: [Cloud sessions](https://kiro.dev/docs/cloud-sessions/)

- S13: [Steering](https://kiro.dev/docs/steering/)

- S14: [Memory](https://kiro.dev/docs/memory/)

- S15: [Model Context Protocol](https://kiro.dev/docs/mcp/)

- S16: [Powers](https://kiro.dev/docs/powers/)

- S17: [Hooks](https://kiro.dev/docs/hooks/)

- S18: [Permissions](https://kiro.dev/docs/permissions/)

- S19: [Sandbox internet access](https://kiro.dev/docs/web/sandbox/internet-access/)

- S20: [Environment variables and secrets](https://kiro.dev/docs/web/sandbox/environment-variables/)

- S21: [Checkpoints and rewind](https://kiro.dev/docs/checkpoints/)

- S22: [Custom agents](https://kiro.dev/docs/custom-agents/)

- S23: [Agent Skills](https://kiro.dev/docs/skills/)

- S24: [Workflows](https://kiro.dev/docs/workflows/)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.


## Mechanisms and enablement extension

See the [detailed source-linked setup and verification guide](../mechanisms/kiro.md). It contains 8 records, a proposed six-step exercise and lifecycle controls. Existing presentation timing is unchanged.
