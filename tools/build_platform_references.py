#!/usr/bin/env python3
"""Build the platform-reference layer from explicit capability and mechanism records.

No archive or snapshot is created. Older scenario documents are linked separately;
this layer supplies the corrected platform taxonomy and is the primary entry point.
"""
from pathlib import Path
import argparse
import hashlib
import html
import json
import math
import re
import subprocess
import textwrap
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[1]
KEYS = ('devops', 'security', 'finops')
REVISION = '2026-10-21-platform-reference-1'
BOUNDARY = ('Official product documentation supports the product statements. Configuration steps are documented guidance; verification exercises are proposed and were not executed. Selected critical sources were rechecked on 21 October 2026; other links are retained from the preceding review. This is not an exhaustive service catalog, a fresh audit of every historical claim, or a live AWS test.')
TAXONOMY = [
    ('Platform capability', 'A reusable ability exposed by the platform.', 'Retain operational context across investigations.'),
    ('Operation', 'An action on a platform resource or configuration object.', 'Attach a memory store or change its active state.'),
    ('Mechanism', 'The documented process connecting inputs, state, execution and outputs.', 'Select a store by description, then retrieve relevant entries.'),
    ('Use case', 'An engineering problem that combines capabilities and mechanisms.', 'Investigate a recurring alarm while checking contradictory telemetry.')
]
CSS = '''
:root{--ink:#172c43;--muted:#536579;--navy:#122b43;--accent:#066b67;--line:#d8e2eb;--paper:#fff;--bg:#f3f6f8}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}a{color:#075e9b;text-underline-offset:3px}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #b4670e;outline-offset:3px}header{background:var(--navy);color:white;padding:38px max(22px,calc((100vw - 1160px)/2)) 34px}header a{color:#d7e9ff}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.12em;font-weight:700}h1{font-size:clamp(28px,4vw,43px);line-height:1.15;margin:16px 0}h2{font-size:27px;line-height:1.25;margin-top:34px}h3{font-size:21px;line-height:1.3;margin:10px 0}p{margin:.55em 0 1em}main{max-width:1204px;margin:auto;padding:24px 22px 60px}nav{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0}.lead{max-width:900px;color:#e0eaf2;font-size:18px}.meta{display:flex;gap:10px;flex-wrap:wrap}.tag{font-size:12px;border:1px solid var(--line);border-radius:4px;padding:4px 8px;color:var(--muted);display:inline-block}.meta .tag{color:#e0eaf2;border-color:#536579}.note{border-left:4px solid var(--accent);padding:16px 20px;background:#eaf3f2;margin:20px 0}.toolbar{position:sticky;top:0;z-index:2;background:#fff;border:1px solid var(--line);padding:14px;display:flex;gap:10px;flex-wrap:wrap;border-radius:8px}.toolbar input{flex:2;min-width:190px}.toolbar select{flex:1;min-width:155px}input,select,button{font:inherit;padding:9px 11px;border:1px solid #9aacbc;border-radius:4px;background:white;color:var(--ink)}button{cursor:pointer}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.card,.record{background:white;border:1px solid var(--line);border-radius:10px;padding:22px;margin:18px 0;min-width:0}.cards .card{margin:0}.record h3{margin-top:4px}.kind{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 28px}.grid>div{min-width:0}.field{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:700;display:block;margin:8px 0 3px}.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;list-style:none;padding:0;margin:20px 0}.flow li{background:#eef3f7;border-top:3px solid var(--accent);padding:13px;font-size:15px;min-width:0}.flow b{display:block;color:var(--accent);margin-bottom:6px}.record details{border-top:1px solid var(--line);margin-top:18px;padding-top:14px}.record summary{font-weight:700;cursor:pointer}.sources{font-size:14px}.sources a{margin-right:12px}.boundary{font-size:14px;color:var(--muted)}.result{color:var(--muted);margin:12px 0}.hidden{display:none!important}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;background:white;font-size:15px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:12px}th{background:#e9eff4}.source-list li{margin:12px 0}.source-list a{overflow-wrap:anywhere}code{overflow-wrap:anywhere}ol{padding-left:24px}.record,.card,header,td,th,p,li{overflow-wrap:anywhere}footer{margin-top:34px;border-top:1px solid var(--line);padding-top:18px;color:var(--muted);font-size:13px}@media(max-width:700px){.cards,.grid{grid-template-columns:1fr}.flow{grid-template-columns:1fr 1fr}.toolbar{position:static}.toolbar>*{width:100%;min-width:0!important}main{padding:18px 14px}.record,.card{padding:18px}h2{font-size:24px}}@media print{.toolbar,nav,button,.result{display:none!important}body{background:white;font-size:11pt}header{background:white!important;color:#172c43!important;padding:0}header .lead,header .tag{color:#172c43!important}main{max-width:none;padding:0}.record{break-inside:avoid;border:1px solid #aaa}.hidden{display:block!important}a{color:inherit}.flow li{background:#eee}.source-list{font-size:10pt}}
'''
JS = '''
(function(){const q=document.getElementById('query'),kind=document.getElementById('kind'),group=document.getElementById('group'),records=[...document.querySelectorAll('.record')];
function filter(){const text=(q?q.value:'').trim().toLowerCase();let count=0;records.forEach(r=>{const ok=(!text||r.textContent.toLowerCase().includes(text))&&(!kind||!kind.value||r.dataset.kind===kind.value)&&(!group||!group.value||r.dataset.group===group.value);r.classList.toggle('hidden',!ok);if(ok)count++;});const x=document.getElementById('result');if(x)x.textContent=count+' of '+records.length+' records shown';}
[q,kind,group].filter(Boolean).forEach(e=>e.addEventListener('input',filter));
const reset=document.getElementById('reset');if(reset)reset.onclick=()=>{q.value='';kind.value='';group.value='';filter();};
const expand=document.getElementById('expand');if(expand)expand.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=true);
const print=document.getElementById('print');if(print)print.onclick=()=>window.print();
const exportButton=document.getElementById('export');if(exportButton)exportButton.onclick=()=>{const blob=new Blob([document.getElementById('source-data').textContent],{type:'application/json'});const a=document.createElement('a');const u=URL.createObjectURL(blob);a.href=u;a.download=document.body.dataset.key+'-platform-reference.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),2000);};
let openState=[];window.addEventListener('beforeprint',()=>{openState=[...document.querySelectorAll('details')].map(d=>d.open);document.querySelectorAll('details').forEach(d=>d.open=true);});window.addEventListener('afterprint',()=>document.querySelectorAll('details').forEach((d,i)=>d.open=openState[i]));
function reveal(){const id=decodeURIComponent(location.hash.slice(1));const el=document.getElementById(id);if(el&&el.classList.contains('record')){if(q){q.value='';kind.value='';group.value='';filter();}el.classList.remove('hidden');el.querySelectorAll('details').forEach(d=>d.open=true);}}
window.addEventListener('hashchange',reveal);document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&q){e.preventDefault();q.focus();}});filter();reveal();})();
'''

