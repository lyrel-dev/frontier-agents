---
id: devops-incident
kind: diagram
title: Incident triage and investigation workflow
refs:
- D-06
---

<!-- block: b-714c2c18c94f561b99de -->
A signal can be linked, skipped, or investigated independently. Steering affects the current analysis; completed-investigation feedback supplies a separate corrective input.

<!-- block: b-35791bb52fce5395a750 -->
```dot
rankdir=TB;
signal [label="Incident signal\nIdentity, service, and time"];
triage [label="Triage decision\nCorrelation and skip criteria",shape=diamond];
linked [label="Linked\nExisting primary investigation"];
skipped [label="Skipped\nRecorded criterion and reason"];
new [label="Proceed\nIndependent investigation"];
evidence [label="Investigation\nTool observations and hypotheses"];
operator [label="Operator steering\nAdditional or contrary evidence"];
result [label="Investigation result\nCause and mitigation proposal"];
feedback [label="Completed-run feedback\nVerdict and verified correction"];
signal -> triage;
triage -> linked [label="correlated"];
triage -> skipped [label="criterion matches"];
triage -> new [label="new work"];
new -> evidence;
operator -> evidence [label="steers"];
evidence -> result;
result -> feedback [label="review"];
linked -> new [label="unlink",style=dashed];
skipped -> new [label="unskip",style=dashed];
```
