# AWS DevOps Agent — presenter reference



The schedule includes prepared-result exercises. It is not a promise of live agent completion time. Questions and breaks are additional. Canonical guide sections are reproduced in speaker notes as reference, not as a required verbatim script.



## 1. An Agent Space connects configuration to executions

**Schedule:** 00:00–02:00. **Type:** flow.

Configuration, execution and evidence are different objects.

**Display content:**

Account registrations | Providers and AWS account access

Agent Space | Associations, selected tools and operator access

Agent definition | Managed behavior or custom prompt and attachments

Execution | Investigation, invocation and observable tool results

**Canonical reference:** [D-01](../guides/devops.html#D-01)



## 2. Two access paths need separate verification

**Schedule:** 02:00–04:00. **Type:** table.

A created workspace is not proof that its data sources are readable.

**Display content:**

Path | Purpose | Acceptance check

Resource role | Read authorized AWS sources | Known resource and identity are correct

Operator role | Let people use the space | Intended user—not only administrator—can enter

Connected provider | Access selected external tools | Arguments and returned source agree

**Canonical reference:** [D-02](../guides/devops.html#D-02)



## 3. MCP setup has authentication-specific decisions

**Schedule:** 04:00–07:00. **Type:** table.

Role-less SigV4 validation is deferred to association.

**Display content:**

Method | Required decisions

OAuth | Token/authorization endpoints, client and scopes

API key / secret headers | Actual header names and supported rotation path

SigV4 | Signing Region, service and role option

Association | Select tools in the Agent Space; verify there

**Canonical reference:** [D-03](../guides/devops.html#D-03)



## 4. Private routing and provider identity are separate

**Schedule:** 07:00–09:00. **Type:** flow.

Check the gateway path and target port before rotating a valid secret.

**Display content:**

Agent service | Uses configured private connection

Resource gateway | ENIs in selected VPC subnets

Endpoint route | DNS, host and allowed port ranges

Authenticated tool | Provider authentication and selected operation

**Canonical reference:** [D-04](../guides/devops.html#D-04)



## 5. Topology is a representation, not an access boundary

**Schedule:** 09:00–11:00. **Type:** columns.

A missing graph node does not establish that a direct resource read is denied.

**Display content:**

Discovery | CloudFormation resources and enabled Resource Explorer supply inventory.

Relationships | Configuration, tags, pipeline mapping and observability supply evidence.

Verification | Compare one service/repository edge with the deployed configuration.

**Canonical reference:** [D-05](../guides/devops.html#D-05)



## 6. Past incidents become selected contextual evidence

**Schedule:** 11:00–14:00. **Type:** flow.

Retention, retrieval and diagnostic correctness require separate observations.

**Display content:**

Investigations | Earlier outcomes and evidence

Learning process | Synthesizes monitor-specific knowledge

Memory store | Descriptions, entries, versions and active state

New investigation | Selects relevant context and checks current evidence

**Canonical reference:** [D-M01](../guides/devops.html#D-M01)



## 7. Corrections and access attachments solve different problems

**Schedule:** 14:00–16:00. **Type:** columns.

Feedback changes contextual knowledge; attachment changes which context an agent may use.

**Display content:**

Correct a diagnosis | Submit verified feedback; inspect the resulting lesson. AWS sharing is a separate choice.

Attach context | New custom agents start without stores. Attach only required stores; managed stores are read-only to them.

**Canonical reference:** [D-M02](../guides/devops.html#D-M02), [D-M07](../guides/devops.html#D-M07)



## 8. Instructions and skills enter the session differently

**Schedule:** 16:00–18:00. **Type:** table.

Prompt guidance does not grant or revoke IAM permissions.

**Display content:**

Control | Loading behavior | Configuration test

Instructions | Applicable text at session startup | Compare an existing and new session

Skill | Procedure selected by description and scope | Compare a matching and nonmatching request

Permissions | Enforced by the connected systems | Test an expected denial separately

**Canonical reference:** [D-M03](../guides/devops.html#D-M03), [D-M04](../guides/devops.html#D-M04)



## 9. Inspect triage before diagnosing a missing investigation

**Schedule:** 18:00–20:00. **Type:** table.

Routing correction and root-cause feedback are different operations.

**Display content:**

Decision | Meaning | Operator response

Linked | Signal belongs to existing work | Inspect the primary investigation; unlink if wrong

Skipped | Configured criteria excluded it | Inspect rule/skill; unskip if wrong

Proceed | Independent work is scheduled | Inspect execution and evidence

**Canonical reference:** [D-06](../guides/devops.html#D-06)



## 10. A trigger creates work; cancellation affects a run

**Schedule:** 20:00–22:00. **Type:** flow.

In-flight calls may finish after cancellation; a schedule is not the data window.

**Display content:**

Definition | Prompt, selected tools, skills and stores

Trigger | Manual, rate or cron; inspect next run

Invocation | History shows status and tool trajectory

Stop controls | Pause future starts; cancel existing work separately

**Canonical reference:** [D-07](../guides/devops.html#D-07)



## 11. Sandbox and directed actions have different boundaries

**Schedule:** 22:00–25:00. **Type:** columns.

Application or tool effects must be reviewed; “read-only” is not a universal agent label.

**Display content:**

Sandbox | Fresh investigation-local environment; configured packages and outbound rules. Empty allowlist still permits AWS endpoints.

Directed actions | Space opt-in, eligible access and specific operation/resource approval. Inspect classification and final state.

**Canonical reference:** [D-M05](../guides/devops.html#D-M05), [D-M06](../guides/devops.html#D-M06)



## 12. Update semantics are part of the operational contract

**Schedule:** 25:00–27:00. **Type:** table.

Read current configuration first, then verify the saved result.

**Display content:**

Object | Update behavior | Avoid

Asset metadata | PATCH semantics | Assuming names can replace required asset IDs

Space preferences map | Replacement when supplied | Dropping existing values unintentionally

Memory entry | New immutable version | Treating edits as erased history

**Canonical reference:** [D-08](../guides/devops.html#D-08), [D-M06](../guides/devops.html#D-M06)



## 13. Exercise: same alarm, different evidence

**Schedule:** 27:00–35:00. **Type:** demo.

Synthetic prepared-result exercise. Do not claim observed AWS recall or a proven deployment cause.

**Display content:**

0–2 min | Inspect historical memory | Earlier database pool saturation

2–4 min | Compare new fixture | DB 34/100 connections; query p95 18 ms

4–6 min | Evaluate current lead | Inventory p95 2,900 ms; checkout 3,100 ms

6–8 min | Record the boundary | Upstream lead supported; internal cause unresolved

**Canonical reference:** [D-U01](../guides/devops.html#D-U01), [D-M01](../guides/devops.html#D-M01), [D-M02](../guides/devops.html#D-M02)



## 14. Diagnose the failing layer, then retest

**Schedule:** 35:00–37:00. **Type:** columns.

Full remote-protocol and release-profile procedures remain linked scope, not completed live tests.

**Display content:**

Access and connectivity | Check operator identity, source role, provider association, route and endpoint port.

Context and execution | Check activation, descriptions, attachments, session start and concurrency.

Changes and coverage | Check exact approval and update semantics; consult current quotas and feature eligibility.

**Canonical reference:** [D-10](../guides/devops.html#D-10), [D-11](../guides/devops.html#D-11)


