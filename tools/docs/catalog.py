"""Render one outcome catalog and reference indexes over shared canonical data."""
from pathlib import Path
from collections import defaultdict
from html import escape
import json
import re

ROOT=Path(__file__).resolve().parents[2]
NAMES={'devops':'AWS DevOps Agent','security':'AWS Security Agent','finops':'AWS FinOps Agent','architecture':'Shared operational practice'}

def esc(value): return escape(str(value),quote=True)
def records(name): return json.loads((ROOT/f'catalog/{name}.json').read_text())['entries']
def registry():
    out={}
    for name in ('mechanisms','features','profiles'):
        for item in records(name): out[item['id']]=(name,item)
    return out

def includes(entry,key): return key in entry.get('platforms',[entry['platform']])
def address(ident):
    if ident.startswith('UC-'): return 'index.html#'+ident
    if ident.startswith('MX-'): return 'mechanisms.html#'+ident
    if ident.startswith('FT-'): return 'features.html#'+ident
    if ident.startswith('PR-'): return 'profiles.html#'+ident
    raise ValueError('Unknown record identifier '+ident)
def link(ident,label=None): return '<a href="../catalog/'+address(ident)+'">'+esc(label or ident)+'</a>'
def section_links(platform,ids,guides):
    return ' · '.join('<a href="../guides/'+platform+'.html#'+sid+'">'+esc(guides[platform]['sections'][sid]['title'])+'</a>' for sid in ids)
def sources(entry,guides):
    g=guides[entry['platform']];ids=[]
    for sid in entry['sections']:ids.extend(g['sections'][sid]['sources'])
    return [(sid,g['refs'][sid]) for sid in dict.fromkeys(ids)]
def evidence(entry,guides):
    return '<p class="reference-links">Technical explanation: '+section_links(entry['platform'],entry['sections'],guides)+'</p><p class="reference-links">Official evidence: '+' · '.join('<a href="'+esc(url)+'">'+esc(sid)+'</a>' for sid,url in sources(entry,guides))+'</p>'

def controls(entries,platform=False):
    def choices(values,label):return '<option value="">All '+label+'</option>'+''.join('<option value="'+esc(v)+'">'+esc(NAMES.get(v,v))+'</option>' for v in sorted(set(values)))
    platforms=set(p for e in entries for p in e.get('platforms',[e['platform']]))
    return ('<div class="catalog-controls"><input data-uc-search type="search" aria-label="Search use cases" placeholder="Search objectives, variants, former titles and dependencies">'
        +('<select data-uc-platform aria-label="Platform">'+choices(platforms,'platforms')+'</select>' if platform else '')
        +'<select data-uc-group aria-label="Use case group">'+choices([e['group'] for e in entries],'groups')+'</select>'
        +'<select data-uc-delivery aria-label="Delivery mode">'+choices([e['delivery'] for e in entries],'delivery modes')+'</select>'
        +'<select data-uc-cadence aria-label="Cadence">'+choices([e['cadence'] for e in entries],'cadences')+'</select>'
        +'<button data-uc-reset>Reset</button></div><p data-uc-count class="result-count" aria-live="polite"></p><p data-uc-empty hidden>No cases match these filters.</p>')

def alias_nodes(catalog):
    parts=[]
    for a in records('aliases'):
        links=' · '.join(link(t) for t in a['targets'])
        parts.append('<section class="migration-choice" id="'+a['id']+'" data-alias-targets="'+esc(json.dumps(a['targets']))+'" hidden><h2>'+esc(a['title'])+'</h2><p>'+esc(a['disposition'])+'. This former record resolves to: '+links+'</p></section>')
    return ''.join(parts)

