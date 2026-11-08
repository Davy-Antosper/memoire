# -*- coding: utf-8 -*-
"""Supprime la redondance entre l'intitule du circuit de distribution
et le paragraphe qui le decrit."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"


def rewrite(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)
n = 0
for p in doc.paragraphs:
    t = p.text
    if t.startswith("Le circuit actuel de distribution des engrais, représenté"):
        rewrite(p, "Le circuit de distribution des engrais")
        n += 1
    elif t.startswith("La distribution des engrais FOMI suit un circuit logistique"):
        rewrite(p,
                "La distribution des engrais FOMI suit un circuit logistique et administratif "
                "hiérarchisé, depuis l’usine de Maramvya jusqu’aux agriculteurs bénéficiaires "
                "(Figure I.1). Ce circuit, restructuré en conformité avec l’organisation "
                "territoriale du pays, implique une chaîne d’approvisionnement en quatre "
                "niveaux de stockage fixes, complétée par un système de distribution finale "
                "au niveau de chaque colline.")
        n += 1

doc.save(DOC)
print("paragraphes ajustes :", n)