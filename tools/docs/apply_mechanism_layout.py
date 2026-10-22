"""One-time renderer and presentation integration for the reviewed mechanism edition."""
from pathlib import Path
from pprint import pformat
import ast
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))

def patch(path,old,new,count=1):
    p=ROOT/path;text=p.read_text()
    if text.count(old)!=count:raise ValueError(f'{path}: expected {count} anchors, found {text.count(old)} for {old[:80]!r}')
    p.write_text(text.replace(old,new))

retired={'devops-memory','security-authentication','security-revalidation','finops-context','finops-automation'}
p=HERE/'diagrams.py';text=p.read_text();tree=ast.parse(text)
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIAGRAMS' for t in n.targets))
old=ast.literal_eval(node.value)
for key in retired:old.pop(key,None)
lines=text.splitlines(keepends=True)
text=''.join(lines[:node.lineno-1])+'DIAGRAMS='+pformat(old,width=105,sort_dicts=False)+'\n'+''.join(lines[node.end_lineno:])
text=text.replace("if __name__=='__main__':","from mechanism_figures import DIAGRAMS as MECHANISM_DIAGRAMS\nDIAGRAMS.update(MECHANISM_DIAGRAMS)\n\nif __name__=='__main__':")
p.write_text(text)
for key in retired:(ROOT/f'assets/diagrams/{key}.svg').unlink(missing_ok=True)
for product in ('devops','security','finops'):
    p=ROOT/f'guides/{product}.md';text=p.read_text()
    for key in retired:text=re.sub(r'^!\[[^\n]*\]\(\.\./assets/diagrams/'+re.escape(key)+r'\.svg\)\n*','',text,flags=re.M)
    p.write_text(text)

patch('tools/docs/build.py','import resource_model\n','import resource_model\nimport mechanism_detail\n')
patch('tools/docs/build.py','renderer does not modify either source.','renderer preserves authored prose and regenerates delimited mechanism-detail blocks from the registry.')
patch('tools/docs/build.py','    build_diagrams();guides=load_guides();catalog=load_catalog()',
 '    mechanism_detail.sync_guides()\n    build_diagrams();guides=load_guides();catalog=load_catalog()')
patch('tools/docs/build.py',"    soup=BeautifulSoup(MD.render(text+'\\n\\n'+definitions),'html.parser')",
 "    text=re.sub(r'^<!-- mechanism-review:(?:start|end) [^>]+ -->\\s*$', '', text, flags=re.M)\n    soup=BeautifulSoup(MD.render(text+'\\n\\n'+definitions),'html.parser')\n    for heading in soup.find_all('h4'):\n        match=re.match(r'(MX-[A-Z]-[A-Z]+)\\s+[—-]\\s+',heading.get_text())\n        if match:heading['id']=(prefix+'-'+match[1]) if '-note' in prefix else match[1]")
patch('tools/docs/build.py','## Product resource models\\n\\n',
 '## Mechanism configuration and lifecycle\\n\\nThe [mechanism index](catalog/mechanisms.html) links to reviewed procedures in each guide: triggers, inputs, state changes, configuration, controls, observable results and explicitly unexecuted verification plans. See the [Stage 3 review](qa/mechanism-review.json) and [claim-level source record](qa/mechanism-source-review.json). The 30 approved outcomes are unchanged.\\n\\n## Product resource models\\n\\n')
patch('tools/docs/build.py','Edit guide prose in `guides/*.md`,',
 'Edit guide prose outside the delimited generated blocks in `guides/*.md`; edit detailed mechanism prose and its claim references in the `review` fields of `catalog/mechanisms.json`. The build synchronizes those blocks before rendering. Edit')
patch('tools/docs/interactions.js',"      if(target.matches('.report-section,.chapter'))reset();\n      const nav=$$('.toc a').find(a=>a.getAttribute('href')==='#'+id);",
 "      const section=target.closest('.report-section');\n      if(target.matches('.report-section,.chapter')||section)reset();\n      const navId=section?section.id:id;\n      const nav=$$('.toc a').find(a=>a.getAttribute('href')==='#'+navId);")
patch('tools/docs/catalog.py','import re\n','import re\nfrom mechanism_detail import index_summary\n')
patch('tools/docs/catalog.py',"                rows=related(ident)","                parts.append(index_summary(item))\n                rows=related(ident)")

import presentation
replacements={
 'devops-memory':('mechanism-devops-retrieval',['D-M01','D-M02','D-M07'],'Memory production, availability and selective retrieval','Separate retained content, access to the entry, observable retrieval and the correctness of the new conclusion.'),
 'security-authentication':('mechanism-security-learning',['S-M01','S-M02','S-05'],'Authentication reuse and finding personalization','Login Optimization reuses navigation. Findings Personalization reuses eligible edits. Neither establishes that the application was repaired.'),
 'security-revalidation':('mechanism-security-replay',['S-M05','S-05'],'Finding replay and verification boundaries','Revalidation creates a linked job. Interpret non-reproduction only after checking the actual target, identity and reached path.'),
 'finops-context':('mechanism-finops-context',['F-M02','F-M03','F-M04'],'Files, memory and conversation-context lifecycles','Soft deletion and restoration apply to files. Forgetting updates memory. Compaction changes working context; these operations are not interchangeable.'),
 'finops-automation':('mechanism-finops-publication',['F-03','F-M05','F-M06'],'Task execution and destination-specific approval','A matching event or schedule creates work. Analysis and publication are separate; Jira approval depends on invocation mode and Slack has no per-message prompt.')}
seen=set()
for product,deck in presentation.DECKS.items():
    for slide in deck['slides']:
        key=slide.get('diagram')
        if key in replacements:
            diagram,refs,title,message=replacements[key]
            slide.update(diagram=diagram,refs=refs,title=title,message=message);seen.add(key)
        if product=='devops' and slide['title'].casefold().startswith('custom agents, schedules'):
            slide.update(kind='diagram',diagram='mechanism-devops-cancellation',data=[],refs=['D-07'],title='Stopping future triggers and current invocations',message='Pause the trigger to stop future starts. Cancel the invocation separately; an in-flight tool call can still complete and previously completed evidence remains.')
assert seen==set(replacements),('Missing slide replacement',set(replacements)-seen)
(HERE/'presentation.py').write_text('"""HTML lessons with reviewed mechanism lifecycles; timing budgets remain unchanged."""\nDECKS='+pformat(presentation.DECKS,width=105,sort_dicts=False)+'\n')
Path(__file__).unlink()
