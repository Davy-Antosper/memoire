# -*- coding: utf-8 -*-
"""Passe de conformite au canevas du professeur.

Applique, dans l'ordre :
  1. suppression de la section PNSEB (1.3) et des renvois « [1, 2, 3] » ;
  2. suppression de l'architecture en couches (II.1.3 + III.2.1) ;
  3. suppression de la machine a etats (III.2.4), de l'algorithme FIFO detaille
     (III.2.5, III.3.2) et de la securite/RBAC (II.1.4, III.2.6, III.5.4) ;
  4. suppression de tous les blocs « Source : https://... » du corps du texte ;
  5. mise en conformite des titres avec le canevas (4 niveaux) ;
  6. ajout des figures « Circuit de distribution » et « Architecture du systeme » ;
  7. sections finales « References bibliographiques » et « Webographie » ;
  8. harmonisation typographique.
"""
import os
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
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

# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
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


def is_heading(el, level=None):
    if el.tag != qn("w:p"):
        return False
    s = style_of(el)
    if level is None:
        return s.startswith("Heading")
    return s == f"Heading{level}" or s == f"Heading {level}"


def remove_range(a, b):
    """Supprime les elements d'indice a (inclus) a b (exclu)."""
    items = elems()
    removed = 0
    for el in items[a:b]:
        el.getparent().remove(el)
        removed += 1
    return removed


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


def insert_many_after(anchor, els):
    cur = anchor
    for e in els:
        cur = insert_after(cur, e)
    return cur


def page_break():
    p = doc.add_paragraph()
    from docx.enum.text import WD_BREAK
    p.add_run().add_break(WD_BREAK.PAGE)
    el = p._element
    body.remove(el)
    return el


def goto_page_break_after(anchor, title):
    pb = page_break()
    h = new_para(title, style="Heading 1")
    return insert_many_after(anchor, [pb, h])


log = []
def note(msg):
    log.append(msg)
    print("  " + msg)


# ===========================================================================
# 1. Suppression de la section PNSEB (1.3)
# ===========================================================================
items = elems()
i_start = index_of(lambda e: is_heading(e) and txt(e).startswith("1.3 Le Programme National"), items=items)
if i_start == -1:
    note("[!] section 1.3 PNSEB introuvable")
else:
    i_end = index_of(lambda e: is_heading(e) and txt(e).startswith("1.4 "), start=i_start + 1, items=items)
    if i_end == -1:
        note("[!] fin de la section 1.3 introuvable")
    else:
        n = remove_range(i_start, i_end)
        note(f"PNSEB : {n} elements supprimes (section 1.3)")
        # Renumerotation : 1.4 devient 1.3
        it2 = elems()
        j = index_of(lambda e: is_heading(e) and txt(e).startswith("1.4 "), items=it2)
        if j != -1:
            set_text(it2[j], "1.3 La réforme administrative de 2023")
            note("renumerotation : 1.3 La reforme administrative de 2023")

# ===========================================================================
# 2. Suppression des blocs « Source : ... » et des URLs nues du corps
# ===========================================================================
URL_RE = re.compile(r"^\s*(https?://\S+|\S*https?://\S*)\s*$")
removed_src = 0
for _ in range(6):
    items = elems()
    changed = False
    for el in items:
        if el.tag != qn("w:p"):
            continue
        t = txt(el)
        if not t:
            continue
        if t.rstrip(" :").lower() in ("source", "sources") or URL_RE.match(t):
            el.getparent().remove(el)
            removed_src += 1
            changed = True
    if not changed:
        break
note(f"blocs « Source » / URLs : {removed_src} paragraphes supprimes")

# Renvois [1, 2, 3] residuels -> supprimes
CIT = re.compile(r"\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\]")
cit = 0
for p in doc.paragraphs:
    if CIT.search(p.text):
        new = CIT.sub("", p.text)
        new = re.sub(r"\s{2,}", " ", new)
        if new != p.text and set_text(p._element, new):
            cit += 1
note(f"renvois [n] dans le texte : {cit} paragraphes nettoyes")

# ===========================================================================
# 3. Suppressions thematiques
# ===========================================================================
def drop_section(prefix, level, label):
    items = elems()
    i = index_of(lambda e: is_heading(e, level) and txt(e).startswith(prefix), items=items)
    if i == -1:
        note(f"[!] introuvable : {label}")
        return 0
    # fin = prochain titre de niveau <= level
    j = len(items)
    for k in range(i + 1, len(items)):
        el = items[k]
        if el.tag != qn("w:p"):
            continue
        s = style_of(el)
        if s.startswith("Heading"):
            try:
                lv = int(s.replace("Heading", "").replace(" ", "") or 0)
            except ValueError:
                lv = 0
            if lv and lv <= level:
                j = k
                break
    n = remove_range(i, j)
    note(f"{label} : {n} elements supprimes")
    return n

# Architecture en couches (concept) -> suppression du titre, texte reecrit plus loin
drop_section("II.1.3", 3, "II.1.3 Architecture logicielle en couches")
# Securite / RBAC (concept)
drop_section("II.1.4", 3, "II.1.4 Securite JWT et RBAC")
# Machine a etats
drop_section("III.2.4", 3, "III.2.4 Machine a etats du ticket")
# Algorithme FIFO detaille (conception)
drop_section("III.2.5", 3, "III.2.5 Algorithme FIFO")
# Securite et RBAC (conception)
drop_section("III.2.6", 3, "III.2.6 Securite et RBAC")

# Renumerotation des sous-sections suivantes de II.1
items = elems()
renames = [
    ("II.1.5 Technologies et outils utilisés", "II.1.4 Technologies et outils utilisés"),
    ("II.1.6 État de l’art", "II.1.5 État de l’art"),
]
for old, new in renames:
    it = elems()
    i = index_of(lambda e: is_heading(e, 3) and txt(e).startswith(old[:9]), items=it)
    if i != -1:
        set_text(it[i], new)
        note(f"renumerotation : {new}")

doc.save(DOC)
print("\nETAPE 1-3 terminee :", len(log), "operations")