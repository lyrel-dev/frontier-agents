"""One-time source migration. Remove after committing the compiled revision."""
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[2]
path = ROOT/'tools/docs/review.js'
s = path.read_text()
def replace(old, new, count=1):
    global s
    assert s.count(old) == count, ('unexpected source', old[:90], s.count(old))
    s = s.replace(old, new)
def section(start, end, replacement):
    global s
    a = s.index(start); b = s.index(end, a)
    s = s[:a]+replacement+s[b:]
replace('/* Contextual source annotations. Read-only content; no network or LLM calls. */',
        '/* Contextual notes. Automatic local persistence; explicit authenticated backend adapter only. */')
replace('  let pending = null, editing = null, replying = null, threadBlock = null;',
        '  let pending = null, editing = null, replying = null, threadBlock = null;\n  let replyDraftId = null, backend = null, backendSession = null, backendBusy = false;\n  let backendGeneration = 0;')
replace("      if (event.key === 'Escape') { event.preventDefault(); closePanel(); clearSelection(); }",
        "      if (event.key === 'Escape') { event.preventDefault(); closePanel(); clearSelection(); if (globalMenu.open) globalMenu.close(); }")
replace("    try { localStorage.setItem(STORE,JSON.stringify(notes)); }\n    catch (_) { storageOK = false; }\n    refreshAnchors();",
        "    try { localStorage.setItem(STORE,JSON.stringify(notes)); storageOK = true; }\n    catch (_) { storageOK = false; }\n    refreshAnchors(); updateLocalStatus();")
