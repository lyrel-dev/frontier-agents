"""Complete the one-time menu revision; no changes to frozen content."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'tools/docs/annotation_menu_check.py';s=p.read_text()
old="                    page.goto(base+'/'+path);page.wait_for_function('window.FrontierReview?.interaction === \"contextual-v3\"')"
new=old+"\n                    page.locator('.report-section:visible p[data-review-block]').first.scroll_into_view_if_needed()"
assert old in s
p.write_text(s.replace(old,new,1))
p=ROOT/'tools/docs/review.js';s=p.read_text()
s=s.replace("  globalMenu.addEventListener('close',()=>document.querySelector('#review-notes-open').focus({preventScroll:true}));", "  globalMenu.addEventListener('close',()=>{if(panel.hidden)document.querySelector('#review-notes-open').focus({preventScroll:true});});")
p.write_text(s)
p=ROOT/'WORKSTREAM.md';s=p.read_text()
s=s.replace('Click its comment control to open an element-anchored composer with the selected source context.', 'Click its comment control to open an element-anchored note editor without source-path or excerpt metadata.')
s=s.replace('The document header exposes optional Search all, Document note, and Notes controls. Document-wide navigation and export are secondary to the element interaction. Export/import is under Export, import and storage in the notes panel.', 'The document header exposes Search all and the global Annotations menu. That menu contains document notes, collection browsing, export/import, explicit connected-user backend saving, and confirmed local clearing. The note popup contains no global actions.')
s=s.replace('The current QA record specifies what was tested. Human acceptance is still pending.', 'The current QA record specifies what was tested. M09 further separates global operations from note popups and adds automatic local persistence. Human acceptance is still pending.')
p.write_text(s)
Path(__file__).unlink()
