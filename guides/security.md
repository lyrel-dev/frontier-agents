# AWS Security Agent

Application scope, assessment configuration, findings, and revalidation

AWS Security Agent analyzes source code and design material, constructs threat models, and performs application penetration tests. An Agent Space selects application sources and assessment configuration. Assessment results, remediation proposals, deployed revisions, and revalidation jobs have separate identities and lifecycles. Feature availability and provider support must be checked for the selected assessment. [SS01] [SS02]

The guide defines shared and application-scoped resources before describing repository access, target rules, authentication, requirements, assessment execution, and finding management. The worked example traces an authorization finding through a proposed repair and targeted revalidation.

**Reading conventions.** Product statements link to official AWS documentation. Configuration recommendations and verification procedures are team guidance; the proposed tests and synthetic examples have not been executed against AWS. Lifecycle tables describe service behavior and operator actions, not an API status enumeration unless explicitly cited. DOC (blue), AWS (green), and EXT (orange) identify concept ownership. Source-review dates and qualifications are recorded in the source registers.

## 01. Resource model and scope

Begin with the product-specific entities, their scope and their relationships. Configuration, executions, knowledge and external evidence are distinct objects with different lifecycles.

### S-01 — Shared configuration, Agent Spaces and assessments

AWS Security Agent organizes work around an application Agent Space. The space groups application sources, assessment settings and user assignments. Some configuration is shared above that boundary, including registered integrations and security requirements. The guide calls this tenant or organizational scope; this model does not turn that phrase into an AWS Organizations resource or infer automatic cross-account policy propagation. [SS50]

A source is connected in stages. The administrator authorizes an integration; the application space selects repositories or documentation; capability settings determine how those sources are used. One repository can supply several spaces without making their assessment settings identical. Source access, permission to submit a fix and permission to publish a finding are separate relationships. [SS50] [SS51]

![Shared configuration and application scope](../assets/diagrams/er-security-scope.svg)

The assessment type determines the execution model. Penetration testing and threat modeling use reusable configurations with separate runs. Full-code scans also have reusable configuration, while repository-event review has provider-specific settings. Design review is a one-off assessment; cloning creates a new review. A generic Configuration → Run arrow is therefore an explanatory starting point, not a universal schema for every Security Agent function. [SS50]

Application context, criteria and access play different roles. Code and documents explain the system. Requirements define what eligible design and code reviews should evaluate. Target rules and credentials define the reachable identity and boundary for a running-application assessment. A retained successful login procedure helps reuse authentication navigation; it is not evidence of a general incident-memory service. [SS52] [SS53] [SS56]

Green nodes below and in the resource index denote AWS-defined concepts; their subtitles distinguish reusable configuration, a run, a result and managed state. Orange denotes the actual repository, test application or external issue. Blue denotes our normalized associations and review structure, not service resources. This distinction becomes important when tracing one original finding through several revalidation jobs.

