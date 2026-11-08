# -*- coding: utf-8 -*-
"""Corrige les effectifs reels des packages et reformule la phrase
'architecture en packages par couche technique'."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

# effectifs reels comptes dans fomi-stock-api
REAL = {
    "controller": "17 classes",
    "service": "14 classes",
    "repository": "16 interfaces",
    "model/entity": "16 classes",
    "model/enums": "6 enums",
    "dto": "34 classes",
    "security": "4 classes",
    "config": "1 classe",
    "exception": "3 classes",
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


doc = Document(DOC)
tbl_fixed = 0

for t in doc.tables:
    header = [c.text.strip() for c in t.rows[0].cells]
    if header[:1] == ["Package"] and "Nombre de classes" in header:
        for row in t.rows[1:]:
            pkg = row.cells[0].text.strip()
            if pkg in REAL:
                if row.cells[2].text.strip() != REAL[pkg]:
                    set_cell(row.cells[2], REAL[pkg])
                    tbl_fixed += 1

para_fixed = 0
OLD = "Le projet suit une architecture en packages organisés par couche technique, chaque package regroupant les classes ayant une responsabilité commune."
NEW = ("Le code source est organisé en packages, chacun regroupant les classes ayant "
       "une responsabilité commune : les contrôleurs exposent l’API, les services portent "
       "la logique métier, les repositories assurent l’accès aux données et les entités "
       "décrivent le modèle persistant.")
for p in doc.paragraphs:
    if OLD in p.text:
        runs = p.runs
        new_text = p.text.replace(OLD, NEW)
        runs[0].text = new_text
        for r in runs[1:]:
            r.text = ""
        para_fixed += 1

doc.save(DOC)
print("cellules corrigees :", tbl_fixed, "| paragraphes :", para_fixed)