"""Logical diagrams. DOT definitions are maintained here; SVG is generated locally."""
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
DIAGRAMS={'agent-execution': ('Agent execution and evidence cycle',
                     'A task and its configuration guide an execution. Authorized tools return '
                     'observations. Those observations can lead to another step or a result. Retention '
                     'is a separate, product-specific path.',
                     ['A-00'],
                     '\n'
                     'rankdir=LR;\n'
                     'request [label="Request or event\\nTask and scope"];\n'
                     'context [label="Applicable configuration\\nInstructions and context"];\n'
                     'run [label="Agent execution\\nSelect the next step"];\n'
                     'tool [label="Authorized tool or assessment\\nQuery or permitted operation"];\n'
                     'result [label="Result\\nAnswer, finding, or artifact"];\n'
                     'request -> run [label="starts"];\n'
                     'context -> run [label="supplies context"];\n'
                     'run -> tool [label="invokes"];\n'
                     'tool -> run [label="returns observations"];\n'
                     'run -> result [label="produces"];\n'),
 'devops-integrations': ('Provider registration and Agent Space association',
                         'Provider authentication is registered at account level. Association and tool '
                         'selection make an explicit subset available to the Agent Space. The '
                         'invocation still needs a working authenticated route.',
                         ['D-12', 'D-03'],
                         '\n'
                         'rankdir=LR;\n'
                         'provider [label="External provider\\nTelemetry, code, or tool service"];\n'
                         'registration [label="Account registration\\nEndpoint and authentication"];\n'
                         'association [label="Agent Space association\\nSelected resources or tools"];\n'
                         'invocation [label="Tool invocation\\nArguments and execution identity"];\n'
                         'observation [label="Source result\\nResource ID and timestamp"];\n'
                         'provider -> registration [label="authorize"];\n'
                         'registration -> association [label="associate"];\n'
                         'association -> invocation [label="permits selected tool"];\n'
                         'invocation -> observation [label="query result"];\n'),
 'devops-memory': ('Incident knowledge production and selective retrieval',
                   'Prior investigations and corrective feedback are separate producers. Available '
                   'store descriptions lead to relevant entry selection. Current telemetry is needed to '
                   'evaluate historical context in the next investigation.',
                   ['D-M01', 'D-M02', 'D-M07'],
                   '\n'
                   'rankdir=TB;\n'
                   'history [label="Prior investigations\\nOutcomes and evidence"];\n'
                   'feedback [label="Verified correction\\nActual cause and feedback"];\n'
                   'learning [label="Managed learning\\nRecurring monitor causes"];\n'
                   'monitor [label="Monitor memory\\nVersioned retained context"];\n'
                   'reflection [label="Corrective memory\\nLesson from feedback"];\n'
                   'select [label="Retrieval\\nStore and entry descriptions"];\n'
                   'run [label="New investigation\\nHistorical context + current evidence"];\n'
                   'telemetry [label="Current telemetry\\nNew time window and measurements"];\n'
                   'history -> learning [label="analyzed"];\n'
                   'learning -> monitor [label="synthesized"];\n'
                   'feedback -> reflection [label="recorded correction"];\n'
                   'monitor -> select [label="when available"];\n'
                   'reflection -> select [label="when relevant"];\n'
                   'select -> run [label="selected content"];\n'
                   'telemetry -> run [label="supports or contradicts"];\n'),
 'devops-incident': ('Incident triage and investigation workflow',
                     'A signal can be linked, skipped, or investigated independently. Steering affects '
                     'the current analysis; completed-investigation feedback supplies a separate '
                     'corrective input.',
                     ['D-06'],
                     '\n'
                     'rankdir=TB;\n'
                     'signal [label="Incident signal\\nIdentity, service, and time"];\n'
                     'triage [label="Triage decision\\nCorrelation and skip criteria",shape=diamond];\n'
                     'linked [label="Linked\\nExisting primary investigation"];\n'
                     'skipped [label="Skipped\\nRecorded criterion and reason"];\n'
                     'new [label="Proceed\\nIndependent investigation"];\n'
                     'evidence [label="Investigation\\nTool observations and hypotheses"];\n'
                     'operator [label="Operator steering\\nAdditional or contrary evidence"];\n'
                     'result [label="Investigation result\\nCause and mitigation proposal"];\n'
                     'feedback [label="Completed-run feedback\\nVerdict and verified correction"];\n'
                     'signal -> triage;\n'
                     'triage -> linked [label="correlated"];\n'
                     'triage -> skipped [label="criterion matches"];\n'
                     'triage -> new [label="new work"];\n'
                     'new -> evidence;\n'
                     'operator -> evidence [label="steers"];\n'
                     'evidence -> result;\n'
                     'result -> feedback [label="review"];\n'
                     'linked -> new [label="unlink",style=dashed];\n'
                     'skipped -> new [label="unskip",style=dashed];\n'),
 'devops-reporting': ('Configured operational-report workflow',
                      'The team defines the report period and selected evidence. An invocation queries '
                      'sources, produces a report, and exposes results for review. Schedule timing and '
                      'the reporting window are separate configuration decisions.',
                      ['D-07'],
                      '\n'
                      'rankdir=TB;\n'
                      'contract [label="Report specification\\nService, window, aggregation, '
                      'audience"];\n'
                      'definition [label="Custom-agent definition\\nPrompt, tools, skills, memory"];\n'
                      'trigger [label="On-demand or scheduled start\\nFlexible schedule window '
                      'applies"];\n'
                      'query [label="Invocation\\nQuery selected logs and metrics"];\n'
                      'report [label="Report\\nMeasured changes and missing signals"];\n'
                      'review [label="Engineering review\\nReproduce a material observation"];\n'
                      'publication [label="Approved destination\\nOnly when separately configured"];\n'
                      'contract -> definition [label="defines the task"];\n'
                      'definition -> query [label="supplies configuration"];\n'
                      'trigger -> query [label="starts work"];\n'
                      'query -> report [label="synthesizes evidence"];\n'
                      'report -> review [label="checked"];\n'
                      'review -> publication [label="team publication path",style=dashed];\n'),
 'security-integrations': ('Application-source registration and selection',
                           'The account registration authorizes a provider. The application selects '
                           'resources from it. Sources are shared across eligible assessments, while '
                           'repository write actions are separately enabled.',
                           ['S-09'],
                           '\n'
                           'rankdir=TB;\n'
                           'providers [label="Provider account\\nGitHub, GitLab, Bitbucket, '
                           'Confluence"];\n'
                           'register [label="Account registration\\nAuthorized provider connection"];\n'
                           'resources [label="Agent Space selection\\nRepositories or pages"];\n'
                           'read [label="Read context\\nEligible assessment inputs"];\n'
                           'write [label="Optional repository writes\\nComments or remediation"];\n'
                           's3 [label="Connected S3 resources\\nSelected source objects"];\n'
                           'providers -> register [label="authorize"];\n'
                           'register -> resources [label="select"];\n'
                           'resources -> read [label="shared source context"];\n'
                           'resources -> write [label="separate opt-in",style=dashed];\n'
                           's3 -> read [label="selected objects"];\n'),
 'security-context': ('Application context and assessment criteria',
                      'Source evidence and scope documents have different jobs. The assessment uses '
                      'selected evidence and applicable criteria; a finding is an output of that '
                      'execution rather than an automatically shared memory.',
                      ['S-M07', 'S-M03'],
                      '\n'
                      'rankdir=TB;\n'
                      'code [label="Implementation evidence\\nRepository revision and API material"];\n'
                      'design [label="Design context\\nDocuments and connected pages"];\n'
                      'scope [label="Assessment scope\\nApplication and system boundary"];\n'
                      'model [label="Selected application context\\nSystem components and '
                      'relationships"];\n'
                      'criteria [label="Applicable requirements\\nReviewed criteria"];\n'
                      'assessment [label="Assessment run\\nAnalysis or authorized active test"];\n'
                      'finding [label="Finding or model result\\nEvidence, assumptions, and limits"];\n'
                      'code -> model;\n'
                      'design -> model;\n'
                      'scope -> model [label="bounds the question"];\n'
                      'model -> assessment [label="context"];\n'
                      'criteria -> assessment [label="eligible evaluation"];\n'
                      'assessment -> finding;\n'),
 'security-authentication': ('Credential retrieval and authenticated test access',
                             'Credential acquisition, login navigation, and application authorization '
                             'are distinct stages. A retained login procedure can support later '
                             'navigation, but actual identity still needs verification.',
                             ['S-M01', 'S-M02'],
                             '\n'
                             'rankdir=TB;\n'
                             'source [label="Credential source\\nDirect input, secret, role, or '
                             'Lambda"];\n'
                             'resolve [label="Credential acquisition\\nRead, assume, or invoke '
                             'permission"];\n'
                             'login [label="Application login\\nURL, instructions, MFA"];\n'
                             'role [label="Authenticated application identity\\nProtected routes and '
                             'permissions"];\n'
                             'skill [label="Login Optimization\\nRetained successful procedure"];\n'
                             'test [label="Authorized assessment\\nTarget and exclusion rules"];\n'
                             'source -> resolve;\n'
                             'resolve -> login [label="credential"];\n'
                             'login -> role [label="successful authentication"];\n'
                             'login -> skill [label="successful procedure"];\n'
                             'skill -> login [label="later reuse",style=dashed];\n'
                             'role -> test [label="actual access"];\n'),
 'security-revalidation': ('Finding, deployment, and revalidation lineage',
                           'The finding, proposed code change, deployed revision, and revalidation job '
                           'are separate records. Revalidation repeats selected evidence using the '
                           'current target and authentication configuration.',
                           ['S-M05', 'S-05'],
                           '\n'
                           'rankdir=LR;\n'
                           'finding [label="Original finding\\nEvidence and affected revision"];\n'
                           'change [label="Reviewed repair\\nPatch and regression tests"];\n'
                           'deploy [label="Deployed revision\\nOriginal authorized environment"];\n'
                           'job [label="Revalidation job\\nCurrent credentials; selected steps"];\n'
                           'result [label="Scoped result\\nReproduced or not reproduced"];\n'
                           'finding -> change [label="accepted work"];\n'
                           'change -> deploy [label="release process"];\n'
                           'deploy -> job [label="target state"];\n'
                           'finding -> job [label="selected finding",style=dashed];\n'
                           'job -> result [label="linked evidence"];\n'),
 'finops-integrations': ('Data-source access and collaboration connections',
                         'AWS source access is controlled by the agent data role. Collaboration uses '
                         'account-level registration and an agent-specific destination. Successful '
                         'source retrieval and successful publication are independent checks.',
                         ['F-08', 'F-05'],
                         '\n'
                         'rankdir=TB;\n'
                         'dataRole [label="Agent data role\\nSpecific AWS actions and scope"];\n'
                         'aws [label="AWS cost and operational services\\nQueries and recommendation '
                         'reads"];\n'
                         'agent [label="Agent task\\nAnalysis and result"];\n'
                         'registration [label="Account integration\\nJira site or Slack workspace"];\n'
                         'connection [label="Agent connection\\nSelected project or channel"];\n'
                         'action [label="Publication action\\nDestination-specific approval '
                         'behavior"];\n'
                         'dataRole -> aws [label="authorizes reads"];\n'
                         'aws -> agent [label="returns evidence"];\n'
                         'registration -> connection [label="destination binding"];\n'
                         'connection -> action [label="permits destination"];\n'
                         'agent -> action [label="requested result publication"];\n'),
 'finops-context': ('Persistent context and session-local working state',
                    'Uploaded files and conversational memory persist within an instance. They are '
                    'loaded into an isolated ephemeral session runtime. Older messages may be '
                    'summarized; that is separate from editing a file or a retained preference.',
                    ['F-M02', 'F-M03', 'F-M04'],
                    '\n'
                    'rankdir=TB;\n'
                    'files [label="Uploaded context files\\nOperator-maintained reference"];\n'
                    'memory [label="Persistent memory\\nPreferences and corrections"];\n'
                    'conversation [label="Conversation history\\nMessages and current task"];\n'
                    'runtime [label="Isolated session runtime\\nWorking context and tool '
                    'observations"];\n'
                    'summary [label="Context compaction\\nOlder messages summarized"];\n'
                    'result [label="Task result or artifact\\nRetained output record"];\n'
                    'files -> runtime [label="loaded / read"];\n'
                    'memory -> runtime [label="loaded / applied"];\n'
                    'conversation -> runtime [label="session context"];\n'
                    'conversation -> summary [label="context limit"];\n'
                    'summary -> runtime [label="condensed history"];\n'
                    'runtime -> result;\n'),
 'finops-automation': ('Anomaly-to-task and publication workflow',
                       'A supported anomaly event matches a configured automation and creates a queued '
                       'task. Result generation and destination publication are separate stages; '
                       'authorization depends on action and invocation path.',
                       ['F-M05', 'F-M06'],
                       '\n'
                       'rankdir=TB;\n'
                       'monitor [label="Cost Anomaly Detection\\nMonitor produces event"];\n'
                       'rule [label="Managed EventBridge rule\\nEvent and permission conditions"];\n'
                       'automation [label="Automation\\nInvestigation and destination definition"];\n'
                       'queue [label="Shared task queue\\nDistinct task execution"];\n'
                       'analysis [label="Source-backed analysis\\nCosts, recommendations, changes"];\n'
                       'result [label="Result and artifact\\nEvidence and unresolved questions"];\n'
                       'jira [label="Jira publication\\nAutomation pre-authorization"];\n'
                       'slack [label="Slack publication\\nNo per-action approval prompt"];\n'
                       'monitor -> rule [label="event"];\n'
                       'rule -> automation [label="matches"];\n'
                       'automation -> queue [label="creates task"];\n'
                       'queue -> analysis;\n'
                       'analysis -> result;\n'
                       'result -> jira [label="configured Jira action"];\n'
                       'result -> slack [label="configured Slack action"];\n'),
 'shared-handoff': ('Team-managed evidence handoff',
                    'An operational finding can become input to separate security and cost work. Each '
                    'receiving service uses its own configuration and authorization; only identifiers, '
                    'evidence references, and decisions are handed over.',
                    ['A-08', 'A-06'],
                    '\n'
                    'rankdir=TB;\n'
                    'incident [label="Operational investigation\\nService, time window, revision"];\n'
                    'handoff [label="Reviewed handoff\\nEvidence references and open questions"];\n'
                    'security [label="Security assessment\\nIts own application scope and identity"];\n'
                    'finops [label="Cost investigation\\nIts own query basis and data role"];\n'
                    'owner [label="Engineering owners\\nReview results and authorize changes"];\n'
                    'verification [label="Independent verification\\nSource measurements and scoped '
                    'tests"];\n'
                    'incident -> handoff [label="team review"];\n'
                    'handoff -> security [label="application evidence",style=dashed];\n'
                    'handoff -> finops [label="service and period",style=dashed];\n'
                    'security -> owner [label="finding evidence"];\n'
                    'finops -> owner [label="cost evidence"];\n'
                    'owner -> verification [label="controlled follow-up"];\n')}


