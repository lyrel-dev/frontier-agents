"""Apply focused nested-element selection corrections; remove after application."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'tools/docs'
p=HERE/'contextual_check.py';s=p.read_text()
old="                    if tag=='diagram':target.focus()"
new="                    # Enter explicitly opens the whole container handle; hover may target its nested cell/item.\n                    target.focus();page.keyboard.press('Enter')"
assert old in s;s=s.replace(old,new);p.write_text(s)
p=HERE/'hierarchy_check.py';s=p.read_text()
old="                heading.hover();page.locator('#review-block-select').click(modifiers=['Control'])"
new="""                # select_option dispatches a change without moving the test pointer;
                # leave and return as a real user does before selecting the child.
                page.mouse.move(1,1);heading.hover()
                expect(page.locator('#review-block-controls')).to_have_attribute('data-scope-id',title_scope)
                page.locator('#review-block-select').click(modifiers=['Control'])"""
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
s=s.replace("if(parent){scopePath.push(id);choose(hierarchy.element(parent));}","if(parent){scopePath.push(id);choose(hierarchy.element(parent),{scopeExpansion:true});}")
s=s.replace("if(child)choose(child);return;}","if(child)choose(child,{scopeExpansion:true});return;}")
s=s.replace("    const id=hierarchy.key(element);if(!hierarchy.nodes[id])return;\n    quote=null;", "    const id=hierarchy.key(element);if(!hierarchy.nodes[id])return;\n    if(!event.scopeExpansion)scopePath=[];\n    quote=null;")
old="Return JSON with schema `frontier-source-patch/v1`"
new="Structural selection roots describe reader-visible scopes, not whole-file permission. Only the captured targets authorize edits; context_ids and newly added descendants do not. A shared canonical target may render in several documents, so inspect all affected outputs rather than creating duplicate source copies.\\n\\nReturn JSON with schema `frontier-source-patch/v1`"
assert old in s;s=s.replace(old,new)
p.write_text(s)
p=HERE/'selection_model.py';s=p.read_text()
old="        for child in list(section.contents):\n            if isinstance(child, Tag) and re.fullmatch(r'h[4-6]', child.name or ''):"
new="""        for child in list(section.contents):
            if isinstance(child, Tag) and any(c in child.get('class',[]) for c in ('feature-reference','related-reading')):
                stack=[(3,section)]
            if isinstance(child, Tag) and re.fullmatch(r'h[4-6]', child.name or ''):"""
assert old in s;s=s.replace(old,new);p.write_text(s)
p=ROOT/'content/site/authoring.md';s=p.read_text()
s=s.replace('No Review mode needs to be enabled. Hover over a source-backed paragraph, heading, list, table, figure, slide title, or presenter note.', 'No Review mode needs to be enabled. Hover over a paragraph, heading, list, table, figure, or other meaningful document element. Use **Selection scope** or **Parent** for its enclosing subsection, section, chapter, complete slide, presenter-notes group, or document.')
s+='''

<!-- block: authoring-shared-source-effects -->
### Shared source effects

A selected rendered instance and its canonical source are different identities. The interface highlights only the selected instance, and its note marker stays on that instance. Editing a shared source target can nevertheless change every compiled occurrence of that source. Inspect those affected outputs before accepting a patch; do not fork content or imply that a source edit changes only the currently viewed page. Annotation-only content has no editable source grant, and the patch validator rejects attempts to promote contextual source IDs into targets.
''';p.write_text(s)
p=ROOT/'content/site/editorial-standard.md';s=p.read_text();s+='''

<!-- block: editorial-selection-authority -->
## Reader selections and source-edit authority

Treat reader-visible selection, captured source membership, and edit permission as separate concepts. A section or slide is selectable as one structural unit, including mapped hidden descendants; it is not a wildcard file-edit instruction. Resolve ancestor/descendant overlap, retain immutable ordered target snapshots, and reject stale or ambiguous edit scopes. Keep unmapped elements annotatable without widening their edit authority. Human acceptance must exercise full containers, nested content, source sharing and partial ranges, not only atomic-block controls or highlighted-node counts.
''';p.write_text(s)
print('Explicit scope navigation, source-aware editing instructions and acceptance decisions corrected.')
Path(__file__).unlink()
