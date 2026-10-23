"""Authored teaching sequence over the frozen model and use cases.

This is a teaching plan, not another capability taxonomy or an AWS orchestration
specification. Each diagram overlay reuses the product's fixed architecture.
"""
from __future__ import annotations

DECKS={}
DECK_CHAPTERS={}


def deck(product,title,prefix):
    DECKS[product]={'title':title,'subtitle':'Agent composition, scope and operational workflows','prefix':prefix,'slides':[]}
    DECK_CHAPTERS[product]=[]


def chapter(product,title):
    DECK_CHAPTERS[product].append((title,[]))


def add(product,title,minutes,refs,kind,data,message,view=None,cases=(),explain=()):
    slides=DECKS[product]['slides']
    s={'title':title,'seconds':int(minutes*60),'refs':list(refs),'kind':kind,'data':data,'message':message,'cases':list(cases)}
    if view:s['diagram']='teaching-'+product+'-'+view
    if explain:s['explain']=list(explain)
    DECK_CHAPTERS[product][-1][1].append(len(slides));slides.append(s)


def diagram(product,title,minutes,refs,view,points,message,cases=()):
    add(product,title,minutes,refs,'diagram',[],message,view,cases,points)


def table(product,title,minutes,refs,rows,message,cases=()):
    add(product,title,minutes,refs,'table',rows,message,cases=cases)


# DEVOPS: establish the worker, then cooperation, then the workspace, then effects.
deck('devops','AWS DevOps Agent','D')
chapter('devops','Agent composition and shared operating scope')
diagram('devops','What an agent is in AWS DevOps Agent',3,['D-90','D-15','D-16'],'agent',
 ['Guidance defines behavior; skills supply procedures; retrieved memory supplies informational context.',
  'An execution selects steps and calls available tools. Connections supply access to external evidence.',
  'A definition is reusable configuration. An invocation or investigation records particular work.'],
 'Begin with a scoped request, not an asset identifier. Trace it into an execution, then down through an authorized source operation and back to an output. The three upper boxes supply different kinds of context. AWS manages some agent roles; a custom definition gives the customer explicit prompt, tool, skill and store choices. Do not imply that every connected tool is assigned to every custom agent.')
table('devops','Instructions, skills, knowledge and integrations have different roles',3,['D-90','D-M03','D-M04','D-M01','D-03'],
 [['Element','Contribution to the execution','Not equivalent to'],
 ['Instructions / system prompt','Standing behavioral guidance or custom definition','A permission grant'],
 ['Skill','Applicable or assigned procedure and supporting files','An incident result'],
 ['Memory','Selected retained facts and lessons','Current telemetry or model retraining'],
 ['Tool','Callable source operation with arguments and results','The external provider itself'],
 ['Integration / connection','Authentication, association and a reachable source','Automatic tool assignment to all agents']],
 'Use one operational example: the prompt asks about checkout timeouts, the skill suggests comparing upstream latency, memory contains an earlier cause, and an authorized telemetry operation returns current observations. Each element contributes something different. The current result can contradict the old memory.')
diagram('devops','How managed roles contribute to one investigation',3,['D-91','D-15','D-06'],'coordination',
 ['Triage decides whether an event joins existing work, is skipped, or starts a new investigation.',
  'RCA, mitigation and output roles have distinct responsibilities within service-managed incident work.',
  'Learning produces reusable context separately. It is not a mandatory final stage of every invocation.'],
 'Read this as a responsibility map, not a published RPC call graph. AWS documents incident roles running within investigations, while Learning has its own history and scheduled work. A mitigation proposal does not directly authorize execution. Grader Reviews, customer feedback, learning refresh and prevention evaluation are different activities; avoid turning them into one universal linear pipeline.')
diagram('devops','What an Agent Space contains and controls',3,['D-92','D-01','D-13','D-12'],'space',
 ['The boundary adds account access, provider associations, operator access, agents and retained records.',
  'Provider registration establishes a connection; association selects its use in this Agent Space.',
  'A custom definition selects tools and stores inside that scope. A source remains outside the service.'],
 'The components have not moved; the enclosing scope is now visible. Agent Space is not the agent, a single run, the observed application or a customer VPC. Establish access for the space, then select resources for the particular custom agent. Private routing changes reachability, not the instructions or authority of a tool.')
