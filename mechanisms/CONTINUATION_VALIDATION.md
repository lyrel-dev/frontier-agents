# Mechanism documentation: continuation validation

Date: 21 October 2026. Revision: `2026-10-21-mechanisms-v2`.

## Result and scope

The earlier mechanism publication completed before the response was interrupted. Its GitHub Actions run, generated files and downloaded artifact were inspected before this follow-up. This revision corrects the published content and records the checks performed. It is a documentation and software-artifact validation, not an execution test against an AWS account.

The collection now contains 32 mechanism records: 10 for AWS DevOps Agent, eight for Kiro, seven for AWS Security Agent and seven for AWS FinOps Agent. The source register contains 46 official AWS or Kiro references. The retained original review covered 44 references; this continuation adds two references and rechecks selected critical memory, feedback, setup and lifecycle claims. It does not claim a new audit of every historical statement.

## Corrections

| Finding | Correction | Acceptance check |
|---|---|---|
| The extracted package linked to a `dist` ZIP that was not included inside that ZIP. | The index now links to the repository package, with a sign-in qualification. | The extracted report has no unresolved local package link. |
| DevOps incident memory coverage omitted corrective-feedback reflections. | Added D-M10, the documented feedback procedure, reflection inspection, independent verification and a separate optional AWS-sharing decision. | The record appears in the report, Markdown, notes and reference deck; the exercise points to D-M10. |
| The default state of monitor memory was not explicit. | D-M01 now distinguishes the documented enabled-by-default monitor store from inspection of store and entry state. | The dated official change record supports the default; custom-agent memory attachment remains a separate requirement. |
| A long reference path overflowed the mechanism index on a narrow display. | Added wrapping for long uninterrupted text. | Desktop and 390-pixel-wide browser checks report no horizontal page overflow. |

## Selected official-source rechecks

| Mechanism | Official reference | Qualified conclusion |
|---|---|---|
| Managed memory and relevance-based retrieval | [DevOps Agent memories](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) | Stores and memory descriptions support selective retrieval of retained context. Recurring-cause memory and corrective-feedback reflections are separate mechanisms. |
| Corrective feedback | [Provide feedback on investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html#provide-feedback-on-investigations) | Use Add feedback on a completed investigation, or provide feedback through Chat. Supply the actual cause when the diagnosis is incorrect. The latest feedback replaces prior feedback for the investigation. Sharing with AWS requires explicit confirmation. |
| Default and lifecycle changes | [DevOps Agent product changes](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) | The dated changes distinguish monitor memory enabled by default, changes to learned-knowledge storage and the addition of reflections. |
| Custom-agent memory attachment | [Custom agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) | A new custom agent does not implicitly receive every memory store. Attach the required stores and preserve their access boundaries. |
| Kiro local memory controls | [Memory](https://kiro.dev/docs/memory/) and [IDE/CLI memory launch](https://kiro.dev/blog/memory-in-ide-cli/) | Memory, Steering, session history and compaction are different forms of context. Local CLI access changes take effect in a new session; automatic-update changes take effect immediately. The launch guidance identifies supported versions and the opt-in default. |
| FinOps context and memory | [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html) and [Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html) | User-maintained context files differ from agent-maintained memory. Forgetting a memory does not establish deletion of conversation or task history. Preview lifecycle restrictions remain explicit. |
| Security finding revalidation | [Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) | Revalidation checks selected prior findings against the target after a deployed fix; it is not a general discovery run. Reviewed guidance did not establish a configurable incident-memory switch for this workflow. This is an evidence limitation, not a claim about undisclosed internal implementations. |

Some retrieved copies of the DevOps documentation were older than the dated product changes and more recent indexed documentation. The revision records this discrepancy instead of treating absence from an older copy as evidence that a documented feature does not exist. Operators should confirm the deployed interface, feature state and relevant documentation before implementation.

## Validation performed

| Check | Observed result | Boundary |
|---|---|---|
| Original publication integrity | Downloaded artifact matched the workflow SHA-256 digest; its nested ZIP matched repository Git blob `93f39d8621a76f632f9a9c87288f5740bf4bb67e`. All 117 original manifest entries matched. | Establishes identity of the starting package, not content accuracy. |
| Structural validation | 14 active HTML files and 2,104 local links/anchors checked; no recorded errors. Source identifiers, required record fields and five core presentation schedules passed. | External pages and live product operation are separate checks. |
| Browser validation | Four mechanism guides, the index and comparison overview checked at 1440 and 390 pixels; no recorded page errors or horizontal overflow. | Self-contained HTML was loaded through Playwright `set_content`; local navigation was checked separately. |
| Interactive controls | Search, family filtering, disclosures, guided steps, presentation navigation, keyboard behavior, exports and print-state restoration passed. | Controls were exercised where present; index and overview pages were layout checks. |
| Integration links | 329 mechanism-companion local links checked; inline mechanism sections inspected in the five main reports. | Link existence does not validate an external product claim. |
| PowerPoint structure | Ten decks, 232 slides: no out-of-bounds shapes or empty speaker notes. | Shape bounds are not a full text-overflow or pixel-level review. |
| Rendered inspection | All 14 DevOps mechanism-reference slides rendered; the new feedback slide and updated exercise page inspected directly. | Other decks received structural checks, not a new pixel-by-pixel review. |
| Editorial validation | No recorded editorial-lint errors; 83 capability/pattern reference records retained. | Automated lint does not replace substantive editorial judgment. |

Machine-readable results are in `qa/mechanism-browser-validation.json`, `qa/mechanism-render-validation.json`, `qa/build-validation.json` and the retained editorial validation records.

## Timing and execution boundaries

The original core programme remains 160 minutes, including 48 minutes of demonstrations. Mechanism reference slides are untimed. Four separately selectable prepared-result exercises total 44 additional minutes: DevOps 12, Kiro 10, Security 12 and FinOps 10. These are delivery budgets, not agent-completion guarantees.

No AWS workflow, incident investigation, memory recall, penetration test, account configuration or cost optimization was executed. There are no measured productivity, diagnostic, security-detection or savings results. Matching an earlier answer is not accepted as proof that memory was retrieved: inspect observable memory reads where available and label recall unverified otherwise.

## Publication acceptance

Rebuild through the repository workflow after this record and the updated test records are committed. Preserve one generated document per commit and leave repository visibility unchanged. Verify the completed run, retrieve its output, compare the published ZIP and manifest, and rerun structural checks on a fresh extraction. Any later publication receipt should identify its actual workflow run and checksums rather than infer success from file creation alone.
