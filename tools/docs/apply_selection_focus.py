"""Apply focused nested-element selection corrections; remove after application."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'tools/docs'
p=HERE/'contextual_check.py';s=p.read_text()
old="                    if tag=='diagram':target.focus()"
new="                    # Focus explicitly selects the whole container; hover may target a nested cell/item.\n                    target.focus()"
assert old in s;s=s.replace(old,new);p.write_text(s)
p=HERE/'review.js';s=p.read_text()
old="    const first=ownerBlock(range.startContainer),last=ownerBlock(range.endContainer);"
new="""    const mappedOwner=value=>(value?.nodeType===1?value:value?.parentElement)?.closest('[data-review-block]');
    const first=mappedOwner(range.startContainer)||ownerBlock(range.startContainer),last=mappedOwner(range.endContainer)||ownerBlock(range.endContainer);"""
assert old in s;s=s.replace(old,new);p.write_text(s)
# Keep generated supplementary links under the owning section, not its final prose subsection.
p=HERE/'selection_model.py';s=p.read_text()
old="        for child in list(section.contents):\n            if isinstance(child, Tag) and re.fullmatch(r'h[4-6]', child.name or ''):"
new="""        for child in list(section.contents):
            if isinstance(child, Tag) and any(c in child.get('class',[]) for c in ('feature-reference','related-reading')):
                stack=[(3,section)]
            if isinstance(child, Tag) and re.fullmatch(r'h[4-6]', child.name or ''):"""
assert old in s;s=s.replace(old,new);p.write_text(s)
print('Explicit container focus, mapped text offsets and subsection ownership corrected.')
Path(__file__).unlink()