The next section explains the assessment-specific relationships. Later chapters configure sources and targets, examine authentication and criteria, and follow the existing assessment, remediation and verification use cases. The [product resource index](../catalog/resource-models.html#model-security) records entity identities and the evidence supporting each relationship.

### S-10 — Assessment configurations, runs and result identities

A saved configuration answers what should be assessed. A run answers what happened during a particular execution. Keeping those identities separate prevents a later configuration change from being mistaken for a change to an earlier result. It also allows the same application to be assessed repeatedly while retaining the conditions of each run. This configuration-and-run relationship is documented for penetration tests, full-code scans and threat models, but not for one-off design reviews. [SS50] [SS57]

![Assessment configurations and executions](../assets/diagrams/er-security-assessments.svg)

For penetration testing, target rules and credential definitions belong to the saved assessment configuration. The execution then reaches the actual deployed application using the available identity. The repository revision used for source context and the revision deployed at the target may differ. A successful credential read is not confirmation that the target login succeeded, and a successful login is not proof that every protected route was exercised. The configuration and the observed conditions of the run must both be retained. [SS52] [SS56]

For code review, separate a full-scan configuration from connected-repository settings for change-triggered analysis. Both can produce source findings, but the event, selected revision and review mode determine what was analyzed. A source-code finding should not be treated as a penetration-test finding merely because both concern authorization. The selected-finding revalidation procedure described later applies to existing penetration-test findings, not to an invented universal finding subtype. [SS50] [SS54]

Requirements also have their own identity. Each requirement belongs to a pack, and enabled criteria inform future eligible reviews. A requirement is a reusable criterion, not the compliance result for every application. Updating a shared requirement does not retroactively rewrite earlier review findings. The criteria-generation workflow has its own replacement behavior, detailed in S-M04. [SS53]

| Subject | Maintained object | Execution or result | Correct interpretation of reuse |
|---|---|---|---|
| Running application | Penetration-test configuration | Independent run and findings | Repeat the configuration; record current target and identity each time |
| Full source | Code-review configuration | Source review and code findings | Repeat against an identified source revision |
| Repository change | Connected-repository review settings | Revision-specific review | Verify supported event and current revision |
| Proposed design | Individual design review | Findings from that assessment | Clone into a new review; do not claim rerun of the same object |
| System threats | Threat-model configuration | Run-specific overview and threats | Re-run with reviewed scope and sources |
| Organization criterion | Requirement pack and requirement | Result within an eligible review | Apply to later assessments, not retroactive result mutation |

These differences determine both operation and failure diagnosis. A draft configuration is not a completed assessment. A code-review comment is not a deployed repair. A threat-model output built around the wrong boundary needs corrected input, not merely a new label on its threats. The supported operations are detailed in S-04 and S-06; the table is their resource-model interpretation. [SS50] [SS57]

Some relationships deliberately remain unspecified. The public guidance documents retained login reuse but does not establish an independently editable skill resource for it. The diagrams use `?` where counts or parent fields are not documented, rather than inventing a universal resource schema. See the [qualified relationship register](../catalog/resource-models.html#model-security) before translating any diagram into implementation assumptions.

## 02. Application sources and target access

Application evidence and a reachable test target are separate prerequisites. The source inventory is followed by user access and the explicit boundaries of a dynamic test.

### S-09 — Supported source and collaboration integrations

Security assessment needs both application evidence and a reachable test surface. A repository explains code; a design page explains intent; a deployed endpoint exposes actual behavior. Connecting one of those sources does not substitute for the others. The account-level integration is registered once, while each Agent Space selects the repositories, pages, buckets, or projects appropriate to its application. [SS30]

| Source or destination | Documented support | Selection in the application space | Effect boundary |
|---|---|---|---|
| GitHub | Cloud-hosted GitHub and cloud-hosted GitHub Enterprise | Connected repositories | Read analysis; repository write features are separate opt-ins |
| GitHub Enterprise Server | Self-hosted server | Selected repositories and configured reachability | Private connectivity may be necessary |
| GitLab | Cloud-hosted GitLab | Selected repositories | Provider-specific review comments and remediation configuration |
| GitLab Self-Managed | Self-hosted instance | Selected repositories and reachable endpoint | Authentication and private routing require their own setup |
| Bitbucket | Bitbucket Cloud | Selected repositories | Do not extend Cloud support to self-hosted editions |
| Azure DevOps | Git repositories; TFVC unsupported | Authorized organization and selected repositories | Entra service principal and Azure DevOps permissions; review comments and remediation configured separately [SS490] |
| Confluence | Confluence Cloud | Selected pages | Read-only documentation context, not a source-code repository |
| Amazon S3 | Connected same-account buckets or prefixes | Resources selected for an assessment | Code-review sources use supported source archives; supporting documents have their own formats |
| Jira | Jira Cloud | Selected projects | Finding issue creation and comments are independently allowed per project |

Connecting a repository grants read context to the eligible assessment functions that share the space. Code-review comments and code-remediation changes are enabled separately per repository. The integration overview excludes these write actions for public repositories; do not interpret read access as permission to publish a patch or comment. [SS30]

For Azure DevOps, registration authorizes the Microsoft Entra application. Add its service principal to the Azure DevOps organization and grant repository and service-hook permissions before selecting repositories in an Agent Space. Public-repository remediation is not supported. The provider guide describes project limits and required permissions; registration alone does not complete access setup. [SS490]

![Application-source registration and selection](../assets/diagrams/security-integrations.svg)

To configure a source, first authorize its supported provider account from Integrations. Open the application Agent Space, select resources from that registration, and save the selection. Then configure the assessment that consumes those resources. For Confluence, selecting a page supplies read context; there are no per-page assessment toggles. For S3, connect the bucket or prefix once and select the needed resources when authoring an assessment. The S3 guide specifies same-account buckets and separate requirements for code-review sources. [SS31] [SS33]

Jira follows a related but action-oriented sequence. Install and authorize the documented Forge application, register the Jira Cloud site, then choose projects for the Agent Space. Allow issue creation, comments, or both according to the workflow. Existing Jira issues are external records: removing the connection does not remove the issues already created. [SS32]

Private source-control access, penetration-test network access, and credential retrieval are separate paths. A reachable repository does not prove that the test runner can reach a private application. Similarly, a readable secret does not establish that its contents successfully log in to that application. The next chapter follows these distinctions through authentication and context construction.

<!-- mechanism-review:start S-09 -->

#### MX-S-JIRA — Finding publication to Jira

A site registration supplies authorization; a project connection chooses where the Agent Space can create issues or comments. Creating an issue publishes a finding into an external system with its own audience and lifecycle. [SS415] [SS416] [SS417]

The link matters later: remediation proposals and revalidation outcomes can be attached to the same issue through supported behavior. Removing the integration stops future actions but does not remove tickets already created. [SS415] [SS416] [SS417]

**Inputs.** Connected Jira Cloud site, permitted project/actions, selected finding and reviewed disclosure scope.

**Configuration**

1. **Register — Site authorization.** Integrations → Add integration → Jira; authorize the Forge app and registration.
2. **Bind — Project-specific effects.** Within Agent Space select project and allowed create/comment actions.
3. **Publish — One issue per selected finding.** Select finding(s) and create issues in a project permitting the Task type.

[SS415] [SS416] [SS417]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Finding selected | Create Jira issue | External record and finding relationship created. |
| Linked finding revalidated | Supported result comment | External history updated when permitted. |
| Integration removed | Future publication attempted | No further action through that integration; existing issues remain. |

**Constraints.** Issue creation and comment permission are separate. Do not import FinOps approval behavior into Security Agent.

**Inspection points.** Actual issue/comment in the intended project and preserved finding link.

**Implementation limits.** Automatic duplicate suppression and transactional rollback across AWS and Jira are not established.

**Verification procedure (proposed)**

1. Use a restricted test project and a non-sensitive finding fixture.
2. Check audience, issue type and finding link.
3. Revoke comment permission; distinguish publication failure from assessment failure and avoid blind duplicate retries.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS415] | Connecting projects to an Agent Space | Create and comment actions are selected per project. |
| [SS416] | Creating issues for findings | The selected project must allow Task and receives one issue per selected finding. |
| [SS417] | Prerequisites for removal | Previously created issues are not deleted with the integration. |

<!-- mechanism-review:end S-09 -->

### S-02 — User access and repository connections

An administrator prepares the application workspace; an operator performs assessments within it. Source-provider registration authorizes a provider account, while repository connection selects application material. Treat these as distinct setup milestones so an inaccessible repository is not confused with a user-access failure.

The console is the administrative surface. The web app is the assessment workspace. IAM-based operators can enter through the console route; IAM Identity Center supports assigned users without requiring ordinary console access. Configure the intended operator identity, not just the administrator who creates the Agent Space. [SS04] [SS05]

**Configuration procedure:** create or select an Agent Space, establish the supported identity mode, register the source integration, connect the application's repositories, and enable the relevant feature. For a GitHub integration, verify whether the installation belongs to a personal account or organization and whether organization approval is required. A successful account registration does not mean a repository was connected. [SS03] [SS05] [SS06]

For code review, independently review the settings for vulnerability analysis, requirement evaluation, comments, and automatic remediation. Enabling one does not establish that all others are active. S3 can be a code source through its own supported configuration path; provider-specific integration instructions remain authoritative. [SS05]

**Engineering verification:** open the web app as the intended user, inspect the connected source and selected branch, and compare the source revision with the deployed test application. Record a known read and an expected denial. Do not place credentials in a repository or presentation to simplify the example.

### S-03 — Test targets, dependencies, and exclusions

A dynamic assessment is defined by what it may reach and what it may test. Some endpoints are application targets, while others are dependencies needed only for authentication or supporting content. Explicit exclusions keep that supporting access from expanding the test into an unintended environment.

Domain verification demonstrates control through a supported verification method, including DNS, HTTP or a private-VPC route. It is a technical prerequisite, not authorization for every downstream system the application can contact. Private testing additionally needs a supported VPC configuration, subnets, routing and security groups. [SS07]

The current penetration-test wizard separates three network rule classes. [SS08]

| Class | Intended behavior | Example in an authorized staging environment |
|---|---|---|
| Target | May be accessed and tested | `https://staging.example.test:8443` |
| Accessible | May be accessed to support the assessment, not attacked as a target | Approved login-provider or static-content endpoint |
| Out of scope | Must not be accessed; exclusions take precedence | A payment or production callback path |

These example names are illustrative, not running targets. Specify the complete scheme and nonstandard port when applicable. The current wizard supports explicit nonstandard ports; an older troubleshooting page states only 80/443. This guide follows the task-specific wizard and records the conflict rather than repeating the older restriction. [SS08] [SS06]

**Configuration procedure:** prepare the verified target and explicit exclusions; choose public or private connectivity; add representative test credentials; complete the network rules after authentication discovery; inspect suggested extra domains before accepting them. Keep essential login dependencies reachable without turning them into attack targets. Only execute against systems and effects that their owners have authorized. [SS07] [SS08]

**Expected confirmation:** the saved configuration identifies the target, network path, credential roles and exclusions. Draft configuration and successful authentication preflight are different states. Neither proves that a complete assessment has run.

<!-- mechanism-review:start S-03 -->

#### MX-S-ACCESS — Target scope and network access

The test configuration separates attack targets from supporting navigation and excluded paths. A login provider can be reachable without becoming a vulnerability-testing target. A private route supplies connectivity; it does not widen the scope approved by the application owner. [SS402] [SS418]

Treat reachability as a prerequisite. If a target cannot be reached, the missing result is a coverage gap. Broadening the target list or removing an exclusion is a scope change, not a routine network troubleshooting shortcut. [SS402] [SS418]

**Inputs.** Verified target domains, supporting accessible domains, excluded paths, applicable VPC route and authorized test scope.

**Configuration**

1. **Target — Active test surface.** Create/edit penetration test: select verified target URLs.
2. **Supporting access — Navigation support, not attack targets.** List necessary accessible URLs separately.
3. **Exclusions and network — Scope and network controls.** Configure excluded paths and the approved VPC connectivity when required.

[SS402] [SS418]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Configuration saved | Preflight/connection attempted | Reachability is checked before meaningful target testing. |
| Target unreachable | Correct approved route or name resolution | Rerun the prerequisite check without broadening authorization. |
| Scope changed | Review authorization and save configuration | A future run has a different assessment surface. |

**Constraints.** Ownership verification and network reachability are not substitutes for owner authorization. Active tests can change application state.

**Inspection points.** Preflight outcome and records of the actual target and paths reached.

**Implementation limits.** The sources do not establish that every reachable path is exercised or that every excluded interaction has a uniform implementation across all targets.

**Verification procedure (proposed)**

1. Use a non-production target, supporting login host and an explicit excluded fixture path.
2. Verify target access and intended application role.
3. A denied path or unresolved target must not produce a claim of assessed coverage.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS402] | Configure penetration test scope; Configure VPC resources | Targets, supporting accessible URLs and excluded paths have different purposes. |
| [SS418] | Review penetration test findings | Failed preflight stops testing and must be inspected separately. |

<!-- mechanism-review:end S-03 -->

## 03. Application knowledge and assessment criteria

Source context explains the application, requirements supply criteria, and authentication provides a reachable identity. Their reuse mechanisms differ and are described separately.

### S-M07 — Application-context construction and reuse

An assessment starts with the application material selected for that task. Source code supplies implementation evidence; API and design documents describe interfaces and intended relationships; scope documents delimit what a threat model should analyze. The Agent Space makes connected material available, but the assessment configuration still determines what is relevant to a particular run. An engineering record should identify the source revision and document version used rather than simply say that the agent knows the application. [SS03] [SS16] [SS31]

