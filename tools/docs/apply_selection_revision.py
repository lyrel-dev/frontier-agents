"""One-time reviewed migration; removed after successful validation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'tools/docs'


def replace_once(text, before, after):
    if text.count(before)!=1:
        raise ValueError('Expected one migration anchor: '+before[:110]+'; found '+str(text.count(before)))
    return text.replace(before,after,1)


def function(text,name,code):
    start=text.index('  function '+name+'(')
    end=text.index('\n  function ',start+5)
    return text[:start]+code.rstrip()+'\n'+text[end:]

p=HERE/'source_review.py';s=p.read_text()
s=replace_once(s,'from markdown_sources import repository, ROOT, FIELD','from markdown_sources import repository, ROOT, FIELD\nfrom selection_model import compile_selections')
s=replace_once(s,"        node=soup.find(True)\n        if node:attach(node,target)","        children=[n for n in soup.contents if getattr(n,'name',None)]\n        if len(children)>1:\n            node=soup.new_tag('div',attrs={'class':'review-source-fragment'})\n            for child in list(soup.contents):node.append(child.extract())\n            soup.append(node)\n        else:node=soup.find(True)\n        if node:attach(node,target)")
s=replace_once(s,"        packet={'schema':'frontier-source-map/v1'", "        selections=compile_selections(soup,current,local,repo.revision)\n        packet={'selection_schema':'frontier-selection/v1','selections':selections,'schema':'frontier-source-map/v1'")
s=s.replace("for asset in ('search-index.js','review.js'):","for asset in ('search-index.js','selection_model.js','review.js'):")
s=s.replace("for name in ('review.js','review.css'):","for name in ('review.js','review.css','selection_model.js'):")
s=s.replace("'mapped_blocks':len(local)}","'mapped_blocks':len(local),'selection_nodes':len(selections)}")
p.write_text(s)

p=HERE/'review.js';s=p.read_text()
s=replace_once(s,"  const allBlocks = [...document.querySelectorAll('[data-review-block]')];", "  const sourceBlocks = [...document.querySelectorAll('[data-review-block]')];\n  const hierarchy = window.FrontierSelection.create(source);\n  const allBlocks = [...document.querySelectorAll('[data-review-scope]')];\n  let selectionRoots = [], scopePath = [];\n  const hasSelection = () => selected.size>0 || selectionRoots.length>0;")
s=s.replace("?.closest('[data-review-block]');","?.closest('[data-review-scope]');")
s=re.sub(r"  const labelFor = element => .*?;\n", "  const labelFor = element => hierarchy.nodes[hierarchy.key(element)]?.kind.replaceAll('-', ' ') || 'element';\n",s,count=1)
s=replace_once(s,"      if (item.selector && typeof item.selector.exact !== 'string')", "      hierarchy.validate(item);\n      if (item.selector && typeof item.selector.exact !== 'string')")
s=replace_once(s,"    if (!selected.has(active.dataset.reviewBlock)) choose(active);", "    if (!selectionRoots.some(id=>hierarchy.ancestors(hierarchy.key(active)).includes(id)) && !selected.has(active.dataset.reviewBlock)) choose(active);")
s=replace_once(s,"  gutter.append(handle,addComment); document.body.append(gutter);", """  const scopePicker = node('select',{id:'review-scope-select','aria-label':'Selection scope',title:'Select this element or an enclosing section, chapter, slide, or document'});
  scopePicker.addEventListener('change',()=>{
    const target=hierarchy.element(scopePicker.value);if(target)choose(target);
  });
  const parentButton=button('Parent',()=>{
    const id=hierarchy.key(active), parent=hierarchy.nodes[id]?.parent;
    if(parent){scopePath.push(id);choose(hierarchy.element(parent));}
  },{id:'review-select-parent','aria-label':'Select enclosing scope'});
  gutter.append(handle,addComment,parentButton,scopePicker); document.body.append(gutter);""")
s=replace_once(s,"  function associated(note,bid) { return note.scope!=='document' && note.targets.some(t=>t.block_id===bid && t.path===source.targets[bid]?.path); }", "  function associated(note,id) { return hierarchy.associated(note,id); }")
s=replace_once(s,"  function stale(note) {\n    return note.targets.some", "  function stale(note) {\n    if(hierarchy.stale(note))return true;\n    return note.targets.some")
s=function(s,'activate',"""  function activate(element) {
    if (!element || !visible(element)) return;
    clearTimeout(hideTimer); active=element; gutter.hidden=false;
    const id=hierarchy.key(element);
    gutter.dataset.blockId=element.dataset.reviewBlock||'';gutter.dataset.scopeId=id;
    gutter.setAttribute('aria-label','Actions for '+labelFor(element));
    handle.setAttribute('aria-label','Select '+labelFor(element));
    addComment.setAttribute('aria-label','Comment on '+labelFor(element));
    scopePicker.replaceChildren();
    for(const key of hierarchy.ancestors(id)){
      const scope=hierarchy.nodes[key];
      const counts=scope.target_ids.length?scope.target_ids.length+' source blocks'+(scope.protected_targets?' · '+scope.protected_targets+' protected':''):'annotation only';
      scopePicker.append(node('option',{value:key},scope.kind+' · '+scope.label.slice(0,65)+' · '+counts));
    }
    scopePicker.value=id;parentButton.disabled=!hierarchy.nodes[id]?.parent;
    scheduleLayout();
  }""")
s=s.replace('!drag && !selected.size','!drag && !hasSelection()')
s=function(s,'choose',"""  function choose(element,event={}) {
    const id=hierarchy.key(element);if(!hierarchy.nodes[id])return;
    quote=null;selectionRect=null;activate(element);
    if(event.shiftKey&&anchor){
      const range=hierarchy.range(anchor,id,visibleBlocks().map(hierarchy.key));
      selectionRoots=hierarchy.normalize(event.ctrlKey||event.metaKey?[...selectionRoots,...range]:range);
    } else if(event.ctrlKey||event.metaKey){
      selectionRoots=hierarchy.normalize(selectionRoots.includes(id)?selectionRoots.filter(x=>x!==id):[...selectionRoots,id]);anchor=id;
    } else {selectionRoots=[id];anchor=id;}
    selected.clear();hierarchy.targets(selectionRoots).forEach(bid=>selected.add(bid));
    paintSelection();
  }""")
s=function(s,'paintSelection',"""  function paintSelection() {
    allBlocks.forEach(element=>{
      element.classList.toggle('review-selected',!!element.dataset.reviewBlock&&selected.has(element.dataset.reviewBlock));
      element.classList.toggle('review-scope-selected',selectionRoots.includes(hierarchy.key(element)));
    });
    const roots=selectionRoots.map(id=>hierarchy.nodes[id]);
    const hidden=[...selected].filter(id=>!sourceBlocks.some(el=>el.dataset.reviewBlock===id&&visible(el))).length;
    const protectedCount=[...selected].filter(id=>source.targets[id]?.protected).length;
    selectionCount.textContent=quote?'Selected text':roots.length===1
      ? roots[0].kind+' · '+roots[0].label.slice(0,70)+' · '+selected.size+' source blocks'
      : roots.length+' selected elements · '+selected.size+' source blocks';
    if(hidden)selectionCount.textContent+=' · '+hidden+' not currently displayed';
    if(protectedCount)selectionCount.textContent+=' · '+protectedCount+' protected';
    if(hasSelection()&&!selected.size)selectionCount.textContent+=' · annotation only';
    if(roots.some(r=>r.unmapped_parts))selectionCount.textContent+=' · unmapped content is not editable';
    selectionTools.hidden=!hasSelection() || !editor.hidden && !panel.hidden;
    scheduleLayout();
  }""")
s=function(s,'clearSelection',"""  function clearSelection() {
    selected.clear();selectionRoots=[];scopePath=[];anchor=null;quote=null;selectionRect=null;paintSelection();
  }""")
s=function(s,'compose',"""  function compose(element) {
    closePanel();
    if(!hasSelection()&&element)choose(element);
    if(!hasSelection())return;
    const targets=copy([...selected].map(bid=>source.targets[bid]).filter(Boolean));
    const selection=selectionRoots.length?hierarchy.snapshot(selectionRoots):null;
    pending={scope:quote?'text':selectionRoots.some(id=>['document','chapter','section','subsection','slide','presenter-notes','group'].includes(hierarchy.nodes[id].kind))?'structure':'blocks',targets,selector:quote?copy(quote):null};
    if(selection)pending.selection=selection;
    const target=selectionRoots.length?hierarchy.element(selectionRoots[0]):element;
    threadBlock=hierarchy.key(target);editing=null;replying=null;replyDraftId=null;
    showPanel(target);editor.hidden=false;kind.value='comment';author.value=backendSession?.user?.displayName||'';text.value='';
    renderThreads();text.focus({preventScroll:true});scheduleLayout();
  }""")
s=function(s,'composeDocument',"""  function composeDocument() {
    closePanel();const root=Object.values(hierarchy.nodes).find(n=>n.kind==='document');
    if(!root)return;
    const selection=hierarchy.snapshot([root.id]);
    pending={scope:'document',targets:copy(selection.target_ids.map(id=>source.targets[id])),selector:null,selection};
    threadBlock=root.id;editing=null;replying=null;replyDraftId=null;
    showPanel(null);editor.hidden=false;kind.value='note';text.value='';renderThreads();text.focus({preventScroll:true});
  }""")
s=s.replace('threadBlock=element.dataset.reviewBlock;activate(element);','threadBlock=hierarchy.key(element);activate(element);')
s=replace_once(s,"      const target=allBlocks.find(block=>item.targets.some(t=>t.block_id===block.dataset.reviewBlock&&t.path===source.targets[t.block_id]?.path));", "      const target=hierarchy.locate(item);")
s=function(s,'locate',"""  function locate(item) {
    const element=hierarchy.locate(item);
    if(!element){status.textContent='The recorded selection is not available here. Open '+item.document+' or review its stale source anchor.';return;}
    reveal(element);element.scrollIntoView({block:'center'});active=element;panelAnchor=element;clearSelection();
    selectionRoots=item.selection?.roots.map(root=>root.id).filter(id=>hierarchy.nodes[id])||[];
    item.targets.forEach(t=>{if(source.targets[t.block_id])selected.add(t.block_id);});paintSelection();
  }""")
s=s.replace('associated(n,block.dataset.reviewBlock)','associated(n,hierarchy.key(block))')
s=s.replace("'data-block-id':block.dataset.reviewBlock,", "'data-block-id':block.dataset.reviewBlock||'', 'data-scope-id':hierarchy.key(block),")
s=s.replace("const elements=visibleBlocks().filter(b=>selected.has(b.dataset.reviewBlock));", "const elements=visibleBlocks().filter(b=>selectionRoots.includes(hierarchy.key(b))||selected.has(b.dataset.reviewBlock));")
s=s.replace("place(gutter,r.left>=70?r.left-66:r.left,r.left>=70?Math.max(8,r.top):Math.max(8,r.top-gutter.offsetHeight-5));", "place(gutter,r.left>=gutter.offsetWidth+10?r.left-gutter.offsetWidth-6:r.left,Math.max(8,r.top-gutter.offsetHeight-5));")
s=s.replace('anchor=drag.block.dataset.reviewBlock;','anchor=hierarchy.key(drag.block);')
s=s.replace("const blocks=visibleBlocks().filter(b=>{try{return range.intersectsNode(b);}catch(_){return false;}});", "const blocks=sourceBlocks.filter(visible).filter(b=>{try{return range.intersectsNode(b);}catch(_){return false;}});")
s=s.replace("    selected.clear();leaves.forEach(b=>selected.add(b.dataset.reviewBlock));", "    selectionRoots=[];selected.clear();leaves.forEach(b=>selected.add(b.dataset.reviewBlock));\n    if(!leaves.length){choose(first);return;}")
s=s.replace('if(!selected.size && active)choose(active);','if(!hasSelection() && active)choose(active);')
s=s.replace("interaction:'contextual-v3'", "interaction:'contextual-v4'")
old="    if(!['ArrowDown','ArrowUp'].includes(event.key)||!active)return;event.preventDefault();"
new="""    if(event.altKey&&event.key==='ArrowUp'&&active){event.preventDefault();parentButton.click();return;}
    if(event.altKey&&event.key==='ArrowDown'&&scopePath.length){event.preventDefault();const child=hierarchy.element(scopePath.pop());if(child)choose(child);return;}
    if(!['ArrowDown','ArrowUp'].includes(event.key)||!active)return;event.preventDefault();"""
s=replace_once(s,old,new)
p.write_text(s)

p=HERE/'review_patch.py';s=p.read_text()
s=replace_once(s,'    repo=Repository()','    repo=Repository()\n    from selection_model import validate_structure')
s=replace_once(s,"        if comment is None or comment.get('status')!='open':\n            raise ReviewError('Edit must reference an open review comment')", "        if comment is None or comment.get('status')!='open':\n            raise ReviewError('Edit must reference an open review comment')\n        validate_structure(comment,repo,ROOT)")
p.write_text(s)

p=HERE/'review.css';s=p.read_text()+'''\n/* Scope controls stay outside note popups and do not mutate content. */
#review-block-controls{max-width:calc(100vw - 16px);flex-wrap:wrap;align-items:center}
#review-block-controls #review-select-parent{width:auto;min-width:58px!important;font-size:12px;padding:3px 7px!important}
#review-scope-select{max-width:min(310px,calc(100vw - 160px));font:12px/1.4 system-ui;background:#fff;color:#23435e;border:1px solid #ccd7e1;border-radius:4px;padding:4px;min-height:30px}
#review-selection-tools{max-width:calc(100vw - 16px);flex-wrap:wrap}
#review-selection-count{white-space:normal;max-width:min(580px,calc(100vw - 160px));overflow-wrap:anywhere}
.review-scope-selected{outline:2px solid #315f9b!important;outline-offset:5px;background-color:#e8f0fa24}
.review-subsection{margin:0;padding:0}
@media print{.review-scope-selected{outline:none!important;background:transparent!important}}
''';p.write_text(s)
for filename in ('contextual_check.py','annotation_menu_check.py','review_check.py'):
    p=HERE/filename;s=p.read_text().replace('contextual-v3','contextual-v4');p.write_text(s)
p=HERE/'review_check.py';s=p.read_text()
s=replace_once(s,"        result['annotation_menu']=validate_menu(ROOT)", "        result['annotation_menu']=validate_menu(ROOT)\n        from hierarchy_check import validate as validate_hierarchy\n        result['hierarchical_selection']=validate_hierarchy(ROOT)")
p.write_text(s)
print('Migrated semantic selection, exact membership snapshots and independent edit guards.')
Path(__file__).unlink()
