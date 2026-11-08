# -*- coding: utf-8 -*-
"""Aligne a gauche les entrees des sections references et webographie
(pour eviter l'etirement des URLs par la justification) et harmonise
la police des annexes."""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)

in_refs = False
count = 0
for p in doc.paragraphs:
    name = p.style.name
    if name == "Heading 1":
        title = p.text.strip().upper()
        in_refs = title.startswith("RÉFÉRENCES") or title.startswith("WEBOGRAPHIE")
        continue
    if in_refs and p.text.strip():
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r._element.rPr.rFonts.set(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cs",
                "Times New Roman")
        count += 1

doc.save(DOC)
print("entrees alignees a gauche :", count)