# -*- coding: utf-8 -*-
"""Audit typographique : styles, polices et tailles reellement utilises."""
import collections
import sys

from docx import Document
from docx.oxml.ns import qn

doc = Document(sys.argv[1])

print("=== STYLES DE PARAGRAPHE ===")
for s in doc.styles:
    if s.type is None or s.type != 1:
        continue
    f = s.font
    print(f"{s.name:20s} | font={str(f.name):18s} | size={str(f.size.pt if f.size else None):8s} "
          f"| bold={str(f.bold):5s} | color={f.color.rgb if f.color and f.color.rgb else None}")

print("\n=== POLICES DIRECTES DANS LES RUNS (par style) ===")
counter = collections.Counter()
sizes = collections.Counter()
for p in doc.paragraphs:
    st = p.style.name
    for r in p.runs:
        if not r.text.strip():
            continue
        counter[(st, r.font.name or "(hérité)")] += 1
        sizes[(st, r.font.size.pt if r.font.size else None)] += 1

for (st, fname), n in counter.most_common(30):
    print(f"{n:5d} | {st:18s} | {fname}")

print("\n=== TAILLES DIRECTES (par style) ===")
for (st, sz), n in sizes.most_common(30):
    print(f"{n:5d} | {st:18s} | {sz}")

print("\n=== STYLE PAR DEFAUT (docDefaults) ===")
styles_el = doc.styles.element
rpr = styles_el.find(qn('w:docDefaults') + '/' + qn('w:rPrDefault') + '/' + qn('w:rPr'))
print("rPrDefault:", rpr is not None)
if rpr is not None:
    from lxml import etree
    print(etree.tostring(rpr, pretty_print=True).decode()[:800])