![Application context, assessment criteria, and findings](../assets/diagrams/security-context.svg)

The context is consolidated into an assessment of the selected system. In a threat-model workflow, this can include a system overview, data flows, trust boundaries, and candidate threats. In a penetration test, source and documentation context supports exploration of the authorized deployed target. Review the inferred model before evaluating its conclusions: a missing identity boundary or a document for the wrong release changes the question being answered. [SS16] [SS34]

Three different forms of reuse must remain distinct. A saved assessment configuration retains reusable setup. A requirement pack supplies criteria to later eligible reviews. Login Optimization retains a successful authentication procedure. None of these establishes the DevOps Agent monitor-memory mechanism for Security Agent. The reviewed guidance does not describe a universal customer-editable vulnerability-memory store or an automatic model-training process across all assessments. [SS03] [SS09] [SS14]

For an application change, reconnect or select the current sources, update the scope where necessary, and create the next run. For a wrong requirement, edit the governing criteria; for a changed login, test the current credential flow. Historical findings remain evidence of earlier executions, not a substitute for the new source and target state. A revalidation job retrieves selected existing finding evidence and tests that finding again; it is narrower than reconstructing or rescanning the whole application. [SS13]

A practical verification starts with a small known boundary: two application roles, one protected resource, and the repository revision deployed to staging. Inspect whether the inferred system and the resulting finding refer to those same roles and revision. When the evidence does not expose which document or procedure was used, record that limitation rather than infer it from plausible output.

<!-- mechanism-review:start S-M07 -->

#### MX-S-CONTEXT — Application-context assembly

Registration authorizes a provider account; connecting particular resources supplies application-specific evidence. A selected repository can support several assessment types without being independently registered for each. Context assembly must nevertheless use the correct application and revision. [SS401]

Read access and publication of comments or proposed changes are separate. A context read can help interpret an application without creating a permission to change its repository. The service documentation describes the evidence inputs but not a universal persistent knowledge store or retrieval algorithm for every assessment. [SS401]

**Inputs.** Connected source/document resources, selected revision or design scope, service-role access and assessment configuration.

**Configuration**

1. **Register — Account-level registration.** Integrations: authorize the supported provider account.
2. **Connect — Application-scoped evidence.** Within the intended Agent Space, select repositories or documentation resources.
3. **Configure effects — Optional repository effects.** Review per-repository write options separately from source reads.

[SS401]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Provider registered | Connect resource to space | Read context becomes available through that association. |
| Application changes | Start assessment against intended sources | A previous result remains tied to its earlier evidence. |
| Write option disabled | Run eligible read analysis | Read context does not imply comment or repair permission. |

**Constraints.** Keep application boundary and revision explicit. Private source-control access is separate from private target access.

**Inspection points.** Selected resource identity and assessment source/preflight evidence.

**Implementation limits.** Cross-assessment cache freshness, internal ranking and automatic refresh guarantees are not established.

**Verification procedure (proposed)**

1. Select a repository and design document that describe one known staging application.
2. Check that a run identifies that application and revision.
3. Supply a mismatched design revision and require an explicit mismatch rather than a merged invented architecture.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS401] | Register once, reuse everywhere; One connection, shared across capabilities | Registration, resource association and write opt-ins are distinct. |

<!-- mechanism-review:end S-M07 -->

### S-M01 — Credential retrieval and application login

Authentication has two stages. The service must obtain a valid test credential, then apply it through the application’s login flow. The second stage may involve navigation and MFA even when the first stage is a straightforward secret read. The evidence should identify which stage succeeded.

The service first obtains a credential and then follows login instructions to apply it to the application. A successful secret retrieval is not a successful application login. Current configuration requires a credential name, access URL, method and login prompt; **Save & Test** or **Test All** exercises authentication and exposes success/failure information. [SS09] [SS08]

| Strategy | Required dependency | Typical failure to distinguish |
|---|---|---|
| Direct test credential | Correct application identity and instructions | Wrong login URL, role or form flow |
| Secrets Manager | Same-account secret; service role with `secretsmanager:GetSecretValue` and `secretsmanager:DescribeSecret` | Access denied versus unusable secret format |
| IAM role | Registered role with correct service trust and limited permissions | Role assumption versus how the temporary credential is used by the target |
| Lambda | Same-account function, invoke permission, synchronous completion within 30 seconds | Invocation/timeout versus invalid returned credential |

The Lambda input includes `pentest_arn` and `actor_identifier`. Login instructions explain the returned credential's application use. The following original function illustrates the response boundary only; it is not a deployable credential provider and deliberately contains no real secret. [SS09]

```python
def handler(event, context):
    required = ("pentest_arn", "actor_identifier")
    if not all(event.get(k) for k in required):
        raise ValueError("Missing assessment identity")
    # Retrieve or mint a scoped TEST credential using your approved backend.
    # Return its actual fields in the format explained by the login prompt.
    raise NotImplementedError("Connect an authorized test-credential backend")
```

Use the official trust/policy examples for the selected strategy, restricted to the actual account, space and resource. This snippet is a contract example, not proof that a particular output schema is universal. [SS09]

The newer authentication guide includes TOTP and email MFA. Email MFA uses a generated forwarding address associated with the test credential; it is not general permission to forward a real user's inbox. SMS, push and hardware-key flows are not supported in the reviewed guidance. Older cached text says email MFA is unsupported; the newer indexed page is used here. [SS09]

**Proposed verification:** inspect both credential-test status and the authenticated application's identity/role. Test an intended protected route and an excluded route using approved test data. When access fails, capture which stage failed: source access, credential generation, login navigation, MFA, or authorization inside the application.

<!-- mechanism-review:start S-M01 -->

#### MX-S-AUTH — Credential resolution and application login

Authentication has two stages: retrieve or obtain the credential, then apply it to the application. Secrets Manager or Lambda can succeed while application login fails. The credential name therefore needs to remain associated with the role and protected paths actually reached. [SS403]

The login instructions describe how to apply the returned value, not how to bypass an inaccessible identity provider. Use the credential mechanisms currently exposed in the test configuration; older and newer retrieved documentation differ on some authentication options. Do not treat that difference as evidence that every deployed interface supports the same flow. [SS403]

**Inputs.** Credential strategy, permitted source resource, access URL, application login instructions and representative test identity.

**Configuration**

1. **Strategy — Credential source.** Choose direct input or a documented AWS-native strategy in the test credential configuration.
2. **Permissions — Resource-resolution authority.** For Secrets Manager, scope GetSecretValue and DescribeSecret; for Lambda, scope InvokeFunction.
3. **Application step — Authenticated surface.** Provide access URL and login instructions; verify the resulting identity before interpreting findings.

[SS403]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Credential source configured | Resolve credential | Credential value is obtained or resolution fails. |
| Credential resolved | Navigate/apply login | Application session succeeds or login fails. |
| Credential rotated or login changed | Repeat authentication verification | Source success does not establish current application access. |

**Constraints.** The credential guide requires same-account Secrets Manager/Lambda resources and a credential Lambda completing within 30 seconds. Never place secrets in the documentation examples.

**Inspection points.** Resolution and login evidence plus actual application role; secret contents are not required in retained review evidence.

**Implementation limits.** The documentation does not establish one universal authentication policy, retry algorithm or credential-refresh behavior for all applications.

**Verification procedure (proposed)**

1. Use a disposable customer-role account and a known protected staging route.
2. Record resolution success and the actual role reaching the route.
3. Use an expired test credential: distinguish source-read success from failed login.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS403] | Use advanced setting; Configure multiple credentials | Resource retrieval and application login are separate; strategy-specific permissions and limits apply. |

<!-- mechanism-review:end S-M01 -->

### S-M02 — Login-workflow retention and reuse

Repeated authentication can reuse a procedure learned from an earlier successful login. This retained procedure concerns navigation through the login flow, not a standing proof that every later run reached the same application role. The role and protected routes remain part of assessment evidence.

The first successful authentication navigation can produce a skill describing the login workflow. Later sessions within the run and subsequent runs reuse it. This is learned procedural navigation, not a general incident-memory store or customer-controlled model retraining. [SS09]

**Enablement:** add at least one credential, open **Additional configuration → Login optimization**, and inspect the default-enabled toggle. Disabling reuse preserves the skill; re-enabling permits reuse again. The documentation describes adaptation to changed login flows, but does not disclose a general selection algorithm or promise a particular speed improvement. [SS09]