table('devops','Teaching order for operational workflows',2,['D-93'],
 [['Priority for this audience','Workflow group','Why it follows here'],
 ['1','Incident triage, investigation and mitigation','Immediate diagnosis and the boundary before a change'],
 ['2','Health reporting and change summaries','Routine reuse of the evidence-access path'],
 ['3','Incident patterns and prevention','Use prior results without substituting them for current evidence'],
 ['4','SOPs and topology documentation','Maintain procedures and environment context'],
 ['5','Configuration and release assurance','Apply criteria to an explicit resource or revision'],
 ['6','Operational review','Combine verified outputs into owned decisions']],
 'This order is an instructional choice for DevOps and SRE teams, not an AWS product ranking. The approved use-case groups and definitions remain unchanged. The remaining slides reuse the same architecture, emphasizing the active path and stating the evidence that ends each workflow.')
chapter('devops','Incident response: evidence, decisions and controlled effects')
diagram('devops','Incident triage and investigation',3,['D-93','D-06'],'incident',
 ['Start with the event identity, affected service and actual incident interval.',
  'Inspect Linked / Skipped / Proceed, then follow current source observations and relevant context.',
  'The result is a supported explanation or an explicit evidence gap—not an automatic infrastructure change.'],
 'Follow the input into triage. A linked event adds context to an existing investigation, so there need not be a new investigation record. A skipped event has a recorded criterion, not a healthy-service verdict. For independent work, inspect telemetry, code and deployment observations. Steering adds current evidence; feedback after completion corrects the recorded diagnosis.', ['UC-D01','UC-D02'])
diagram('devops','Mitigation planning and approved execution',3,['D-93','D-M06'],'mitigation',
 ['A mitigation plan states target, parameters, validation and rollback conditions.',
  'Execution adds the service enablement, permissions, tool classification and applicable approval.',
  'Inspect the actual effect and service recovery independently of the generated proposal.'],
 'The operator box becomes relevant at the effect boundary. Preserve the distinction between proposing a change and carrying it out. An approved operation still depends on the selected account role and actual parameters. After execution, compare resource state and service measurements; a successful tool call alone does not show that the incident ended.', ['UC-D03','UC-D04'])
diagram('devops','Incident communication and the investigation record',2,['D-93','D-23','D-06'],'incident',
 ['Use the current investigation record and a declared observation cutoff.',
  'State impact, evidence-supported findings, work in progress and unresolved reads.',
  'Treat publication as a destination-specific effect; report time is not the measurement time.'],
 'The same investigation can supply an incident bulletin. Distinguish an update from a new diagnostic run. The output role and configured collaboration path influence delivery. A request for minute-resolution data does not establish a minute-by-minute custom-agent schedule or delivery guarantee.', ['UC-D05'])
diagram('devops','How prior incidents inform later investigations',3,['D-93','D-M01','D-M02','D-M08'],'learning',
 ['Completed investigations and verified corrections are different knowledge inputs.',
  'Managed learning and feedback-related retention create context for later relevant work.',
  'Later retrieval selects available stores and entries; the diagnosis still depends on current evidence.'],
 'Trace production and reuse as separate lifecycles. A stored monitor entry establishes retained content. A later observable read establishes retrieval. Neither alone establishes diagnostic correctness. The Learning schedule is not the prevention evaluation schedule, and a correction submitted now is not proof of immediate recall.')
add('devops','Exercise: a recurring alarm with a different current cause',8,['D-U01','D-93'],'demo',
 [['0–2 min','Inspect the earlier incident','Database connections 100/100; inventory p95 40 ms'],
  ['2–4 min','Compare current observations','Database connections 34/100; inventory p95 2,900 ms'],
  ['4–6 min','Follow the evidence path','Prior cause is context; current dependency latency is the stronger lead'],
  ['6–8 min','State the conclusion and remaining work','Upstream logs are missing; no live run or automatic rollback is claimed']],
 'Use the repository synthetic fixture. Ask which diagram input establishes the old cause, which operation would retrieve current measurements, and what output is justified. Participants should reject repetition of the database cause when current evidence contradicts it. This is a prepared-result exercise, not an AWS response-time measurement.', cases=['UC-D02'])
