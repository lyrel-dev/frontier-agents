"""Chapter definitions are read from canonical Markdown front matter."""
import json
from pathlib import Path
from markdown_sources import settings
from source_views import chapters, deck_chapters
ROOT=Path(__file__).resolve().parents[2]
REVISION=json.loads((ROOT/'documentation-build.json').read_text())['revision']
BASELINE=settings('structure')['baseline']
CHAPTERS=chapters()
DECK_CHAPTERS=deck_chapters()
TYPES=settings('structure')['types']
LABELS=settings('structure')['labels']
def section_type(sid):
    return 'example' if '-U' in sid else 'mechanism' if '-M' in sid else TYPES.get(sid,'reference')