**Proposed test:** use a staging login flow that the team controls. Retain first-login and later-login evidence, then make an authorized change to the test flow. Verify the actual authenticated role on every run. Without observable reuse evidence, distinguish a successful login from a proven reuse of the learned procedure.

<!-- mechanism-review:start S-M02 -->

#### MX-S-LOGIN — Successful login-procedure reuse

Successful navigation produces a reusable login procedure. Later login sessions can read that procedure instead of rediscovering the path. Reuse concerns navigation; it does not establish that an old credential remains valid or that the application still assigns the intended role. [SS403]

This is separate from finding personalization and vulnerability revalidation. A changed login flow calls for a fresh authentication check, while a changed vulnerability calls for assessment or revalidation. Switching off reuse is not a documented deletion of learned material. [SS403]

**Inputs.** Configured test credentials, a successfully discovered login flow and the Login Optimization setting.

![Successful login-procedure reuse: state and control paths](../assets/diagrams/mechanism-security-learning.svg)

**Configuration**

1. **Prerequisite — Procedure-production input.** Configure a credential and complete a successful login.
2. **Reuse — Reuse control.** Inspect Login Optimization in the penetration-test configuration; the documentation identifies it as enabled by default.
3. **Verification — Coverage prerequisite.** On later sessions, verify authenticated identity independently from any observable reuse.

[SS403]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| No successful login procedure | Successful navigation | A reusable skill file is produced. |
| Procedure retained; reuse enabled | Later login | Saved navigation can be applied. |
| Reuse disabled | Later login | Reuse stops; retained learning is preserved. |
| Reuse re-enabled | Later login | Retained procedure becomes applicable again. |

**Constraints.** Test current credentials and role on each relevant run. Retained navigation is not a general-purpose incident memory.

**Inspection points.** Authenticated session and, where exposed, evidence of reuse. Do not infer reuse solely from faster execution.

**Implementation limits.** No independent public CRUD API or guaranteed invalidation policy for the saved login skill is established.

**Verification procedure (proposed)**

1. Use an authorized multistep staging login.
2. Compare first and later logins while verifying the same application role.
3. Change the login form; failure to reach the protected route remains a coverage gap.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS403] | Login Optimization | Successful navigation produces a skill reused in later sessions/runs; disabling reuse preserves learning. |

<!-- mechanism-review:end S-M02 -->

### S-M03 — Requirement applicability and evaluation

Security criteria are useful only when their applicability is explicit. A rule about authorization of account-owned invoices should not be evaluated as though it governed every public handler. Requirement packs provide the criteria, while an eligible assessment supplies the evidence against which they are evaluated.

A requirement contains a name/description, applicability, compliance criteria and optional remediation guidance. Applicability can distinguish a violation from a case to which the requirement does not apply. Packs group requirements; managed and custom packs differ in editability. Enabled packs inform subsequent eligible reviews, not retroactive rewrites of completed results. [SS14]

**Procedure:** open **Security requirements**, select or create the pack, review applicability and criteria, enable it, and configure the design/code review to evaluate requirements. A vulnerability-only review is not the same evaluation mode. Inspect findings against the selected requirement, not merely the total count. [SS14] [SS05]

**Original example:** require an authorization check before returning an account-owned invoice. Applicability: handlers returning account-owned invoices. Compliance: the authenticated principal must be authorized for the invoice's owning account. A public static-document handler is inapplicable, not automatically compliant with an invoice rule. Test all three cases: compliant, violating and inapplicable.

<!-- mechanism-review:start S-M03 -->

#### MX-S-CRITERIA — Requirement applicability and evaluation

Requirement evaluation first needs a criterion that applies to the subject. The compliance assessment then compares the supplied evidence with that criterion. Missing evidence is not the same as a demonstrated violation or an inapplicable requirement. [SS408] [SS412]

Packs are shared policy configuration. Enabling, disabling or editing one affects future eligible reviews, not the historical conclusions of reviews already completed. This shared reach makes requirement maintenance a cross-application change. [SS408] [SS412]

**Inputs.** Enabled pack, requirement applicability/compliance definitions and eligible source/design review evidence.

**Configuration**

1. **Define — Evaluation rule.** Security requirements → chosen pack → inspect applicability, compliance criteria and optional remediation guidance.
2. **Enable — Future assessment behavior.** Enable the reviewed pack and select requirement evaluation in the eligible review mode.
3. **Inspect — Criterion-level evidence.** Review the stated reason for applicability and result.

[SS408] [SS412]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Pack disabled | Enable | Criteria apply to new eligible reviews. |
| Requirement edited | Start new review | Updated criteria apply prospectively. |
| Existing result | Pack changed | Historical review is not rewritten. |

**Constraints.** Framework labels and managed packs are not compliance certification; applicability is part of the evaluated claim.

**Inspection points.** Requirement-linked result and explanation, including missing-data or inapplicable distinctions where exposed.

**Implementation limits.** Full semantic evaluation rules and a deterministic false-positive/false-negative guarantee are not documented.

**Verification procedure (proposed)**

1. Prepare compliant, violating and deliberately inapplicable examples for one requirement.
2. Check applicability before the compliance verdict.
3. Remove decisive design evidence; require an insufficient-evidence interpretation, not assumed compliance.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS408] | Overview; Enable or disable a pack | Enabled packs govern future eligible reviews and have distinct applicability/compliance fields. |
| [SS412] | Understand compliance statuses | Design reviews distinguish Insufficient data and Not applicable from compliance/violation. |

<!-- mechanism-review:end S-M03 -->

### S-M04 — Requirement generation and replacement

Generating criteria from policy documents is an administrative authoring operation. The generated pack needs review because policy language can be ambiguous and because replacement changes what later assessments evaluate. It is separate from evaluating a codebase against an already approved pack.

Generating requirements from uploaded documents is a separate administrative mechanism. Supported input includes DOC, DOCX, Markdown, PDF and text. Select a custom pack, upload policy material, generate, inspect and edit the result, then enable it. [SS15]

Uploading new documents regenerates the pack and replaces existing requirements, including manually added ones. It is not an append operation. Do not start a competing upload while generation is running. Keep the governing policy and reviewed requirement source in Git; inspect the replacement before enabling it. A framework pack is not a compliance certificate. [SS15] [SS14]

<!-- mechanism-review:start S-M04 -->

#### MX-S-GENERATE — Requirement-pack regeneration

Generation reads policy documents and constructs structured requirements. Running it again for an existing pack replaces the requirements; it is not an append operation. A successful generation therefore establishes a proposed replacement, not approval of every generated rule. [SS409]

Reconcile overlapping policies before submission. Review applicability and technical criteria afterward, and explicitly compare the replacement with any manual entries that existed before the upload. [SS409]

**Inputs.** Documents submitted for a custom requirement pack. The team reviews the policy source and replacement before enabling the pack.

**Configuration**

1. **Select — Replacement target.** Security requirements → Custom packs → choose/create the intended pack.
2. **Generate — Generation operation.** Upload supported documents and choose Generate requirements; acknowledge replacement when applicable.
3. **Accept — Team approval of generated criteria.** Review/edit resulting requirements before enabling the pack for later assessments.

[SS409]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Pack has requirements | Regenerate from new documents | Existing requirements, including manual ones, are replaced. |
| Generation in progress | Attempt another upload | The documented workflow blocks another upload until processing finishes. |
| Generated criteria | Review and enable | New eligible reviews use the accepted configuration. |

**Constraints.** Keep authoritative policy and reviewed configuration in Git; do not treat a generated pack as the only source of policy.

**Inspection points.** Generated requirement definitions and prospective pack state.

**Implementation limits.** Automatic merge of old/manual rules and transactional rollback are not documented.

**Verification procedure (proposed)**

1. Use a disposable pack containing one manual rule and an approved small policy fixture.
2. Compare resulting criteria with source and prior contents.
3. Confirm replacement behavior without using a production policy pack.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS409] | Generate requirements; Replace requirements with a new upload | Generation replaces existing pack contents and requires review before use. |

<!-- mechanism-review:end S-M04 -->

### S-M06 — Encryption keys, identities, and access

Encryption controls concern both key material and the identity requesting access. A valid key selected in a console is not sufficient when the relevant runtime or asynchronous identity lacks the required permission. The documented hierarchy explains which object each key protects and which policy path to inspect.

