"""Editorial regression checks; these do not establish technical completeness."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
BASELINE = '13b619a7cddd8249fbaa54931ca2099409eb8890'
PATTERNS = (
    r'\bseamless(?:ly)?\b', r'\beffortless(?:ly)?\b', r'\bgame[- ]changing\b',
    r'\brevolutionary\b', r'\bsupercharg\w*\b', r'\bunlock the (?:power|potential)\b',
    r'\bunleash\w*\b', r'\bworld[- ]class\b', r'\bbest[- ]in[- ]class\b',
    r'\bcutting[- ]edge\b', r'\btransformative\b', r'\bpowerful\b',
)
BOILERPLATE = (
    'The rows describe documented consequences and logical stages; they are not an invented SDK status enumeration.',
    'The verification procedure is authored engineering guidance. A failed or unobservable check must remain unresolved; no live AWS outcome is represented here.',
    'Applies to:',
)


def language_hits(text: str) -> list[str]:
    return [m.group(0) for pattern in PATTERNS for m in re.finditer(pattern, text, re.I)]


def rendered_text(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    for node in soup.select('script,style,pre,code,.claim-evidence'):
        node.decompose()
    return soup.get_text(' ', strip=True)


def validate(guides: dict) -> dict:
    errors: list[str] = []
    from presentation import DECKS
    from markdown_sources import repository
    MECHANISM_FIGURES = repository().diagrams()
    from mechanism_detail import load
    registry = load()
    entries = {e['id']: e for e in registry['entries']}
    records = json.loads((ROOT/'qa/technical-edit-record.json').read_text())
    inspected = []
    titles = []
    for product, guide in guides.items():
        for sid, section in guide['sections'].items():
            titles.append({'product': product, 'id': sid, 'title': section['title']})
        for relative in (f'guides/{product}.html', f'presentations/{product}.html'):
            text = rendered_text(ROOT/relative)
            hits = language_hits(text)
            if hits:
                errors.append(relative+': promotional phrasing '+', '.join(sorted(set(hits))))
            for phrase in BOILERPLATE:
                if phrase in text:
                    errors.append(relative+': repeated boilerplate remains: '+phrase[:65])
            inspected.append(relative)
        source = (ROOT/f'guides/{product}.md').read_text()
        if source.count('**Reading conventions.**') != 1:
            errors.append(product+': missing or repeated reading conventions')
        if re.search(r'\n{4,}', source):
            errors.append(product+': excessive empty paragraph spacing')
        for slide in DECKS[product]['slides']:
            titles.append({'product': product, 'id': 'slide', 'title': slide['title']})
            if not slide['message'].strip():
                errors.append(product+': missing presenter explanation')
    for relative in ('catalog/index.html','catalog/resource-models.html','index.html',*[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'catalog').glob('UC-*.html'))]):
        hits = language_hits(rendered_text(ROOT/relative))
        if hits:
            errors.append(relative+': promotional phrasing '+', '.join(sorted(set(hits))))
        inspected.append(relative)
    publication=MECHANISM_FIGURES['mechanism-finops-publication'][3]
    if 'chat -> jira' not in publication or 'chat -> slack' not in publication:errors.append('Diagram omits direct conversation publication')
    if 'Verify the actual role reached' in MECHANISM_FIGURES['mechanism-security-learning'][3]:errors.append('Team verification remains inside an AWS-owned state label')
    if any(s['title']=='Documentation and presentation acceptance criteria' for d in DECKS.values() for s in d['slides']):errors.append('Document-quality meta-slide remains in the technical programme')
    protected = {}
    for name in ('use-cases','features','profiles','aliases','resource-models'):
        relative = f'catalog/{name}.json'
        old = subprocess.check_output(['git','show',BASELINE+':'+relative], cwd=ROOT)
        current = (ROOT/relative).read_bytes()
        protected[relative] = {'unchanged': old == current, 'sha256': hashlib.sha256(current).hexdigest()}
        if old != current:
            errors.append(relative+': change outside the editorial review scope')
    for correction in records['core_corrections']:
        entry = entries[correction['id']]
        if entry[correction['field']] != correction['after']:
            errors.append(correction['id']+': reviewed correction does not match the register')
    if 'conversation' not in entries['MX-F-ARTIFACT']['state'].lower():
        errors.append('Report artifact provenance incorrectly requires a task')
    if 'outcome' not in entries['MX-F-MEMORY']['trigger'].lower():
        errors.append('Memory trigger omits retained task outcomes')
    if 'approved' in entries['MX-S-GENERATE']['trigger'].lower():
        errors.append('Team approval incorrectly represented as a native generation prerequisite')
    security = guides['security']['sections']['S-09']['body']
    if 'Azure DevOps' not in security or 'TFVC' not in security or 'SS490' not in security:
        errors.append('Security source inventory omits the qualified Azure DevOps binding')
    # Negative controls check that the language detector rejects actual slogans,
    # not legitimate API names, official product terms, or negative limitations.
    if not language_hits('Seamless deployment unlocks the power of automation.'):
        errors.append('Promotional-language negative control failed')
    if language_hits('A task can run automatically. Delivery is not guaranteed.'):
        errors.append('Language detector rejects technical qualification')
    result = {
        'reviewed_on': records['reviewed_on'], 'baseline': BASELINE,
        'scope': 'Technical wording, selected factual corrections, source/render consistency; not a full service audit.',
        'rendered_documents_checked': inspected, 'headings_and_slide_titles': titles,
        'protected_sources': protected, 'core_corrections': records['core_corrections'],
        'regressions': ['Promotional phrase rejected','Technical limitation accepted','Artifact provenance permits conversation or task','Memory inputs include task outcomes','Generation distinguished from team approval'],
        'errors': errors,
        'boundary': 'Lexical and consistency checks supplement editorial review. They do not measure prose quality, product completeness or live service behavior.'
    }
    (ROOT/'qa/editorial-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return result