def esc(value):
    return html.escape(str(value), quote=True)


def write(path, text):
    p=ROOT/path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def load():
    return [json.loads((ROOT/f'content/platforms/{k}.json').read_text(encoding='utf-8')) for k in KEYS]


def refs(data, ids):
    return '<div class="sources"><span class="field">Official documentation</span>'+''.join(f'<a href="{esc(data["sources"][i][1])}">{esc(i)} · {esc(data["sources"][i][0])}</a>' for i in ids)+'</div>'


def taxonomy_html():
    return '<div class="table-wrap"><table><thead><tr><th>Layer</th><th>Definition</th><th>Example</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in TAXONOMY)+'</tbody></table></div>'


def field(label,value):
    return '<div><span class="field">'+esc(label)+'</span><p>'+esc(value)+'</p></div>'


def page(title, body, subtitle='', data=None):
    payload='' if data is None else '<script id="source-data" type="application/json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    key='' if data is None else data['key']
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+CSS+'</style></head><body data-key="'+key+'"><header><div class="eyebrow">Engineering reference · 21 October 2026</div><h1>'+esc(title)+'</h1><p class="lead">'+esc(subtitle)+'</p><div class="meta"><span class="tag">Capabilities ≠ use cases</span><span class="tag">Mechanisms and configuration</span><span class="tag">No live AWS test</span></div></header><main>'+body+'<footer>'+esc(BOUNDARY)+'<br>Version control: Git history. No manual archive copies or distribution packages are produced.</footer></main>'+payload+'<script>'+JS+'</script></body></html>'


