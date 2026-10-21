#!/usr/bin/env python3
"""Build self-contained reports and native slide decks from versioned source data.

No AWS calls are made. Source evidence is retained; recommendations and
illustrative examples are not represented as executed product results.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, shutil, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ['devops', 'security', 'finops', 'architecture']
PATHS = {'devops':'devops/validated-report.html','security':'security/report.html','finops':'finops/report.html','architecture':'architecture/common-patterns.html'}
PPTX = {'devops':'aws-devops-agent-presentation.pptx','security':'aws-security-agent-presentation.pptx','finops':'aws-finops-agent-presentation.pptx','architecture':'aws-frontier-agents-common-architecture-presentation.pptx'}
DATE = '21 October 2026'
E = lambda value: html.escape(str(value), quote=True)
GENERATED: list[str] = []

def annotation_for(annotations: dict, key: str, capability_id: str) -> dict:
    return annotations['capability_records'][key].get(capability_id, {})

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

def capability_reference_slide(c: dict, record: dict, key: str, evidence: dict, index: int, total: int, offset: int) -> str:
    """Compact reference slide; distinguish product behavior from team records."""
    sources = source_map(evidence)
    claim = c.get('claim', c.get('rule', ''))
    limit = c.get('limit', c.get('boundary', ''))
    availability = c.get('availability', c.get('kind', 'Proposed pattern'))
    status = c.get('verdict', 'Proposed architecture pattern' if key == 'architecture' else 'Documented product behavior')
    output = record.get('record', 'No recommended record specified.')
    function_label = 'Proposed architecture pattern' if key == 'architecture' else 'Documented function'
    cells = [
        (function_label, claim, ''),
        ('Invocation and scope', c.get('setup', ''), ''),
        ('Review record to retain', output, 'Team recommendation'),
        ('Independent acceptance', c.get('check', ''), 'Team recommendation'),
        ('Known limits and effects', limit, ''),
    ]
    content = '<div class="reference-grid">' + ''.join(
        '<section class="reference-panel' + (' limit-panel' if i == 4 else '') + '"><h3>' + E(title) + '</h3>'
        + (f'<span class="proposed-label">{E(tag)}</span>' if tag else '') + paragraph(body) + '</section>'
        for i, (title, body, tag) in enumerate(cells)
    ) + '</div>'
    meta = ' · '.join([status, availability, c.get('delivery', 'Team architecture pattern')])
    src = refs(item_refs(c), sources)
    prompt = ('<details class="slide-notes"><summary>Illustrative task (not executed)</summary>'
              + paragraph(c['prompt']) + '</details>') if c.get('prompt') else ''
    return (f'<article class="slide reference-slide" data-kind="reference" data-slide="{offset+index}" '
            f'data-ref-position="{index+1}/{total}" hidden><div class="kicker">UNTIMED CAPABILITY REFERENCE · {E(c["id"])}</div>'
            f'<h2>{E(c["title"])}</h2><p class="takeaway">{E(meta)}</p><div class="slide-body">{content}</div>'
            f'<div class="slide-foot"><span>{E(c["id"])} · {E(c.get("product", c.get("layer", "Pattern")))}</span>'
            f'<span>Outside the timed session</span><span>Official evidence: {src}</span></div>{prompt}</article>')


def presentation(deck: dict, evidence: dict, annotations: dict, key: str) -> str:
    items = evidence.get('capabilities', evidence.get('patterns', []))
    options = '<optgroup label="Timed core">' + ''.join(
        f'<option value="{i}">{i+1:02} · {E(s["title"])}</option>'
        for i, s in enumerate(deck['slides'])) + '</optgroup>'
    options += '<optgroup label="Untimed capability references">' + ''.join(
        f'<option value="{len(deck["slides"])+i}">{E(c["id"])} · {E(c["title"])}</option>'
        for i, c in enumerate(items)) + '</optgroup>'
    controls = (f'<div class="deck-toolbar"><button id="leave-presentation">Return to report</button>'
                f'<button id="slide-prev" aria-label="Previous slide">←</button>'
                f'<select id="slide-select" aria-label="Choose slide">{options}</select>'
                f'<button id="slide-next" aria-label="Next slide">→</button><span id="slide-position"></span>'
                f'<button id="toggle-notes">Speaker notes</button><button id="timer-toggle">Start timer</button>'
                f'<button id="timer-reset">Reset</button><button data-print>Print slides</button>'
                f'<span class="timer" id="session-clock"></span></div>'
                f'<p class="small">The core is {len(deck["slides"])} timed slides ({deck["minutes"]} minutes, including '
                f'{deck["demo"]} minutes of demonstrations). The {len(items)} individual capability references are untimed. '
                f'Arrow keys: navigate; N: notes; Esc: report. Questions and breaks are additional.</p>'
                f'<p id="reference-status" class="small" role="status" hidden>Untimed reference. Session timer paused.</p>')
    out = []
    elapsed = 0
    for i, s in enumerate(deck['slides']):
        end = elapsed + s['seconds']
        hero = ' slide-hero' if s['kind'] == 'hero' else ''
        links = refs(s.get('refs', []), deck['sources'], 'deck-source')
        out.append(
            f'<article class="slide{hero}" data-kind="timed" data-slide="{i}" {"hidden" if i else ""}>'
            f'<div class="kicker">{E(s["phase"])} / {i+1:02}</div><h2>{E(s["title"])}</h2>'
            f'<p class="takeaway">{E(s["takeaway"])}</p><div class="slide-body">{slide_body(s)}</div>'
            f'<div class="slide-foot"><span>{E(deck["title"])} · {i+1} / {len(deck["slides"])}</span>'
            f'<span>{timecode(s["seconds"])} allocated · {timecode(elapsed)}–{timecode(end)}</span>'
            f'<span>Official evidence: {links}</span></div>'
            f'<details class="slide-notes"><summary>Speaker notes and delivery guidance</summary>{paragraph(s["notes"])}</details></article>')
        elapsed = end
    assert elapsed == deck['minutes'] * 60
    assert sum(s['seconds'] for s in deck['slides'] if s['kind'] == 'demo') == deck['demo'] * 60
    for i, c in enumerate(items):
        out.append(capability_reference_slide(c, annotation_for(annotations, key, c['id']),
                                              key, evidence, i, len(items), len(deck['slides'])))
    return '<section id="presentation-view" class="presentation-view" hidden><span id="presentation"></span>' + controls + ''.join(out) + '</section>'


def narrative(story: dict, evidence: dict, annotations: dict, key: str) -> str:
    items = {x['id']: x for x in evidence.get('capabilities', evidence.get('patterns', []))}
    sources = source_map(evidence)
    buttons = ''.join(f'<button data-stage-button="{i}" aria-pressed="false">{i+1:02} · {E(s["title"].split(" ")[0])}</button>' for i, s in enumerate(story['stages']))
    out = ['<section class="section" id="workflow"><div class="kicker">03 / Use-case execution sequence</div>'
           '<h2>Steps, responsibility, review records and acceptance</h2>'
           '<p>Each step separates documented product mechanisms from proposed team steps. Responsible roles, '
           'evidence-retention records, gates and fallbacks are not native agent assurances.</p>'
           '<div class="story-controls"><button id="focus-story">Focus one workflow step</button>' + buttons + '</div>']
    for i, s in enumerate(story['stages']):
        ids = []
        for cap in s['caps']:
            if cap in items:
                ids.extend(item_refs(items[cap]))
        caplinks = ' · '.join(f'<a href="#cap-{E(c)}">{E(c)}</a>' for c in s['caps'])
        owner = annotations['stage_owners'][key][i]
        fields = [
            ('Responsible role (proposed)', owner),
            ('Required input and scope', s['input']),
            ('Review record to retain (proposed)', s['artifact']),
            ('Independent acceptance gate', s['gate']),
            ('Failure / fallback', s['fallback']),
        ]
        out.append(f'<article class="story-stage" id="stage-{i+1}"><div class="story-head">'
                   f'<span class="step-number">{i+1:02}</span><div><h3>{E(s["title"])}</h3>'
                   f'<span class="small">Related capabilities: {caplinks}</span></div></div>'
                   f'<div class="story-body"><div><h4>Operation and evidence context</h4>'
                   f'{"".join(paragraph(p) for p in s["paragraphs"])}</div><aside class="contract-panel">'
                   f'{definition(fields)}</aside></div><div class="evidence-strip">Official evidence for mechanisms: '
                   f'{refs(ids, sources)} · Sequence, roles and gates: proposed team workflow.</div></article>')
    return ''.join(out) + '</section>'


def capabilities(key: str, evidence: dict, annotations: dict) -> str:
    items = evidence.get('capabilities', evidence.get('patterns', []))
    sources = source_map(evidence)
    groups = sorted({x.get('product', x.get('layer', 'Pattern')) for x in items})
    include = key in ['finops', 'architecture']
    out = [f'<section class="section" id="capabilities"><div class="kicker">04 / Capability records</div>'
           '<h2>Function, invocation, evidence, acceptance and limits</h2>'
           '<p>Every record uses the same field order. Proposed review records and acceptance checks are '
           'team practices, not guaranteed native output formats. See the '
           '<a href="../style-guide.html">editorial standard</a>.</p>'
           '<div class="filterbar"><label class="search-label"><span>Search capabilities and limitations</span>'
           '<input id="cap-search" type="search" placeholder="Try: sandbox, approval, CI…"></label>'
           '<label><span>Capability family</span><select id="cap-group"><option value="">All families</option>'
           + ''.join(f'<option>{E(x)}</option>' for x in groups) + '</select></label>'
           + f'<label class="check-label"><input type="checkbox" id="include-preview" {"checked" if include else ""}>'
           'Include preview entries</label><button id="expand-caps">Expand visible</button>'
           '<button id="collapse-caps">Collapse all</button></div><p class="small" id="cap-count" role="status"></p>'
           '<div class="empty" id="cap-empty" hidden>No matching entries.</div><div class="cap-list">']
    for c in items:
        preview = c.get('preview', False)
        group = c.get('product', c.get('layer', 'Pattern'))
        companion = key == 'devops' and group != 'AWS DevOps Agent'
        claim = c.get('claim', c.get('rule', ''))
        limit = c.get('limit', c.get('boundary', ''))
        setup = c.get('setup', '')
        check = c.get('check', '')
        availability = c.get('availability', c.get('kind', 'Proposed architecture pattern'))
        output = annotation_for(annotations, key, c['id']).get('record', 'No recommended retention record specified.')
        badges = f'<span class="pill">{E(c["id"])}</span><span class="pill">{E(group)}</span>'
        if c.get('verdict'):
            badges += f'<span class="pill">{E(c["verdict"])}</span>'
        if preview:
            badges += '<span class="pill preview">Preview</span>'
        if companion:
            badges += '<span class="pill companion">Separate product</span>'
        detail = ('<div class="cap-section"><h4>1 · Classification and scope</h4>'
                  + definition([('Availability and surface', availability),
                                ('Delivery mechanism', c.get('delivery', 'Proposed architecture pattern')),
                                ('Invocation and required scope', setup)]) + '</div>')
        detail += ('<div class="cap-section"><h4>2 · Review record to retain '
                   '<span class="proposed-label">Proposed team practice</span></h4>' + paragraph(output) + '</div>')
        detail += ('<div class="cap-section cap-verification"><h4>3 · Independent acceptance '
                   '<span class="proposed-label">Proposed team practice</span></h4>' + paragraph(check) + '</div>')
        detail += ('<div class="cap-section cap-limits"><h4>4 · Known limitations and effects</h4>'
                   + paragraph(limit) + '</div>')
        if c.get('prompt'):
            detail += ('<div class="cap-section"><h4>Illustrative task — not executed</h4>'
                       '<pre>' + E(c['prompt']) + '</pre></div>')
        if c.get('anti'):
            detail += ('<div class="cap-section"><h4>Anti-pattern (proposed)</h4>'
                       + paragraph(c['anti']) + '</div>')
        impl = c.get('implementations', c.get('implementation'))
        if impl:
            detail += '<details class="audit"><summary>Product-specific mechanisms</summary>'
            if isinstance(impl, list):
                for x in impl:
                    if isinstance(x, dict):
                        detail += paragraph(' · '.join(str(v) for k, v in x.items() if k != 'refs')) + refs(x.get('refs', []), sources)
                    else:
                        detail += paragraph(str(x))
            elif isinstance(impl, dict):
                for k, v in impl.items():
                    detail += f'<h4>{E(k)}</h4>' + paragraph(v if isinstance(v, str) else ' · '.join(str(q) for k2, q in v.items() if k2 != 'refs'))
            detail += '</details>'
        detail += '<div class="evidence-strip">Official evidence: ' + refs(item_refs(c), sources) + '</div>'
        search = E(json.dumps(c, ensure_ascii=False).lower() + ' ' + output.lower())
        function_label = 'Proposed architecture pattern' if key == 'architecture' else 'Documented function'
        out.append(f'<details class="cap" id="cap-{E(c["id"])}" data-search="{search}" '
                   f'data-group="{E(group)}" data-preview="{str(preview).lower()}">'
                   f'<summary><div class="badge-row">{badges}</div><h3>{E(c["title"])}</h3>'
                   f'<p class="claim"><strong>{E(function_label)}:</strong> {E(claim)}</p></summary>'
                   f'<div class="cap-detail">{detail}</div></details>')
    return ''.join(out) + '</div></section>'

def sources_section(evidence: dict,deck: dict) -> str:
    def entries(data: list,prefix: str) -> str:
        return '<ol class="source-list">'+''.join(f'<li id="{prefix}-{E(s["id"])}"><strong>{E(s["id"])}</strong> · <a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["title"])}</a><span class="small">{E(s.get("note",s.get("scope",s.get("locator","Official product documentation"))))}</span></li>' for s in data)+'</ol>'
    allsrc=[dict(v,id=k) for k,v in deck['sources'].items()]
    return '<section class="section" id="evidence"><div class="kicker">08 / Evidence and provenance</div><h2>Claims remain attached to their source.</h2><div class="notice"><p>The original capability audit is a 20 October 2026 snapshot. Presentation source material was assembled on 21 October 2026. Selected availability and safety boundaries were rechecked for this narrative revision; this is not a fresh execution test or a claim that every external page was revalidated.</p><p>Examples, gates, fallback procedures and pilot measures are author recommendations. No AWS account was accessed, no security assessment was run, and no savings or productivity outcome was measured.</p></div><h3>Capability and narrative evidence</h3>'+entries(evidence['sources'],'source')+'<h3>Presentation evidence</h3>'+entries(allsrc,'deck-source')+'</section>'

def report_markdown(key: str,story: dict,evidence: dict,deck: dict,annotations: dict) -> str:
    lines=[f'# {story["title"]}',story['strapline'],f'\nRevision: {DATE}. Independent engineering field guide.\n',f'**Audience:** {story["audience"]}',f'**Availability:** {story["availability"]}',f'**Recommended starting decision:** {story["decision"]}','\n## Decision brief',*story['summary'],'\n## Running use case']
    for k,v in story['use_case'].items():lines.append(f'**{k.replace("_"," ").title()}:** {v}')
    for i,s in enumerate(story['stages'],1):
        lines.extend([f'\n## {i}. {s["title"]}',*s['paragraphs'],f'**Capability crosswalk:** {", ".join(s["caps"])}',f'**Responsible role (team recommendation):** {annotations["stage_owners"][key][i-1]}'])
        for k in ['input','artifact','gate','fallback']:lines.append(f'**{k.title()}:** {s[k]}')
    lines.extend(['\n## Detailed capability reference'])
    for c in evidence.get('capabilities',evidence.get('patterns',[])):
        lines.append(f'\n### {c["id"]} — {c["title"]}')
        for k in ['claim','rule','availability','delivery','setup','limit','boundary','check','prompt','anti']:
            if c.get(k):lines.append(f'**{k.title()}:** {c[k]}')
        lines.append('**Review record to retain (team recommendation):** '+annotation_for(annotations,key,c['id']).get('record','Not specified.'))
        lines.append('Official documentation references: '+', '.join(item_refs(c)))
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

def report(key: str,story: dict,evidence: dict,deck: dict,css: str,js: str,annotations: dict) -> str:
    count=len(evidence.get('capabilities',evidence.get('patterns',[])));kind='patterns' if key=='architecture' else 'capabilities'
    uc=story['use_case'];summary=''.join(paragraph(p) for p in story['summary'])
    main=f'''<section class="section" id="decision"><div class="kicker">01 / Decision brief</div><h2>{E(story['strapline'])}</h2><div class="intro-grid"><div>{summary}</div><aside class="panel decision"><h3>Recommended starting decision</h3>{paragraph(story['decision'])}{definition([('Audience',story['audience']),('Availability',story['availability'])])}</aside></div><div class="stats"><div class="stat"><strong>{count}</strong><span>Detailed {kind}</span></div><div class="stat"><strong>{deck['minutes']} min</strong><span>Presentation, including {deck['demo']} min of demos</span></div><div class="stat"><strong>6</strong><span>Narrative steps with inputs, artifacts and gates</span></div></div></section><section class="section" id="scenario"><div class="kicker">02 / Running example</div><h2>{E(uc['name'])}</h2><p class="small">Illustrative scenario, not an observed customer result or an executed demonstration.</p><div class="grid2"><div class="panel">{definition([('Trigger',uc['trigger']),('Scope',uc['scope']),('Deliverable',uc['deliverable'])])}</div><div class="panel"><div class="limit"><strong>Not done</strong>{paragraph(uc['not_done'])}</div><div class="gate"><strong>Done means</strong>{paragraph(uc['done'])}</div></div></div></section>'''
    main+=narrative(story,evidence,annotations,key)+capabilities(key,evidence,annotations)
    controls=''
    if key=='architecture':controls=table(['Execution path','Effect','Documented control','Proposed team control'],[[x['path'],x['effect'],x['native'],x['recommendation']] for x in evidence['controls']])
    main+=f'''<section class="section" id="controls"><div class="kicker">05 / Controls and handoff</div><h2>Accept the artifact; authorize the effect separately.</h2><p>{E(story['related'])}</p>{controls}<div class="grid2" style="margin-top:24px"><div><h3>Illustrative work contract</h3><p class="small">Product-neutral template. It is not a native agent configuration file, a credential container or an authorization token.</p><pre class="sample" id="handoff-template">{E(story['handoff'])}</pre><button data-copy="handoff-template">Copy example contract</button></div><div class="panel"><h3>Authorization and evidentiary limits</h3><p>A generated recommendation, PR, finding or cost report is evidence for a decision. It is not a universal approval to act in another product.</p><p>Verify current feature availability, integration permissions and target safety before using a workflow. Preserve unresolved evidence gaps and use the existing team process when a configured path is not available.</p><p class="small">These are proposed engineering controls, not a claim of one shared AWS permission model.</p></div></div></section>'''
    demos=[s for s in deck['slides'] if s['kind']=='demo']
    main+=f'<section class="section" id="demos"><div class="kicker">06 / Demonstrations</div><h2>Demonstrate observable results and explicit limits</h2><p>The {deck["demo"]}-minute allocation is included in the {deck["minutes"]}-minute session. Prepare completed, sanitized results before presenting. A fresh agent run is not guaranteed to finish inside the walkthrough slot.</p>'
    for d in demos:main+=f'<article class="panel" style="margin:22px 0"><h3>{E(d["title"])} · {timecode(d["seconds"])}</h3>{slide_body(d)}</article>'
    main+='</section>'
    checks=''.join(f'<label><input type="checkbox" data-check="{i}" data-text="{E(c)}"><span>{E(c)}</span></label>' for i,c in enumerate(story['checks']))
    pilot=evidence.get('pilot',[]);rows=[]
    for p in pilot:
        if isinstance(p,dict):rows.append([p.get('days',''),p.get('title',''),p.get('description','')])
        else:rows.append(p)
    main+=f'''<section class="section" id="readiness"><div class="kicker">07 / Adoption and acceptance</div><h2>Verify a scoped workflow before expanding it.</h2><div class="grid2"><div class="panel readiness"><h3>Local readiness worksheet</h3><p class="small">Checks are manually marked and stored only in this browser. They are not tests, approvals or a certification.</p><div class="progress-track"><div class="progress-fill" id="readiness-fill"></div></div><p id="readiness-count" class="small" role="status"></p>{checks}<div class="actions" style="margin-top:20px"><button id="export-checks">Export worksheet</button><button id="clear-checks">Clear checks</button></div></div><div><h3>Proposed 30-day pilot</h3>{table(['Window','Focus','Acceptance work'],rows)}<div class="notice">Track accepted results, review effort, rework, boundary failures and unfinished work. Do not substitute output volume or projected savings for verified outcomes.</div></div></div></section>'''
    main+=sources_section(evidence,deck)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(story['title'])}: a detailed, source-linked engineering field guide with narrative workflows, capabilities and a timed presentation."><title>{E(story['title'])} | Frontier agents field guide</title><style>{css}</style></head><body data-agent="{key}" data-seconds="{deck['minutes']*60}" style="--accent:{story['accent']}"><a class="skip" href="#decision">Skip to report</a><header class="masthead"><div class="wrap"><a href="../index.html">← Frontier agents / report collection</a><div class="eyebrow">Engineering field guide / {story['number']} / Narrative edition</div><h1>{E(story['title'])}</h1><p class="lead">{E(story['strapline'])}</p><div class="meta"><span class="pill">{DATE}</span><span class="pill">{count} {kind}</span><span class="pill">{len(deck['slides'])} timed slides</span><span class="pill">Documentation synthesis, not runtime testing</span></div><div class="actions"><button data-present>Open timed presentation</button><a class="button" href="../presentations/{PPTX[key]}" download>PowerPoint</a><a class="button" href="report.md" download>Report as Markdown</a><a class="button" href="presentation-transcript.md" download>Presentation transcript</a><a class="button" href="../style-guide.html">Format standard</a><button data-print>Print report</button></div></div></header><nav class="topnav" aria-label="Report sections"><div class="wrap navinner"><a href="#decision">Decision brief</a><a href="#scenario">Use case</a><a href="#workflow">Narrative</a><a href="#capabilities">Capabilities</a><a href="#controls">Controls</a><a href="#demos">Demos</a><a href="#readiness">Pilot</a><a href="#evidence">Evidence</a></div></nav><main class="wrap report-view">{main}</main>{presentation(deck,evidence,annotations,key)}<footer class="footer"><div class="wrap"><strong>Independent engineering analysis.</strong> Not an AWS publication or an implemented multi-agent architecture. Official links support product mechanisms; workflow sequencing, gates and examples are author synthesis. <a href="../VALIDATION.md">Validation record</a> · <a href="../index.html">All reports</a></div></footer><div id="toast" class="toast" role="status" hidden></div><script>{js}</script></body></html>'''

def style_guide(css: str) -> str:
    capability_rows=[
        ('1','Identity & maturity','Capability ID, product or surface, feature status and delivery mechanism','Always visible'),
        ('2','Documented function','Concrete product operation, without outcome claims','Always visible'),
        ('3','Invocation & scope','Prerequisites, sources, required authorization and affected target','Expanded record'),
        ('4','Review record to retain','Suggested artifact for the team; explicitly not guaranteed native output','Expanded record'),
        ('5','Independent acceptance','Evidence or test capable of contradicting the agent result','Expanded record'),
        ('6','Known limits & effects','Preview constraints, unsupported surfaces, write effects and gaps','Expanded record'),
        ('7','Official sources','Feature-specific source IDs linked to AWS pages','Expanded record'),
    ]
    usecase_rows=[
        ('Context','Trigger, target, time window and owner'),
        ('Scope','Allowed effects, exclusions, client/Region/permission constraints'),
        ('Action sequence','Steps with inputs, responsible role and cited native mechanism'),
        ('Output','Reviewable artifact and source provenance'),
        ('Decision','Acceptance condition, reviewer and authorizer'),
        ('Failure path','Missing evidence, blocked permissions, rollback/stop and fallback'),
    ]
    slide_rows=[
        ('Scenario contract','One bounded problem, expected artifact, exclusions and acceptance'),
        ('Capability matrix','Only related functions; label preview and configured paths'),
        ('Input → function → artifact','One mechanism, with source dependencies and independent verification'),
        ('Controls / availability','Exactly which actor can perform which effect and under which conditions'),
        ('Live demo','Timed steps, preflight, source evidence, pass/fail and prepared fallback'),
        ('Untimed reference','One slide per capability; full function, setup, record, verification, limits, sources'),
    ]
    samples=[
        ('"AI automatically resolves production incidents."','"A connected investigation can produce a mitigation proposal. Production changes require the configured execution and approval path."'),
        ('"Security assurance is end-to-end."','"A scoped assessment returns findings; the team reviews fixes and revalidates the authorized target."'),
        ('"Optimize cloud costs effortlessly."','"Reconcile source totals, review optimization recommendations and measure separately approved changes."'),
        ('"Agents share one permission boundary."','"A team can pass evidence between products; permissions and approval controls remain product-specific."'),
    ]
    part=lambda title,body:f'<section class="section"><h2>{E(title)}</h2>{body}</section>'
    content='<section class="section"><div class="kicker">Engineering publication standard</div><h2>Use a fixed evidence structure for every feature and workflow</h2><p>A product capability is a documented mechanism; a use case is a bounded sequence that applies mechanisms to a problem. Keep proposed team controls separate from product behavior. Speaker notes contain details that would reduce slide legibility.</p><div class="grid3"><div class="panel"><h3>Report mode</h3><p>Full capability fields, steps, limitations, acceptance evidence and official URLs.</p></div><div class="panel"><h3>Presentation core</h3><p>Decision-oriented slides and timeboxed demonstrations; fewer statements on each slide.</p></div><div class="panel"><h3>Reference appendix</h3><p>One untimed capability slide per entry, available for technical questions.</p></div></div></section>'
    content+=part('1. Capability record — seven fields', table(['#','Field','Required content','Placement'],capability_rows))
    content+=part('2. Use-case record — bounded process', table(['Stage','Information required'],usecase_rows)+'<p>For each execution step, show a proposed responsible role, the required input, operation narrative, reviewable artifact, acceptance gate, fallback and source IDs. Do not imply that crossing products transfers credentials or approvals.</p>')
    content+=part('3. Slide selection by information type',table(['Layout','Use it for'],slide_rows)+'<div class="notice">The 70 core slides remain timed at 128 minutes including 35 minutes of walkthrough demonstrations. The 50 capability-reference slides are untimed and do not change these allocations. Questions and breaks are additional.</div>')
    content+=part('4. Neutral wording',table(['Avoid','Use'],samples)+'<p>Write claims as observable operations, not performance promises. “Automatic” is appropriate only where a documented trigger actually initiates a task. Unmeasured quality, time-saving or cost-saving claims must not appear as achieved results.</p>')
    content+=part('5. Publication checks','<div class="grid2"><div class="panel"><h3>Evidence</h3><p>Every product statement cites an official feature source. Label preview and client/Region limits. Label proposed artifacts, owners, prompts and cross-agent sequences.</p></div><div class="panel"><h3>Execution and quality</h3><p>Show permissions and side effects. Include independent checks and fallbacks. Verify timed durations, readable layouts, local links and uncropped content. No untested benefit is represented as measured.</p></div></div>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Engineering report and slide format | Frontier agents</title><style>{css}</style></head><body><header class="masthead"><div class="wrap"><a href="index.html">← Report collection</a><div class="eyebrow">Factual publication format · 21 October 2026</div><h1>Capability and use-case format</h1><p class="lead">Standard record fields for the interactive reports and timed presentations.</p><div class="actions"><a class="button" href="EDITORIAL_STANDARD.md">Full editorial standard</a><a class="button" href="index.html">All reports</a></div></div></header><main class="wrap">{content}</main><footer class="footer"><div class="wrap">This is a documentation and presentation standard, not a product capability claim. Source evidence is linked within each report.</div></footer></body></html>'''

def index(config: dict,decks: dict,css: str,js: str) -> str:
    cards=[];rows=[]
    for key in AGENTS:
        story=config['agents'][key];d=decks[key];path=PATHS[key]
        cards.append(f'''<article class="card portfolio-card" data-portfolio style="--card-accent:{story['accent']}"><div class="kicker">Field guide {story['number']}</div><h3>{E(story['title'])}</h3><p>{E(story['strapline'])}</p><p class="small">{E(story['availability'])}</p><p><strong>Use case:</strong> {E(story['use_case']['name'])}</p><p class="small">{len(d['slides'])} timed slides + untimed capability references · {d['minutes']} minutes including {d['demo']} minutes of demos</p><div class="actions"><a class="button primary" href="{path}">Read report</a><a class="button" href="{path}#presentation">Present</a><a class="button" href="presentations/{PPTX[key]}" download>PPTX</a></div></article>''')
        rows.append([story['title'],story['use_case']['deliverable'],story['use_case']['done']])
    main='<section class="section"><div class="kicker">Reports and presentations</div><h2>Three agent reports and their shared architecture using a common evidence format</h2><p>Each guide describes a bounded engineering problem, documented capabilities, prerequisites, reviewable records, execution limits and independent acceptance. The same fields appear in HTML and PowerPoint. Detailed report reading and timed presentation are separate modes.</p><label class="search-label"><span>Find a report by task or audience</span><input id="portfolio-filter" type="search" placeholder="Try: cost, security, incident, code…"></label><div class="grid2" style="margin-top:24px">'+''.join(cards)+'</div></section><section class="section"><div class="kicker">Consolidated perspective</div><h2>Choose by the evidence and outcome you need.</h2>'+table(['Guide','Reviewable artifact','Acceptance boundary'],rows)+'</section><section class="section"><h2>How to use the collection</h2><div class="grid3">'+tile('Read the story','Start with the running use case, then follow its six steps. Inputs, outputs, gates and failure paths stay visible.','01')+tile('Inspect a capability','Search the detailed inventory. Check the delivery mechanism, availability, prerequisites and limitations before piloting.','02')+tile('Run the session','Open presentation mode or a PowerPoint deck. Demo slots include prepared-result fallbacks; questions and breaks are extra.','03')+'</div><p class="small"><strong>Publication format:</strong> <a href="style-guide.html">Read the editorial and information-design standard</a>. Product behavior, proposed team steps and independent verification are kept distinct.</p><div class="notice">The timed programme is 128 minutes, including 35 minutes of demonstrations. Untimed capability-reference slides are available after each timed section. No live AWS workflow was executed. Examples are illustrative; the FinOps teaching fixture is synthetic. These documents do not claim measured productivity, security coverage or savings.</div><div class="actions"><a class="button" href="README.md">Repository guide</a><a class="button" href="VALIDATION.md">Validation</a><a class="button" href="MANIFEST.json">File manifest</a><a class="button" href="demo-assets/agent-handoff.example.yaml" download>Handoff template</a><a class="button" href="https://github.com/lyrel-dev/frontier-agents">Repository and Git history</a></div></section>'
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Frontier agents | Engineering field guides</title><style>{css}</style></head><body data-agent="portfolio"><a class="skip" href="#collection">Skip to collection</a><header class="masthead"><div class="wrap"><div class="eyebrow">AWS frontier agents / Independent engineering field guides</div><h1>AWS frontier agents<br>engineering reference</h1><p class="lead">Detailed interactive reports, concrete use cases and timed presentations for DevOps, software, security and cost teams.</p><div class="meta"><span class="pill">4 field guides</span><span class="pill">38 capabilities + 12 patterns</span><span class="pill">70 timed slides + 50 reference slides</span><span class="pill">128 min including demos</span></div></div></header><main class="wrap" id="collection">{main}</main><footer class="footer"><div class="wrap">Revision {DATE}. Official sources are linked at claim level. Not an AWS publication or an executed deployment design. Download or clone the repository and open index.html; no server is required. Repository storage is not the same as a deployed GitHub Pages site.</div></footer><script>{js}</script></body></html>'

def static_checks() -> dict:
    errors=[];count=0;links=0
    for rel in ['index.html','style-guide.html',*PATHS.values(),'devops/initial-report.html',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'mechanisms').glob('*.html'))]]:
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
    result={'html_files':count,'local_links_checked':links,'errors':errors,'timing_checks':'four sessions; three agents and shared architecture','boundary':'Structural checks only. External links, rendered layout and live AWS behavior require separate checks.'}
    if errors:raise ValueError(json.dumps(result,indent=2))
    return result

def build() -> None:
    config=read_json('content/narratives.json');annotations=read_json('content/format-annotations.json');css=(ROOT/'assets/report.css').read_text();js=(ROOT/'assets/report.js').read_text();decks={};evidence={}
    for key in AGENTS:
        evidence[key]=prepare_evidence(key);decks[key]=read_json(f'content/{key}-presentation.json');story=config['agents'][key]
        put(PATHS[key],report(key,story,evidence[key],decks[key],css,js,annotations))
        put(f'{key}/report.md',report_markdown(key,story,evidence[key],decks[key],annotations))
        put(f'{key}/presentation-transcript.md',transcript(decks[key]))
    put('devops/initial-report.html','<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0; url=validated-report.html"><title>Current DevOps Agent report</title></head><body><p><a href="validated-report.html">Open the current DevOps Agent report.</a></p></body></html>')
    from build_presentations import build_deck
    for key in AGENTS:
        p=ROOT/'presentations'/PPTX[key];p.parent.mkdir(exist_ok=True);build_deck(decks[key],config['agents'][key],p,evidence[key],annotations['capability_records'][key]);GENERATED.append(str(p.relative_to(ROOT)))
    put('demo-assets/agent-handoff.example.yaml','# Illustrative team contract; not an AWS configuration or authorization.\n'+config['agents']['architecture']['handoff']+'\n')
    csv='period,day,cost_usd,data_kind\n'+''.join(f'{period},{i},{amount:.2f},synthetic\n' for period,amount in [('baseline',100),('comparison',141)] for i in range(1,15))
    put('demo-assets/finops-storage-cost-synthetic.csv',csv)
    put('demo-assets/finops-fixture-guide.md','# Synthetic FinOps teaching fixture\n\nThis is not an AWS export or a measured account result. Fourteen baseline rows total $1,400; fourteen comparison rows total $1,974. The difference is $574 / $1,400 = 41%. The deliberately simple values teach reconciliation, not realistic forecasting or causal inference.\n\nState the date window, currency, filters and cost basis before comparing real data. Do not claim an observed anomaly, causal driver or realized saving from this fixture.\n')
    put('index.html',index(config,decks,css,js))
    put('style-guide.html',style_guide(css))
    reference_total=sum(len(evidence[k].get('capabilities',evidence[k].get('patterns',[]))) for k in AGENTS)
    put('FORMAT_IMPLEMENTATION.md',f'# Format implementation\n\nAll four interactive reports now use fixed capability records (documented function, prerequisites, proposed retained record, independent acceptance, limits and official evidence). Each use-case step specifies a proposed role, related documented mechanisms and a review gate. The 70 timed presentation slides remain within their existing allocations; {reference_total} untimed capability reference slides are appended across the HTML and PowerPoint presentation views. These slides are reference material and do not extend session times. See [EDITORIAL_STANDARD.md](EDITORIAL_STANDARD.md) for details.\n')
    rows='\n'.join(f'| {config["agents"][k]["title"]} | [Report]({PATHS[k]}) | [PowerPoint](presentations/{PPTX[k]}) | {decks[k]["minutes"]} min / {decks[k]["demo"]} min demo |' for k in AGENTS)
    put('README.md','# Frontier agents — engineering field guides\n\nDetailed, source-linked interactive reports and timed presentations. Download or clone the repository and open `index.html` in a browser. No server, build step or external JavaScript is needed to read the generated reports. GitHub file previews do not execute the report HTML; repository publication is not a GitHub Pages deployment.\n\n| Guide | Interactive report | Presentation | Timing |\n|---|---|---|---|\n'+rows+'\n\nEach guide includes a six-step narrative, use-case scope, a detailed capability inventory, controls, examples, timed demos, readiness worksheet and official sources. The entire programme is 128 minutes including 35 minutes of demonstrations; questions and breaks are additional.\n\n## Format and editorial standard\n\nSee [EDITORIAL_STANDARD.md](EDITORIAL_STANDARD.md) and [FORMAT_IMPLEMENTATION.md](FORMAT_IMPLEMENTATION.md). Every capability now has an untimed reference slide for detailed discussion; timing applies only to the core.\n\n## Documents\n\n- `*/report.md`: narrative and capability report in Markdown.\n- `*/presentation-transcript.md`: speaker transcript, timing and demo runbooks.\n- `presentations/`: four editable PowerPoint decks generated from the same slide source as the HTML presentations; one untimed evidence appendix per deck.\n- `*/validation-record.md`: scope-filtered capability evidence records.\n- `content/`: versioned narrative, presentation and evidence source data.\n- `demo-assets/`: product-neutral contract and explicitly synthetic cost fixture.\n- `MANIFEST.json`, `VALIDATION.md`: file integrity and validation scope.\n\n## Rebuild\n\n```sh\npython -m pip install beautifulsoup4==4.13.4 python-pptx==1.0.2\npython tools/build_suite.py\npython tools/build_suite.py --check\n```\n\nThe documentation workflow builds and checks the suite and commits each generated file separately. Existing Git history and unrelated repository files are not replaced. The historical PowerPoint edition is superseded by the report-aligned, editable publication edition; it is not a byte-for-byte copy of the earlier image-led decks.\n\n## Evidence boundary\n\nIndependent analysis, not an AWS publication. The original audits are 20 October 2026 snapshots; the presentation source and narrative revision are dated 21 October. Selected critical product boundaries were rechecked, not every source page. Examples and gates are recommendations. No live AWS account or agent workflow was exercised, and no productivity, diagnostic accuracy, security coverage or cost savings are claimed.\n')
    put('CHANGELOG.md','# Publication revision — 21 October 2026\n\nCurrent three-agent revision: Standardized factual capability records and use-case steps in the report and slide views; added proposed review records, named responsible roles, 50 untimed reference slides, and an editorial standard. Speaking and demo allocations unchanged.\n\nAdded four detailed narrative reports with six-stage use cases, explicit input/output contracts, failure paths and acceptance gates. Retained the in-scope capability evidence. Earlier editions remain in Git history. Added the portfolio index, report Markdown, source-aligned PowerPoint decks, timed transcripts, synthetic demo assets and reproducible build. Presentation budgets remain 35, 30, 27 and 36 minutes, including demonstrations.\n\nPowerPoint publication decks contain the 70 timed slides plus 50 untimed capability reference slides from the same source records. Decorative title imagery from the earlier 61-slide edition is not reused; core content is editable and each deck has an additional untimed evidence appendix.\n')
    put('VALIDATION.md','# Validation boundary\n\n## Editorial format\n\nSee `EDITORIAL_STANDARD.md` for field definitions, source classification and wording policy. Team-proposed review records and roles are kept separate from documented product behavior.\n\n## Evidence\n\nThe retained capability evidence originates in the earlier documentation review and has been filtered to the current scope. The source-linked presentation material and this narrative revision are dated 21 October 2026. Selected availability, execution and authorization boundaries were rechecked against official AWS documentation; this is not a new claim-by-claim audit of every URL.\n\n## Build checks\n\nThe build checks local paths and anchors, unique HTML IDs, narrative completeness, all four presentation and demonstration budgets, presentation reference IDs, all 50 capability/pattern reference records, neutral wording in authored titles/takeaways, and PowerPoint existence. `qa/build-validation.json` records the structural results. Browser checks, when available, are recorded separately in `qa/browser-validation.json`; absence of that file does not imply they passed.\n\n## Not tested\n\nNo live AWS accounts, repositories, deployments, agent runs, penetration tests or purchasing workflows were exercised. Demonstration budgets include prepared-result fallback paths and are not agent-runtime guarantees. The cost fixture is synthetic. No measured reliability, accuracy, security-detection, productivity or savings outcomes are claimed.\n\n## Publication\n\nRepository visibility and hosting settings are not changed by the build. The generated HTML works locally. Publishing files to GitHub does not automatically enable GitHub Pages. Earlier document revisions remain in Git history.\n')
    from build_mechanisms import build_mechanisms
    build_mechanisms(ROOT)
    put('MANIFEST.json','{}\n')
    result=static_checks();put('qa/build-validation.json',json.dumps(result,indent=2)+'\n')
    subprocess.run([sys.executable,str(ROOT/'tools/editorial_lint.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    files={}
    for p in sorted(ROOT.rglob('*')):
        rel=str(p.relative_to(ROOT))
        if p.is_file() and not any(x in p.parts for x in ['.git','__pycache__']) and rel not in ['MANIFEST.json']:
            files[rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    put('MANIFEST.json',json.dumps({'revision':read_json('content/mechanisms.json')['revision'],'files':files,'excluded':['MANIFEST.json itself','.git/','__pycache__/']},indent=2)+'\n')
    print(json.dumps({'generated':len(set(GENERATED)),'structural_checks':result},indent=2))

def commit_files() -> None:
    def git(*args: str) -> bytes:return subprocess.check_output(['git','-C',str(ROOT),*args])
    paths=set(x for x in (git('diff','--name-only','-z')+git('ls-files','--others','--exclude-standard','-z')).decode().split('\0') if x)
    for path in sorted(paths):
        if path.startswith('.git/') or '__pycache__' in path:continue
        git('add','-A','--',path);git('commit','-m',f'docs: publish {path}','--',path)
    print(f'Committed {len(paths)} changed files separately.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--commit',action='store_true');args=parser.parse_args()
    if args.check:print(json.dumps(static_checks(),indent=2))
    elif args.commit:commit_files()
    else:build()
