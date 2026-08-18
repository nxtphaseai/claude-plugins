#!/usr/bin/env python3
"""Zet een Markdown-bronbestand om naar een Word-document in de huisstijl van Nxt Phase AI.

Alleen de standaardbibliotheek. Geen pip install, geen pandoc, geen Word nodig.

    python build_docx.py bron.md -o "Technische documentatie.docx"

Het bronbestand begint met front matter:

    ---
    klant: Voorbeeld Groep
    project: Analyse tool en Routing tool
    document: Technische documentatie
    datum: 4 augustus 2026
    ---

De voorpagina en de inhoudsopgave worden hieruit opgebouwd. Zet ze niet zelf in de
Markdown.

Ondersteunde Markdown: koppen (#, ##, ###), alinea's, opsommingen (-, *) en genummerde
lijsten, tabellen met een koprij, codeblokken met ```, aandachtsblokken met >,
afbeeldingen met ![bijschrift](pad), en inline **vet**, *cursief*, `code` en
[link](url).

Alle opmaak loopt via Word-stijlen, zodat de klant het document echt kan bewerken.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import struct
import sys
import zipfile
from xml.etree import ElementTree
from xml.sax.saxutils import escape as xml_escape

# ---------------------------------------------------------------------------
# Huisstijl
# ---------------------------------------------------------------------------

SIGNAL_GREEN = "3E9B5D"
GREEN_DEEP = "2A6B3F"
OFF_BLACK = "090909"
STONE = "9B9590"
CREAM = "F5F0E8"
CREAM_LIGHT = "FAF6F2"
HAIRLINE = "D9D9D9"

FONT_DISPLAY = "PP Editorial New"
FONT_BODY = "Switzer Medium"
FONT_MONO = "Consolas"

# A4 staand, marges 2,5 cm. Alles in twips (1/1440 inch).
PAGE_W = 11906
PAGE_H = 16838
MARGIN = 1417
CONTENT_W = PAGE_W - 2 * MARGIN  # 9072

EMU_PER_TWIP = 635
EMU_PER_PIXEL = 9525  # bij 96 dpi

LOGO_W_EMU = 1408736
LOGO_H_EMU = 197223

MAANDEN = [
    "januari", "februari", "maart", "april", "mei", "juni",
    "juli", "augustus", "september", "oktober", "november", "december",
]

# ---------------------------------------------------------------------------
# Hulpjes
# ---------------------------------------------------------------------------


def esc(text: str) -> str:
    return xml_escape(text, {'"': "&quot;"})


def nl_datum(d: datetime.date) -> str:
    return f"{d.day} {MAANDEN[d.month - 1]} {d.year}"


def rfonts(name: str) -> str:
    return f'<w:rFonts w:ascii="{esc(name)}" w:hAnsi="{esc(name)}" w:cs="{esc(name)}"/>'


class BuildError(Exception):
    pass


# ---------------------------------------------------------------------------
# Afbeeldingen: afmetingen uit de bytes lezen, zonder Pillow
# ---------------------------------------------------------------------------


def png_size(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if data[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def jpeg_size(data: bytes):
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    n = len(data)
    while i < n - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > n:
            break
        seglen = struct.unpack(">H", data[i:i + 2])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 3:i + 7])
            return w, h
        i += seglen
    return None


def gif_size(data: bytes):
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    w, h = struct.unpack("<HH", data[6:10])
    return w, h


def image_size_px(data: bytes):
    for fn in (png_size, jpeg_size, gif_size):
        size = fn(data)
        if size:
            return size
    return None


IMAGE_CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}


# ---------------------------------------------------------------------------
# Inline opmaak
# ---------------------------------------------------------------------------

INLINE_RE = re.compile(
    r"(?P<codefence>`+)(?P<code>.+?)(?P=codefence)"
    r"|!\[(?P<ialt>[^\]]*)\]\((?P<isrc>[^)\s]+)\)"
    r"|\[(?P<ltext>[^\]]*)\]\((?P<lurl>[^)\s]+)\)"
    r"|\*\*(?P<bold>[^*]+(?:\*(?!\*)[^*]*)*)\*\*"
    r"|(?<![*\w])\*(?P<ital>[^*\n]+?)\*(?!\w)"
    r"|(?<![_\w])_(?P<ital2>[^_\n]+?)_(?!\w)",
    re.S,
)


class Run:
    __slots__ = ("text", "bold", "italic", "code", "url")

    def __init__(self, text, bold=False, italic=False, code=False, url=None):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.code = code
        self.url = url


def parse_inline(text: str, bold=False, italic=False) -> list:
    """Splits een tekstregel in runs met opmaak."""
    runs = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            runs.append(Run(text[pos:m.start()], bold, italic))
        if m.group("code") is not None:
            runs.append(Run(m.group("code"), bold, italic, code=True))
        elif m.group("isrc") is not None:
            # Een inline afbeelding midden in een alinea ondersteunen we niet;
            # toon de alt-tekst zodat er niets stilzwijgend verdwijnt.
            runs.append(Run(m.group("ialt") or m.group("isrc"), bold, italic))
        elif m.group("lurl") is not None:
            inner = parse_inline(m.group("ltext"), bold, italic)
            if not inner:
                inner = [Run(m.group("lurl"), bold, italic)]
            for r in inner:
                r.url = m.group("lurl")
            runs.extend(inner)
        elif m.group("bold") is not None:
            runs.extend(parse_inline(m.group("bold"), True, italic))
        elif m.group("ital") is not None:
            runs.extend(parse_inline(m.group("ital"), bold, True))
        elif m.group("ital2") is not None:
            runs.extend(parse_inline(m.group("ital2"), bold, True))
        pos = m.end()
    if pos < len(text):
        runs.append(Run(text[pos:], bold, italic))
    return [r for r in runs if r.text != ""]


# ---------------------------------------------------------------------------
# Blokstructuur
# ---------------------------------------------------------------------------


class Block:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
ORDERED_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)\s*(\S*)\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
HR_RE = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")


def split_row(line: str) -> list:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def parse_frontmatter(src: str):
    m = FRONTMATTER_RE.match(src)
    if not m:
        return {}, src
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip().lower()] = value
    return meta, src[m.end():]


def parse_blocks(body: str) -> list:
    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0] * 3
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith(marker):
                code_lines.append(lines[i])
                i += 1
            i += 1  # sluitende fence
            while code_lines and not code_lines[-1].strip():
                code_lines.pop()
            blocks.append(Block("code", lines=code_lines, taal=fence.group(2)))
            continue

        if HR_RE.match(line):
            blocks.append(Block("hr"))
            i += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = min(len(heading.group(1)), 3)
            blocks.append(Block("heading", level=level, text=heading.group(2).strip()))
            i += 1
            continue

        image = IMAGE_RE.match(line)
        if image:
            blocks.append(Block("image", alt=image.group(1).strip(), src=image.group(2)))
            i += 1
            continue

        # Tabel: een regel met | gevolgd door een scheidingsregel.
        if "|" in line and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]) and "|" in lines[i + 1]:
            header = split_row(line)
            aligns = []
            for cell in split_row(lines[i + 1]):
                left = cell.startswith(":")
                right = cell.endswith(":")
                aligns.append("center" if left and right else "right" if right else "left")
            i += 2
            rows = []
            while i < n and lines[i].strip() and "|" in lines[i]:
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append(Block("table", header=header, aligns=aligns, rows=rows))
            continue

        if line.lstrip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(Block("quote", lines=[l for l in quote_lines if l.strip()]))
            continue

        bullet = BULLET_RE.match(line)
        ordered = ORDERED_RE.match(line)
        if bullet or ordered:
            ordered_list = ordered is not None
            items = []
            while i < n:
                b = BULLET_RE.match(lines[i])
                o = ORDERED_RE.match(lines[i])
                if b and not ordered_list:
                    indent, text = b.group(1), b.group(2)
                elif o and ordered_list:
                    indent, text = o.group(1), o.group(3)
                elif lines[i].strip() and items and lines[i].startswith(("  ", "\t")) \
                        and not b and not o:
                    items[-1][1] += " " + lines[i].strip()
                    i += 1
                    continue
                else:
                    break
                level = min(len(indent.replace("\t", "    ")) // 2, 2)
                items.append([level, text.strip()])
                i += 1
            blocks.append(Block("list", ordered=ordered_list, items=items))
            continue

        # Gewone alinea: loopt door tot een lege regel of een ander blok.
        para = [line.strip()]
        i += 1
        while i < n and lines[i].strip():
            nxt = lines[i]
            if (HEADING_RE.match(nxt) or BULLET_RE.match(nxt) or ORDERED_RE.match(nxt)
                    or FENCE_RE.match(nxt) or IMAGE_RE.match(nxt) or HR_RE.match(nxt)
                    or nxt.lstrip().startswith(">")
                    or ("|" in nxt and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]))):
                break
            para.append(nxt.strip())
            i += 1
        blocks.append(Block("paragraph", text=" ".join(para)))

    return blocks


# ---------------------------------------------------------------------------
# XML-onderdelen
# ---------------------------------------------------------------------------

W_NS = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
)

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def borders(color: str, sz: int = 4) -> str:
    sides = ("top", "left", "bottom", "right", "insideH", "insideV")
    return "<w:tblBorders>" + "".join(
        f'<w:{s} w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>' for s in sides
    ) + "</w:tblBorders>"


def build_styles() -> str:
    body_run = f'{rfonts(FONT_BODY)}<w:color w:val="{OFF_BLACK}"/><w:sz w:val="21"/><w:szCs w:val="21"/>'
    parts = [XML_DECL, f"<w:styles {W_NS}>"]

    parts.append(
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        f'{rfonts(FONT_BODY)}<w:color w:val="{OFF_BLACK}"/>'
        '<w:sz w:val="21"/><w:szCs w:val="21"/>'
        '<w:lang w:val="nl-NL" w:eastAsia="nl-NL" w:bidi="ar-SA"/>'
        "</w:rPr></w:rPrDefault>"
        "<w:pPrDefault><w:pPr>"
        '<w:spacing w:before="0" w:after="140" w:line="264" w:lineRule="auto"/>'
        "</w:pPr></w:pPrDefault></w:docDefaults>"
    )

    def style(sid, name, typ="paragraph", based=None, nxt=None, link=None,
              ppr="", rpr="", extra="", qformat=True, priority=None):
        out = [f'<w:style w:type="{typ}" w:styleId="{sid}">', f'<w:name w:val="{esc(name)}"/>']
        if based:
            out.append(f'<w:basedOn w:val="{based}"/>')
        if nxt:
            out.append(f'<w:next w:val="{nxt}"/>')
        if link:
            out.append(f'<w:link w:val="{link}"/>')
        if priority is not None:
            out.append(f'<w:uiPriority w:val="{priority}"/>')
        if qformat:
            out.append("<w:qFormat/>")
        if ppr:
            out.append(f"<w:pPr>{ppr}</w:pPr>")
        if rpr:
            out.append(f"<w:rPr>{rpr}</w:rPr>")
        out.append(extra)
        out.append("</w:style>")
        return "".join(out)

    # Basis. Bewust geen kleur en geen uitlijning: die staan in docDefaults, zodat de
    # tabelstijl de koprij nog wit en gecentreerd kan maken. Een alineastijl wint van
    # een tabelstijl, dus alles wat hier staat blokkeert de opmaak van de koprij.
    parts.append(style(
        "Standaard", "Normal",
        ppr='<w:spacing w:before="0" w:after="140" w:line="264" w:lineRule="auto"/>',
        rpr=f"{rfonts(FONT_BODY)}", priority=0,
    ))
    parts.append('<w:style w:type="character" w:default="1" w:styleId="Standaardalinea-lettertype">'
                 '<w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/>'
                 "<w:semiHidden/><w:unhideWhenUsed/></w:style>")
    parts.append('<w:style w:type="table" w:default="1" w:styleId="Standaardtabel">'
                 '<w:name w:val="Normal Table"/><w:uiPriority w:val="99"/>'
                 "<w:semiHidden/><w:unhideWhenUsed/>"
                 '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar>'
                 '<w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
                 '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
                 "</w:tblCellMar></w:tblPr></w:style>")
    parts.append('<w:style w:type="numbering" w:default="1" w:styleId="Geenlijst">'
                 '<w:name w:val="No List"/><w:uiPriority w:val="99"/>'
                 "<w:semiHidden/><w:unhideWhenUsed/></w:style>")

    # Koppen
    parts.append(style(
        "Kop1", "heading 1", based="Standaard", nxt="Standaard", link="Kop1Char", priority=9,
        ppr='<w:keepNext/><w:keepLines/><w:pageBreakBefore/>'
            '<w:spacing w:before="0" w:after="240" w:line="240" w:lineRule="auto"/>'
            '<w:outlineLvl w:val="0"/>',
        rpr=f'{rfonts(FONT_DISPLAY)}<w:b/><w:bCs/><w:color w:val="{SIGNAL_GREEN}"/>'
            '<w:sz w:val="34"/><w:szCs w:val="34"/>',
    ))
    parts.append(style(
        "Kop2", "heading 2", based="Standaard", nxt="Standaard", link="Kop2Char", priority=9,
        ppr='<w:keepNext/><w:keepLines/>'
            '<w:spacing w:before="320" w:after="100" w:line="240" w:lineRule="auto"/>'
            '<w:outlineLvl w:val="1"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:b/><w:bCs/><w:color w:val="{OFF_BLACK}"/>'
            '<w:sz w:val="24"/><w:szCs w:val="24"/>',
    ))
    parts.append(style(
        "Kop3", "heading 3", based="Standaard", nxt="Standaard", link="Kop3Char", priority=9,
        ppr='<w:keepNext/><w:keepLines/>'
            '<w:spacing w:before="240" w:after="80" w:line="240" w:lineRule="auto"/>'
            '<w:outlineLvl w:val="2"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:b/><w:bCs/><w:color w:val="{OFF_BLACK}"/>'
            '<w:sz w:val="21"/><w:szCs w:val="21"/>',
    ))
    for lvl, font, color, sz in (
        (1, FONT_DISPLAY, SIGNAL_GREEN, 34), (2, FONT_BODY, OFF_BLACK, 24), (3, FONT_BODY, OFF_BLACK, 21)
    ):
        parts.append(
            f'<w:style w:type="character" w:customStyle="1" w:styleId="Kop{lvl}Char">'
            f'<w:name w:val="Kop {lvl} Char"/><w:link w:val="Kop{lvl}"/><w:uiPriority w:val="9"/>'
            f'<w:rPr>{rfonts(font)}<w:b/><w:bCs/><w:color w:val="{color}"/>'
            f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr></w:style>'
        )

    # Geen afstand, en de drie regels van de voorpagina
    parts.append(style(
        "Geenafstand", "No Spacing", based="Standaard", priority=1,
        ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
    ))
    parts.append(style(
        "Voorpaginaklant", "Voorpagina klant", based="Geenafstand", nxt="Standaard",
        ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_DISPLAY)}<w:color w:val="{OFF_BLACK}"/>'
            '<w:sz w:val="28"/><w:szCs w:val="28"/>',
    ))
    parts.append(style(
        "Voorpaginatitel", "Voorpagina titel", based="Geenafstand", nxt="Standaard",
        ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_DISPLAY)}<w:color w:val="{OFF_BLACK}"/>'
            '<w:sz w:val="36"/><w:szCs w:val="36"/>',
    ))
    parts.append(style(
        "Voorpaginaafzender", "Voorpagina afzender", based="Geenafstand", nxt="Standaard",
        ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:color w:val="{OFF_BLACK}"/>'
            '<w:sz w:val="24"/><w:szCs w:val="24"/>',
    ))

    # Inhoudsopgave
    parts.append(style(
        "KopvanInhoudsopgave", "TOC Heading", based="Standaard", nxt="Standaard", priority=39,
        ppr='<w:keepNext/><w:keepLines/>'
            '<w:spacing w:before="480" w:after="200" w:line="240" w:lineRule="auto"/>'
            '<w:outlineLvl w:val="9"/>',
        rpr=f'{rfonts(FONT_DISPLAY)}<w:b/><w:bCs/><w:color w:val="{SIGNAL_GREEN}"/>'
            '<w:sz w:val="30"/><w:szCs w:val="30"/>',
    ))
    parts.append(style(
        "Inhopg1", "toc 1", based="Standaard", nxt="Standaard", priority=39, qformat=False,
        ppr='<w:spacing w:before="120" w:after="0" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:sz w:val="22"/><w:szCs w:val="22"/>',
    ))
    parts.append(style(
        "Inhopg2", "toc 2", based="Standaard", nxt="Standaard", priority=39, qformat=False,
        ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="397"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:color w:val="{OFF_BLACK}"/><w:sz w:val="19"/><w:szCs w:val="19"/>',
    ))

    # Lijsten
    parts.append(style(
        "Lijstalinea", "List Paragraph", based="Standaard", priority=34,
        ppr='<w:spacing w:before="0" w:after="60" w:line="264" w:lineRule="auto"/>'
            '<w:ind w:left="397" w:hanging="284"/><w:contextualSpacing/>',
    ))

    # Codeblok en inline code
    parts.append(style(
        "Codeblok", "Codeblok", based="Standaard", nxt="Standaard",
        ppr='<w:keepLines/>'
            '<w:spacing w:before="120" w:after="180" w:line="240" w:lineRule="auto"/>'
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{SIGNAL_GREEN}"/></w:pBdr>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="{CREAM}"/>'
            '<w:ind w:left="170" w:right="170"/>',
        rpr=f'{rfonts(FONT_MONO)}<w:color w:val="{OFF_BLACK}"/><w:sz w:val="18"/><w:szCs w:val="18"/>',
    ))
    parts.append(
        '<w:style w:type="character" w:customStyle="1" w:styleId="Codetekst">'
        '<w:name w:val="Codetekst"/><w:uiPriority w:val="1"/><w:qFormat/>'
        f'<w:rPr>{rfonts(FONT_MONO)}<w:color w:val="{GREEN_DEEP}"/>'
        f'<w:sz w:val="19"/><w:szCs w:val="19"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{CREAM}"/></w:rPr></w:style>'
    )

    # Aandachtsblok en bijschrift
    parts.append(style(
        "Aandachtsblok", "Aandachtsblok", based="Standaard", nxt="Standaard",
        ppr='<w:spacing w:before="140" w:after="180" w:line="264" w:lineRule="auto"/>'
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="10" w:color="{SIGNAL_GREEN}"/></w:pBdr>'
            '<w:ind w:left="227"/>',
    ))
    parts.append(style(
        "Bijschrift", "caption", based="Standaard", nxt="Standaard", priority=35,
        ppr='<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:i/><w:iCs/><w:color w:val="{STONE}"/>'
            '<w:sz w:val="18"/><w:szCs w:val="18"/>',
    ))

    # Voettekst
    parts.append(style(
        "Voettekst", "footer", based="Standaard", link="VoettekstChar", priority=99, qformat=False,
        ppr='<w:tabs>'
            f'<w:tab w:val="center" w:pos="{CONTENT_W // 2}"/>'
            f'<w:tab w:val="right" w:pos="{CONTENT_W}"/></w:tabs>'
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
        rpr=f'{rfonts(FONT_BODY)}<w:color w:val="{STONE}"/><w:sz w:val="18"/><w:szCs w:val="18"/>',
    ))
    parts.append(
        '<w:style w:type="character" w:customStyle="1" w:styleId="VoettekstChar">'
        '<w:name w:val="Voettekst Char"/><w:link w:val="Voettekst"/><w:uiPriority w:val="99"/>'
        f'<w:rPr>{rfonts(FONT_BODY)}<w:color w:val="{STONE}"/>'
        '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
    )
    parts.append(
        '<w:style w:type="character" w:styleId="Paginanummer">'
        '<w:name w:val="page number"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/>'
        f'<w:rPr>{rfonts(FONT_BODY)}<w:color w:val="{STONE}"/>'
        '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
    )

    # Tekenstijlen
    parts.append(
        '<w:style w:type="character" w:styleId="Hyperlink">'
        '<w:name w:val="Hyperlink"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
        f'<w:rPr><w:color w:val="{SIGNAL_GREEN}"/><w:u w:val="single"/></w:rPr></w:style>'
    )
    parts.append(
        '<w:style w:type="character" w:styleId="Zwaar">'
        '<w:name w:val="Strong"/><w:uiPriority w:val="22"/><w:qFormat/>'
        "<w:rPr><w:b/><w:bCs/></w:rPr></w:style>"
    )
    parts.append(
        '<w:style w:type="character" w:styleId="Nadruk">'
        '<w:name w:val="Emphasis"/><w:uiPriority w:val="20"/><w:qFormat/>'
        "<w:rPr><w:i/><w:iCs/></w:rPr></w:style>"
    )

    # Tabelstijl
    parts.append(
        '<w:style w:type="table" w:styleId="Nxtphasetabel">'
        '<w:name w:val="Nxt Phase tabel"/><w:basedOn w:val="Standaardtabel"/>'
        '<w:uiPriority w:val="99"/><w:qFormat/>'
        '<w:pPr><w:spacing w:before="40" w:after="40" w:line="252" w:lineRule="auto"/></w:pPr>'
        f'<w:rPr>{rfonts(FONT_BODY)}<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>'
        "<w:tblPr>"
        + borders(HAIRLINE)
        + '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
          '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>"
        '<w:tblStylePr w:type="firstRow">'
        f'<w:rPr><w:b/><w:bCs/><w:color w:val="{CREAM_LIGHT}"/></w:rPr>'
        f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{SIGNAL_GREEN}"/>'
        '<w:vAlign w:val="center"/></w:tcPr>'
        "</w:tblStylePr>"
        "</w:style>"
    )

    parts.append("</w:styles>")
    return "".join(parts)


def build_numbering(ordered_count: int) -> str:
    bullets = ["", "o", ""]
    fonts = ["Symbol", "Courier New", "Wingdings"]
    chars = ["", "o", ""]
    lvls = []
    for i in range(3):
        lvls.append(
            f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
            f'<w:lvlText w:val="{esc(chars[i])}"/><w:lvlJc w:val="left"/>'
            f'<w:pPr><w:ind w:left="{397 + i * 340}" w:hanging="284"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{fonts[i]}" w:hAnsi="{fonts[i]}" w:hint="default"/></w:rPr>'
            "</w:lvl>"
        )
    abstract_bullet = (
        '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
        + "".join(lvls) + "</w:abstractNum>"
    )

    fmts = ["decimal", "lowerLetter", "lowerRoman"]
    texts = ["%1.", "%2.", "%3."]
    lvls = []
    for i in range(3):
        lvls.append(
            f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="{fmts[i]}"/>'
            f'<w:lvlText w:val="{texts[i]}"/><w:lvlJc w:val="left"/>'
            f'<w:pPr><w:ind w:left="{397 + i * 340}" w:hanging="284"/></w:pPr>'
            "</w:lvl>"
        )
    abstract_ordered = (
        '<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>'
        + "".join(lvls) + "</w:abstractNum>"
    )

    nums = ['<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>']
    for k in range(ordered_count):
        nums.append(
            f'<w:num w:numId="{k + 2}"><w:abstractNumId w:val="1"/>'
            '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride>'
            '<w:lvlOverride w:ilvl="1"><w:startOverride w:val="1"/></w:lvlOverride>'
            '<w:lvlOverride w:ilvl="2"><w:startOverride w:val="1"/></w:lvlOverride>'
            "</w:num>"
        )

    return XML_DECL + f"<w:numbering {W_NS}>" + abstract_bullet + abstract_ordered + "".join(nums) + "</w:numbering>"


def build_settings() -> str:
    return (
        XML_DECL + f"<w:settings {W_NS}>"
        '<w:zoom w:percent="100"/>'
        "<w:defaultTabStop w:val=\"709\"/>"
        "<w:characterSpacingControl w:val=\"doNotCompress\"/>"
        "<w:compat>"
        '<w:compatSetting w:name="compatibilityMode" '
        'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
        "</w:compat>"
        '<w:themeFontLang w:val="nl-NL"/>'
        "</w:settings>"
    )


def build_font_table() -> str:
    fonts = [
        (FONT_BODY, "swiss", "variable"),
        (FONT_DISPLAY, "roman", "variable"),
        (FONT_MONO, "modern", "fixed"),
        ("Symbol", "roman", "fixed"),
        ("Courier New", "modern", "fixed"),
        ("Wingdings", "decorative", "fixed"),
    ]
    out = [XML_DECL, f"<w:fonts {W_NS}>"]
    for name, family, pitch in fonts:
        out.append(
            f'<w:font w:name="{esc(name)}"><w:family w:val="{family}"/>'
            f'<w:pitch w:val="{pitch}"/></w:font>'
        )
    out.append("</w:fonts>")
    return "".join(out)


def build_theme() -> str:
    """Minimaal thema met de merkkleuren, zodat Word niet naar zijn eigen blauw terugvalt."""
    accents = [SIGNAL_GREEN, GREEN_DEEP, STONE, "E86B10", "86C0D5", "F7DFDE"]
    accent_xml = "".join(
        f'<a:accent{i + 1}><a:srgbClr val="{c}"/></a:accent{i + 1}>' for i, c in enumerate(accents)
    )
    return (
        XML_DECL
        + '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'name="Nxt Phase AI"><a:themeElements>'
          '<a:clrScheme name="Nxt Phase AI">'
          '<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
          f'<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>'
          f'<a:dk2><a:srgbClr val="{OFF_BLACK}"/></a:dk2>'
          f'<a:lt2><a:srgbClr val="{CREAM}"/></a:lt2>'
        + accent_xml
        + f'<a:hlink><a:srgbClr val="{SIGNAL_GREEN}"/></a:hlink>'
          f'<a:folHlink><a:srgbClr val="{GREEN_DEEP}"/></a:folHlink>'
          "</a:clrScheme>"
          f'<a:fontScheme name="Nxt Phase AI">'
          f'<a:majorFont><a:latin typeface="{esc(FONT_DISPLAY)}"/><a:ea typeface=""/>'
          '<a:cs typeface=""/></a:majorFont>'
          f'<a:minorFont><a:latin typeface="{esc(FONT_BODY)}"/><a:ea typeface=""/>'
          '<a:cs typeface=""/></a:minorFont>'
          "</a:fontScheme>"
          '<a:fmtScheme name="Nxt Phase AI">'
          '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
          '<a:lnStyleLst>'
          '<a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          "</a:lnStyleLst>"
          '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
          '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
          "</a:fmtScheme>"
          "</a:themeElements></a:theme>"
    )


def build_footer(has_logo: bool) -> str:
    page_field = (
        '<w:r><w:rPr><w:rStyle w:val="Paginanummer"/></w:rPr>'
        '<w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:rPr><w:rStyle w:val="Paginanummer"/></w:rPr>'
        '<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
        '<w:r><w:rPr><w:rStyle w:val="Paginanummer"/></w:rPr>'
        '<w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:rPr><w:rStyle w:val="Paginanummer"/><w:noProof/></w:rPr><w:t>1</w:t></w:r>'
        '<w:r><w:rPr><w:rStyle w:val="Paginanummer"/></w:rPr>'
        '<w:fldChar w:fldCharType="end"/></w:r>'
    )
    logo = ""
    if has_logo:
        # Twee tabs: de eerste springt naar de middentab van de voettekststijl,
        # de tweede naar de rechtertab. Met één tab landt het logo in het midden.
        logo = (
            "<w:r><w:tab/><w:tab/></w:r><w:r><w:rPr><w:noProof/></w:rPr><w:drawing>"
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{LOGO_W_EMU}" cy="{LOGO_H_EMU}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:docPr id="1001" name="Logo Nxt Phase AI" descr="Logo van Nxt Phase AI"/>'
            "<wp:cNvGraphicFramePr>"
            '<a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            "<a:graphic><a:graphicData "
            'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            "<pic:pic><pic:nvPicPr>"
            '<pic:cNvPr id="1001" name="Logo Nxt Phase AI"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="rIdLogo"/><a:stretch><a:fillRect/></a:stretch>'
            "</pic:blipFill>"
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
            f'<a:ext cx="{LOGO_W_EMU}" cy="{LOGO_H_EMU}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
        )
    return (
        XML_DECL + f"<w:ftr {W_NS}>"
        '<w:p><w:pPr><w:pStyle w:val="Voettekst"/></w:pPr>'
        + page_field + logo +
        "</w:p></w:ftr>"
    )


def build_core_props(meta: dict) -> str:
    titel = f"{meta.get('project', '')} | {meta.get('document', '')}".strip(" |")
    stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        XML_DECL
        + '<cp:coreProperties '
          'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
          'xmlns:dc="http://purl.org/dc/elements/1.1/" '
          'xmlns:dcterms="http://purl.org/dc/terms/" '
          'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
          f"<dc:title>{esc(titel)}</dc:title>"
          f"<dc:subject>{esc(meta.get('klant', ''))}</dc:subject>"
          "<dc:creator>Nxt Phase AI</dc:creator>"
          "<cp:lastModifiedBy>Nxt Phase AI</cp:lastModifiedBy>"
          f'<dcterms:created xsi:type="dcterms:W3CDTF">{stamp}</dcterms:created>'
          f'<dcterms:modified xsi:type="dcterms:W3CDTF">{stamp}</dcterms:modified>'
          "</cp:coreProperties>"
    )


def build_app_props() -> str:
    return (
        XML_DECL
        + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
          'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
          "<Application>nxtphase-documentatie</Application>"
          "<Company>Nxt Phase AI</Company>"
          "</Properties>"
    )


# ---------------------------------------------------------------------------
# Document opbouwen
# ---------------------------------------------------------------------------


class Document:
    def __init__(self, meta: dict, assets_dir: str):
        self.meta = meta
        self.assets_dir = assets_dir
        self.body = []
        self.rels = []          # (id, type, target, mode)
        self.media = {}         # naam in het pakket -> bytes
        self.headings = []      # (level, tekst, bookmark)
        self.ordered_lists = 0
        self._rel_seq = 0
        self._bm_seq = 0
        self._img_seq = 0
        self._missing_images = []

    # -- relaties ---------------------------------------------------------
    def add_rel(self, rtype: str, target: str, mode: str = None) -> str:
        self._rel_seq += 1
        rid = f"rId{self._rel_seq}"
        self.rels.append((rid, rtype, target, mode))
        return rid

    def add_hyperlink(self, url: str) -> str:
        return self.add_rel(
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            url, "External",
        )

    def add_image(self, path: str):
        full = path if os.path.isabs(path) else os.path.join(self.assets_dir, path)
        if not os.path.isfile(full):
            self._missing_images.append(path)
            return None
        ext = os.path.splitext(full)[1].lower()
        if ext not in IMAGE_CONTENT_TYPES:
            self._missing_images.append(f"{path} (niet-ondersteund bestandstype)")
            return None
        data = open(full, "rb").read()
        size = image_size_px(data)
        if not size:
            self._missing_images.append(f"{path} (afmetingen niet leesbaar)")
            return None
        self._img_seq += 1
        name = f"afbeelding{self._img_seq}{ext}"
        self.media[name] = data
        rid = self.add_rel(
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            f"media/{name}",
        )
        return rid, size, ext

    def next_bookmark(self) -> str:
        self._bm_seq += 1
        return f"_Toc9000{self._bm_seq:03d}"

    # -- runs -------------------------------------------------------------
    def render_runs(self, runs: list) -> str:
        out = []
        for run in runs:
            rpr = []
            if run.code:
                rpr.append('<w:rStyle w:val="Codetekst"/>')
            if run.url:
                rpr.append('<w:rStyle w:val="Hyperlink"/>')
            if run.bold:
                rpr.append("<w:b/><w:bCs/>")
            if run.italic:
                rpr.append("<w:i/><w:iCs/>")
            rpr_xml = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
            xml = f'<w:r>{rpr_xml}<w:t xml:space="preserve">{esc(run.text)}</w:t></w:r>'
            if run.url:
                if run.url.startswith("#"):
                    xml = f'<w:hyperlink w:anchor="{esc(run.url[1:])}" w:history="1">{xml}</w:hyperlink>'
                else:
                    rid = self.add_hyperlink(run.url)
                    xml = f'<w:hyperlink r:id="{rid}" w:history="1">{xml}</w:hyperlink>'
            out.append(xml)
        return "".join(out)

    def para(self, style: str, runs_xml: str, extra_ppr: str = "") -> str:
        ppr = f'<w:pStyle w:val="{style}"/>{extra_ppr}'
        return f"<w:p><w:pPr>{ppr}</w:pPr>{runs_xml}</w:p>"

    def text_para(self, style: str, text: str, extra_ppr: str = "") -> str:
        return self.para(style, self.render_runs(parse_inline(text)), extra_ppr)

    # -- voorpagina en inhoudsopgave --------------------------------------
    def cover(self):
        m = self.meta
        klant = m.get("klant", "")
        project = m.get("project", "")
        document = m.get("document", "")
        datum = m.get("datum") or nl_datum(datetime.date.today())
        afzender = m.get("afzender", "Nxt Phase AI")

        self.body.append(self.para(
            "Voorpaginaklant",
            f'<w:r><w:t xml:space="preserve">{esc(klant)}</w:t></w:r>',
        ))
        self.body.append(self.para("Geenafstand", ""))
        titel_runs = (
            f'<w:r><w:rPr><w:b/><w:bCs/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(project)}</w:t></w:r>'
            f'<w:r><w:t xml:space="preserve"> | </w:t></w:r>'
            f'<w:r><w:rPr><w:color w:val="{SIGNAL_GREEN}"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(document)}</w:t></w:r>'
        )
        self.body.append(self.para("Voorpaginatitel", titel_runs))
        self.body.append(self.para("Geenafstand", ""))
        self.body.append(self.para(
            "Voorpaginaafzender",
            f'<w:r><w:t xml:space="preserve">Opgeleverd door {esc(afzender)} | '
            f'{esc(datum)}</w:t></w:r>',
        ))

    def toc(self):
        self.body.append(self.para(
            "KopvanInhoudsopgave",
            '<w:r><w:t xml:space="preserve">Inhoudsopgave</w:t></w:r>',
        ))
        entries = [(lvl, txt, bm) for lvl, txt, bm in self.headings if lvl <= 2]
        instr = ' TOC \\o "1-2" \\h \\z \\n \\u '
        if not entries:
            self.body.append(
                '<w:p><w:pPr><w:pStyle w:val="Inhopg1"/></w:pPr>'
                '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
                '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
                '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
            )
            return

        out = ["<w:sdt><w:sdtPr><w:docPartObj>"
               '<w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/>'
               "</w:docPartObj></w:sdtPr><w:sdtContent>"]
        for idx, (lvl, txt, bm) in enumerate(entries):
            style = "Inhopg1" if lvl == 1 else "Inhopg2"
            link = (
                f'<w:hyperlink w:anchor="{bm}" w:history="1">'
                f'<w:r><w:rPr><w:rStyle w:val="Hyperlink"/><w:noProof/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(txt)}</w:t></w:r></w:hyperlink>'
            )
            if idx == 0:
                out.append(
                    f'<w:p><w:pPr><w:pStyle w:val="{style}"/>'
                    "<w:rPr><w:noProof/></w:rPr></w:pPr>"
                    '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                    f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
                    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
                    f"{link}</w:p>"
                )
            else:
                out.append(
                    f'<w:p><w:pPr><w:pStyle w:val="{style}"/>'
                    f"<w:rPr><w:noProof/></w:rPr></w:pPr>{link}</w:p>"
                )
        out.append('<w:p><w:pPr><w:pStyle w:val="Inhopg1"/></w:pPr>'
                   '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        out.append("</w:sdtContent></w:sdt>")
        self.body.append("".join(out))

    # -- blokken ----------------------------------------------------------
    def add_heading(self, level: int, text: str, bookmark: str):
        runs = self.render_runs(parse_inline(text))
        bm_id = self._bm_seq
        opening = f'<w:bookmarkStart w:id="{bm_id}" w:name="{bookmark}"/>'
        closing = f'<w:bookmarkEnd w:id="{bm_id}"/>'
        ppr = f'<w:pStyle w:val="Kop{level}"/>'
        self.body.append(f"<w:p><w:pPr>{ppr}</w:pPr>{opening}{runs}{closing}</w:p>")

    def add_list(self, block: Block):
        if block.ordered:
            self.ordered_lists += 1
            num_id = self.ordered_lists + 1
        else:
            num_id = 1
        for level, text in block.items:
            ppr = (
                f'<w:numPr><w:ilvl w:val="{level}"/><w:numId w:val="{num_id}"/></w:numPr>'
                f'<w:ind w:left="{397 + level * 340}" w:hanging="284"/>'
            )
            self.body.append(self.text_para("Lijstalinea", text, ppr))

    def add_code(self, block: Block):
        if not block.lines:
            return
        runs = []
        for idx, line in enumerate(block.lines):
            if idx:
                runs.append("<w:r><w:br/></w:r>")
            runs.append(f'<w:r><w:t xml:space="preserve">{esc(line)}</w:t></w:r>')
        self.body.append(self.para("Codeblok", "".join(runs)))

    def add_quote(self, block: Block):
        for line in block.lines:
            self.body.append(self.text_para("Aandachtsblok", line))

    def add_image_block(self, block: Block):
        result = self.add_image(block.src)
        if not result:
            self.body.append(self.text_para(
                "Bijschrift",
                f"[Afbeelding ontbreekt: {block.src}]",
            ))
            return
        rid, (px_w, px_h), _ext = result
        cx = px_w * EMU_PER_PIXEL
        cy = px_h * EMU_PER_PIXEL
        max_cx = CONTENT_W * EMU_PER_TWIP
        if cx > max_cx:
            cy = int(cy * max_cx / cx)
            cx = max_cx
        self._img_seq_id = getattr(self, "_img_seq_id", 2000) + 1
        drawing = (
            "<w:p><w:pPr><w:pStyle w:val=\"Geenafstand\"/>"
            '<w:spacing w:before="180" w:after="60"/></w:pPr>'
            "<w:r><w:rPr><w:noProof/></w:rPr><w:drawing>"
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{self._img_seq_id}" name="Afbeelding {self._img_seq}" '
            f'descr="{esc(block.alt)}"/>'
            "<wp:cNvGraphicFramePr>"
            '<a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            "<a:graphic><a:graphicData "
            'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f"<pic:pic><pic:nvPicPr><pic:cNvPr id=\"{self._img_seq_id}\" "
            f'name="Afbeelding {self._img_seq}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/>'
            "<a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
        )
        self.body.append(drawing)
        if block.alt:
            self.body.append(self.text_para("Bijschrift", block.alt))

    def add_table(self, block: Block):
        cols = max(len(block.header), max((len(r) for r in block.rows), default=0))
        header = list(block.header) + [""] * (cols - len(block.header))
        aligns = list(block.aligns) + ["left"] * (cols - len(block.aligns))

        # Kolombreedte naar de langste cel, maar gedempt met een macht kleiner dan 1.
        # Zonder demping slurpt een kolom met lange tekst alle ruimte op en gaat een
        # korte kopkolom onnodig afbreken.
        weights = []
        for c in range(cols):
            longest = len(header[c])
            for row in block.rows:
                if c < len(row):
                    longest = max(longest, len(row[c]))
            weights.append(max(longest, 6) ** 0.6)
        total = sum(weights)
        widths = [max(int(CONTENT_W * w / total), 700) for w in weights]
        drift = CONTENT_W - sum(widths)
        widths[-1] += drift

        out = [
            "<w:tbl><w:tblPr>"
            '<w:tblStyle w:val="Nxtphasetabel"/>'
            f'<w:tblW w:w="{CONTENT_W}" w:type="dxa"/>'
            '<w:tblLayout w:type="fixed"/>'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0" '
            'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
            "</w:tblPr><w:tblGrid>"
            + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
            + "</w:tblGrid>"
        ]

        def cell(text, width, align, is_header):
            jc = "" if align == "left" else f'<w:jc w:val="{align}"/>'
            ppr = f'<w:pStyle w:val="Standaard"/><w:spacing w:before="40" w:after="40"/>{jc}'
            runs = self.render_runs(parse_inline(text))
            return (
                f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f"<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p></w:tc>"
            )

        out.append(
            "<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>"
            + "".join(cell(header[c], widths[c], aligns[c], True) for c in range(cols))
            + "</w:tr>"
        )
        for row in block.rows:
            row = list(row) + [""] * (cols - len(row))
            out.append(
                "<w:tr>"
                + "".join(cell(row[c], widths[c], aligns[c], False) for c in range(cols))
                + "</w:tr>"
            )
        out.append("</w:tbl>")
        self.body.append("".join(out))
        # Word wil een alinea na een tabel, anders plakken twee tabellen aan elkaar.
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Standaard"/>'
                         '<w:spacing w:before="0" w:after="0" w:line="120" '
                         'w:lineRule="exact"/></w:pPr></w:p>')

    # -- alles samen ------------------------------------------------------
    def render(self, blocks: list, footer_rid_present: bool) -> str:
        # Eerst de bookmarks vaststellen, zodat de inhoudsopgave klopt.
        marks = {}
        for idx, b in enumerate(blocks):
            if b.kind == "heading" and b.level <= 2:
                bm = self.next_bookmark()
                marks[idx] = bm
                self.headings.append((b.level, b.text, bm))

        self.cover()
        self.toc()

        for idx, b in enumerate(blocks):
            if b.kind == "heading":
                bm = marks.get(idx)
                if bm is None:
                    self._bm_seq += 1
                    bm = f"_Sub9000{self._bm_seq:03d}"
                self.add_heading(b.level, b.text, bm)
            elif b.kind == "paragraph":
                self.body.append(self.text_para("Standaard", b.text))
            elif b.kind == "list":
                self.add_list(b)
            elif b.kind == "table":
                self.add_table(b)
            elif b.kind == "code":
                self.add_code(b)
            elif b.kind == "quote":
                self.add_quote(b)
            elif b.kind == "image":
                self.add_image_block(b)
            elif b.kind == "hr":
                self.body.append(
                    '<w:p><w:pPr><w:pStyle w:val="Standaard"/>'
                    f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" '
                    f'w:color="{HAIRLINE}"/></w:pBdr></w:pPr></w:p>'
                )

        footer_ref = ('<w:footerReference w:type="default" r:id="rIdFooter"/>'
                      if footer_rid_present else "")
        sect = (
            f"<w:sectPr>{footer_ref}"
            f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}" w:orient="portrait"/>'
            f'<w:pgMar w:top="{MARGIN}" w:right="{MARGIN}" w:bottom="{MARGIN}" '
            f'w:left="{MARGIN}" w:header="708" w:footer="567" w:gutter="0"/>'
            '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
        )
        return XML_DECL + f"<w:document {W_NS}><w:body>{''.join(self.body)}{sect}</w:body></w:document>"


# ---------------------------------------------------------------------------
# Pakket schrijven
# ---------------------------------------------------------------------------


def build_content_types(media_names, has_logo) -> str:
    exts = {"rels": "application/vnd.openxmlformats-package.relationships+xml",
            "xml": "application/xml"}
    for name in list(media_names) + (["logo.png"] if has_logo else []):
        ext = os.path.splitext(name)[1].lower().lstrip(".")
        exts[ext] = IMAGE_CONTENT_TYPES["." + ext]
    defaults = "".join(
        f'<Default Extension="{e}" ContentType="{c}"/>' for e, c in sorted(exts.items())
    )
    wml = "application/vnd.openxmlformats-officedocument.wordprocessingml"
    overrides = "".join([
        f'<Override PartName="/word/document.xml" ContentType="{wml}.document.main+xml"/>',
        f'<Override PartName="/word/styles.xml" ContentType="{wml}.styles+xml"/>',
        f'<Override PartName="/word/numbering.xml" ContentType="{wml}.numbering+xml"/>',
        f'<Override PartName="/word/settings.xml" ContentType="{wml}.settings+xml"/>',
        f'<Override PartName="/word/fontTable.xml" ContentType="{wml}.fontTable+xml"/>',
        f'<Override PartName="/word/footer1.xml" ContentType="{wml}.footer+xml"/>',
        '<Override PartName="/word/theme/theme1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/docProps/core.xml" '
        'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ])
    return (XML_DECL
            + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            + defaults + overrides + "</Types>")


def build_root_rels() -> str:
    o = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    p = "http://schemas.openxmlformats.org/package/2006/relationships"
    return (XML_DECL
            + f'<Relationships xmlns="{p}">'
            f'<Relationship Id="rId1" Type="{o}/officeDocument" Target="word/document.xml"/>'
            f'<Relationship Id="rId2" Type="{p.replace("/relationships", "/metadata")}/core-properties" '
            'Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{o}/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>")


def build_document_rels(doc: Document, has_logo: bool) -> str:
    o = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    p = "http://schemas.openxmlformats.org/package/2006/relationships"
    fixed = [
        ("rIdStyles", f"{o}/styles", "styles.xml", None),
        ("rIdNumbering", f"{o}/numbering", "numbering.xml", None),
        ("rIdSettings", f"{o}/settings", "settings.xml", None),
        ("rIdFontTable", f"{o}/fontTable", "fontTable.xml", None),
        ("rIdTheme", f"{o}/theme", "theme/theme1.xml", None),
    ]
    fixed.append(("rIdFooter", f"{o}/footer", "footer1.xml", None))
    items = fixed + doc.rels
    out = [XML_DECL, f'<Relationships xmlns="{p}">']
    for rid, rtype, target, mode in items:
        extra = f' TargetMode="{mode}"' if mode else ""
        out.append(f'<Relationship Id="{rid}" Type="{rtype}" Target="{esc(target)}"{extra}/>')
    out.append("</Relationships>")
    return "".join(out)


def build_footer_rels() -> str:
    o = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    p = "http://schemas.openxmlformats.org/package/2006/relationships"
    return (XML_DECL + f'<Relationships xmlns="{p}">'
            f'<Relationship Id="rIdLogo" Type="{o}/image" Target="media/logo.png"/>'
            "</Relationships>")


def write_package(path: str, doc: Document, document_xml: str, logo_bytes, ordered_lists: int):
    has_logo = logo_bytes is not None
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", build_content_types(doc.media.keys(), has_logo))
        z.writestr("_rels/.rels", build_root_rels())
        z.writestr("docProps/core.xml", build_core_props(doc.meta))
        z.writestr("docProps/app.xml", build_app_props())
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/_rels/document.xml.rels", build_document_rels(doc, has_logo))
        z.writestr("word/styles.xml", build_styles())
        z.writestr("word/numbering.xml", build_numbering(ordered_lists))
        z.writestr("word/settings.xml", build_settings())
        z.writestr("word/fontTable.xml", build_font_table())
        z.writestr("word/theme/theme1.xml", build_theme())
        z.writestr("word/footer1.xml", build_footer(has_logo))
        if has_logo:
            z.writestr("word/_rels/footer1.xml.rels", build_footer_rels())
            z.writestr("word/media/logo.png", logo_bytes)
        for name, data in doc.media.items():
            z.writestr(f"word/media/{name}", data)


def verify_package(path: str):
    """Controleer dat elk XML-onderdeel geldig is. Fouten hier zijn stille fouten in Word."""
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise BuildError(f"beschadigd onderdeel in het pakket: {bad}")
        for name in z.namelist():
            if name.endswith((".xml", ".rels")):
                try:
                    ElementTree.fromstring(z.read(name))
                except ElementTree.ParseError as exc:
                    raise BuildError(f"ongeldige XML in {name}: {exc}") from exc


# ---------------------------------------------------------------------------
# Hoofdprogramma
# ---------------------------------------------------------------------------

VERPLICHTE_VELDEN = ("klant", "project", "document")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Markdown naar een Word-document in de huisstijl van Nxt Phase AI.")
    ap.add_argument("bron", help="Markdown-bestand met front matter")
    ap.add_argument("-o", "--output", help="Pad van het .docx-bestand")
    ap.add_argument("--assets-dir",
                    help="Map waarin relatieve afbeeldingspaden worden gezocht "
                         "(standaard: de map van het bronbestand)")
    ap.add_argument("--logo", help="Pad naar het logo voor de voettekst "
                                   "(standaard: brand/nxt-phase-ai-logo-black.png naast dit script)")
    ap.add_argument("--geen-logo", action="store_true",
                    help="Voettekst zonder logo, alleen het paginanummer")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.bron):
        print(f"bronbestand niet gevonden: {args.bron}", file=sys.stderr)
        return 2

    src = open(args.bron, encoding="utf-8").read()
    meta, body = parse_frontmatter(src)

    ontbreekt = [k for k in VERPLICHTE_VELDEN if not meta.get(k)]
    if ontbreekt:
        print("front matter mist verplichte velden: " + ", ".join(ontbreekt), file=sys.stderr)
        print("verwacht: klant, project, document (en bij voorkeur datum)", file=sys.stderr)
        return 2

    assets_dir = args.assets_dir or os.path.dirname(os.path.abspath(args.bron))
    output = args.output or os.path.splitext(args.bron)[0] + ".docx"

    logo_bytes = None
    if not args.geen_logo:
        logo_path = args.logo or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "brand", "nxt-phase-ai-logo-black.png")
        if os.path.isfile(logo_path):
            logo_bytes = open(logo_path, "rb").read()
        else:
            print(f"let op: logo niet gevonden op {logo_path}, de voettekst krijgt alleen "
                  "een paginanummer", file=sys.stderr)

    blocks = parse_blocks(body)
    doc = Document(meta, assets_dir)
    document_xml = doc.render(blocks, footer_rid_present=True)

    write_package(output, doc, document_xml, logo_bytes, doc.ordered_lists)
    verify_package(output)

    koppen = sum(1 for b in blocks if b.kind == "heading")
    tabellen = sum(1 for b in blocks if b.kind == "table")
    print(f"geschreven: {output}")
    print(f"  {koppen} koppen, {tabellen} tabellen, {len(doc.media)} afbeeldingen, "
          f"{doc.ordered_lists} genummerde lijsten")
    if doc._missing_images:
        print("  afbeeldingen niet gevonden of niet bruikbaar:", file=sys.stderr)
        for m in doc._missing_images:
            print(f"    {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        print(f"fout: {exc}", file=sys.stderr)
        sys.exit(1)
