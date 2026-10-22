"""Logical mechanism views; colors use the approved concept-ownership convention."""
PALETTE='''
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];
'''

def view(title,description,refs,dot):
    return (title,description+' Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.',refs,PALETTE+dot)

DIAGRAMS={
'mechanism-devops-retrieval':view('Incident memory: production, availability and retrieval',
'Producing context does not prove a later execution selected it. Activation and applicable attachments control availability; current evidence controls interpretation.',
['D-M01','D-M02','D-M07'],r'''
history [label="AWS · Prior investigations\nRecorded evidence and conclusions"];
feedback [label="AWS · Investigation feedback\nOperator-supplied correction"];
store [label="AWS · Retained entry\nDescription, content and version"];
available [label="AWS · Available context\nActive state; applicable attachment"];
select [label="AWS · Select and read\nStore then entry descriptions"];
current [label="EXT · Current observations\nNew incident time window",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
review [label="DOC · Memory verification\nEntry identity, observed access, current evidence",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
history -> store [label="managed synthesis"];
feedback -> store [label="corrective context"];
{rank=same;history;feedback}
store -> available [label="activation and scope"];
available -> select [label="relevant description"];
select -> review [label="selected history",style=dashed];
current -> review [label="supports or contradicts",style=dashed];
{rank=same;select;current}
'''),
'mechanism-devops-cancellation':view('Custom work: future triggers and current invocations',
'Pausing a schedule stops future starts. Cancelling an invocation preserves completed evidence and may not interrupt a tool call already in progress. The scheduling window is not a delivery SLA.',
['D-07'],r'''
definition [label="AWS · Custom definition\nPrompt, tools, skills, store access"];
trigger [label="AWS · Schedule trigger\nActive or paused"];
run [label="AWS · Invocation\nSeparate execution and trajectory"];
call [label="EXT · Tool operation\nAlready-started external work",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
record [label="AWS · Retained trajectory\nCompleted calls and outputs"];
check [label="DOC · Stop verification\nFuture starts and in-flight effects",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
definition -> run [label="loads configuration"];
trigger -> run [label="eligible future occurrence"];
run -> call [label="invokes"];
run -> record [label="cancel retains completed work"];
call -> check [label="may complete after cancellation",style=dashed];
record -> check [label="inspect actual outcome",style=dashed];
{rank=same;definition;trigger}
{rank=same;call;record}
'''),
'mechanism-security-learning':view('Security reuse: login navigation and finding preferences',
'The two retained processes have different producers and effects. Disabling reuse or personalization preserves learned material; neither operation repairs the application.',
['S-M02','S-05'],r'''
login [label="AWS · Successful login\nCurrent credential and navigation"];
procedure [label="AWS · Login procedure\nLogin Optimization setting"];
nextlogin [label="AWS · Later login\nAuthenticated application session"];
edit [label="AWS · Eligible finding edits\nMost recent completed test run"];
preference [label="AWS · Finding preferences\nPersonalization enabled at test start"];
nextfinding [label="AWS · Later similar finding\nOriginal and personalized attributes"];
review [label="DOC · Engineering verification\nConfirm session identity and finding changes",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
login -> procedure [label="learns navigation"];
procedure -> nextlogin [label="reuse when enabled"];
edit -> preference [label="learns eligible changes"];
preference -> nextfinding [label="apply to similar finding"];
nextlogin -> review [style=dashed];
nextfinding -> review [style=dashed];
{rank=same;login;edit}
{rank=same;procedure;preference}
{rank=same;nextlogin;nextfinding}
'''),
'mechanism-security-replay':view('Finding revalidation: evidence and result boundaries',
'Revalidation creates a separate job for selected existing findings. Non-reproduction must be interpreted under the identity and path actually reached; it is not broad new discovery.',
['S-M05','S-05'],r'''
finding [label="AWS · Original finding\nValidation steps and history"];
repair [label="EXT · Deployed repair\nApproved target revision",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
auth [label="AWS · Current test credentials\nAuthenticated role and route"];
job [label="AWS · Revalidation job\nRepeat selected validation steps"];
active [label="AWS · Active\nIssue reproduced"];
resolved [label="AWS · Resolved\nIssue not reproduced in this replay"];
accept [label="DOC · Acceptance check\nVerify target, role and completed path",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
finding -> job [label="selected finding"];
repair -> job [label="current deployment"];
auth -> job [label="current identity"];
job -> active;
job -> resolved;
active -> accept [style=dashed];
resolved -> accept [label="not sufficient alone",style=dashed];
{rank=same;finding;repair;auth}
{rank=same;active;resolved}
'''),
'mechanism-finops-context':view('FinOps context: three independent lifecycle operations',
'File restoration, memory updates and conversation compaction operate on different representations. Their controls do not remove copies held in other representations.',
['F-M02','F-M03','F-M04'],r'''
file [label="AWS · Active uploaded file\nOperator-maintained reference"];
deleted [label="AWS · Soft-deleted file\nNot active context"];
memory [label="AWS · Retained memory\nPreference or correction"];
updated [label="AWS · Updated memory\nRemember, update or forget"];
conversation [label="AWS · Conversation context\nOlder and recent messages"];
summary [label="AWS · Compacted context\nOlder summary + recent full messages"];
check [label="DOC · Context verification\nCheck file state, retained preference and query constraints",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
file -> deleted [label="delete"];
deleted -> file [label="restore"];
memory -> updated [label="conversational request"];
conversation -> summary [label="context approaches limit"];
file -> check [style=dashed];
updated -> check [style=dashed];
summary -> check [style=dashed];
{rank=same;file;memory;conversation}
{rank=same;deleted;updated;summary}
'''),
'mechanism-finops-publication':view('FinOps tasks and destination-specific authorization',
'Conversations can request publication directly; explicit tasks and automations use the task queue. Jira confirmation depends on invocation mode. Slack has no per-message approval prompt.',
['F-03','F-M05','F-M06'],r'''
manual [label="AWS · On-demand task request"];
chat [label="AWS · Conversation analysis\nDirect answer or action request"];
auto [label="AWS · Schedule / anomaly automation"];
task [label="AWS · Queued task and analysis\nSource reads and result"];
jira [label="AWS · Jira action\nInteractive: confirm\nAutomation: setup authorization"];
slack [label="AWS · Slack action\nNo per-message approval prompt"];
external [label="EXT · Project / channel record\nExternal audience and retention",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
check [label="DOC · Delivery verification\nInspect actual destination before retry",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
manual -> task [label="explicit task request"];
chat -> jira [label="direct requested action"];
chat -> slack [label="direct requested action"];
auto -> task [label="eligible occurrence"];
task -> jira [label="configured action"];
task -> slack [label="configured action"];
jira -> external;
slack -> external;
external -> check [style=dashed];
{rank=same;manual;auto;chat}
{rank=same;jira;slack}
''')
}