def build():
    out=ROOT/'assets/diagrams';out.mkdir(parents=True,exist_ok=True)
    ns='{http://www.w3.org/2000/svg}'
    for key,(title,description,sections,dot) in DIAGRAMS.items():
        src='digraph G { graph [bgcolor="transparent",pad="0.25",nodesep="0.35",ranksep="0.6",fontname="DejaVu Sans",fontsize=16]; node [shape=box,style="rounded,filled",fillcolor="#edf5f4",color="#496b78",fontcolor="#142c3e",fontname="DejaVu Sans",fontsize=14,margin="0.18,0.12"]; edge [color="#496b78",fontname="DejaVu Sans",fontsize=11,arrowsize=0.75];\n'+dot+'\n}'
        proc=subprocess.run(['dot','-Tsvg'],input=src,text=True,capture_output=True,check=True)
        root=ET.fromstring(proc.stdout)
        for child in list(root):
            if child.tag in (ns+'title',ns+'desc'):root.remove(child)
        t=ET.Element(ns+'title',{'id':key+'-title'});t.text=title
        d=ET.Element(ns+'desc',{'id':key+'-desc'});d.text=description
        root.insert(0,t);root.insert(1,d)
        root.set('role','img');root.set('aria-labelledby',key+'-title '+key+'-desc')
        root.set('data-diagram',key)
        ET.register_namespace('',ns[1:-1]);ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
        (out/(key+'.svg')).write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
    return len(DIAGRAMS)


