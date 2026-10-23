"""Complete the reviewed source-selection migration, then remove this helper."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'tools/docs'
p=HERE/'contextual_check.py';s=p.read_text()
old="                assert page.locator('.review-selected').count() == 2"
new="""                expected=page.evaluate('''ids=>{const map=JSON.parse(document.getElementById('review-source-map').textContent);return [...new Set(ids.flatMap(id=>map.selections[id].target_ids))];}''', [candidates.nth(0).get_attribute('data-review-scope'),candidates.nth(2).get_attribute('data-review-scope')])
                actual=page.locator('.review-selected').evaluate_all('(els)=>[...new Set(els.map(el=>el.dataset.reviewBlock))]')
                assert set(actual)==set(expected), {'selected':actual,'expected':expected}"""
assert old in s;s=s.replace(old,new);p.write_text(s)
p=HERE/'review.js';s=p.read_text()
old="element.classList.toggle('review-selected',!!element.dataset.reviewBlock&&selected.has(element.dataset.reviewBlock));"
new="element.classList.toggle('review-selected',!!element.dataset.reviewBlock&&selected.has(element.dataset.reviewBlock)&&(!selectionRoots.length||selectionRoots.some(id=>{const root=hierarchy.element(id);return root===element||root?.contains(element);})));"
assert old in s;s=s.replace(old,new)
old="if(!block.hasAttribute('tabindex'))block.tabIndex=0;"
new="if(!block.hasAttribute('tabindex')&&(block.hasAttribute('data-review-block')||['document','chapter','section','subsection','slide','presenter-notes','group'].includes(hierarchy.nodes[hierarchy.key(block)]?.kind)))block.tabIndex=0;"
assert old in s;s=s.replace(old,new);p.write_text(s)

p=ROOT/'content/site/authoring.md';s=p.read_text()
s+='''

<!-- block: authoring-hierarchical-selection -->
## Selection scope, source membership, and edit authorization

Selection follows the document hierarchy, not the storage layout of its Markdown files. Hover or focus an element and use **Parent** or the **Selection scope** control to choose the enclosing subsection, section, chapter, slide, or document. A heading selection refers to its heading text; choosing the section refers to the heading and its complete contents. The selection outline and count identify the selected boundary before a note is created. On a focused selection handle, Alt+Up selects the parent and Alt+Down returns through the expansion path.

A container selection includes mapped descendants even when a reader search, collapsed detail, or inactive chapter hides them. The selection summary reports source blocks not currently displayed and protected targets. A range of peer structural units uses their document order, not just their visible descendants. Selecting an ancestor and one of its descendants is normalized to the ancestor. Source targets are deduplicated in reading order, while highlights and comment markers remain attached to the selected rendered instance.

Three independent concepts govern review: the **presentation scope** the reader selected, the **source membership snapshot** captured for that scope, and the **allowed edit** within that snapshot. Selecting a chapter never grants whole-file access. A proposed patch may change only explicitly listed source targets; source paths, exact prior text, hashes, block identities, frozen-register restrictions and human diff review remain required.

The compiler adds a `selections` tree to each source map. Nodes carry parent identity, kind, label, rendered anchor, ordered source-target IDs, contextual IDs, and a membership digest. A new annotation records `selection.schema: frontier-selection/v1`, its source revision, chosen root snapshots and the exact resolved target list. `frontier-review/v1` and `frontier-source-patch/v1` remain compatible with existing block/quote records. The structural metadata is this documentation application's model, not a change to the approved AWS entity model.

Unmapped generated prose and nested elements without an independent exact Markdown range can receive **annotation-only** notes. Their containing source block is contextual information, not an edit grant. For example, selecting an unmapped table cell does not silently authorize rewriting its complete table. Choose the explicitly mapped table scope for a block-level edit after reviewing that wider selection. Mixed containers allow edits only to their enumerated mapped targets; the interface identifies unmapped content.

Structural annotations keep immutable membership. They do not acquire newly added children or get reassigned to another section after a rebuild. The initial policy is conservative: a change to the canonical content revision requires renewed structural review before automated source editing, even if some selected text is unchanged. Missing or changed roots are stale. Legacy block and quote annotations retain their exact-source hash checks. Imported metadata is untrusted and the patch guard independently validates it against current compiled membership and canonical source ranges.

A structural note has a marker on the selected container, not a separate duplicated thread on every paragraph. Note popups still show only notes and note actions. Export, backend saving, import and confirmed clearing remain in the global annotation menu; all annotation text continues to save locally automatically. Exporting a selection does not transmit it to an LLM or authorize its instructions to execute.
'''
p.write_text(s)
p=ROOT/'content/site/readme.md';s=p.read_text();s+='''

<!-- block: readme-hierarchical-selection -->
### Select a section or complete slide

Hover or focus content, then use **Parent** or **Selection scope** to select a complete subsection, section, chapter, slide, or document. The displayed boundary is independent of Markdown file boundaries. Comments capture an immutable ordered list of exact source targets, including hidden descendants. Annotation-only elements and protected records do not grant source-edit permission. See the selection contract in [AUTHORING.md](AUTHORING.md).
''';p.write_text(s)
p=ROOT/'WORKSTREAM.md';s=p.read_text();header,body=s[4:].split('\n---\n',1);m=yaml.safe_load(header)
m['document_version']=4
m['repository']['implementation_branch']='docs/hierarchical-selection'
m['repository']['implementation_baseline']='516ad5d14b05cc732600efd5ae1b51e41994168b'
m['repository'].pop('validated_output_before_handoff',None)
m['contextual_annotation_contract']['version']='contextual-v4'
m['contextual_annotation_contract']['selection']='Text and semantic elements through subsection, section, chapter, complete slide and document; explicit parent/scope controls.'
m['selection_contract']={
 'schema':'frontier-selection/v1',
 'concepts':['presentation scope','immutable source-membership snapshot','explicit permitted edit'],
 'product_model_changes':False,
 'containers':'Complete mapped membership, independent of filtering or collapse.',
 'normalization':'Ancestor subsumes descendant; exact source targets deduplicated in reading order.',
 'heading_policy':'Heading text is distinct from its containing section.',
 'unmapped_policy':'Annotation-only; surrounding source is context, not edit permission.',
 'marker_policy':'One thread anchor per selected rendered root, not one per child.',
 'revision_policy':'Changed canonical content invalidates structural edit authorization; no fuzzy reattachment.',
 'guard_policy':'Validate root snapshots, membership, canonical ranges and existing frozen/hash constraints.',
 'compatibility':'Existing frontier-review/v1 block and quote records retain their previous guards.'}
m['validation_snapshot']['hierarchy_evidence']='qa/authoring-review.json hierarchical_selection; inspect the successful run for this exact revision.'
m['validation_snapshot']['historical_run_note']='Earlier run links validate their own snapshots, not new structural selection changes.'
m['milestones'].append({'id':'M10','status':'implementation_requires_current_validation','name':'Hierarchical selection, exact member snapshots, guard and acceptance-test correction','qualification':'Source-level protection and human acceptance remain separate.'})
for item in m['roadmap']:
 if item['id']=='N03':
  item['status']='hierarchical_acceptance_pending'
  item['tasks'].extend(['Demonstrate heading versus complete section/chapter/slide selection, including hidden members.','Verify one container thread, immutable exported membership, and rejection of broader or stale edits.'])
 if item['id']=='N04':item['tasks'].append('Extend nested, context-only, sibling-range and generated-content coverage; do not collapse semantic scope back into source-block identity.')
m['operating_rules'].append('Reader selection scope is not a source file or an edit wildcard; do not use visible-only blocks to represent a complete section.')
body+='''

## Hierarchical-selection decision correction

The prior selection implementation treated atomic source blocks as the complete set of reader-selectable objects. That decision was incorrect. It also let tests use the number of highlighted nodes as a proxy for selection scope. Semantic containers and their source-edit ranges are now independent: a complete section or slide has one selected boundary and an ordered, immutable set of source targets, potentially spanning multiple Markdown files.

The compiler constructs the presentation hierarchy; the client exposes explicit parent/scope selection, source-boundary highlighting and scope-root markers; the export captures membership; the patch tool independently validates that snapshot before permitting any exact member change. Parent membership includes filtered and collapsed descendants. Repeated source content does not cause selection highlighting to appear in unrelated rendered instances. Context-only or generated elements can be annotated without acquiring permission to edit their enclosing source.

This changes the documentation application's selection metadata only. It does not change approved AWS concepts, the frozen thirty use cases, or their relations. The note-only popup, global annotation menu, automatic local storage, explicit authenticated backend adapter, and manual LLM handoff remain the interaction contract.

Implementation modules: `tools/docs/selection_model.py` builds and validates the hierarchy; `selection_model.js` normalizes client scope selection; `source_review.py` embeds it; `review.js` exposes controls; `review_patch.py` enforces exact-edit authority. `hierarchy_check.py` adds semantic container, hidden-membership, ancestor-normalization, thread-anchor and unsafe-patch tests. All earlier contextual, automatic-save and backend-adapter tests remain enabled. Use `qa/authoring-review.json` and the successful current CI run as evidence; do not treat the older run links as validation of this revision.

The conservative first policy marks a structural snapshot stale whenever canonical content revision changes. That is intentionally stricter than locating a paragraph by its text: a newly inserted or removed member must never silently alter an editing scope. Any future relaxation must independently prove unchanged membership and retain the original reviewer-authorized target set.
'''
p.write_text('---\n'+yaml.safe_dump(m,sort_keys=False,allow_unicode=True,width=100)+'---\n'+body)
print('Updated semantic assertions, rendering boundaries, authoring decisions and handoff.')
Path(__file__).unlink()
