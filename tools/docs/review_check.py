#!/usr/bin/env python3
"""Regression checks for source mapping, contextual review and guarded patching."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import ast
import json
import subprocess
import tempfile
import traceback
from bs4 import BeautifulSoup
import markdown_sources as ms
import review_patch as guard
from contextual_check import browser_checks

ROOT=Path(__file__).resolve().parents[2]
BASELINE='4a34aaadc5f9fd0e4dbb492c36aa152730c8ba5a'


def source_checks():
    repo=ms.Repository();results=[]
    for name,value in repo.registers().items():
        expected=json.loads(subprocess.check_output(['git','show',BASELINE+':catalog/'+name+'.json'],cwd=ROOT))
        assert value==expected,'Frozen register changed: '+name
    results.append('all registry values equal the approved baseline')
    mapped=0
    for path in [ROOT/'index.html',*(ROOT/'guides').glob('*.html'),*(ROOT/'catalog').glob('*.html'),*(ROOT/'presentations').glob('*.html')]:
        page=BeautifulSoup(path.read_text(),'html.parser');node=page.find(id='review-source-map')
        assert node is not None,path.as_posix()
        data=json.loads(node.string)
        for bid,target in data['targets'].items():
            raw=(ROOT/target['path']).read_text()
            assert ms.digest(raw)==target['file_sha256']
            assert raw[target['start_char']:target['end_char']]==target['markdown']
            assert raw.encode()[target['start_byte']:target['end_byte']].decode()==target['markdown']
            assert ms.digest(target['markdown'])==target['block_sha256']
            assert bid in repo.targets
            mapped+=1
    results.append(f'{mapped} rendered source targets match exact Unicode and UTF-8 source ranges')
    for script in (ROOT/'tools/docs').glob('*.py'):
        if script.name == 'migrate_markdown_once.py':
            continue
        for stmt in ast.walk(ast.parse(script.read_text(encoding='utf-8'))):
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                if any(isinstance(t, ast.Name) and t.id == 'DECKS' for t in targets) and isinstance(stmt.value, (ast.Dict, ast.List)):
                    raise AssertionError('Literal presentation content remains in '+script.name)
    assert len(repo.select('slide'))==52
    assert len(repo.select('section'))>=111
    return results


def guard_checks():
    outcomes=[]
    original=(ms.ROOT,ms.CONTENT,guard.ROOT,guard.CONTENT)
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);content=root/'content';content.mkdir()
        ms.ROOT=root;ms.CONTENT=content;guard.ROOT=root;guard.CONTENT=content
        try:
            path=content/'example.md'
            raw='---\nid: example\nkind: section\ntitle: Example\n---\n\n<!-- block: example-one -->\nFirst paragraph with café and an emoji 🧭.\n\n<!-- block: example-two -->\nSecond paragraph must remain unchanged.\n'
            path.write_text(raw)
            target=ms.Repository().targets['example-one']
            review={'schema':'frontier-review/v1','review_id':'review-test','comments':[{'id':'comment-1','status':'open','scope':'blocks','targets':[target]}]}
            edit={'comment_id':'comment-1','path':'content/example.md','block_id':'example-one',
                  'expected_file_sha256':target['file_sha256'],'expected_block_sha256':target['block_sha256'],
                  'before':target['markdown'],'after':target['markdown'].replace('First','Reviewed')}
            patch={'schema':'frontier-source-patch/v1','review_id':'review-test','edits':[edit]}
            changes,_=guard.plan(review,patch)
            assert path.read_text()==raw,'Dry-run modified a source'
            guard.apply_plan(changes)
            assert 'Reviewed paragraph' in path.read_text() and 'Second paragraph must remain unchanged.' in path.read_text()
            assert path.read_text().count('<!-- block:')==2
            path.write_text(raw);outcomes.append('dry-run and exact Unicode block replacement')
            scoped=deepcopy(review)
            scoped['comments'][0]['scope']='text'
            scoped['comments'][0]['selector']={'type':'TextQuoteSelector','exact':'First'}
            changes,_=guard.plan(scoped,patch)
            assert 'Reviewed paragraph' in changes[path]['after']
            outcomes.append('exact selected text can be edited without widening block scope')
            def reject_text(proposal):
                try:guard.plan(scoped,proposal)
                except (ValueError,KeyError,TypeError):pass
                else:raise AssertionError('Text review authorized edits outside its quote')
            widened=deepcopy(patch)
            widened['edits'][0]['after']=edit['before'].replace('First','Reviewed').replace('paragraph','sentence')
            reject_text(widened)
            ambiguous=deepcopy(scoped)
            ambiguous['comments'][0]['selector']['exact']='with paragraph'
            try:guard.plan(ambiguous,patch)
            except (ValueError,KeyError,TypeError):pass
            else:raise AssertionError('Nonmatching rendered quote accepted for patch')
            outcomes.append('text selection rejects edits outside quote and unmappable selections')
            def reject(label,packet=review,proposal=patch):
                snapshot=path.read_bytes()
                try:guard.plan(packet,proposal)
                except (ValueError,KeyError,TypeError):pass
                else:raise AssertionError('Accepted invalid patch: '+label)
                assert path.read_bytes()==snapshot,'Rejected patch wrote bytes'
                outcomes.append(label)
            bad=deepcopy(patch);bad['review_id']='another';reject('review identity mismatch',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['path']='../outside.md';reject('path traversal',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['path']='guides/devops.html';reject('generated output target',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['block_id']='example-two';reject('unselected source block',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['before']='approximate';reject('nonexact source excerpt',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['after']+='\n<!-- block: forged -->\n';reject('block identity insertion',proposal=bad)
            bad=deepcopy(patch);bad['edits'].append(deepcopy(edit));reject('duplicate edits',proposal=bad)
            bad=deepcopy(review);bad['comments'][0]['status']='resolved';reject('resolved comment',packet=bad)
            path.write_text(raw+'\nAn unrelated newer edit.\n');reject('stale file even when selected block is unchanged');path.write_text(raw)
            protected=content/'registers';protected.mkdir();locked=protected/'locked.md'
            locked.write_text('---\nid: locked\nkind: record\ncollection: use-cases\n---\n<!-- block: frozen-one -->\nApproved objective.\n')
            frozen=ms.Repository().targets['frozen-one'];frozen['protected']=False
            bad=deepcopy(review);bad['comments'][0]['targets']=[frozen]
            proposal=deepcopy(patch);proposal['edits']=[{**edit,'path':'content/registers/locked.md','block_id':'frozen-one','before':frozen['markdown'],'after':'Changed objective.','expected_file_sha256':frozen['file_sha256'],'expected_block_sha256':frozen['block_sha256']}]
            reject('frozen record despite forged protection flag',packet=bad,proposal=proposal)
            link=content/'link.md';link.symlink_to(path)
            bad=deepcopy(patch);bad['edits'][0]['path']='content/link.md'
            packet=deepcopy(review);packet['comments'][0]['targets'][0]['path']='content/link.md'
            reject('symlink source',packet=packet,proposal=bad);link.unlink()
            second=content/'second.md';second.write_text(raw.replace('id: example','id: second').replace('example-one','second-one').replace('example-two','second-two'))
            second_target=ms.Repository().targets['second-one']
            packet=deepcopy(review);packet['comments'][0]['targets'].append(second_target)
            proposal=deepcopy(patch);proposal['edits'].append({**edit,'path':'content/second.md','block_id':'second-one',
                'expected_file_sha256':second_target['file_sha256'],'expected_block_sha256':second_target['block_sha256']})
            changes,_=guard.plan(packet,proposal);second.write_text(second.read_text()+'\nConcurrent edit.\n')
            try:guard.apply_plan(changes)
            except ValueError:pass
            else:raise AssertionError('Batch accepted concurrent change')
            assert path.read_text()==raw
            outcomes.append('batch preflight prevents partial application')
        finally:
            ms.ROOT,ms.CONTENT,guard.ROOT,guard.CONTENT=original
    return outcomes


if __name__=='__main__':
    result={'schema':'frontier-authoring-validation/v1','interaction':'contextual-v4','errors':[]}
    try:
        result['source_mapping']=source_checks()
        result['patch_guards']=guard_checks()
        result['browser']=browser_checks(ROOT)
        from annotation_menu_check import validate as validate_menu
        result['annotation_menu']=validate_menu(ROOT)
        from hierarchy_check import validate as validate_hierarchy
        result['hierarchical_selection']=validate_hierarchy(ROOT)
    except Exception:
        result['errors'].append(traceback.format_exc())
    (ROOT/'qa/authoring-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if result['errors']:raise SystemExit(1)