def entry(e,guides,embedded=False):
    reg=registry();prose=''.join('<p>'+esc(p)+'</p>' for p in e['narrative'])
    workflow=[]
    for i,s in enumerate(e['workflow'],1):
        mid=s['mechanism']; m=reg[mid][1] if mid else None
        implementation=link(mid,m['title']) if m else 'Team procedure; not represented as a native agent function'
        fids=s['configuration_features']
        config=' · '.join(link(f,reg[f][1]['title']) for f in fids) or 'No platform feature is asserted for this human decision.'
        workflow.append('<li><h4>'+esc(s['title'])+'</h4><p>'+esc(s['purpose'])+'</p><dl class="dependency-fields"><dt>Responsible actor</dt><dd>'+esc(s['actor'])+'</dd><dt>Mechanism</dt><dd>'+implementation+'</dd><dt>Dependency</dt><dd>'+esc(s['dependency'])+' — '+esc(s['condition'])+'</dd><dt>Configuration</dt><dd>'+config+'</dd><dt>Effect</dt><dd>'+esc(s['effect'])+'</dd><dt>Acceptance evidence</dt><dd>'+esc(s['verification'])+'</dd><dt>When the step cannot proceed</dt><dd>'+esc(s['on_failure'])+'</dd></dl></li>')
    variants=''.join('<section class="case-variant"><h4>'+esc(v['name'])+'</h4><p>'+esc(v['changes'])+' '+esc(v['controls'])+'</p></section>' for v in e['variants'])
    profile_links=' · '.join(link(p,reg[p][1]['title']) for p in e['profiles'])
    former=' '.join(e.get('aliases',[])+e.get('keywords',[])+e.get('legacy_ids',[]))
    return ('<article class="usecase-entry" id="'+e['id']+'" data-platform="'+esc(' '.join(e['platforms']))+'" data-group="'+esc(e['group'])+'" data-delivery="'+esc(e['delivery'])+'" data-cadence="'+esc(e['cadence'])+'">'
        +'<div class="section-meta">'+e['id']+' · '+esc(e['actor'])+' · '+esc(e['delivery'])+'</div><h3><a href="#'+e['id']+'">'+esc(e['title'])+'</a></h3><p class="case-objective"><strong>Objective.</strong> '+esc(e['objective'])+'</p><div class="narrative">'+prose+'</div>'
        +'<h4>Completion criteria</h4><ul>'+''.join('<li>'+esc(x)+'</li>' for x in e['completion'])+'</ul>'
        +('<h4>Configuration variants</h4>'+variants if variants else '')
        +'<details class="case-reference"><summary>Read the workflow, mechanism dependencies and configuration</summary><p>'+esc(e['steps_basis'])+'</p><ol class="workflow-steps">'+''.join(workflow)+'</ol><h4>Implementation profiles</h4><p>'+profile_links+'</p>'
        +'<dl><dt>Inputs</dt><dd>'+esc(e['inputs'])+'</dd><dt>Reviewed output</dt><dd>'+esc(e['output'])+'</dd><dt>Cadence</dt><dd>'+esc(e['cadence'])+'</dd><dt>Feature eligibility</dt><dd>'+esc(e['availability'])+'</dd><dt>Limits</dt><dd>'+esc(e['constraints'])+'</dd><dt>Example request</dt><dd>'+esc(e['example'])+'</dd></dl>'+evidence(e,guides)+'</details>'
        +'<span class="search-aliases" hidden>'+esc(former)+'</span></article>')

def content(catalog,guides,key=None):
    selected=[e for e in catalog['entries'] if key is None or includes(e,key)]
    groups=defaultdict(list)
    for e in selected:groups[(e['platform'],e['group'])].append(e)
    parts=[controls(selected,key is None),'<p class="catalog-reference-nav"><a href="../catalog/mechanisms.html">Mechanisms and dependent workflows</a> · <a href="../catalog/features.html">Platform features and change impact</a> · <a href="../catalog/profiles.html">Implementation profiles</a> · <a href="../catalog/migration.md">Former-record mapping</a></p>',alias_nodes(catalog)]
    for (platform,group),items in groups.items():
        title=group if key else NAMES[platform]+' — '+group
        ident='usecase-'+re.sub('[^a-z0-9]+','-',(platform+'-'+group).lower()).strip('-')
        parts.append('<section class="catalog-group" id="'+ident+'" data-uc-group-block><header><h2>'+esc(title)+'</h2><p>'+esc(catalog['group_introductions'][group])+'</p></header>'+''.join(entry(e,guides,key is not None) for e in items)+'</section>')
    return ''.join(parts)

