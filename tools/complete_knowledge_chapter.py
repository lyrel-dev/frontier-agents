#!/usr/bin/env python3
"""Complete the knowledge chapter before the one-time layout migration."""
from pathlib import Path
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from docs_build import parse_source,group_markdown
from docs_structure import CHAPTERS,TYPES,LABELS,DECK_CHAPTERS

BODY='''Knowledge consolidation is the step between collecting source material and retaining a useful explanation. In DevOps Agent, managed learning produces several kinds of environment knowledge: the application and resource model, code dependencies, pipeline relationships, and effective tool-use patterns. Those stores support different questions. A service map helps locate evidence, whereas a tool-use lesson helps construct an appropriate query. [DS06] [DS07] [DS19]

| Managed store | Retained subject | Operational use |
|---|---|---|
| `understanding-agent-space` | Logical services, components, request paths, source-to-resource relationships, and observability context | Orient an investigation or review a dependency description |
| `understanding-dependencies` | Service and package dependencies | Examine upstream/downstream relationships and change scope |
| `understanding-pipeline-topology` | Pipeline steps, environments, and promotions | Interpret a deployment or release context |
| `tool-use-best-practices` | Query patterns, recurring tool errors, and output-management guidance | Avoid previously observed invocation problems |

These are informational memories, not extra permissions or a replacement for the original systems. The memory guidance describes a browsable file structure: names can represent paths, and an index leads to relevant files. This arrangement supports progressive disclosure instead of placing the entire environment model into every task. [DS07]

![Environment-knowledge consolidation](../assets/diagrams/devops-knowledge.svg)

Refresh is not one universal timer. The environment understanding begins after discovery and can be regenerated when connected repositories, pipelines, or observability integrations change. The guidance separately describes scheduled refresh for active spaces, with account changes appearing on a scheduled refresh rather than immediately. Tool-use guidance is refreshed after enough new completed investigations and is rate-limited; monitor history follows its own daily rule. Consult the memory page's current thresholds before assigning freshness expectations to an operational report. [DS07]

To inspect the result, follow the learning execution and examine the resulting memory version. The summary report is a versioned, read-only representation of the environment understanding; the topology visualizes its resource relationships. A successful connection or submitted regeneration request is not yet evidence that those views have incorporated the change. [DS04] [DS06] [DS07]

For example, after adding an inventory service, identify its deployed resources, repository, and critical request path. Compare them with the updated understanding and note any inferred or missing relationships. If a query repeatedly fails because it uses an obsolete namespace, inspect the relevant tool guidance as well as the source configuration. Correct the representation that is wrong rather than adding unrelated permissions.

A custom store serves a different authoring need. It can hold reviewed facts, service conventions, and reporting context supplied by the team. Give it a subject-specific description and keep each entry focused on information that remains useful across tasks. Raw tool output for one investigation belongs in that execution's evidence; copying it into memory is not a documented same-run cache or a substitute for the original logs. Attach the store explicitly to a custom agent that needs it, then verify retrieval against a known fact. [DS07] [DS10]'''

path=ROOT/'guides/devops.md';g=parse_source(path.read_text())
g['sections']['D-M08']={'id':'D-M08','title':'Environment-knowledge consolidation and refresh','body':BODY,'level':3}
sections=CHAPTERS['devops'][2]['sections'];sections.insert(sections.index('D-05')+1,'D-M08')
path.write_text(group_markdown('devops',g))
structure=ROOT/'tools/docs_structure.py'
structure.write_text('"""Chapter membership and record types."""\nREVISION="2026-10-22-narrative-guides"\nBASELINE="c3d6f2dafdd87e083989135690e2f4f169e80fc2"\nCHAPTERS='+repr(CHAPTERS)+'\nDECK_CHAPTERS='+repr(DECK_CHAPTERS)+'\nTYPES='+repr(TYPES)+'\nLABELS='+repr(LABELS)+'\ndef section_type(sid):\n    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]\n')
catpath=ROOT/'catalog/use-cases.json';catalog=json.loads(catpath.read_text())
for e in catalog['entries']:
    if e['id'] in ('D-UC16','D-UC17','D-UC20'):e['sections'].append('D-M08')
catpath.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
file=ROOT/'tools/docs/diagrams.py';text=file.read_text()
addition='''\nDIAGRAMS['devops-knowledge']=(
    'Environment-knowledge consolidation',
    'Discovery, connected evidence, and completed investigations feed distinct retained knowledge. A later execution selects the relevant context; it still reads current source evidence.',
    ['D-M08','D-05'],r"""
rankdir=TB;
sources [label="Environment evidence\\nResources, repositories, pipelines, telemetry"];
history [label="Completed investigations\\nObserved tool use and outcomes"];
learning [label="Managed learning\\nSynthesis and refresh"];
map [label="Environment understanding\\nServices, components, request paths"];
deps [label="Dependencies and pipelines\\nRelationships and delivery stages"];
tools [label="Tool-use guidance\\nQuery patterns and recurring errors"];
selection [label="Later execution\\nSelect relevant stored context"];
sources -> learning [label="environment inputs"];
history -> learning [label="operational experience"];
learning -> map;
learning -> deps;
learning -> tools;
map -> selection [label="relevant descriptions"];
deps -> selection;
tools -> selection;
""")\n'''
text=text.replace("if __name__=='__main__':print(build())",addition+"\nif __name__=='__main__':print(build())")
file.write_text(text)
layout=ROOT/'tools/prepare_documentation_layout.py';text=layout.read_text().replace("'devops-memory','devops-incident'","'devops-memory','devops-knowledge','devops-incident'")
text=text.replace('import json, re, shutil, sys','import json, re, shutil, sys\nfrom pprint import pformat')
text=text.replace("repr(DECKS)","pformat(DECKS,width=105,sort_dicts=False)").replace("repr(CHAPTERS)","pformat(CHAPTERS,width=105,sort_dicts=False)").replace("repr(chapters)","pformat(chapters,width=105,sort_dicts=False)").replace("repr(TYPES)","pformat(TYPES,width=105,sort_dicts=False)").replace("repr(LABELS)","pformat(LABELS,width=105,sort_dicts=False)")
layout.write_text(text)
Path(__file__).unlink()
