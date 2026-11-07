# -*- coding: utf-8 -*-
"""Passe 9 : harmonisation typographique + numerotation des figures/tableaux.
Regles :
  * police unique : Times New Roman ;
  * corps : 12 pt, justifie, interligne 1,5 ;
  * Heading1 : 16 pt gras, Heading2 : 14 pt gras, Heading3 : 12 pt gras,
    Heading4 : 12 pt gras italique ;
  * legendes : 9 pt italique, centrees.
"""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.table import Table

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(DOC)
FONT = "Times New Roman"

# ---------------------------------------------------------------------------
# 1. Styles de paragraphe
# ---------------------------------------------------------------------------
def force_font(style, size=None, bold=None, italic=None, color=None):
    f = style.font
    f.name = FONT
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(attr), FONT)
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color


S = doc.styles
force_font(S["Normal"], size=12)
S["Normal"].paragraph_format.line_spacing = 1.5
S["Normal"].paragraph_format.space_after = Pt(6)
S["Normal"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

HEAD = {
    "Heading 1": (16, True, False, 24, 12),
    "Heading 2": (14, True, False, 18, 8),
    "Heading 3": (12, True, False, 12, 6),
    "Heading 4": (12, True, True, 10, 4),
}
for name, (size, bold, italic, before, after) in HEAD.items():
    st = S[name]
    force_font(st, size=size, bold=bold, italic=italic, color=RGBColor(0x00, 0x00, 0x00))
    pf = st.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.keep_with_next = True
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT

for name in ("List Paragraph", "Normal (Web)", "z1qcye", "Body Text", "List Bullet"):
    try:
        force_font(S[name], size=12)
    except KeyError:
        pass

TECH = "II.1.4.1"  # placeholder pour eviter les erreurs

# ---------------------------------------------------------------------------
# 2. Runs : supprimer toute police/size directe sur les titres, normaliser le corps
# ---------------------------------------------------------------------------
def dominant_ok(p):
    st = p.style.name
    return st.startswith("Heading")


fixed_runs = 0
for p in doc.paragraphs:
    st = p.style.name
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn("w:rPr"))
        if rpr is not None:
            rf = rpr.find(qn("w:rFonts"))
            if rf is not None:
                rpr.remove(rf)
            sz = rpr.find(qn("w:sz"))
            if sz is not None:
                # les blocs de code (Annexes) gardent leur taille
                if not (st == "Normal" and r.font.name == "Consolas"):
                    rpr.remove(sz)
            szcs = rpr.find(qn("w:szCs"))
            if szcs is not None:
                rpr.remove(szcs)
            fixed_runs += 1
print(f"runs nettoyes : {fixed_runs}")

# ---------------------------------------------------------------------------
# 3. Blocs de code : Consolas 8,5 pt, sans justification
# ---------------------------------------------------------------------------
code = 0
for p in doc.paragraphs:
    if p.style.name != "Normal":
        continue
    t = p.text
    looks_code = bool(re.match(r"^(public |private |@|import |CREATE |ALTER |\}|if |for |return |\.|[a-zA-Z]+\(.*\);?$)", t.strip())) \
        and ("(" in t or ";" in t or "=" in t or t.strip().startswith(("@", "}", "CREATE", "ALTER")))
    if not looks_code:
        continue
    for r in p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        rpr = r._element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.insert(0, rf)
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rf.set(qn(attr), "Consolas")
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.line_spacing = 1.0
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)
    code += 1
print(f"paragraphes de code : {code}")

# ---------------------------------------------------------------------------
# 4. Legendes de figures et de tableaux
# ---------------------------------------------------------------------------
CAP = re.compile(r"^(Figure|Tableau)\s+(?:[IVX]+\.)?\d+")
caps = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if not CAP.match(t):
        continue
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.space_before = Pt(2)
    for r in p.runs:
        r.italic = True
        r.font.size = Pt(9)
        r.bold = False
    caps += 1
print(f"legendes normalisees : {caps}")

# ---------------------------------------------------------------------------
# 5. Renumerotation finale des figures et tableaux (ordre d'apparition)
# ---------------------------------------------------------------------------
items = []
for child in doc.element.body.iterchildren():
    if child.tag == qn("w:p"):
        items.append(("p", child))
    elif child.tag == qn("w:tbl"):
        items.append(("t", child))

chapter = "INTRO"
fig_n = {"INTRO": 0, "I": 0, "II": 0, "III": 0}
tab_n = dict(fig_n)
renames = []

from docx.text.paragraph import Paragraph
for kind, el in items:
    if kind == "p":
        p = Paragraph(el, doc)
        t = p.text.strip()
        if not t:
            continue
        if p.style.name == "Heading 1":
            u = t.upper()
            if "CHAPITRE I" in u:
                chapter = "I"
            elif "CHAPITRE II" in u:
                chapter = "II"
            elif "CHAPITRE III" in u:
                chapter = "III"
            elif "INTRODUCTION" in u:
                chapter = "INTRO"
            continue
        m = re.match(r"^(Figure|Tableau)\s+(?:[IVX]+\.)?\d+\s*(—|-)?\s*(.*)$", t)
        if m and p.style.name == "Normal":
            kind_w = m.group(1)
            label = m.group(3).strip()
            if kind_w == "Figure":
                fig_n[chapter] += 1
                num = fig_n[chapter]
            else:
                tab_n[chapter] += 1
                num = tab_n[chapter]
            prefix = "" if chapter == "INTRO" else f"{chapter}."
            new = f"{kind_w} {prefix}{num} — {label}"
            if new != t:
                renames.append((p, new))

print(f"legende a renumeroter : {len(renames)}")
for p, new in renames:
    runs = p.runs
    if runs:
        runs[0].text = new
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
    print(f"   {p.text[:70]}")

doc.save(DOC)
print("\nPasse 9 terminee")