STYLE='''
.catalog-reference-nav{line-height:1.9}.workflow-steps>li{padding:12px 0 22px;border-bottom:1px solid #c8d1d9}.workflow-steps h4{margin:8px 0}.dependency-fields{display:grid;grid-template-columns:160px minmax(0,1fr);gap:7px 16px}.dependency-fields dt{font-weight:600}.dependency-fields dd{margin:0;overflow-wrap:anywhere}.reference-entry{padding:24px 0 32px;border-top:2px solid #c8d1d9;scroll-margin-top:20px}.reference-entry h2{font-size:24px}.reference-entry p{max-width:88ch}.reference-controls{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}.reference-controls input{flex:2;min-width:220px}.reference-controls select{flex:1}.reference-controls input,.reference-controls select{padding:10px;border:1px solid #9aaabd;border-radius:4px}.migration-choice{border-left:4px solid #385f76;padding:16px;margin:20px 0}.case-variant{padding:0 0 0 14px;border-left:2px solid #c8d1d9}.case-variant h4{margin-bottom:3px}.dependency-path{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:18px 0}.dependency-path span{border:1px solid #9aaabd;padding:8px}.reference-main{max-width:1120px;margin:30px auto;padding:0 24px}.reference-entry table{width:100%;border-collapse:collapse}.reference-entry th,.reference-entry td{padding:9px;border-bottom:1px solid #c8d1d9;text-align:left;vertical-align:top}.reference-entry td{overflow-wrap:anywhere}.alias-labels{color:#526474;font-size:14px}.reference-filter-empty{padding:20px;border:1px dashed #9aaabd} [hidden]{display:none!important}
@media(max-width:700px){.dependency-fields{grid-template-columns:1fr}.dependency-fields dd{margin:0 0 10px}.reference-main{padding:0 16px}.reference-controls>*{width:100%;min-width:0}.reference-entry .table-wrap{overflow-x:auto}}
'''
SCRIPT='''
(()=>{
 const aliases=[...document.querySelectorAll('[data-alias-targets]')];
 function alias(){const id=decodeURIComponent(location.hash.slice(1));const item=aliases.find(x=>x.id===id);if(!item)return;const targets=JSON.parse(item.dataset.aliasTargets);if(targets.length===1){const id2=targets[0];const page=id2.startsWith('UC-')?'index':id2.startsWith('MX-')?'mechanisms':id2.startsWith('FT-')?'features':'profiles';if(document.getElementById(id2)){location.replace('#'+id2);}else{location.replace('../catalog/'+page+'.html#'+id2);}}else{item.hidden=false;item.scrollIntoView();}}
 addEventListener('hashchange',alias);alias();
 const input=document.querySelector('[data-ref-search]'),select=document.querySelector('[data-ref-platform]'),nodes=[...document.querySelectorAll('.reference-entry')];
 if(!input)return;
 function show(){const words=input.value.toLowerCase().split(/\\s+/).filter(Boolean);let count=0;nodes.forEach(n=>{const yes=words.every(w=>n.textContent.toLowerCase().includes(w))&&(!select.value||n.dataset.platform.split(' ').includes(select.value));n.hidden=!yes;if(yes)count++;});document.querySelector('[data-ref-count]').textContent=count+' of '+nodes.length+' records shown';document.querySelector('[data-ref-empty]').hidden=count!==0;}
 input.addEventListener('input',show);select.addEventListener('input',show);document.querySelector('[data-ref-reset]').onclick=()=>{input.value='';select.value='';show();};
 function reveal(){const id=decodeURIComponent(location.hash.slice(1));const n=document.getElementById(id);if(n&&n.matches('.reference-entry')){input.value='';select.value='';show();n.scrollIntoView();}}
 addEventListener('hashchange',reveal);show();reveal();
})();
'''

