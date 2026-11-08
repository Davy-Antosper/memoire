# -*- coding: utf-8 -*-
"""Force les polices de theme (majorFont/minorFont) sur Times New Roman
et nettoie les runs/tables residuels en Arial."""
import re
import shutil
import zipfile
import os
from docx import Document
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"
FONT = "Times New Roman"


# ---------- 1. polices de theme ----------
src = DOC
tmp = DOC + ".tmp"
with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/theme/theme1.xml":
            txt = data.decode("utf-8")
            txt = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*(")',
                         r'\g<1>' + FONT + r'\g<2>', txt)
            txt = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*(")',
                         r'\g<1>' + FONT + r'\g<2>', txt)
            # neutraliser les polices de script (Jpan, Hang, etc.)
            data = txt.encode("utf-8")
        zout.writestr(item, data)
os.replace(tmp, DOC)

# ---------- 2. runs Arial restants ----------
doc = Document(DOC)
fixed = 0
for p in doc.paragraphs:
    for r in p.runs:
        if r.font.name and r.font.name.lower() in ("arial", "calibri", "cambria"):
            r.font.name = FONT
            fixed += 1
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    if r.font.name and r.font.name.lower() in ("arial", "calibri", "cambria"):
                        r.font.name = FONT
                        fixed += 1

# rFonts residuels avec des polices nommees autres que Times/Consolas
for p in doc.paragraphs:
    for r in p.runs:
        rPr = r._element.find(qn("w:rPr"))
        if rPr is None:
            continue
        for rf in rPr.findall(qn("w:rFonts")):
            names = [rf.get(qn("w:ascii")), rf.get(qn("w:hAnsi")), rf.get(qn("w:cs"))]
            if any(n and n not in (FONT, "Consolas") for n in names):
                for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                    rf.set(qn(attr), FONT)
                fixed += 1

doc.save(DOC)
print("runs/rFonts corriges :", fixed)