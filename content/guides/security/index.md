---
id: guide-security
kind: guide
product: security
title: AWS Security Agent
output: guides/security.html
references:
  SS01: https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html
  SS02: https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html
  SS03: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  SS04: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
  SS05: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html
  SS06: https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html
  SS07: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html
  SS08: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
  SS09: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  SS10: https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html
  SS11: https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html
  SS12: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
  SS13: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
  SS14: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
  SS15: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html
  SS16: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
  SS17: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html
  SS18: https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html
  SS30: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
  SS31: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html
  SS32: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
  SS33: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-confluence.html
  SS34: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
  SS401: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
  SS402: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
  SS403: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  SS404: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  SS405: https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html
  SS406: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
  SS407: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
  SS408: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
  SS409: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html
  SS410: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html
  SS411: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html
  SS412: https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html
  SS413: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
  SS414: https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html
  SS415: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
  SS416: https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html
  SS417: https://docs.aws.amazon.com/securityagent/latest/userguide/remove-jira.html
  SS418: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart.html
  SS490: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-azure-devops.html
  SS50: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  SS501: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  SS502: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
  SS503: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
  SS504: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  SS505: https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html
  SS506: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
  SS507: https://docs.aws.amazon.com/securityagent/latest/userguide/data-protection.html
  SS508: https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html
  SS51: https://docs.aws.amazon.com/securityagent/latest/userguide/about-integrations.html
  SS52: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  SS53: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
  SS54: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
  SS55: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
  SS56: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
  SS57: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
  SS58: https://docs.aws.amazon.com/securityagent/latest/userguide/connect-jira.html
  SS701: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
  SS702: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  SS703: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
---

<!-- block: b-f337fe67f40451de8759 -->
# AWS Security Agent

<!-- block: b-b6ac1918685552f7bd25 -->
Application scope, assessment capabilities, and execution mechanisms

<!-- block: b-1a24fe9c48d451cd9c3d -->
AWS Security Agent exposes application-scoped assessments and the configuration needed to supply source context, criteria, target access, and credentials. Penetration testing, code review, design review, and threat modeling have different configuration and execution lifecycles. They are managed product functions, not interchangeable customer-defined agents. [SS501] [SS502]

<!-- block: b-67e87aa5cfac59eeb76d -->
The guide separates workspace organization, assessment definition, context, invocation, provider integration, network access, execution controls, managed assessment workflows, outputs, and administration. The approved resource model introduces the objects; the use-case catalog explains their application to operational objectives.

<!-- block: b-60b058b84a495ddb9672 -->
**Reading conventions.** These capability dimensions are editorial. The DevOps custom-agent, skill, memory-store, and trigger types are not assumed to exist here. Official sources identify Security Agent's own facilities. DOC/AWS/EXT colors retain the approved ownership convention. Worked examples and verification instructions are team guidance, not executed assessments.

<!-- block: b-659b0e71f5f254219ec2 -->
Start with the agent overview and workflow walkthroughs. Use the subsequent capability chapters for detailed setup, lifecycle behavior and troubleshooting. The use-case catalog remains separate and unchanged.
