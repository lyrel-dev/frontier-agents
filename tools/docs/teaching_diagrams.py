"""Compatibility geometry metadata; all diagram content is Markdown-backed."""
from markdown_sources import repository, settings
DIAGRAMS={k:v for k,v in repository().diagrams().items() if k.startswith('teaching-')}
BOXES=settings('teaching-layout')['boxes']
PRODUCTS=settings('teaching-layout')['products']
