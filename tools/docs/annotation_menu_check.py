"""Acceptance of note-only popups, global operations and local-first persistence."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
from playwright.sync_api import sync_playwright, expect

STORE='frontier-document-reviews-v1'

def validate(root: Path):
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    base=f'http://127.0.0.1:{server.server_port}'
    reports=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width in (390,1440):
                context=browser.new_context(viewport={'width':width,'height':1000})
                page=context.new_page();errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                def ready(path='guides/devops.html'):
                    page.goto(base+'/'+path);page.wait_for_function('window.FrontierReview?.interaction === "contextual-v3"')
                    page.locator('.report-section:visible p[data-review-block]').first.scroll_into_view_if_needed()
                def popup():
                    target=page.locator('.report-section:visible p[data-review-block]').first
                    target.hover();page.locator('#review-block-comment').click();return target
                def close(): page.locator('#review-drawer .review-panel-heading button').click()
                def menu(): page.locator('#review-notes-open').click();expect(page.locator('#review-global-menu')).to_be_visible()
                def menu_close(): page.get_by_role('button',name='Close annotation menu',exact=True).click()
                def notes(): return page.evaluate('FrontierReview.exportPacket().comments')
                ready();target=popup();bid=target.get_attribute('data-review-block')
                assert page.locator('#review-drawer input,#review-drawer select,#review-drawer code,#review-drawer blockquote,#review-drawer #review-export,#review-drawer #review-backend-save').count()==0
                expect(page.locator('#review-save')).to_have_text('Done')
                page.locator('#review-text').fill('Persist this note without clicking Done.')
                first=notes()[0];ident=first['id']
                assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))[0].body',STORE)==first['body']
                page.locator('#review-text').fill('Changed note, still without Done.')
                assert len(notes())==1 and notes()[0]['id']==ident
                ready();assert notes()[0]['body']=='Changed note, still without Done.'
                badge=page.locator(f'.review-comment-marker[data-block-id="{bid}"]:visible').first
                badge.click();page.get_by_role('button',name='Reply',exact=True).click()
                page.locator('#review-text').fill('Reply saved automatically.')
                page.locator('#review-text').fill('Reply updated automatically.')
                assert len(notes()[0]['replies'])==1
                ready();assert notes()[0]['replies'][0]['body']=='Reply updated automatically.'
                page.locator(f'.review-comment-marker[data-block-id="{bid}"]:visible').first.click()
                page.get_by_role('button',name='Edit',exact=True).click()
                page.locator('#review-text').fill('Edited note saved automatically.')
                close();assert notes()[0]['body']=='Edited note saved automatically.'
                menu()
                for selector in ('#review-export','#review-export-prompt','#review-copy','#review-backend-save','#review-clear-document','#review-clear-all'):
                    expect(page.locator('#review-global-menu '+selector)).to_be_visible()
                expect(page.locator('#review-backend-save')).to_be_disabled()
                with page.expect_download() as dl:page.locator('#review-export').click()
                exported=json.loads(Path(dl.value.path()).read_text())
                assert exported['comments'][0]['body']=='Edited note saved automatically.'
                assert exported['comments'][0]['targets'][0]['block_id']==bid
                # A host adapter is optional. No user means no backend write.
                page.evaluate('''async()=>{
                    window.backendCalls=0;window.backendUser=null;
                    await FrontierReview.setBackend({getSession:async()=>backendUser,
                      saveReview:async(packet)=>{backendCalls++;window.backendPacket=packet;return {saved:true,id:'test-record'};}});
                }''')
                expect(page.locator('#review-backend-save')).to_be_disabled()
                page.evaluate('''async()=>{
                    window.backendUser={user:{id:'user-a',displayName:'Connected reviewer'}};
                    await FrontierReview.setBackend({getSession:async()=>backendUser,
                      saveReview:async(packet)=>{backendCalls++;window.backendPacket=packet;return {saved:true,id:'test-record'};}});
                }''')
                expect(page.locator('#review-backend-save')).to_be_enabled()
                assert page.evaluate('backendCalls')==0
                page.locator('#review-backend-save').click()
                expect(page.locator('#review-backend-status')).to_contain_text('Backend confirmed test-record')
                assert page.evaluate('backendCalls')==1
                assert page.evaluate('backendPacket.comments[0].body')==notes()[0]['body']
                page.evaluate('''async()=>await FrontierReview.setBackend({
                  getSession:async()=>({user:{id:'user-a'}}),
                  saveReview:async()=>{throw new Error('unavailable');}})''')
                page.locator('#review-backend-save').click()
                expect(page.locator('#review-backend-status')).to_contain_text('Backend save failed')
                assert notes()[0]['id']==ident
                # Session expiry between menu open and clicking save is rechecked.
                page.evaluate('''async()=>{
                  window.backendUser={user:{id:'user-a'}};window.expiredCalls=0;
                  await FrontierReview.setBackend({getSession:async()=>backendUser,
                    saveReview:async()=>{expiredCalls++;return {saved:true,id:'wrong'};}});
                  window.backendUser=null;
                }''')
                page.locator('#review-backend-save').click()
                expect(page.locator('#review-backend-save')).to_be_disabled()
                assert page.evaluate('expiredCalls')==0
                page.evaluate('''async()=>await FrontierReview.setBackend({
                    getSession:async()=>({user:{id:'user-a'}}),saveReview:async()=>({})})''')
                page.locator('#review-backend-save').click()
                expect(page.locator('#review-backend-status')).to_contain_text('did not confirm')
                menu_close()
                ready('guides/security.html');popup();page.locator('#review-text').fill('Second document note.');close()
                assert len(notes())==2
                ready();menu()
                page.once('dialog',lambda d:d.dismiss());page.locator('#review-clear-document').click()
                assert len(notes())==2
                page.once('dialog',lambda d:d.accept());page.locator('#review-clear-document').click()
                assert len(notes())==1 and notes()[0]['document']=='guides/security.html'
                assert page.locator('.review-comment-marker').count()==0
                page.once('dialog',lambda d:d.accept());page.locator('#review-clear-all').click()
                assert notes()==[] and page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).length',STORE)==0
                menu_close();ready();assert notes()==[]
                assert not errors,errors
                reports.append({'viewport':width,'popup_note_only':'passed','global_menu_actions':'passed',
                    'automatic_note_reply_edit_persistence_without_done':'passed','stable_note_ids':'passed',
                    'explicit_authenticated_backend_adapter_success_failure_and_expiry':'passed',
                    'export_source_precision':'passed','confirmed_document_and_all_local_clear':'passed',
                    'javascript_errors':errors})
                context.close()
            context=browser.new_context()
            context.add_init_script('''const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){
                if(k==='frontier-document-reviews-v1')throw new DOMException('quota','QuotaExceededError');
                return original.call(this,k,v);
            };''')
            page=context.new_page();page.goto(base+'/guides/devops.html');page.wait_for_function('!!window.FrontierReview')
            page.locator('.report-section:visible p[data-review-block]').first.hover()
            page.locator('#review-block-comment').click();page.locator('#review-text').fill('Still available in memory.')
            expect(page.locator('#review-local-status')).to_have_attribute('data-state','failed')
            assert page.evaluate('FrontierReview.exportPacket().comments[0].body')=='Still available in memory.'
            reports.append({'localStorage_failure_visible_and_memory_export_retained':'passed'})
            context.close();browser.close()
    finally:
        server.shutdown();server.server_close();worker.join(timeout=2)
    return reports