chapter('devops','Routine reporting and reliability improvement')
diagram('devops','Service-health reporting from logs and metrics',3,['D-93','D-16','D-19'],'reporting',
 ['Define services, UTC interval, measures, aggregation and comparison period.',
  'Use Chat for a scoped inquiry or a configured custom definition for repeatable reporting.',
  'Produce measurements, comparisons and evidence gaps; enable recurrence only after a reviewed trial.'],
 'The architecture is unchanged. The request is now a report contract, skills contain the reporting procedure, and selected tools retrieve observations. Memory can help interpret service names but cannot replace failed current reads. A trigger creates another invocation; it does not create continuous monitoring.', ['UC-D06'])
table('devops','Health-report contents and verification',2,['D-93','D-07'],
 [['Report section','Evidence required','Review question'],
 ['Scope','Service identities and exact observation interval','Which systems and time period were actually examined?'],
 ['Measurements','Query, aggregation and material source values','Do displayed values match the source result?'],
 ['Comparison','Comparable periods and population','Was a change caused by workload mix or a changed calculation?'],
 ['Exceptions','Failed reads, missing signals and uncertainty','Is missing data incorrectly presented as normal operation?'],
 ['Actions','Owner, evidence and next check','Which decision is supported, and which is still a hypothesis?']],
 'This is an authored report design, not a new AWS feature. Explain the actual artifact the team needs. A short summary and a detailed report can share the query basis while exposing different detail. Neither is useful without the period, failed-read treatment and source evidence.', ['UC-D06'])
diagram('devops','Incident patterns and prevention priorities',3,['D-93','D-06','D-M01'],'learning',
 ['Pattern identification groups relevant investigation evidence; monitor memory is one retained representation.',
  'Prevention evaluation proposes improvements informed by multiple investigations.',
  'The team prioritizes work and records acceptance criteria; a recommendation is not an implemented fix.'],
 'Reuse the knowledge-production path but change the question: across incidents, what recurs and which change is justified? Explain the difference between identifying a recurring cause and deciding which intervention to fund or implement. Keep source investigation identities with each conclusion.', ['UC-D08','UC-D09'])
chapter('devops','Operational knowledge, change assurance and reviews')
diagram('devops','SOP consolidation and skill maintenance',3,['D-93','D-M04','D-17'],'knowledge',
 ['The team reconciles contradictory procedures and identifies the applicable operational conditions.',
  'A skill packages the approved procedure, description and supporting references.',
  'Test applicability and actual tool availability; storing a runbook does not grant its required permissions.'],
 'Here the engineer produces procedural content. A skill is not a finding and is not created merely by concatenating incident summaries. Show how a revised SOP reaches the procedural box, how relevance or explicit assignment makes it available, and why the tool-access path remains separate.', ['UC-D10'])
diagram('devops','Topology and dependency documentation',3,['D-93','D-05','D-M08'],'knowledge',
 ['Connected configuration, source and delivery evidence inform environment understanding.',
  'Learning and topology views expose relationships that must be compared with deployed reality.',
  'Publish owner-reviewed architecture with inferred or missing relationships identified.'],
 'Use the same diagram but follow source evidence to environment knowledge rather than to an incident diagnosis. Distinguish the observed deployment, its inferred topology, retained understanding and the accepted engineering document. A graph boundary is not an IAM boundary.', ['UC-D11'])
diagram('devops','Deployment review and configuration auditing',3,['D-93','D-16','D-12'],'change',
 ['Select immutable revisions or resource identities and the relevant observation interval.',
  'Retrieve deployment states or resource values and compare them with declared criteria.',
  'Return change evidence or resource-specific findings, not an approval inferred from a summary.'],
 'The deployment-review and configuration-audit objectives remain separate approved cases. They share selected source operations and a controlled comparison procedure. Explain their different acceptance evidence: a deployment report identifies revision and state; an audit finding identifies the resource, rule and observed value.', ['UC-D07','UC-D12'])
diagram('devops','Release readiness and active release testing',3,['D-93','D-22'],'change',
 ['Readiness review examines a defined proposed change and its dependencies.',
  'Release testing acts against an explicitly configured deployed UI or API target.',
  'Revision, target, credentials and permitted effects differ; keep the preview qualification.'],
 'Keep the same access and execution model while distinguishing the two subjects. Reviewing code is not equivalent to testing a deployed application. A test profile is native release-test configuration; the catalog configuration recipes are authored guidance, not that resource.', ['UC-D13','UC-D14'])
