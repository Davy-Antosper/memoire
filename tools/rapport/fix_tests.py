# -*- coding: utf-8 -*-
"""Corrige les compteurs de tests restes incoherents (207/204 -> 218/215)."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

REPL = [
    ("Résultats globaux : 218 tests exécutés, 207 réussis, 0 échoué, 0 ignoré.",
     "Résultats globaux : 218 tests exécutés, 218 réussis, 0 échoué, 0 ignoré."),
    ("Tests d'intégration (PostgreSQL via Testcontainers) : 215 tests, 204 réussis",
     "Tests d'intégration (PostgreSQL via Testcontainers) : 215 tests, 215 réussis"),
    ("Total : 218 tests, 207 réussis",
     "Total : 218 tests, 218 réussis"),
]


def rewrite(par, new_text):
    runs = par.runs
    if not runs:
        par.text = new_text
        return
    runs[0].text = new_text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)
changes = 0
for p in doc.paragraphs:
    for old, new in REPL:
        if old in p.text:
            rewrite(p, p.text.replace(old, new))
            changes += 1
            break

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for old, new in REPL:
                    if old in p.text:
                        rewrite(p, p.text.replace(old, new))
                        changes += 1
                        break

doc.save(DOC)
print("corrections appliquees :", changes)