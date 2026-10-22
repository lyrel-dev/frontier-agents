# AWS Security Agent — presenter reference



The schedule includes prepared-result exercises. It is not a promise of live agent completion time. Questions and breaks are additional. Canonical guide sections are reproduced in speaker notes as reference, not as a required verbatim script.



## 1. Application resources sit beneath shared account configuration

**Schedule:** 00:00–02:00. **Type:** flow.

Requirements and integrations can have broader scope than a single application.

**Display content:**

Account resources | Integrations, identity and requirement packs

Agent Space | Application sources, users and settings

Configuration | Target, authentication, criteria and limits

Run and evidence | Assessment results and linked verification

**Canonical reference:** [S-01](../guides/security.html#S-01)



## 2. Registration is not repository connection

**Schedule:** 02:00–04:00. **Type:** table.

Verify the deployed revision separately from the latest source branch.

**Display content:**

Action | Establishes | Inspect

Register integration | Available source provider | Account type and authorization

Connect repository | Application source selection | Repository and branch identity

Enable feature | Selected assessment behavior | Modes, comments and remediation settings

Open as operator | Usable assessment access | Intended user rather than setup administrator

**Canonical reference:** [S-02](../guides/security.html#S-02)



## 3. Network rules separate targets, dependencies and exclusions

**Schedule:** 04:00–06:00. **Type:** table.

A verified domain is not authorization for every downstream effect.

**Display content:**

Rule | Permitted purpose | Example

Target | Access and testing | Authorized staging application

Accessible | Supporting access; not attack target | Approved login dependency

Out of scope | No access; exclusion precedence | Production callback or payment path

**Canonical reference:** [S-03](../guides/security.html#S-03)



## 4. Obtaining a credential is not logging into the application

**Schedule:** 06:00–09:00. **Type:** flow.

Save & Test verifies the configured flow; inspect where authentication fails.

**Display content:**

Credential source | Direct input, secret, role or Lambda

Service access | Required trust and read/invoke permissions

Login instructions | How credentials and MFA apply

Authenticated role | Observed identity and protected routes

**Canonical reference:** [S-M01](../guides/security.html#S-M01)



## 5. Learned login navigation is a specific reuse mechanism

**Schedule:** 09:00–11:00. **Type:** flow.

Login Optimization is not a universal vulnerability-memory service.

**Display content:**

First successful login | Navigation is discovered

Saved skill | Successful procedure is retained

Later session | Procedure can be reused

Setting / flow change | Toggle reuse; verify actual identity again

**Canonical reference:** [S-M02](../guides/security.html#S-M02)



## 6. A reusable configuration produces distinct executions

**Schedule:** 11:00–13:00. **Type:** table.

A completed status does not establish exhaustive coverage.

**Display content:**

Object | Meaning

Draft | Incomplete configuration, not a completed test

Saved configuration | Reusable target, credentials and execution choices

Run | Assessment against then-current target/configuration

Task-hour limit | Cumulative task work, not elapsed wall time

**Canonical reference:** [S-04](../guides/security.html#S-04)



## 7. Requirement evaluation starts with applicability

**Schedule:** 13:00–15:00. **Type:** columns.

Configure requirement evaluation explicitly; vulnerability analysis alone is different.

**Display content:**

Applicable and compliant | The required ownership check exists and supporting evidence is present.

Applicable and violating | A handler returns account-owned data without the required authorization.

Inapplicable | The requirement does not govern the evaluated component.

**Canonical reference:** [S-M03](../guides/security.html#S-M03)



## 8. Regeneration replaces requirements; it does not append

**Schedule:** 15:00–17:00. **Type:** flow.

Keep authoritative requirement source in Git and review replacement before enabling.

**Display content:**

Source policy | Reviewed governing documents

Generate | Replace the pack contents

Review | Inspect generated and formerly manual rules

Enable | Use the reviewed replacement in later assessments

**Canonical reference:** [S-M04](../guides/security.html#S-M04)



## 9. A proposed repair is not a deployed repair

**Schedule:** 17:00–19:00. **Type:** flow.

Use the finding ID to connect the records, not similarity of titles.

**Display content:**

Finding | Evidence and affected revision

Proposed change | Provider-specific patch or pull request

Engineering review | Tests and approval

Deployment | Known revision on the authorized target

**Canonical reference:** [S-05](../guides/security.html#S-05)



## 10. Revalidation preserves the original finding

**Schedule:** 19:00–21:00. **Type:** flow.

A non-reproduction result is scoped; failed authentication can invalidate its interpretation.

**Display content:**

Selected finding | Original completed assessment

New job | Current credentials; repeat selected steps

Result | Reproduced or not reproduced

History | Original finding linked to new evidence

**Canonical reference:** [S-M05](../guides/security.html#S-M05)



## 11. Earlier assessments use different resource lifecycles

**Schedule:** 21:00–23:00. **Type:** table.

Review inferred system context before relying on individual findings.

**Display content:**

Assessment | Configuration model | Result focus

Code | Full scan or supported change trigger | Locations, evidence and suggested fixes

Design | One-off review; clone for new work | Design findings against requirements

Threat model | Reusable configuration and runs | System boundary, flows and threats

**Canonical reference:** [S-06](../guides/security.html#S-06)



## 12. Encryption requires the correct identity and context

**Schedule:** 23:00–25:00. **Type:** flow.

Administrator, web-app role, assessment role and asynchronous service access are distinct.

**Display content:**

Customer KMS key | Protects resource branch keys

Branch key | Service-managed stored key material

Derived wrapping key | Protects data-encryption keys

Authorized request | Caller, action and encryption context must match

**Canonical reference:** [S-M06](../guides/security.html#S-M06)



## 13. Exercise: verify the repaired account boundary

**Schedule:** 25:00–33:00. **Type:** demo.

Synthetic staging evidence only. No live penetration test or exploit execution.

**Display content:**

0–2 min | Inspect the finding | User A received account B’s test invoice in demo-r1

2–4 min | Inspect the change | Ownership check reviewed; demo-r2 deployed

4–6 min | Inspect revalidation | Actual user A role and selected path reached

6–8 min | State the result scope | Prepared denial supports that path, not whole-app security

**Canonical reference:** [S-U01](../guides/security.html#S-U01), [S-M05](../guides/security.html#S-M05)



## 14. Troubleshooting follows the failed prerequisite

**Schedule:** 33:00–35:00. **Type:** columns.

Full provider/pipeline and GenAI exception setup remains explicitly linked coverage.

**Display content:**

Access | Separate repository connection, secret retrieval, application login and private routing.

Criteria | Check pack activation, applicability, regeneration and evaluation mode.

Evidence | Check deployment, actual identity, reachable path and linked job before closing a finding.

**Canonical reference:** [S-07](../guides/security.html#S-07), [S-08](../guides/security.html#S-08)