DIAGRAMS['devops-knowledge']=(
    'Environment-knowledge consolidation',
    'Discovery, connected evidence, and completed investigations feed distinct retained knowledge. A later execution selects the relevant context; it still reads current source evidence.',
    ['D-M08','D-05'],r"""
rankdir=TB;
sources [label="Environment evidence\nResources, repositories, pipelines, telemetry"];
history [label="Completed investigations\nObserved tool use and outcomes"];
learning [label="Managed learning\nSynthesis and refresh"];
map [label="Environment understanding\nServices, components, request paths"];
deps [label="Dependencies and pipelines\nRelationships and delivery stages"];
tools [label="Tool-use guidance\nQuery patterns and recurring errors"];
selection [label="Later execution\nSelect relevant stored context"];
sources -> learning [label="environment inputs"];
history -> learning [label="operational experience"];
learning -> map;
learning -> deps;
learning -> tools;
map -> selection [label="relevant descriptions"];
deps -> selection;
tools -> selection;
""")


DIAGRAMS['workflow-feature-map']=(
'Outcome, workflow, mechanism, and feature relationships',
'An authored documentation model: each workflow step declares a dependency on a documented mechanism and concrete feature configuration. Reverse links support impact review. This is not an AWS runtime design.',
['A-09'],r"""
rankdir=TB;
outcome [label="Operational objective\nActor and completion criteria"];
variant [label="Variant\nScope, trigger, network, format"];
step [label="Workflow step\nPurpose and responsible actor"];
mechanism [label="Documented mechanism\nTrigger, state, process, effect"];
feature [label="Platform feature\nResources and supported operations"];
recipe [label="Implementation profile\nValues, permissions, checks, failure handling"];
evidence [label="Verification evidence\nObservable result and limitations"];
outcome -> step [label="is carried out through"];
variant -> step [label="conditions a dependency"];
step -> mechanism [label="requires / optionally uses"];
mechanism -> feature [label="implemented with"];
recipe -> feature [label="configures"];
recipe -> step [label="binds to environment"];
step -> evidence [label="accepted using"];
""")



# The canonical resource register supplies specialized ER figures.
from resource_model import diagram_definitions
DIAGRAMS.update(diagram_definitions())

if __name__=='__main__':
    print(build())