The documented hierarchy uses a customer KMS key to protect a resource-specific branch key held in a service-managed DynamoDB store. The keyring derives wrapping keys used to protect data-encryption keys. Branch-key rotation and rotation of the KMS key are separate processes; old key versions remain necessary to decrypt older data. [SS18]

Resource-specific encryption context and identity determine authorization. The relevant actors are not interchangeable:

| Actor/path | Permission responsibility |
|---|---|
| Administrator using console | Caller permissions for configuration and forwarded operations |
| Web-app access role | Supported web-app data access |
| Assessment service role | Customer resources such as S3, secrets and logs |
| Service principal / asynchronous workflow | Service-managed background access as documented |

**Configuration procedure:** select a supported enabled symmetric key, apply the current role/service-principal policy statements with the documented resource and encryption-context conditions, and choose the key when creating the supported resource. An application default can be overridden by an explicit resource key; changing the default does not re-encrypt existing resources. Review the current example policies rather than granting all KMS actions to all four identities. [SS18]

**Failure diagnosis:** identify the calling identity and denied KMS action from authorized audit evidence; inspect the matching key policy, grants/role policy and encryption context. Re-enabling a deliberately disabled test key can restore access; deletion can make retained data permanently unavailable. Do not disable a production key merely to demonstrate this mechanism. [SS18]

## 04. Assessment and finding workflows

A run produces findings under particular conditions. Proposed changes, deployed revisions, and subsequent verification remain linked but distinct steps in the engineering workflow.

### S-04 — Assessment configuration and run lifecycle

A saved configuration describes how an assessment should run; a run describes what happened under those settings at a particular time. Reuse saves setup effort but does not freeze the target application, source revision, or credentials. Those inputs still need to be identified for each execution.

A penetration-test configuration can be saved as a draft and completed through wizard steps for details, VPC, credentials, network and additional settings. It is reusable. A run is a separate execution against the then-current configuration and target. **Create** and **Create and execute** are not equivalent actions. [SS08]

Select sources and branch context deliberately: a latest repository branch is not necessarily the deployed revision. For private testing, configure approved network access and optional CloudWatch logging. For repeated tests, inspect the supported scheduling setup and associated Scheduler role rather than assuming that an external cron trigger is the only path. Complete schedule administration is linked to AWS rather than reproduced here. [SS07] [SS08]

Task-hours aggregate work across concurrent tasks; they are not wall-clock duration. The run's configured spending/work limit, account quota and any schedule are different controls. A run reaching its task-hour limit can complete without establishing exhaustive application coverage. Consult pricing before execution; cancelling does not erase work already performed. [SS08] [SS10] [SS11]

**Engineering run record:** capture the configuration ID, target revision, authenticated roles, exclusions, run ID, configured limit, start/end times and incomplete areas. Inspect findings and execution/log evidence while the run operates. Stop on unexpected effects; preserve an incomplete outcome rather than relabeling it a pass. These recordkeeping recommendations do not add product-level guarantees.

<!-- mechanism-review:start S-04 -->

#### MX-S-RUN — Saved assessment and independent execution

A saved penetration-test configuration is reusable; each execution has its own record and findings. Saving the configuration does not freeze a deployment that continues to change. Identify the deployed revision and current credentials for every run. [SS404] [SS418]

Execution begins with prerequisite checks before assessment work. A preflight failure is neither a successful clean assessment nor evidence that the target contains no vulnerabilities. The assessment record should retain incomplete areas along with findings. [SS404] [SS418]

**Inputs.** Saved penetration-test configuration, current target deployment, credentials, exclusions and execution/work limit.

**Configuration**

1. **Define — Reusable configuration.** Penetration tests → create: configure target, role, credentials, network and source context.
2. **Save or start — Definition versus run.** Choose the supported save-only or create-and-execute action.
3. **Inspect — Execution evidence.** Open the run overview, preflight/logs and findings.

[SS404] [SS418]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Configuration saved | Start execution | An independent run is created. |
| Preflight fails | Resolve prerequisite and start a new run | No successful runtime coverage is established. |
| Run completes | Review findings and coverage | Further execution uses a new run, not rewritten evidence. |

**Constraints.** Work limits, test scope and owner authorization must remain explicit; budget limits do not guarantee a particular coverage level.

**Inspection points.** Run identity, actual target context, logs, discovered/tested endpoints and findings.

**Implementation limits.** The documented interface does not expose the complete assessment-planning or vulnerability-discovery algorithm.

**Verification procedure (proposed)**

1. Use a deliberately limited staging target and record its deployed revision.
2. Inspect actual reached paths and completed phases.
3. Make a required target unreachable; require a preflight failure or explicit coverage gap.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS404] | Penetration testing: reusable configurations with independent executions | One configuration supports separate runs and new findings. |
| [SS418] | Create and execute; Review findings | Saving, executing and preflight outcomes are different stages. |

<!-- mechanism-review:end S-04 -->

### S-05 — Finding review and code remediation

A finding begins an engineering decision rather than ending it. Its evidence identifies the affected behavior or code, a proposed repair changes a revision, and deployment makes that revision available to a later test. Linking these objects prevents an unmerged patch from being recorded as a resolved application defect.

A finding identifies the issue and its supporting evidence in a particular assessment context. The review surface can expose description, code locations, evidence and a suggested fix. Configured remediation can produce a patch or pull request, with provider-specific behavior. For example, the reviewed GitHub path distinguishes private-repository pull requests from a downloadable diff for public repositories. [SS05] [SS12]

**Procedure:** select a material finding, verify the affected source and target revision, inspect reproduction or code evidence, request remediation only when the repository path is configured, then review and test the proposed change through the normal engineering process. A generated patch is neither deployment nor revalidation. [SS12]

**Engineering verification:** before closure, identify the exact deployed revision and re-run relevant regression tests. Retain rejected changes and failed builds as unfinished work. Use the finding ID as the link between assessment, change, deployment and revalidation—not similarity of issue titles.

<!-- mechanism-review:start S-05 -->

#### MX-S-FINDING — Finding evidence inspection

A finding combines an observation with an interpretation of risk. Inspect the supporting request, response or source evidence before accepting that interpretation. The findings view can hide unverified items, so the visible count depends on the active filter. [SS405]

Editing a finding changes its recorded attributes; it does not repair the application. The separately documented Findings Personalization mechanism can also influence later similar findings. Read the original and latest values when determining whether a change reflects new vulnerability evidence or a revised organizational preference. [SS405]

**Inputs.** Finding identifier, current/original attributes, validation evidence, assessment revision and application-owner context.

**Configuration**

1. **Inspect — Evidence and affected context.** Completed/in-progress run → Findings → select finding and trace its actions/logs.
2. **Visibility — Display scope.** Review the unverified-findings filter before counting results.
3. **Disposition — Human decision versus generated attributes.** Review current and original values where edits exist.

[SS405]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Finding observed | Inspect evidence | Confidence and supported impact can be assessed. |
| Finding edited | Save current values | Latest attributes change; original view remains available. |
| Repair proposed | Review/deploy/verify separately | An edited status does not establish deployed remediation. |

**Constraints.** Generated reproduction scripts require review and an authorized target before execution. Finding counts and severity alone do not establish risk or coverage.

**Inspection points.** Finding identity, supporting evidence, original/latest values and a reviewer disposition.

**Implementation limits.** No calibrated probability interpretation of confidence or exhaustive false-negative rate is established.

**Verification procedure (proposed)**

1. Use the synthetic authorization-finding fixture for a tabletop.
2. Trace the claim to the supplied identity, request and affected revision.
3. Hide/unhide unverified findings and verify that changed visibility is not reported as remediation.

