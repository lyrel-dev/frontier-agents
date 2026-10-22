"""Explicit report and presentation chapters.

Canonical guide sections remain unchanged. Use cases are maintained in the
separate structured catalog and are injected into each HTML report.
"""
REVISION = '2026-10-22-use-case-catalog'
BASELINE = '7ed9843ed35f6c78214dd2853df497b670a49995'


def chapter(slug, title, purpose, sections):
    return {'slug': slug, 'title': title, 'purpose': purpose, 'sections': sections.split()}


CHAPTERS = {
    'devops': [
        chapter('model', 'Product Functions and Resource Model', 'Define the built-in functions, configuration objects and execution records before applying them to operational work.', 'D-01'),
        chapter('access', 'Access Roles and Tool Connections', 'Configure operator access, AWS resource access, external tools and private network paths.', 'D-02 D-03 D-04'),
        chapter('knowledge', 'Knowledge, Memory and Operational Procedures', 'Separate discovery, recurring-cause memory, corrections, attachments, instructions and skills.', 'D-05 D-M01 D-M02 D-M07 D-M03 D-M04'),
        chapter('operations', 'Incident Operations and Controlled Execution', 'Trace triage, investigations, custom-agent work, sandbox computation, approvals and configuration updates.', 'D-06 D-07 D-M05 D-M06 D-08 D-09'),
        chapter('example', 'Worked Incident Analysis', 'Use prepared evidence to examine a recurring alarm without assuming the previous cause has returned.', 'D-U01'),
        chapter('diagnosis', 'Troubleshooting, Limits and Failure Modes', 'Locate the first failed prerequisite and distinguish limits from missing access, context or approval.', 'D-10'),
        chapter('evidence', 'Coverage and Source Notes', 'Identify detailed coverage, linked subjects, deferred procedures and source-version qualifications.', 'D-11'),
    ],
    'security': [
        chapter('model', 'Product Functions and Resource Model', 'Define application scope, shared resources, assessment configurations, executions and findings.', 'S-01'),
        chapter('access', 'Identity, Sources and Target Boundaries', 'Configure operator identity, repository sources, target rules and private access.', 'S-02 S-03'),
        chapter('mechanisms', 'Authentication, Criteria and Protection Mechanisms', 'Examine credential resolution, login reuse, requirement evaluation, regeneration and encryption.', 'S-M01 S-M02 S-M03 S-M04 S-M06'),
        chapter('operations', 'Assessment, Remediation and Evidence Lifecycle', 'Follow saved configurations, runs, findings, repairs, revalidation and shift-left assessments.', 'S-04 S-05 S-M05 S-06'),
        chapter('example', 'Worked Finding Revalidation', 'Trace an authorization finding through a deployed repair and prepared revalidation evidence.', 'S-U01'),
        chapter('diagnosis', 'Troubleshooting, Limits and Failure Modes', 'Diagnose the failed access, authentication, criteria, execution or evidence prerequisite.', 'S-07'),
        chapter('evidence', 'Coverage and Source Notes', 'Review coverage decisions, availability boundaries and official sources.', 'S-08'),
    ],
    'finops': [
        chapter('model', 'Product Functions and Resource Model', 'Distinguish the agent instance, access roles, retained context, queued work and outputs.', 'F-01'),
        chapter('access', 'Access Roles, Source Data and Integrations', 'Establish policy responsibilities, data-source dependencies and external destinations.', 'F-02 F-M01 F-05'),
        chapter('context', 'Reference Files, Memory and Conversation Context', 'Separate operator-maintained inputs, cross-session memory and within-session compaction.', 'F-M02 F-M03 F-M04'),
        chapter('operations', 'Tasks, Automations, Publication and Data Lifecycle', 'Trace task creation, event matching, report artifacts, approvals and object-specific removal.', 'F-03 F-M05 F-04 F-M06 F-M07'),
        chapter('example', 'Worked Cost Analysis', 'Reconcile cost components before assessing limited evidence for a causal explanation.', 'F-U01'),
        chapter('diagnosis', 'Troubleshooting, Limits and Failure Modes', 'Test the query, retained context, execution and publication layers separately.', 'F-06'),
        chapter('evidence', 'Coverage and Source Notes', 'Review scope exclusions, preview boundaries and the source-review record.', 'F-07'),
    ],
    'architecture': [
        chapter('models', 'Resource and Context Models', 'Compare the documented objects and retained information without assuming a common runtime.', 'A-01 A-02'),
        chapter('boundaries', 'Connectivity, Identity and Effect Boundaries', 'Separate reachability, authenticated identity and authority to perform an operation.', 'A-03 A-04'),
        chapter('lifecycle', 'Execution Lifecycles and Handoff Records', 'Compare configuration, execution, artifacts and team-composed handoffs.', 'A-05 A-06'),
        chapter('example', 'Worked Cross-Platform Comparison', 'Assign different evidence obligations to the three services for one operational symptom.', 'A-U01'),
        chapter('evidence', 'Documentation Acceptance and Evidence Boundaries', 'Identify what is documented, recommended, tested and undisclosed.', 'A-07'),
    ],
}

