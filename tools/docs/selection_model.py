"""Semantic HTML scopes are not source-edit units or AWS entities.

Membership includes collapsed and filtered content. Unmapped generated elements
remain annotatable but do not authorize edits to enclosing source blocks.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
from bs4 import BeautifulSoup, Tag

SCHEMA = 'frontier-selection/v1'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode('utf-8')).hexdigest()


def ordered_unique(values):
    return list(dict.fromkeys(values))


def wrap_subsections(soup):
    """Group a heading with its following body, stopping at the next peer."""
    for section in list(soup.select('.report-section')):
        stack = [(3, section)]
        for child in list(section.contents):
            if isinstance(child, Tag) and any(c in child.get('class',[]) for c in ('feature-reference','related-reading')):
                stack=[(3,section)]
            if isinstance(child, Tag) and re.fullmatch(r'h[4-6]', child.name or ''):
                level = int(child.name[1])
                while len(stack) > 1 and stack[-1][0] >= level:
                    stack.pop()
                group = soup.new_tag('section', attrs={'class': 'review-subsection'})
                stack[-1][1].append(group)
                group.append(child.extract())
                stack.append((level, group))
            elif len(stack) > 1:
                stack[-1][1].append(child.extract())


def compile_selections(soup, document, targets, revision):
    wrap_subsections(soup)
    main = soup.find('main')
    if main is None:
        return {}
    selectors = ('main,[data-review-block],[data-reader-chapter],.report-section,'
        '.review-subsection,.slide,.note-block,.guide-introduction,.content-unit,'
        '.case-narrative,.configuration-recipe,.case-variant,section,article,'
        'p,h1,h2,h3,h4,h5,h6,ul,ol,li,table,tr,td,th,figure,figcaption,pre,blockquote')
    excluded = ('nav,form,button,input,textarea,select,script,style,svg,'
        '[data-review-ui],.deck-toolbar,.timer-bar,.reader-search,.chapter-pager,'
        '.slide-top,.slide-foot,.edition-links,.breadcrumbs,.toc')
    excluded_ids = {id(e) for e in soup.select(excluded)}
    candidates = []
    for element in soup.select(selectors):
        if element is not main and main not in element.parents:
            continue
        if any(id(p) in excluded_ids for p in [element, *element.parents]):
            continue
        if element is not main and not element.get_text(strip=True) and not element.get('data-review-block'):
            continue
        candidates.append(element)
    used = Counter()
    nodes = {}
    by_element = {}
    for order, element in enumerate(candidates):
        classes = element.get('class', [])
        kind = ('document' if element is main else 'chapter' if element.has_attr('data-reader-chapter')
            else 'section' if 'report-section' in classes else 'subsection' if 'review-subsection' in classes
            else 'slide' if 'slide' in classes else 'presenter-notes' if 'note-block' in classes
            else 'group' if element.name in ('section', 'article', 'header', 'div')
            else {'p':'paragraph','ul':'list','ol':'list','li':'list-item','tr':'table-row',
                  'td':'table-cell','th':'table-cell','figure':'figure','figcaption':'caption',
                  'pre':'code','blockquote':'quotation'}.get(element.name,element.name))
        if re.fullmatch(r'h[1-6]', element.name or ''):
            kind = 'heading'
        heading = element.find(re.compile('^h[1-6]$'))
        text = element.get_text(' ', strip=True)
        label = (' '.join((heading.get_text(' ', strip=True) if heading and kind in
            ('document','chapter','section','subsection','slide','presenter-notes','group') else text).split()))[:110]
        ancestor = next((by_element[id(p)] for p in element.parents if id(p) in by_element), None)
        anchor = element.get('id')
        if not anchor:
            seed = [document, ancestor, kind, element.get('data-review-block'), label]
            stem = 'selection-' + digest(seed)[:18]
            used[stem] += 1
            anchor = stem + ('-' + str(used[stem]) if used[stem] > 1 else '')
            element['id'] = anchor
        ident = 'scope:' + anchor
        if ident in nodes:
            raise ValueError('Duplicate selection anchor in ' + document + ': ' + anchor)
        element['data-review-scope'] = ident
        element['data-review-kind'] = kind
        by_element[id(element)] = ident
        members = [element] + list(element.select('[data-review-block]'))
        ids = ordered_unique(e.get('data-review-block') for e in members if e.get('data-review-block') in targets)
        contextual = next((p.get('data-review-block') for p in element.parents
                           if p.get('data-review-block') in targets), None)
        context_ids = [contextual] if contextual and contextual not in ids else []
        nodes[ident] = {'id': ident, 'anchor': anchor, 'kind': kind, 'label': label or kind,
            'parent': ancestor, 'order': order, 'target_ids': ids, 'context_ids': context_ids,
            'protected_targets': sum(bool(targets[t].get('protected')) for t in ids),
            'annotation_only': not ids}
    for element in candidates:
        node = nodes[by_element[id(element)]]
        descendants = [nodes[by_element[id(child)]] for child in element.descendants
                       if isinstance(child, Tag) and id(child) in by_element]
        gaps = [child['id'] for child in descendants if child['annotation_only'] and
                not set(child['context_ids']).intersection(node['target_ids'])]
        node['unmapped_parts'] = len(gaps)
        fingerprints = [[t, targets[t]['path'], targets[t]['file_sha256'], targets[t]['block_sha256']]
                        for t in node['target_ids'] + node['context_ids']]
        node['membership_sha256'] = digest([node['id'], node['parent'], node['kind'], fingerprints, gaps])
    return nodes


def snapshot_keys():
    return ('id','anchor','kind','label','target_ids','context_ids','membership_sha256')


def validate_structure(comment, repo, root):
    """Check captured scopes without expanding them or trusting CSS selectors.

