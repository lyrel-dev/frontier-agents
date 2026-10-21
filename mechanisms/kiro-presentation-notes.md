# Kiro — mechanism reference speaker notes

All reference slides are untimed. Optional exercises are additional to the core programme.

## K-M01 — Retain debugging context in local memory

Kiro can extract and refine selected context, then retrieve it for later tasks. Local memories are shared by IDE and CLI on the same machine and can be repository-scoped or global; they are not full conversation copies.

**Setup:** IDE: open Memories in the activity bar, then settings, and choose Use and learn. CLI: open /memories → config, select read & write and enable automatic memory updates when desired. Start a new CLI session after changing access. Use /memories → list to inspect entries.

**Proposed verification:** Record a harmless repository-specific prerequisite, then inspect the saved entry and its scope. In a new session, ask for the relevant test plan and look for an explicit Memory read in the transcript. Correct the fact and test again; check that an unrelated repository does not inherit repository-only advice.

**Boundary:** Recalled text consumes context. Capture and recall do not guarantee correctness or update model weights as a user-controlled operation.

## K-M02 — Use the task creator’s Web review feedback

Kiro Web responds to review feedback and can carry the task creator’s guidance into future work. The steering guide limits this learning to the user who created the task, not other reviewers.

**Setup:** Connect GitHub in Web settings and grant only required repositories. Create a bounded task and review its proposed change. Add a specific review correction from the task creator’s account; inspect the resulting revision and later behavior.

**Proposed verification:** Use a small formatting or error-handling correction in a disposable repository. Compare the changed PR and a later task; label a behavioral match as observation, not proof of an undocumented storage implementation.

**Boundary:** Commenting does not authorize merging or deployment. Avoid treating every reviewer’s comment as persistent policy.

## K-M03 — Maintain explicit project guidance in steering

Workspace steering lives in .kiro/steering; local global steering lives in ~/.kiro/steering. Inclusion modes control when guidance is loaded. The cloud cannot read the local global directory.

**Setup:** Create a Markdown steering file with a clear applicability statement. Choose the documented inclusion mode for the client; use workspace scope for repository-owned conventions. For a custom agent, explicitly include steering in its resources configuration. Upload local global guidance through Configuration Sync when it is required in cloud sessions.

**Proposed verification:** Check a matching and a nonmatching task for a conditional instruction. Inspect the custom-agent resources rather than assuming default-agent behavior carries over.

**Boundary:** Steering content is not a sandbox, access-control policy or substitute for tests.

## K-M04 — Load a reusable procedure through Agent Skills

Kiro first discovers a skill’s name and description, then loads instructions when relevant; scripts and references can be loaded as needed. This is procedure selection, not learned incident memory.

**Setup:** Place a SKILL.md package in .kiro/skills/<name>/ with name and description frontmatter. Keep supporting references in the package and describe the tasks that should activate it. For global local use, use ~/.kiro/skills; verify cloud availability separately.

**Proposed verification:** Choose a read-only procedure and inspect the loaded skill when the task matches. Verify any command uses the intended working directory and least required permissions.

**Boundary:** Skill activation does not validate its content or authorize every script it references.

## K-M05 — Run event-driven hooks with an explicit effect

Kiro hooks run a shell command or inject an agent prompt when a configured event occurs. Standalone v1 JSON files allow the same event definition to be used by local IDE and CLI clients.

**Setup:** Create .kiro/hooks/<name>.json using version v1 and the documented hooks array. Select a supported trigger and matcher; start with a non-mutating validation command. Migrate older formats using the client’s documented migration flow, then inspect the resulting configuration.

**Proposed verification:** In a disposable repository, trigger one matching file event and one unrelated event. Check the actual command exit result and side effects; guard against repeated-trigger loops.

**Boundary:** A hook can run code automatically. Do not use unreviewed scripts or commands downloaded at invocation time.

## K-M06 — Expose tools through MCP with controlled approval

MCP adds tool interfaces from a local process or remote server. Configuration and tool approval are separate from the text that tells the agent how to use a tool.

**Setup:** Use .kiro/settings/mcp.json for workspace configuration or the user-level equivalent. Configure the server endpoint/process without hard-coded credentials; leave autoApprove empty for initial evaluation. Save, inspect available tools, and approve or deny the requested operation after reviewing its arguments.

**Proposed verification:** Choose one read-only tool, record its input and compare its output with the source system. Deny a write request and verify the external system did not change.

**Boundary:** Connecting a server is not proof that its data is trustworthy. Do not auto-approve all tools to fix a failed read.

## K-M07 — Run a repository task on a Web schedule

A Web automation runs a prompt against selected repositories in autonomous mode on a schedule. When changes are produced, the review artifact can be a pull request.

**Setup:** Open Automations in the Web sidebar and create the automation. Specify its name, prompt, repositories and schedule; review the configuration. Inspect a run and its output; use the row status or Edit screen to disable future runs.

**Proposed verification:** Start with a report-only task in a test repository. Confirm repository selection, schedule interpretation and resulting session. Check that a disabled automation does not start a subsequent scheduled run.

**Boundary:** A scheduled task is not permission to merge or deploy. Completion time depends on the work; inspect failures rather than inferring success from a schedule.

## K-M08 — Separate reference retrieval from session compaction

A configured CLI knowledge base indexes selected reference material for retrieval. Compaction instead summarizes older conversation content within an existing task; it is not proof that durable memory was saved.

**Setup:** Configure a knowledgeBase resource using the documented source, name and indexing options. Use autoUpdate only when re-indexing on agent start is intended. Use /compact to summarize a long conversation; preserve critical evidence outside the conversation.

**Proposed verification:** Change one non-sensitive reference fact, refresh the index and ask for its source. After compaction, verify the current goal and next action still match the approved task.

**Boundary:** A summary may omit details. Do not use it as the only retained incident record or infer full-text retention.

## Optional use-case exercise



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

