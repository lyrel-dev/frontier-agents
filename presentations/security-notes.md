# AWS Security Agent: presentation notes



Presentation: 41 minutes, including 8 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. What AWS Security Agent executes

00:00–03:00 · Assessment execution, application scope and context

Start with an application-security question and the kind of evidence that can answer it. Explain the assessment settings, criteria and context before discussing identifiers. A dynamic test needs a running target and identity; source and design reviews use different inputs and effects.



![Security assessment inputs and execution](../assets/diagrams/teaching-security-agent.svg)



Detailed reference: [What AWS Security Agent executes](../guides/security.html#S-90)



Detailed reference: [Assessment definitions and customization](../guides/security.html#S-12)


## 02. How assessment, repair and verification relate

03:00–06:00 · Assessment execution, application scope and context

These are linked work records, not assertions about an undocumented internal multi-agent graph. The team deployment step is external. The original finding remains distinct from the remediation pull request and subsequent revalidation job.



![Assessment, repair and verification are separate work records](../assets/diagrams/teaching-security-coordination.svg)



Detailed reference: [How assessment, remediation and verification are coordinated](../guides/security.html#S-91)



Detailed reference: [Assessment configurations, runs and result identities](../guides/security.html#S-10)



Detailed reference: [Finding revalidation and evidence lineage](../guides/security.html#S-M05)


## 03. Application Agent Spaces and shared requirements

06:00–09:00 · Assessment execution, application scope and context

Do not equate this scope with a DevOps operational Agent Space. The diagram shows selected criteria; it does not place ownership of shared requirement packs inside the application. The detailed resource model specifies which objects are shared and which belong to the application.



![Application scope and shared assessment criteria](../assets/diagrams/teaching-security-space.svg)



Detailed reference: [Application Agent Spaces and shared assessment criteria](../guides/security.html#S-92)



Detailed reference: [Shared configuration, Agent Spaces and assessments](../guides/security.html#S-01)


## 04. Assess an authorized running application

09:00–12:00 · Assessment and finding resolution

Public/private, authenticated/unauthenticated and recurring execution are configuration dimensions of the approved assessment case. Failed authentication cannot establish coverage of authenticated functionality. Explicitly identify the application effects permitted during the test.



![Assess source or an authorized running application](../assets/diagrams/teaching-security-assessment.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Test targets, dependencies, and exclusions](../guides/security.html#S-03)



Detailed reference: [Credential retrieval and application login](../guides/security.html#S-M01)



Detailed reference: [Assessment configuration and run lifecycle](../guides/security.html#S-04)


## 05. Review source code and proposed changes

12:00–15:00 · Assessment and finding resolution

The same context-and-execution diagram now reads source rather than exercising a deployed endpoint. A source finding does not establish exploitability of an unseen deployment. Keep full-source and proposed-change variants explicit.



![Assess source or an authorized running application](../assets/diagrams/teaching-security-assessment.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Code review, design review, and threat modeling](../guides/security.html#S-06)



Detailed reference: [Requirement applicability and evaluation](../guides/security.html#S-M03)


## 06. Triage findings and prepare a remediation proposal

15:00–18:00 · Assessment and finding resolution

Distinguish finding disposition from changing the application. Eligible personalization may alter later finding attributes, but it does not fix the underlying defect. The proposal remains subject to ordinary code-review and release controls.



![Finding triage, repair proposal, deployment and revalidation](../assets/diagrams/teaching-security-repair.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Finding review and code remediation](../guides/security.html#S-05)


## 07. Revalidate a finding after deploying the repair

18:00–21:00 · Assessment and finding resolution

A new revalidation job is associated with the original finding. A non-reproduction result needs the tested target, deployment and identity to be interpretable. It does not constitute a complete new assessment of the application.



![Finding triage, repair proposal, deployment and revalidation](../assets/diagrams/teaching-security-repair.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Finding revalidation and evidence lineage](../guides/security.html#S-M05)


## 08. Exercise: trace a finding to a deployed repair

21:00–29:00 · Assessment and finding resolution

Use the supplied synthetic evidence. Ask participants to identify the record proving deployment and the record proving which identity was used. A finding status update or merged pull request alone cannot answer both questions.



0–2 min | Read the finding | Identify target, revision, test identity and evidence

2–4 min | Inspect the proposal | Separate repository change from deployed version

4–6 min | Check verification conditions | Match deployed revision and revalidation identity

6–8 min | Interpret the result | State tested scope and unresolved coverage


Detailed reference: [Authorization-finding remediation: worked example](../guides/security.html#S-U01)



Detailed reference: [How assessment, remediation and verification are coordinated](../guides/security.html#S-91)


## 09. Design review and application threat modeling

29:00–32:00 · Design, requirements and reusable context

These remain distinct approved cases. Use the same diagram to show the changed inputs and outputs rather than inventing a universal assessment pipeline. Explain why cloning a design review differs from rerunning a threat-model configuration.



![Assess source or an authorized running application](../assets/diagrams/teaching-security-assessment.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Code review, design review, and threat modeling](../guides/security.html#S-06)



Detailed reference: [Assessment configurations, runs and result identities](../guides/security.html#S-10)


## 10. Maintain security requirements and assessment criteria

32:00–35:00 · Design, requirements and reusable context

Requirement consolidation is an engineering objective; pack configuration and evaluation are service facilities supporting it. Separate generation from evaluation. A source-policy approval is a team decision, not a hidden native approval API.



![Criteria, application context and narrowly scoped reuse](../assets/diagrams/teaching-security-context.svg)



Detailed reference: [Assessment and finding-resolution workflows](../guides/security.html#S-93)



Detailed reference: [Requirement applicability and evaluation](../guides/security.html#S-M03)



Detailed reference: [Requirement generation and replacement](../guides/security.html#S-M04)


## 11. Three distinct forms of retained context

35:00–38:00 · Design, requirements and reusable context

Do not label all retained state as the same learning mechanism. Compare producer, consumer, enablement and lifecycle. The learner should know which representation to inspect when a result reflects an obsolete criterion, failed login or inappropriate finding preference.



Representation | What is reused | What it does not establish

Application context | Selected source and application understanding | A universal incident-memory service

Login Optimization | A successful authentication-navigation procedure | Authorization for additional targets or roles

Findings Personalization | Eligible earlier edits applied to similar findings | That a vulnerability was repaired

Requirement pack | Criteria for applicable future code/design reviews | A certification or retrospective change to old findings


Detailed reference: [Application-context construction and reuse](../guides/security.html#S-M07)



Detailed reference: [Login-workflow retention and reuse](../guides/security.html#S-M02)



Detailed reference: [Finding-edit personalization](../guides/security.html#S-13)


## 12. Operational checks and failure boundaries

38:00–41:00 · Design, requirements and reusable context

End with checks that follow from the model, not a generic warning list. Use the guide chapters for provider setup, network paths, IAM, encryption and quotas. Each unresolved prerequisite limits the conclusion that can be drawn from the assessment.



Area | Inspect | Decision

Application scope | Target domains, exclusions and owners | Stop when authorization is unclear

Source identity | Repository or document revision | Reject a conclusion without a traceable subject

Authentication | Resolved credential and actual application role | Do not infer coverage from a retrieved secret

Execution | Configuration, run state and limits | Separate incomplete execution from absence of findings

Verification | Finding, deployed revision and revalidation job | Keep unresolved cases open


Detailed reference: [User access and repository connections](../guides/security.html#S-02)



Detailed reference: [Test targets, dependencies, and exclusions](../guides/security.html#S-03)



Detailed reference: [Assessment failures and operating limits](../guides/security.html#S-07)
