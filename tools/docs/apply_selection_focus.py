"""Apply focused nested-element selection corrections; remove after application."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'tools/docs'
p=HERE/'contextual_check.py';s=p.read_text()
old="                    if tag=='diagram':target.focus()"
new="                    # Enter explicitly opens the whole container handle; hover may target its nested cell/item.\n                    target.focus();page.keyboard.press('Enter')"
assert old in s;s=s.replace(old,new);p.write_text(s)
p=HERE/'review.js';s=p.read_text()
old="    const first=ownerBlock(range.startContainer),last=ownerBlock(range.endContainer);"
new="""    const mappedOwner=value=>(value?.nodeType===1?value:value?.parentElement)?.closest('[data-review-block]');
    const first=mappedOwner(range.startContainer)||ownerBlock(range.startContainer),last=mappedOwner(range.endContainer)||ownerBlock(range.endContainer);"""
assert old in s;s=s.replace(old,new)
s=s.replace('  let active = null, anchor = null, quote = null, selectionRect = null;', '  let keyboardScope=false;\n  let active = null, anchor = null, quote = null, selectionRect = null;')
s=s.replace("if(inUI(event.target)||drag||!panel.hidden)return;", "if(inUI(event.target)||drag||!panel.hidden||keyboardScope)return;")
s=s.replace("else if(event.key==='Enter' && ownerBlock(event.target)===event.target){event.preventDefault();activate(event.target);handle.focus({preventScroll:true});}", "else if(event.key==='Enter' && ownerBlock(event.target)===event.target){event.preventDefault();keyboardScope=true;activate(event.target);handle.focus({preventScroll:true});}")
needle="  document.addEventListener('pointerout',event=>"
insert="""  document.addEventListener('pointermove',event=>{
    if(keyboardScope&&(event.movementX||event.movementY)&&!inUI(event.target)){
      keyboardScope=false;const block=ownerBlock(event.target);if(block&&panel.hidden&&!drag)activate(block);
    }
  });
  document.addEventListener('pointerout',event=>"""
assert needle in s;s=s.replace(needle,insert)
p.write_text(s)
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
