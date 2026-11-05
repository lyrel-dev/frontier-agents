#!/usr/bin/env python3
"""Build report.pdf from canonical report.md and the four source-derived SVGs.

Usage, from any directory:
    python3 /path/to/analysis/tools/build_report.py

Dependency: reportlab. Fonts fall back to PDF standard fonts when DejaVu Sans
is unavailable. The Markdown and SVG readers intentionally support only the
small, documented subset used by this report. No network, browser, Node, or
external Mermaid service is needed. Editable .mmd data drives SVG rendering.
"""
from __future__ import annotations

import argparse
import re
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from render_diagrams import ANALYSIS, LAYOUTS, render_one

PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 84
INK = colors.HexColor("#23364A")
NAVY = colors.HexColor("#172D43")
TEAL = colors.HexColor("#087884")
BLUE = colors.HexColor("#2456A1")
MUTED = colors.HexColor("#5C6F82")
LINE = colors.HexColor("#D6E0E8")
PALE = colors.HexColor("#F2F6F9")


def configure_fonts() -> tuple[str, str, str]:
    roots = [Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/local/share/fonts"), Path.home() / ".fonts"]
    for root in roots:
        regular, bold, mono = (root / name for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSansMono.ttf"))
        if all(path.is_file() for path in (regular, bold, mono)):
            for name, path in [("BodyFont", regular), ("BoldFont", bold), ("MonoFont", mono)]:
                pdfmetrics.registerFont(TTFont(name, str(path)))
            pdfmetrics.registerFontFamily("BodyFont", normal="BodyFont", bold="BoldFont", italic="BodyFont", boldItalic="BoldFont")
            return "BodyFont", "BoldFont", "MonoFont"
    return "Helvetica", "Helvetica-Bold", "Courier"


BODY, BOLD, MONO = configure_fonts()
STYLES = {
    "body": ParagraphStyle("body", fontName=BODY, fontSize=9, leading=13.3, textColor=INK, spaceAfter=7, allowWidows=0, allowOrphans=0),
    "cover": ParagraphStyle("cover", fontName=BOLD, fontSize=30, leading=36, textColor=NAVY, spaceBefore=14, spaceAfter=17, keepWithNext=True),
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=20, leading=25, textColor=NAVY, spaceBefore=0, spaceAfter=12, keepWithNext=True),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=12, leading=16.5, textColor=TEAL, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    "cell": ParagraphStyle("cell", fontName=BODY, fontSize=7.65, leading=10.9, textColor=INK, spaceAfter=0),
    "cell_head": ParagraphStyle("cell_head", fontName=BOLD, fontSize=7.8, leading=11.2, textColor=colors.white, spaceAfter=0),
    "bullet": ParagraphStyle("bullet", fontName=BODY, fontSize=9, leading=13.3, textColor=INK, leftIndent=11, firstLineIndent=-9, spaceAfter=5),
    "source": ParagraphStyle("source", fontName=BODY, fontSize=7.65, leading=10.8, textColor=INK, spaceAfter=7),
    "caption": ParagraphStyle("caption", fontName=BODY, fontSize=8, leading=11.5, textColor=MUTED, spaceAfter=6),
}


def inline(text: str, references: dict[str, str], compact: bool = False) -> str:
    """Escape source text, then render links/emphasis/code from our Markdown subset."""
    placeholders: list[str] = []
    def keep(markup: str) -> str:
        placeholders.append(markup)
        return f"ZZINLINE{len(placeholders)-1}ZZ"
    def code(match: re.Match) -> str:
        size = "7.25" if compact else "8.1"
        return keep(f'<font name="{MONO}" size="{size}">{escape(match.group(1))}</font>')
    text = re.sub(r"`([^`]+)`", code, text)
    def link(match: re.Match) -> str:
        label, url = match.groups()
        # Repository-relative links remain usable next to the source package.
        return keep(f'<link href="{escape(url, quote=True)}" color="#2456A1">{escape(label)}</link>')
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    def reference(match: re.Match) -> str:
        key = match.group(1)
        if key not in references:
            raise ValueError(f"Undefined source reference [{key}]")
        return f'<link href="{escape(references[key], quote=True)}" color="#2456A1">[{key}]</link>'
    text = re.sub(r"\[(\d+)\]", reference, text)
    for i, markup in enumerate(placeholders):
        text = text.replace(f"ZZINLINE{i}ZZ", markup)
    return text


def paragraph(text: str, references: dict[str, str], style: str = "body") -> Paragraph:
    return Paragraph(inline(text, references, style.startswith("cell")), STYLES[style])


def svg_color(value: str | None) -> colors.Color | None:
    return None if value in (None, "none") else colors.HexColor(value)


class SvgDiagram(Flowable):
    """Vector renderer for the rect/polyline/text SVG subset we generate."""
    def __init__(self, path: Path):
        super().__init__()
        self.root = ET.parse(path).getroot()
        _, _, source_w, source_h = map(float, self.root.attrib["viewBox"].split())
        self.source_w, self.source_h = source_w, source_h
        self.scale_factor = min(CONTENT_W / source_w, 510 / source_h)
        self.width, self.height = source_w * self.scale_factor, source_h * self.scale_factor
        self.hAlign = "CENTER"

    def draw(self) -> None:
        c = self.canv
        c.saveState()
        c.scale(self.scale_factor, self.scale_factor)
        for element in self.root.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            a = element.attrib
            fill, stroke = svg_color(a.get("fill")), svg_color(a.get("stroke"))
            if tag in ("rect", "polyline", "line"):
                if fill is not None:
                    c.setFillColor(fill)
                if stroke is not None:
                    c.setStrokeColor(stroke)
                c.setLineWidth(float(a.get("stroke-width", "1")))
            if tag == "rect":
                x, y, w, h = (float(a.get(k, 0)) for k in ("x", "y", "width", "height"))
                radius = float(a.get("rx", "0"))
                if radius:
                    c.roundRect(x, self.source_h-y-h, w, h, radius, stroke=int(stroke is not None), fill=int(fill is not None))
                else:
                    c.rect(x, self.source_h-y-h, w, h, stroke=int(stroke is not None), fill=int(fill is not None))
            elif tag == "polyline":
                coords = [tuple(map(float, pair.split(","))) for pair in a["points"].split()]
                p = c.beginPath()
                p.moveTo(coords[0][0], self.source_h-coords[0][1])
                for x, y in coords[1:]:
                    p.lineTo(x, self.source_h-y)
                c.drawPath(p, stroke=1, fill=0)
            elif tag == "line":
                c.line(float(a["x1"]), self.source_h-float(a["y1"]), float(a["x2"]), self.source_h-float(a["y2"]))
            elif tag == "text":
                text = "".join(element.itertext())
                x, y = float(a.get("x", 0)), self.source_h-float(a.get("y", 0))
                font = BOLD if a.get("font-weight") == "700" else BODY
                c.setFont(font, float(a.get("font-size", "12")))
                c.setFillColor(fill or INK)
                anchor = a.get("text-anchor", "start")
                {"start": c.drawString, "end": c.drawRightString, "middle": c.drawCentredString}[anchor](x, y, text)
        c.restoreState()


def render_table(lines: list[str], references: dict[str, str]) -> Table:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    headers, body = rows[0], rows[2:]
    count = len(headers)
    if any(len(row) != count for row in body):
        raise ValueError(f"Uneven Markdown table near {headers}")
    if count == 2:
        ratios = [0.30, 0.70]
    elif count == 4:
        ratios = [0.17, 0.18, 0.31, 0.34]
    elif headers[0] == "Operation":
        ratios = [0.37, 0.28, 0.35]
    elif "Entity" in headers[0] or "Supporting" in headers[0]:
        ratios = [0.26, 0.42, 0.32]
    else:
        ratios = [0.27, 0.36, 0.37]
    data = [[paragraph(cell, references, "cell_head") for cell in headers]]
    data.extend([paragraph(cell, references, "cell") for cell in row] for row in body)
    table = Table(data, colWidths=[CONTENT_W * ratio for ratio in ratios], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PALE]),
        ("LINEBELOW", (0,1), (-1,-1), 0.35, LINE),
    ]))
    return table


