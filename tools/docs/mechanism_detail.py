"""Render mechanism detail in the existing guides; validate separately from live operation.

The review field in catalog/mechanisms.json owns the detailed mechanism prose.
Generated, delimited Markdown blocks keep GitHub's readable edition aligned with
HTML and speaker notes. Prose outside those blocks remains manually maintained.
"""
from pathlib import Path
from collections import defaultdict, Counter
from copy import deepcopy
from html import escape
from urllib.parse import urlsplit
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
BASELINE='75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9'
DATE='2026-10-22'
REQUIRED={'primary_section','kind','inputs','narrative','configuration','lifecycle','controls','observable_output','undocumented','test','claims'}
STABLE=('use-cases','features','profiles','aliases','resource-models')
CORE=('id','platform','title','features','sections','trigger','state','process','effect','verification','on_failure')


def load():
    return json.loads((ROOT/'catalog/mechanisms.json').read_text(encoding='utf-8'))


def esc(value):
    return escape(str(value),quote=True)


def markdown_table(headers,rows):
    def cell(value):
        return str(value).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers),*['| '+' | '.join(cell(v) for v in row)+' |' for row in rows]])


def block(entry):
    d=entry['review'];refs=list(dict.fromkeys(c['source'] for c in d['claims']))
    cite=' '.join('['+r+']' for r in refs)
    lines=[f"#### {entry['id']} — {entry['title']}",'']
    lines.extend(p+' '+cite+'\n' for p in d['narrative'])
    lines.extend(['**Inputs.** '+d['inputs'],''])
    if d.get('diagram'):
        lines.extend([f"![{entry['title']}: state and control paths](../assets/diagrams/{d['diagram']}.svg)",''])
    lines.extend(['**Configuration**',''])
    for i,(control,procedure,scope) in enumerate(d['configuration'],1):
        lines.append(f'{i}. **{control} — {scope.rstrip(".")}.** {procedure}')
    lines.extend(['',cite,'','**Lifecycle and operator actions**','',
                  markdown_table(['Initial condition','Operation or event','Result'],d['lifecycle']), '',
                  '**Constraints.** '+d['controls'],'',
                  '**Inspection points.** '+d['observable_output'],'',
                  '**Implementation limits.** '+d['undocumented'],'',
                  '**Verification procedure (proposed)**',''])
    for i,t in enumerate(d['test'],1):lines.append(f'{i}. {t}')
    lines.append('')
    if entry.get('related_mechanisms'):
        lines.append('**Related mechanism.** '+' '.join(f"[{r['id']}](../catalog/mechanisms.html#{r['id']}): {r['dependency']} — {r['condition']}" for r in entry['related_mechanisms']))
        lines.append('')
    lines.extend(['**Source mapping**','',markdown_table(['Reference','Documentation section','Supported behavior'],[['['+c['source']+']',c['section'],c['assertion']] for c in d['claims']]),''])
    return '\n'.join(lines)


def section_boundaries(body):
    """Locate canonical sections without treating headings inside examples as structure."""
    marks=[];offset=0;fence=None
    for line in body.splitlines(keepends=True):
        marker=re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            token=marker[1]
            if fence is None:fence=(token[0],len(token))
            elif token[0]==fence[0] and len(token)>=fence[1]:fence=None
            offset+=len(line);continue
        if fence is None:
            section=re.match(r'^###\s+([DSFA]-(?:M|U)?\d+)\s+[—-]\s+',line)
            if section:marks.append((offset,section[1]))
            elif re.match(r'^##\s+\d{2}\.\s+',line):marks.append((offset,None))
        offset+=len(line)
    result={}
    for i,(start,sid) in enumerate(marks):
        if sid:result[sid]=(start,marks[i+1][0] if i+1<len(marks) else len(body))
    return result


def sync_guides():
    data=load();groups=defaultdict(lambda:defaultdict(list))
    for e in data['entries']:groups[e['platform']][e['review']['primary_section']].append(e)
    for product,sections in groups.items():
        path=ROOT/f'guides/{product}.md';text=path.read_text(encoding='utf-8')
        text=re.sub(r'\n*<!-- mechanism-review:start [^>]+ -->.*?<!-- mechanism-review:end [^>]+ -->\n*','\n\n',text,flags=re.S)
        # Remove only this register's generated reference definitions before appending once.
        for ref in data['review_sources']:
            text=re.sub(r'^\['+re.escape(ref)+r'\]:[^\n]*\n?','',text,flags=re.M)
        definition_start=re.search(r'^\[[DSFA]S\d+\]:',text,re.M)
        if not definition_start:raise ValueError(product+': missing reference definitions')
        body=text[:definition_start.start()].rstrip();definitions=text[definition_start.start():].strip()
        boundaries=section_boundaries(body);inserts=[]
        for sid,items in sections.items():
            if sid=="D-07":items=sorted(items,key=lambda e:e["id"]!="MX-D-QUERY")
            if sid not in boundaries:raise ValueError('Unknown mechanism section '+sid)
            end=boundaries[sid][1]
            content=f'\n\n<!-- mechanism-review:start {sid} -->\n\n'+ '\n\n'.join(block(e) for e in items)+f'\n<!-- mechanism-review:end {sid} -->\n\n'
            inserts.append((end,content))
        for position,content in sorted(inserts,reverse=True):body=body[:position].rstrip()+content+body[position:]
        refs={c['source'] for items in sections.values() for e in items for c in e['review']['claims']}
        newdefs='\n'.join('['+r+']: '+data['review_sources'][r]['url'] for r in sorted(refs))
        path.write_text(re.sub(r'\n{3,}', '\n\n', body.rstrip()+'\n\n'+definitions+'\n'+newdefs+'\n'),encoding='utf-8')


