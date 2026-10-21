# Kiro — mechanisms and enablement

Reviewed 21 October 2026. Independent checks and examples are proposed; no live workflow was executed.

## Mechanism model

Separate facts discovered during coding from rules the team intentionally maintains. Local memory can retain a debugging lesson; steering expresses maintained conventions; skills provide procedures; hooks and MCP enable actions. No one control replaces the others.

Local IDE/CLI memory retains selected context on the same machine. Web can incorporate the task creator’s review feedback. Neither statement establishes a shared memory store across local clients, cloud agents and teammates.

IDE, CLI and Web have different controls. Local memory requires supported versions; Web features retain their own availability and plan restrictions.

## K-M01 — Retain debugging context in local memory

**Surface:** IDE ≥1.4.0; CLI ≥2.29.0 in local V3 sessions

**Availability:** Documented 20 October 2026 release; off by default

**Activation:** User opt-in

### Documented mechanism

Kiro can extract and refine selected context, then retrieve it for later tasks. Local memories are shared by IDE and CLI on the same machine and can be repository-scoped or global; they are not full conversation copies.

### Enable and configure

A supported client version and a trusted local workspace for memory changes.

1. IDE: open Memories in the activity bar, then settings, and choose Use and learn.

2. CLI: open /memories → config, select read & write and enable automatic memory updates when desired.

3. Start a new CLI session after changing access. Use /memories → list to inspect entries.

### Scope and persistence

Local storage is not documented as automatic synchronization to Kiro Web or other team members.

### Independent checks — proposed

- Record a harmless repository-specific prerequisite, then inspect the saved entry and its scope.

- In a new session, ask for the relevant test plan and look for an explicit Memory read in the transcript.

- Correct the fact and test again; check that an unrelated repository does not inherit repository-only advice.

### Record to retain — proposed

Client versions, memory mode, repository scope, entry before/after correction and recall evidence.

### Stop, correct or remove

IDE supports inspection and deletion; CLI supports read only/off modes and chat-based corrections when writable. Access changes apply to a new CLI session.

### Limits and fallback

Recalled text consumes context. Capture and recall do not guarantee correctness or update model weights as a user-controlled operation.

Keep the approved fact in version-controlled steering when automatic retention is absent or unsuitable; do not enable broad access merely to obtain recall.

### Illustrative task — not executed

Illustrative: “Remember for this training repository that integration tests require the local test fixture. This is a test convention, not a credential.”

### Official guidance