**Related mechanism.** [MX-S-PERSONALIZE](../catalog/mechanisms.html#MX-S-PERSONALIZE): conditional — Findings Personalization was enabled at test start and eligible edits are available; it changes finding attributes, not application state.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS405] | Default confidence filter; Review finding details; View original agent version | Evidence, display filtering and original/latest attributes are distinct review surfaces. |

#### MX-S-FIX — Repository repair proposal

Remediation produces a proposed source change. Current provider guidance describes pull/merge requests for eligible private repositories and a downloadable diff for S3 sources. Older retrieved text describes a narrower provider/public-repository path; do not generalize either wording to unsupported provider writes. [SS406] [SS401]

The proposal remains separate from review, merge, deployment and finding revalidation. Preserve the original finding relationship through those steps, including any linked Jira record. [SS406] [SS401]

**Inputs.** Finding, eligible connected repository or S3 source, configured remediation permission and selected source context.

**Configuration**

1. **Enable — Optional source-write capability.** Enable remediation in the administrative configuration and select the appropriate repositories/source.
2. **Start — Remediation attempt.** From the finding, choose Remediate code or use the configured automatic proposal path.
3. **Review — Team acceptance.** Inspect proposal/diff and its tests before normal deployment.

[SS406] [SS401]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Finding confirmed | Remediation requested | Attempt and proposed change are produced. |
| Proposal created | Engineering review | Accept, revise or reject without implying deployment. |
| Repair deployed | Revalidate finding separately | Test the actual target rather than the branch. |

**Constraints.** Read-only source access does not grant proposal-write permission. A pull request is not an automatically deployed fix.

**Inspection points.** Remediation status, linked proposal/diff and original finding identity.

**Implementation limits.** No universal guarantee of successful repair, regression coverage or automatic deployment is provided.

**Verification procedure (proposed)**

1. Use a known authorized fixture finding and isolated test repository.
2. Inspect intended diff, tests and unrelated changes.
3. A failing build or undeployed merge must keep verification incomplete.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS406] | Start and view code remediation | Current guidance distinguishes private-repository proposals and S3 diffs. |
| [SS401] | Write actions are opt-in | Repository writes are separately configured and provider-limited. |

#### MX-S-PERSONALIZE — Finding-edit personalization

Findings Personalization learns eligible edits and applies preferences to similar findings on later runs. It is distinct from discovering vulnerabilities, retaining a login procedure and replaying a finding. Learned changes can alter finding attributes without proving that application behavior changed. [SS405]

Inspect the Personalization changes explanation and original values before interpreting a severity change. For status, the documented learnable signal is marking a finding FALSE_POSITIVE; other status updates are not equivalent learning inputs. [SS405]

**Inputs.** Eligible operator edits in the most recent completed penetration-test run and Findings Personalization enabled when the test starts.

**Configuration**

1. **Enablement — Must be enabled at test start for learning.** Inspect Findings Personalization in the penetration-test configuration; documented default is enabled.
2. **Eligible input — Not arbitrary edits from all historical runs.** Review edits in the most recent completed run.
3. **Inspection — Observed preference application.** Compare original/latest attributes and Personalization changes where shown.

[SS405]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Eligible edited finding | Next applicable run | Similar findings can receive personalized attributes. |
| Later edit | Subsequent learning | Most recent edit replaces the earlier preference. |
| Feature disabled | Run without personalization | Raw agent-produced findings are shown; preferences remain retained. |

**Constraints.** Personalized severity is not evidence of a repaired vulnerability. Disabling the feature is not deleting learned preferences.

**Inspection points.** Original/latest attributes and a Personalization changes explanation on affected findings.

**Implementation limits.** Similarity thresholds, internal preference storage and a public preference CRUD resource are not established by the guide.

**Verification procedure (proposed)**

1. Use a controlled staging finding whose risk context can be changed without modifying the application.
2. Inspect whether a later similar finding exposes the personalization change.
3. Disable personalization; compare raw output without claiming that retained preferences were deleted.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS405] | How personalization learns from your edits; Enable or disable Findings Personalization | Learning uses eligible edits from the most recent completed run; false-positive status is special, and disabling preserves preferences. |

<!-- mechanism-review:end S-05 -->

### S-M05 — Finding revalidation and evidence lineage

Revalidation answers a narrower question than a new assessment: can the selected existing finding still be reproduced under the current test configuration? It preserves the original finding and creates a new execution record, allowing the team to inspect what changed between observations.

After a repair reaches the original test environment, open the completed penetration-test run, choose **Multiselect findings for revalidation**, select findings, and choose **Revalidate findings**. The service starts a separate job using current authentication/configuration and repeats the selected validation steps. It does not conduct broad new discovery. [SS13]

The original finding is preserved and linked to the new job. A non-reproduction result is scoped to that finding and execution conditions. An authentication or environment failure can undermine its interpretation; inspect reachability before treating a result as evidence of repair. [SS13]

<!-- mechanism-review:start S-M05 -->

#### MX-S-REVALIDATE — Selected finding replay and lineage

Revalidation repeats validation steps for selected existing findings and creates a separate job. The original finding remains available and the result links back to it. This is targeted replay, not new vulnerability discovery. [SS407]

An Active result means reproduction succeeded. Resolved means the service could not reproduce the issue during this replay. The engineering review must still confirm that the intended identity and path were reached; a failed login cannot demonstrate a repaired authorization check. [SS407]

**Inputs.** Completed test findings, deployed repair on the original target and current authentication configuration.

![Selected finding replay and lineage: state and control paths](../assets/diagrams/mechanism-security-replay.svg)

**Configuration**

1. **Prepare — Current target state.** Deploy the reviewed repair to the environment originally tested.
2. **Select — Selected replay scope.** Completed run → Multiselect findings for revalidation → select findings → Revalidate findings.
3. **Inspect — Evidence lineage.** Open the job, original finding and revalidation history.

[SS407]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Original finding | Start revalidation | Separate job created. |
| Validation reproduced | Active result | Further remediation remains necessary. |
| Validation not reproduced | Resolved result | Interpret within reached identity and scope. |
| Another repair deployed | Repeat selected replay | A further linked job records a new attempt. |

**Constraints.** Full assessments remain necessary for broader changes; replay does not certify whole-application security.

**Inspection points.** Linked job and per-finding replay result; linked Jira issues can receive result comments.

**Implementation limits.** No exactly-once callback or universal guarantee distinguishing every environmental failure from non-reproduction is established.

**Verification procedure (proposed)**

1. Use a deployed repair with a known test identity and retained original finding.
2. Check the reached identity and link to the replay result.
3. Break authentication in a controlled test; record verification as inconclusive rather than celebrating non-reproduction.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS407] | Select findings; Interpret results; Trace history | Replay has separate job identity, selected scope and preserved original finding. |

<!-- mechanism-review:end S-M05 -->

### S-06 — Code review, design review, and threat modeling

Code, design, and threat-model reviews examine different representations of an application. Their inputs and resource lifecycles therefore differ. Source analysis should identify the exact revision; design review should identify the document being reviewed; threat modeling should establish the intended system boundary before assessing individual threats.

| Assessment | Configuration and execution | Reviewable result |
|---|---|---|
| Code review | Connect sources, select vulnerability/requirement modes, start full review or configure supported repository events | Locations, evidence, suggested fixes; preflight failures remain separate |
| Design review | Submit a design for a one-off assessment; clone to create a new review | Design findings against relevant requirements |
| Threat model | Create a reusable definition with scope documents and source context, then start a run | System overview, boundaries, data flows and threats |

Code review preflight checks source and execution prerequisites before analysis. Ready-for-review repository events differ from draft changes; inspect the actual provider and configured trigger. Threat-model scope documents define what to analyze, while source documents/code provide system context. Do not treat them as interchangeable fields. [SS03] [SS05] [SS16] [SS17]

**Threat-model procedure:** in the web app, create the model, provide title, scope documents, sources and service role, optionally configure logs, save, then start a run. Review the inferred system model before relying on individual threats. Inspect severity, evidence and dispositions. A model generated from the wrong system boundary is not repaired merely by dismissing inconvenient threats. [SS16]

The full pipeline integration, complete design-review walkthrough and provider-specific remediation matrix are linked coverage, not reproduced procedures in this edition. This is an explicit limit of the guide, not a claim that those functions are absent.

<!-- mechanism-review:start S-06 -->

#### MX-S-CODE — Full-source or change-focused code assessment

Full-source and change-focused reviews use related analysis but different evidence boundaries. Preflight must first obtain the source and prepare the environment. A failure at that stage is not a clean scan. [SS410] [SS411]

Repository-event settings and optional comments are distinct from a manually started full review. The documented filtering file is read from the repository main branch, so changing it only in an unmerged branch may not change the current review behavior. [SS410] [SS411]

**Inputs.** Exact source revision, full/differential scope, selected review modes, enabled requirements and source-access role.

**Configuration**

