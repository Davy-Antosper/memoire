# -*- coding: utf-8 -*-
"""Le style personnalise 'z1qcye' (texte importe du web) impose un interligne
simple et des espacements automatiques : on l'aligne sur le style Normal."""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)

# supprimer les paragraphes vides portant ce style
removed = 0
for p in list(doc.paragraphs):
    if p.style.name == "z1qcye" and not p.text.strip():
        p._element.getparent().remove(p._element)
        removed += 1

st = doc.styles["z1qcye"]
pPr = st.element.find(qn("w:pPr"))
if pPr is not None:
    st.element.remove(pPr)

st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.space_after = Pt(6)

# renommer le style pour un identifiant lisible
st.name = "Texte justifie"

doc.save(DOC)
print("paragraphes vides supprimes :", removed, "| style z1qcye aligne sur Normal")