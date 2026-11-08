# -*- coding: utf-8 -*-
"""Affiche le texte complet des elements entre deux index du dump."""
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

path = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
doc = Document(path)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
elems = [c for c in body.iterchildren() if c is not sectPr]

for i, child in enumerate(elems):
    if not (start <= i <= end):
        continue
    if child.tag == qn('w:p'):
        p = Paragraph(child, doc)
        has_img = bool(child.findall('.//' + qn('w:drawing')))
        txt = p.text.strip()
        if not txt and not has_img:
            continue
        print(f"--- [{i}] {p.style.name} {'[IMG] ' if has_img else ''}")
        print(txt)
    elif child.tag == qn('w:tbl'):
        t = Table(child, doc)
        print(f"--- [{i}] TABLE {len(t.rows)}x{len(t.columns)}")
        for row in t.rows[:3]:
            print("   | " + " | ".join(c.text.strip()[:40] for c in row.cells))
        if len(t.rows) > 3:
            print(f"   ... ({len(t.rows)} lignes)")