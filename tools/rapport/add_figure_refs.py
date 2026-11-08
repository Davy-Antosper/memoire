# -*- coding: utf-8 -*-
"""Ajoute les renvois explicites aux figures dans les paragraphes
introductifs qui en manquent (exigence de coherence figure / texte)."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

REPL = [
    # Figure I.1 - circuit de distribution
    ("Le circuit actuel de distribution des engrais",
     "Le circuit actuel de distribution des engrais est représenté à la Figure I.1"),

    # Figure III.3 - architecture
    ("L’architecture du système décrit l’organisation d’ensemble de la solution : "
     "les composants logiciels, leur rôle respectif et la manière dont ils communiquent.",
     "L’architecture du système décrit l’organisation d’ensemble de la solution : "
     "les composants logiciels, leur rôle respectif et la manière dont ils communiquent "
     "(Figure III.3)."),

    # Figure III.4 - ER
    ("Le modèle de données du système comprend 16 tables principales, modélisant "
     "l'ensemble des entités métier et leurs relations. Le diagramme Entité-Relation "
     "ci-dessus présente les relations entre les principales entités du système.",
     "Le modèle de données du système comprend seize tables principales, modélisant "
     "l’ensemble des entités métier et leurs relations. Le diagramme Entité-Relation "
     "(Figure III.4) présente ces relations, tandis que le diagramme de classes "
     "(Figure III.5) en donne la traduction orientée objet."),

    # Figure III.7 - sequence
    ("Le diagramme de séquence de la création et validation d'un ticket illustre le flux "
     "complet depuis la demande de l'agriculteur jusqu'à l'activation du ticket.",
     "Le diagramme de séquence de la création et validation d’un ticket (Figure III.7) "
     "illustre le flux complet depuis la demande de l’agriculteur jusqu’à l’activation "
     "du ticket."),
]


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
    for old, new in REPL:
        if old in p.text:
            rewrite(p, p.text.replace(old, new))
            n += 1
            break

doc.save(DOC)
print("renvois ajoutes :", n)