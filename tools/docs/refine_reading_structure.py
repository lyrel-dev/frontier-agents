"""One-time refinement of reader navigation tests; removed after applying."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=HERE/'reading_check.py';t=p.read_text()
t=t.replace("                        page.locator('#next-chapter').click()\n                        assert", "                        page.locator('#next-chapter').click()\n                        page.wait_for_function('(id)=>document.querySelector(\".chapter:not([hidden])\").id===id',arg='chapter-'+CHAPTERS[p][1]['slug'])\n                        assert")
t=t.replace("                        page.locator('#previous-chapter').click()\n                        page.locator('#read-all')", "                        page.locator('#previous-chapter').click()\n                        page.wait_for_function('(id)=>document.querySelector(\".chapter:not([hidden])\").id===id',arg='chapter-'+CHAPTERS[p][0]['slug'])\n                        page.locator('#read-all')")
t=t.replace("                        page.evaluate('(id)=>location.hash=id',dest);page.wait_for_timeout(60)", "                        page.evaluate('(id)=>location.hash=id',dest)\n                        page.wait_for_function('(id)=>{const n=document.getElementById(id);return n&&!n.closest(\".chapter\").hidden}',arg=dest)")
t=t.replace("errors.append('Reading journey '+str(width)+': '+str(exc)+'; '+traceback.format_exc(limit=2))", "errors.append('Reading journey '+str(width)+' at '+page.url+': '+str(exc)+'; JavaScript='+str(js)+'; '+traceback.format_exc(limit=2))")
p.write_text(t)
Path(__file__).unlink()
