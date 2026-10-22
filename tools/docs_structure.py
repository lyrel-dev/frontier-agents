"""Explicit chapters; every canonical section belongs to exactly one chapter."""
REVISION = '2026-10-22-structured-html'
BASELINE = '03ad431ecb7636a2f22688c674e8d05b3dae5d5a'

def chapter(slug, title, purpose, sections):
    return {'slug': slug, 'title': title, 'purpose': purpose, 'sections': sections.split()}

CHAPTERS = {
    'devops': [
        chapter('overview', 'Platform overview and capabilities', 'Understand the service functions, configuration objects and reusable capabilities.', 'D-01'),
        chapter('access', 'Access and integrations', 'Configure operator access, resource access, external tools and network connectivity.', 'D-02 D-03 D-04'),
        chapter('context', 'Context, memory and behavior', 'Distinguish discovery, memory production, correction, retrieval, attachment, instructions and skills.', 'D-05 D-M01 D-M02 D-M07 D-M03 D-M04'),
        chapter('execution', 'Execution and administration', 'Trace incident routing, custom-agent runs, computation, approvals and configuration changes.', 'D-06 D-07 D-M05 D-M06 D-08 D-09'),
        chapter('example', 'Worked example', 'Use prepared evidence to examine a recurring alarm without assuming the previous cause has returned.', 'D-U01'),
        chapter('diagnosis', 'Troubleshooting and limits', 'Locate the failed prerequisite and distinguish limits from missing access or context.', 'D-10'),
        chapter('evidence', 'Coverage and official evidence', 'Identify detailed coverage, linked subjects and source-version qualifications.', 'D-11'),
    ],
    'security': [
        chapter('overview', 'Platform overview and capabilities', 'Understand application scope, shared resources, assessment definitions and results.', 'S-01'),
        chapter('access', 'Identity, sources and target scope', 'Configure source access and distinguish test targets, dependencies and exclusions.', 'S-02 S-03'),
        chapter('mechanisms', 'Authentication, criteria and protection', 'Examine credential resolution, login reuse, requirement evaluation, regeneration and encryption.', 'S-M01 S-M02 S-M03 S-M04 S-M06'),
        chapter('operations', 'Assessment and finding lifecycle', 'Follow configurations, executions, findings, repairs, revalidation and earlier assessments.', 'S-04 S-05 S-M05 S-06'),
        chapter('example', 'Worked example', 'Trace an authorization finding through the deployed repair and prepared revalidation evidence.', 'S-U01'),
        chapter('diagnosis', 'Troubleshooting and limits', 'Diagnose the failed access, authentication, criteria or execution prerequisite.', 'S-07'),
        chapter('evidence', 'Coverage and official evidence', 'Review coverage decisions and the sources supporting the guide.', 'S-08'),
    ],
    'finops': [
        chapter('overview', 'Platform overview and capabilities', 'Distinguish the agent instance, permissions, retained context, tasks and outputs.', 'F-01'),
        chapter('access', 'Access, sources and integrations', 'Establish role responsibilities, source-data dependencies and destination connections.', 'F-02 F-M01 F-05'),
        chapter('context', 'Reference files, memory and compaction', 'Separate operator-maintained inputs, cross-session memory and within-session summaries.', 'F-M02 F-M03 F-M04'),
        chapter('operations', 'Tasks, publication and lifecycle', 'Trace task creation, event matching, report artifacts, approval and object-specific removal.', 'F-03 F-M05 F-04 F-M06 F-M07'),
        chapter('example', 'Worked example', 'Reconcile cost components before assessing the limited evidence for a causal explanation.', 'F-U01'),
        chapter('diagnosis', 'Troubleshooting and limits', 'Test the data, context, execution and destination layers separately.', 'F-06'),
        chapter('evidence', 'Coverage and official evidence', 'Review scope exclusions and the source-review record.', 'F-07'),
    ],
    'architecture': [
        chapter('models', 'Resource and context models', 'Compare the documented objects and retained information without assuming a common runtime.', 'A-01 A-02'),
        chapter('boundaries', 'Access and effect boundaries', 'Separate reachability, identity and the authority to perform an operation.', 'A-03 A-04'),
        chapter('lifecycle', 'Lifecycle and handoffs', 'Compare configuration, execution, artifacts and team-composed handoff records.', 'A-05 A-06'),
        chapter('example', 'Worked comparison', 'Identify different jobs for the three services from the same operational symptom.', 'A-U01'),
        chapter('evidence', 'Coverage and official evidence', 'Identify what is documented, recommended and undisclosed.', 'A-07'),
    ],
}

TYPES = {
    'D-01':'overview', 'D-02':'configuration', 'D-03':'configuration', 'D-04':'mechanism', 'D-05':'mechanism',
    'D-06':'operation', 'D-07':'operation', 'D-08':'operation', 'D-09':'reference', 'D-10':'troubleshooting', 'D-11':'evidence',
    'S-01':'overview', 'S-02':'configuration', 'S-03':'configuration', 'S-04':'operation', 'S-05':'operation',
    'S-06':'operation', 'S-07':'troubleshooting', 'S-08':'evidence',
    'F-01':'overview', 'F-02':'configuration', 'F-03':'operation', 'F-04':'operation', 'F-05':'configuration', 'F-06':'troubleshooting', 'F-07':'evidence',
    'A-01':'overview', 'A-02':'mechanism', 'A-03':'mechanism', 'A-04':'mechanism', 'A-05':'operation', 'A-06':'operation', 'A-07':'evidence',
}
LABELS = {'overview':'Overview and capabilities', 'configuration':'Configuration', 'mechanism':'Mechanism', 'operation':'Operation', 'example':'Worked example', 'troubleshooting':'Troubleshooting', 'reference':'Reference', 'evidence':'Official evidence'}
def section_type(sid):
    if '-U' in sid: return 'example'
    if '-M' in sid: return 'mechanism'
    return TYPES[sid]

DECK_CHAPTERS = {
    'devops': [('Platform model', [0]), ('Access and integrations', [1,2,3]), ('Context and behavior', [4,5,6,7]), ('Execution and control', [8,9,10,11]), ('Prepared-result exercise', [12]), ('Troubleshooting and coverage', [13])],
    'security': [('Platform model', [0]), ('Scope and authentication', [1,2,3,4]), ('Assessment and criteria', [5,6,7]), ('Repair, evidence and protection', [8,9,10,11]), ('Prepared-result exercise', [12]), ('Troubleshooting and coverage', [13])],
    'finops': [('Platform model', [0]), ('Access and source data', [1,2]), ('Context mechanisms', [3,4,5]), ('Tasks, publication and lifecycle', [6,7,8,9,10]), ('Prepared-result exercise', [11]), ('Troubleshooting and coverage', [12])],
    'architecture': [('Resource and context models', [0,1]), ('Access and effect boundaries', [2,3]), ('Lifecycle and handoffs', [4,5]), ('Evidence boundaries', [6]), ('Prepared-result tabletop', [7]), ('Acceptance criteria', [8])],
}
