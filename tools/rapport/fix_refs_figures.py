# -*- coding: utf-8 -*-
"""Corrige les renvois de figures errones et nettoie une legende."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"


def set_text(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)
fixed = 0

for p in doc.paragraphs:
    t = p.text
    new = t
    if "diagramme de cas d'utilisation (Figure III.6)" in t:
        new = new.replace("diagramme de cas d'utilisation (Figure III.6)",
                          "diagramme de cas d'utilisation (Figure III.1)")
    if "diagramme d'activités (Figure III.7)" in t:
        new = new.replace("diagramme d'activités (Figure III.7)",
                          "diagramme d'activités (Figure III.2)")
    if "Figure III.4 — Diagramme Entité-Relation (régénéré avec résolution améliorée)" in t:
        new = new.replace(
            "Figure III.4 — Diagramme Entité-Relation (régénéré avec résolution améliorée)",
            "Figure III.4 — Diagramme Entité-Relation")
    if new != t:
        set_text(p, new)
        fixed += 1

doc.save(DOC)
print("renvois/legendes corriges :", fixed)