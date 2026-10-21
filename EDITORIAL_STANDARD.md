# Frontier agents — editorial and information-design standard

**Revision:** 21 October 2026  
**Scope:** AWS DevOps Agent, AWS Security Agent, AWS FinOps Agent, and their proposed common architecture patterns.  
**Purpose:** Provide an auditable engineering reference and a presentation that can be delivered without marketing claims, unverified product promises, or ambiguity about who authorizes an action.

## 1. Editorial rules

Use **observable behaviors** rather than adjectives. Write a short, testable statement in the form **actor + operation + bounded object + observable result**. Name the product or acting team. Do not substitute “the agent automates DevOps” for “a configured DevOps Agent investigation correlates the connected data sources and returns an incident analysis.”

Every externally verifiable product claim needs a link to an official AWS product source and, where relevant, a feature-level availability label. A hypothetical workflow, process gate, prompt, output to retain, metric, or team role is explicitly marked **proposed**. A link documents product functionality; it does not establish that a proposed sequence was run or that an outcome was measured.

Use consistent classifications:

| Label | Meaning | Valid evidence |
| --- | --- | --- |
| **Documented product behavior** | Described directly in official documentation for the relevant client, Region, and feature. | Product documentation and feature-specific release notes. |
| **Configured capability** | Documented operation that depends on a named integration, permission, trigger or option. | Product documentation plus the prerequisites shown. |
| **Composed team workflow** | Proposed sequence assembled from one or more documented mechanisms. | Product references for individual mechanisms; team sequence labeled as proposed. |
| **Preview** | Feature/service documentation identifies non-GA availability or limitations. | Current official availability notice; do not generalize service-level GA. |
| **Proposed architecture pattern** | Operating policy or cross-agent design synthesized for this report, **not** a shared AWS control plane. | Explicitly labeled recommendation, plus evidence for individual product analogues. |

Do not infer availability across surfaces (local IDE, CLI, Web, cloud session, repository integration) or across Regions. Do not equate a textual recommendation with execution approval, a code proposal with merge approval, a severity rating with exploitability, or a projected saving with realized saving.

## 2. Capability record — HTML report

One capability is one expandable record. **The same ordered fields appear for every capability:**

| Order | Field | Content rule | Display priority |
| --- | --- | --- | --- |
| 1 | Identity and status | Stable ID, exact product/surface, maturity, delivery type, and preview indicator where applicable. | Visible in collapsed row. |
| 2 | Documented function | One direct statement about what the named component does. Avoid benefits without measurements. | Visible in collapsed row. |
| 3 | Invocation and scope | Trigger/required connection, permissions, target and configuration. Say if user input is needed. | Expanded detail. |
| 4 | Review record to retain | **Proposed** evidence artifact the team should preserve; do not imply the product emits it natively. | Expanded detail. |
| 5 | Independent acceptance | Reproduction, review, test, or cost reconciliation that can refute the result. | Expanded detail. |
| 6 | Known limits and effects | Product/client/Region limits; data-access gaps; write effects; approval and target safety. | Expanded detail, adjacent to acceptance. |
| 7 | Working example | Short illustrative prompt/task, clearly labeled **not executed**. | Optional. |
| 8 | Official evidence | Source IDs link to the official-documentation register and can be followed to the original page. | Footer of record. |

**Do not** add implied productivity uplift, quality scores, run durations, automatic merges, broad write capabilities, or supported integrations without explicit evidence. Keep the factual function separate from acceptance advice.

### Sample capability record

**C01 · Incident triage and root-cause investigation**  
**Product:** AWS DevOps Agent · **Availability:** GA production operations · **Delivery:** Connected data required

- **Documented function:** Correlates accessible telemetry, topology, code and deployment information in an investigation.
- **Invocation/scope:** Connect one service’s relevant data sources and authorize only the required reads. Include an incident window and deployed revision.
- **Review record to retain (team recommendation):** Timestamped incident timeline with source references and competing hypotheses.
- **Independent acceptance:** Compare timestamps, resource IDs and the deployed change with the underlying telemetry.
- **Known limits:** Missing sources or permissions limit coverage. A root-cause proposal is not proof.
- **Official evidence:** Source references in the report, linked to AWS documentation.

## 3. Use-case record — HTML report

A use case is a **bounded workflow**, not a promotional success story. Present exactly these elements in order:

1. **Problem/trigger:** observable signal or request, with time/environment where appropriate.
2. **Scope and exclusions:** repository, branch, workload, accounts, Regions, target, allowed effects, and what the workflow will not do.
3. **Target artifact and completion decision:** what a reviewer receives and what constitutes evidence of completion.
4. **Execution sequence:** an ordered set of steps. Each step displays a **proposed responsible role**, **input**, **action narrative**, **reviewable artifact**, **acceptance gate**, **fallback**, and linked documented mechanisms.
5. **Demo contract:** preflight, fixed time budget, what is shown live, observable success/failure, and prepared evidence fallback.
6. **Residual risk:** untested inputs, source gaps, preview restrictions, unreconciled assumptions, and owner action.

Use actual product surface names and show whether a step is native functionality, configured access, or a composed workflow. Cross-product flows require a **human/system boundary and explicit authorization at each side**. Do not imply a common AWS orchestrator.

