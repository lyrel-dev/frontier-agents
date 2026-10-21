#!/usr/bin/env python3
"""Build self-contained reports and native slide decks from versioned source data.

No AWS calls are made. Historical evidence is retained; recommendations and
illustrative examples are not represented as executed product results.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, shutil, subprocess, sys, zipfile
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ['devops', 'kiro', 'security', 'finops', 'architecture']
PATHS = {'devops':'devops/validated-report.html','kiro':'kiro/report.html','security':'security/report.html','finops':'finops/report.html','architecture':'architecture/common-patterns.html'}
PPTX = {'devops':'aws-devops-agent-presentation.pptx','kiro':'kiro-presentation.pptx','security':'aws-security-agent-presentation.pptx','finops':'aws-finops-agent-presentation.pptx','architecture':'aws-frontier-agents-common-architecture-presentation.pptx'}
DATE = '21 October 2026'
E = lambda value: html.escape(str(value), quote=True)
GENERATED: list[str] = []

def put(path: str, content: str | bytes) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes): target.write_bytes(content)
    else: target.write_text(content, encoding='utf-8')
    GENERATED.append(path)

def read_json(path: str) -> dict:
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def prepare_evidence(key: str) -> dict:
    target = ROOT/'content'/f'{key}-evidence.json'
    if target.exists(): return read_json(str(target.relative_to(ROOT)))
    source = ROOT/PATHS[key]
    soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    element = soup.find('script', id='report-data')
    if element is None: raise ValueError(f'Missing retained evidence in {source}')
    data = json.loads(element.string or element.get_text())
    put(f'archive/2026-10-20/{PATHS[key]}', source.read_bytes())
    put(f'content/{key}-evidence.json', json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    return data

def source_map(data: dict) -> dict:
    return {s['id']:s for s in data['sources']}

def refs(ids: list, sources: dict, prefix: str='source') -> str:
    return ' '.join(f'<a href="#{prefix}-{E(i)}" title="{E(sources[i]["title"])}">{E(i)}</a>' for i in dict.fromkeys(ids) if i in sources)

def item_refs(item: dict) -> list:
    result = list(item.get('refs', []))
    impl = item.get('implementations', item.get('implementation', []))
    if isinstance(impl, list):
        for x in impl:
            if isinstance(x,dict): result.extend(x.get('refs',[]))
    elif isinstance(impl,dict):
        for x in impl.values():
            if isinstance(x,dict): result.extend(x.get('refs',[]))
    return list(dict.fromkeys(result))

def paragraph(text: str) -> str:
    return f'<p>{E(text)}</p>'

def definition(pairs: list[tuple[str,str]]) -> str:
    return '<dl class="definition">'+''.join(f'<dt>{E(k)}</dt><dd>{E(v)}</dd>' for k,v in pairs)+'</dl>'

def timecode(value: int) -> str:
    return f'{int(value)//60:02}:{int(value)%60:02}'

def tile(title: str, body: str, tag: str='') -> str:
    return '<div class="slide-tile">'+(f'<div class="tag">{E(tag)}</div>' if tag else '')+f'<h3>{E(title)}</h3><p>{E(body)}</p></div>'

def table(headers: list, rows: list) -> str:
    return '<div class="table-wrap"><table><thead><tr>'+''.join(f'<th scope="col">{E(h)}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{E(c)}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def slide_body(slide: dict) -> str:
    kind = slide['kind']
    if kind == 'hero':
        return '<div class="stats">'+''.join(f'<div class="stat"><strong>{E(a)}</strong><span>{E(b)}</span></div>' for a,b in slide['metrics'])+'</div>'+f'<p class="outcome">{E(slide["outcome"])}</p>'
    if kind in ('cards','flow','close'):
        items=slide['items']; cls=' two' if len(items) in (2,4) else ''
        return f'<div class="slide-grid{cls}">'+''.join(tile(x['title'],x['body'],x.get('tag','')) for x in items)+'</div>'
    if kind == 'lens':
        return '<div class="slide-grid">'+''.join(tile(label,' · '.join(slide[field]),label.upper()) for label,field in [('Inputs','inputs'),('Agent work','actions'),('Outputs','outputs')])+'</div>'
    if kind == 'compare':
        return '<div class="slide-grid two">'+''.join(tile(slide[k]['title'],slide[k]['body'],slide[k].get('tag','')) for k in ['left','right'])+'</div>'+f'<div class="notice">{E(slide.get("callout",""))}</div>'
    if kind == 'matrix': return table(slide['headers'],slide['rows'])
    if kind == 'contract': return '<pre class="sample">'+E('\n'.join(f'{k}: {v}' for k,v in slide['fields']))+'</pre>'
    if kind == 'demo':
        rows=''.join(f'<div class="demo-step"><time>{timecode(s)}</time><div><strong>{E(t)}</strong><p>{E(b)}</p></div></div>' for s,t,b in slide['steps'])
        return '<div class="demo-layout"><div><div class="kicker">Example prompt / proposed exercise</div><pre class="sample">'+E(slide['prompt'])+'</pre>'+definition([('Preflight',slide['preflight']),('Success criterion',slide['success']),('Fallback',slide['fallback'])])+'</div><div>'+rows+'</div></div>'
    raise ValueError(f'Unknown slide type: {kind}')

def presentation(deck: dict) -> str:
    options=''.join(f'<option value="{i}">{i+1:02} · {E(s["title"])}</option>' for i,s in enumerate(deck['slides']))
    controls=f'''<div class="deck-toolbar"><button id="leave-presentation">Return to report</button><button id="slide-prev" aria-label="Previous slide">←</button><select id="slide-select" aria-label="Choose slide">{options}</select><button id="slide-next" aria-label="Next slide">→</button><span id="slide-position"></span><button id="toggle-notes">Speaker notes</button><button id="timer-toggle">Start timer</button><button id="timer-reset">Reset</button><button data-print>Print slides</button><span class="timer" id="session-clock"></span></div><p class="small">Arrow keys navigate; N toggles notes; Esc returns to the report. Demo time is included. Questions and breaks are additional. The timer does not start automatically.</p>'''
    output=[]; elapsed=0
    for i,s in enumerate(deck['slides']):
        end=elapsed+s['seconds']; hero=' slide-hero' if s['kind']=='hero' else ''
        links=refs(s.get('refs',[]),deck['sources'],'deck-source')
        output.append(f'''<article class="slide{hero}" data-slide="{i}" {'hidden' if i else ''}><div class="kicker">{E(s['phase'])} / {i+1:02}</div><h2>{E(s['title'])}</h2><p class="takeaway">{E(s['takeaway'])}</p><div class="slide-body">{slide_body(s)}</div><div class="slide-foot"><span>{E(deck['title'])} · {i+1} / {len(deck['slides'])}</span><span>{timecode(s['seconds'])} allocated · {timecode(elapsed)}–{timecode(end)}</span><span>Official evidence: {links}</span></div><details class="slide-notes"><summary>Speaker notes and delivery guidance</summary>{paragraph(s['notes'])}</details></article>''')
        elapsed=end
    assert elapsed==deck['minutes']*60,(deck['title'],elapsed)
    assert sum(s['seconds'] for s in deck['slides'] if s['kind']=='demo')==deck['demo']*60
    return '<section id="presentation-view" class="presentation-view" hidden><span id="presentation"></span>'+controls+''.join(output)+'</section>'

def narrative(story: dict, evidence: dict) -> str:
    items={x['id']:x for x in evidence.get('capabilities',evidence.get('patterns',[]))}; sources=source_map(evidence)
    buttons=''.join(f'<button data-stage-button="{i}" aria-pressed="false">{i+1:02} · {E(s["title"].split(" ")[0])}</button>' for i,s in enumerate(story['stages']))
    out=['<section class="section" id="workflow"><div class="kicker">03 / The working narrative</div><h2>A complete path from question to accepted result.</h2><p>Read the full sequence, or focus on one step. Product behavior is grounded in the linked documentation; gates, example artifacts and fallback procedures are proposed team practices.</p><div class="story-controls"><button id="focus-story">Focus one workflow step</button>'+buttons+'</div>']
    for i,s in enumerate(story['stages']):
        ids=[]
        for cap in s['caps']:
            if cap in items: ids.extend(item_refs(items[cap]))
        caplinks=' · '.join(f'<a href="#cap-{E(c)}">{E(c)}</a>' for c in s['caps'])
        out.append(f'''<article class="story-stage" id="stage-{i+1}"><div class="story-head"><span class="step-number">{i+1:02}</span><div><h3>{E(s['title'])}</h3><span class="small">Capability crosswalk: {caplinks}</span></div></div><div class="story-body"><div>{''.join(paragraph(p) for p in s['paragraphs'])}</div><aside>{definition([('Input',s['input']),('Reviewable artifact',s['artifact']),('Acceptance gate',s['gate']),('When the path fails',s['fallback'])])}</aside></div><div class="evidence-strip">Documented mechanisms: {refs(ids,sources)} · Workflow sequencing and gates: author synthesis.</div></article>''')
    return ''.join(out)+'</section>'

def capabilities(key: str,evidence: dict) -> str:
    items=evidence.get('capabilities',evidence.get('patterns',[]));sources=source_map(evidence)
    groups=sorted({x.get('product',x.get('layer','Pattern')) for x in items})
    include=key in ['kiro','finops','architecture']
    out=[f'''<section class="section" id="capabilities"><div class="kicker">04 / Detailed capability reference</div><h2>What it does, what it needs, and where it stops.</h2><p>Use this reference alongside the narrative. Open an entry for setup, limitations, an example task and an independent acceptance check. Availability is feature-specific; companion products are not native DevOps Agent capabilities.</p><div class="filterbar"><label class="search-label"><span>Search capabilities and limitations</span><input id="cap-search" type="search" placeholder="Try: sandbox, evidence, approval, CI…"></label><label><span>Capability family</span><select id="cap-group"><option value="">All families</option>{''.join(f'<option>{E(x)}</option>' for x in groups)}</select></label><label class="check-label"><input type="checkbox" id="include-preview" {'checked' if include else ''}>Include preview entries</label><button id="expand-caps">Expand visible</button><button id="collapse-caps">Collapse all</button></div><p class="small" id="cap-count" role="status"></p><div class="empty" id="cap-empty" hidden>No matching entries. Clear the search or include preview capabilities.</div><div class="cap-list">''']
    for c in items:
        preview=c.get('preview',False);group=c.get('product',c.get('layer','Pattern'));companion=key=='devops' and group!='AWS DevOps Agent'
        claim=c.get('claim',c.get('rule',''));limit=c.get('limit',c.get('boundary',''));setup=c.get('setup','');check=c.get('check','');availability=c.get('availability',c.get('kind','Team architecture pattern'))
        if key=='kiro' and re.search(r'Web|cloud|sandbox',availability,re.I): availability+=' · Web surface is preview; check client-specific support'
        badge=f'<span class="pill">{E(c["id"])}</span><span class="pill">{E(group)}</span>'
        if preview:badge+='<span class="pill preview">Preview</span>'
        if companion:badge+='<span class="pill companion">Companion product</span>'
        detail=definition([('Availability / classification',availability),('Delivery',c.get('delivery','Product-specific mechanisms; proposed common pattern')),('Setup',setup)])
        detail+=f'<div class="limit"><strong>Boundary</strong><p>{E(limit)}</p></div><div class="gate"><strong>Independent acceptance</strong><p>{E(check)}</p></div>'
        if c.get('prompt'): detail+='<h4>Example prompt — not an executed test</h4><pre>'+E(c['prompt'])+'</pre>'
        if c.get('anti'):detail+='<h4>Avoid this anti-pattern</h4>'+paragraph(c['anti'])
        impl=c.get('implementations',c.get('implementation'))
        if impl:
            detail+='<details class="audit"><summary>Product-specific mechanisms</summary>'
            if isinstance(impl,list):
                for x in impl:
                    if isinstance(x,dict):detail+=paragraph(' · '.join(str(v) for k,v in x.items() if k!='refs'))+refs(x.get('refs',[]),sources)
                    else:detail+=paragraph(str(x))
            elif isinstance(impl,dict):
                for k,v in impl.items():detail+=f'<h4>{E(k)}</h4>'+paragraph(v if isinstance(v,str) else ' · '.join(str(q) for k2,q in v.items() if k2!='refs'))
            detail+='</details>'
        detail+='<div class="evidence-strip">Official documentation: '+refs(item_refs(c),sources)+'</div>'
        search=E(json.dumps(c,ensure_ascii=False).lower())
        out.append(f'<details class="cap" id="cap-{E(c["id"])}" data-search="{search}" data-group="{E(group)}" data-preview="{str(preview).lower()}"><summary><div class="badge-row">{badge}</div><h3>{E(c["title"])}</h3><p class="claim">{E(claim)}</p></summary><div class="cap-detail">{detail}</div></details>')
    return ''.join(out)+'</div></section>'

def sources_section(evidence: dict,deck: dict) -> str:
    def entries(data: list,prefix: str) -> str:
        return '<ol class="source-list">'+''.join(f'<li id="{prefix}-{E(s["id"])}"><strong>{E(s["id"])}</strong> · <a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["title"])}</a><span class="small">{E(s.get("note",s.get("scope",s.get("locator","Official product documentation"))))}</span></li>' for s in data)+'</ol>'
    allsrc=[dict(v,id=k) for k,v in deck['sources'].items()]
    return '<section class="section" id="evidence"><div class="kicker">08 / Evidence and provenance</div><h2>Claims remain attached to their source.</h2><div class="notice"><p>The original capability audit is a 20 October 2026 snapshot. Presentation source material was assembled on 21 October 2026. Selected availability and safety boundaries were rechecked for this narrative revision; this is not a fresh execution test or a claim that every external page was revalidated.</p><p>Examples, gates, fallback procedures and pilot measures are author recommendations. No AWS account was accessed, no security assessment was run, and no savings or productivity outcome was measured.</p></div><h3>Capability and narrative evidence</h3>'+entries(evidence['sources'],'source')+'<h3>Presentation evidence</h3>'+entries(allsrc,'deck-source')+'</section>'

def report_markdown(key: str,story: dict,evidence: dict,deck: dict) -> str:
    lines=[f'# {story["title"]}',story['strapline'],f'\nRevision: {DATE}. Independent engineering field guide.\n',f'**Audience:** {story["audience"]}',f'**Availability:** {story["availability"]}',f'**Recommended starting decision:** {story["decision"]}','\n## Decision brief',*story['summary'],'\n## Running use case']
    for k,v in story['use_case'].items():lines.append(f'**{k.replace("_"," ").title()}:** {v}')
    for i,s in enumerate(story['stages'],1):
        lines.extend([f'\n## {i}. {s["title"]}',*s['paragraphs'],f'**Capability crosswalk:** {", ".join(s["caps"])}'])
        for k in ['input','artifact','gate','fallback']:lines.append(f'**{k.title()}:** {s[k]}')
    lines.extend(['\n## Detailed capability reference'])
    for c in evidence.get('capabilities',evidence.get('patterns',[])):
        lines.append(f'\n### {c["id"]} — {c["title"]}')
        for k in ['claim','rule','availability','delivery','setup','limit','boundary','check','prompt','anti']:
            if c.get(k):lines.append(f'**{k.title()}:** {c[k]}')
        lines.append('Evidence: '+', '.join(item_refs(c)))
    lines.extend(['\n## Illustrative handoff','```yaml',story['handoff'],'```','\n## Readiness checklist'])
    lines.extend('- [ ] '+s for s in story['checks'])
    lines.extend(['\n## Sources'])
    lines.extend(f'- {s["id"]}: [{s["title"]}]({s["url"]})' for s in evidence['sources'])
    lines.extend(['\n## Validation boundary','Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.'])
    return '\n\n'.join(lines)+'\n'

def transcript(deck: dict) -> str:
    lines=[f'# {deck["title"]} — presentation transcript',f'{deck["minutes"]} minutes including {deck["demo"]} minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.'];elapsed=0
    for i,s in enumerate(deck['slides'],1):
        lines.extend([f'\n## {i:02}. {s["title"]}',f'**{timecode(elapsed)}–{timecode(elapsed+s["seconds"])} · {timecode(s["seconds"])} allocated**',f'**Takeaway:** {s["takeaway"]}',s['notes']]);elapsed+=s['seconds']
        if s['kind']=='demo':
            lines.extend([f'**Preflight:** {s["preflight"]}','```text',s['prompt'],'```'])
            lines.extend(f'- {timecode(t)} — **{title}:** {body}' for t,title,body in s['steps'])
            lines.extend([f'**Success:** {s["success"]}',f'**Fallback:** {s["fallback"]}'])
        for k in s.get('refs',[]):
            if k in deck['sources']:
                r=deck['sources'][k];lines.append(f'[{k} — {r["title"]}]({r["url"]})')
    return '\n\n'.join(lines)+'\n'

def report(key: str,story: dict,evidence: dict,deck: dict,css: str,js: str) -> str:
    count=len(evidence.get('capabilities',evidence.get('patterns',[])));kind='patterns' if key=='architecture' else 'capabilities'
    uc=story['use_case'];summary=''.join(paragraph(p) for p in story['summary'])
    main=f'''<section class="section" id="decision"><div class="kicker">01 / Decision brief</div><h2>{E(story['strapline'])}</h2><div class="intro-grid"><div>{summary}</div><aside class="panel decision"><h3>Recommended starting decision</h3>{paragraph(story['decision'])}{definition([('Audience',story['audience']),('Availability',story['availability'])])}</aside></div><div class="stats"><div class="stat"><strong>{count}</strong><span>Detailed {kind}</span></div><div class="stat"><strong>{deck['minutes']} min</strong><span>Presentation, including {deck['demo']} min of demos</span></div><div class="stat"><strong>6</strong><span>Narrative steps with inputs, artifacts and gates</span></div></div></section><section class="section" id="scenario"><div class="kicker">02 / Running example</div><h2>{E(uc['name'])}</h2><p class="small">Illustrative scenario, not an observed customer result or an executed demonstration.</p><div class="grid2"><div class="panel">{definition([('Trigger',uc['trigger']),('Scope',uc['scope']),('Deliverable',uc['deliverable'])])}</div><div class="panel"><div class="limit"><strong>Not done</strong>{paragraph(uc['not_done'])}</div><div class="gate"><strong>Done means</strong>{paragraph(uc['done'])}</div></div></div></section>'''
    main+=narrative(story,evidence)+capabilities(key,evidence)
    controls=''
    if key=='architecture':controls=table(['Execution path','Effect','Documented control','Proposed team control'],[[x['path'],x['effect'],x['native'],x['recommendation']] for x in evidence['controls']])
    main+=f'''<section class="section" id="controls"><div class="kicker">05 / Controls and handoff</div><h2>Accept the artifact; authorize the effect separately.</h2><p>{E(story['related'])}</p>{controls}<div class="grid2" style="margin-top:24px"><div><h3>Illustrative work contract</h3><p class="small">Product-neutral template. It is not a native agent configuration file, a credential container or an authorization token.</p><pre class="sample" id="handoff-template">{E(story['handoff'])}</pre><button data-copy="handoff-template">Copy example contract</button></div><div class="panel"><h3>Where the narrative stops</h3><p>A generated recommendation, PR, finding or cost report is evidence for a decision. It is not a universal approval to act in another product.</p><p>Verify current feature availability, integration permissions and target safety before using a workflow. Preserve unresolved evidence gaps and use the existing team process when a configured path is not available.</p><p class="small">These are proposed engineering controls, not a claim of one shared AWS permission model.</p></div></div></section>'''
    demos=[s for s in deck['slides'] if s['kind']=='demo']
    main+=f'<section class="section" id="demos"><div class="kicker">06 / Demonstrations</div><h2>Show the evidence, not a promise of autonomy.</h2><p>The {deck["demo"]}-minute allocation is included in the {deck["minutes"]}-minute session. Prepare completed, sanitized results before presenting. A fresh agent run is not guaranteed to finish inside the walkthrough slot.</p>'
    for d in demos:main+=f'<article class="panel" style="margin:22px 0"><h3>{E(d["title"])} · {timecode(d["seconds"])}</h3>{slide_body(d)}</article>'
    main+='</section>'
    checks=''.join(f'<label><input type="checkbox" data-check="{i}" data-text="{E(c)}"><span>{E(c)}</span></label>' for i,c in enumerate(story['checks']))
    pilot=evidence.get('pilot',[]);rows=[]
    for p in pilot:
        if isinstance(p,dict):rows.append([p.get('days',''),p.get('title',''),p.get('description','')])
        else:rows.append(p)
    main+=f'''<section class="section" id="readiness"><div class="kicker">07 / Adoption and acceptance</div><h2>Prove a small workflow before expanding it.</h2><div class="grid2"><div class="panel readiness"><h3>Local readiness worksheet</h3><p class="small">Checks are manually marked and stored only in this browser. They are not tests, approvals or a certification.</p><div class="progress-track"><div class="progress-fill" id="readiness-fill"></div></div><p id="readiness-count" class="small" role="status"></p>{checks}<div class="actions" style="margin-top:20px"><button id="export-checks">Export worksheet</button><button id="clear-checks">Clear checks</button></div></div><div><h3>Proposed 30-day pilot</h3>{table(['Window','Focus','Acceptance work'],rows)}<div class="notice">Track accepted results, review effort, rework, boundary failures and unfinished work. Do not substitute output volume or projected savings for verified outcomes.</div></div></div></section>'''
    main+=sources_section(evidence,deck)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(story['title'])}: a detailed, source-linked engineering field guide with narrative workflows, capabilities and a timed presentation."><title>{E(story['title'])} | Frontier agents field guide</title><style>{css}</style></head><body data-agent="{key}" data-seconds="{deck['minutes']*60}" style="--accent:{story['accent']}"><a class="skip" href="#decision">Skip to report</a><header class="masthead"><div class="wrap"><a href="../index.html">← Frontier agents / report collection</a><div class="eyebrow">Engineering field guide / {story['number']} / Narrative edition</div><h1>{E(story['title'])}</h1><p class="lead">{E(story['strapline'])}</p><div class="meta"><span class="pill">{DATE}</span><span class="pill">{count} {kind}</span><span class="pill">{len(deck['slides'])} timed slides</span><span class="pill">Documentation synthesis, not runtime testing</span></div><div class="actions"><button data-present>Open timed presentation</button><a class="button" href="../presentations/{PPTX[key]}" download>PowerPoint</a><a class="button" href="report.md" download>Report as Markdown</a><a class="button" href="presentation-transcript.md" download>Presentation transcript</a><button data-print>Print report</button></div></div></header><nav class="topnav" aria-label="Report sections"><div class="wrap navinner"><a href="#decision">Decision brief</a><a href="#scenario">Use case</a><a href="#workflow">Narrative</a><a href="#capabilities">Capabilities</a><a href="#controls">Controls</a><a href="#demos">Demos</a><a href="#readiness">Pilot</a><a href="#evidence">Evidence</a></div></nav><main class="wrap report-view">{main}</main>{presentation(deck)}<footer class="footer"><div class="wrap"><strong>Independent engineering analysis.</strong> Not an AWS publication or an implemented multi-agent architecture. Official links support product mechanisms; workflow sequencing, gates and examples are author synthesis. <a href="../VALIDATION.md">Validation record</a> · <a href="../index.html">All reports</a></div></footer><div id="toast" class="toast" role="status" hidden></div><script>{js}</script></body></html>'''

def index(config: dict,decks: dict,css: str,js: str) -> str:
    cards=[];rows=[]
    for key in AGENTS:
        story=config['agents'][key];d=decks[key];path=PATHS[key]
        cards.append(f'''<article class="card portfolio-card" data-portfolio style="--card-accent:{story['accent']}"><div class="kicker">Field guide {story['number']}</div><h3>{E(story['title'])}</h3><p>{E(story['strapline'])}</p><p class="small">{E(story['availability'])}</p><p><strong>Use case:</strong> {E(story['use_case']['name'])}</p><p class="small">{len(d['slides'])} slides · {d['minutes']} minutes including {d['demo']} minutes of demos</p><div class="actions"><a class="button primary" href="{path}">Read report</a><a class="button" href="{path}#presentation">Present</a><a class="button" href="presentations/{PPTX[key]}" download>PPTX</a></div></article>''')
        rows.append([story['title'],story['use_case']['deliverable'],story['use_case']['done']])
    main='<section class="section"><div class="kicker">Choose the engineering job</div><h2>Five reports. One consistent decision framework.</h2><p>Each guide connects a concrete problem to the product capabilities, required context, reviewable artifacts, effect-specific controls and independent acceptance. Detailed report reading and timed presentation are separate modes.</p><label class="search-label"><span>Find a report by task or audience</span><input id="portfolio-filter" type="search" placeholder="Try: cost, security, incident, code…"></label><div class="grid2" style="margin-top:24px">'+''.join(cards)+'</div></section><section class="section"><div class="kicker">Consolidated perspective</div><h2>Choose by the evidence and outcome you need.</h2>'+table(['Guide','Reviewable artifact','Acceptance boundary'],rows)+'</section><section class="section"><h2>How to use the collection</h2><div class="grid3">'+tile('Read the story','Start with the running use case, then follow its six steps. Inputs, outputs, gates and failure paths stay visible.','01')+tile('Inspect a capability','Search the detailed inventory. Check the delivery mechanism, availability, prerequisites and limitations before piloting.','02')+tile('Run the session','Open presentation mode or a PowerPoint deck. Demo slots include prepared-result fallbacks; questions and breaks are extra.','03')+'</div><div class="notice">The full programme is 160 minutes, including 48 minutes of demonstrations. No live AWS workflow was executed. Examples are illustrative; the FinOps teaching fixture is synthetic. These documents do not claim measured productivity, security coverage or savings.</div><div class="actions"><a class="button" href="README.md">Repository guide</a><a class="button" href="VALIDATION.md">Validation</a><a class="button" href="MANIFEST.json">File manifest</a><a class="button" href="demo-assets/agent-handoff.example.yaml" download>Handoff template</a><a class="button" href="dist/frontier-agents-document-suite.zip" download>Download document package</a></div></section>'
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Frontier agents | Engineering field guides</title><style>{css}</style></head><body data-agent="portfolio"><a class="skip" href="#collection">Skip to collection</a><header class="masthead"><div class="wrap"><div class="eyebrow">AWS frontier agents / Independent engineering field guides</div><h1>From capability lists<br>to engineering decisions.</h1><p class="lead">Detailed interactive reports, concrete use cases and timed presentations for DevOps, software, security and cost teams.</p><div class="meta"><span class="pill">5 field guides</span><span class="pill">71 capabilities + 12 patterns</span><span class="pill">88 timed slides</span><span class="pill">160 min including demos</span></div></div></header><main class="wrap" id="collection">{main}</main><footer class="footer"><div class="wrap">Revision {DATE}. Official sources are linked at claim level. Not an AWS publication or an executed deployment design. Download or clone the repository and open index.html; no server is required. Repository storage is not the same as a deployed GitHub Pages site.</div></footer><script>{js}</script></body></html>'

def static_checks() -> dict:
    errors=[];count=0;links=0
    for rel in ['index.html',*PATHS.values(),'devops/initial-report.html']:
        p=ROOT/rel
        if not p.exists():errors.append('Missing '+rel);continue
        soup=BeautifulSoup(p.read_text(),'html.parser');count+=1
        ids=[e.get('id') for e in soup.find_all(id=True)]
        if len(ids)!=len(set(ids)):errors.append('Duplicate IDs in '+rel)
        for a in soup.find_all('a',href=True):
            h=a['href'];links+=1
            if h.startswith(('https:','http:','mailto:','data:')):continue
            path,_,anchor=h.partition('#')
            target=(p.parent/path).resolve() if path else p
            if not target.exists():errors.append(f'{rel}: missing {h}')
            elif anchor:
                target_ids=ids if target==p else [e.get('id') for e in BeautifulSoup(target.read_text(),'html.parser').find_all(id=True)]
                if anchor not in target_ids:errors.append(f'{rel}: missing anchor {h}')
        if rel in PATHS.values():
            if len(soup.select('.story-stage'))!=6:errors.append('Incomplete narrative '+rel)
            if not soup.select('[data-slide]'):errors.append('Missing presentation '+rel)
    for key in AGENTS:
        d=read_json(f'content/{key}-presentation.json')
        if sum(x['seconds'] for x in d['slides'])!=d['minutes']*60:errors.append('Timing mismatch '+key)
        if sum(x['seconds'] for x in d['slides'] if x['kind']=='demo')!=d['demo']*60:errors.append('Demo timing mismatch '+key)
        for s in d['slides']:
            if any(r not in d['sources'] for r in s.get('refs',[])):errors.append('Unresolved presentation source '+key)
        if not (ROOT/'presentations'/PPTX[key]).exists():errors.append('Missing PPTX '+key)
    result={'html_files':count,'local_links_checked':links,'errors':errors,'timing_checks':'all five sessions and demo allocations','boundary':'Structural checks only. External links, rendered layout and live AWS behavior require separate checks.'}
    if errors:raise ValueError(json.dumps(result,indent=2))
    return result

def build() -> None:
    config=read_json('content/narratives.json');css=(ROOT/'assets/report.css').read_text();js=(ROOT/'assets/report.js').read_text();decks={};evidence={}
    for key in AGENTS:
        evidence[key]=prepare_evidence(key);decks[key]=read_json(f'content/{key}-presentation.json');story=config['agents'][key]
        put(PATHS[key],report(key,story,evidence[key],decks[key],css,js))
        put(f'{key}/report.md',report_markdown(key,story,evidence[key],decks[key]))
        put(f'{key}/presentation-transcript.md',transcript(decks[key]))
    initial=ROOT/'devops/initial-report.html';old=ROOT/'archive/2026-10-20/devops/initial-report.html'
    if initial.exists() and not old.exists():put(str(old.relative_to(ROOT)),initial.read_bytes())
    put('devops/initial-report.html','<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0; url=validated-report.html"><title>DevOps report moved</title></head><body><h1>The current DevOps report</h1><p><a href="validated-report.html">Open the detailed interactive report and timed presentation.</a></p><p><a href="../archive/2026-10-20/devops/initial-report.html">Read the historical first draft.</a></p></body></html>')
    from build_presentations import build_deck
    for key in AGENTS:
        p=ROOT/'presentations'/PPTX[key];p.parent.mkdir(exist_ok=True);build_deck(decks[key],config['agents'][key],p);GENERATED.append(str(p.relative_to(ROOT)))
    put('demo-assets/agent-handoff.example.yaml','# Illustrative team contract; not an AWS configuration or authorization.\n'+config['agents']['architecture']['handoff']+'\n')
    csv='period,day,cost_usd,data_kind\n'+''.join(f'{period},{i},{amount:.2f},synthetic\n' for period,amount in [('baseline',100),('comparison',141)] for i in range(1,15))
    put('demo-assets/finops-storage-cost-synthetic.csv',csv)
    put('demo-assets/finops-fixture-guide.md','# Synthetic FinOps teaching fixture\n\nThis is not an AWS export or a measured account result. Fourteen baseline rows total $1,400; fourteen comparison rows total $1,974. The difference is $574 / $1,400 = 41%. The deliberately simple values teach reconciliation, not realistic forecasting or causal inference.\n\nState the date window, currency, filters and cost basis before comparing real data. Do not claim an observed anomaly, causal driver or realized saving from this fixture.\n')
    put('index.html',index(config,decks,css,js))
    rows='\n'.join(f'| {config["agents"][k]["title"]} | [Report]({PATHS[k]}) | [PowerPoint](presentations/{PPTX[k]}) | {decks[k]["minutes"]} min / {decks[k]["demo"]} min demo |' for k in AGENTS)
    put('README.md','# Frontier agents — engineering field guides\n\nDetailed, source-linked interactive reports and timed presentations. Download or clone the repository and open `index.html` in a browser. No server, build step or external JavaScript is needed to read the generated reports. GitHub file previews do not execute the report HTML; repository publication is not a GitHub Pages deployment.\n\n| Guide | Interactive report | Presentation | Timing |\n|---|---|---|---|\n'+rows+'\n\nEach guide includes a six-step narrative, use-case scope, a detailed capability inventory, controls, examples, timed demos, readiness worksheet and official sources. The entire programme is 160 minutes including 48 minutes of demonstrations; questions and breaks are additional.\n\n## Documents\n\n- `*/report.md`: narrative and capability report in Markdown.\n- `*/presentation-transcript.md`: speaker transcript, timing and demo runbooks.\n- `presentations/`: five editable PowerPoint decks generated from the same slide source as the HTML presentations; one untimed evidence appendix per deck.\n- `*/validation-record.md`: retained original capability audits, unchanged.\n- `archive/2026-10-20/`: original HTML reports preserved for provenance.\n- `content/`: versioned narrative, presentation and evidence source data.\n- `demo-assets/`: product-neutral contract and explicitly synthetic cost fixture.\n- `MANIFEST.json`, `VALIDATION.md`: file integrity and validation scope.\n\n## Rebuild\n\n```sh\npython -m pip install beautifulsoup4==4.13.4 python-pptx==1.0.2\npython tools/build_suite.py\npython tools/build_suite.py --check\n```\n\nThe documentation workflow builds and checks the suite and commits each generated file separately. Existing Git history and unrelated repository files are not replaced. The historical PowerPoint edition is superseded by the report-aligned, editable publication edition; it is not a byte-for-byte copy of the earlier image-led decks.\n\n## Evidence boundary\n\nIndependent analysis, not an AWS publication. The original audits are 20 October 2026 snapshots; the presentation source and narrative revision are dated 21 October. Selected critical product boundaries were rechecked, not every source page. Examples and gates are recommendations. No live AWS account or agent workflow was exercised, and no productivity, diagnostic accuracy, security coverage or cost savings are claimed.\n')
    put('CHANGELOG.md','# Publication revision — 21 October 2026\n\nAdded five detailed narrative reports with six-stage use cases, explicit input/output contracts, failure paths and acceptance gates. Preserved the capability audits and original HTML reports. Added the portfolio index, report Markdown, source-aligned PowerPoint decks, timed transcripts, synthetic demo assets and reproducible build. Presentation budgets remain 35, 32, 30, 27 and 36 minutes, including demonstrations.\n\nPowerPoint publication decks are rebuilt from the 88-slide HTML presentation source. Decorative title imagery from the earlier 61-slide edition is not reused; core content is editable and each deck has an additional untimed evidence appendix.\n')
    put('VALIDATION.md','# Validation boundary\n\n## Evidence\n\nOriginal capability audits are retained as 20 October 2026 snapshots. The source-linked presentation material and this narrative revision are dated 21 October 2026. Selected availability, execution and authorization boundaries were rechecked against official AWS and Kiro documentation; this is not a new claim-by-claim audit of every URL.\n\n## Build checks\n\nThe build checks local paths and anchors, unique HTML IDs, narrative completeness, all five presentation and demonstration budgets, presentation reference IDs and PowerPoint existence. `qa/build-validation.json` records the structural results. Browser checks, when available, are recorded separately in `qa/browser-validation.json`; absence of that file does not imply they passed.\n\n## Not tested\n\nNo live AWS accounts, repositories, deployments, agent runs, penetration tests or purchasing workflows were exercised. Demonstration budgets include prepared-result fallback paths and are not agent-runtime guarantees. The cost fixture is synthetic. No measured reliability, accuracy, security-detection, productivity or savings outcomes are claimed.\n\n## Publication\n\nRepository visibility and hosting settings are not changed by the build. The generated HTML works locally. Publishing files to GitHub does not automatically enable GitHub Pages. Historical audits, code revisions and unrelated files remain intact.\n')
    (ROOT/'dist').mkdir(exist_ok=True);(ROOT/'dist/frontier-agents-document-suite.zip').touch(exist_ok=True)
    put('MANIFEST.json','{}\n')
    result=static_checks();put('qa/build-validation.json',json.dumps(result,indent=2)+'\n')
    files={}
    for p in sorted(ROOT.rglob('*')):
        rel=str(p.relative_to(ROOT))
        if p.is_file() and not any(x in p.parts for x in ['.git','__pycache__']) and rel not in ['MANIFEST.json'] and not rel.startswith('dist/'):
            files[rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    put('MANIFEST.json',json.dumps({'revision':config['revision'],'files':files,'excluded':['MANIFEST.json itself','dist/ convenience archives','.git/','__pycache__/']},indent=2)+'\n')
    target=ROOT/'dist/frontier-agents-document-suite.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in [*files,'MANIFEST.json']:z.write(ROOT/rel,rel)
    GENERATED.append(str(target.relative_to(ROOT)))
    print(json.dumps({'generated':len(set(GENERATED)),'structural_checks':result,'package':str(target)},indent=2))

def commit_files() -> None:
    def git(*args: str) -> bytes:return subprocess.check_output(['git','-C',str(ROOT),*args])
    paths=set(x for x in (git('diff','--name-only','-z')+git('ls-files','--others','--exclude-standard','-z')).decode().split('\0') if x)
    for path in sorted(paths):
        if path.startswith('.git/') or '__pycache__' in path:continue
        git('add','--',path);git('commit','-m',f'docs: publish {path}','--',path)
    print(f'Committed {len(paths)} changed files separately.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--commit',action='store_true');args=parser.parse_args()
    if args.check:print(json.dumps(static_checks(),indent=2))
    elif args.commit:commit_files()
    else:build()
