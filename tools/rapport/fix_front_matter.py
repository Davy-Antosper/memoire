# -*- coding: utf-8 -*-
"""Elimine la page blanche entre le resume et la table des matieres :
supprime les paragraphes vides et remplace le saut de page manuel par
un 'saut avant paragraphe' sur le titre suivant."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)
pars = doc.paragraphs

# supprimer tous les paragraphes vides consecutifs dans le liminaire
# (index 33 a 46) puis poser page_break_before sur TABLE DES MATIÈRES
titles = {"RÉSUMÉ", "TABLE DES MATIÈRES", "DÉDICACE", "REMERCIEMENTS"}

removed = 0
for t in titles:
    pars = doc.paragraphs
    for i, p in enumerate(pars):
        if p.text.strip() == t:
            # retirer les paragraphes vides qui precedent
            j = i - 1
            while j >= 0 and not pars[j].text.strip():
                prev = pars[j]
                prev._element.getparent().remove(prev._element)
                removed += 1
                j -= 1
            # saut de page propre sur le titre + suppression du saut manuel
            p.paragraph_format.page_break_before = t != "RÉSUMÉ" or True
            for br in p._p.findall(
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r/"
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br"):
                p._p.remove(br)
            break

# supprimer les sauts de page manuels isoles restants avant le TOC
pars = doc.paragraphs
for i, p in enumerate(pars):
    if p.text.strip() == "TABLE DES MATIÈRES":
        j = i - 1
        while j >= 0 and not pars[j].text.strip():
            prev = pars[j]
            prev._element.getparent().remove(prev._element)
            removed += 1
            j -= 1
        break

doc.save(DOC)
print("paragraphes vides supprimes :", removed)