---
id: devops-integrations
kind: diagram
title: Provider registration and Agent Space association
refs:
- D-12
- D-03
---

<!-- block: b-af64db0ec4125814a035 -->
Provider authentication is registered at account level. Association and tool selection make an explicit subset available to the Agent Space. The invocation still needs a working authenticated route.

<!-- block: b-3e2be55cd67556a4859f -->
```dot
rankdir=LR;
provider [label="External provider\nTelemetry, code, or tool service"];
registration [label="Account registration\nEndpoint and authentication"];
association [label="Agent Space association\nSelected resources or tools"];
invocation [label="Tool invocation\nArguments and execution identity"];
observation [label="Source result\nResource ID and timestamp"];
provider -> registration [label="authorize"];
registration -> association [label="associate"];
association -> invocation [label="permits selected tool"];
invocation -> observation [label="query result"];
```
