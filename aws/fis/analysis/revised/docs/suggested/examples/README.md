---
id: aws-fis-revised-docs-suggested-examples-readme
title: Assessment scenario examples
type: examples-index
service: aws-fis
status: reviewed-proposal
version: '0.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- examples-index
aliases:
- Assessment scenario examples
related:
- ../README.md
- ../model.md
- ../adapters.md
- alarm-delivery.md
- logs-error-budget.md
---

# Assessment scenario examples

These are complete proposed authoring documents, not executable AWS automation. Each example declares inputs and trusted connection bindings, a main step graph, explicit assessment criteria and an unconditional finalization graph. Its companion lock pins the program and synthetic operation/schema contracts.

| Example | Question | Main steps / finalizers / criteria |
| --- | --- | --- |
| [Alarm and receiver delivery](alarm-delivery.md) | Did the bound alarm transition, and did the specifically bound probe receiver observe its notification in the declared window? | 7 / 2 / 2 |
| [Logged error count](logs-error-budget.md) | Does a complete covered query for the declared log scope and event-time window meet the configured count threshold? | 2 / 1 / 1 |

The YAML documents and lock JSON are preserved from the reviewed baseline. Implementation digests are synthetic labels: there is no executable operation package behind them here. The [model](../model.md), [adapter contracts](../adapters.md), [authoring schema](../scenario.schema.json) and [operation catalogue](../operation-catalog.json) specify the semantics.

From the repository root:

```bash
python3 aws/fis/analysis/revised/docs/suggested/contract.py
python3 -m unittest discover -s aws/fis/analysis/revised/docs/suggested/tests -v
```

These checks validate structure, reference scope, locks and selected normative decisions. They do not execute CEL, query AWS, authenticate evidence, prove collector coverage or implement durable cancellation/finalization.
