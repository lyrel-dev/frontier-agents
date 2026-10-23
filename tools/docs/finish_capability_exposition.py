"""Complete the one-time capability migration and remove this migration source."""
from pathlib import Path
import re
import json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def patch(path,old,new,required=True):
    p=ROOT/path;text=p.read_text()
    if old not in text:
        if required:raise ValueError('Missing patch anchor in '+path+': '+old[:80])
        return
    p.write_text(text.replace(old,new))

patch('tools/docs/check.py','from editorial_check import validate as validate_editorial','from editorial_check import validate as validate_editorial\nfrom exposition_check import validate as validate_exposition')
patch('tools/docs/check.py','    editorial_result=validate_editorial(guides)','    exposition_result=validate_exposition(guides)\n    errors.extend(exposition_result["errors"])\n    editorial_result=validate_editorial(guides)')
patch('tools/docs/check.py',"    results['technical_editorial_review']=editorial_result","    results['technical_editorial_review']=editorial_result\n    results['capability_exposition']=exposition_result")
# Keep the historical validation modules, but test reference destinations rather than a superseded heading template.
patch('tools/docs/mechanism_detail.py',"if not node or node.name!='h4':errors.append(e['id']+': detailed guide anchor missing')", "if not node or not node.find_parent(class_='report-section'):errors.append(e['id']+': technical reference destination missing')",False)
patch('tools/docs/mechanism_detail.py','Generated, delimited Markdown blocks keep GitHub\'s readable edition aligned with\nHTML and speaker notes. Prose outside those blocks remains manually maintained.', 'The registry is retained for traceability. Capability exposition is authored in guides; registry rows are not emitted as peer product mechanisms.',False)
patch('tools/docs/reader.py','This revision does not change the model, case selection, workflow semantics, or source claims.', 'This revision preserves the model, case selection, and workflow semantics. Product exposition follows the supplied capability outline; targeted source qualifications are recorded in qa/exposition-review.json.',False)
patch('tools/docs/reader.py','Mechanisms and feature configuration are explained in their product-guide context rather than in separate record indexes.', 'The product guides explain concrete platform facilities and their operating mechanisms by capability dimension. The frozen dependency registers supply references, not a product taxonomy.',False)
patch('tools/docs/reader.py','Guides have chapter navigation and one search.', 'Guides distinguish workspace organization, definition, context, invocation, integrations, network connectivity, execution controls, managed functions, outputs, and administration. They have chapter navigation and one search.',False)
p=HERE/'presentation.py';text=p.read_text()
text=text.replace('An automation is a task factory; it is not the task or the external ','An automation creates tasks on the configured condition; it is separate from the external ')
text=text.replace('An automation is a task factory','An automation creates tasks on the configured condition')
p.write_text(text)
# Add concrete memory lifecycle information from the supplied outline without changing the frozen registry.
p=ROOT/'guides/devops.md';text=p.read_text()
marker='### D-17 — Attachments and repository-backed authoring'
addition='Memories can be organized by `/`-separated paths within a store. Store and entry descriptions guide selection. The documented limits are 50 stores per Agent Space, 200 memories per store, and 100 KB per memory. Historical viewing, deactivation, and custom-store deletion are different operations; retention of versions is not a claim that a deleted custom store can be restored. [DS505]\n\n'
text=text.replace(marker,addition+marker)
p.write_text(text)
# The source-authoring instructions must no longer tell editors to maintain generated prose blocks.
p=HERE/'build.py';text=p.read_text()
text=text.replace('Edit guide prose outside the delimited generated blocks in `guides/*.md`; edit detailed mechanism prose and its claim references in the `review` fields of `catalog/mechanisms.json`. The build synchronizes those blocks before rendering.', 'Edit capability exposition and its official references in `guides/*.md`. The six catalog registers are frozen; they supply identifiers, approved workflows, and resource relationships, not automatic guide prose.')
text=text.replace('Edit cases in `catalog/use-cases.json`, mechanism and feature relationships in `catalog/mechanisms.json` and `catalog/features.json`, recipes in `catalog/profiles.json`, product entities and relationships in `catalog/resource-models.json`, chapter membership in `tools/docs/structure.py`, slide content in `tools/docs/presentation.py`, and figures in `tools/docs/diagrams.py`.', 'Change chapter membership in `tools/docs/structure.py`, HTML slide content in `tools/docs/presentation.py`, and figure definitions in their maintained modules. Changes to the frozen model or use-case definitions require explicit approval.')
p.write_text(text)
# State the current authorship rule once and retain the earlier entries only as Git history.
p=ROOT/'EDITORIAL_STANDARD.md';text=p.read_text()
text=re.sub(r'## Mechanism explanations\n.*?(?=\n## |\Z)', '''## Mechanism explanations\n\nDescribe the documented process in the capability section that owns it. A mechanism explanation follows its relevant inputs, selection or execution behavior, state changes, and controls. Do not impose a fixed number of steps or render every registry row as an AWS mechanism. Link use-case steps to the corresponding authored explanation. Preserve the frozen registry for traceability, not as a second source of guide prose.\n\n''',text,flags=re.S)
p.write_text(text)
p=ROOT/'qa/exposition-review.json';data=json.loads(p.read_text())
data['presentation_changes']='Existing useful tables/figures/exercises retained and ordered by the capability chapters; new slides cover managed/custom definition, event filters, integration direction, transport, and administrative APIs.'
data['removed_rendering']='Automatic mechanism-review blocks and their nested index headings; frozen references resolve to authored technical sections.'
p.write_text(json.dumps(data,indent=2)+'\n')
Path(__file__).unlink()