def markdown_flowables(source: Path) -> list:
    raw = source.read_text(encoding="utf-8")
    references = dict(re.findall(r"^\[(\d+)\]:\s*(\S+)\s*$", raw, re.M))
    lines, story = raw.splitlines(), []
    i = 0
    source_index = False
    while i < len(lines):
        line = lines[i].strip()
        if not line or re.match(r"^\[\d+\]:", line):
            i += 1
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak()); i += 1; continue
        if line.startswith("<!--"):
            i += 1; continue
        if line.startswith("# "):
            story.append(paragraph(line[2:], references, "cover")); i += 1; continue
        if line.startswith("## "):
            heading = line[3:]
            source_index = "Official source index" in heading
            style = "h2" if heading == "Design recommendation" else "h1"
            story.append(paragraph(heading, references, style)); i += 1; continue
        if line.startswith("### "):
            story.append(paragraph(line[4:], references, "h2")); i += 1; continue
        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image:
            target = (source.parent / image.group(2)).resolve()
            if target.suffix != ".svg" or not target.is_relative_to(source.parent):
                raise ValueError(f"Unsupported or unsafe image reference: {line}")
            story.append(SvgDiagram(target)); story.append(Spacer(1, 8)); i += 1; continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i]); i += 1
            story.append(render_table(table_lines, references)); story.append(Spacer(1, 8)); continue
        if line.startswith("- "):
            story.append(paragraph("• " + line[2:], references, "bullet")); i += 1; continue
        if re.match(r"^\d+\. ", line):
            if source_index:
                match = re.fullmatch(r"(\d+)\. \[([^\]]+)\]\(([^)]+)\)", line)
                if not match:
                    raise ValueError(f"Unsupported source-list entry: {line}")
                number, name, url = match.groups()
                label = f'<b>[{number}] {escape(name)}</b><br/><link href="{escape(url, quote=True)}" color="#2456A1">{escape(url)}</link>'
                story.append(Paragraph(label, STYLES["source"]))
            else:
                story.append(paragraph(line, references, "bullet"))
            i += 1; continue
        if line.startswith("```"):
            raise ValueError("This report uses diagram images with editable .mmd links; fenced code rendering is intentionally unsupported")
        paragraph_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |!\[|<!--|\[\d+\]:|\d+\. )", lines[i].strip()):
            paragraph_lines.append(lines[i].strip()); i += 1
        style = "caption" if line.startswith("Editable source:") else "body"
        story.append(paragraph(" ".join(paragraph_lines), references, style))
    return story


