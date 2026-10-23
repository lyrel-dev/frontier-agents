"""Chapter definitions are read from canonical Markdown front matter."""
from pathlib import Path
from markdown_sources import settings, repository
from source_views import chapters, deck_chapters
ROOT=Path(__file__).resolve().parents[2]
REVISION='markdown-'+repository().revision[:16]
BASELINE=settings('structure')['baseline']
CHAPTERS=chapters()
DECK_CHAPTERS=deck_chapters()
TYPES=settings('structure')['types']
LABELS=settings('structure')['labels']
def section_type(sid):
    return 'example' if '-U' in sid else 'mechanism' if '-M' in sid else TYPES.get(sid,'reference')
