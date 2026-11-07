# -*- coding: utf-8 -*-
"""Passe 8 : Securite -> III.3.9.4, correction du trou III.3.2, typographie."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

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


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Securite -> III.3.9.4 (Heading 4)
# ===========================================================================
items = elems()
k = index_of(lambda e: is_h(e) and txt(e).startswith("III.5.4"), items=items)
if k != -1:
    set_text(items[k], "III.3.9.4 Sécurité")
    set_style(items[k], "Heading4")
    note("Securite -> III.3.9.4")
else:
    note("[!] III.5.4 introuvable")

# ===========================================================================
# 2. Combler le trou de numerotation III.3.2 (ancienne section FIFO supprimee)
#    -> renumeroter a partir de III.3.3
# ===========================================================================
items = elems()
i_sec = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
i_end = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_sec + 1, items=items)
items = elems()

h3 = [k for k in range(i_sec + 1, i_end) if is_h(items[k], 3)]
for pos, k in enumerate(h3, 1):
    t = txt(items[k])
    m = re.match(r"^III\.3\.(\d+)\s+(.+)$", t)
    if not m:
        continue
    if int(m.group(1)) != pos:
        set_text(items[k], f"III.3.{pos} {m.group(2)}")
        note(f"renum : {t[:28]} -> III.3.{pos}")

# Renumeroter les Heading4 en consequence (III.3.x.y)
items = elems()
i_sec = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.3"), items=items)
i_end = index_of(lambda e: is_h(e, 1) and txt(e).startswith("CONCLUSION"), start=i_sec + 1, items=items)
items = elems()

cur_h3 = None
sub = 0
for k in range(i_sec + 1, i_end):
    el = items[k]
    if is_h(el, 3):
        m = re.match(r"^III\.3\.(\d+)", txt(el))
        cur_h3 = m.group(1) if m else None
        sub = 0
    elif is_h(el, 4) and cur_h3:
        sub += 1
        t = txt(el)
        label = re.sub(r"^III\.\d+\.\d+(\.\d+)?\s*", "", t)
        new = f"III.3.{cur_h3}.{sub} {label}"
        if new != t:
            set_text(el, new)
            note(f"renum h4 : {t[:34]} -> {new[:34]}")

doc.save(DOC)
print(f"\nPasse 8 terminee : {len(log)} operations")