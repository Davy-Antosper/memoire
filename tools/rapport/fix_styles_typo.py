# -*- coding: utf-8 -*-
"""Harmonise la typographie au niveau des STYLES (et non plus des runs) :
- docDefaults et tous les styles -> Times New Roman (suppression des polices de theme)
- Heading 1 = 16 pt gras, Heading 2 = 14 pt gras,
  Heading 3 = 12 pt gras, Heading 4 = 12 pt gras italique
- Normal = 12 pt, justifie, interligne 1,5, espace apres 6 pt
- Caption = 9 pt italique, centre
- styles toc 1/2/3 -> Times New Roman
- code (macros / runs Consolas) preserve
"""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"
FONT = "Times New Roman"

doc = Document(DOC)
styles = doc.styles


def force_font(rPr):
    """Remplace les polices de theme par Times New Roman explicite."""
    if rPr is None:
        return None
    for rf in rPr.findall(qn("w:rFonts")):
        rPr.remove(rf)
    rf = rPr.makeelement(qn("w:rFonts"), {})
    rf.set(qn("w:ascii"), FONT)
    rf.set(qn("w:hAnsi"), FONT)
    rf.set(qn("w:cs"), FONT)
    rf.set(qn("w:eastAsia"), FONT)
    rPr.insert(0, rf)
    return rf


def set_size(rPr, pt):
    for tag in ("w:sz", "w:szCs"):
        for el in rPr.findall(qn(tag)):
            rPr.remove(el)
    for tag in ("w:sz", "w:szCs"):
        el = rPr.makeelement(qn(tag), {})
        el.set(qn("w:val"), str(int(pt * 2)))
        rPr.append(el)


def set_flag(rPr, tag, on=True):
    for el in rPr.findall(qn(tag)):
        rPr.remove(el)
    if on:
        rPr.append(rPr.makeelement(qn(tag), {}))


# --- 1. docDefaults ---
dd = styles.element.find(qn("w:docDefaults"))
rpr_def = dd.find(qn("w:rPrDefault")).find(qn("w:rPr"))
force_font(rpr_def)
set_size(rpr_def, 12)

# --- 2. styles de titres ---
SPECS = {
    "Heading 1": (16, False),
    "Heading 2": (14, False),
    "Heading 3": (12, False),
    "Heading 4": (12, True),
}
for name, (size, italic) in SPECS.items():
    st = styles[name]
    rPr = st.element.find(qn("w:rPr"))
    if rPr is None:
        rPr = st.element.makeelement(qn("w:rPr"), {})
        st.element.append(rPr)
    force_font(rPr)
    set_size(rPr, size)
    set_flag(rPr, "w:b", True)
    set_flag(rPr, "w:bCs", True)
    set_flag(rPr, "w:i", italic)
    set_flag(rPr, "w:iCs", italic)
    # couleur noire
    for c in rPr.findall(qn("w:color")):
        rPr.remove(c)
    col = rPr.makeelement(qn("w:color"), {})
    col.set(qn("w:val"), "000000")
    rPr.append(col)

# --- 3. Normal ---
normal = styles["Normal"]
rPr = normal.element.find(qn("w:rPr"))
if rPr is not None:
    force_font(rPr)
    set_size(rPr, 12)
    for c in rPr.findall(qn("w:color")):
        rPr.remove(c)
    col = rPr.makeelement(qn("w:color"), {})
    col.set(qn("w:val"), "000000")
    rPr.append(col)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(6)

# --- 4. Caption : 9 pt italique centre ---
try:
    cap = styles["Caption"]
    crPr = cap.element.find(qn("w:rPr"))
    if crPr is None:
        crPr = cap.element.makeelement(qn("w:rPr"), {})
        cap.element.append(crPr)
    force_font(crPr)
    set_size(crPr, 9)
    set_flag(crPr, "w:b", False)
    set_flag(crPr, "w:i", True)
    set_flag(crPr, "w:iCs", True)
    for c in crPr.findall(qn("w:color")):
        crPr.remove(c)
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(3)
    cap.paragraph_format.space_after = Pt(9)
except KeyError:
    pass

# --- 5. styles de table des matieres ---
for name in ("toc 1", "toc 2", "toc 3", "toc 4", "TOC Heading"):
    try:
        st = styles[name]
    except KeyError:
        continue
    trPr = st.element.find(qn("w:rPr"))
    if trPr is None:
        trPr = st.element.makeelement(qn("w:rPr"), {})
        st.element.append(trPr)
    force_font(trPr)

# --- 6. Neutraliser les polices de theme restantes dans tous les styles ---
for st in styles:
    try:
        srPr = st.element.find(qn("w:rPr"))
    except Exception:
        continue
    if srPr is None:
        continue
    rfs = srPr.findall(qn("w:rFonts"))
    if any(rf.get(qn("w:asciiTheme")) or rf.get(qn("w:hAnsiTheme")) for rf in rfs):
        # ne pas toucher aux styles de code
        if "code" in st.name.lower() or st.name == "macro":
            continue
        force_font(srPr)

doc.save(DOC)
print("styles harmonises :", len(SPECS) + 1, "| docDefaults + Caption + TOC")