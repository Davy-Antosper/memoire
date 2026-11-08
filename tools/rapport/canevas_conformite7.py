# -*- coding: utf-8 -*-
"""Passe 7 : reconstruction propre de la structure de III.3 et des sections finales."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table

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


# ===========================================================================
# 1. III.3.7 : la piste d'audit a ete fusionnee par erreur -> scinder
# ===========================================================================
items = elems()
i_337 = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.3.7"), items=items)
i_der = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.4.1"), start=i_337 + 1, items=items)

if i_337 != -1:
    # renommer III.3.7 en « Piste d'audit » et creer III.3.8 pour les tests
    set_text(items[i_337], "III.3.7 Piste d’audit")
    note("III.3.7 = Piste d'audit")

    # Reperer le paragraphe d'introduction des tests (orphelin) et les titres III.4.x
    items = elems()
    i_der = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.4.1"), items=items)
    # Le paragraphe juste avant III.4.1 est l'intro des tests
    intro_tests = items[i_der - 1]

    # transformer les III.4.x / III.5.x en Heading4 sous de nouveaux Heading3
    mapping = {
        "III.4.1": ("Stratégie de test", "III.3.8.1"),
        "III.4.2": ("Tests d’intégration", "III.3.8.2"),
        "III.4.3": ("Intégration et déploiement continus", "III.3.8.3"),
        "III.4.4": ("Résultats", "III.3.8.4"),
        "III.5.1": ("Conformité au cahier des charges", "III.3.9.1"),
        "III.5.2": ("Performance", "III.3.9.2"),
        "III.5.3": ("Maintenabilité", "III.3.9.3"),
    }
    for old, (label, new_num) in mapping.items():
        items = elems()
        k = index_of(lambda e: is_h(e, 3) and txt(e).startswith(old), items=items)
        if k != -1:
            set_text(items[k], f"{new_num} {label}")
            set_style(items[k], "Heading4")

    # inserer les deux nouveaux Heading3
    items = elems()
    i_intro = index_of(lambda e: e.tag == qn("w:p") and
                       txt(e).startswith("Cette section présente la stratégie de test"), items=items)
    h_tests = new_para("III.3.8 Tests et déploiement", style="Heading 3")
    insert_after(items[i_intro - 1], h_tests)

    items = elems()
    i_eval_intro = index_of(lambda e: e.tag == qn("w:p") and
                            txt(e).startswith("Cette section évalue le système réalisé"), items=items)
    h_eval = new_para("III.3.9 Évaluation des résultats", style="Heading 3")
    insert_after(items[i_eval_intro - 1], h_eval)
    note("III.3.8 Tests et deploiement + III.3.9 Evaluation crees")

# Supprimer l'introduction redondante de l'ancien III.3
items = elems()
i_intro33 = index_of(lambda e: e.tag == qn("w:p") and
                     txt(e).startswith("Cette section présente les détails de l'implémentation"), items=items)
if i_intro33 != -1:
    set_text(items[i_intro33],
             "Cette section présente la réalisation du système, les tests qui l’ont validé et "
             "l’évaluation de ses résultats. Elle décrit d’abord la structure du projet et les "
             "principaux mécanismes implémentés, puis la stratégie de test, le déploiement et les "
             "enseignements tirés de la mise en œuvre.")
    note("introduction III.3 corrigee")

# ===========================================================================
# 2. Securite (ancien III.5.4) : reecriture sans RBAC
# ===========================================================================
items = elems()
k = index_of(lambda e: is_h(e, 4) and txt(e).startswith("III.3.9.3") is False and
             "Sécurité" in txt(e), items=items)
if k != -1:
    set_text(items[k], "III.3.9.4 Sécurité")
    note("section Securite renumerotee")

doc.save(DOC)
print(f"\nPasse 7 terminee : {len(log)} operations")