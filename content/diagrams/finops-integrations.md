---
id: finops-integrations
kind: diagram
title: Data-source access and collaboration connections
refs:
- F-08
- F-05
---

<!-- block: b-1e91e3cb7f8f5225a905 -->
AWS source access is controlled by the agent data role. Collaboration uses account-level registration and an agent-specific destination. Successful source retrieval and successful publication are independent checks.

<!-- block: b-f6efc5e4728c5e138f92 -->
```dot
rankdir=TB;
dataRole [label="Agent data role\nSpecific AWS actions and scope"];
aws [label="AWS cost and operational services\nQueries and recommendation reads"];
agent [label="Agent task\nAnalysis and result"];
registration [label="Account integration\nJira site or Slack workspace"];
connection [label="Agent connection\nSelected project or channel"];
action [label="Publication action\nDestination-specific approval behavior"];
dataRole -> aws [label="authorizes reads"];
aws -> agent [label="returns evidence"];
registration -> connection [label="destination binding"];
connection -> action [label="permits destination"];
agent -> action [label="requested result publication"];
```