diagram('devops','Operational reviews: from reports to owned decisions',2,['D-93','D-14'],'review',
 ['Assemble verified health, deployment, incident-pattern and prevention evidence.',
  'Identify decisions, accountable owners and unresolved questions.',
  'Follow actions through the normal engineering process; no shared cross-service runtime is implied.'],
 'This is the shared review use case applied to reliability work. The team consumes outputs from independently scoped executions. Agent output supplies evidence and proposals; the meeting determines priorities and owners. A later Security or FinOps task receives explicit evidence and its own authorization.', ['UC-G01'])
table('devops','Configuration checks before using a workflow',3,['D-02','D-03','D-04','D-M07','D-19'],
 [['Check','Object to inspect','Failure interpretation'],
 ['Operator access','User identity and space role','Can the intended operator enter and act?'],
 ['Evidence access','Account role, provider association and selected tool','Connection existence does not prove a successful read'],
 ['Context availability','Instruction scope, skill assignment and memory attachment','Available content may still not be selected'],
 ['Execution control','Trigger, current invocation and applicable approval','Pausing future starts is not cancelling or undoing work'],
 ['Completion evidence','Observed sources, output and actual effect','Generated text is not independent verification']],
 'Finish with prerequisites the learner can now explain, rather than opening with identifiers. Refer to the capability chapters for full procedures, provider differences, quotas and APIs. Every use case should be traceable from its input through configured source access to its own completion criteria.')

# SECURITY: preserve its assessment model; do not invent DevOps-style peer agents.
deck('security','AWS Security Agent','S')
chapter('security','Assessment execution, application scope and context')
diagram('security','What AWS Security Agent executes',3,['S-90','S-12'],'agent',
 ['A selected assessment uses application evidence, criteria and configured access.',
  'Code review, design review, threat modeling and penetration testing are different operations.',
  'The exposed model is assessment configuration and results—not a customer-configurable roster of DevOps agents.'],
 'Start with an application-security question and the kind of evidence that can answer it. Explain the assessment settings, criteria and context before discussing identifiers. A dynamic test needs a running target and identity; source and design reviews use different inputs and effects.')
diagram('security','How assessment, repair and verification relate',3,['S-91','S-10','S-M05'],'coordination',
 ['An assessment produces findings associated with its inputs and run.',
  'A repair proposal becomes a reviewed and deployed change through the application team.',
  'Revalidation creates new evidence for selected findings; it is not broad new discovery.'],
 'These are linked work records, not assertions about an undocumented internal multi-agent graph. The team deployment step is external. The original finding remains distinct from the remediation pull request and subsequent revalidation job.')
diagram('security','Application Agent Spaces and shared requirements',3,['S-92','S-01'],'space',
 ['An application Agent Space selects sources, configurations, users and assessment records.',
  'Requirement packs and provider registration can be shared; application bindings remain specific.',
  'Target scope, credentials and network access are separate configuration choices.'],
 'Do not equate this scope with a DevOps operational Agent Space. The diagram shows selected criteria; it does not place ownership of shared requirement packs inside the application. The detailed resource model specifies which objects are shared and which belong to the application.')
chapter('security','Assessment and finding resolution')
diagram('security','Assess an authorized running application',3,['S-93','S-03','S-M01','S-04'],'assessment',
 ['Verify the target, exclusions, application revision and authorized test identities.',
  'Resolve credentials, reach the intended authenticated surface and execute the configured test.',
  'Interpret coverage and findings against the actual identity and reachable scope.'],
 'Public/private, authenticated/unauthenticated and recurring execution are configuration dimensions of the approved assessment case. Failed authentication cannot establish coverage of authenticated functionality. Explicitly identify the application effects permitted during the test.', ['UC-S01'])
diagram('security','Review source code and proposed changes',3,['S-93','S-06','S-M03'],'assessment',
 ['Identify repository, revision and full-source versus change-focused scope.',
  'Select vulnerability analysis and applicable requirement validation separately.',
  'Retain finding evidence and revision identity in the review result.'],
 'The same context-and-execution diagram now reads source rather than exercising a deployed endpoint. A source finding does not establish exploitability of an unseen deployment. Keep full-source and proposed-change variants explicit.', ['UC-S02'])
diagram('security','Triage findings and prepare a remediation proposal',3,['S-93','S-05'],'repair',
 ['Review reproducibility, impact, affected revision and evidence gaps.',
  'A remediation proposal is a patch or pull request, not a deployed repair.',
  'Review, test and deploy through the application team before claiming remediation.'],
 'Distinguish finding disposition from changing the application. Eligible personalization may alter later finding attributes, but it does not fix the underlying defect. The proposal remains subject to ordinary code-review and release controls.', ['UC-S05','UC-S06'])