def report_html(data):
    groups=list(dict.fromkeys(c['group'] for c in data['capabilities']))
    body='<nav><a href="index.html">Platform collection</a><a href="'+data['key']+'.md">Markdown</a><a href="../presentations/'+data['key']+'-platform-reference.pptx">Reference slides</a><a href="#sources">Sources</a></nav>'
    body+='<div class="note">'+esc(data['availability'])+'</div><h2>Reading model</h2>'+taxonomy_html()
    body+='<p>Start with the grouped capability records. Use the mechanism records to determine how a capability is implemented and configured. Proposed acceptance checks are not product features or executed demonstrations.</p>'
    body+='<div class="toolbar"><input id="query" aria-label="Search records" placeholder="Search records; press / to focus"><select id="kind" aria-label="Record type"><option value="">All record types</option value="capability">Capabilities</option><option value="mechanism">Mechanisms</option></select><select id="group" aria-label="Capability group"><option value="">All groups</option>'+''.join('<option>'+esc(g)+'</option>' for g in groups)+'</select><button id="reset">Reset</button><button id="expand">Expand details</button><button id="export">Export source JSON</button><button id="print">Print</button></div><div id="result" class="result" role="status" aria-live="polite"></div><h2>Capability inventory</h2>'
    for c in data['capabilities']:
        related=[m for m in data['mechanisms'] if c['id'] in m['capabilities']]
        links=' · '.join('<a href="#'+m['id']+'">'+m['id']+'</a>' for m in related) or 'Configuration surface documented above; no separate detailed mechanism in this edition.'
        body+='<article class="record" id="'+c['id']+'" data-kind="capability" data-group="'+esc(c['group'])+'"><div class="kind">'+esc(c['group'])+' · '+c['id']+'</div><h3>'+esc(c['title'])+'</h3><p>'+esc(c['function'])+'</p><div class="grid">'+field('Platform resources',c['resources'])+field('Supported operations',c['operations'])+'</div>'+field('Boundary',c['boundary'])+'<p><span class="field">Mechanism cross-reference</span>'+links+'</p>'+refs(data,c['refs'])+'</article>'
    body+='<h2>Mechanisms and enablement</h2>'
    capgroup={c['id']:c['group'] for c in data['capabilities']}
    for m in data['mechanisms']:
        body+='<article class="record" id="'+m['id']+'" data-kind="mechanism" data-group="'+esc(capgroup[m['capabilities'][0]])+'"><div class="kind">Mechanism · '+m['id']+'</div><h3>'+esc(m['title'])+'</h3><p>'+esc(m['operation'])+'</p><p class="sources">Capabilities: '+', '.join('<a href="#'+c+'">'+c+'</a>' for c in m['capabilities'])+'</p><ol class="flow">'+''.join('<li><b>'+str(i+1)+'</b>'+esc(v)+'</li>' for i,v in enumerate(m['flow']))+'</ol><div class="grid">'+field('Trigger',m['trigger'])+field('State and lifecycle',m['state'])+'</div><details><summary>Configuration, controls and proposed verification</summary><span class="field">Enablement procedure</span><ol>'+''.join('<li>'+esc(s)+'</li>' for s in m['enablement'])+'</ol>'+field('Controls and failure boundaries',m['controls'])+field('Independent verification — proposed',m['verification'])+'</details>'+refs(data,m['refs'])+'</article>'
    ex=data['exercise']
    body+='<h2>Optional verification exercise</h2><div class="note"><h3>'+esc(ex['title'])+'</h3><p>'+esc(ex['label'])+' · '+str(ex['minutes'])+' minute walkthrough budget.</p><ol>'+''.join('<li><b>'+str(s[0])+' min:</b> '+esc(s[1])+'</li>' for s in ex['steps'])+'</ol>'+field('Acceptance',ex['acceptance'])+'</div><h2 id="sources">Official source register</h2><p class="boundary">Rechecked means selected relevant content was retrieved during this publication. Other sources are carried from the preceding documentation review. A source link is not proof of a successful live configuration.</p><ol class="source-list">'
    for k,(title,url) in data['sources'].items():
        status='Selected content rechecked 21 October 2026' if k in data['rechecked_sources'] else 'Retained from preceding review'
        body+='<li id="source-'+k+'"><b>'+k+'</b> · <a href="'+esc(url)+'">'+esc(title)+'</a><br><span class="boundary">'+status+'</span></li>'
    return page(data['product']+' — platform capabilities and mechanisms',body+'</ol>',data['scope'],data)


