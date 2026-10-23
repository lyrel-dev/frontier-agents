---
id: security-integrations
kind: diagram
title: Application-source registration and selection
refs:
- S-09
---

<!-- block: b-0de1b6184a86596e8e42 -->
The account registration authorizes a provider. The application selects resources from it. Sources are shared across eligible assessments, while repository write actions are separately enabled.

<!-- block: b-a0e5e8bcd52d517c8ff9 -->
```dot
rankdir=TB;
providers [label="Provider account\nGitHub, GitLab, Bitbucket, Confluence"];
register [label="Account registration\nAuthorized provider connection"];
resources [label="Agent Space selection\nRepositories or pages"];
read [label="Read context\nEligible assessment inputs"];
write [label="Optional repository writes\nComments or remediation"];
s3 [label="Connected S3 resources\nSelected source objects"];
providers -> register [label="authorize"];
register -> resources [label="select"];
resources -> read [label="shared source context"];
resources -> write [label="separate opt-in",style=dashed];
s3 -> read [label="selected objects"];
```
