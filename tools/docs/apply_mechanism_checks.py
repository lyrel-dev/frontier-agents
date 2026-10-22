"""One-time wiring of mechanism-specific validation and editorial provenance."""
from pathlib import Path
import json
import re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASELINE='75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9'
REVISION='2026-10-22-mechanism-review'

def patch(path,old,new,count=1):
    p=ROOT/path;text=p.read_text()
    if text.count(old)!=count:raise ValueError(f'{path}: expected {count} anchors, found {text.count(old)} for {old[:80]!r}')
    p.write_text(text.replace(old,new))

patch('tools/docs/model_check.py',"    for m in M:\n        if m not in consumers:",
 "    for m in mechanisms:\n        for related in m.get('related_mechanisms',[]):\n            target=related.get('id')\n            if target not in M:errors.append(m['id']+': unknown related mechanism')\n            elif M[target]['platform']!=m['platform']:errors.append(m['id']+': cross-product related mechanism')\n            if related.get('dependency') not in ('optional','conditional') or not related.get('condition'):errors.append(m['id']+': unqualified related mechanism')\n            consumers.add(target)\n    for m in M:\n        if m not in consumers:")
# Mechanisms are explicitly authorized for review in Stage 3. Their 40 existing
# core identities and dependencies are now protected by mechanism_detail.validate.
# The existing checks continue to protect all approved outcome/configuration data.
patch('tools/docs/resource_model.py',"    for name in ('use-cases','mechanisms','features','profiles','aliases'):",
 "    # Mechanism review has its own core-field preservation check in Stage 3.\n    for name in ('use-cases','features','profiles','aliases'):")
patch('tools/docs/check.py','from resource_model import validate as validate_resources\n',
 'from resource_model import validate as validate_resources\nfrom mechanism_detail import validate as validate_mechanisms\n')
patch('tools/docs/check.py','    model_result=validate_model(guides, browser=browser)',
 '    mechanism_result=validate_mechanisms(guides,browser=browser)\n    errors.extend(mechanism_result["errors"])\n    model_result=validate_model(guides, browser=browser)')
patch('tools/docs/check.py',"    results['relationship_model']=model_result",
 "    results['mechanism_review']=mechanism_result\n    results['relationship_model']=model_result")
patch('tools/docs/check.py','# Documentation validation\\n\\n',
 '# Documentation validation\\n\\nStage 3 adds [mechanism lifecycle and preservation checks](qa/mechanism-review.json) and [claim-specific source review](qa/mechanism-source-review.json). Proposed AWS tests are documented but were not executed. Existing outcome, feature, profile, alias and resource-model sources are checked against the Stage 2 baseline.\\n\\n')
p=HERE/'structure.py';text=p.read_text()
text=re.sub(r'^REVISION=.*$',f'REVISION={REVISION!r}',text,flags=re.M)
text=re.sub(r'^BASELINE=.*$',f'BASELINE={BASELINE!r}',text,flags=re.M)
p.write_text(text)
p=ROOT/'EDITORIAL_STANDARD.md'
p.write_text(p.read_text()+'''\n\n## Mechanism explanations\n\nMaintain detailed mechanism narratives in the review field of the mechanism registry. The build renders the same explanation inside its primary guide section and includes that section in relevant presenter notes. Do not hand-edit the delimited generated blocks. A mechanism record identifies observable service behavior separately from undisclosed internals. Configuration and lifecycle steps vary in number with the subject. State labels are explanatory unless an exact service enum is cited. Tests are proposed engineering checks until separately executed and recorded.\n\nA conditional related-mechanism link can document behavior such as finding personalization without adding an outcome or changing the approved use-case workflow. Do not confuse eligibility for a mechanism with evidence that it ran. Material product assertions have section-specific official references; retrieval-version conflicts are recorded rather than silently resolved.\n''')
p=ROOT/'CHANGELOG.md'
p.write_text(p.read_text()+'''\n\n## 2026-10-22 — Mechanism configuration and lifecycle review\n\nReviewed the 40 existing mechanisms and added conditional Security Findings Personalization under the existing finding feature. The approved 30 use cases and the feature, profile, alias and resource-model sources are unchanged. Added detailed narrative, setup, state transitions, controls, observable output, undocumented boundaries and proposed positive/negative verification. Replaced selected slides and figures without increasing the 221-minute programme or 28-minute exercise allocation. No live AWS tests were run.\n''')
(ROOT/'qa/stage3-content-review.json').write_text(json.dumps({
 'stage':3,'baseline':BASELINE,'approved_use_cases':'preserved byte-for-byte',
 'mechanisms':'40 existing records retain core identities/dependencies; one documented support mechanism added',
 'new_mechanism':'Findings Personalization is distinct from Login Optimization and revalidation',
 'timing':'Existing per-slide budgets retained; no appended presentation track',
 'source_policy':'42 targeted official references; conflicting retrieved versions and unknown internals qualified',
 'live_aws_execution':False},indent=2)+'\n')
Path(__file__).unlink()
