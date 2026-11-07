# -*- coding: utf-8 -*-
"""Remplace les paragraphes vides porteurs d'un saut de page par un
'saut avant' sur le titre qui suit (evite les pages blanches)."""
from docx import Document
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = Document(DOC)
removed = 0

changed = True
while changed:
    changed = False
    pars = doc.paragraphs
    for i, p in enumerate(pars):
        # paragraphe vide contenant un saut de page manuel
        has_br = any(br.get(qn("w:type")) == "page" for br in p._p.iter(qn("w:br")))
        if has_br and not p.text.strip():
            # chercher le prochain paragraphe non vide
            nxt = None
            for j in range(i + 1, len(pars)):
                if pars[j].text.strip():
                    nxt = pars[j]
                    break
            if nxt is not None and nxt.style.name.startswith("Heading"):
                nxt.paragraph_format.page_break_before = True
                p._element.getparent().remove(p._element)
                removed += 1
                changed = True
                break

doc.save(DOC)
print("sauts de page convertis en 'page_break_before' :", removed)