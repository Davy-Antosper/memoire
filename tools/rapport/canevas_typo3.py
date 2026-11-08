# -*- coding: utf-8 -*-
"""Passe 11 : remplacer la figure redondante du dictionnaire par le diagramme
de classes, corriger les renvois, renumeroter, verifier la typographie."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
ASSETS = os.path.join(HERE, "memoire_assets")

doc = Document(DOC)
body = doc.element.body


def txt(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


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
# 1. La figure « Dictionnaire de données » (image matplotlib obsolete et
#    redondante avec le Tableau III.7) devient le diagramme de classes.
# ===========================================================================
items = elems()
target = None
for k, el in enumerate(items):
    if el.tag == qn("w:p") and txt(el).startswith("Figure") and "Dictionnaire de données" in txt(el):
        target = k
        break

if target is None:
    note("[!] figure dictionnaire introuvable")
else:
    cap_el = items[target]
    img_el = items[target - 1]
    assert img_el.tag == qn("w:p") and img_el.findall(".//" + qn("w:drawing"))

    # remplacer le blob de l'image
    path = os.path.join(ASSETS, "class_diagram.png")
    with open(path, "rb") as fh:
        blob = fh.read()
    for blip in img_el.iter(qn("a:blip")):
        rid = blip.get(qn("r:embed"))
        doc.part.related_parts[rid]._blob = blob
    note(f"image remplacee par class_diagram.png ({len(blob)} o)")

    set_text(cap_el, "Figure — Diagramme de classes UML")
    note("legende -> Diagramme de classes UML")

    # Deplacer ce bloc a la fin du III.2.2 (apres le Tableau III.7)
    items = elems()
    tab7 = None
    for k, el in enumerate(items):
        if el.tag == qn("w:tbl"):
            from docx.table import Table
            t = Table(el, doc)
            head = " ".join(c.text for c in t.rows[0].cells)
            if "Colonne" in head and len(t.rows) > 20:
                tab7 = k
    if tab7 is not None:
        anchor = items[tab7]
        img_el.getparent().remove(img_el)
        cap_el.getparent().remove(cap_el)
        anchor.addnext(img_el)
        img_el.addnext(cap_el)
        note("bloc deplace apres le dictionnaire de donnees")

        # paragraphe d'introduction avant l'image
        p = doc.add_paragraph()
        r = p.add_run(
            "Le diagramme de classes présente les seize entités du système, leurs attributs "
            "principaux et les associations qui les relient : la hiérarchie géographique "
            "(province, zone, colline), les acteurs (agriculteur, utilisateur), les objets de stock "
            "(type d’engrais, lot, stock, stock par lot), les objets de flux (ticket, mouvement, "
            "distribution) et les objets de pilotage (alerte, seuil d’alerte, journal d’audit).")
        p.style = doc.styles["Normal"]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pel = p._element
        body.remove(pel)
        anchor.addnext(pel)
        note("paragraphe d'introduction insere")

# ===========================================================================
# 2. Renumerotation des figures et tableaux + renvois
# ===========================================================================
def chap_of(t):
    u = t.upper()
    if "CHAPITRE III" in u:
        return "III"
    if "CHAPITRE II" in u:
        return "II"
    if "CHAPITRE I" in u:
        return "I"
    if any(s in u for s in ("CONCLUSION", "CRITIQUES", "RÉFÉRENCES", "WEBOGRAPHIE", "ANNEXES")):
        return "SORTIE"
    if "INTRODUCTION" in u:
        return "INTRO"
    return None


CAP = re.compile(r"^(Figure|Tableau)\s+([IVX]+\.)?(\d+)\s*(?:—|-)\s*(.*)$")

def renumber():
    chapter = "INTRO"
    fig = {"INTRO": 0, "I": 0, "II": 0, "III": 0}
    tab = dict(fig)
    mapping = {}
    changed = 0
    for el in elems():
        if el.tag != qn("w:p"):
            continue
        p = Paragraph(el, doc)
        t = p.text.strip()
        if not t:
            continue
        if p.style.name == "Heading 1":
            c = chap_of(t)
            if c:
                chapter = c
            continue
        if chapter not in fig:
            continue
        m = CAP.match(t)
        if not m or p.style.name != "Normal":
            continue
        kind_w, pref, num, label = m.groups()
        old_key = f"{kind_w} {pref or ''}{num}".strip()
        if kind_w == "Figure":
            fig[chapter] += 1
            n = fig[chapter]
        else:
            tab[chapter] += 1
            n = tab[chapter]
        prefix = "" if chapter == "INTRO" else f"{chapter}."
        new_key = f"{kind_w} {prefix}{n}"
        mapping[old_key] = new_key
        new_t = f"{new_key} — {label.strip()}"
        if new_t != t:
            if p.runs:
                set_text(el, new_t)
                for r in p.runs:
                    r.italic = True
                    r.font.size = Pt(9)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                changed += 1
    return mapping, changed


mapping, changed = renumber()
note(f"legendes renumerotees : {changed}")

# renvois internes
REF = re.compile(r"\b(Figure|Tableau|figure|tableau)\s+([IVX]+\.)?(\d+)\b")
fixed = 0
for el in elems():
    if el.tag != qn("w:p"):
        continue
    p = Paragraph(el, doc)
    if p.style.name != "Normal":
        continue
    t = p.text
    if not t or not REF.search(t):
        continue
    if CAP.match(t.strip()):
        continue

    def repl(mo):
        key = f"{mo.group(1).capitalize()} {mo.group(2) or ''}{mo.group(3)}".strip()
        return mapping.get(key, mo.group(0))

    new = REF.sub(repl, t)
    if new != t:
        set_text(el, new)
        fixed += 1
note(f"renvois internes corriges : {fixed}")

doc.save(DOC)
print(f"\nPasse 11 terminee : {len(log)} operations")