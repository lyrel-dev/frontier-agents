"""Product resource model rendering and validation.

Canonical entity, relationship and source data live in catalog/resource-models.json.
The approved use-case and mechanism catalogs are read, never rewritten here.
"""
from __future__ import annotations
import copy
import hashlib
import html
import json
import re
import subprocess
import textwrap
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'catalog/resource-models.json'
PRODUCTS = ('devops', 'security', 'finops')


def load():
    return json.loads(SOURCE.read_text(encoding='utf-8'))


def esc(value):
    return html.escape(str(value), quote=True)


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def source_links(ids, model):
    return ' '.join(f'<a href="{esc(model["sources"][sid]["url"])}" title="{esc(model["sources"][sid]["section"])}">{sid}</a>' for sid in ids)


def legend(model):
    return '<div class="ownership-legend" aria-label="Concept ownership">' + ''.join(
        f'<span style="background:{v["fill"]};border-color:{v["stroke"]}"><strong>{v["tag"]}</strong> {esc(v["label"])}</span>'
        for v in model['legend'].values()
    ) + '</div>'


def dot_node(entity, model):
    palette = model['legend'][entity['owner']]
    label = '[' + palette['tag'] + '] ' + '\n'.join(textwrap.wrap(entity['name'], width=28))
    label += '\n' + entity.get('kind', 'concept')
    return f'{q(entity["id"])} [label={q(label)},fillcolor={q(palette["fill"])},color={q(palette["stroke"])},fontcolor="#152636",style="rounded,filled",shape=box];'


def dot_legend(model):
    lines = ['subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;']
    for i, (owner, v) in enumerate(model['legend'].items()):
        short = {'documentation':'Documentation-defined', 'aws':'AWS-defined', 'external':'External / engineering-owned'}[owner]
        lines.append(f'legend_{i} [label={q(v["tag"]+" · "+short)},fillcolor={q(v["fill"])},color={q(v["stroke"])},style=filled,fontsize=10];')
    lines.append('legend_0 -> legend_1 -> legend_2 [style=invis];}')
    return '\n'.join(lines)


def diagram_definitions():
    model = load()
    result = {}
    for key, product in model['products'].items():
        entities = {e['id']:e for e in product['entities']}
        relationships = {r['id']:r for r in product['relationships']}
        for view in product['views']:
            lines = ['rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];']
            lines.extend(dot_node(entities[i], model) for i in view['nodes'])
            for ident in view['edges']:
                r = relationships[ident]
                if r['from'] not in view['nodes'] or r['to'] not in view['nodes']:
                    raise ValueError('Diagram relationship has missing endpoint: '+ident)
                cardinality = f'{r["sources_per_target"]} : {r["targets"]}'
                label = r['verb'] + '\n' + cardinality
                style = 'solid' if r['basis']=='documented' else 'dashed'
                lines.append(f'{q(r["from"])} -> {q(r["to"])} [label={q(label)},style={q(style)}];')
            lines.append(dot_legend(model))
            description = ('Colors identify concept ownership; labels distinguish resources, configuration members and derived state. '
                           'An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.')
            result[view['key']] = (view['title'], description, view['sections'], '\n'.join(lines))
    concepts = {c['id']:dict(c,kind='documentation concept' if c['owner']=='documentation' else 'external evidence or process') for c in model['concepts']}
    lines = ['rankdir=TB; nodesep=0.25; ranksep=0.4; node [fontsize=11,margin="0.10,0.07"]; edge [fontsize=10];']
    lines.extend(dot_node(c,model) for c in concepts.values())
    for a,b,label in [
        ('C-USECASE','C-VARIANT','has optional variants'),('C-USECASE','C-WORKFLOW','is achieved through'),
        ('C-WORKFLOW','C-STEP','orders'),('C-STEP','C-MECHANISM','uses conditionally'),
        ('C-CAPABILITY','C-MECHANISM','groups explanations'),('C-MECHANISM','C-FEATURE','uses documented facilities'),
        ('C-PROFILE','C-USECASE','implements selected variant'),('C-PROFILE','C-BINDING','specifies configuration'),
        ('C-FEATURE','C-BINDING','maps to actual types'),('X-EVIDENCE','C-STEP','supplies observations'),
        ('C-STEP','X-REVIEW','provides result for acceptance')]:
        lines.append(f'{q(a)} -> {q(b)} [label={q(label)},style=dashed];')
    for key, ident in [('devops','D-Custom'),('security','S-Pentest'),('finops','F-Automation')]:
        entity=next(e for e in model['products'][key]['entities'] if e['id']==ident)
        lines.append(dot_node(entity,model))
        lines.append(f'"C-BINDING" -> {q(ident)} [label="product-specific example",style=dashed];')
    lines.append(dot_legend(model))
    result['er-concept-model'] = ('The documentation model and its AWS resource bindings',
        'The blue entities are the approved explanatory vocabulary. Green examples are named product configurations, not equivalent resources. Orange nodes retain the external evidence and review boundary. Product diagrams refine this model.',
        ['A-10','A-11'], '\n'.join(lines))
    return result


