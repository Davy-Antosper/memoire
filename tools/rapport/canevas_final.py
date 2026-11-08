# -*- coding: utf-8 -*-
"""Passe finale : numerotation complete des figures/tableaux, renvois,
et controle global de coherence."""
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


CAP = re.compile(r"^(Figure|Tableau)\s+([IVX]+\.)?(\d+)?\s*(?:—|-)?\s*(.*)$")
CAP_NUM = re.compile(r"^(Figure|Tableau)\s+([IVX]+\.)?(\d+)\s*(?:—|-)\s*(.*)$")

# --- 1. attribuer un numero manquant aux legendes sans numero --------------
chapter = "INTRO"
fig = {"INTRO": 0, "I": 0, "II": 0, "III": 0}
tab = dict(fig)
mapping = {}
order = []

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
    if p.style.name != "Normal":
        continue
    m = CAP.match(t)
    if not m:
        continue
    if not t.startswith(("Figure", "Tableau")):
        continue
    kind_w, pref, num, label = m.groups()
    # une legende valide : commence par Figure/Tableau et a un numero ou un tiret
    if not label:
        continue
    if kind_w == "Figure":
        fig[chapter] += 1
        n = fig[chapter]
    else:
        tab[chapter] += 1
        n = tab[chapter]
    prefix = "" if chapter == "INTRO" else f"{chapter}."
    new_key = f"{kind_w} {prefix}{n}"
    if pref and num:
        mapping[f"{kind_w} {pref}{num}"] = new_key
    new_t = f"{new_key} — {label.strip()}"
    if new_t != t:
        set_text(el, new_t)
        for r in p.runs:
            r.italic = True
            r.font.size = Pt(9)
            r.bold = False
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    order.append(new_t)

print(f"legendes : {len(order)}")
for o in order:
    print("   " + o)

# --- 2. renvois internes ---------------------------------------------------
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
    if CAP_NUM.match(t.strip()):
        continue

    def repl(mo):
        key = f"{mo.group(1).capitalize()} {mo.group(2) or ''}{mo.group(3)}".strip()
        return mapping.get(key, mo.group(0))

    new = REF.sub(repl, t)
    if new != t:
        set_text(el, new)
        fixed += 1
print(f"\nrenvois corriges : {fixed}")

doc.save(DOC)

# --- 3. controle final -----------------------------------------------------
print("\n=== CONTROLE FINAL ===")
d2 = Document(DOC)
FORBIDDEN = ["architecture en couches", "layered", "machine à états", "RBAC",
             "PNSEB", "http://", "https://", "Source :"]
issues = []
for p in d2.paragraphs:
    for f in FORBIDDEN:
        if f in p.text:
            issues.append((f, p.text[:120]))
for t in d2.tables:
    for row in t.rows:
        for c in row.cells:
            for f in FORBIDDEN:
                if f in c.text:
                    issues.append((f, c.text[:120]))
if issues:
    print(f"{len(issues)} mentions a verifier :")
    seen = set()
    for f, t in issues:
        if (f, t[:60]) in seen:
            continue
        seen.add((f, t[:60]))
        print(f"   [{f}] {t}")
else:
    print("aucune mention interdite")

# numerotation des titres
print("\n=== TITRES ===")
for p in d2.paragraphs:
    if p.style.name.startswith("Heading"):
        print(f"{p.style.name:12s} | {p.text[:80]}")