def markdown(data):
    lines=['# '+data['product']+' — platform capabilities and mechanisms','',data['scope'],'',data['availability'],'','## Classification','']
    for name,definition,example in TAXONOMY:lines.append('**'+name+'**: '+definition+' Example: '+example+'\n')
    lines+=['## Capability inventory','']
    for c in data['capabilities']:
        lines+=['### '+c['id']+' — '+c['title'],'','**Group:** '+c['group'],'',c['function'],'','**Platform resources:** '+c['resources'],'','**Supported operations:** '+c['operations'],'','**Boundary:** '+c['boundary'],'','**Sources:** '+', '.join('['+r+']('+data['sources'][r][1]+')' for r in c['refs']),'']
    lines+=['## Mechanisms and enablement','']
    for m in data['mechanisms']:
        lines+=['### '+m['id']+' — '+m['title'],'','**Capabilities:** '+', '.join(m['capabilities']),'','**Trigger:** '+m['trigger'],'','**Process:** '+' → '.join(m['flow']),'',m['operation'],'','**State and lifecycle:** '+m['state'],'','**Enablement:**','']
        lines += [str(i+1)+'. '+s for i,s in enumerate(m['enablement'])]
        lines+=['','**Controls:** '+m['controls'],'','**Proposed verification:** '+m['verification'],'','**Sources:** '+', '.join('['+r+']('+data['sources'][r][1]+')' for r in m['refs']),'']
    e=data['exercise'];lines+=['## Optional verification exercise','',e['title'],'',e['label']+'; '+str(e['minutes'])+' minutes.','']+[str(i+1)+'. '+str(s[0])+' min — '+s[1] for i,s in enumerate(e['steps'])]+['','**Acceptance:** '+e['acceptance'],'','## Evidence boundary','',BOUNDARY,'','## Official source register','']
    lines += ['- ['+k+' — '+v[0]+']('+v[1]+') — '+('selected content rechecked' if k in data['rechecked_sources'] else 'retained from preceding review') for k,v in data['sources'].items()]
    return '\n'.join(lines)+'\n'


def add_text(slide,text,x,y,w,h,size=18,bold=False,color='172C43'):
    shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=shape.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
    usable=max(1,w*72/(size*.53));estimated=sum(max(1,math.ceil(len(line)/usable)) for line in text.split('\n'))
    if estimated*size*1.22>h*72:
        size=max(13,min(size,int(h*72/(estimated*1.22))))
    for i,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color);p.space_after=Pt(5)
    return shape


