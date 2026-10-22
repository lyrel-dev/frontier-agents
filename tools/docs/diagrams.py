"""Logical diagrams. DOT definitions are maintained here; SVG is generated locally."""
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
DIAGRAMS={
'agent-execution':('Agent execution and evidence cycle','A task and its configuration guide an execution. Authorized tools return observations. Those observations can lead to another step or a result. Retention is a separate, product-specific path.',['A-00'],r'''
rankdir=LR;
request [label="Request or event\nTask and scope"];
context [label="Applicable configuration\nInstructions and context"];
run [label="Agent execution\nSelect the next step"];
tool [label="Authorized tool or assessment\nQuery or permitted operation"];
result [label="Result\nAnswer, finding, or artifact"];
request -> run [label="starts"];
context -> run [label="supplies context"];
run -> tool [label="invokes"];
tool -> run [label="returns observations"];
run -> result [label="produces"];
'''),
'devops-architecture':('DevOps Agent resource and execution architecture','Account-level providers and roles are associated with an Agent Space. An execution uses the selected tools and context; learning creates knowledge for later executions.',['D-01'],r'''
rankdir=TB;
subgraph cluster_account {label="Account configuration";color="#a9bbc7";style="rounded";providers [label="Provider registrations\nAuthentication and endpoints"];roles [label="AWS account roles\nResource and operator access"];}
space [label="Agent Space\nAssociations and selected tools"];
definition [label="Agent configuration\nInstructions, skills, store access"];
run [label="Investigation or invocation\nCurrent task and evidence"];
sources [label="Connected sources\nTelemetry, code, deployment data"];
learning [label="Managed learning\nEnvironment and incident context"];
memory [label="Knowledge and memory\nDescriptions, content, versions"];
output [label="Execution record\nFindings, tool results, status"];
providers -> space [label="associate"];
roles -> space [label="scope access"];
space -> definition [label="configures"];
definition -> run [label="used by"];
run -> sources [label="authorized queries"];
sources -> run [label="observations"];
run -> output [label="records"];
output -> learning [label="prior work"];
learning -> memory [label="synthesizes"];
memory -> run [label="selected context",style=dashed];
'''),
'devops-integrations':('Provider registration and Agent Space association','Provider authentication is registered at account level. Association and tool selection make an explicit subset available to the Agent Space. The invocation still needs a working authenticated route.',['D-12','D-03'],r'''
rankdir=LR;
provider [label="External provider\nTelemetry, code, or tool service"];
registration [label="Account registration\nEndpoint and authentication"];
association [label="Agent Space association\nSelected resources or tools"];
invocation [label="Tool invocation\nArguments and execution identity"];
observation [label="Source result\nResource ID and timestamp"];
provider -> registration [label="authorize"];
registration -> association [label="associate"];
association -> invocation [label="permits selected tool"];
invocation -> observation [label="query result"];
'''),
'devops-memory':('Incident knowledge production and selective retrieval','Prior investigations and corrective feedback are separate producers. Available store descriptions lead to relevant entry selection. Current telemetry is needed to evaluate historical context in the next investigation.',['D-M01','D-M02','D-M07'],r'''
rankdir=TB;
history [label="Prior investigations\nOutcomes and evidence"];
feedback [label="Verified correction\nActual cause and feedback"];
learning [label="Managed learning\nRecurring monitor causes"];
monitor [label="Monitor memory\nVersioned retained context"];
reflection [label="Corrective memory\nLesson from feedback"];
select [label="Retrieval\nStore and entry descriptions"];
run [label="New investigation\nHistorical context + current evidence"];
telemetry [label="Current telemetry\nNew time window and measurements"];
history -> learning [label="analyzed"];
learning -> monitor [label="synthesized"];
feedback -> reflection [label="recorded correction"];
monitor -> select [label="when available"];
reflection -> select [label="when relevant"];
select -> run [label="selected content"];
telemetry -> run [label="supports or contradicts"];
'''),
'devops-incident':('Incident triage and investigation workflow','A signal can be linked, skipped, or investigated independently. Steering affects the current analysis; completed-investigation feedback supplies a separate corrective input.',['D-06'],r'''
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
'''),
'devops-reporting':('Configured operational-report workflow','The team defines the report period and selected evidence. An invocation queries sources, produces a report, and exposes results for review. Schedule timing and the reporting window are separate configuration decisions.',['D-07'],r'''
rankdir=TB;
contract [label="Report specification\nService, window, aggregation, audience"];
definition [label="Custom-agent definition\nPrompt, tools, skills, memory"];
trigger [label="On-demand or scheduled start\nFlexible schedule window applies"];
query [label="Invocation\nQuery selected logs and metrics"];
report [label="Report\nMeasured changes and missing signals"];
review [label="Engineering review\nReproduce a material observation"];
publication [label="Approved destination\nOnly when separately configured"];
contract -> definition [label="defines the task"];
definition -> query [label="supplies configuration"];
trigger -> query [label="starts work"];
query -> report [label="synthesizes evidence"];
report -> review [label="checked"];
review -> publication [label="team publication path",style=dashed];
'''),
'security-architecture':('Security Agent application and assessment architecture','Shared account resources are selected for an application Agent Space. Assessment configuration combines sources, criteria, and authorized target access. Runs produce findings that can be reviewed and revalidated.',['S-01','S-09'],r'''
rankdir=TB;
subgraph cluster_shared {label="Shared configuration";color="#a9bbc7";style="rounded";integrations [label="Registered integrations\nRepositories and documentation"];requirements [label="Requirement packs\nApplicability and criteria"];}
space [label="Application Agent Space\nSelected sources and assigned users"];
config [label="Assessment configuration\nScope and selected evidence"];
access [label="Dynamic-test access\nTargets, exclusions, credentials"];
run [label="Assessment run\nCurrent source and target state"];
finding [label="Findings\nEvidence and affected revision"];
repair [label="Engineering remediation\nReview, test, deploy"];
revalidate [label="Revalidation job\nSelected existing finding"];
integrations -> space [label="select resources"];
space -> config;
requirements -> config [label="eligible criteria"];
access -> run [label="authorized reachability"];
config -> run [label="execute"];
run -> finding [label="records"];
finding -> repair [label="accepted work"];
repair -> revalidate [label="deployed change"];
finding -> revalidate [label="original evidence",style=dashed];
'''),
'security-integrations':('Application-source registration and selection','The account registration authorizes a provider. The application selects resources from it. Sources are shared across eligible assessments, while repository write actions are separately enabled.',['S-09'],r'''
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
'''),
'security-context':('Application context and assessment criteria','Source evidence and scope documents have different jobs. The assessment uses selected evidence and applicable criteria; a finding is an output of that execution rather than an automatically shared memory.',['S-M07','S-M03'],r'''
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
'''),
'security-authentication':('Credential retrieval and authenticated test access','Credential acquisition, login navigation, and application authorization are distinct stages. A retained login procedure can support later navigation, but actual identity still needs verification.',['S-M01','S-M02'],r'''
rankdir=TB;
source [label="Credential source\nDirect input, secret, role, or Lambda"];
resolve [label="Credential acquisition\nRead, assume, or invoke permission"];
login [label="Application login\nURL, instructions, MFA"];
role [label="Authenticated application identity\nProtected routes and permissions"];
skill [label="Login Optimization\nRetained successful procedure"];
test [label="Authorized assessment\nTarget and exclusion rules"];
source -> resolve;
resolve -> login [label="credential"];
login -> role [label="successful authentication"];
login -> skill [label="successful procedure"];
skill -> login [label="later reuse",style=dashed];
role -> test [label="actual access"];
'''),
'security-revalidation':('Finding, deployment, and revalidation lineage','The finding, proposed code change, deployed revision, and revalidation job are separate records. Revalidation repeats selected evidence using the current target and authentication configuration.',['S-M05','S-05'],r'''
rankdir=LR;
finding [label="Original finding\nEvidence and affected revision"];
change [label="Reviewed repair\nPatch and regression tests"];
deploy [label="Deployed revision\nOriginal authorized environment"];
job [label="Revalidation job\nCurrent credentials; selected steps"];
result [label="Scoped result\nReproduced or not reproduced"];
finding -> change [label="accepted work"];
change -> deploy [label="release process"];
deploy -> job [label="target state"];
finding -> job [label="selected finding",style=dashed];
job -> result [label="linked evidence"];
'''),
'finops-architecture':('FinOps Agent instance and execution architecture','The instance owns its roles, context, queue, and connections. Data sources supply evidence to a session or task, which produces an answer or artifact and may publish through a configured destination.',['F-01','F-08'],r'''
rankdir=TB;
roles [label="Access configuration\nAgent data role and operator entry"];
instance [label="Agent instance\nContext, memory, tasks, connections"];
sources [label="Authorized AWS sources\nCosts, anomalies, recommendations, changes"];
runtime [label="Conversation or task runtime\nInterpret retrieved evidence"];
context [label="Instance-local context\nFiles and retained preferences"];
result [label="Result or report artifact\nQuery basis and source evidence"];
destination [label="Connected project or channel\nAction-specific publication rules"];
roles -> instance;
instance -> runtime [label="execution configuration"];
sources -> runtime [label="query results"];
context -> runtime [label="loaded context"];
runtime -> result;
result -> destination [label="when configured"];
'''),
'finops-integrations':('Data-source access and collaboration connections','AWS source access is controlled by the agent data role. Collaboration uses account-level registration and an agent-specific destination. Successful source retrieval and successful publication are independent checks.',['F-08','F-05'],r'''
rankdir=TB;
dataRole [label="Agent data role\nSpecific AWS actions and scope"];
aws [label="AWS cost and operational services\nQueries and recommendation reads"];
agent [label="Agent task\nAnalysis and result"];
registration [label="Account integration\nJira site or Slack workspace"];
connection [label="Agent connection\nSelected project or channel"];
action [label="Publication action\nDestination-specific approval behavior"];
dataRole -> aws [label="authorizes reads"];
aws -> agent [label="returns evidence"];
registration -> connection [label="destination binding"];
connection -> action [label="permits destination"];
agent -> action [label="requested result publication"];
'''),
'finops-context':('Persistent context and session-local working state','Uploaded files and conversational memory persist within an instance. They are loaded into an isolated ephemeral session runtime. Older messages may be summarized; that is separate from editing a file or a retained preference.',['F-M02','F-M03','F-M04'],r'''
rankdir=TB;
files [label="Uploaded context files\nOperator-maintained reference"];
memory [label="Persistent memory\nPreferences and corrections"];
conversation [label="Conversation history\nMessages and current task"];
runtime [label="Isolated session runtime\nWorking context and tool observations"];
summary [label="Context compaction\nOlder messages summarized"];
result [label="Task result or artifact\nRetained output record"];
files -> runtime [label="loaded / read"];
memory -> runtime [label="loaded / applied"];
conversation -> runtime [label="session context"];
conversation -> summary [label="context limit"];
summary -> runtime [label="condensed history"];
runtime -> result;
'''),
'finops-automation':('Anomaly-to-task and publication workflow','A supported anomaly event matches a configured automation and creates a queued task. Result generation and destination publication are separate stages; authorization depends on action and invocation path.',['F-M05','F-M06'],r'''
rankdir=TB;
monitor [label="Cost Anomaly Detection\nMonitor produces event"];
rule [label="Managed EventBridge rule\nEvent and permission conditions"];
automation [label="Automation\nInvestigation and destination definition"];
queue [label="Shared task queue\nDistinct task execution"];
analysis [label="Source-backed analysis\nCosts, recommendations, changes"];
result [label="Result and artifact\nEvidence and unresolved questions"];
jira [label="Jira publication\nAutomation pre-authorization"];
slack [label="Slack publication\nNo per-action approval prompt"];
monitor -> rule [label="event"];
rule -> automation [label="matches"];
automation -> queue [label="creates task"];
queue -> analysis;
analysis -> result;
result -> jira [label="configured Jira action"];
result -> slack [label="configured Slack action"];
'''),
'shared-handoff':('Team-managed evidence handoff','An operational finding can become input to separate security and cost work. Each receiving service uses its own configuration and authorization; only identifiers, evidence references, and decisions are handed over.',['A-08','A-06'],r'''
rankdir=TB;
incident [label="Operational investigation\nService, time window, revision"];
handoff [label="Reviewed handoff\nEvidence references and open questions"];
security [label="Security assessment\nIts own application scope and identity"];
finops [label="Cost investigation\nIts own query basis and data role"];
owner [label="Engineering owners\nReview results and authorize changes"];
verification [label="Independent verification\nSource measurements and scoped tests"];
incident -> handoff [label="team review"];
handoff -> security [label="application evidence",style=dashed];
handoff -> finops [label="service and period",style=dashed];
security -> owner [label="finding evidence"];
finops -> owner [label="cost evidence"];
owner -> verification [label="controlled follow-up"];
''')}


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

if __name__=='__main__':print(build())

# The canonical resource register supplies specialized ER figures.
from resource_model import diagram_definitions
DIAGRAMS.update(diagram_definitions())
