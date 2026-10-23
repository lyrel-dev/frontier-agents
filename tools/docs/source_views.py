"""Typed projections from Markdown front matter into the existing HTML renderer."""
import json
from markdown_sources import repository, ROOT


def chapters():
    result={}
    for source in repository().select('chapter'):
        definition={**source.meta['definition'],'title':source.meta['title'],'purpose':source.body}
        result.setdefault(source.meta['product'],[]).append(definition)
    return result


def deck_chapters():
    return {s.meta['product']:s.meta['chapters'] for s in repository().select('deck')}


def prepare():
    repo=repository()
    for name,value in repo.registers().items():
        source=next(s for s in repo.select('register') if s.meta['collection']==name)
        fmt=source.meta['json_format']
        raw=json.dumps(value,indent=fmt['indent'],ensure_ascii=fmt['ensure_ascii'])+('\n' if fmt['newline'] else '')
        (ROOT/'catalog'/f'{name}.json').write_text(raw,encoding='utf-8')
    for product,guide in repo.guides().items():
        lines=[guide['intro'],'']
        for number,chapter in enumerate(chapters()[product],1):
            lines += [f'## {number:02d}. {chapter["title"]}','',chapter['purpose'],'']
            for sid in chapter['sections']:
                section=guide['sections'][sid]
                lines += [f'### {sid} — {section["title"]}','',section['body'],'']
        lines += [guide['definitions'],'']
        (ROOT/'guides'/f'{product}.md').write_text('\n'.join(lines),encoding='utf-8')


def publish_pages():
    allowed={'README.md','PUBLISHING.md','AUTHORING.md','EDITORIAL_STANDARD.md'}
    for source in repository().select('page'):
        output=source.meta.get('output')
        if output not in allowed:
            raise ValueError('Unsupported authored page output: '+str(output))
        (ROOT/output).write_text(source.body.rstrip()+'\n',encoding='utf-8')
