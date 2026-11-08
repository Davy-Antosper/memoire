# -*- coding: utf-8 -*-
"""Remplace les mentions de l'algorithme FIFO dans les tableaux par des
formulations descriptives, sans supprimer les identifiants de code reels
(DistributionFifoIntegrationTest)."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

# (texte exact de cellule -> remplacement)
CELLS = {
    "Distribution aux agriculteurs selon l'algorithme FIFO":
        "Distribution aux agriculteurs par lots, selon leur date de réception",
    "Les lots dont la date de péremption est dépassée sont exclus de la distribution FIFO ; "
    "le chemin avec lot imposé doit encore être corrigé.":
        "Les lots dont la date de péremption est dépassée sont exclus de la distribution ; "
        "le chemin avec lot imposé doit encore être corrigé.",
    "L'allocation des engrais suit un algorithme FIFO basé sur la date de réception FOMI, "
    "après exclusion des lots périmés.":
        "L’allocation des engrais suit l’ordre des dates de réception FOMI, "
        "après exclusion des lots périmés.",
    "Déstockage automatique via l'algorithme FIFO":
        "Déstockage automatique par ordre de réception des lots",
    "NOT NULL DEFAULT NOW() (base FIFO)":
        "NOT NULL DEFAULT NOW() (base du tri par date)",
    "FIFO multi-lots, partiel, complet":
        "Sorties multi-lots, partielles et complètes",
    "Distribution FIFO":
        "Distribution par lots",
    "Distribuer des engrais (FIFO)":
        "Distribuer des engrais",
}


def set_cell(cell, text):
    p = cell.paragraphs[0]
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""
    else:
        p.add_run(text)
    # supprimer les paragraphes surnumeraires de la cellule
    for extra in cell.paragraphs[1:]:
        if not extra.text.strip():
            extra._element.getparent().remove(extra._element)


doc = Document(DOC)
n = 0
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            txt = cell.text.strip()
            if txt in CELLS:
                set_cell(cell, CELLS[txt])
                n += 1

# cas particulier : le nom du test reste un identifiant de code
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            if "DistributionFifoIntegrationTest" in cell.text:
                # conserver le nom de classe, reformuler la categorie si besoin
                pass

doc.save(DOC)
print("cellules reformulees :", n)