def footer(c, doc) -> None:
    c.saveState()
    c.setStrokeColor(LINE)
    c.line(42, PAGE_H-37, PAGE_W-42, PAGE_H-37)
    c.setFillColor(MUTED); c.setFont(BOLD, 7)
    c.drawString(42, PAGE_H-28, "AWS HEALTH / REVIEWED MODEL")
    c.setFont(BODY, 7)
    c.drawRightString(PAGE_W-42, PAGE_H-28, "05 NOV 2026 · REVISION 1.1")
    c.line(42, 35, PAGE_W-42, 35)
    c.drawString(42, 23, "AWS facts, local workflow, derived posture, and coverage retain distinct meanings.")
    c.drawRightString(PAGE_W-42, 23, str(doc.page))
    c.restoreState()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ANALYSIS / "report.pdf")
    args = parser.parse_args()
    for stem in LAYOUTS:
        render_one(stem)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=55, bottomMargin=51,
        title="AWS Health API and Abstract Data Model — Reviewed Report",
        author="Frontier Agents", subject="Official API model, ERDs, lifecycle posture, operator workflow, and mock application contract",
        pageCompression=1, invariant=1, lang="en",
    )
    doc.build(markdown_flowables(ANALYSIS / "report.md"), onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == "__main__":
    main()
