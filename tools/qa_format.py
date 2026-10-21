import shutil, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[1]
qa=Path(tempfile.gettempdir())/'frontier-editorial-checks';qa.mkdir(parents=True,exist_ok=True)
checks=[]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for name in ['devops','security','finops','architecture']:
    page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
    dest={'devops':'devops/validated-report.html','security':'security/report.html','finops':'finops/report.html','architecture':'architecture/common-patterns.html'}[name]
    page.set_content((root/dest).read_text(encoding='utf-8'),wait_until='load')
    assert page.locator('#workflow .story-stage').count()==6
    n=page.locator('#capabilities .cap').count()
    assert n in (8,17,13,12)
    page.locator('#cap-search').fill('approval')
    visible=page.locator('#capabilities .cap:not([hidden])').count()
    assert visible>0,(name,visible)
    page.locator('#cap-search').fill('')
    page.locator('#include-preview').check()
    first=page.locator('#capabilities .cap').first
    first.locator('summary').first.click()
    first.scroll_into_view_if_needed();page.screenshot(path=str(qa/f'{name}-capability.png'))
    assert first.locator('.proposed-label').count()>0
    assert first.locator('.evidence-strip a').count()>0
    page.locator('#workflow').scroll_into_view_if_needed()
    page.screenshot(path=str(qa/f'{name}-workflow.png'))
    page.locator('button[data-present]').click()
    assert page.locator('body').evaluate('(el)=>el.classList.contains("presenting")')
    total=page.locator('.slide').count()
    core={'devops':18,'security':18,'finops':16,'architecture':18}[name]
    assert total==core+n,(name,total,core,n)
    page.locator('#slide-select').select_option(str(core))
    assert 'Reference' in page.locator('#slide-position').inner_text()
    assert page.locator('#timer-toggle').is_disabled()
    page.screenshot(path=str(qa/f'{name}-reference.png'))
    card=page.locator('.slide:not([hidden]) .reference-panel').count()
    assert card==5
    page.locator('#slide-select').select_option('0')
    assert not page.locator('#timer-toggle').is_disabled()
    checks.append({'report':name,'capabilities':n,'core_slides':core,'reference_slides':n,'tested_filter':'approval','html_nav':'pass','timer_boundary':'pass'})
    page.close()
  mobile=b.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
  mobile.set_content((root/'security/report.html').read_text(encoding='utf-8'),wait_until='load')
  mobile.locator('#include-preview').check()
  cap=mobile.locator('.cap').first
  cap.scroll_into_view_if_needed();cap.locator('summary').first.click()
  mobile.screenshot(path=str(qa/'security-mobile-capability.png'))
  mobile.locator('button[data-present]').click()
  mobile.locator('#slide-select').select_option('18')
  mobile.screenshot(path=str(qa/'security-mobile-reference.png'))
  mobile.close()
  b.close()
(root/'qa'/'editorial-interaction-validation.json').write_text(json.dumps({'checks':checks,'mobile':'security capability and reference captured'},indent=2)+'\n')
print(json.dumps(checks,indent=2))
