"""Diagram source is in DOT or SVG fences in content/diagrams/*.md."""
from markdown_sources import repository, build_diagrams
DIAGRAMS=repository().diagrams()
def build():
    return build_diagrams()