section('  // Document-wide functions stay', '  // Portalled controls', r'''  // Global actions are separate from the note popup; no annotation mode is required.
  const documentTools = surface('nav',{id:'review-document-tools','aria-label':'Document search and annotations'});
  const localStatus = node('span',{id:'review-local-status',role:'status','aria-live':'polite'},'Automatic local save');
  documentTools.append(button('Search all',()=>{ searchDialog.showModal(); searchInput.focus(); },{id:'review-search-open'}),
    button('Annotations',()=>openCollection(),{id:'review-notes-open','aria-haspopup':'dialog'}), localStatus);
  (document.querySelector('main') || document.body).prepend(documentTools);

''')
section("  const panel = surface('aside'", '  function associated(', r'''  // The anchored popup contains only the note/thread and its editing actions.
  const panel = surface('aside',{id:'review-drawer',role:'dialog','aria-modal':'false','aria-label':'Note',hidden:true});
  const panelHeading = node('div',{class:'review-panel-heading'});
  const panelTitle = node('h2',{},'Note');
  panelHeading.append(panelTitle,button('Close',()=>closePanel(),{'aria-label':'Close note'}));
  const editor = node('div',{id:'review-composer',hidden:true});
  // Author/kind remain annotation metadata, not form controls in the note popup.
  const author = {value:''}, kind = {value:'comment'};
  const text = node('textarea',{id:'review-text',rows:4,placeholder:'Write a note…','aria-label':'Note text'});
  const save = button('Done',()=>commit(),{id:'review-save',title:'Close the editor. Changes are saved locally as you type.'});
  editor.append(text,save);
  const threads = node('div',{id:'review-threads'});
  panel.append(panelHeading,editor,threads); document.body.append(panel);

  // One document-level menu owns collection management and all I/O operations.
  const globalMenu = surface('dialog',{id:'review-global-menu','aria-label':'Annotation menu'});
  const globalHeading = node('div',{class:'review-panel-heading'});
  globalHeading.append(node('h2',{},'Annotations'),button('Close',()=>globalMenu.close(),{'aria-label':'Close annotation menu'}));
  const status = node('p',{id:'review-status',role:'status'});
  const storageStatus = node('p',{id:'review-storage-status',class:'review-help',role:'status'});
  const globalActions = node('div',{class:'review-global-actions'});
  globalActions.append(button('Add document note',()=>{globalMenu.close();composeDocument();},{id:'review-document-note'}));
  const io = node('section',{class:'review-global-actions','aria-label':'Export and import'});
  io.append(button('Export JSON',()=>{autosave();download('frontier-review.json',JSON.stringify(packet(),null,2),'application/json');},{id:'review-export'}),
    button('Export LLM request',()=>{autosave();download('frontier-review-request.md',prompt(),'text/markdown');},{id:'review-export-prompt'}),
    button('Copy LLM request',async()=>{
      autosave();
      try { await navigator.clipboard.writeText(prompt());status.textContent='Request copied. Nothing was sent to an LLM.'; }
      catch (_) { status.textContent='Clipboard unavailable; use Export LLM request.'; }
    },{id:'review-copy'}));
  const importLabel = node('label',{for:'review-import',class:'review-help'},'Import annotations');
  const importInput = node('input',{type:'file',id:'review-import',accept:'.json,application/json','aria-label':'Import review JSON'});
  importInput.addEventListener('change',async()=>{
    const file = importInput.files[0]; if (!file) return;
    try {
      if (file.size>20000000) throw new Error('Review file exceeds 20 MB');
      const incoming=JSON.parse(await file.text());validatePacket(incoming);
      const merged=new Map(notes.map(note=>[note.id,note]));
      for (const note of incoming.comments) if (!merged.has(note.id) || note.updated_at>merged.get(note.id).updated_at) merged.set(note.id,note);
      const combined=[...merged.values()];validatePacket({schema:SCHEMA,comments:combined});notes=combined;
      saveStore();filter.value='all';renderCollection();status.textContent=`Imported ${incoming.comments.length} annotations. Stale source references are not reassigned.`;
    } catch (error) { status.textContent='Import rejected: '+error.message; }
    importInput.value='';
  });
  const backendStatus = node('p',{id:'review-backend-status',class:'review-help',role:'status'},'No backend is connected. Notes are saved in this browser.');
  const backendButton = button('Save to backend',()=>saveBackend(),{id:'review-backend-save',disabled:true});
  const backendSection = node('section',{class:'review-global-section','aria-label':'Backend storage'});
  backendSection.append(backendButton,backendStatus);
  const clearActions = node('section',{class:'review-global-actions','aria-label':'Clear local annotations'});
  clearActions.append(button('Clear this document',()=>clearNotes('document'),{id:'review-clear-document'}),
    button('Clear all local annotations',()=>clearNotes('all'),{id:'review-clear-all'}));
  const filter = node('select',{id:'review-note-filter','aria-label':'Filter annotations'});
  for(const [value,label] of [['page','This document'],['all','All stored documents'],['open','Open notes']])filter.append(node('option',{value},label));
  filter.addEventListener('change',()=>renderCollection());
  const collection = node('div',{id:'review-collection'});
  globalMenu.append(globalHeading,storageStatus,status,globalActions,io,importLabel,importInput,backendSection,clearActions,
    node('p',{class:'review-help'},'Clear removes local notes, comments and replies only; it does not delete a previously saved backend copy.'),filter,collection);
  document.body.append(globalMenu);
  globalMenu.addEventListener('close',()=>document.querySelector('#review-notes-open').focus({preventScroll:true}));

  function updateLocalStatus() {
    const message=storageOK?'Saved locally automatically':'Local save unavailable — export your notes';
    localStatus.textContent=message;localStatus.dataset.state=storageOK?'saved':'failed';
    storageStatus.textContent=storageOK
      ? 'Notes and replies are saved in this browser as you type. Backend saving is a separate, explicit action.'
      : 'Browser storage failed or is unavailable. Your current notes remain in memory; export them before closing this page.';
  }
  function clearNotes(scope) {
    const question=scope==='all'?'Clear every local note, comment and reply on this browser origin?':'Clear this document’s local notes, comments and replies?';
    if(!confirm(question+' Previously saved backend copies will not be deleted.'))return;
    closePanel();pending=null;editing=null;replying=null;replyDraftId=null;text.value='';
    notes=scope==='all'?[]:notes.filter(note=>note.document!==source.document);
    clearSelection();saveStore();renderCollection();
    status.textContent=storageOK?'Local annotations cleared. Backend copies were not changed.':'Cleared in memory, but local storage could not be updated.';
  }
  function renderCollection() {
    collection.replaceChildren();
    const values=notes.filter(note=>filter.value==='all'||filter.value==='open'&&note.status==='open'||filter.value==='page'&&note.document===source.document);
    if(!values.length)collection.append(node('p',{},'No annotations in this view.'));
    for(const item of values){
      const card=node('article',{class:'review-collection-entry','data-comment-id':item.id});
      card.append(node('h3',{},item.document_title||item.document),node('p',{class:'review-comment-body'},item.body||'Empty note'));
      if(stale(item))card.append(node('p',{class:'review-warning'},'Source changed. Review this anchor before editing the source.'));
      const target=allBlocks.find(block=>item.targets.some(t=>t.block_id===block.dataset.reviewBlock&&t.path===source.targets[t.block_id]?.path));
      if(target || item.document===source.document){
        card.append(button('Open note',()=>{
          globalMenu.close();
          if(target&&item.scope!=='document'){reveal(target);target.scrollIntoView({block:'center'});openThreads(target);}
          else {threadBlock=null;showPanel(null);editor.hidden=true;renderThreads();}
        }));
      } else if(/^[A-Za-z0-9_./-]+\.html$/.test(item.document)&&!item.document.split('/').includes('..')){
        const prefix='../'.repeat(source.document.split('/').length-1);
        card.append(node('a',{href:prefix+item.document},'Open document'));
      }
      collection.append(card);
    }
  }
  async function setBackend(adapter) {
    if(adapter!==null&&(!adapter||typeof adapter.getSession!=='function'||typeof adapter.saveReview!=='function'))throw new TypeError('Backend requires getSession() and saveReview(packet, options)');
    backend=adapter;backendSession=null;backendGeneration++;
    return refreshBackend();
  }
  function requestWithTimeout(operation) {
    const controller=new AbortController();let timer;
    const timeout=new Promise((_,reject)=>{timer=setTimeout(()=>{controller.abort();reject(new Error('Backend request timed out'));},15000);});
    return Promise.race([Promise.resolve().then(()=>operation(controller.signal)),timeout]).finally(()=>clearTimeout(timer));
  }
  async function refreshBackend() {
    const adapter=backend, generation=backendGeneration;
    backendButton.disabled=true;
    if(!adapter){backendSession=null;backendStatus.textContent='No backend is connected. Notes are saved in this browser.';return;}
    if(backendBusy)return;
    backendStatus.textContent='Checking the connected user…';
    try {
      const session=await requestWithTimeout(signal=>adapter.getSession({signal}));
      if(adapter!==backend||generation!==backendGeneration)return;
      backendSession=session&&typeof session.user?.id==='string'&&session.user.id.trim()?session:null;
      backendButton.disabled=!backendSession;
      backendStatus.textContent=backendSession?'Connected as '+(session.user.displayName||session.user.id)+'. Save explicitly to copy these annotations to the backend.':'Sign in through the host application to save to the backend. Local saving remains active.';
    } catch(error) {
      if(adapter!==backend||generation!==backendGeneration)return;
      backendSession=null;backendStatus.textContent='Backend session unavailable: '+error.message+'. Local notes are retained.';
    }
  }
  async function saveBackend() {
    if(backendBusy)return;
    autosave();await refreshBackend();
    if(!backendSession||!backend)return;
    const adapter=backend, generation=backendGeneration, userId=backendSession.user.id, snapshot=packet();
    backendBusy=true;backendButton.disabled=true;backendStatus.textContent='Saving a copy to the backend…';
    try {
      const receipt=await requestWithTimeout(signal=>adapter.saveReview(copy(snapshot),{signal}));
      if(adapter!==backend||generation!==backendGeneration)throw new Error('Backend connection changed during saving');
      const session=await requestWithTimeout(signal=>adapter.getSession({signal}));
      if(session?.user?.id!==userId)throw new Error('Connected user changed; verify the backend result');
      if(receipt?.saved!==true||typeof receipt.id!=='string'||!receipt.id.trim())throw new Error('Backend did not confirm a saved record');
      const newer=JSON.stringify(snapshot.comments)!==JSON.stringify(notes);
      backendStatus.textContent='Backend confirmed '+receipt.id+'. '+(newer?'Newer local changes have not been sent.':'Local annotations are also retained.');
    } catch(error) {
      backendStatus.textContent='Backend save failed: '+error.message+'. Local annotations are retained.';
    } finally {backendBusy=false;backendButton.disabled=!backendSession||adapter!==backend;}
  }

''')
section('  function contextQuote(', '  function reveal(', r'''  function showPanel(element) {
    returnFocus=document.activeElement;panelAnchor=element||null;panel.hidden=false;
    panel.dataset.context=element?'element':'document';panelTitle.textContent='Note';
    gutter.hidden=true;selectionTools.hidden=true;scheduleLayout();
  }
  function compose(element) {
    closePanel();
    if(!selected.size&&element)choose(element);
    if(!selected.size)return;
    const targets=copy([...selected].map(bid=>source.targets[bid]).filter(Boolean));
    pending={scope:quote?'text':'blocks',targets,selector:quote?copy(quote):null};
    threadBlock=targets[0]?.block_id;editing=null;replying=null;replyDraftId=null;
    showPanel(element);editor.hidden=false;kind.value='comment';author.value=backendSession?.user?.displayName||'';text.value='';
    renderThreads();text.focus({preventScroll:true});scheduleLayout();
  }
  function composeDocument() {
    closePanel();pending={scope:'document',targets:copy(Object.values(source.targets)),selector:null};
    threadBlock=null;editing=null;replying=null;replyDraftId=null;
    showPanel(null);editor.hidden=false;kind.value='note';text.value='';renderThreads();text.focus({preventScroll:true});
  }
  function openCollection() {
    closePanel();clearSelection();filter.value='page';renderCollection();updateLocalStatus();status.textContent='';
    if(!globalMenu.open)globalMenu.showModal();refreshBackend();
  }
  function openThreads(element) {
    closePanel();pending=null;editing=null;replying=null;replyDraftId=null;threadBlock=element.dataset.reviewBlock;activate(element);
    showPanel(element);editor.hidden=true;renderThreads();panelHeading.querySelector('button').focus({preventScroll:true});
  }
  function closePanel() {
    autosave();panel.hidden=true;pending=null;editing=null;replying=null;replyDraftId=null;editor.hidden=true;panelAnchor=null;
    if(returnFocus?.isConnected&&visible(returnFocus))returnFocus.focus({preventScroll:true});
    paintSelection();
  }
  function autosave() {
    if(editor.hidden||panel.hidden||!pending&&!editing&&!replying)return;
    const body=text.value;
    if(body.length>100000){localStatus.textContent='Note exceeds 100,000 characters; newest input is not saved';localStatus.dataset.state='failed';return;}
    const timestamp=now();let item,changed=false;
    if(replying){
      item=notes.find(n=>n.id===replying);if(!item)return;
      item.replies||=[];let reply=item.replies.find(r=>r.id===replyDraftId);
      if(!reply){if(!body.trim())return;reply={id:uid(),body,author:author.value.trim(),created_at:timestamp};replyDraftId=reply.id;item.replies.push(reply);changed=true;}
      else if(reply.body!==body){reply.body=body;changed=true;}
      if(changed)item.updated_at=timestamp;
    } else if(editing){
      item=notes.find(n=>n.id===editing);if(!item)return;
      if(item.body!==body){item.body=body;item.updated_at=timestamp;changed=true;}
    } else {
      if(!body.trim()||!pending)return;
      if(notes.length>=2000){localStatus.textContent='Local note limit reached; export and clear older annotations';localStatus.dataset.state='failed';return;}
      item={id:uid(),kind:kind.value,body,author:author.value.trim(),status:'open',created_at:timestamp,updated_at:timestamp,
        document:source.document,document_title:source.title,content_revision:nowSource,...copy(pending),replies:[]};
      notes.push(item);editing=item.id;pending=null;changed=true;
    }
    if(changed)saveStore();
  }
  text.addEventListener('input',autosave);
  window.addEventListener('pagehide',autosave);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)autosave();});
  function commit() {
    autosave();pending=null;editing=null;replying=null;replyDraftId=null;editor.hidden=true;text.value='';
    clearSelection();renderThreads();
  }
  function renderThreads() {
    threads.replaceChildren();
    const values=notes.filter(note=>threadBlock?associated(note,threadBlock):note.scope==='document'&&note.document===source.document);
    for(const item of values){
      if(editing===item.id&&!editor.hidden)continue;
      const card=node('section',{class:'review-thread','data-comment-id':item.id});
      if(stale(item))card.append(node('p',{class:'review-warning'},'The source changed. Review the anchor before editing source text.'));
      card.append(node('p',{class:'review-comment-body'},item.body||'Empty note'));
      const actions=node('div',{class:'review-actions'});
      actions.append(button('Reply',()=>{
        autosave();replying=item.id;editing=null;pending=null;replyDraftId=null;editor.hidden=false;text.value='';text.focus();
      }),button('Edit',()=>{
        autosave();editing=item.id;replying=null;pending=null;replyDraftId=null;editor.hidden=false;text.value=item.body;author.value=item.author||'';renderThreads();text.focus();
      }),button(item.status==='resolved'?'Reopen':'Resolve',()=>{
        autosave();item.status=item.status==='resolved'?'open':'resolved';item.updated_at=now();saveStore();renderThreads();
      }),button('Delete',()=>{
        if(confirm('Delete this local note and its replies?')){
          if(editing===item.id||replying===item.id){editing=null;replying=null;pending=null;replyDraftId=null;editor.hidden=true;text.value='';}
          notes=notes.filter(n=>n.id!==item.id);saveStore();renderThreads();
        }
      }));
      for(const reply of item.replies||[])card.append(node('p',{class:'review-reply'},reply.body));
      card.append(actions);threads.append(card);
    }
    scheduleLayout();
  }
''')
replace("    document.querySelector('#review-notes-open').textContent='Notes'+(notes.length?' ('+notes.length+')':'');scheduleLayout();",
        "    document.querySelector('#review-notes-open').textContent='Annotations'+(notes.length?' ('+notes.length+')':'');scheduleLayout();")
