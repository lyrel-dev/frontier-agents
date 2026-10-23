"""One-time export from the existing publication into canonical Markdown sources.

This command refuses to replace an existing content/ directory. It does not
remove the previous inputs; retirement is a separate reviewed change.
"""
from pathlib import Path
import json
import uuid
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'content'
BASELINE = '4a34aaadc5f9fd0e4dbb492c36aa152730c8ba5a'
if DEST.exists():
    raise SystemExit('content/ already exists; migration will not overwrite it')
from build import load_guides
import structure
import presentation
import diagrams
import teaching_diagrams

old_guides = load_guides()
old_registers = {p.stem: (p.read_text(), json.loads(p.read_text())) for p in (ROOT/'catalog').glob('*.json')}
old_chapters = structure.CHAPTERS
old_decks = presentation.DECKS
old_diagrams = dict(diagrams.DIAGRAMS)
parser = MarkdownIt('commonmark', {'html': False}).enable('table')


def mark(body, ident):
    if not body.strip():
        return ''
    lines = body.strip('\n').splitlines(keepends=True)
    starts = sorted({t.map[0] for t in parser.parse(''.join(lines)) if t.map and t.level == 0 and t.type != 'inline'})
    if not starts or starts[0] != 0:
        starts.insert(0, 0)
    result = []
    for i, start in enumerate(starts):
        end = starts[i+1] if i+1 < len(starts) else len(lines)
        text = ''.join(lines[start:end]).strip('\n')
        if text:
            bid = 'b-' + uuid.uuid5(uuid.NAMESPACE_URL, ident+':'+str(i)).hex[:20]
            result += [f'<!-- block: {bid} -->', text, '']
    return '\n'.join(result).rstrip()+'\n'


def save(rel, meta, body=''):
    path = DEST/rel
    path.parent.mkdir(parents=True, exist_ok=True)
    text = '---\n'+yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100000)+'---\n\n'+mark(body, meta['id'])
    path.write_text(text, encoding='utf-8')


for product, guide in old_guides.items():
    save(f'guides/{product}/index.md', {'id':'guide-'+product, 'kind':'guide', 'product':product,
         'title':old_decks[product]['title'], 'output':f'guides/{product}.html', 'references':guide['refs']}, guide['intro'])
    for number, chapter in enumerate(old_chapters[product], 1):
        definition = {k:v for k,v in chapter.items() if k not in ('purpose','title')}
        save(f'guides/{product}/chapters/{number:02d}-{chapter["slug"]}.md',
             {'id':f'chapter-{product}-{chapter["slug"]}', 'kind':'chapter', 'product':product,
              'order':number, 'title':chapter['title'], 'definition':definition}, chapter['purpose'])
    for number, (sid, section) in enumerate(guide['sections'].items(), 1):
        save(f'guides/{product}/sections/{sid}.md', {'id':sid,'kind':'section','product':product,
             'title':section['title'],'order':number}, section['body'])

for product, deck in old_decks.items():
    definition = {k:v for k,v in deck.items() if k not in ('slides','subtitle')}
    save(f'presentations/{product}/index.md', {'id':'deck-'+product,'kind':'deck','product':product,
         'title':deck['title'],'definition':definition,'chapters':structure.DECK_CHAPTERS[product]}, deck.get('subtitle',''))
    for number, slide in enumerate(deck['slides'], 1):
        definition = {k:v for k,v in slide.items() if k not in ('data','message','title','explain')}
        body = []
        if slide['kind'] == 'diagram':
            body += [f'![{old_diagrams[slide["diagram"]][0]}](../assets/diagrams/{slide["diagram"]}.svg)', '']
            body += [f'{i}. {text}' for i,text in enumerate(slide.get('explain',[]),1)]
        elif slide['kind'] in ('table','demo'):
            rows = slide['data'] if slide['kind']=='table' else [['Time','Action','Prepared evidence'],*slide['data']]
            def cell(value):
                return str(value).replace('\\','\\\\').replace('|','\\|').replace('\n',' ')
            body += ['| '+' | '.join(cell(x) for x in rows[0])+' |','| '+' | '.join('---' for _ in rows[0])+' |']
            body += ['| '+' | '.join(cell(x) for x in row)+' |' for row in rows[1:]]
        else:
            for heading,text in slide['data']:
                body += ['## '+heading,'',text,'']
        body += ['','## Presenter notes','',slide['message']]
        save(f'presentations/{product}/{number:02d}.md', {'id':f'slide-{product}-{number:02d}',
             'kind':'slide','product':product,'title':slide['title'],'order':number,'definition':definition}, '\n'.join(body))