## 4. Presentation slide taxonomy

Maintain a **timed core presentation** and an **untimed capability appendix**. The appendix must never silently extend the advertised duration. The core answers an engineering decision; the appendix supplies exhaustive reference detail.

| Slide format | Best use | Maximum visible material | What the presenter must demonstrate |
| --- | --- | --- | --- |
| **Scenario contract** | Introduce a use case and its boundaries. | Trigger, scope, output, exclusions, done test. | Clarify what is not authorized and who reviews. |
| **Capability overview** | Compare 3–6 related documented functions. | One functional sentence per cell, with maturity and boundary. | Explain selection criteria, not product superiority. |
| **Input → operation → evidence** | Explain one central capability, integration or lifecycle stage. | Three distinct columns; key limits are separate. | Identify source dependencies and review artifact. |
| **Sequence/decision flow** | Show engineering steps and responsibility changes. | 3–6 numbered steps or a compact matrix. | Identify approval before any external effect. |
| **Control/availability matrix** | Explain feature/client/Region limits or write permissions. | 3–6 rows, direct conditions and outcomes. | Identify “not available/not authorized” scenarios. |
| **Live demonstration** | Verify one observable behavior. | Prompt, preflight, timed steps, expected evidence, fallback. | Show source records and independent result checks. |
| **Capability reference appendix** | Provide one standard slide per capability or pattern. | Function, invocation, retained record, acceptance, limits, evidence. | Use only in discussion or as take-home reference. |

**Slide headline:** factual conclusion (e.g. “Release testing sends real application requests”), rather than “Unlock release confidence.”

**Slide hierarchy:** concise title; one-sentence claim; 2–4 blocks/tables; a lower footer with maturity, source IDs and timing. Move detailed prerequisites and citations to notes or the appendix rather than compressing body text below readable size. Keep a source register; citations must identify the product-specific claim they support. Presenter notes supply the mechanism, exception and demo instructions rather than re-reading the slide.

## 5. Demo evidence and timing

Every demonstration has a single observable result and a **fixed walkthrough allocation**, not an implied agent completion SLA. Use this record:

| Field | Required value |
| --- | --- |
| Scenario | Named task and environment; real/synthetic explicitly identified. |
| Authorization | Owner, affected targets, write effects and stop procedure. |
| Preflight | Data, source revision, credentials boundary, fallback capture. |
| Runbook | Timed operator steps that total exactly the demo allocation. |
| Expected evidence | Inspectable record with its source and version. |
| Failure condition | What prevents accepting the demonstration as proof. |
| Fallback | Pre-captured or schematic walkthrough clearly labeled not live. |
| Measurement | Only actual measured observations; otherwise state “not measured.” |

The existing session budgets are retained: DevOps **35m / 12m demo**; Security **30m / 8m**; FinOps **27m / 7m**; architecture **36m / 8m**. Total **128m / 35m demo**, excluding questions and breaks.

## 6. Wording policy

Use: **supports**, **can**, **when configured**, **requires**, **returns**, **proposes**, **reports**, **records**, **reviewed**, **verified**, **documented**, **depends on**, **preview**. Qualify the claim by product, permission and feature surface.

Avoid in authored descriptions: *revolutionary, transformative, game-changing, seamless, effortless, powerful, cutting-edge, next-generation, magical, fully autonomous, guaranteed, eliminate incidents, secure by default, best-in-class, dramatically faster, zero-touch*. Do not replace one promotional adjective with another. “Automatic” is acceptable only for a documented automatic trigger and with the exact trigger semantics identified.

Prefer the following rewrites:

| Avoid | Use |
| --- | --- |
| “The agent fixes incidents.” | “The agent can investigate and recommend mitigation; an operator reviews and authorizes changes under the documented controls.” |
| “AI performs security assurance end-to-end.” | “A scoped assessment returns findings; the owner must review, remediate and independently revalidate.” |
| “Eliminate development toil.” | “Delegate a defined code change, review the diff and run tests.” |
| “Optimize cloud spending automatically.” | “Inspect recommendations, verify their constraints and track approved changes against comparable cost data.” |
| “All agents share context and permissions.” | “A team can exchange evidence artifacts across products; authorizations and integration boundaries remain product-specific.” |

## 7. Quality gates

Before publication, check every capability and use case for these conditions:

- Product statement has a source reference or is labeled *proposed*.
- Feature maturity, client and Region restrictions are not generalized.
- Each action requiring a permission or approval identifies who/what enforces it.
- A reviewable output is specified, and a separate independent acceptance step exists.
- All presented demonstrations state **preflight, data effects, timing, success condition and fallback**.
- Core slides meet the advertised allocation; reference appendices are untimed.
- No metric is represented as realized without direct measurements.
- Titles, body text, captions, notes, README and HTML report follow the same neutral style.
- Print and mobile layouts remain legible; links and evidence anchors resolve.

**Evidence boundary:** This standard and its sample records are publication rules, not new AWS product claims. Existing official-documentation citations remain in the agent-specific reports. The updated HTML and PowerPoint are generated from the same versioned source data and maintain a common revision record.
