# -*- coding: utf-8 -*-
"""Renomme la section III.2.3 au singulier (un seul diagramme de sequence
restant) et reecrit son paragraphe introductif."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

INTRO = (
    "Le diagramme de séquence modélise les interactions entre les composants du "
    "système lors d’une opération critique. Il illustre l’échange chronologique des "
    "messages entre l’utilisateur, l’API, les services métier et la base de données. "
    "Le scénario retenu est la création et la validation d’un ticket, qui constitue "
    "le point d’entrée du processus de distribution."
)


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
    if p.style.name.startswith("Heading") and "Diagrammes de séquence" in p.text:
        rewrite(p, "III.2.3 Diagramme de séquence")
        n += 1
    elif p.text.startswith("Les diagrammes de séquence modélisent"):
        rewrite(p, INTRO)
        n += 1

doc.save(DOC)
print("corrections :", n)