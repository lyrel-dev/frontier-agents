# AWS Security Agent — HTML presentation reference



Open [security.html](security.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Application resources sit beneath shared account configuration

**Chapter:** Platform model. **Schedule:** 00:00–02:00. **Slide budget:** 02:00.

Requirements and integrations can have broader scope than a single application.



Account resources | Integrations, identity and requirement packs

Agent Space | Application sources, users and settings

Configuration | Target, authentication, criteria and limits

Run and evidence | Assessment results and linked verification



**Guide:** [S-01](../guides/security.html#S-01)



## 2. Registration is not repository connection

**Chapter:** Scope and authentication. **Schedule:** 02:00–04:00. **Slide budget:** 02:00.

Verify the deployed revision separately from the latest source branch.



Action | Establishes | Inspect

Register integration | Available source provider | Account type and authorization

Connect repository | Application source selection | Repository and branch identity

Enable feature | Selected assessment behavior | Modes, comments and remediation settings

Open as operator | Usable assessment access | Intended user rather than setup administrator



**Guide:** [S-02](../guides/security.html#S-02)



## 3. Network rules separate targets, dependencies and exclusions

**Chapter:** Scope and authentication. **Schedule:** 04:00–06:00. **Slide budget:** 02:00.

A verified domain is not authorization for every downstream effect.



Rule | Permitted purpose | Example

Target | Access and testing | Authorized staging application

Accessible | Supporting access; not attack target | Approved login dependency

Out of scope | No access; exclusion precedence | Production callback or payment path



**Guide:** [S-03](../guides/security.html#S-03)



## 4. Obtaining a credential is not logging into the application

**Chapter:** Scope and authentication. **Schedule:** 06:00–09:00. **Slide budget:** 03:00.

Save & Test verifies the configured flow; inspect where authentication fails.



Credential source | Direct input, secret, role or Lambda

Service access | Required trust and read/invoke permissions

Login instructions | How credentials and MFA apply

Authenticated role | Observed identity and protected routes



**Guide:** [S-M01](../guides/security.html#S-M01)



## 5. Learned login navigation is a specific reuse mechanism

**Chapter:** Scope and authentication. **Schedule:** 09:00–11:00. **Slide budget:** 02:00.

Login Optimization is not a universal vulnerability-memory service.



First successful login | Navigation is discovered

Saved skill | Successful procedure is retained

Later session | Procedure can be reused

Setting / flow change | Toggle reuse; verify actual identity again



**Guide:** [S-M02](../guides/security.html#S-M02)



## 6. A reusable configuration produces distinct executions

**Chapter:** Assessment and criteria. **Schedule:** 11:00–13:00. **Slide budget:** 02:00.

A completed status does not establish exhaustive coverage.



Object | Meaning

Draft | Incomplete configuration, not a completed test

Saved configuration | Reusable target, credentials and execution choices

Run | Assessment against then-current target/configuration

Task-hour limit | Cumulative task work, not elapsed wall time



**Guide:** [S-04](../guides/security.html#S-04)



## 7. Requirement evaluation starts with applicability

**Chapter:** Assessment and criteria. **Schedule:** 13:00–15:00. **Slide budget:** 02:00.

Configure requirement evaluation explicitly; vulnerability analysis alone is different.



Applicable and compliant | The required ownership check exists and supporting evidence is present.

Applicable and violating | A handler returns account-owned data without the required authorization.

Inapplicable | The requirement does not govern the evaluated component.



**Guide:** [S-M03](../guides/security.html#S-M03)



## 8. Regeneration replaces requirements; it does not append

**Chapter:** Assessment and criteria. **Schedule:** 15:00–17:00. **Slide budget:** 02:00.

Keep authoritative requirement source in Git and review replacement before enabling.



Source policy | Reviewed governing documents

Generate | Replace the pack contents

Review | Inspect generated and formerly manual rules

Enable | Use the reviewed replacement in later assessments



**Guide:** [S-M04](../guides/security.html#S-M04)



## 9. A proposed repair is not a deployed repair

**Chapter:** Repair, evidence and protection. **Schedule:** 17:00–19:00. **Slide budget:** 02:00.

Use the finding ID to connect the records, not similarity of titles.



Finding | Evidence and affected revision

Proposed change | Provider-specific patch or pull request

Engineering review | Tests and approval

Deployment | Known revision on the authorized target



**Guide:** [S-05](../guides/security.html#S-05)



## 10. Revalidation preserves the original finding

**Chapter:** Repair, evidence and protection. **Schedule:** 19:00–21:00. **Slide budget:** 02:00.

A non-reproduction result is scoped; failed authentication can invalidate its interpretation.



Selected finding | Original completed assessment

New job | Current credentials; repeat selected steps

Result | Reproduced or not reproduced

History | Original finding linked to new evidence



**Guide:** [S-M05](../guides/security.html#S-M05)



## 11. Earlier assessments use different resource lifecycles

**Chapter:** Repair, evidence and protection. **Schedule:** 21:00–23:00. **Slide budget:** 02:00.

Review inferred system context before relying on individual findings.



Assessment | Configuration model | Result focus

Code | Full scan or supported change trigger | Locations, evidence and suggested fixes

Design | One-off review; clone for new work | Design findings against requirements

Threat model | Reusable configuration and runs | System boundary, flows and threats



**Guide:** [S-06](../guides/security.html#S-06)



## 12. Encryption requires the correct identity and context

**Chapter:** Repair, evidence and protection. **Schedule:** 23:00–25:00. **Slide budget:** 02:00.

Administrator, web-app role, assessment role and asynchronous service access are distinct.



Customer KMS key | Protects resource branch keys

Branch key | Service-managed stored key material

Derived wrapping key | Protects data-encryption keys

Authorized request | Caller, action and encryption context must match



**Guide:** [S-M06](../guides/security.html#S-M06)



## 13. Exercise: verify the repaired account boundary

**Chapter:** Prepared-result exercise. **Schedule:** 25:00–33:00. **Slide budget:** 08:00.

Synthetic staging evidence only. No live penetration test or exploit execution.



0–2 min | Inspect the finding | User A received account B’s test invoice in demo-r1

2–4 min | Inspect the change | Ownership check reviewed; demo-r2 deployed

4–6 min | Inspect revalidation | Actual user A role and selected path reached

6–8 min | State the result scope | Prepared denial supports that path, not whole-app security



**Guide:** [S-U01](../guides/security.html#S-U01), [S-M05](../guides/security.html#S-M05)



## 14. Troubleshooting follows the failed prerequisite

**Chapter:** Troubleshooting and coverage. **Schedule:** 33:00–35:00. **Slide budget:** 02:00.

Full provider/pipeline and GenAI exception setup remains explicitly linked coverage.



Access | Separate repository connection, secret retrieval, application login and private routing.

Criteria | Check pack activation, applicability, regeneration and evaluation mode.

Evidence | Check deployment, actual identity, reachable path and linked job before closing a finding.



**Guide:** [S-07](../guides/security.html#S-07), [S-08](../guides/security.html#S-08)