CSS = '''
.ownership-legend{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.ownership-legend span{border:1px solid;padding:6px 10px;font-size:13px;color:#152636;border-radius:3px}.model-intro{max-width:85ch}.model-controls{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0}.model-controls input{flex:2;min-width:180px}.model-controls select{flex:1;min-width:150px}.model-controls>*{padding:9px}.model-record{border-top:1px solid #bccbd5;padding:20px 0;scroll-margin-top:20px}.model-record h3{margin:0 0 10px}.model-identity{font-family:monospace;font-size:13px;overflow-wrap:anywhere}.model-scope{font-size:13px;color:#415566}.model-evidence{font-size:13px}.model-index{max-width:1180px;margin:auto;padding:32px}.resource-binding{margin:14px 0;font-size:14px;border-left:3px solid #447AC2;padding:8px 12px}.model-relations th,.model-relations td{font-size:13px}.model-basis{font-weight:600}.model-product>h2{border-bottom:2px solid #183b69;padding:20px 0 12px}.model-title-note{max-width:88ch}.model-links a{display:inline-block;margin:3px 8px 3px 0}.model-record[hidden],.model-product[hidden]{display:none!important}
@media(max-width:700px){.model-index{padding:16px}.model-controls>*{min-width:0!important;width:100%}.model-identity{font-size:12px}}
@media print{.model-controls{display:none!important}.model-record[hidden],.model-product[hidden]{display:block!important}.model-record{break-inside:avoid}}
'''
JS = '''
(()=>{const root=document.querySelector('[data-resource-model]');if(!root)return;
const search=root.querySelector('#resource-search'),product=root.querySelector('#resource-product'),owner=root.querySelector('#resource-owner');
const rows=[...root.querySelectorAll('.model-record')],status=root.querySelector('#resource-status');
function run(){const q=search.value.trim().toLowerCase();let n=0;rows.forEach(el=>{const yes=(!product.value||el.dataset.product===product.value)&&(!owner.value||el.dataset.owner===owner.value)&&(!q||el.textContent.toLowerCase().includes(q));el.hidden=!yes;n+=yes?1:0});root.querySelectorAll('.model-product').forEach(el=>{el.hidden=!!product.value&&product.value!==el.dataset.product});status.textContent=n+' of '+rows.length+' entities shown';}
[search,product,owner].forEach(el=>el.addEventListener('input',run));root.querySelector('#resource-reset').onclick=()=>{search.value='';product.value='';owner.value='';run()};
function hash(){const el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el&&el.classList.contains('model-record')){search.value='';owner.value='';product.value=el.dataset.product;run();el.scrollIntoView();}}
addEventListener('hashchange',hash);run();hash();})();
'''


def case_features(case, mechanisms):
    ids=set()
    for step in case.get('workflow',[]):
        ids.update(step.get('configuration_features',[]))
        mid=step.get('mechanism')
        if mid in mechanisms:ids.update(mechanisms[mid].get('features',[]))
    return ids