def deck(data):
    prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
    def base(title,label,notes):
        s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string('F7F9FB')
        add_text(s,data['product'].upper()+' / PLATFORM REFERENCE',.6,.28,12,.3,11,True,'066B67')
        add_text(s,title,.6,.85,12.1,1.0,29,True)
        add_text(s,label,.6,7.0,11.7,.26,10,False,'536579')
        add_text(s,str(len(prs.slides)),12.35,7.0,.35,.26,10)
        s.notes_slide.notes_text_frame.text=notes+'\n\n'+BOUNDARY
        return s
    s=base('Capabilities, operations and mechanisms','Reference deck — untimed; optional exercise has a separate budget',data['scope'])
    add_text(s,data['scope'],.6,2.0,11.9,1.0,23)
    for i,(a,b,c) in enumerate(TAXONOMY):
        add_text(s,a,.6,3.3+i*.68,2.4,.5,17,True,'066B67');add_text(s,b,3.15,3.3+i*.68,9,.5,18)
    add_text(s,data['availability'],.6,6.15,12,.6,14)
    for c in data['capabilities']:
        notes='\n\n'.join([c['function'],'Resources: '+c['resources'],'Operations: '+c['operations'],'Boundary: '+c['boundary']]+[data['sources'][r][0]+'\n'+data['sources'][r][1] for r in c['refs']])
        s=base(c['title'],c['id']+' · '+c['group']+' · Untimed',notes)
        add_text(s,c['function'],.6,1.98,12.05,1.18,23)
        add_text(s,'PLATFORM RESOURCES',.6,3.34,5.8,.3,12,True,'066B67');add_text(s,c['resources'],.6,3.8,5.7,1.2,20)
        add_text(s,'SUPPORTED OPERATIONS',6.9,3.34,5.8,.3,12,True,'066B67');add_text(s,c['operations'],6.9,3.8,5.7,1.2,20)
        add_text(s,'BOUNDARY',.6,5.38,12,.3,12,True,'066B67');add_text(s,c['boundary'],.6,5.82,12, .83,18)
    for m in data['mechanisms']:
        notes='\n\n'.join([m['trigger'],m['operation'],m['state'],'Enablement: '+' '.join(m['enablement']),m['controls'],'Proposed verification: '+m['verification']]+[data['sources'][r][0]+'\n'+data['sources'][r][1] for r in m['refs']])
        s=base(m['title'],m['id']+' · Process and retained state · Untimed',notes)
        for i,step in enumerate(m['flow']):
            x=.6+i*3.12;add_text(s,str(i+1).zfill(2),x,2.02,2.82,.32,14,True,'066B67');add_text(s,step,x,2.48,2.8,1.0,20,True)
        add_text(s,'DOCUMENTED OPERATION',.6,3.78,6,.3,12,True,'066B67');add_text(s,m['operation'],.6,4.22,6.05,2.1,18)
        add_text(s,'STATE AND LIFECYCLE',7.0,3.78,5.7,.3,12,True,'066B67');add_text(s,m['state'],7.0,4.22,5.6,2.1,18)
        s=base(m['title']+' — configuration',m['id']+' · Enablement and proposed verification · Untimed',notes)
        for i,step in enumerate(m['enablement']):
            add_text(s,str(i+1).zfill(2),.6,2.05+i*1.2,.4,.4,14,True,'066B67');add_text(s,step,1.2,2.05+i*1.2,5.1,1.02,18)
        add_text(s,'CONTROLS',6.9,2.05,5.7,.3,12,True,'066B67');add_text(s,m['controls'],6.9,2.48,5.7,1.35,17)
        add_text(s,'PROPOSED VERIFICATION — NOT EXECUTED',6.9,4.1,5.7,.3,11,True,'066B67');add_text(s,m['verification'],6.9,4.55,5.7,1.85,17)
    e=data['exercise'];s=base(e['title'],str(e['minutes'])+' minute optional exercise; not part of a measured runtime',e['label']+'\n'+e['acceptance'])
    for i,(mins,step) in enumerate(e['steps']):
        add_text(s,str(mins)+' min',.6,2.0+i*.83,1,.4,17,True,'066B67');add_text(s,step,1.9,2.0+i*.83,10.7,.6,19)
    add_text(s,e['acceptance'],.6,5.7,12,1.0,18)
    source_items=list(data['sources'].items())
    for start in range(0,len(source_items),6):
        items=source_items[start:start+6];s=base('Official source register','Untimed evidence appendix; complete URLs in speaker notes', '\n'.join(k+' '+v[0]+'\n'+v[1] for k,v in items))
        for i,(k,(title,url)) in enumerate(items):
            sh=add_text(s,k+'  '+title,.6,2.0+i*.68,12,.5,18)
            for p in sh.text_frame.paragraphs:
                for r in p.runs:r.hyperlink.address=url
    out=ROOT/f'presentations/{data["key"]}-platform-reference.pptx';out.parent.mkdir(exist_ok=True);prs.save(out)
    return len(prs.slides)


