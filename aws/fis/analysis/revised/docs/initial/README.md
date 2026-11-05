---
id: aws-fis-revised-docs-initial-readme
title: Initial AWS FIS model
type: index
service: aws-fis
status: reviewed
version: '1.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- index
aliases:
- Initial AWS FIS model
related:
- report.md
- REVIEW.md
- sources.md
- ../suggested/README.md
- ../../diagrams/initial/README.md
---

# Initial AWS FIS model

This is the reviewed provider model that the initial interface demonstrates. It separates **catalog Action**, **named template action** and **named action execution**, then records run configuration, selected target memberships, source observations, report state and application assessments without merging their meanings.

| Read or inspect | Purpose |
| --- | --- |
| [Complete report](report.md) | Experiment and ExperimentAction fields, identity, relationships, lifecycle, API operations, derived measures, collection architecture and limits. |
| [Review entry](REVIEW.md) | Findings and the boundary between preserved baseline evidence and current revision validation. |
| [Official sources](sources.md) | Human-readable register of the 53 cited AWS pages; [JSON](sources.json) retains the original register bytes. |
| [Five entity relationship diagrams](../../diagrams/initial/README.md) | Execution, definitions, selected scope, evidence/reports and workload assessments. |
| [Initial interface](../../initial/index.html) | Preserved synthetic FIS Observatory, including live/history replay and action drilldown. |
| [Suggested workflow model](../suggested/README.md) | The next design: a general assessment program that treats FIS as one adapter. |

The report's native facts are sourced to official AWS documentation. Application normalization and workload verdicts are explicitly proposed extensions. No generic per-resource fault result or application resilience verdict is inferred from a completed FIS experiment. See the report's source-backed [purpose and scope](report.md#1-purpose-and-recommended-design).