TYPES = {
    'D-01': 'overview', 'D-02': 'configuration', 'D-03': 'configuration', 'D-04': 'mechanism', 'D-05': 'mechanism',
    'D-06': 'operation', 'D-07': 'operation', 'D-08': 'operation', 'D-09': 'reference', 'D-10': 'troubleshooting', 'D-11': 'evidence',
    'S-01': 'overview', 'S-02': 'configuration', 'S-03': 'configuration', 'S-04': 'operation', 'S-05': 'operation',
    'S-06': 'operation', 'S-07': 'troubleshooting', 'S-08': 'evidence',
    'F-01': 'overview', 'F-02': 'configuration', 'F-03': 'operation', 'F-04': 'operation', 'F-05': 'configuration', 'F-06': 'troubleshooting', 'F-07': 'evidence',
    'A-01': 'overview', 'A-02': 'mechanism', 'A-03': 'mechanism', 'A-04': 'mechanism', 'A-05': 'operation', 'A-06': 'operation', 'A-07': 'evidence',
}
LABELS = {
    'overview': 'Overview and capabilities',
    'configuration': 'Configuration',
    'mechanism': 'Mechanism',
    'operation': 'Operation',
    'example': 'Worked example',
    'troubleshooting': 'Troubleshooting',
    'reference': 'Reference',
    'evidence': 'Official evidence',
}


def section_type(sid):
    if '-U' in sid:
        return 'example'
    if '-M' in sid:
        return 'mechanism'
    return TYPES[sid]


DECK_CHAPTERS = {
    'devops': [
        ('Part I · Product Model', [0]),
        ('Part II · Use Case Catalog', [1, 2, 3, 4]),
        ('Part III · Access and Knowledge', [5, 6, 7]),
        ('Part IV · Incident Operations and Control', [8, 9, 10, 11]),
        ('Part V · Worked Example', [12]),
        ('Part VI · Troubleshooting', [13]),
    ],
    'security': [
        ('Part I · Product Model', [0]),
        ('Part II · Use Case Catalog', [1, 2, 3, 4]),
        ('Part III · Scope and Authentication', [5, 6, 7]),
        ('Part IV · Assessment and Evidence Lifecycle', [8, 9, 10, 11, 12]),
        ('Part V · Worked Example', [13]),
        ('Part VI · Troubleshooting', [14]),
    ],
    'finops': [
        ('Part I · Product Model', [0]),
        ('Part II · Use Case Catalog', [1, 2, 3, 4, 5]),
        ('Part III · Context and Automation', [6, 7, 8, 9]),
        ('Part IV · Access and Source Dependencies', [10]),
        ('Part V · Worked Example', [11]),
        ('Part VI · Troubleshooting', [12]),
    ],
    'architecture': [
        ('Part I · Comparison Framework', [0, 1]),
        ('Part II · Resource, Context and Access', [2, 3]),
        ('Part III · Execution, Lifecycle and Handoffs', [4, 5, 6]),
        ('Part IV · Tabletop', [7]),
        ('Part V · Acceptance Criteria', [8]),
    ],
}