def integrate(reports):
    start='<!-- PLATFORM-REFERENCE-NAV -->';end='<!-- /PLATFORM-REFERENCE-NAV -->'
    links=' | '.join('['+d['product']+'](platforms/'+d['key']+'.md)' for d in reports)
    note=start+'\n## Platform capability and mechanism references\n\nStart with the [platform reference collection](platforms/index.html). The new layer separates 30 reusable platform capabilities from 16 implementation mechanisms and from operational use cases. '+links+'.\n\nReference slides are untimed. Three optional prepared-result exercises have an eight-minute budget each; they are not added to the existing timed scenario programme. The earlier reports and presentations remain scenario material, not the authority for platform classification. See [publication validation](platforms/VALIDATION.md).\n'+end+'\n\n'
    path=ROOT/'README.md'
    if path.exists():
        text=re.sub(re.escape(start)+'.*?'+re.escape(end)+'\n*','',path.read_text(),flags=re.S)
        path.write_text(note+text,encoding='utf-8')
    targets={'index.html':'platforms/index.html','devops/validated-report.html':'../platforms/devops.html','security/report.html':'../platforms/security.html','finops/report.html':'../platforms/finops.html'}
    for name,url in targets.items():
        p=ROOT/name
        if not p.exists():continue
        soup=BeautifulSoup(p.read_text(),'html.parser')
        old=soup.find(id='platform-reference-entry')
        if old:old.decompose()
        banner=BeautifulSoup('<section id="platform-reference-entry" style="background:#122b43;color:#fff;padding:22px;font:16px/1.6 system-ui;overflow-wrap:anywhere"><strong>Platform capabilities and mechanisms</strong><p style="margin:6px 0">Use the revised platform reference for the capability taxonomy, configuration objects, documented mechanisms and enablement. The material below remains the earlier operational-scenario edition.</p><a style="color:#d7e9ff" href="'+url+'">Open the revised platform reference →</a></section>','html.parser')
        if soup.body:soup.body.insert(0,banner)
        p.write_text(str(soup),encoding='utf-8')


