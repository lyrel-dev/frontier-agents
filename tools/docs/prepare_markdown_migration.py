"""One-time migration prerequisite; removed after use."""
from pathlib import Path
import ast
p=Path(__file__).resolve().parent/'md_source.py'
s=p.read_text();tree=ast.parse(s);f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='stamp_text')
replacement='''def stamp_text(text, prefix='b'):
    """Persist anchors while preserving every authored character between them."""
    if re.search(r'^<!-- block:',text,flags=re.M):return text
    lines=text.splitlines(keepends=True);ranges=[];end=0
    for t in MD.parse(text):
        if t.map and t.level==0 and t.map[0]>=end:
            a,b=t.map
            if a>end and ''.join(lines[end:a]).strip():ranges.append((end,a))
            ranges.append((a,b));end=b
    if ''.join(lines[end:]).strip():ranges.append((end,len(lines)))
    if not ranges and text.strip():ranges=[(0,len(lines))]
    out=[];cursor=0
    for i,(a,b) in enumerate(ranges,1):
        out.append(''.join(lines[cursor:a]))
        raw=''.join(lines[a:b]);has_newline=raw.endswith('\\n')
        if has_newline:raw=raw[:-1]
        ident=prefix+'-'+f'{i:04d}'+'-'+digest(raw)[:8]
        out.append('<!-- block: '+ident+' -->\\n'+raw+'\\n<!-- /block -->'+('\\n' if has_newline else ''))
        cursor=b
    out.append(''.join(lines[cursor:]))
    return ''.join(out)
'''
lines=s.splitlines(True);lines[f.lineno-1:f.end_lineno]=[replacement];p.write_text(''.join(lines))
Path(__file__).unlink()