1. **Full review — Saved source assessment.** Web app → Code reviews → create: select sources and role; Start review.
2. **Modes — Analysis criteria.** Select vulnerability findings, requirement evaluation or both.
3. **Change guidance — Change scope and filtering.** Review supported provider triggers and .awssecurityagent/filtering.md on the main branch.

[SS410] [SS411]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Review requested | Preflight | Source/environment prerequisites checked. |
| Preflight fails | Fix access and start a new run | Static analysis has not completed. |
| Source revision changes | Supported new review/reanalysis | Prior findings remain revision-specific. |

**Constraints.** Read analysis, posted comments and proposed repairs are different effects. Excluded source is unassessed, not verified safe.

**Inspection points.** Preflight results, reviewed revision, findings and any configured provider comments.

**Implementation limits.** No complete vulnerability-discovery algorithm or exhaustive language/framework coverage is inferred from a successful run.

**Verification procedure (proposed)**

1. Review a known source fixture with exact commit identity.
2. Check that findings reference the expected revision and modes.
3. Deny source access or exclude a known fixture path; retain the resulting assessment gap.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS410] | Create and run a code review; Review findings | Source preflight precedes analysis and has inspectable failure outcomes. |
| [SS411] | How code review works; Filtering findings | Change-trigger and main-branch filtering behavior are distinct configuration paths. |

#### MX-S-DESIGN — Point-in-time design assessment

Design review evaluates a submitted description of the system. It does not observe whether the deployed implementation actually enforces that description. The review must distinguish a requirement violation from missing design evidence. [SS404] [SS412]

Its lifecycle is one-off rather than a reusable test configuration. Clone or create a new review for revised material so the earlier result remains attributable to its original documents. [SS404] [SS412]

**Inputs.** Current design documents, application context and enabled security criteria.

**Configuration**

1. **Submit — Point-in-time subject.** Select the design-review workflow and current design material.
2. **Inspect — Criteria and evidence.** Open findings by requirement and read the compliance explanation.
3. **Revise — Independent later assessment.** Clone/create a new review with updated material.

[SS404] [SS412]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Design submitted | Review | Requirement-level findings produced. |
| Evidence insufficient | Add the missing design information | Prepare a new assessment, not a fabricated pass. |
| Design revised | Clone/new review | New point-in-time result; original review remains separate. |

**Constraints.** Design compliance is not implementation verification.

**Inspection points.** Reviewed files, requirement result and explanation.

**Implementation limits.** Automatic refresh of existing design reviews and continuous synchronized system models are not documented.

**Verification procedure (proposed)**

1. Use a design fixture with an explicit identity boundary and one omitted control.
2. Verify the difference between violation and insufficient evidence.
3. Revise the document without rerunning; the old result must not be presented as a new assessment.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS404] | Key differences between security capabilities | Design reviews have a different one-off lifecycle. |
| [SS412] | Understand statuses; Next steps | Missing evidence and non-compliance differ; cloning creates a new review. |

#### MX-S-THREAT — System-model construction and threat analysis

Scope documents express what should be modeled; source code supplies context for the current system. The output includes a system overview and threats derived for that representation. Review the system boundary and flows before accepting the threats built on them. [SS413]

A model of the wrong system can produce plausible but irrelevant threats. Correct the scope or source mismatch and run again rather than dismissing every downstream item individually. [SS413]

**Inputs.** Scope documents, selected sources or both, application boundary and service role.

**Configuration**

1. **Create — Reusable model configuration.** Threat models → Create threat model: title, scope documents and/or sources, service role and optional log group.
2. **Execute — Independent run.** Start run; inspect Preflight and Logs.
3. **Review — System representation and threat records.** Inspect Overview before Threats; review evidence and recommendations.

[SS413]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Configuration saved | Start run | Preflight and analysis create a system model. |
| Model produced | Review boundaries and threats | Accept, resolve or dismiss findings with rationale. |
| Scope changes | Rerun with corrected input | New result reflects the intended subject. |

**Constraints.** Inferred relationships require owner review; threat status is not proof that a mitigation is deployed.

**Inspection points.** System overview, threat statements, classifications, evidence and recommendations.

**Implementation limits.** The exhaustive threat-generation strategy and completeness of inferred flows are not published.

**Verification procedure (proposed)**

1. Provide a small design with a known trust boundary and supporting source.
2. Check that the overview reflects the known boundary.
3. Use a deliberately stale scope document; identify the mismatch before interpreting threat counts.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS413] | Create and run a threat model; Review threats | Scope documents and source context have distinct roles; overview and threats are reviewable. |

#### MX-S-PIPELINE — Pipeline invocation and result observation

The pipeline step starts and observes a server-side test of a deployed change. It does not create the application or replace the saved assessment scope, and it does not run the penetration-testing engine inside the delivery runner. [SS414]

Configure the release decision before enabling the integration. Invocation failure, unfinished assessment and a completed result above the selected severity threshold need distinct handling. This decision policy is authored team behavior, not a claim that every pipeline fails closed automatically. [SS414]

**Inputs.** Existing penetration-test configuration with CI/CD mode, source connection, pipeline OIDC identity and deployed change identifiers.

**Configuration**

1. **Prerequisite — Existing assessment definition.** Verify target and create a test with current credentials/network scope; enable CI/CD mode and record space/test IDs.
2. **Identity — Short-lived pipeline authentication.** Configure the provider-specific OIDC path and supported integration step.
3. **Decision — Team promotion policy.** Set accepted threshold and explicit behavior for missing/incomplete results.

[SS414]

**Lifecycle and operator actions**

| Initial condition | Operation or event | Result |
|---|---|---|
| Deployment completed | Authorized integration step | Server-side assessment job starts. |
| Job running | Pipeline waits/observes | Runner completion is not yet assessment completion. |
| Job result available | Apply declared gate | Promote, block or escalate using that result and revision. |

**Constraints.** This preview path is post-deployment assessment, not pull-request static analysis.

**Inspection points.** Pipeline execution, deployed change, assessment job and applied promotion decision.

**Implementation limits.** Exactly-once invocation, universal timeout behavior and identical provider semantics are not established.

**Verification procedure (proposed)**

1. Use a non-production pipeline with known deployed revision and saved assessment.
2. Retain the server job ID with the gate result.
3. Simulate unavailable/incomplete result; follow the declared blocking/escalation rule rather than passing silently.

**Source mapping**

| Reference | Documentation section | Supported behavior |
|---|---|---|
| [SS414] | Before you start; Post-deployment gate | The integration invokes an existing configured test, uses OIDC and observes server-side work. |

<!-- mechanism-review:end S-06 -->

## 05. Applying the model to operational outcomes

Trace the approved use cases through their concrete configuration and execution objects, then examine the prepared evidence. The examples remain synthetic, not live AWS results.

### S-11 — Finding lineage from assessment to repair verification

The approved running-application assessment case ends with reviewed findings and known coverage, not with an automatically repaired application. An accepted finding may lead to a code proposal; that proposal must pass the engineering delivery process before its effect can be tested. The resource model keeps the original finding, remediation attempt, external change and later verification separate so the result can be traced through that sequence. [SS54] [SS55]

![Finding, repair and revalidation lineage](../assets/diagrams/er-security-lineage.svg)

