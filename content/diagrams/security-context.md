---
id: security-context
kind: diagram
title: Application context and assessment criteria
refs:
- S-M07
- S-M03
---

<!-- block: b-e4bce562badc5bf393d8 -->
Source evidence and scope documents have different jobs. The assessment uses selected evidence and applicable criteria; a finding is an output of that execution rather than an automatically shared memory.

<!-- block: b-28fc9c6e0d43523ab21f -->
```dot
rankdir=TB;
code [label="Implementation evidence\nRepository revision and API material"];
design [label="Design context\nDocuments and connected pages"];
scope [label="Assessment scope\nApplication and system boundary"];
model [label="Selected application context\nSystem components and relationships"];
criteria [label="Applicable requirements\nReviewed criteria"];
assessment [label="Assessment run\nAnalysis or authorized active test"];
finding [label="Finding or model result\nEvidence, assumptions, and limits"];
code -> model;
design -> model;
scope -> model [label="bounds the question"];
model -> assessment [label="context"];
criteria -> assessment [label="eligible evaluation"];
assessment -> finding;
```