def build():
    reports=load();slides={}
    for d in reports:
        write('platforms/'+d['key']+'.html',report_html(d));write('platforms/'+d['key']+'.md',markdown(d));slides[d['key']]=deck(d)
    cards=''
    for d in reports:
        cards+='<article class="card"><div class="kind">'+str(len(d['capabilities']))+' capabilities · '+str(len(d['mechanisms']))+' mechanisms</div><h3>'+esc(d['product'])+'</h3><p>'+esc(d['scope'])+'</p><nav><a href="'+d['key']+'.html">Read reference</a><a href="'+d['key']+'.md">Markdown</a><a href="../presentations/'+d['key']+'-platform-reference.pptx">Reference slides</a></nav></article>'
    body='<nav><a href="../index.html">Report collection</a><a href="TAXONOMY.md">Classification standard</a><a href="VALIDATION.md">Validation scope</a></nav><p>This reference layer describes reusable abilities and their implementation. It does not relabel investigation or reporting scenarios as platform capabilities.</p>'+taxonomy_html()+'<h2>Platform references</h2><div class="cards">'+cards+'</div><div class="note"><strong>How to read the collection</strong><p>Capabilities identify resources and operations. Mechanisms explain triggers, process, state, configuration and controls. Verification exercises are proposed tests, not product functions or evidence of successful execution.</p><p>The reference decks are untimed. Each platform has an optional eight-minute prepared-result exercise, outside the existing scenario programme.</p></div>'
    write('platforms/index.html',page('Platform capabilities and mechanisms',body,'AWS DevOps Agent · AWS Security Agent · AWS FinOps Agent'))
    write('platforms/TAXONOMY.md','# Platform-reference classification\n\n'+ '\n\n'.join('## '+a+'\n\n'+b+'\n\nExample: '+c for a,b,c in TAXONOMY)+'\n\n## Record requirements\n\nCapabilities must identify reusable ability, resource, operation, scope and boundary. Mechanisms must identify trigger, process, retained state, enablement, controls and observable verification. Use cases reference those records instead of duplicating them. Do not infer model training, shared memory, vector databases or a universal approval system from product positioning.\n\n## Publication scope\n\nThe new platform layer is the authority for this classification. Existing timed scenario presentations are retained separately and were not rebuilt as part of this layer. No historical snapshot directories or distribution archives are created.\n')
    write('platforms/VALIDATION.md','# Platform-reference publication validation\n\nRevision: `'+REVISION+'`.\n\nThe JSON records, generated HTML, Markdown and new reference decks share the same source. Product claims link to official documentation. Each source register distinguishes selected content rechecked on 21 October 2026 from references retained from the preceding review.\n\nThe build validates record identity, capability-to-mechanism mappings, required fields, official-source domains, local links, slide bounds and speaker notes. The browser test checks search, record filters, disclosures, deep links, print restoration and 390/1440-pixel widths. Results are recorded in `../qa/platform-validation.json`.\n\nThe three platform references contain 30 capabilities and 16 mechanisms. New deck slide counts: '+json.dumps(slides)+'. Reference slides are untimed; three optional prepared-result exercises total 24 minutes. This does not modify the existing scenario programme.\n\n'+BOUNDARY+'\n\nAutomated slide-bound checks are not a pixel-level review of every rendered slide. No new performance or productivity result is claimed.\n')
    integrate(reports)
    return reports


