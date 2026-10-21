from pathlib import Path
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/mechanism-screens';Q.mkdir(exist_ok=True)
results={'revision':'2026-10-21-mechanisms-v1','files':[],'errors':[],'live_aws_execution':False,'render_method':'self-contained HTML loaded through Playwright set_content; local file URL navigation is restricted in this environment'};linkcount=0
for path in (ROOT/'mechanisms').glob('*.html'):
 soup=BeautifulSoup(path.read_text(),'html.parser');ids=[e['id'] for e in soup.find_all(id=True)]
 if len(ids)!=len(set(ids)):results['errors'].append('duplicate IDs '+path.name)
 for a in soup.find_all('a',href=True):
  h=a['href']
  if h.startswith(('http:','https:','mailto:','data:')):continue
  rel,_,anchor=h.partition('#');dest=(path.parent/rel).resolve() if rel else path;linkcount+=1
  if not dest.exists():results['errors'].append('missing '+str(dest))
  elif anchor:
   dids=ids if dest==path else [x['id'] for x in BeautifulSoup(dest.read_text(),'html.parser').find_all(id=True)]
   if anchor not in dids:results['errors'].append('missing anchor '+h)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for key in ['devops','kiro','security','finops','index']:
  page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True);errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.set_content((ROOT/f'mechanisms/{key}.html').read_text());page.wait_for_timeout(100)
  n=page.locator('.record').count()
  if n:
   page.locator('#expand').click();assert page.locator('.record[open]').count()==n
   page.locator('#search').fill('unmatchable-random-value');assert page.locator('.record:visible').count()==0
   page.locator('#reset').click();assert page.locator('.record:visible').count()==n
   family=page.locator('#family option').nth(1).text_content();page.locator('#family').select_option(label=family);assert page.locator('.record:visible').count()>0;page.locator('#reset').click()
   page.locator('[data-step="2"]').click();assert page.locator('.stage:visible').count()==1;page.locator('[data-step="all"]').click();assert page.locator('.stage:visible').count()==6
   page.locator('#next').click();assert '2 /' in page.locator('#slide-count').text_content()
   page.locator('#focus').click();page.keyboard.press('ArrowRight');assert '3 /' in page.locator('#slide-count').text_content();page.keyboard.press('Escape');assert 'fullscreen' not in page.locator('#reference').get_attribute('class') if page.locator('#reference').get_attribute('class') else True
   with page.expect_download() as dl:page.locator('#export').click()
   assert dl.value.suggested_filename=='mechanism-reference.json'
   page.locator('.checklist input').first.check()
   with page.expect_download() as dl:page.locator('#save-checks').click()
   assert dl.value.suggested_filename=='mechanism-review-worksheet.json'
   page.locator('#collapse').click();page.evaluate("window.dispatchEvent(new Event('beforeprint'))");assert page.locator('.record[open]').count()==n;page.evaluate("window.dispatchEvent(new Event('afterprint'))");assert page.locator('.record[open]').count()==0
   page.locator('.record').first.locator('summary').click();page.locator('.record').first.scroll_into_view_if_needed()
  overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+2');assert not overflow,(key,'desktop overflow')
  page.screenshot(path=str(Q/f'{key}-desktop.png'),full_page=False)
  page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100)
  overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+2');assert not overflow,(key,'mobile overflow')
  page.screenshot(path=str(Q/f'{key}-mobile.png'),full_page=False)
  if errors:results['errors']+=errors
  results['files'].append({'page':key,'mechanism_records':n,'desktop_width':1440,'mobile_width':390,'page_errors':errors,'interaction_checks':bool(n)})
  page.close()
 for rel in ['devops/validated-report.html','kiro/report.html','security/report.html','finops/report.html','architecture/common-patterns.html']:
  page=browser.new_page(viewport={'width':390,'height':844});page.set_content((ROOT/rel).read_text());assert page.locator('#mechanisms').count()==1
  page.locator('#mechanisms').scroll_into_view_if_needed()
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),rel
  page.close()
 browser.close()
results['companion_local_links_checked']=linkcount
(ROOT/'qa/mechanism-browser-validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2));assert not results['errors']