diagram('security','Revalidate a finding after deploying the repair',3,['S-93','S-M05'],'repair',
 ['Confirm the repaired revision is deployed to the selected test environment.',
  'Repeat validation for selected existing findings with the intended identity.',
  'Record reproduced, not reproduced or unresolved results within the tested scope.'],
 'A new revalidation job is associated with the original finding. A non-reproduction result needs the tested target, deployment and identity to be interpretable. It does not constitute a complete new assessment of the application.', ['UC-S07'])
add('security','Exercise: trace a finding to a deployed repair',8,['S-U01','S-91'],'demo',
 [['0–2 min','Read the finding','Identify target, revision, test identity and evidence'],
  ['2–4 min','Inspect the proposal','Separate repository change from deployed version'],
  ['4–6 min','Check verification conditions','Match deployed revision and revalidation identity'],
  ['6–8 min','Interpret the result','State tested scope and unresolved coverage']],
 'Use the supplied synthetic evidence. Ask participants to identify the record proving deployment and the record proving which identity was used. A finding status update or merged pull request alone cannot answer both questions.',cases=['UC-S06','UC-S07'])
chapter('security','Design, requirements and reusable context')
diagram('security','Design review and application threat modeling',3,['S-93','S-06','S-10'],'assessment',
 ['Design review evaluates supplied design documents against applicable requirements.',
  'Threat modeling uses source, scope documents or both to describe threats and trust boundaries.',
  'One-off design reviews and reusable threat-model configurations have different lifecycles.'],
 'These remain distinct approved cases. Use the same diagram to show the changed inputs and outputs rather than inventing a universal assessment pipeline. Explain why cloning a design review differs from rerunning a threat-model configuration.', ['UC-S03','UC-S04'])
diagram('security','Maintain security requirements and assessment criteria',3,['S-93','S-M03','S-M04'],'context',
 ['Consolidate the policy sources and define applicability and compliance criteria.',
  'Enable the relevant pack for eligible future reviews.',
  'Document-based regeneration replaces pack content; review changes before adoption.'],
 'Requirement consolidation is an engineering objective; pack configuration and evaluation are service facilities supporting it. Separate generation from evaluation. A source-policy approval is a team decision, not a hidden native approval API.', ['UC-S08'])
table('security','Three distinct forms of retained context',3,['S-M07','S-M02','S-13'],
 [['Representation','What is reused','What it does not establish'],
 ['Application context','Selected source and application understanding','A universal incident-memory service'],
 ['Login Optimization','A successful authentication-navigation procedure','Authorization for additional targets or roles'],
 ['Findings Personalization','Eligible earlier edits applied to similar findings','That a vulnerability was repaired'],
 ['Requirement pack','Criteria for applicable future code/design reviews','A certification or retrospective change to old findings']],
 'Do not label all retained state as the same learning mechanism. Compare producer, consumer, enablement and lifecycle. The learner should know which representation to inspect when a result reflects an obsolete criterion, failed login or inappropriate finding preference.')
table('security','Operational checks and failure boundaries',3,['S-02','S-03','S-07'],
 [['Area','Inspect','Decision'],
 ['Application scope','Target domains, exclusions and owners','Stop when authorization is unclear'],
 ['Source identity','Repository or document revision','Reject a conclusion without a traceable subject'],
 ['Authentication','Resolved credential and actual application role','Do not infer coverage from a retrieved secret'],
 ['Execution','Configuration, run state and limits','Separate incomplete execution from absence of findings'],
 ['Verification','Finding, deployed revision and revalidation job','Keep unresolved cases open']],
 'End with checks that follow from the model, not a generic warning list. Use the guide chapters for provider setup, network paths, IAM, encryption and quotas. Each unresolved prerequisite limits the conclusion that can be drawn from the assessment.')

# FINOPS: tasks coordinate execution; source services remain the analytical basis.
deck('finops','AWS FinOps Agent','F')
chapter('finops','Analysis, context and instance scope')
diagram('finops','What AWS FinOps Agent does with a request',3,['F-90','F-11','F-M01'],'agent',
 ['The request defines a cost question, period and analysis basis.',
  'Authorized AWS data supplies observations; files and retained memory supply organizational context.',
  'The result is an answer, analysis or artifact. An engineering or financial change is a separate decision.'],
 'The labels deliberately differ from DevOps. Uploaded context files are not a native SKILL.md registry, and a requested task is not a custom-agent asset. Recommendation estimates come from their upstream services and must retain their provenance.')
