# -*- coding: utf-8 -*-
"""Passe 4 : renumerotation du chapitre III, restauration du diagramme de classes,
mise a jour des chiffres reels, nettoyage des restes de sections supprimees."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
ASSETS = os.path.join(HERE, "memoire_assets")

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


def index_of(pred, start=0, items=None):
    items = items if items is not None else elems()
    for i in range(start, len(items)):
        if pred(items[i]):
            return i
    return -1


def is_h(el, level=None):
    if el.tag != qn("w:p"):
        return False
    s = style_of(el).replace(" ", "")
    if level is None:
        return s.startswith("Heading")
    return s == f"Heading{level}"


def remove_el(el):
    el.getparent().remove(el)


def remove_range(a, b):
    items = elems()
    n = 0
    for el in items[a:b]:
        el.getparent().remove(el)
        n += 1
    return n


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


def new_para(text="", style=None, bold=False, italic=False, size=None, align=None):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        if bold:
            r.bold = True
        if italic:
            r.italic = True
        if size:
            r.font.size = Pt(size)
    if style:
        p.style = doc.styles[style]
    if align is not None:
        p.alignment = align
    el = p._element
    body.remove(el)
    return el


def new_image(path, width_in=5.8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(path, width=Inches(width_in))
    el = p._element
    body.remove(el)
    return el


def insert_after(anchor, el):
    anchor.addnext(el)
    return el


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Restauration du diagramme de classes (supprime par erreur en passe 3)
# ===========================================================================
items = elems()
i_cls = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Figure") and "classes" in txt(e).lower(),
                 items=items)
if i_cls == -1:
    # inserer apres le tableau des enums (III.6) ou apres le dictionnaire
    i_dep = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Le diagramme de déploiement"),
                     items=items)
    anchor = items[i_dep - 1] if i_dep != -1 else None
    if anchor is not None:
        img = new_image(os.path.join(ASSETS, "class_diagram.png"), 5.8)
        cap = new_para("Figure — Diagramme de classes UML", italic=True, size=9,
                       align=WD_ALIGN_PARAGRAPH.CENTER)
        intro = new_para(
            "Le diagramme de classes présente les seize entités du système, leurs attributs "
            "principaux et les associations qui les relient : la hiérarchie géographique (province, "
            "zone, colline), les acteurs (agriculteur, utilisateur), les objets de stock (type "
            "d’engrais, lot, stock, stock par lot), les objets de flux (ticket, mouvement, "
            "distribution) et les objets de pilotage (alerte, seuil d’alerte, journal d’audit).")
        insert_after(anchor, intro)
        insert_after(intro, img)
        insert_after(img, cap)
        note("diagramme de classes restaure")
else:
    note("diagramme de classes deja present")

# ===========================================================================
# 2. Renumerotation des sous-sections III.3.x et III.4.x / III.5.x
# ===========================================================================
items = elems()
i_sec3 = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
i_end3 = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_sec3 + 1, items=items)
items = elems()

# Collecter les titres Heading3 entre III.3 et CONCLUSION
h3_idx = [k for k in range(i_sec3 + 1, i_end3) if is_h(items[k], 3)]
print("Heading3 dans III.3 :", [txt(items[k])[:45] for k in h3_idx])

labels = []
for k in h3_idx:
    t = txt(items[k])
    # retirer l'ancien prefixe
    t = re.sub(r"^III\.\d+\.\d+\s*", "", t)
    labels.append(t)

for pos, k in enumerate(h3_idx, 1):
    set_text(items[k], f"III.3.{pos} {labels[pos - 1]}")
note(f"renumerotation III.3.x : {len(h3_idx)} sous-sections")

# ===========================================================================
# 3. Ajout des sous-sections « Tests », « Deploiement », « Evaluation »
# ===========================================================================
items = elems()
i_sec3 = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
i_end3 = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_sec3 + 1, items=items)
items = elems()
existing = [txt(items[k]) for k in range(i_sec3 + 1, i_end3) if is_h(items[k], 3)]
print("sous-sections III.3 :")
for e in existing:
    print("   ", e)