def index_summary(entry):
    d=entry.get('review')
    if not d:return ''
    refs=load()['review_sources'];ident=entry['id'];product=entry['platform']
    text='<section class="mechanism-review-summary"><h3>Configuration, lifecycle and verification</h3>'
    text+='<p><strong>'+esc(d['kind'])+'.</strong> '+esc(d['inputs'])+'</p>'
    text+='<p><a href="../guides/'+product+'.html#'+ident+'">Read the configuration, lifecycle, and verification procedure</a></p>'
    text+='<p><strong>Implementation limits.</strong> '+esc(d['undocumented'])+'</p>'
    text+='<ul class="claim-evidence">'+''.join('<li><a href="'+esc(refs[c['source']]['url'])+'">'+esc(c['source']+' — '+c['section'])+'</a>: '+esc(c['assertion'])+'</li>' for c in d['claims'])+'</ul>'
    if entry.get('related_mechanisms'):
        text+='<h3>Conditional related mechanisms</h3><ul>'+''.join('<li><a href="mechanisms.html#'+esc(r['id'])+'">'+esc(r['id'])+'</a> — '+esc(r['dependency']+': '+r['condition'])+'</li>' for r in entry['related_mechanisms'])+'</ul>'
    parents=[p for p in load()['entries'] if any(r['id']==ident for r in p.get('related_mechanisms',[]))]
    if parents:text+='<p>Related from: '+' · '.join('<a href="mechanisms.html#'+esc(p['id'])+'">'+esc(p['title'])+'</a>' for p in parents)+'</p>'
    return text+'</section>'


def source_record():
    data=load()
    return {'reviewed_on':DATE,'stage':3,'scope':'Mechanism behavior, configuration and lifecycle; not a whole-service audit.',
            'sources':data['review_sources'],
            'claims':{e['id']:e['review']['claims'] for e in data['entries']},
            'qualifications':['Some official direct-page and indexed-page revisions differ; relevant record notes identify those differences.','State labels are logical explanations, not invented API enum names.','Similarity algorithms, ranking, exact retry guarantees and unsupported recovery operations remain undocumented.'],
            'live_aws_execution':False}


def review_errors(data,guides):
    errors=[];entries=data['entries'];ids={e['id'] for e in entries};sources=data.get('review_sources',{})
    for e in entries:
        mid=e['id'];d=e.get('review',{})
        missing=REQUIRED-set(d)
        if missing:errors.append(mid+': missing reviewed fields '+','.join(sorted(missing)));continue
        if d['primary_section'] not in e['sections'] or d['primary_section'] not in guides[e['platform']]['sections']:errors.append(mid+': unresolved primary explanation')
        for field in REQUIRED:
            if not d[field]:errors.append(mid+': empty '+field)
        for field in ('configuration','lifecycle'):
            if any(len(row)!=3 or not all(row) for row in d[field]):errors.append(mid+': invalid '+field+' row')
        for c in d['claims']:
            if not all(c.get(f) for f in ('source','section','assertion')):errors.append(mid+': incomplete supported claim')
            if c.get('source') not in sources:errors.append(mid+': unresolved claim source')
        for related in e.get('related_mechanisms',[]):
            if related.get('id') not in ids:errors.append(mid+': unknown related mechanism')
            if related.get('dependency') not in ('optional','conditional') or not related.get('condition'):errors.append(mid+': unqualified related dependency')
    for ident,s in sources.items():
        if urlsplit(s['url']).hostname!='docs.aws.amazon.com':errors.append(ident+': non-official source')
        if s.get('reviewed_on')!=DATE or not s.get('scope'):errors.append(ident+': incomplete review provenance')
    return errors