diagram('finops','How conversations, automations and tasks coordinate work',3,['F-91','F-03','F-M05'],'coordination',
 ['Ordinary questions can be answered directly in a conversation.',
  'Explicit on-demand tasks and matching automations create queued work.',
  'A task result and external publication are independently observable outcomes.'],
 'Do not draw each task as another agent. A schedule or supported anomaly event creates a new task from its automation. Disabling that automation stops future creation; current tasks and existing outputs retain their separate lifecycle.')
diagram('finops','The agent instance and its access boundaries',3,['F-92','F-01','F-02','F-05'],'space',
 ['An instance has its own data access, organizational context, work history and connections.',
  'Data-source access is separate from operator access and destination authorization.',
  'Jira and Slack connections select where an output may be published.'],
 'Registration of an integration and an instance-specific destination connection are distinct. The same source permission does not authorize publication to every channel. Instance-local retained context is not a shared memory across the three AWS products.')
chapter('finops','Cost inquiry, anomaly investigation and reporting')
diagram('finops','Analyze historical cost and usage',3,['F-93','F-14','F-M01'],'analysis',
 ['Define accounts, dates, currency, cost basis, dimensions and filters.',
  'Retrieve and reconcile totals before interpreting dimensional differences.',
  'Separate numerical contribution, correlation and supported causal explanation.'],
 'The first analytical task establishes a repeatable query contract. A different cost basis or period can explain two apparently conflicting totals. Preserve failed reads and missing ownership mappings rather than inventing an allocation.', ['UC-F01'])
diagram('finops','Investigate a cost anomaly',3,['F-93','F-M05','F-M01'],'analysis',
 ['Use the anomaly event or explicit question to establish the affected scope.',
  'Inspect cost drivers and optional operational-change evidence through their actual source services.',
  'Record reconciled contributions and remaining causal uncertainty before publication.'],
 'An anomaly is a reason to investigate, not proof of cause. EventBridge matching, task creation, analytical completion and destination delivery are distinct inspection points. A nearby CloudTrail event is corroborating evidence only when its relation to the cost change is established.', ['UC-F05'])
add('finops','Exercise: explain a cost increase from the supplied evidence',8,['F-U01','F-M01'],'demo',
 [['0–2 min','Fix the comparison contract','Same period basis, scope and unit rates'],
  ['2–4 min','Reconcile the supplied table','Quantity × rate and component totals'],
  ['4–6 min','Assess the proposed driver','Separate arithmetic attribution from change-event correlation'],
  ['6–8 min','Assign follow-up','Name missing workload evidence and the responsible owner']],
 'Use the committed synthetic cost table and its arithmetic checks. Participants should identify which claim follows from the numbers and which requires service-owner evidence. Do not present the synthetic change as an observed AWS saving or real customer event.',cases=['UC-F01','UC-F05'])
diagram('finops','Prepare a periodic cost report',3,['F-93','F-04','F-03'],'reporting',
 ['Retain the query contract and a reviewed ownership mapping or report template.',
  'Create the task or automation appropriate to the delivery requirement.',
  'Inspect report content and artifact provenance separately from publication success.'],
 'Reporting reuses source-backed analysis and adds a stable presentation contract. An artifact may originate in a conversation or a task. A scheduled automation creates successive tasks; it does not make their periods or currencies comparable automatically.', ['UC-F04'])
table('finops','Publication controls depend on the action and invocation',3,['F-M06','F-05'],
 [['Action','Conversation / on-demand task','Scheduled / event automation'],
 ['Create Jira issue or comment','Approval request','Authorization established during automation setup'],
 ['Post Slack message','No per-message approval prompt','No per-message approval prompt'],
 ['Read cost or recommendation data','Source permissions apply','Source permissions apply'],
 ['Verify delivery','Inspect destination and action result','Inspect task result and destination']],
 'Do not teach a universal human-approval switch. The action and invocation mode determine the documented behavior. The destination audience and permitted content must be reviewed before enabling an unattended publication path.')
