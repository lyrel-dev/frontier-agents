---
id: agent-execution
kind: diagram
title: Agent execution and evidence cycle
refs:
- A-00
---

<!-- block: b-373b2cec067355369d7e -->
A task and its configuration guide an execution. Authorized tools return observations. Those observations can lead to another step or a result. Retention is a separate, product-specific path.

<!-- block: b-abfd81e3a85a5a57a023 -->
```dot
rankdir=LR;
request [label="Request or event\nTask and scope"];
context [label="Applicable configuration\nInstructions and context"];
run [label="Agent execution\nSelect the next step"];
tool [label="Authorized tool or assessment\nQuery or permitted operation"];
result [label="Result\nAnswer, finding, or artifact"];
request -> run [label="starts"];
context -> run [label="supplies context"];
run -> tool [label="invokes"];
tool -> run [label="returns observations"];
run -> result [label="produces"];
```