replace("  window.addEventListener('storage',event=>{if(event.key===STORE){notes=readStore();refreshAnchors();if(!panel.hidden)renderThreads();}});",r'''  window.addEventListener('storage',event=>{
    if(event.key===STORE){
      notes=readStore();
      if(editing&&!notes.some(n=>n.id===editing)||replying&&!notes.some(n=>n.id===replying)){
        pending=null;editing=null;replying=null;replyDraftId=null;text.value='';editor.hidden=true;panel.hidden=true;
      }
      refreshAnchors();updateLocalStatus();if(!panel.hidden)renderThreads();if(globalMenu.open)renderCollection();
    }
  });''')
replace("  window.FrontierReview={exportPacket:packet,exportPrompt:prompt,validatePacket,sourceRevision:source.content_revision,interaction:'contextual-v2'};",r'''  window.FrontierReview={exportPacket:packet,exportPrompt:prompt,validatePacket,setBackend,sourceRevision:source.content_revision,interaction:'contextual-v3'};
  if(window.FrontierReviewBackend){
    setBackend(window.FrontierReviewBackend).catch(error=>{backendStatus.textContent='Invalid backend adapter: '+error.message;});
  }
  updateLocalStatus();''')
path.write_text(s)

p=ROOT/'tools/docs/review.css'
css=p.read_text()+r'''
/* Global annotation actions are not part of the anchored note popup. */
#review-global-menu{position:fixed;inset:7vh auto auto 50%;transform:translateX(-50%);margin:0;width:min(720px,calc(100vw - 24px));max-height:84vh;overflow:auto;padding:22px;border:1px solid #adc0d0;border-radius:10px;background:#fff;overscroll-behavior:contain}
#review-global-menu::backdrop{background:#19304466}
#review-global-menu h2{font:600 20px/1.3 system-ui;margin:0}
#review-global-menu h3{font:600 15px/1.4 system-ui;margin:0 0 6px}
#review-global-menu p{margin:8px 0;overflow-wrap:anywhere}
#review-global-menu .review-help{font-size:12px;color:#526979}
#review-global-menu input,#review-global-menu select{font:inherit;box-sizing:border-box;width:100%;padding:8px;margin:8px 0;border:1px solid #a9bac9;border-radius:4px}
.review-global-actions{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.review-global-section{border-top:1px solid #d4dee6;padding-top:12px;margin-top:12px}
.review-collection-entry{border-top:1px solid #d4dee6;padding:12px 0}
#review-global-menu .review-warning{font-size:12px;border-left:3px solid #b37035;padding:8px;background:#fff2e4}
#review-local-status{align-self:center;font-size:11px;color:#526979}
#review-local-status[data-state=failed]{color:#a04924;font-weight:600}
#review-drawer{width:min(340px,calc(100vw - 24px));padding:12px}
#review-drawer h2{font-size:16px;margin:0}
#review-drawer .review-thread:first-child{border:0;margin-top:4px;padding-top:4px}
#review-drawer textarea{border:0;background:#fafbfd;min-height:110px;margin:10px 0;resize:vertical}
#review-drawer #review-save{font-size:12px;padding:4px 9px}
[data-review-ui] button:disabled{opacity:.55;cursor:not-allowed}
@media(max-width:600px){#review-global-menu{padding:15px}#review-local-status{flex-basis:100%}#review-drawer{max-height:68vh}}
'''
p.write_text(css)
p=ROOT/'tools/docs/contextual_check.py';t=p.read_text().replace('contextual-v2','contextual-v3')
t=t.replace("                expect(page.locator('#review-note-filter')).to_have_value('anchor')", "                assert page.locator('#review-drawer select,#review-drawer .review-io,#review-drawer code,#review-context-quote').count()==0")
t=t.replace("                page.locator('#review-document-note').click();", "                page.locator('#review-notes-open').click();page.locator('#review-document-note').click();")
t=t.replace("page.locator('#review-notes-open').click();page.locator('.review-io summary').click()", "page.locator('#review-notes-open').click()")
t=t.replace("expect(page.locator('#review-drawer')).to_be_hidden();page.emulate_media", "expect(page.locator('#review-drawer')).to_be_hidden();expect(page.locator('#review-global-menu')).to_be_hidden();page.emulate_media")
p.write_text(t)
p=ROOT/'tools/docs/review_check.py';t=p.read_text().replace("'interaction':'contextual-v2'", "'interaction':'contextual-v3'")
t=t.replace("        result['browser']=browser_checks(ROOT)", "        result['browser']=browser_checks(ROOT)\n        from annotation_menu_check import validate as validate_menu\n        result['annotation_menu']=validate_menu(ROOT)")
p.write_text(t)