[KL: Introducing memory in Kiro IDE and CLI — 20 October 2026](https://kiro.dev/blog/memory-in-ide-cli/)

[KM: Memory](https://kiro.dev/docs/memory/)

## K-M02 — Use the task creator’s Web review feedback

**Surface:** Kiro Web / repository pull requests

**Availability:** Web feature; separate from local memory

**Activation:** Connected repository and task feedback

### Documented mechanism

Kiro Web responds to review feedback and can carry the task creator’s guidance into future work. The steering guide limits this learning to the user who created the task, not other reviewers.

### Enable and configure

A connected repository and a Web task created by the reviewing user.

1. Connect GitHub in Web settings and grant only required repositories.

2. Create a bounded task and review its proposed change.

3. Add a specific review correction from the task creator’s account; inspect the resulting revision and later behavior.

### Scope and persistence

This is a Web feedback mechanism. The reviewed guides do not establish shared storage with local IDE/CLI memory.

### Independent checks — proposed

- Use a small formatting or error-handling correction in a disposable repository.

- Compare the changed PR and a later task; label a behavioral match as observation, not proof of an undocumented storage implementation.

### Record to retain — proposed

Task creator, PR/comment link, revision diff and later task result.

### Stop, correct or remove

Use checked-in steering for rules requiring explicit team ownership and version control. A dedicated Web memory-delete control is not established by these pages.

### Limits and fallback

Commenting does not authorize merging or deployment. Avoid treating every reviewer’s comment as persistent policy.

Put the reviewed rule in repository steering and provide it explicitly; record the uncertainty about implicit feedback retention.

### Illustrative task — not executed

Illustrative: “Use the existing request-ID propagation helper instead of creating a new helper.”

### Official guidance

[KS: Steering](https://kiro.dev/docs/steering/)

[KW: Working with the agent on Web](https://kiro.dev/docs/web/using-the-agent/)

[KG: GitHub integration](https://kiro.dev/docs/web/github/)

## K-M03 — Maintain explicit project guidance in steering

**Surface:** IDE / CLI / Web, with surface-specific scope

**Availability:** Documented; custom-agent inclusion must be configured

**Activation:** Version-controlled Markdown

### Documented mechanism

Workspace steering lives in .kiro/steering; local global steering lives in ~/.kiro/steering. Inclusion modes control when guidance is loaded. The cloud cannot read the local global directory.

### Enable and configure

Repository access and an approved guidance file; correct client-specific configuration.

1. Create a Markdown steering file with a clear applicability statement.

2. Choose the documented inclusion mode for the client; use workspace scope for repository-owned conventions.

3. For a custom agent, explicitly include steering in its resources configuration. Upload local global guidance through Configuration Sync when it is required in cloud sessions.

### Scope and persistence

Workspace guidance takes priority over conflicting local-global guidance. Steering is explicitly maintained text, unlike inferred memory.

### Independent checks — proposed

- Check a matching and a nonmatching task for a conditional instruction.

- Inspect the custom-agent resources rather than assuming default-agent behavior carries over.

### Record to retain — proposed

Guidance file revision, inclusion mode, client/surface and test transcript.

### Stop, correct or remove

Edit or remove the file through normal review; verify the new context in a fresh session.

### Limits and fallback

Steering content is not a sandbox, access-control policy or substitute for tests.

Attach the approved guidance explicitly while correcting inclusion or sync settings.

### Illustrative task — not executed

Illustrative: “When changing request-ID handling, preserve the public header contract and add a regression test.”

### Official guidance

[KS: Steering](https://kiro.dev/docs/steering/)

[KR: Custom-agent configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/)

## K-M04 — Load a reusable procedure through Agent Skills

**Surface:** IDE / CLI / Web

**Availability:** Documented; global directories are local-only

**Activation:** Task-relevant skill activation

### Documented mechanism

Kiro first discovers a skill’s name and description, then loads instructions when relevant; scripts and references can be loaded as needed. This is procedure selection, not learned incident memory.

### Enable and configure

A reviewed skill package and appropriate permissions for any actions it describes.

1. Place a SKILL.md package in .kiro/skills/<name>/ with name and description frontmatter.

2. Keep supporting references in the package and describe the tasks that should activate it.

3. For global local use, use ~/.kiro/skills; verify cloud availability separately.

### Scope and persistence

Package contents can include executable material. Read the package before enabling it.

### Independent checks — proposed

- Choose a read-only procedure and inspect the loaded skill when the task matches.

- Verify any command uses the intended working directory and least required permissions.

### Record to retain — proposed

Skill package revision, activation evidence, command log and reviewed result.

### Stop, correct or remove

Remove or revise the package through the repository’s change process.

### Limits and fallback

Skill activation does not validate its content or authorize every script it references.

Use the reviewed steps manually when activation is uncertain; do not accept a successful-looking narrative without command results.

### Illustrative task — not executed

Illustrative skill: inspect existing request-ID entry points and report missing propagation tests without changing code.

### Official guidance

[KK: Agent Skills](https://kiro.dev/docs/skills/)

## K-M05 — Run event-driven hooks with an explicit effect

**Surface:** IDE / CLI; not Web or Mobile

**Availability:** Documented v1 standalone hooks

**Activation:** Event + matcher + command or prompt

### Documented mechanism

Kiro hooks run a shell command or inject an agent prompt when a configured event occurs. Standalone v1 JSON files allow the same event definition to be used by local IDE and CLI clients.

### Enable and configure

An applicable local client, repository tooling and a reviewed command or prompt.

1. Create .kiro/hooks/<name>.json using version v1 and the documented hooks array.

2. Select a supported trigger and matcher; start with a non-mutating validation command.

3. Migrate older formats using the client’s documented migration flow, then inspect the resulting configuration.

### Scope and persistence

An agent-prompt action and a blocking command hook are not equivalent. File patterns and event semantics are client-specific.

### Independent checks — proposed

- In a disposable repository, trigger one matching file event and one unrelated event.

- Check the actual command exit result and side effects; guard against repeated-trigger loops.

### Record to retain — proposed

Hook JSON revision, matching event, command output, exit status and changed-file list.

### Stop, correct or remove

Remove or revise the hook file and confirm it is no longer loaded; avoid broad event matchers.

### Limits and fallback

A hook can run code automatically. Do not use unreviewed scripts or commands downloaded at invocation time.

Disable the hook and run the validation command manually until trigger behavior is understood.

### Illustrative task — not executed

Illustrative task: run an already-installed test check after a relevant local file event; do not install dependencies as part of the hook.

### Official guidance

[KH: Hooks](https://kiro.dev/docs/hooks/)

[KJ: Hooks migration in CLI V3](https://kiro.dev/docs/cli/v3/hooks-migration/)

## K-M06 — Expose tools through MCP with controlled approval

**Surface:** Local IDE / CLI configuration; cloud setup differs

**Availability:** Documented MCP configuration

**Activation:** Explicit server and tool configuration

### Documented mechanism

MCP adds tool interfaces from a local process or remote server. Configuration and tool approval are separate from the text that tells the agent how to use a tool.

### Enable and configure

A reviewed MCP server, suitable authentication and the installed client’s supported transport.

1. Use .kiro/settings/mcp.json for workspace configuration or the user-level equivalent.

2. Configure the server endpoint/process without hard-coded credentials; leave autoApprove empty for initial evaluation.

3. Save, inspect available tools, and approve or deny the requested operation after reviewing its arguments.

### Scope and persistence

Workspace configuration can override user configuration. Local filesystem configuration does not imply that a cloud session has the same credentials.

### Independent checks — proposed

- Choose one read-only tool, record its input and compare its output with the source system.

- Deny a write request and verify the external system did not change.

### Record to retain — proposed

Redacted config, server identity, exposed tool list, approval decision and external result.

### Stop, correct or remove

Use disabled or disabledTools to remove exposure; review any autoApprove changes as a permission decision.

### Limits and fallback

Connecting a server is not proof that its data is trustworthy. Do not auto-approve all tools to fix a failed read.

Disable the server; obtain the evidence through an approved read-only path.

### Illustrative task — not executed

Illustrative: “Retrieve the documented configuration of this test resource. Do not perform any write operation.”

### Official guidance

[KC: MCP configuration](https://kiro.dev/docs/mcp/configuration/)

[KP: MCP tool approval](https://kiro.dev/docs/mcp/usage/)

## K-M07 — Run a repository task on a Web schedule

**Surface:** Kiro Web Automations

**Availability:** Eligible paid plans; Web availability applies

**Activation:** User-enabled recurring automation

### Documented mechanism

A Web automation runs a prompt against selected repositories in autonomous mode on a schedule. When changes are produced, the review artifact can be a pull request.

### Enable and configure

An eligible plan, connected repositories and a prompt with bounded output.

1. Open Automations in the Web sidebar and create the automation.

2. Specify its name, prompt, repositories and schedule; review the configuration.

3. Inspect a run and its output; use the row status or Edit screen to disable future runs.

### Scope and persistence

Scheduling is a Web mechanism, separate from local hooks and local memory.

### Independent checks — proposed

- Start with a report-only task in a test repository.

- Confirm repository selection, schedule interpretation and resulting session.

- Check that a disabled automation does not start a subsequent scheduled run.

### Record to retain — proposed

Automation definition, run/session link, output or PR and responsible reviewer.

### Stop, correct or remove

Disable or delete the automation to stop future scheduled runs.

### Limits and fallback

A scheduled task is not permission to merge or deploy. Completion time depends on the work; inspect failures rather than inferring success from a schedule.

Perform the same task manually while resolving plan access or execution failures.

### Illustrative task — not executed

Illustrative: “Summarize merged request-ID changes in the last review window. Do not edit repository files.”

### Official guidance

[KA: Automations](https://kiro.dev/docs/web/automations/)

## K-M08 — Separate reference retrieval from session compaction

**Surface:** CLI knowledge bases / supported session commands

**Availability:** Documented; verify current profile schema

**Activation:** Explicit indexed sources; automatic or manual summary

### Documented mechanism

A configured CLI knowledge base indexes selected reference material for retrieval. Compaction instead summarizes older conversation content within an existing task; it is not proof that durable memory was saved.

### Enable and configure

A current custom-agent profile and approved local documents for a knowledge base.

1. Configure a knowledgeBase resource using the documented source, name and indexing options.

2. Use autoUpdate only when re-indexing on agent start is intended.

3. Use /compact to summarize a long conversation; preserve critical evidence outside the conversation.

### Scope and persistence

Indexed files, current-session summaries and cross-session memories have different sources and lifecycles.

### Independent checks — proposed

- Change one non-sensitive reference fact, refresh the index and ask for its source.

- After compaction, verify the current goal and next action still match the approved task.

### Record to retain — proposed

Source revision, profile configuration, retrieval citation and before/after task-state checklist.

### Stop, correct or remove

Remove the knowledge-base resource to stop offering that index. Correct source files and rebuild rather than editing a summary as if it were source truth.

### Limits and fallback

A summary may omit details. Do not use it as the only retained incident record or infer full-text retention.

Reattach the authoritative document and restate the active task if retrieval or compaction loses essential context.

### Illustrative task — not executed

Illustrative: “Find the request-ID contract in the indexed project documents and identify the file revision. Do not substitute an older conversation summary.”

### Official guidance

[KR: Custom-agent configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/)

[KQ: CLI slash commands](https://kiro.dev/docs/cli/reference/slash-commands/)

[KM: Memory](https://kiro.dev/docs/memory/)

## Proposed use-case exercise

Verify opt-in memory on a local development client

Optional 10-minute walkthrough; additional to the core programme. Not an agent-runtime guarantee.

Use a disposable repository, supported IDE/CLI versions and a harmless preference. Avoid secrets, personal data and production tools.

### 1. Verify client and state · 00:00–01:30

**Role:** Developer · **Mechanism:** K-M01

Check supported version and whether memory is off, read-only or read/write.

**Gate:** Actual client version and state recorded.

### 2. Enable intentionally · 01:30–03:00

**Role:** Developer · **Mechanism:** K-M01

Select Use and learn in the IDE or set the CLI memory read/write configuration.

**Gate:** The explicit opt-in is recorded.

### 3. Add a scoped fact · 03:00–04:30

**Role:** Developer · **Mechanism:** K-M01

Ask to retain a non-sensitive debugging lesson for this repository.

**Gate:** Inspectable memory entry with the correct scope.

### 4. Test a fresh session · 04:30–06:30

**Role:** Reviewer · **Mechanism:** K-M01

Ask a task that would need the fact without restating it.

**Gate:** Separate session and observable entry use where available.

### 5. Keep policy explicit · 06:30–08:30

**Role:** Repository owner · **Mechanism:** K-M03

Move mandatory team convention into reviewed steering rather than relying solely on inferred memory.

**Gate:** Version-controlled guidance with deliberate inclusion.

### 6. Correct and disable · 08:30–10:00

**Role:** Developer · **Mechanism:** K-M01

Edit/delete the test entry and disable or restrict future memory use.

**Gate:** New-session behavior agrees with the changed setting.

### Exit

Memory scope, inspectability and stop behavior are demonstrated. No claim is made about Web synchronization or teammates’ clients.

### Fallback

Use a prepared memory-settings walkthrough; retain the rule in checked-in steering until the installed client supports the feature.