def resource_index(guides, frame, write, figure):
    model=load()
    features={e['id']:e for e in json.loads((ROOT/'catalog/features.json').read_text())['entries']}
    mechanisms={e['id']:e for e in json.loads((ROOT/'catalog/mechanisms.json').read_text())['entries']}
    cases=json.loads((ROOT/'catalog/use-cases.json').read_text())['entries']
    refs={c['id']:case_features(c,mechanisms) for c in cases}
    chunks=['<main id="main" class="model-index" data-resource-model><header class="book-title"><p class="eyebrow">Stage 2 · Product-specific resource models</p><h1>Product resource models</h1><p class="model-intro">The approved use cases describe objectives. This reference identifies the actual configuration, execution and evidence objects used to implement them. Follow a feature to its resource bindings, then inspect the relationship and lifecycle in the product guide. The model does not turn every concept into a creatable AWS resource.</p>'+legend(model)+'<p class="model-title-note">'+esc(model['boundary'])+'</p></header>']
    chunks.append('<div class="model-controls"><input id="resource-search" type="search" aria-label="Search resource models" placeholder="Search entity, identity, purpose or use case"><select id="resource-product" aria-label="Product"><option value="">All products</option>'+''.join(f'<option value="{k}">{esc(p["title"])}</option>' for k,p in model['products'].items())+'</select><select id="resource-owner" aria-label="Concept ownership"><option value="">All ownership classes</option>'+''.join(f'<option value="{k}">{esc(v["label"])}</option>' for k,v in model['legend'].items())+'</select><button id="resource-reset">Reset</button><button data-print>Print</button></div><p id="resource-status" aria-live="polite"></p>')
    md=['# Product resource models','',model['boundary'],'',model['notation']['ownership'],'',model['notation']['range'],'']
    for key,p in model['products'].items():
        entities={e['id']:e for e in p['entities']}
        chunks.append(f'<section class="model-product" data-product="{key}" id="model-{key}"><h2>{esc(p["title"])}</h2><p><a href="../guides/{key}.html#{p["overview_section"]}">Read the model overview</a> · <a href="../guides/{key}.html#{p["dictionary_section"]}">Read relationships and lifecycle</a> · <a href="../guides/{key}.html#{p["application_section"]}">Follow the approved use cases through the model</a></p>')
        for view in p['views']:
            chunks.append(figure(view['key'],'resource-index-'+view['key']))
        chunks.append('<h3>Entity dictionary</h3><p>Identity describes how the object is located, not a proposed universal key. Configuration members and managed state are explicitly distinguished from independently addressable resources.</p>')
        md+=['## '+p['title'],'','| Entity | Ownership / kind | Identity and scope | Meaning |','|---|---|---|---|']
        for e in p['entities']:
            used_by=[fid for fid,ids in p['feature_bindings'].items() if e['id'] in ids]
            impacted=[c for c in cases if refs[c['id']]&set(used_by)]
            palette=model['legend'][e['owner']]
            links=' '.join(f'<a href="features.html#{fid}">{esc(features[fid]["title"])}</a>' for fid in used_by)
            outcomes=' '.join(f'<a href="index.html#{c["id"]}">{esc(c["title"])}</a>' for c in impacted)
            chunks.append(f'<section class="model-record" id="{e["id"]}" data-product="{key}" data-owner="{e["owner"]}"><h3><span style="background:{palette["fill"]};border:1px solid {palette["stroke"]};padding:2px 5px;font-size:12px">{palette["tag"]}</span> {esc(e["name"])}</h3><p class="model-scope">{esc(e["kind"])} · {esc(e["scope"])}</p><p>{esc(e["meaning"])}</p><p class="model-identity">Identity: {esc(e["identity"])}</p><p class="model-evidence">Evidence: {source_links(e["sources"],model) if e["sources"] else "External or authored concept; no native resource claim."}</p><p class="model-links"><strong>Feature references:</strong> {links or "Foundational scope or explanatory entity."}</p><p class="model-links"><strong>Related outcomes:</strong> {outcomes or "See the product model overview."}</p></section>')
            md.append('| '+e['name']+' | '+e['owner']+' / '+e['kind']+' | '+e['identity']+'; '+e['scope']+' | '+e['meaning']+' |')
        chunks.append('<h3>Relationship register</h3><p>'+esc(model['notation']['range'])+' '+esc(model['notation']['basis'])+'</p><div class="table-wrap"><table class="model-relations"><thead><tr><th>Relationship</th><th>Targets/source</th><th>Sources/target</th><th>Evidence class and qualification</th></tr></thead><tbody>')
        md+=['','### Relationships','','| Source → relationship → target | Targets/source | Sources/target | Basis and qualification |','|---|---|---|---|']
        for r in p['relationships']:
            a,b=entities[r['from']],entities[r['to']]
            relation=esc(a['name'])+' → '+esc(r['verb'])+' → '+esc(b['name'])
            chunks.append(f'<tr id="{r["id"]}"><td><a href="#{a["id"]}">{esc(a["name"])}</a> → {esc(r["verb"])} → <a href="#{b["id"]}">{esc(b["name"])}</a></td><td>{r["targets"]}</td><td>{r["sources_per_target"]}</td><td><span class="model-basis">{r["basis"]}.</span> {esc(r["note"])} {source_links(r["sources"],model)}</td></tr>')
            md.append('| '+a['name']+' → '+r['verb']+' → '+b['name']+' | '+r['targets']+' | '+r['sources_per_target']+' | '+r['basis']+'. '+r['note']+' |')
        chunks.append('</tbody></table></div></section>')
    chunks.append('<section id="source-register"><h2>Official evidence and review boundaries</h2><p>Reviewed on '+esc(model['reviewed_on'])+'. The fields below identify the sections used, including differences between indexed and cached versions. This is not an exhaustive audit of every retained guide claim.</p>')
    md+=['','## Official evidence','']
    for sid,s in model['sources'].items():
        chunks.append(f'<p id="source-{sid}"><strong>{sid}</strong> · <a href="{esc(s["url"])}">{esc(s["section"])}</a>. {esc(s["basis"])}. {esc(s.get("qualification",""))}</p>')
        md.append(f'- [{sid}]({s["url"]}): {s["section"]}. {s["basis"]}. '+s.get('qualification',''))
    chunks.append('</section><p>Reverse dependencies describe possible documentation relationships. A conditional profile is not automatically required, and this index is not an account inventory or readiness test.</p></main>')
    page=frame('Product resource models',''.join(chunks),'reference')
    page=page.replace('</style>',CSS+'\n</style>',1).replace('</body>','<script>'+JS+'</script></body>')
    write('catalog/resource-models.html',page)
    write('catalog/resource-models.md','\n'.join(md))
    review={'reviewed_on':model['reviewed_on'],'baseline':model['baseline'],'scope':model['scope'],'sources':{}}
    for sid,s in model['sources'].items():
        rows=[]
        for p in model['products'].values():
            rows += [e['id'] for e in p['entities'] if sid in e['sources']]
            rows += [r['id'] for r in p['relationships'] if sid in r['sources']]
        review['sources'][sid]=dict(s,supports=rows)
    write('qa/product-source-review.json',json.dumps(review,indent=2,ensure_ascii=False))