def decorate(page):return page.replace('</style>',STYLE+'</style>').replace('</body>','<script>'+SCRIPT+'</script></body>')
def table(headers,rows):
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="Dependency reference table"><table><thead><tr>'+''.join('<th scope="col">'+esc(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def reference_pages(catalog,guides,frame,write):
    reg=registry();cases=catalog['entries'];aliases=records('aliases')
    def related(mid):
        rows=[]
        for c in cases:
            for step in c['workflow']:
                if step['mechanism']==mid:rows.append([link(c['id'],c['title']),esc(step['title']),esc(step['dependency']+' — '+step['condition'])])
        return rows
    def profile_cases(pid):return [c for c in cases if pid in c['profiles']]
    for kind,title,intro in [
        ('mechanisms','Mechanisms and workflow dependencies','Read how a documented process is used by specific workflow steps. Required, optional and conditional dependencies refer to the proposed implementation, not a universal property of the service.'),
        ('features','Platform features and change impact','Inspect the concrete configuration surface and trace which mechanisms, implementation profiles and outcomes depend on it. This is an index into the maintained guides, not a second competing technical guide.'),
        ('profiles','Implementation profiles','Select a product-specific configuration recipe after choosing the operational objective. Profile parameters and acceptance checks are authored guidance; they are not deployable AWS payloads or evidence that a live test ran.')]:
        articles=[];items=records(kind)
        for item in items:
            ident=item['id'];platforms=item.get('platforms',[item.get('platform','')]);parts=[]
            if kind=='mechanisms':
                parts=['<p>'+esc(item['process'])+'</p><dl class="dependency-fields">'+''.join('<dt>'+esc(label)+'</dt><dd>'+esc(item[field])+'</dd>' for label,field in [('Trigger','trigger'),('Retained or execution state','state'),('Effect','effect'),('Proposed verification','verification'),('Failure handling','on_failure')])+'</dl>', '<h3>Feature configuration</h3><p>'+' · '.join(link(f,reg[f][1]['title']) for f in item['features'])+'</p>',evidence(item,guides)]
                rows=related(ident)
                parts+=['<h3>Workflow steps using this mechanism</h3>',table(['Outcome','Step','Dependency'],rows) if rows else '<p>This mechanism is selected through an implementation profile rather than required by every primary case.</p>']
                p=[r for r in records('profiles') if ident in r['mechanisms']]
                parts+=['<h3>Implementation profiles</h3><p>'+' · '.join(link(x['id'],x['title']) for x in p)+'</p>']
            elif kind=='features':
                parts=['<p>'+esc(item['configuration'])+'</p><p><strong>Objects:</strong> '+esc(', '.join(item['objects']))+'</p>',evidence(item,guides)]
                ms=[r for r in records('mechanisms') if ident in r['features']]
                parts+=['<h3>Mechanisms implemented with this feature</h3><p>'+' · '.join(link(m['id'],m['title']) for m in ms)+'</p>']
                rows=[];seen=set()
                for m in ms:
                    for c in cases:
                        direct=[s for s in c['workflow'] if s['mechanism']==m['id']]
                        via=[p for p in records('profiles') if p['id'] in c['profiles'] and m['id'] in p['mechanisms']]
                        if not direct and not via:continue
                        tag=(c['id'],m['id']);
                        if tag in seen:continue
                        seen.add(tag)
                        impact='; '.join(s['dependency']+': '+s['condition'] for s in direct) if direct else 'Profile-selected support; not a mandatory dependency for every variant.'
                        rows.append([link(c['id'],c['title']),link(m['id'],m['title']),esc(impact)])
                parts+=['<h3>Potential effect of disabling or changing this feature</h3><p>Required edges may block the selected implementation; optional edges reduce context or convenience; conditional edges apply only when their stated variant is selected. Diagnose the actual configuration before predicting a runtime failure.</p>',table(['Outcome','Mechanism','Impact condition'],rows)]
            else:
                parts=['<p>'+esc(item.get('status','Proposed recipe; verify feature eligibility and substitute approved identifiers.'))+'</p>',table(['Parameter','Purpose','Illustrative value'],[[esc(x) for x in row] for row in item['parameters']]),'<h3>Configuration procedure</h3><ol>'+''.join('<li>'+esc(x)+'</li>' for x in item['setup'])+'</ol><h3>Acceptance exercises</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in item['tests'])+'</ul><h3>Stop and lifecycle behavior</h3><p>'+esc(item['stop_behavior'])+'</p>','<h3>Linked mechanisms</h3><p>'+' · '.join(link(m,reg[m][1]['title']) for m in item['mechanisms'])+'</p>','<h3>Applicable outcomes</h3><p>'+' · '.join(link(c['id'],c['title']) for c in profile_cases(ident))+'</p>']
            names=[a['title'] for a in aliases if ident in a['targets']]
            if names:parts.append('<p class="alias-labels">Former catalog labels: '+esc('; '.join(names))+'</p>')
            articles.append('<article class="reference-entry" id="'+ident+'" data-platform="'+esc(' '.join(platforms))+'"><p class="section-meta">'+esc(ident+' · '+', '.join(NAMES.get(p,p) for p in platforms))+'</p><h2><a href="#'+ident+'">'+esc(item['title'])+'</a></h2>'+''.join(parts)+'</article>')
        controls='<div class="reference-controls"><input data-ref-search aria-label="Search reference" type="search" placeholder="Search names, configuration, former labels and dependent outcomes"><select data-ref-platform aria-label="Platform"><option value="">All platforms</option>'+''.join('<option value="'+p+'">'+esc(n)+'</option>' for p,n in NAMES.items())+'</select><button data-ref-reset>Reset</button></div><p data-ref-count aria-live="polite"></p><p class="reference-filter-empty" data-ref-empty hidden>No matching records.</p>'
        nav='<p><a href="index.html">Operational outcomes</a> · <a href="mechanisms.html">Mechanisms</a> · <a href="features.html">Features</a> · <a href="profiles.html">Profiles</a> · <a href="migration.md">Consolidation mapping</a></p>'
        body='<main id="main" class="reference-main"><header class="book-title"><h1>'+title+'</h1><p>'+intro+'</p>'+nav+'</header>'+controls+''.join(articles)+'</main>'
        write('catalog/'+kind+'.html',decorate(frame(title,body,'reference')))

def build_pages(catalog,guides,frame,write,*unused):
    head='<header class="book-title"><p class="eyebrow">Operational objectives</p><h1>Use-case catalog</h1><p>'+esc(catalog['description'])+'</p><p>Choose the objective first. Follow its workflow, inspect the required and optional mechanisms, then select a configuration profile. Cadence, connectivity and publication choices are variants rather than duplicate cases.</p><div class="dependency-path"><span>Operational outcome</span> → <span>Workflow step</span> → <span>Mechanism</span> → <span>Platform feature</span> → <span>Configuration and evidence</span></div></header>'
    body='<main id="main" class="catalog-main" data-usecase-catalog>'+head+content(catalog,guides)+'</main>'
    write('catalog/index.html',decorate(frame('Operational use-case catalog',body,'catalog')))
    lines=['# Operational use-case catalog',catalog['description'],'[Mechanisms](mechanisms.html) · [Features](features.html) · [Implementation profiles](profiles.html) · [Former-record mapping](migration.md)']
    for e in catalog['entries']:
        lines += ['## '+e['id']+' — '+e['title'],'**Actor:** '+e['actor'],'**Objective:** '+e['objective'],*e['narrative'],'### Completion criteria',*['- '+x for x in e['completion']],'### Workflow and dependencies']
        for i,s in enumerate(e['workflow'],1):
            lines += [f'#### {i}. {s["title"]}',s['purpose'],'**Responsible actor:** '+s['actor'],'**Mechanism:** '+('['+s['mechanism']+']('+address(s['mechanism'])+')' if s['mechanism'] else 'Team procedure; no native agent function asserted.'),'**Dependency:** '+s['dependency']+' — '+s['condition'],'**Configuration features:** '+', '.join('['+f+']('+address(f)+')' for f in s['configuration_features']),'**Effect:** '+s['effect'],'**Verification:** '+s['verification'],'**Failure handling:** '+s['on_failure']]
        for v in e['variants']:lines+=['### Variant: '+v['name'],v['changes'],v['controls']]
        lines+=['### Implementation profiles',', '.join('['+p+']('+address(p)+')' for p in e['profiles']),'**Detailed guide:** '+', '.join('['+sid+'](../guides/'+e['platform']+'.html#'+sid+')' for sid in e['sections'])]
    write('catalog/use-cases.md','\n\n'.join(lines))
    migration=['# Use-case consolidation mapping','The table maps every former record to its current outcome, mechanism or profile. It retains identifiers and reasons, not superseded document copies. Prior prose remains in Git history.','| Former ID | Former label | Decision | Current destination |','|---|---|---|---|']
    for a in records('aliases'):migration.append('| '+a['id']+' | '+a['title']+' | '+a['disposition']+' | '+'; '.join('['+t+']('+address(t)+')' for t in a['targets'])+' |')
    write('catalog/migration.md','\n'.join(migration))
    reference_pages(catalog,guides,frame,write)
