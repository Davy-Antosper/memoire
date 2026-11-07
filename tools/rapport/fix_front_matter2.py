# -*- coding: utf-8 -*-
"""Nettoie le liminaire : supprime les paragraphes vides inutiles et
remplace les sauts de page manuels par un saut avant paragraphe."""
from docx import Document
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = Document(DOC)

TITLES = ["DÉDICACE", "REMERCIEMENTS", "RÉSUMÉ", "TABLE DES MATIÈRES"]
removed = 0

for title in TITLES:
    # 1. supprimer les paragraphes vides qui precedent le titre
    while True:
        pars = doc.paragraphs
        target = None
        for i, p in enumerate(pars):
            if p.text.strip() == title and p.style.name == "Normal":
                target = i
                break
        if target is None:
            break

        # retirer les paragraphes vides precedents
        j = target - 1
        n_removed = 0
        while j >= 0 and not pars[j].text.strip():
            prev = pars[j]
            prev._element.getparent().remove(prev._element)
            n_removed += 1
            j -= 1
        removed += n_removed

        # 2. poser le saut de page sur le titre
        p = doc.paragraphs[target - n_removed]
        p.paragraph_format.page_break_before = True

        # 3. supprimer les sauts de page manuels DANS les runs du titre
        for r in p._p.findall(W + "r"):
            for br in r.findall(W + "br"):
                r.remove(br)
        break

# 4. supprimer les paragraphes vides restants entre RESUME et TOC
while True:
    pars = doc.paragraphs
    idx = None
    for i, p in enumerate(pars):
        if p.text.strip() == "TABLE DES MATIÈRES":
            idx = i
            break
    if idx is None:
        break
    j = idx - 1
    n = 0
    while j >= 0 and not pars[j].text.strip():
        prev = pars[j]
        prev._element.getparent().remove(prev._element)
        n += 1
        j -= 1
    removed += n
    break

# 5. supprimer le champ TOC residuel eventuel dans un run vide
doc.save(DOC)
print("paragraphes vides supprimes :", removed)