chapter('finops','Planning, optimization and review')
table('finops','Forecasting and commitment coverage answer different questions',3,['F-93','F-14'],
 [['Analysis','Question','Required interpretation'],
 ['Cost forecast','What expenditure is projected for the selected horizon?','Source, period, scope and uncertainty'],
 ['Commitment coverage','What eligible usage is covered by existing commitments?','Commitment type, eligible usage and period'],
 ['Comparison','Are assumptions and filters compatible?','Do not combine unlike denominators'],
 ['Decision','What follow-up is justified?','Agent analysis is not purchase authorization']],
 'These are two approved cases, not two labels for one output. A forecast concerns expected expenditure; coverage concerns eligible usage and commitments. Retain the distinct query basis and completion criteria.', ['UC-F02','UC-F03'])
diagram('finops','Prioritize recommendations and measure an implemented change',3,['F-93','F-14','F-M01'],'optimization',
 ['Retain the original recommendation source, scope, assumptions and estimated benefit.',
  'The service owner reviews and implements an authorized change outside this analytical workflow.',
  'Measure a comparable post-change period; observed savings are not the original estimate.'],
 'Show the two separate objectives on the same path. First prioritize candidates; later measure the actual outcome of an implemented action. They use different evidence and are not one automatic optimization loop.', ['UC-F06','UC-F07'])
diagram('finops','Prepare the cost-management contribution to an operational review',2,['F-93','F-10'],'reporting',
 ['Assemble reconciled reports, anomaly explanations and original recommendations.',
  'Separate estimates from observed outcomes and unresolved owner questions.',
  'Assign decisions and follow-up using the shared review case; do not imply cross-agent orchestration.'],
 'The shared operational-review case has a cost-management profile. That profile is authored setup guidance, not a platform resource. The team receives evidence from separately scoped work and decides what happens next.', ['UC-G01'])
table('finops','Diagnose data, context, execution and delivery separately',3,['F-06','F-M02','F-M03','F-M04','F-M07'],
 [['Symptom','Inspect','Do not infer'],
 ['Totals disagree','Dates, basis, scope and filters','That one answer is correct because it is generated'],
 ['Wrong ownership','Source mapping and retained preference','That editing a file updates every memory'],
 ['Work did not start','Automation condition and task history','That an existing automation proves execution'],
 ['No destination result','Connection and action outcome','That analytical completion proves publication'],
 ['Old context persists','File, memory and conversation lifecycle','That compaction or cancellation deletes stored content']],
 'Return to the diagram: each symptom belongs to a specific object or path. The operator should be able to distinguish a missing source result from a stale mapping and a failed delivery. Use the detailed guide for lifecycle procedures and preview constraints.')

# CROSS-SERVICE: compare only after teaching concrete meanings.
deck('architecture','Cross-service architecture','A')
chapter('architecture','Agents and their operating context')
table('architecture','An agent is an executor, not the surrounding workspace',3,['A-90','A-00'],
 [['Concept','Meaning in this collection','Example'],
 ['Agent','A configured or managed AI executor using permitted operations and context','DevOps managed role or custom definition'],
 ['Execution','One scoped piece of work and its evidence','Investigation, assessment run or task'],
 ['Context','Information and procedures made available through product-specific paths','Skill, application context or uploaded cost mapping'],
 ['Workspace','Configuration and access scope around work','Operational Agent Space, application Agent Space or FinOps instance'],
 ['Result','A produced record that still needs interpretation','Diagnosis, finding or report']],
 'Start with the simple execution cycle, then identify the actual nouns of each service. This is an explanatory comparison, not a common AWS resource type or a universal internal agent framework.')
add('architecture','The agent execution cycle',3,['A-90','A-00'],'diagram',[],
 'A request supplies scope; applicable context informs an execution; authorized operations return observations; the execution produces a result or another step. Retention and action approval are separate product-specific paths. This logical cycle does not disclose the foundation model or internal orchestration implementation.')
DECKS['architecture']['slides'][-1]['diagram']='agent-execution'
table('architecture','Context and control differ between the three products',3,['A-90','A-02','A-12'],
 [['Concern','DevOps','Security','FinOps'],
 ['Behavior','Managed instructions or custom prompt','Assessment settings and criteria','Request, task instructions and context files'],
 ['Reusable context','Skills and selected memory','Application context, requirements and specific retained state','Files, persistent memory and conversation summary'],
 ['Execution','Managed investigation or custom invocation','Assessment-specific run or one-off review','Conversation or explicit queued task'],
 ['Scope','Operational Agent Space','Application Agent Space with shared settings','Agent instance and destination connections']],
 'Do not carry the DevOps meaning of skills or custom agent into the other two products. Similar responsibilities can be implemented through different configuration objects and lifecycle rules.')