def integrate_pages(write):
    """Add resource links to generated views, not to approved source records."""
    model=load()
    pages=[ROOT/'index.html',ROOT/'presentations/index.html',ROOT/'catalog/index.html',ROOT/'catalog/mechanisms.html',ROOT/'catalog/features.html',ROOT/'catalog/profiles.html']
    pages += [ROOT/f'guides/{k}.html' for k in (*PRODUCTS,'architecture')]
    pages += [ROOT/f'presentations/{k}.html' for k in (*PRODUCTS,'architecture')]
    for path in pages:
        soup=BeautifulSoup(path.read_text(),'html.parser')
        prefix='' if path.parent==ROOT else '../'
        nav=soup.select_one('.site-header nav')
        if nav and not nav.find('a',href=prefix+'catalog/resource-models.html'):
            a=soup.new_tag('a',href=prefix+'catalog/resource-models.html');a.string='Resource models';nav.append(a)
        if path.name=='features.html':
            for key,p in model['products'].items():
                lookup={e['id']:e for e in p['entities']}
                for fid,ids in p['feature_bindings'].items():
                    target=soup.find(id=fid)
                    if target:
                        block=BeautifulSoup('<p class="resource-binding"><strong>Product resource bindings:</strong> '+', '.join(f'<a href="resource-models.html#{i}">{esc(lookup[i]["name"])}</a>' for i in ids)+'</p>','html.parser').p
                        target.append(block)
        style=soup.find('style')
        if style:style.append('\n'+CSS)
        write(path.relative_to(ROOT),str(soup))


