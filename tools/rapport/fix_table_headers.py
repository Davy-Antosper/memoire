# -*- coding: utf-8 -*-
"""Rend les en-tetes de tableaux repetes sur chaque page et
aligne la typographie des cellules (Times New Roman 11 pt)."""
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"
FONT = "Times New Roman"

doc = Document(DOC)
n_tables = 0
n_runs = 0

for t in doc.tables:
    # 1. repetition de l'en-tete
    tr = t.rows[0]._tr
    trPr = tr.find(qn("w:trPr"))
    if trPr is None:
        trPr = tr.makeelement(qn("w:trPr"), {})
        tr.insert(0, trPr)
    if trPr.find(qn("w:tblHeader")) is None:
        trPr.append(trPr.makeelement(qn("w:tblHeader"), {}))
    n_tables += 1

    # 2. typographie des cellules
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    if r.font.name != "Consolas":
                        r.font.name = FONT
                        rPr = r._element.get_or_add_rPr()
                        for rf in rPr.findall(qn("w:rFonts")):
                            for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                                rf.set(qn(attr), FONT)
                        if r.font.size is None:
                            r.font.size = Pt(11)
                        n_runs += 1

doc.save(DOC)
print("tableaux traites :", n_tables, "| runs harmonises :", n_runs)