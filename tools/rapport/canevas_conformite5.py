# -*- coding: utf-8 -*-
"""Passe 5 : regroupement des sous-sections du III.3 et mise a jour des faits."""
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


def set_style(el, sid):
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        el.insert(0, pPr)
    ps = pPr.find(qn("w:pStyle"))
    if ps is None:
        ps = OxmlElement("w:pStyle")
        pPr.insert(0, ps)
    ps.set(qn("w:val"), sid)


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


def insert_after(anchor, el):
    anchor.addnext(el)
    return el


log = []
def note(m):
    log.append(m)
    print("  " + m)


def find_h3(prefix, items=None):
    items = items if items is not None else elems()
    return index_of(lambda e: is_h(e, 3) and txt(e).startswith(prefix), items=items)


# ===========================================================================
# 1. Fusion « Strategie de test » + « Tests d'integration » + « Resultats »
# ===========================================================================
i_strat = find_h3("III.3.7")
i_integ = find_h3("III.3.8")
i_results = find_h3("III.3.10")

if i_strat != -1:
    items = elems()
    set_text(items[i_strat], "III.3.7 Tests et résultats")
    note("III.3.7 renommee « Tests et resultats »")

for pfx in ("III.3.8", "III.3.10"):
    items = elems()
    k = index_of(lambda e: is_h(e, 3) and txt(e).startswith(pfx), items=items)
    if k != -1:
        # supprimer le titre et son eventuel paragraphe d'intro redondant
        title = txt(items[k])
        remove_el(items[k])
        note(f"titre fusionne supprime : {title}")

# ===========================================================================
# 2. Fusion de l'evaluation : un seul titre + 3 sous-sous-sections
# ===========================================================================
items = elems()
i_eval = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.3.11"), items=items)
i_end = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_eval + 1, items=items)

if i_eval != -1:
    # supprimer « Securite » (III.3.14) : RBAC deja retire a la demande
    items = elems()
    k = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.3.14"), items=items)
    if k != -1:
        j = k + 1
        while j < len(items) and not is_h(items[j]):
            j += 1
        n = remove_range(k, j)
        note(f"evaluation « Securite » : {n} elements supprimes")

    items = elems()
    i_eval = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.3.11"), items=items)
    # transformer le titre d'evaluation
    set_text(items[i_eval], "III.3.9 Évaluation des résultats")
    note("III.3.9 Evaluation des resultats")

    # renommer les sous-titres en Heading4
    ren = {"III.3.11": "III.3.9.1 Conformité au cahier des charges",
           "III.3.12": "III.3.9.2 Performance",
           "III.3.13": "III.3.9.3 Maintenabilité"}
    for old, new in ren.items():
        items = elems()
        k = index_of(lambda e: is_h(e, 3) and txt(e).startswith(old), items=items)
        if k != -1:
            set_text(items[k], new)
            set_style(items[k], "Heading4")
            note(f"-> {new}")

# ===========================================================================
# 3. Mise a jour des faits (chiffres reels du code)
# ===========================================================================
FACTS = [
    ("207 tests", "218 tests"),
    ("207/207", "218/218"),
    ("204 tests d'intégration", "215 tests d'intégration"),
    ("Les 204 tests", "Les 215 tests"),
    ("204 tests", "215 tests"),
    ("les 204 tests d'intégration", "les 215 tests d'intégration"),
    ("Les 204 tests d'intégration", "Les 215 tests d'intégration"),
    ("soixante endpoints", "soixante-deux endpoints"),
    ("soixante points d'entrée", "soixante-deux points d'entrée"),
    ("11 versions de migration", "12 versions de migration"),
    ("onze migrations Flyway", "douze migrations Flyway"),
    ("11 migrations Flyway", "12 migrations Flyway"),
    ("20 classes de tests d'intégration", "22 classes de tests d'intégration"),
]
count = 0
for p in doc.paragraphs:
    t = p.text
    if not t.strip():
        continue
    new = t
    for old, rep in FACTS:
        if old in new:
            new = new.replace(old, rep)
    if new != t and set_text(p._element, new):
        count += 1
note(f"faits mis a jour : {count} paragraphes")

# ===========================================================================
# 4. Verification des chiffres dans les tableaux
# ===========================================================================
tables = doc.tables
for t in tables:
    for row in t.rows:
        for cell in row.cells:
            txtc = cell.text
            new = txtc
            for old, rep in FACTS:
                if old in new:
                    new = new.replace(old, rep)
            if new != txtc:
                cell.text = new
note("tableaux verifies")

# ===========================================================================
# 5. Controle des mentions interdites residuelles
# ===========================================================================
FORBIDDEN = [
    "architecture en couches", "Architecture en couches",
    "layered architecture", "machine à états", "Machine à états",
    "RBAC", "Matrice RBAC",
]
items = elems()
i_intro = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), items=items)
print("\nMentions residuelles :")
for el in items[:i_intro]:
    if el.tag != qn("w:p"):
        continue
    t = txt(el)
    for f in FORBIDDEN:
        if f in t:
            print(f"   [{f}] {t[:130]}")

doc.save(DOC)
print(f"\nPasse 5 terminee : {len(log)} operations")