chapter('architecture','Coordination, boundaries and evidence')
table('architecture','Three different meanings of coordination',3,['A-91','A-11','A-06'],
 [['Level','Documented or authored relationship','Boundary'],
 ['Inside DevOps incident work','Managed roles contribute to an investigation; Learning supplies later context','No customer-authored internal routing graph is implied'],
 ['Within a Security or FinOps workflow','Linked assessments/results or automation-created tasks','Not a documented roster of DevOps-style peer agents'],
 ['Across the three products','A team transfers explicit evidence and a new request','Separate identities, scope and authorization'],
 ['Acceptance','A reviewer checks the receiving work against its own criteria','A generated summary is not a transferred approval']],
 'The term multi-agent must not collapse these cases. Explain exactly what passes: a signal, a retained entry, a finding identity, an event, or a team-owned handoff. Where the service does not document the internal graph, leave it unspecified.')
add('architecture','Cross-service evidence handoff',3,['A-91','A-06','A-08'],'diagram',[],
 'A team may use an incident investigation to frame a security assessment or a cost inquiry. The handoff carries evidence identities, target revision, period, question and owner. It does not transfer credentials, permissions or an established root cause.')
DECKS['architecture']['slides'][-1]['diagram']='shared-handoff'
table('architecture','Controls follow the effect',3,['A-04','A-03'],
 [['Effect','Control to identify','Evidence to retain'],
 ['Read source data','Source identity, permission and network path','Actual source result and scope'],
 ['Change infrastructure','Directed-action configuration and applicable approval','Requested parameters, attribution and resulting state'],
 ['Exercise an application','Authorized target, test identity and exclusions','Run, tested revision and observations'],
 ['Publish externally','Destination and invocation-specific rule','Actual issue, comment or message result'],
 ['Accept a conclusion','Independent engineering or financial review','Acceptance verdict and unresolved questions']],
 'Network reachability and instruction text do not establish authorization. Conversely, an approved effect still requires the correct technical identity. Show how each control belongs to the operation rather than to a vague autonomy level.')
chapter('architecture','Apply the model to approved operational work')
table('architecture','A use case applies platform facilities to a defined objective',3,['A-09','A-90'],
 [['Example','Facilities used','Completion evidence'],
 ['Service-health report','Current source reads; optional context; optional custom schedule','Measurements, interval and explicit gaps'],
 ['Finding revalidation','Original finding; deployed repair; configured test identity','Revalidation result under stated conditions'],
 ['Cost anomaly investigation','Anomaly, cost queries and optional change evidence','Reconciled contribution and causal limits'],
 ['Operational review','Reviewed outputs and team-owned decisions','Owners, actions and criteria for closure']],
 'Use the frozen use cases to apply—not redefine—the concepts. A configuration recipe is a way to supply environment-specific choices for an objective. It is not an AWS facility or a new type of agent.', ['UC-D06','UC-S07','UC-F05','UC-G01'])
add('architecture','Exercise: one event, three independently scoped inquiries',4,['A-U01','A-91'],'demo',
 [['0–1 min','Define the observation','Service symptom, revision and observation period'],
  ['1–2 min','Assign incident work','Current evidence and unresolved dependencies'],
  ['2–3 min','Define Security and FinOps questions','Authorized target/revision and comparable cost basis'],
  ['3–4 min','Record handoff and acceptance','Separate owners, permissions and verification criteria']],
 'Use the supplied tabletop. The same event can motivate three questions without establishing one shared cause or one shared execution. Ask the audience which facts are transferred and which must be verified again by the receiving workflow.',cases=['UC-G01'])
table('architecture','Reading path after the presentation',2,['A-90','A-12','A-07'],
 [['Need','Read','Expected understanding'],
 ['Understand one product','Agent overview, then capability chapters','Objects, context, access and work'],
 ['Perform a task','Approved use-case page','Scope, workflow, configuration and acceptance'],
 ['Inspect identity and ownership','Resource model','Product-specific objects and qualified relationships'],
 ['Configure or troubleshoot','Detailed procedure and official reference','Actual controls, limits and expected observations']],
 'The presentation builds the mental model and demonstrates its use. The guide retains detailed configuration, source qualifications and limits. Do not turn the reference taxonomy into the required teaching order.')