def validate(guides,browser=False):
    data=load();errors=review_errors(data,guides);preserved={};results=[]
    for name in STABLE:
        rel=f'catalog/{name}.json';old=subprocess.check_output(['git','show',BASELINE+':'+rel],cwd=ROOT)
        current=(ROOT/rel).read_bytes();same=old==current
        preserved[rel]={'unchanged':same,'sha256':hashlib.sha256(current).hexdigest()}
        if not same:errors.append(rel+': approved source changed')
    old=json.loads(subprocess.check_output(['git','show',BASELINE+':catalog/mechanisms.json'],cwd=ROOT))['entries']
    current={e['id']:e for e in data['entries']};changed=[]
    for e in old:
        if e['id'] not in current:errors.append(e['id']+': former mechanism removed');continue
        fields=[f for f in CORE if current[e['id']].get(f)!=e.get(f)]
        if fields:changed.append({'id':e['id'],'fields':fields})
    edit_record=ROOT/'qa/technical-edit-record.json'
    permitted=json.loads(edit_record.read_text())['core_corrections'] if edit_record.exists() else []
    for item in changed:
        old_entry=next(e for e in old if e['id']==item['id'])
        for field in item['fields']:
            matches=[c for c in permitted if c['id']==item['id'] and c['field']==field and c['before']==old_entry.get(field) and c['after']==current[item['id']].get(field)]
            if len(matches)!=1:errors.append(item['id']+': unreviewed summary change '+field)
    if set(current)-{e['id'] for e in old}!={'MX-S-PERSONALIZE'}:errors.append('Unexpected mechanism addition')
    # Mutation tests establish that checks reject defects rather than only counting records.
    regression=[]
    bad=deepcopy(data);bad['entries'][0]['review']['lifecycle']=[]
    if not any('empty lifecycle' in x for x in review_errors(bad,guides)):errors.append('Missing-lifecycle regression not detected')
    else:regression.append('Missing lifecycle rejected')
    bad=deepcopy(data);bad['entries'][0]['review']['claims'][0]['source']='UNKNOWN'
    if not any('unresolved claim source' in x for x in review_errors(bad,guides)):errors.append('Unsupported-claim regression not detected')
    else:regression.append('Unresolved claim evidence rejected')
    bad=deepcopy(data);bad['entries'][0]['related_mechanisms']=[{'id':'UNKNOWN','dependency':'conditional','condition':''}]
    if not any('unqualified related dependency' in x for x in review_errors(bad,guides)):errors.append('Conditional-dependency regression not detected')
    else:regression.append('Missing condition and unknown related mechanism rejected')
    for product in ('devops','security','finops'):
        page=BeautifulSoup((ROOT/f'guides/{product}.html').read_text(),'html.parser')
        for e in data['entries']:
            if e['platform']!=product:continue
            node=page.find(id=e['id'])
            if not node or node.name!='h4':errors.append(e['id']+': detailed guide anchor missing')
    for mid in ('MX-D-CUSTOM','MX-F-FILES','MX-S-PERSONALIZE','MX-F-JIRA','MX-F-SLACK'):
        if not current[mid]['review']['undocumented']:errors.append(mid+': unknown boundary missing')
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for width in (390,1440):
                page=br.new_page(viewport={'width':width,'height':1000});js=[];page.on('pageerror',lambda err:js.append(str(err)))
                try:
                    for mid in ('MX-D-RECALL','MX-S-PERSONALIZE','MX-F-SLACK'):
                        e=current[mid];page.goto((ROOT/'catalog/mechanisms.html').as_uri()+'#'+mid)
                        page.locator('#'+mid+' .mechanism-review-summary a[href*="../guides/"]').click()
                        page.wait_for_function('(mid)=>location.hash==="#"+mid',arg=mid)
                        assert page.locator('h4#'+mid).is_visible()
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    page.goto((ROOT/'catalog/mechanisms.html').as_uri()+'#MX-S-FINDING')
                    page.locator('#MX-S-FINDING a[href="mechanisms.html#MX-S-PERSONALIZE"]').click()
                    assert page.locator('#MX-S-PERSONALIZE').is_visible()
                    assert not js
                    results.append({'width':width,'mechanism_to_detailed_procedure':'passed','conditional_personalization_link':'passed','javascript_errors':js})
                except Exception as exc:errors.append('Mechanism detail browser '+str(width)+': '+str(exc))
                finally:page.close()
            br.close()
    result={'stage':3,'reviewed_on':DATE,'baseline':BASELINE,'reviewed_mechanisms':len(data['entries']),
            'distribution':dict(Counter(e['platform'] for e in data['entries'])),
            'official_sources':len(data['review_sources']),'claim_mappings':sum(len(e['review']['claims']) for e in data['entries']),
            'approved_sources':preserved,'old_mechanism_core_fields_preserved':not changed,
            'added_mechanism':'MX-S-PERSONALIZE','reviewed_core_corrections':permitted,'regression_checks':regression,'browser':results,'errors':errors,
            'boundary':'Document-level review and proposed test plans, not live AWS execution or an exhaustive internal algorithm specification.'}
    (ROOT/'qa/mechanism-review.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'qa/mechanism-source-review.json').write_text(json.dumps(source_record(),ensure_ascii=False,indent=2)+'\n')
    return result
