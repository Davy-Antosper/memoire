# -*- coding: utf-8 -*-
"""Passe 3 : fusion des sections du chapitre III, reorganisation des figures,
renumerotation des figures et tableaux, suppression du FIFO detaille."""
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


def remove_range(a, b):
    items = elems()
    n = 0
    for el in items[a:b]:
        el.getparent().remove(el)
        n += 1
    return n


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


def move_after(src_els, anchor):
    """Deplace une liste d'elements juste apres l'ancre."""
    cur = anchor
    for e in src_els:
        e.getparent().remove(e)
        cur.addnext(e)
        cur = e
    return cur


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Fusion III.3 / III.4 / III.5 / III.6 -> III.3
# ===========================================================================
items = elems()
i3 = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
i_test = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.4"), start=i3 + 1, items=items)
i_eval = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.5"), start=i_test + 1, items=items)
i_cli = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.6"), start=i_eval + 1, items=items)
i_end = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_cli + 1, items=items)

print(f"indices: III.3={i3} III.4={i_test} III.5={i_eval} III.6={i_cli} fin={i_end}")

# Supprimer les titres Heading2 (III.4, III.5, III.6) et leur paragraphe d'intro
for idx in (i_cli, i_eval, i_test):
    items = elems()
    if idx >= len(items):
        continue
    remove_el(items[idx])

# III.3 devient III.3 Realisation, tests et evaluation
items = elems()
i3 = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
set_text(items[i3], "III.3 Réalisation, tests et évaluation")
note("III.3 renommee")

# Supprimer l'introduction de l'ancien III.3 (elle parle de « ce chapitre »)
items = elems()
i3 = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
nxt = items[i3 + 1]
if nxt.tag == qn("w:p") and txt(nxt).startswith("Ce chapitre présente les détails"):
    set_text(nxt,
             "Cette section présente la réalisation du système, les tests qui l’ont validé et "
             "l’évaluation de ses résultats. Elle décrit d’abord la structure et les principaux "
             "mécanismes implémentés, puis la stratégie de test, le déploiement et les enseignements "
             "tirés de la mise en œuvre.")
    note("introduction III.3 reecrite")

# ===========================================================================
# 2. Suppression de III.3.2 Gestion des stocks FIFO (trop detaille)
# ===========================================================================
items = elems()
a = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.3.2"), items=items)
if a != -1:
    b = index_of(lambda e: is_h(e, 3), start=a + 1, items=items)
    n = remove_range(a, b)
    note(f"III.3.2 Gestion des stocks FIFO : {n} elements supprimes")

# ===========================================================================
# 3. Reorganisation des figures du III.2.2
# ===========================================================================
# 3.1 Diagramme de deploiement (figure + paragraphe) -> a la fin du III.2.2
items = elems()
i_dep_para = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Le diagramme de déploiement"),
                      items=items)
if i_dep_para != -1:
    dep_para = items[i_dep_para]
    dep_img = items[i_dep_para + 1]
    dep_cap = items[i_dep_para + 2]
    # verifier que c'est bien image + legende
    ok = (dep_img.tag == qn("w:p") and dep_img.findall(".//" + qn("w:drawing"))
          and txt(dep_cap).startswith("Figure"))
    if ok:
        # destination : juste avant le titre III.2.3
        items = elems()
        i_next = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.2.3"), items=items)
        anchor = items[i_next - 1]
        move_after([dep_para, dep_img, dep_cap], anchor)
        note("diagramme de deploiement deplace en fin de III.2.2")

# 3.2 Diagramme de classes -> apres le tableau des enums
items = elems()
i_cls_cap = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Figure") and "classes" in txt(e),
                     items=items)
if i_cls_cap != -1:
    cls_cap = items[i_cls_cap]
    cls_img = items[i_cls_cap - 1]
    if cls_img.tag == qn("w:p") and cls_img.findall(".//" + qn("w:drawing")):
        # supprimer le paragraphe d'introduction orphelin juste avant
        prev = items[i_cls_cap - 2]
        if prev.tag == qn("w:p") and txt(prev).startswith("Le diagramme de classes UML"):
            remove_el(prev)
        items = elems()
        i_enum_tab = index_of(lambda e: e.tag == qn("w:tbl") and
                              txt(e).startswith("EnumValeursUsage"), items=items)
        if i_enum_tab == -1:
            # fallback : apres le tableau des enums (7 lignes)
            for k, el in enumerate(items):
                if el.tag == qn("w:tbl"):
                    t = Table(el, doc)
                    if len(t.rows) == 7 and "NiveauDepot" in t.rows[1].cells[0].text:
                        i_enum_tab = k
                        break
        if i_enum_tab != -1:
            intro = new_para(
                "Le diagramme de classes présente les seize entités du système, leurs attributs "
                "principaux et les associations qui les relient : la hiérarchie géographique "
                "(province, zone, colline), les acteurs (agriculteur, utilisateur), les objets de stock "
                "(type d’engrais, lot, stock, stock par lot), les objets de flux (ticket, mouvement, "
                "distribution) et les objets de pilotage (alerte, seuil d’alerte, journal d’audit).")
            insert_after(items[i_enum_tab], intro)
            move_after([cls_img, cls_cap], intro)
            note("diagramme de classes deplace apres le tableau des enums")

# 3.3 Diagramme de cas d'utilisation + activites -> III.1 (analyse des besoins)
items = elems()
i_uc_cap = index_of(lambda e: e.tag == qn("w:p") and "cas d'utilisation" in txt(e) and
                    txt(e).startswith("Figure"), items=items)
i_uc_para = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Le diagramme de cas d'utilisation"),
                     items=items)
i_act_para = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Le diagramme d'activités"),
                      items=items)
i_act_cap = index_of(lambda e: e.tag == qn("w:p") and txt(e).startswith("Figure") and
                     "activités" in txt(e), items=items)

if all(x != -1 for x in (i_uc_cap, i_uc_para, i_act_para, i_act_cap)):
    uc_block = [items[i_uc_para], items[i_uc_para + 1], items[i_uc_cap]]
    act_block = [items[i_act_para], items[i_act_para + 1], items[i_act_cap]]
    # cible : juste avant le titre III.2
    items = elems()
    i_conc = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.2"), items=items)
    anchor = items[i_conc - 1]
    # retirer la phrase de renvoi du III.2.2 si presente
    move_after(act_block, anchor)
    move_after(uc_block, anchor)
    note("diagrammes cas d'utilisation et activites deplaces dans III.1")

doc.save(DOC)
print(f"\nPasse 3 terminee : {len(log)} operations")