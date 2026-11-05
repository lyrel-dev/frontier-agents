---
id: aws-fis-revised-docs-readme
title: FIS analysis reading guide
type: index
service: aws-fis
status: reviewed
version: '1.0'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- index
aliases:
- FIS analysis reading guide
related:
- initial/README.md
- suggested/README.md
- ../README.md
- ../REVIEW.md
- ../VALIDATION.md
---

# FIS analysis reading guide

Read the **initial AWS FIS model first**, then the **suggested assessment workflow model**. The initial model preserves the native provider contract, while the suggested model defines an application-owned assessment program that can use FIS, queries and observations.

## 1. Initial: native AWS FIS

Start with the [initial model guide](initial/README.md), then the complete [Experiment and Action analysis](initial/report.md). The report retains all 14 sections, the complete Experiment and ExperimentAction field inventories, derived measures, mutation boundaries, five entity relationship diagrams and the [53-source official AWS register](initial/sources.md).

Open the [preserved FIS interface](../initial/index.html) to inspect synthetic live and completed experiments. The [initial diagram index](../diagrams/initial/README.md) supplies an Obsidian note, editable Mermaid and portable SVG for each view.

## 2. Suggested: general assessment workflows

Continue with the [suggested design guide](suggested/README.md), [model](suggested/model.md), [API](suggested/api.md), and [adapter contracts](suggested/adapters.md). The model has six identity-bearing concepts: Scenario, ScenarioRevision, Run, StepRun, StepAttempt and Evidence. Queries, assertions, observations and reports use typed contracts and owned values.

The [suggested interface](../suggested/index.html) presents that model with realistic synthetic run and evidence data. The [class and lifecycle diagrams](../diagrams/suggested/README.md) cover every core entity and the important owned values. The complete [example programs](suggested/examples/README.md), schemas, locks and reference checks remain inspectable alongside the prose.

## 3. Review and evidence

| Record | Scope |
| --- | --- |
| [Current revision review](../REVIEW.md) | Changes and quality findings for this revised package and both interface views. |
| [Current revision validation](../VALIDATION.md) | Checks actually performed for the revised deliverables. |
| [Baseline model review](review/baseline-review.md) | Preserved findings from the reviewed native FIS model and generalized design. |
| [Baseline adversarial review](review/quality-review.md) | The earlier application, model, API and artifact defects, decisions and integration limits. |
| [Baseline validation](review/baseline-validation.md) | Historical tests, browser observations and PDF provenance; not a new validation claim. |
| [Documentation provenance](manifest.json) | Source commit and hashes for copied artifacts, plus the revised document/diagram inventory. |

All prose documents are Obsidian-compatible Markdown with unique YAML identities, related-note paths and explicit status. Standard relative Markdown links work in Obsidian and repository viewers. Each diagram note embeds its canonical Mermaid and links its SVG; machine schemas, locks, sources and code retain their native formats.

The reviewed source commit is `1b5ae1bd11fc61a2701d74ea89ccce2721889ef0`. The new package does not duplicate the historical PDF pipeline. Its [baseline review](review/baseline-review.md) provides immutable links to that earlier PDF and renderer. Provider facts, proposed product behavior and synthetic demonstrations retain separate provenance.