Structural annotations require a compiled map of the same canonical revision.
Legacy block/quote packets retain the existing exact-hash validation path.
"""
    selection = comment.get('selection')
    if selection is None:
        if comment.get('scope') == 'structure':
            raise ValueError('Structural annotation lacks a selection snapshot')
        return
    if not isinstance(selection, dict) or selection.get('schema') != SCHEMA:
        raise ValueError('Unsupported structural selection schema')
    if selection.get('content_revision') != repo.revision:
        raise ValueError('Structural selection is stale; rebuild and review the current scope')
    document = comment.get('document')
    if not isinstance(document, str) or not re.fullmatch(r'(?:index|(?:guides|catalog|presentations)/[A-Za-z0-9_.-]+)\.html', document):
        raise ValueError('Invalid structural document path')
    path = Path(root) / PurePosixPath(document)
    if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents] if p != Path(root)):
        raise ValueError('Structural document unavailable or uses a symlink')
    if not path.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError('Structural document escapes the repository')
    element = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser').find(id='review-source-map')
    if element is None:
        raise ValueError('Rebuild the structural source map before editing')
    current = json.loads(element.string)
    if current.get('content_revision') != repo.revision or current.get('document') != document:
        raise ValueError('Generated selection map is stale; rebuild before editing')
    roots = selection.get('roots')
    if not isinstance(roots, list) or not 1 <= len(roots) <= 10000:
        raise ValueError('Selection requires explicit roots')
    nodes = current.get('selections', {})
    ids = []; contexts = []; root_ids = []
    for chosen in roots:
        if not isinstance(chosen, dict) or set(chosen) != set(snapshot_keys()):
            raise ValueError('Invalid selection root snapshot')
        key = chosen['id']
        if not isinstance(key, str) or key in root_ids or key not in nodes:
            raise ValueError('Selected root is duplicate, missing, or ambiguous')
        node = nodes[key]
        if any(chosen[k] != node.get(k) for k in snapshot_keys()):
            raise ValueError('Selected scope membership changed; obtain a new review')
        root_ids.append(key); ids.extend(node['target_ids']); contexts.extend(node['context_ids'])
    for key in root_ids:
        seen = set(); parent = nodes[key]['parent']
        while parent:
            if parent in seen or parent not in nodes:
                raise ValueError('Invalid hierarchy')
            if parent in root_ids:
                raise ValueError('Ancestor/descendant selections must be normalized')
            seen.add(parent); parent = nodes[parent]['parent']
    expected = ordered_unique(ids)
    if selection.get('target_ids') != expected or selection.get('context_ids') != ordered_unique(contexts):
        raise ValueError('Selection members were broadened, reordered, or omitted')
    supplied = comment.get('targets')
    if not isinstance(supplied, list) or [t.get('block_id') for t in supplied] != expected:
        raise ValueError('Comment source targets do not match the captured scope')
    for target in supplied:
        actual = repo.targets.get(target['block_id'])
        if actual is None or any(actual[k] != target.get(k) for k in
            ('path','source_id','file_sha256','block_sha256','markdown','start_char','end_char','start_byte','end_byte')):
            raise ValueError('A captured scope member is stale or invalid')
    if not expected:
        raise ValueError('This element is annotation-only; no exact source edit was authorized')
