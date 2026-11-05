#!/usr/bin/env python3
"""Build reviewed-report.pdf from report.md and the five local SVG diagrams.

Dependencies: reportlab and PyMuPDF (fitz). No browser or network is required.
Run from any directory: python path/to/analysis/scripts/build_report.py
"""
from pathlib import Path
from io import BytesIO
import html
import os
import re
import fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviewed-report.pdf"
WIDTH = A4[0] - 84
INK, TEAL, NAVY = "#263645", "#087f83", "#183750"
FONT_DIR = Path(os.environ.get("REPORT_FONT_DIR", "/usr/share/fonts/truetype/dejavu"))
NORMAL, BOLD, MONO = "Helvetica", "Helvetica-Bold", "Courier"
if all((FONT_DIR / name).exists() for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSansMono.ttf")):
    for name, filename in (("ReportSans", "DejaVuSans.ttf"), ("ReportSans-Bold", "DejaVuSans-Bold.ttf"), ("ReportMono", "DejaVuSansMono.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
    NORMAL, BOLD, MONO = "ReportSans", "ReportSans-Bold", "ReportMono"
pdfmetrics.registerFontFamily(NORMAL, normal=NORMAL, bold=BOLD, italic=NORMAL, boldItalic=BOLD)

styles = getSampleStyleSheet()
for name, size, leading, options in [
    ("TitleR", 25, 30, dict(fontName=BOLD, textColor=colors.HexColor(NAVY), spaceAfter=16)),
    ("H1R", 18, 23, dict(fontName=BOLD, textColor=colors.HexColor(NAVY), spaceAfter=12, keepWithNext=True)),
    ("H2R", 12, 16, dict(fontName=BOLD, textColor=colors.HexColor(NAVY), spaceBefore=12, spaceAfter=7, keepWithNext=True)),
    ("BodyR", 9.5, 13.6, dict(spaceAfter=8, allowWidows=0, allowOrphans=0)),
    ("SmallR", 8.3, 11.6, dict(textColor=colors.HexColor("#53677c"), spaceAfter=7)),
    ("CellR", 8.4, 11.7, dict(spaceAfter=0)),
    ("HeaderR", 8.4, 11.7, dict(fontName=BOLD, textColor=colors.white)),
]:
    base = dict(fontName=NORMAL, textColor=colors.HexColor(INK))
    base.update(options)
    styles.add(ParagraphStyle(name=name, fontSize=size, leading=leading, **base))

source = (ROOT / "report.md").read_text()
references = dict(re.findall(r'^\[(S\d+)\]:\s+(\S+)', source, re.M))


def inline(value):
    value = html.escape(value)
    value = re.sub(r'`([^`]+)`', lambda m: f'<font name="{MONO}">{m.group(1)}</font>', value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', value)
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<link href="{m.group(2)}" color="{TEAL}">{m.group(1)}</link>', value)
    value = re.sub(r' ?\[(S\d+)\]', lambda m: f'&#160;<link href="{references[m.group(1)]}" color="{TEAL}">[{m.group(1)}]</link>', value)
    return value.replace("\\|", "|")


def paragraph(value, style="BodyR"):
    return Paragraph(inline(value), styles[style])


def table(lines):
    rows = [[x.strip() for x in re.split(r'(?<!\\)\|', line.strip())[1:-1]] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r':?-+:?', col) for col in row)]
    columns = len(rows[0])
    if columns == 2:
        ratios = [0.10, 0.90] if rows[0][0] == "ID" else [0.30, 0.70]
    elif columns == 3:
        ratios = [0.23, 0.39, 0.38]
    else:
        ratios = [1 / columns] * columns
    data = [[paragraph(cell, "HeaderR" if n == 0 else "CellR") for cell in row] for n, row in enumerate(rows)]
    result = Table(data, colWidths=[WIDTH * r for r in ratios], repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6f8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 1), (-1, -1), .3, colors.HexColor("#d8e1e8")),
    ]))
    return result


story, pending, in_table = [], [], []


def flush():
    if pending:
        story.append(paragraph(" ".join(pending)))
        pending.clear()
    if in_table:
        story.append(table(in_table))
        story.append(Spacer(1, 9))
        in_table.clear()


for line in source.splitlines():
    if re.match(r'^\[S\d+\]:', line):
        continue
    if line.startswith("|"):
        if pending:
            flush()
        in_table.append(line)
        continue
    if not line.strip():
        flush()
        continue
    flush()
    if line.startswith("# "):
        story.append(paragraph(line[2:], "TitleR"))
    elif line.startswith("## "):
        story.append(PageBreak() if line.startswith("## 2.") else CondPageBreak(205))
        story.append(Spacer(1, 12))
        story.append(paragraph(line[3:], "H1R"))
    elif line.startswith("### "):
        story.append(paragraph(line[4:], "H2R"))
    elif line.startswith("!["):
        relative = re.search(r'\]\(([^)]+)\)', line).group(1)
        svg = fitz.open(ROOT / relative)
        pix = svg[0].get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
        data = BytesIO(pix.tobytes("png"))
        image = Image(data)
        scale = min(WIDTH / image.imageWidth, 470 / image.imageHeight)
        image.drawWidth = image.imageWidth * scale
        image.drawHeight = image.imageHeight * scale
        story.extend([image, Spacer(1, 9)])
        svg.close()
    elif line.startswith("> "):
        note = Table([[paragraph(line[2:])]], colWidths=[WIDTH])
        note.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eaf5f4")), ("BOX", (0, 0), (-1, -1), .5, colors.HexColor("#b7d6d3")), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8)]))
        story.extend([note, Spacer(1, 9)])
    elif line.startswith("[Editable Mermaid"):
        story.append(paragraph(line, "SmallR"))
    else:
        pending.append(line)
flush()


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d8e1e8"))
    canvas.line(42, 35, A4[0] - 42, 35)
    canvas.setFont(NORMAL, 7.3)
    canvas.setFillColor(colors.HexColor("#53677c"))
    canvas.drawString(42, 23, "AWS RESILIENCE HUB / REVIEWED OPERATOR UI DATA MODEL")
    canvas.drawRightString(A4[0] - 42, 23, f"5 NOV 2026 | {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=39, bottomMargin=47,
    title="AWS Resilience Hub: Reviewed Operator UI Data Model", author="OpenAI", subject="Official v2 API analysis and reviewed entity relationships")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