def validate(guides, browser=False):
    model=load();errors=[];ids=[];bindings={};count_rel=0
    fields={'id','name','owner','kind','identity','scope','meaning','sources'}
    allowed_ranges={'?','1','0..1','0..*','1..*'}
    features={e['id']:e for e in json.loads((ROOT/'catalog/features.json').read_text())['entries']}
    for key,p in model['products'].items():
        entities={e['id']:e for e in p['entities']}
        if len(entities)!=len(p['entities']):errors.append(key+': duplicate entity')
        for e in p['entities']:
            ids.append(e['id'])
            if fields-set(e):errors.append(e['id']+': incomplete entity')
            if e['owner'] not in model['legend']:errors.append(e['id']+': unknown ownership')
            if e['owner']=='aws' and not e['sources']:errors.append(e['id']+': AWS concept has no evidence')
            if not set(e['sources'])<=set(model['sources']):errors.append(e['id']+': unresolved source')
        for r in p['relationships']:
            count_rel+=1;ids.append(r['id'])
            if r['from'] not in entities or r['to'] not in entities:errors.append(r['id']+': unresolved entity')
            if r['targets'] not in allowed_ranges or r['sources_per_target'] not in allowed_ranges:errors.append(r['id']+': invalid multiplicity')
            if r['basis'] not in ('documented','logical','editorial'):errors.append(r['id']+': unclassified relationship')
            if not r.get('note') or not r['sources'] or not set(r['sources'])<=set(model['sources']):errors.append(r['id']+': missing relationship qualification/evidence')
        for fid,eids in p['feature_bindings'].items():
            bindings[fid]=eids
            if fid not in features or features[fid]['platform']!=key:errors.append(fid+': cross-product feature binding')
            if not eids or not set(eids)<=set(entities):errors.append(fid+': unresolved binding')
        for sid in (p['overview_section'],p['dictionary_section'],p['application_section']):
            if sid not in guides[key]['sections']:errors.append(key+': missing model explanation '+sid)
        for view in p['views']:
            if len(view['nodes'])!=len(set(view['nodes'])):errors.append(view['key']+': duplicate node')
            if not set(view['nodes'])<=set(entities):errors.append(view['key']+': invalid node')
    if set(bindings)!=set(features):errors.append('Feature/resource crosswalk differs from the approved feature index')
    if len(ids)!=len(set(ids)):errors.append('Resource-model identifiers are not unique')
    for sid,s in model['sources'].items():
        if urlsplit(s['url']).hostname!='docs.aws.amazon.com':errors.append(sid+': non-official evidence')
    preserved={}
    # Mechanism review has its own core-field preservation check in Stage 3.
    for name in ('use-cases','features','profiles','aliases'):
        path=f'catalog/{name}.json'
        previous=subprocess.check_output(['git','show',model['baseline']+':'+path],cwd=ROOT)
        current=(ROOT/path).read_bytes();same=previous==current
        preserved[path]={'unchanged':same,'sha256':hashlib.sha256(current).hexdigest()}
        if not same:errors.append(path+': approved source changed during resource specialization')
    entities={e['id']:e for p in model['products'].values() for e in p['entities']}
    # Semantic regressions address previous overgeneralizations, not word counts.
    assert entities['S-SelectedResult']['owner']=='documentation'
    assert 'AgentSpace' in entities['F-Agent']['identity'] and 'finops-agent' in entities['F-Agent']['identity']
    assert entities['D-Topology']['kind']=='derived view'
    assert entities['S-Login']['kind']=='managed procedural state'
    assert not any(r['from']=='S-Design' and r['verb']=='is executed as' for r in model['products']['security']['relationships'])
    assert next(r for r in model['products']['finops']['relationships'] if r['id']=='FR11')['targets']=='?'
    browser_results=[]
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for width in (390,1440):
                page=br.new_page(viewport={'width':width,'height':1000});js=[]
                page.on('pageerror',lambda err:js.append(str(err)))
                try:
                    page.goto((ROOT/'catalog/resource-models.html').as_uri())
                    assert page.locator('.model-record:visible').count()==len(entities)
                    page.locator('#resource-product').select_option('finops')
                    assert page.locator('.model-record:visible').count()==len(model['products']['finops']['entities'])
                    page.locator('#resource-search').fill('no-such-resource-q927');assert page.locator('.model-record:visible').count()==0
                    page.evaluate("location.hash='S-SelectedResult'");page.wait_for_timeout(100)
                    assert page.locator('#S-SelectedResult').is_visible()
                    page.locator('#resource-reset').click();page.locator('#resource-owner').select_option('documentation')
                    assert page.locator('#S-SelectedResult').is_visible()
                    assert not page.locator('#S-Space').is_visible()
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    page.emulate_media(media='print');assert page.locator('.model-record:visible').count()==len(entities)
                    page.emulate_media(media='screen')
                    assert not js
                    browser_results.append({'width':width,'entity_search_ownership_product_hash_print':'passed','javascript_errors':js})
                except Exception as exc:errors.append('Resource index '+str(width)+': '+str(exc))
                finally:page.close()
            br.close()
    result={'reviewed_on':model['reviewed_on'],'products':len(model['products']),'entities':len(entities),'relationships':count_rel,'feature_bindings':len(bindings),'official_references':len(model['sources']),'approved_sources':preserved,'semantic_checks':['Named FinOps AgentSpace alias remains service-specific','One-off design review is not converted to reusable configuration','Revalidation result association remains documentation-defined','Topology is a derived view, not authorization scope','Retained login procedure is not an asserted CRUD resource','Unspecified event-rule multiplicity remains unknown'],'browser':browser_results,'errors':errors,'boundary':model['boundary']}
    (ROOT/'qa/resource-models.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
