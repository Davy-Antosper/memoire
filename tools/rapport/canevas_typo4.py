# -*- coding: utf-8 -*-
"""Passe 12 : combler le trou II.1.3, corriger la legende du diagramme de classes
et le placer correctement, puis renumeroter."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(DOC)
body = doc.element.body


def txt(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def style_of(el):
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        return ""
    ps = pPr.find(qn("w:pStyle"))
    return ps.get(qn("w:val")) if ps is not None else ""


def elems():
    sectPr = body.find(qn("w:sectPr"))
    return [c for c in body.iterchildren() if c is not sectPr]


def set_text(el, new_text):
    runs = el.findall(".//" + qn("w:r"))
    if not runs:
        return False
    first = runs[0]
    for r in runs[1:]:
        r.getparent().remove(r)
    for t in first.findall(qn("w:t")):
        first.remove(t)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = new_text
    first.append(t)
    return True


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Combler le trou II.1.3
# ===========================================================================
items = elems()
k = None
for i, el in enumerate(items):
    if el.tag == qn("w:p") and txt(el).startswith("II.1.4 Technologies"):
        k = i
        break

if k is not None:
    set_text(items[k], "II.1.3 Technologies et outils utilisés")
    note("II.1.4 -> II.1.3")

    # renumeroter les sous-sections II.1.4.x -> II.1.3.x
    for el in elems():
        if el.tag == qn("w:p"):
            t = txt(el)
            m = re.match(r"^II\.1\.4\.(\d+)\s+(.+)$", t)
            if m and style_of(el) == "Heading4":
                set_text(el, f"II.1.3.{m.group(1)} {m.group(2)}")
    note("sous-sections II.1.3.x renumerotees")

# ===========================================================================
# 2. Diagramme de classes : legende numerotee + replacement apres le modele
# ===========================================================================
items = elems()
cls_idx = None
for i, el in enumerate(items):
    if el.tag == qn("w:p") and txt(el).startswith("Figure") and "classes" in txt(el).lower():
        cls_idx = i
        break

if cls_idx is None:
    note("[!] legende du diagramme de classes introuvable")
else:
    cap_el = items[cls_idx]
    img_el = items[cls_idx - 1]
    intro_el = items[cls_idx - 2]

    # deplacer le bloc juste apres le paragraphe de normalisation du modele
    items = elems()
    anchor = None
    for el in items:
        if el.tag == qn("w:p") and txt(el).startswith("Le modèle de données du système comprend"):
            anchor = el
            break
    if anchor is not None:
        for e in (img_el, cap_el):
            e.getparent().remove(e)
        anchor.addnext(img_el)
        img_el.addnext(cap_el)
        note("diagramme de classes replace apres le paragraphe du modele")

doc.save(DOC)
print(f"\nPasse 12 terminee : {len(log)} operations")