# -*- coding: utf-8 -*-
"""Supprime la page blanche apres la table des matieres
(deux sauts de page consecutifs)."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)
pars = doc.paragraphs

# trouver le dernier paragraphe de la table des matieres
last_toc = max(i for i, p in enumerate(pars) if p.style.name.startswith("toc"))

removed = 0
# supprimer les paragraphes vides porteurs d'un saut de page juste apres le TOC,
# en conservant un seul saut avant INTRODUCTION
i = last_toc + 1
while i < len(pars):
    p = pars[i]
    if p.style.name.startswith("Heading"):
        break
    if "w:type=\"page\"" in p._p.xml and not p.text.strip():
        p._element.getparent().remove(p._element)
        removed += 1
        pars = doc.paragraphs  # reindex
        i = last_toc + 1
        continue
    i += 1

doc.save(DOC)
print("sauts de page vides supprimes apres le TOC :", removed)