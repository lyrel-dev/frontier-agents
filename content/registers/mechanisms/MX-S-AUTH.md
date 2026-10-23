---
id: record-mechanisms-MX-S-AUTH
kind: record
collection: mechanisms
product: security
title: Credential resolution and application login
order: 16
frozen: true
data:
  id: MX-S-AUTH
  platform: security
  title: Credential resolution and application login
  features:
  - FT-S-AUTH
  sections:
  - S-M01
  trigger: Authenticated assessment
  state: Credential strategy and login instructions
  process:
    $markdown: field-0001
  effect: Authentication requests
  verification: Check the actual application identity and protected route, not only credential retrieval.
  on_failure: Mark protected paths unassessed when login fails.
  review:
    primary_section: S-M01
    kind: Credential-resolution and login mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Strategy
      - $markdown: field-0005
      - Credential source
    - - Permissions
      - $markdown: field-0006
      - Resource-resolution authority
    - - Application step
      - $markdown: field-0007
      - Authenticated surface
    lifecycle:
    - - Credential source configured
      - Resolve credential
      - Credential value is obtained or resolution fails.
    - - Credential resolved
      - Navigate/apply login
      - Application session succeeds or login fails.
    - - Credential rotated or login changed
      - Repeat authentication verification
      - Source success does not establish current application access.
    controls:
      $markdown: field-0008
    observable_output:
      $markdown: field-0009
    undocumented:
      $markdown: field-0010
    test:
    - Use a disposable customer-role account and a known protected staging route.
    - Record resolution success and the actual role reaching the route.
    - 'Use an expired test credential: distinguish source-read success from failed login.'
    claims:
    - source: SS403
      section: Use advanced setting; Configure multiple credentials
      assertion:
        $markdown: field-0011
---

<!-- block: b-e93a61e24f66592db257 -->
## process

<!-- block: b-67624e5561f85a07b5c6 -->
<!-- field: field-0001 -->
Obtain the test credential and apply it to the application.
<!-- /field -->

<!-- block: b-20068e5abbe45bc5a879 -->
## review / inputs

<!-- block: b-17485d09fb665682924c -->
<!-- field: field-0002 -->
Credential strategy, permitted source resource, access URL, application login instructions and representative test identity.
<!-- /field -->

<!-- block: b-b37983c9eb375915bb33 -->
## review / narrative / 0

<!-- block: b-39e3da726cb056c4882b -->
<!-- field: field-0003 -->
Authentication has two stages: retrieve or obtain the credential, then apply it to the application. Secrets Manager or Lambda can succeed while application login fails. The credential name therefore needs to remain associated with the role and protected paths actually reached.
<!-- /field -->

<!-- block: b-2b993f8bdebb5304970a -->
## review / narrative / 1

<!-- block: b-d4730d64d7a55d3bb199 -->
<!-- field: field-0004 -->
The login instructions describe how to apply the returned value, not how to bypass an inaccessible identity provider. Use the credential mechanisms currently exposed in the test configuration; older and newer retrieved documentation differ on some authentication options. Do not treat that difference as evidence that every deployed interface supports the same flow.
<!-- /field -->

<!-- block: b-8b89f0336de256639a32 -->
## review / configuration / 0 / 1

<!-- block: b-f4de127c445253c9aefa -->
<!-- field: field-0005 -->
Choose direct input or a documented AWS-native strategy in the test credential configuration.
<!-- /field -->

<!-- block: b-05ac55d538d65754a550 -->
## review / configuration / 1 / 1

<!-- block: b-8ecc5937852159f58f00 -->
<!-- field: field-0006 -->
For Secrets Manager, scope GetSecretValue and DescribeSecret; for Lambda, scope InvokeFunction.
<!-- /field -->

<!-- block: b-4743d294fa7053ccbe5c -->
## review / configuration / 2 / 1

<!-- block: b-7a2985ddf20d582bab16 -->
<!-- field: field-0007 -->
Provide access URL and login instructions; verify the resulting identity before interpreting findings.
<!-- /field -->

<!-- block: b-3cfbfb0fb930579795d5 -->
## review / controls

<!-- block: b-feae0d5ad2815a44a711 -->
<!-- field: field-0008 -->
The credential guide requires same-account Secrets Manager/Lambda resources and a credential Lambda completing within 30 seconds. Never place secrets in the documentation examples.
<!-- /field -->

<!-- block: b-91de1347928c50e59b84 -->
## review / observable output

<!-- block: b-b5b523d3321b5661abe3 -->
<!-- field: field-0009 -->
Resolution and login evidence plus actual application role; secret contents are not required in retained review evidence.
<!-- /field -->

<!-- block: b-434b593eef6956178e89 -->
## review / undocumented

<!-- block: b-62e48110cb6457959a23 -->
<!-- field: field-0010 -->
The documentation does not establish one universal authentication policy, retry algorithm or credential-refresh behavior for all applications.
<!-- /field -->

<!-- block: b-97c850e27cc85505a7d3 -->
## review / claims / 0 / assertion

<!-- block: b-58375d078a195688bacd -->
<!-- field: field-0011 -->
Resource retrieval and application login are separate; strategy-specific permissions and limits apply.
<!-- /field -->