def split_record(data):
    paragraphs = []
    def walk(value, keys=()):
        if isinstance(value,dict):
            return {k:walk(v,(*keys,k)) for k,v in value.items()}
        if isinstance(value,list):
            return [walk(v,(*keys,str(i))) for i,v in enumerate(value)]
        if isinstance(value,str) and (len(value)>90 or '\n' in value or any(k in ('narrative','process','purpose','setup','tests','definition','description') for k in keys)):
            field = f'field-{len(paragraphs)+1:04d}'
            heading = ' / '.join(keys).replace('_',' ')
            paragraphs.append(f'## {heading}\n\n<!-- field: {field} -->\n{value}\n<!-- /field -->')
            return {'$markdown':field}
        return value
    return walk(data), '\n\n'.join(paragraphs)

for name,(raw,register) in old_registers.items():
    metadata = dict(register)
    frozen = name in ('use-cases','mechanisms','features','profiles','aliases','resource-models')
    if isinstance(register.get('entries'),list):
        refs=[]
        for index,entry in enumerate(register['entries']):
            rid=entry.get('id',f'item-{index:04d}')
            source_id='record-'+name+'-'+rid
            data,body=split_record(entry)
            save(f'registers/{name}/{rid}.md',{'id':source_id,'kind':'record','collection':name,
                 'product':entry.get('platform',''),'title':entry.get('title',rid),'order':index,'frozen':frozen,'data':data},body)
            refs.append({'$record':source_id})
        metadata['entries']=refs
    if name=='resource-models':
        metadata['products']={}
        for product,value in register['products'].items():
            data,body=split_record(value)
            source_id='model-'+product
            save(f'registers/resource-models/{product}.md',{'id':source_id,'kind':'record','collection':name,
                 'product':product,'title':product+' resource model','frozen':True,'data':data},body)
            metadata['products'][product]={'$record':source_id}
    fmt=None
    for indent in (2,4,None):
        for ascii_flag in (True,False):
            for newline in (True,False):
                if json.dumps(register,indent=indent,ensure_ascii=ascii_flag)+('\n' if newline else '')==raw:
                    fmt={'indent':indent,'ensure_ascii':ascii_flag,'newline':newline}
    if fmt is None:
        raise ValueError('Unknown JSON formatting: '+name)
    data,body=split_record(metadata)
    save(f'registers/{name}/index.md',{'id':'register-'+name,'kind':'register','collection':name,
         'title':name+' register','frozen':frozen,'json_format':fmt,'data':data},body)

for ident,(title,description,refs,dot) in old_diagrams.items():
    language='dot' if dot.strip() else 'svg'
    code=dot.strip() if language=='dot' else (ROOT/f'assets/diagrams/{ident}.svg').read_text().strip()
    save(f'diagrams/{ident}.md',{'id':ident,'kind':'diagram','title':title,'refs':refs},description+'\n\n```'+language+'\n'+code+'\n```')

prefix='digraph G { graph [bgcolor="transparent",pad="0.25",nodesep="0.35",ranksep="0.6",fontname="DejaVu Sans",fontsize=16]; node [shape=box,style="rounded,filled",fillcolor="#edf5f4",color="#496b78",fontcolor="#142c3e",fontname="DejaVu Sans",fontsize=14,margin="0.18,0.12"]; edge [color="#496b78",fontname="DejaVu Sans",fontsize=11,arrowsize=0.75];\n'
save('configuration/diagram-defaults.md',{'id':'settings-diagram-defaults','kind':'settings','data':{'graph_prefix':prefix}})
save('configuration/structure.md',{'id':'settings-structure','kind':'settings','data':{'baseline':structure.BASELINE,'types':structure.TYPES,'labels':structure.LABELS}})
save('configuration/teaching-layout.md',{'id':'settings-teaching-layout','kind':'settings','data':{'boxes':teaching_diagrams.BOXES,'products':teaching_diagrams.PRODUCTS}})
# The report is verification evidence, not an alternative editable source.
(ROOT/'qa/markdown-migration.json').write_text(json.dumps({'baseline':BASELINE,
    'guide_sections':sum(len(g['sections']) for g in old_guides.values()),
    'slides':sum(len(d['slides']) for d in old_decks.values()),'diagrams':len(old_diagrams),
    'registers':sorted(old_registers),'markdown_sources':len(list(DEST.rglob('*.md')))},indent=2)+'\n')
print('Exported Markdown sources; run the preservation test before publication.')