p=ROOT/'content/site/authoring.md';a=p.read_text()
a=a.replace('Existing annotations have persistent margin markers. Click a marker to open only the threads attached to that element, with the source excerpt and path shown. Reply, edit, resolve, or reopen the thread in that context. Resolved threads remain accessible; stale source hashes are flagged rather than silently attached to different text. The **Notes** control in the document header opens the optional document-wide collection. **Document note** records an observation about the whole document. Export/import controls are in the notes panel under **Export, import and storage**.', 'Existing annotations have persistent margin markers. Click a marker to open only the note and its replies. The popup does not show source excerpts, paths, filters, or export controls. Reply, edit, resolve, or reopen the note in context. Note text and replies persist locally as you type; Done closes the editor rather than saving it. The **Annotations** menu in the document header holds the document-wide collection, document notes, export/import, connected-user backend saving, and confirmed clearing. Resolved notes remain accessible, and stale source hashes remain flagged.')
a += '''\n\n<!-- block: authoring-local-first-menu -->
## Note popup, global menu, and automatic local persistence

The anchored popup contains only its note/thread and note-level actions. It has no source excerpt, source-path display, author/type form, document filter, export tools, or backend controls. Changes to note text and replies are written to localStorage on input; **Done** only closes the editor. Closing the popup or reloading does not require a Save action. A storage failure is reported in the document header; export the in-memory notes before closing the page.

The **Annotations** menu owns document-level notes, collection filtering, JSON/LLM export, import, **Save to backend**, and confirmed clearing for this document or all local annotations. Clearing removes local comments, notes, and replies; it does not delete a previously saved backend copy. The existing storage keys, export schemas, source hashes, block IDs and frozen-record patch protections are retained.

<!-- block: authoring-backend-adapter -->
## Connected-user backend adapter

The static documentation does not include a deployed authentication or storage service. A host application may register `FrontierReview.setBackend(adapter)` after the reader loads, or provide `window.FrontierReviewBackend` before it loads. The adapter implements `getSession({signal})`, returning `null` or `{user: {id, displayName}}`, and `saveReview(packet, {signal})`, returning `{saved: true, id}` only after successful server persistence. The reader disables backend saving without both an adapter and a connected user. Explicit saving sends a snapshot; typing saves locally and does not trigger remote writes. Failures retain local annotations and never display a successful remote-save message.

Authentication, server-side authorization, CSRF protection where applicable, TLS, ownership checks, request limits and retention belong to the host/backend implementation. The server must derive the user from its authenticated session, not trust user IDs supplied in review JSON. Do not store access tokens in annotation localStorage or embed credentials in generated HTML. Registering an adapter does not authenticate a user by itself. An actual production backend is not provisioned or verified by the documentation build.
'''
p.write_text(a)
p=ROOT/'content/site/readme.md';a=p.read_text()
a += '''\n\n<!-- block: readme-annotation-menu -->
## Annotation controls

Hover over source-backed content to add a note. Its popup contains the note and thread actions only. Text and replies save locally as you type. The document-level **Annotations** menu contains export/import, optional connected-user backend saving, and confirmed clearing of local annotations. Backend saving requires an authenticated host adapter; the static checkout does not supply a backend service. See AUTHORING.md for the adapter contract and persistence limits.
'''
p.write_text(a)
p=ROOT/'WORKSTREAM.md';raw=p.read_text();front,body=raw[4:].split('\n---\n',1);meta=yaml.safe_load(front)
meta['document_version']=3
meta['repository']['implementation_branch']='docs/annotation-menu-autosave'
meta['repository']['implementation_baseline']='c9db501798470a2dbfc3961eafaef9fd431f52c0'
meta['contextual_annotation_contract'].update({'version':'contextual-v3','popup':'Note/thread and note-level editing actions only','global_controls':'Annotations menu: export/import, connected-user backend save, confirmed clear and collection browsing','local_persistence':'Automatic on note/reply input and every annotation mutation','backend_save':'Explicit host adapter call for an authenticated connected user; no deployed backend included','user_acceptance':'pending'})
meta['validation_snapshot']['status']='This revision requires the current CI run; prior run links are historical.'
meta['milestones'].append({'id':'M09','status':'implementation_pending_validation','name':'Minimal note popup, global annotation menu and automatic local persistence'})
meta['next_action']='Validate contextual-v3 behavior and backend adapter boundaries, then complete N01/N03 human acceptance.'
body += '''\n\n## Contextual-v3 update: local-first notes and global operations

The user clarified that the anchored popup must show only the note. Export, save-to-backend, and clearing controls belong in a global menu, and all annotations must persist locally automatically. The current revision removes global operations, source excerpts/paths, and author/type forms from the note popup. Note text, edits, and replies save on input; Done is not a save prerequisite. Existing note IDs, storage keys, source mappings and patch safeguards remain unchanged.

The document-level Annotations menu provides collection browsing, export/import, confirmed local clearing, and explicit backend save. Backend save requires an authenticated host adapter; absent a connected user or adapter it is disabled. The compiler does not deploy a backend. No remote write occurs merely because a user types. Server authorization and data ownership must be enforced by the host implementation, independently of the exported source metadata.

The additional acceptance tests cover reload without Done, reply/edit persistence, popup/global-control separation, local clearing/cancellation, export after input, authenticated adapter success/failure/session changes, and storage failures. Human acceptance and live backend validation remain distinct from mocked adapter regression tests. The approved model, use cases, and independent application remain frozen/out of scope.
'''
p.write_text('---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n'+body)
Path(__file__).unlink()
print('Applied note-only popup, global menu and automatic-local-save revision.')
