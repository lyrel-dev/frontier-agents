# Platform mechanisms and enablement

Documented configuration, not a claim about undisclosed internals. No live AWS test or measured improvement. Retained context does not establish customer-controlled model training.

## Comparison

### DevOps Agent

**Context:** Managed investigation/environment memory; attached custom stores

**Activation:** Managed learning plus explicit store controls

**Surface:** Knowledge → Memories; custom-agent attachments

**Verification:** Current investigation evidence; inspect versions

**Limit:** No customer model-training switch established

### Kiro

**Context:** Local memory; explicit steering; Web creator feedback

**Activation:** Local memory opt-in; instructions and tools separately configured

**Surface:** Memories panel or /memories; repository files; Web settings

**Verification:** Separate session, scoped entry and code/test evidence

**Limit:** No assumed local↔Web or team-memory synchronization

### Security Agent

**Context:** Selected application resources; explicit requirements; finding/revalidation records

**Activation:** Per-test inputs; per-pack and repository settings

**Surface:** Test setup; Security requirements; repository wizard

**Verification:** Safe reproduction; deployed revision; revalidation job

**Limit:** No cross-incident memory toggle identified in reviewed pages

### FinOps Agent

**Context:** Uploaded organization files; conversational memory; task history

**Activation:** Context upload; remember/update/forget; explicit automation

**Surface:** Context files; chat; Tasks and Automations

**Verification:** Current cost query and reconciliation; inspect destination effects

**Limit:** Remembered outcomes are not fresh cost evidence

## Proposed common controls

### Name the storage boundary

Record whether context is local-machine, repository, Agent Space, individual agent or task-specific. Never infer a portfolio-wide store.

[DM](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

[KM](https://kiro.dev/docs/memory/)

[SC](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[FP](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

### Separate content from authority

Instructions and memory affect what is considered. IAM, application credentials and tool approvals determine what can be accessed or changed.

[DA](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

[KP](https://kiro.dev/docs/mcp/usage/)

[SA](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

[FG](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

### Make activation observable

Record the selected feature, setting, attachment, client version and first new session or job used to test it.

[DC](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html)

[KM](https://kiro.dev/docs/memory/)

[SP](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

[FT](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

### Validate with independent evidence

Use retained context to form a hypothesis, not to prove it. Reconcile with current telemetry, tests, reproduced findings or billing queries.

[DM](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

[KW](https://kiro.dev/docs/web/using-the-agent/)

[SG](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

[FD](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

### Control correction and residual data

A disabled trigger, removed attachment, forgotten fact and deleted history are different outcomes. Test the documented control for the actual data category.

[DM](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

[KM](https://kiro.dev/docs/memory/)

[ST](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[FP](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

### Track documentation changes

Store official source, review date, surface and unresolved discrepancy. Treat a changed configuration path or migration as a reason to recheck before rollout.

[DL](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html)

[KL](https://kiro.dev/blog/memory-in-ide-cli/)

[SI](https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html)

[KC](https://kiro.dev/docs/mcp/configuration/)

## Evidence qualifications

Incident learning is used here only for the documented retention and reuse of knowledge. It is not a claim that tenant incidents fine-tune model weights. Service-improvement data use is a separate policy question.

DevOps learned-skills guidance is migrating to managed memory. Current and cached official pages differ; confirm the live UI and avoid relying on historical numeric refresh thresholds.

Kiro local memory is documented in the dated 20 October 2026 release. Older cached pages describing IDE support as forthcoming must not override that dated release.

The Security Agent IDE guide and current Kiro guide differ on manual MCP paths. This guide uses the supported Power installation and requires inspection of the actual client configuration.

Executable DevOps skills have a preview exception alongside older restrictive wording. Only document-only DevOps skills are prescribed here.

Feature-specific Region, plan, role and preview constraints must be checked in the linked guide before enabling a mechanism. This extension is not a new audit of every historical capability record.
