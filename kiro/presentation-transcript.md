# Kiro — presentation transcript

32 minutes including 13 minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.


## 01. Kiro

**00:00–00:45 · 00:45 allocated**

**Takeaway:** Turn a bounded engineering outcome into a reviewable change.

This presentation follows a request-ID propagation change in checkout-api and a small scheduled maintenance job. It separates Kiro Web’s cloud work from local IDE and CLI controls. Access depends on plan, administrator enablement and feature rollout; current documentation also labels Web as preview in some pages. Do not apply a blanket general-availability statement across every client. The merge decision stays with the team.

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)


## 02. Choose the interaction model by uncertainty

**00:45–01:45 · 01:00 allocated**

**Takeaway:** Collaboration, specs and autonomous work solve different coordination problems.

When the design is unclear, work interactively. When behavior needs to be agreed before implementation, use a spec. When the outcome is bounded and sufficiently clear, delegate it through autonomous mode. These are not mandatory sequential stages. The demonstration chooses spec-first planning deliberately; it does not imply that every autonomous task must begin with a user-authored spec.

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[K08 — Specifications](https://kiro.dev/docs/specs/)


## 03. Use case · request-ID propagation

**01:45–03:15 · 01:30 allocated**

**Takeaway:** A concrete contract constrains the change before the first edit.

The example asks for an inbound request ID to be preserved on outbound calls. The team must first define behavior when the inbound value is missing or invalid. That policy is not an agent decision to make silently. Limit the work to middleware and the HTTP client, preserve public APIs, and name the tests that will demonstrate success. This task contract is our recommended practice, built on documented repository and spec capabilities.

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[K08 — Specifications](https://kiro.dev/docs/specs/)


## 04. Specs make intended behavior inspectable

**03:15–04:30 · 01:15 allocated**

**Takeaway:** Acceptance: approve behavior and non-goals before accepting implementation work.

A feature spec captures requirements and acceptance criteria. A bugfix spec makes the defect and unaffected behavior explicit. The design connects requirements to existing components; the task list makes execution reviewable. Not every advanced spec capability exists on every client, so check the documented support matrix. Treat the three artifacts as editable engineering agreements rather than evidence that the code is already correct.

[K08 — Specifications](https://kiro.dev/docs/specs/)


## 05. Repository understanding and test generation

**04:30–05:30 · 01:00 allocated**

**Takeaway:** Acceptance: a test must challenge the requirement; generated test code alone is not a pass.

Ask Kiro to cite the files and symbols it inspected. Then compare the explanation with a known execution path. Test generation is useful when the tests would fail for the original defect, exercise an important boundary and execute successfully in the chosen environment. A browser check can strengthen UI verification, but it does not establish coverage of every user journey.

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[K09 — Built-in tools](https://kiro.dev/docs/tools/)

[K10 — Cloud sandbox](https://kiro.dev/docs/web/sandbox/)


## 06. Cloud sandbox: configure the execution boundary

**05:30–06:30 · 01:00 allocated**

**Takeaway:** Acceptance: sandbox isolation is not permission to call production systems.

The sandbox is where cloud work executes. Dependency access, network settings and injected credentials determine what it can reach. A test command can still call an external API when credentials and connectivity permit it. Keep production credentials out of a development demonstration and use disposable services. Secrets can be exposed through program output or requests, so review both code and environment configuration.

[K10 — Cloud sandbox](https://kiro.dev/docs/web/sandbox/)

[K19 — Sandbox internet access](https://kiro.dev/docs/web/sandbox/internet-access/)

[K20 — Environment variables and secrets](https://kiro.dev/docs/web/sandbox/environment-variables/)


## 07. GitHub, GitLab and cross-repository work

**06:30–07:30 · 01:00 allocated**

**Takeaway:** Repository access and review artifacts remain provider-specific.

Connect the required repositories rather than granting blanket organization access for convenience. GitHub task assignment can originate from an issue through the documented label or command. A cross-repository task can produce separate pull or merge requests; the team still coordinates compatibility and merge order. A request to change one service must not silently broaden into other repositories.

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)

[K07 — GitLab integration](https://kiro.dev/docs/web/gitlab/)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)


## 08. Demo 1 · request ID from task to PR

**07:30–15:30 · 08:00 allocated**

**Takeaway:** Specify and review request-ID propagation without changing the public API.

The eight-minute allocation is for explaining the workflow and reviewing evidence. It is not an implementation-duration claim. Show a completed run if a fresh task has not reached a useful stage. A passing check is meaningful only if it ran on the displayed commit and exercised the relevant behavior. Reject unsupported claims that tests passed if the output shows a missing dependency or an unexecuted command.

**Preflight:** Prepare a test repository, an approved spec and a completed PR; document whether evidence is live or replayed.

```text

Plan request-ID propagation in checkout-api. Preserve public APIs and unrelated behavior. First show requirements, design and tasks. Cite relevant files. After plan approval, implement the scoped change, run repository checks and open a PR; do not merge.

```

- 01:00 — **Agree the contract:** Confirm missing-ID behavior, scope and non-goals.

- 02:00 — **Review the spec:** Inspect requirements, affected components and the planned tests.

- 02:00 — **Inspect execution:** Start the task or open the prepared completed session.

- 01:30 — **Inspect test evidence:** Show a meaningful failure case and fresh check output.

- 01:30 — **Review the PR:** Trace changed files to requirements; keep merge manual.

**Success:** A focused diff with requirement-linked tests and an explicit human review decision.

**Fallback:** Use the prepared spec, diff and test output after 60 seconds without usable progress; inspect rather than imply live completion.

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[K08 — Specifications](https://kiro.dev/docs/specs/)

[K09 — Built-in tools](https://kiro.dev/docs/tools/)


## 09. Review feedback is a new work item

**15:30–16:45 · 01:15 allocated**

**Takeaway:** Acceptance: verify the latest revision, not the first green result.

Use code review to refine the task rather than as a formality after generation. A review comment should state the behavior or constraint that must change. When supplying CI failures, include the log and failing command rather than asking the agent to guess. The team verifies the latest diff and check state before merge. Do not assume that every CI provider or failure is automatically connected.

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)


## 10. Automations handle repeatable repository work

**16:45–17:45 · 01:00 allocated**

**Takeaway:** Acceptance: recurring work should reduce toil without creating uncontrolled PR noise.

Start with a narrow task: one dependency group, a changelog or documentation drift. Keep the update policy explicit, including whether major versions are excluded and which checks must pass. Review the first runs and disable the automation if outputs become noisy or misleading. Scheduling execution does not authorize automatic merging.

[K11 — Automations](https://kiro.dev/docs/web/automations/)


## 11. Demo 2 · bounded dependency maintenance

**17:45–22:45 · 05:00 allocated**

**Takeaway:** Configure one weekly repository task and review an example output.

This is a configuration and result-review demo, not a timed dependency-upgrade benchmark. The schedule should remain disabled until the team approves it. Use a prepared output to show the reviewer’s decision. A run with no appropriate update can be successful; the goal is useful maintenance, not a mandatory pull request every week.

**Preflight:** Use a non-production repository and prepare a completed sample run; do not wait for the next scheduled trigger.

```text

Each week, inspect only the approved development dependency group. Exclude major-version changes and unrelated files. Run the repository checks. Open a small PR when an update is justified; otherwise report no change. Do not merge.

```

- 00:45 — **Choose scope:** One repository, dependency group and accountable reviewer.

- 00:45 — **Write the prompt:** Show exclusions and required evidence.

- 01:00 — **Inspect the setup:** Review cadence, repository access and enabled state.

- 01:30 — **Review a prepared run:** Inspect changed files, check results and a no-change outcome.

- 01:00 — **Set the stop rule:** Explain how the owner disables noisy or failing automation.

**Success:** A limited, reviewable maintenance task with a named owner and a disabled-by-default rehearsal setup.

**Fallback:** Walk through the reviewed configuration and a labeled example PR; do not claim the schedule ran during the session.

[K11 — Automations](https://kiro.dev/docs/web/automations/)

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)


## 12. Steering and memory serve different purposes

**22:45–23:45 · 01:00 allocated**

**Takeaway:** Explicit team rules and learned context are useful—but neither is an authorization policy.

Put stable, explicit conventions in steering. Learned memory helps avoid rediscovering repository commands or earlier corrections, but it can become stale. Inspect and correct remembered information where the client supports it. When a remembered claim conflicts with current source code or policy, verify the present evidence. Neither mechanism substitutes for permissions or branch protections.

[K13 — Steering](https://kiro.dev/docs/steering/)

[K14 — Memory](https://kiro.dev/docs/memory/)


## 13. Extend capabilities deliberately

**23:45–24:45 · 01:00 allocated**

**Takeaway:** Choose the smallest reusable mechanism that fits the task.

An MCP integration connects tools. A Power packages task-oriented capabilities and guidance. A custom agent defines a reusable specialist configuration. A skill packages a procedure and its resources. These mechanisms can compose, but their existence does not imply universal client support or permission to access every service. Review tool provenance, credentials, network reach and the side effects before adding an extension.

[K15 — Model Context Protocol](https://kiro.dev/docs/mcp/)

[K16 — Powers](https://kiro.dev/docs/powers/)

[K22 — Custom agents](https://kiro.dev/docs/custom-agents/)

[K23 — Agent Skills](https://kiro.dev/docs/skills/)


## 14. Local hooks are not cloud automation controls

**24:45–25:45 · 01:00 allocated**

**Takeaway:** Use the capability matrix for the client actually running the work.

The dedicated hooks and permissions pages document IDE and CLI support and do not list Web support for those controls. Other pages discuss cloud configuration more broadly, so do not infer exact parity from the shared product name. Verify the feature in the client you deploy. Cloud network and secret settings remain a distinct set of controls. A prompt or steering file is not an enforced deny rule.

[K17 — Hooks](https://kiro.dev/docs/hooks/)

[K18 — Permissions](https://kiro.dev/docs/permissions/)

[K19 — Sandbox internet access](https://kiro.dev/docs/web/sandbox/internet-access/)


## 15. Workflows make multi-step delegation explicit

**25:45–27:15 · 01:30 allocated**

**Takeaway:** Acceptance: bound retries and verify account/client availability before relying on a workflow.

Workflows differ from autonomous mode. Autonomous mode lets the agent determine the process for a task; a workflow makes the multi-step structure explicit and reusable. It can separate implementation from a fresh-context review step. The feature is opt-in and may not be exposed to every account. More structure also consumes more usage, so use it for work that benefits from independent stages rather than every small edit.

[K24 — Workflows](https://kiro.dev/docs/workflows/)

[K22 — Custom agents](https://kiro.dev/docs/custom-agents/)


## 16. Resume work and recover with the correct mechanism

**27:15–28:30 · 01:15 allocated**

**Takeaway:** Session continuity, local rewind and Git recovery are not interchangeable.

Cloud-session continuity helps an engineer return to ongoing work from supported clients. Local checkpoint or rewind features have their own documented scope. Neither implies that an external system or deployed service is rolled back. Git remains the review and version-history mechanism for repository changes. For the first pilot, test recovery with an unimportant branch before relying on it during a real change.

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[K21 — Checkpoints and rewind](https://kiro.dev/docs/checkpoints/)

[K10 — Cloud sandbox](https://kiro.dev/docs/web/sandbox/)


## 17. IaC, CI diagnosis and runbooks are composed workflows

**28:30–30:00 · 01:30 allocated**

**Takeaway:** General coding tools help; specialist validation still determines correctness.

The supplied-log diagnosis and infrastructure examples are not separate native guarantees. Give the exact failing command, configuration, environment and relevant logs. Ask for a minimal proposed change, then rerun the same check. Generated runbook steps should be rehearsed with safe inputs by the service owner. Never treat a plausible explanation of Terraform, a build or an incident procedure as executed validation.

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[K09 — Built-in tools](https://kiro.dev/docs/tools/)

[K17 — Hooks](https://kiro.dev/docs/hooks/)


## 18. Pilot for accepted changes, not generated volume

**30:00–32:00 · 02:00 allocated**

**Takeaway:** Scale only when review effort, correctness and operational risk improve together.

Start with one repository and one reproducible change. Record review effort before the pilot, then compare similar work produced with Kiro. Track accepted changes, failed checks, reviewer corrections and scope drift; include tool and model consumption. Add recurring maintenance only after the interactive workflow is reliable. Every outcome must remain reviewable. The detailed capability crosswalk maps all 21 entries below to this presentation, including the local and cloud distinctions.

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[K11 — Automations](https://kiro.dev/docs/web/automations/)