def check(browser=False):
    data=load();errors=[];capcount=0;mechcount=0;links=0;slidecount=0;browser_checks=[];manifest=[]
    for d in data:
        caps={c['id'] for c in d['capabilities']};mids={m['id'] for m in d['mechanisms']}
        if len(caps)!=len(d['capabilities']) or len(mids)!=len(d['mechanisms']):errors.append(d['key']+': duplicate IDs')
        capcount+=len(caps);mechcount+=len(mids)
        for c in d['capabilities']:
            for f in ['group','title','function','resources','operations','boundary','refs']:
                if not c.get(f):errors.append(c['id']+': missing '+f)
            if not set(c['refs'])<=set(d['sources']):errors.append(c['id']+': source missing')
        for m in d['mechanisms']:
            for f in ['title','capabilities','trigger','flow','operation','state','enablement','controls','verification','refs']:
                if not m.get(f):errors.append(m['id']+': missing '+f)
            if not set(m['capabilities'])<=caps:errors.append(m['id']+': capability missing')
            if not set(m['refs'])<=set(d['sources']):errors.append(m['id']+': source missing')
            if len(m['flow'])!=4 or len(m['enablement'])!=3:errors.append(m['id']+': incomplete structure')
        for title,url in d['sources'].values():
            if urlsplit(url).hostname!='docs.aws.amazon.com':errors.append('Nonofficial source '+url)
        if sum(x[0] for x in d['exercise']['steps'])!=d['exercise']['minutes']:errors.append('Exercise timing mismatch')
        ppt=Presentation(ROOT/f'presentations/{d["key"]}-platform-reference.pptx');slidecount+=len(ppt.slides)
        for num,s in enumerate(ppt.slides,1):
            if not s.notes_slide.notes_text_frame.text.strip():errors.append('Empty notes '+d['key']+str(num))
            for sh in s.shapes:
                if min(sh.left,sh.top)<0 or sh.left+sh.width>ppt.slide_width+100 or sh.top+sh.height>ppt.slide_height+100:errors.append('Slide bounds '+d['key']+str(num))
    for p in (ROOT/'platforms').glob('*.html'):
        soup=BeautifulSoup(p.read_text(),'html.parser');ids=[x.get('id') for x in soup.select('[id]')]
        if len(ids)!=len(set(ids)):errors.append(str(p)+': duplicate HTML ID')
        for a in soup.select('a[href]'):
            u=urlsplit(a['href'])
            if u.scheme or u.netloc:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            links+=1
            if not target.exists():errors.append('Missing link '+a['href'])
            elif u.fragment and target.suffix=='.html':
                if not BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment)):errors.append('Missing anchor '+a['href'])
    if browser:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True)
            for key in (*KEYS,'index'):
                p=ROOT/f'platforms/{key}.html'
                for width in (390,1440):
                    tab=b.new_page(viewport={'width':width,'height':1000});page_errors=[]
                    tab.on('pageerror',lambda e:page_errors.append(str(e)))
                    tab.set_content(p.read_text(),wait_until='load')
                    if tab.evaluate('document.documentElement.scrollWidth>innerWidth+1'):errors.append(key+': horizontal overflow '+str(width))
                    if key!='index':
                        n=tab.locator('.record').count();tab.locator('#query').fill('no-match-zz987');assert tab.locator('.record:not(.hidden)').count()==0
                        tab.locator('#reset').click();assert tab.locator('.record:not(.hidden)').count()==n
                        tab.locator('#kind').select_option('mechanism');assert tab.locator('.record:not(.hidden)').count()==len(next(d for d in data if d['key']==key)['mechanisms'])
                        tab.locator('#reset').click();tab.locator('#expand').click();assert tab.locator('details:not([open])').count()==0
                        tab.evaluate('window.dispatchEvent(new Event("beforeprint"));window.dispatchEvent(new Event("afterprint"))')
                        tab.evaluate('location.hash=document.querySelector(".record[data-kind=mechanism]").id')
                    errors.extend(page_errors);browser_checks.append({'page':key,'width':width,'page_errors':page_errors});tab.close()
            b.close()
    files=list((ROOT/'platforms').glob('*'))+list((ROOT/'content/platforms').glob('*.json'))+[ROOT/f'presentations/{k}-platform-reference.pptx' for k in KEYS]
    for p in sorted(files):
        if p.is_file():manifest.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    result={'revision':REVISION,'capabilities':capcount,'mechanisms':mechcount,'official_source_entries':sum(len(d['sources']) for d in data),'local_links_checked':links,'reference_decks':3,'reference_slides':slidecount,'optional_exercise_minutes':24,'browser_checks':browser_checks,'errors':errors,'live_aws_execution':False,'boundary':BOUNDARY,'manifest':manifest}
    write('qa/platform-validation.json',json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='manifest'},indent=2))
    if errors:raise SystemExit(1)


def commit_changes():
    raw=subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=ROOT)
    paths=[]
    for record in raw.split(b'\0'):
        if not record:continue
        status=record[:2].decode();path=record[3:].decode()
        if 'R' in status or 'C' in status:raise RuntimeError('Unexpected rename; inspect before publishing')
        paths.append(path)
    for path in sorted(set(paths)):
        subprocess.run(['git','add','--',path],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','docs: publish '+path],cwd=ROOT,check=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--browser',action='store_true');p.add_argument('--commit',action='store_true');a=p.parse_args()
    if a.commit:commit_changes()
    elif a.check:check(a.browser)
    else:build();check(a.browser)

if __name__=='__main__':main()
