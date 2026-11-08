# -*- coding: utf-8 -*-
"""Elimine les formulations residuelles de type 'architecture en couches'
et corrige quelques coquilles."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"

REPL = [
    # paragraphe sur la structure en packages (suppression de la logique 'couche')
    ("La structure en packages permet une séparation claire des responsabilités et facilite "
     "la maintenabilité du code. Chaque couche ne dépend que de la couche adjacente : le "
     "contrôleur dépend du service, le service dépend du repository, et le repository dépend "
     "de l'entité. Cette dépendance unidirectionnelle réduit les couplages et facilite les "
     "tests unitaires par mock (Mockito). Les exceptions sont gérées centralisément via "
     "@ControllerAdvice et @ExceptionHandler, garantissant des réponses d'erreur uniformes et "
     "structurées pour tous les endpoints.",
     "Cette organisation permet une séparation claire des responsabilités et facilite la "
     "maintenabilité du code. Les dépendances entre packages restent unidirectionnelles : un "
     "contrôleur invoque un service, le service s’appuie sur un ou plusieurs repositories, et "
     "les repositories manipulent les entités. Ce sens unique de dépendance réduit les "
     "couplages et rend les services testables par simulation (Mockito). Les exceptions sont "
     "gérées de manière centralisée via @ControllerAdvice et @ExceptionHandler, ce qui garantit "
     "des réponses d’erreur uniformes et structurées pour tous les endpoints."),

    ("Chaque règle est implémentée dans la couche Service du système et validée par des tests "
     "d'intégration correspondants.",
     "Chaque règle est implémentée dans les services du système et validée par les tests "
     "d’intégration correspondants."),

    ("Chaque besoin a été implémenté dans les couches appropriées du système et validé par des "
     "tests d'intégration spécifiques.",
     "Chaque besoin a été implémenté dans les composants appropriés du système et validé par "
     "des tests d’intégration spécifiques."),

    ("de la couche HTTP à la base de données", "de l’interface HTTP à la base de données"),
    ("de la couche API à la base de données", "de l’API à la base de données"),
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
print("paragraphes reformules :", n)