In [UC-S01, assess a running application](../catalog/index.html#UC-S01), public or private reachability and authentication are configuration dimensions. They do not create four separate assessment objectives. The configuration selects the authorized surface, while the run records what was reached. Login Optimization can reuse a successful navigation procedure; the operator must still inspect the current role and reachability when interpreting coverage. [SS52] [SS56]

In [UC-S06, prepare a code-remediation proposal](../catalog/index.html#UC-S06), source and remediation settings determine where eligible proposal work can occur. The remediation attempt and its output are not the same object: an attempt may fail, and a produced patch or pull request remains an external engineering artifact. Its review, test and deployment records belong to the delivery process. The guide does not infer deployment authority from permission to create a proposal. [SS55]

In [UC-S07, revalidate a finding](../catalog/index.html#UC-S07), the operator selects one or more existing findings after deploying the repair to the original authorized environment. A separate job repeats the selected validation steps using current configuration and authentication. The original finding remains linked to the revalidation history. This is scoped retesting, not new broad vulnerability discovery. [SS54]

The blue Finding-to-revalidation result node is introduced by this documentation. It records the relationship between an original finding and a particular revalidation job, including the observed disposition and any incomplete evidence. It is useful because one finding can be retested repeatedly and one job can select several findings. The model does not claim that AWS exposes a separate API resource with that name. A pending or failed job may not yet have a conclusive result.

| Transition | Identity to preserve | Acceptance question |
|---|---|---|
| Configuration to assessment | Test configuration, run, target revision and role | Was the intended surface actually assessed? |
| Finding to proposal | Original finding and proposed source revision | Does the change address the evidenced issue without unrelated changes? |
| Proposal to deployment | Reviewed change and deployed revision | Did the accepted repair reach the test environment? |
| Finding to revalidation job | Original finding and new job | Were the selected validation steps reached under the intended identity? |
| Result to work tracking | Finding link and external issue key | Does the ticket describe the observed result rather than only completion status? |

These acceptance questions are authored engineering procedure. AWS documents the assessment, proposal and revalidation operations; the team decides whether the evidence is sufficient to accept the outcome. A linked Jira issue is another external record with its own audience and lifecycle. Removing the integration does not erase the previously published finding details. [SS54] [SS58]

### S-U01 — Authorization-finding remediation: worked example

**Synthetic, authorized-staging exercise.** Two test users belong to different customer accounts. The illustrative finding is that user A can receive a test invoice owned by account B. No live endpoint, credential or exploit execution is supplied.

| Evidence record | Before repair | Candidate repair | After deployment |
|---|---|---|---|
| Application revision | `demo-r1` | `demo-r2` under review | `demo-r2` deployed |
| Same-account test | Expected invoice returned | Regression test passes | Expected invoice returned |
| Cross-account test | Test invoice returned unexpectedly | Ownership check added; unit test passes | Access denied in prepared result |
| Identity evidence | User A / account A | Test principal controlled | User A / account A confirmed |

**Walkthrough:** inspect the original finding and target revision; review the proposed ownership check; verify that the prepared deployment record names `demo-r2`; select the finding for revalidation; inspect the new job and its linkage. The observation that a patch exists is not used as evidence of deployment. The prepared post-deployment denial supports only this tested path and identity.

**Failure branch:** if revalidation instead logs in as a privileged administrator, its result is not the intended test of user A. Correct the credential role and rerun the authorized verification. If no application path was reached, do not interpret the absence of reproduction as proof of repair.

**Expected deliverable:** a finding disposition linking original evidence, reviewed change, deployed revision, actual authenticated identity and targeted result, with untested routes stated explicitly. The fixture teaches evidence lineage; it is not an assessment result or a security guarantee.

## 06. Troubleshooting and operating limits

An incomplete assessment may reflect an inaccessible source, failed authentication, a wrong criterion, or an execution limit. These cases require different corrective actions.

### S-07 — Assessment failures and operating limits

The reviewed quota page distinguishes assessment capacity from spending controls. Examples include five concurrent penetration tests and five concurrent code-review runs as adjustable quotas, plus 20 requirement packs, 30 requirements per pack and 150 enabled requirements per account/Region as fixed limits. Confirm actual quotas and pricing before large-scale execution; a concurrency limit is not a financial budget. [SS10] [SS11]

| Symptom | Likely boundary | Next inspection |
|---|---|---|
| Repository missing | Registration or connection | Account type, installation approval, connected repo and feature setting |
| Credential source denied | Service-role resource access | Correct ARN/account, required read/invoke actions and trust |
| Secret resolves; login fails | Application flow | Access URL, instructions, MFA, identity and credential-test result |
| Private endpoint unreachable | Network | DNS, route/NAT requirements, egress, target rules and VPC configuration |
| Additional domain blocked | Target/access/exclusion rules | Login-derived domains; approve only necessary accessible endpoints |
| No requirement findings | Configuration/applicability | Enabled pack, selected evaluation mode, inapplicable versus compliant |
| New document removed a manual rule | Pack regeneration | Compare generated replacement with the governing Git source |
| Finding not reproduced | Target and authentication | Deployed revision, role reached and revalidation job evidence |
| Encrypted object inaccessible | KMS identity/context | Relevant role/principal, key state, action and context conditions |

This ordering is engineering guidance derived from the cited procedures. It does not claim that every error message has one unique cause. [SS06] [SS09] [SS18]

## 07. Documentation coverage

The source register separates documented product behavior from authored engineering examples and identifies linked procedures.

### S-08 — Documentation coverage and references

The assessment chapters connect application sources, target access, criteria, executions, and finding verification. The following coverage table identifies which procedures are explained and which require the provider-specific official guide. Availability belongs to an individual assessment or integration feature, not to the collection as a whole.

The source register supports product behavior rather than the synthetic application example or the team decisions proposed around it. Integration inventories and selected authentication and context mechanisms were rechecked on 22 October 2026; this is not a new exhaustive audit of every historical statement. The diagrams are logical models and do not assert undisclosed runtime internals.

| Official subject | Treatment | Remaining boundary |
|---|---|---|
| Resource lifecycle and identities | Model plus setup sequence | Complete SSO and organization-policy deployment linked |
| Penetration testing | Configuration, target classes, credentials, run interpretation | Full GenAI risk-exception authoring not reproduced |
| Authentication | Strategy matrix, preflight, learned login reuse | No actual secrets or running credential backend |
| Requirements | Evaluation separated from destructive regeneration | Full managed-pack inventory linked |
| Code and threat models | Usable configuration sequence and result model | Complete CI/CD and provider compatibility matrix deferred |
| Findings and KMS | Lineage, remediation boundaries, key hierarchy and actors | Full policy documents remain official reference |
| Limits/troubleshooting | Selected operational constraints and diagnostic paths | Not an exhaustive error catalog |

**Version conflicts:** current indexed authentication/wizard pages include email MFA and nonstandard ports. Older cached authentication/troubleshooting pages contradict those points. The newer task-specific pages are used; the older troubleshooting source supports only the remaining diagnostics. Review date means retrieval, not a page publication date.

#### Official sources and reviewed sections

- [SS01] Service scope and feature distinctions.
- [SS02] Documentation history; feature announcements and availability.
- [SS03] Account versus space resources; configuration/run lifecycle by assessment type.
- [SS04] Administrative and assessment surfaces, application context.
- [SS05] Code-review setup, modes, preflight, full scans and findings.
- [SS06] Source registration and network troubleshooting; stale port restriction excluded.
- [SS07] Target verification, VPC/role/logging setup and optional scheduling; newer indexed content.
- [SS08] Current penetration-test wizard, network classes, credentials and task-hours; newer indexed content.
- [SS09] Credential methods, preflight, login reuse and MFA; newer indexed content resolves older cached text.
- [SS10] Quotas and adjustability; current indexed table.
- [SS11] Pricing versus capacity and cancellation implications.
- [SS12] Remediation provider behavior and proposed patches.
- [SS13] Revalidation initiation, results and lineage.
- [SS14] Requirement fields, applicability, activation and review behavior.
- [SS15] Requirement generation and replacement consequences.
- [SS16] Threat-model scope/source distinction, setup, preflight and result review.
- [SS17] Repository-triggered review and comments.
- [SS18] Hierarchical keyring, identities, encryption context and key lifecycle.

[SS01]: https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html

[SS02]: https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html

[SS03]: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html

[SS04]: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html

[SS05]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html

[SS06]: https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html

[SS07]: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html

[SS08]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html

[SS09]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html

[SS10]: https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html

[SS11]: https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html

[SS12]: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html

[SS13]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html

[SS14]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html

[SS15]: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html

[SS16]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html

[SS17]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html

[SS18]: https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html

[SS30]: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html

[SS31]: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html

[SS32]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html

[SS33]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html

[SS34]: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html

[SS50]: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html

[SS51]: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html

[SS52]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html

[SS53]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html

[SS54]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html

[SS55]: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html

[SS56]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html

[SS57]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html

[SS58]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html

[SS490]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-azure-devops.html
[SS401]: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
[SS402]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
[SS403]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
[SS404]: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
[SS405]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html
[SS406]: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
[SS407]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
[SS408]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
[SS409]: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html
[SS410]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html
[SS411]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html
[SS412]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html
[SS413]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
[SS414]: https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html
[SS415]: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
[SS416]: https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html
[SS417]: https://docs.aws.amazon.com/securityagent/latest/userguide/remove-jira.html
[SS418]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart.html
