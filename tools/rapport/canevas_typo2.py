# -*- coding: utf-8 -*-
"""Passe 10 : reprise de la numerotation des figures/tableaux + renvois internes."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(DOC)
body = doc.element.body


def txt(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def elems():
    sectPr = body.find(qn("w:sectPr"))
    return [c for c in body.iterchildren() if c is not sectPr]


def chap_of(heading_text):
    u = heading_text.upper()
    if "CHAPITRE III" in u:
        return "III"
    if "CHAPITRE II" in u:
        return "II"
    if "CHAPITRE I" in u:
        return "I"
    if "CONCLUSION" in u or "CRITIQUES" in u or "RÉFÉRENCES" in u or "WEBOGRAPHIE" in u or "ANNEXES" in u:
        return "SORTIE"
    if "INTRODUCTION" in u:
        return "INTRO"
    return None


from docx.text.paragraph import Paragraph

chapter = "INTRO"
fig_n = {"INTRO": 0, "I": 0, "II": 0, "III": 0}
tab_n = {"INTRO": 0, "I": 0, "II": 0, "III": 0}
mapping = {}  # (kind, old_label) -> new_label
current = {}

renames = []
for el in elems():
    if el.tag == qn("w:p"):
        p = Paragraph(el, doc)
        t = p.text.strip()
        if not t:
            continue
        if p.style.name == "Heading 1":
            c = chap_of(t)
            if c:
                chapter = c
            continue
        if chapter == "SORTIE" or chapter not in fig_n:
            continue
        m = re.match(r"^(Figure|Tableau)\s+([IVX]+\.)?(\d+)\s*(—|-)\s*(.*)$", t)
        if m and p.style.name == "Normal":
            kind_w = m.group(1)
            old = f"{kind_w} {m.group(2) or ''}{m.group(3)}"
            label = m.group(5).strip()
            if kind_w == "Figure":
                fig_n[chapter] += 1
                num = fig_n[chapter]
            else:
                tab_n[chapter] += 1
                num = tab_n[chapter]
            prefix = "" if chapter == "INTRO" else f"{chapter}."
            new = f"{kind_w} {prefix}{num} — {label}"
            current[id(p)] = new
            mapping[old.replace("  ", " ").strip()] = f"{kind_w} {prefix}{num}"
            if new != t:
                renames.append((p, new))

print(f"legendes renumérotees : {len(renames)}")
for p, new in renames:
    if p.runs:
        p.runs[0].text = new
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
print("\nNouvelle numerotation :")
for k, v in mapping.items():
    print(f"   {k:16s} -> {v}")

# ---------------------------------------------------------------------------
# Renvois internes : « (Figure III.5) », « figure III.3 », « Figure I.1 »
# ---------------------------------------------------------------------------
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
    # ne pas toucher aux legendes elles-memes
    if re.match(r"^\s*(Figure|Tableau)\s+[IVX]*\.?\d+\s*—", t):
        continue

    def repl(mo):
        kind_w, pref, num = mo.group(1), mo.group(2), mo.group(3)
        key = f"{kind_w.capitalize()} {pref or ''}{num}"
        return mapping.get(key, mo.group(0))

    new = REF.sub(repl, t)
    if new != t and p.runs:
        p.runs[0].text = new
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
        fixed += 1
print(f"\nrenvois internes corriges : {fixed}")

doc.save(DOC)
print("Passe 10 terminee")