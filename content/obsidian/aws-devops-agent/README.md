---
id: obsidian-devops-readme
kind: obsidian-note
product: devops
title: AWS DevOps Agent Obsidian dossier
type: index
tags:
  - aws/devops-agent
  - documentation
  - obsidian
created: '2026-11-03'
updated: '2026-11-05'
source_cutoff: '2026-10-31'
api_addendum_source_cutoff: '2026-11-05'
status: documentation-vetted
related:
  - '[[00_Start_Here]]'
---

<!-- block: obsidian-devops-readme-overview -->
# AWS DevOps Agent Obsidian dossier

The original 21 Markdown notes introduce agents and their mechanisms, map DevOps responsibilities to AWS capabilities, explain orchestration and operational cases, and extend an illustrative established system with custom agents. Four additional notes analyze the official AWS API and define an investigation data model and live/history UI contract.

The original framework and presentation preserve their **31 October 2026 source cutoff**. The investigation API addendum was separately reviewed on **5 November 2026**, with pinned official SDK models and explicit public-contract gaps.

<!-- block: obsidian-devops-readme-navigation -->
## Reading and presentation routes

| Purpose | Entry point |
| --- | --- |
| Reading order and shorter briefing route | [Start here](00_Start_Here.md) |
| Complete conceptual narrative | [Framework](AWS_DevOps_Agent_Framework.md) |
| 44-slide Markdown presentation | [Presentation](AWS_DevOps_Agent_Presentation.md) |
| Explanations and presentation caveats | [Presenter notes](Presentation_Notes.md) |
| Reusable Mermaid figures | [Diagram atlas](Diagram_Atlas.md) |
| Agent mechanism taxonomy | [Mechanism catalogue](Mechanism_Catalog.md) |
| Documentation evidence | [Source index](Source_Index.md) |
| Review scope and known limits | [Validation and use](Validation_and_Use.md) |
| Investigation entity relationships and derived data | [Investigation data model](Investigation_Data_Model.md) |
| All 63 native API operations and selected field contracts | [Investigation API catalog](Investigation_API_Catalog.md) |
| Live synchronization, history and operator UI behavior | [Investigation UI contract](Investigation_UI_Contract.md) |
| API source pins, review scope and diagram verification | [Investigation API evidence](Investigation_API_Sources.md) |

<!-- block: obsidian-devops-readme-obsidian -->
## Open in Obsidian

Open this folder as a vault or copy its notes into an existing vault. Internal note links use Obsidian wikilinks; external references use ordinary Markdown links. To present, enable the core Slides plugin and start the presentation from `AWS_DevOps_Agent_Presentation.md`. Slide separators and Mermaid diagrams remain editable Markdown. GitHub readers can use the relative links above to navigate the entry points.

The complete route has 44 slides and 19 presentation diagrams. The original notes contain 35 distinct Mermaid graphs. The API addendum adds nine diagrams: seven ER diagrams, one sequence diagram and one flowchart. The start note includes a shorter 22-slide route. No additional visual asset files are required.

<!-- block: obsidian-devops-readme-repository -->
## Repository integration

These notes are authored sources under `content/`. Their `obsidian-note` kind and prefixed source IDs keep them distinct from the compiled guide sections, registered HTML slides and frozen catalog records. The existing compiler loads their source metadata without projecting them into the HTML guide or presentation routes. The API addendum proposes a future operator UI; it does not implement or change the independent application. The canonical README source links to this folder.

The three operational cases and three custom-agent extensions are explanatory customer designs, not additions to the repository's approved use-case register. The validation note distinguishes documentation and rendered-diagram review from live AWS testing.
