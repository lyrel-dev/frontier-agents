"""Check the supplied capability organization and preserve the accepted semantic model."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
BASELINE='d081eade643537905690c54c4968a2445489cf96'
DIMENSIONS=('workspace','definition','knowledge','invocation','integrations','network','runtime','managed-workflows','interfaces','administration')
FROZEN=('use-cases','mechanisms','features','profiles','aliases','resource-models')


def validate(guides):
    from structure import CHAPTERS
    from presentation import DECKS
    errors=[]
    preservation={}
    for name in FROZEN:
        path='catalog/'+name+'.json'
        expected=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
        actual=(ROOT/path).read_bytes()
        preservation[path]={'unchanged':expected==actual,'sha256':hashlib.sha256(actual).hexdigest()}
        if expected!=actual:errors.append('Frozen semantic source changed: '+path)
    reviewed={}
    for product in ('devops','security','finops'):
        chapters=CHAPTERS[product]
        if tuple(c['slug'] for c in chapters[:10])!=DIMENSIONS:
            errors.append(product+': supplied capability sequence not followed')
        if not chapters[-1].get('appendix'):
            errors.append(product+': worked example/reference material not separated from capability domains')
        text=(ROOT/f'guides/{product}.md').read_text()
        if '<!-- mechanism-review:' in text:
            errors.append(product+': record-schema block remains in the narrative')
        if '**Classification:**' in text or '**Inputs:**' in text:
            errors.append(product+': automatic registry-field exposition remains')
        if not all(c['purpose'].strip() and c['sections'] for c in chapters):
            errors.append(product+': empty chapter explanation')
        page=BeautifulSoup((ROOT/f'guides/{product}.html').read_text(),'html.parser')
        if page.select('h4[id^="MX-"]'):
            errors.append(product+': heterogeneous registry rows still presented as peer mechanisms')
        if len(page.select('.report-section'))!=len(guides[product]['sections']):
            errors.append(product+': authored sections missing from HTML')
        reviewed[product]={'primary_dimensions':[c['title'] for c in chapters[:10]],'appendix':chapters[-1]['title'],'sections':len(guides[product]['sections'])}
    devops=guides['devops']['sections']
    checks={
        'Managed roster and definition controls':('D-15',['Grader','Learning','system prompt']),
        'Custom-agent definition distinct from invocation':('D-16',['System prompt','Tools','Skills','Memory stores']),
        'Actual event-evaluation mechanism':('D-18',['JMESPath','4,096','10,000','project']),
        'Outbound delegation distinct from inbound access':('D-20',['agent card','external agent']),
        'Transport distinct from provider':('D-04',['VPC Lattice','443','DNS']),
        'Asset versus trigger':('D-13',['memory_store','test_profile','trigger']),
        'Service usage telemetry':('D-24',['ConsumedOnDemandTime','ConsumedChatRequests']),
    }
    for name,(sid,terms) in checks.items():
        body=devops[sid]['body']
        if not all(t.lower() in body.lower() for t in terms):errors.append(name+': expected technical distinction missing')
    if 'task factory' in (ROOT/'tools/docs/presentation.py').read_text():
        errors.append('Presentation retains an imprecise automation metaphor')
    if 'sync_guides()' in (ROOT/'tools/docs/build.py').read_text():
        errors.append('Build still overwrites guide prose from the dependency registry')
    result={'revision':'2026-10-23-capability-exposition','baseline':BASELINE,
            'basis':'Supplied ten-part DevOps capability outline, adapted to documented facilities of the other two services.',
            'frozen_sources':preservation,'guide_structure':reviewed,'distinctions_checked':list(checks),
            'errors':errors,
            'boundary':'Structural and preservation tests supplement the authored review. They do not establish exhaustive AWS coverage, explain undisclosed internals, or represent live service execution.'}
    (ROOT/'qa/exposition-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
