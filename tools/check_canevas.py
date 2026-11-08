# -*- coding: utf-8 -*-
"""Compare la structure du rapport au canevas exige."""
import re
import sys

from docx import Document

CANEVAS = [
    ("H1", "INTRODUCTION GENERALE"),
    ("H2", "Contexte et justification"),
    ("H2", "Problématique"),
    ("H2", "Objectifs"),
    ("H3", "Objectif global"),
    ("H3", "Objectifs spécifiques"),
    ("H2", "Hypothèses de recherche"),
    ("H2", "Méthodologie de recherche"),
    ("H2", "Intérêt du sujet"),
    ("H2", "Délimitation du Sujet"),
    ("H2", "Articulations"),
    ("H1", "CHAPITRE I : PRESENTATION DU LIEU DE STAGE"),
    ("H2", "I.1. Introduction"),
    ("H2", "I.2. Historique de l’institution"),
    ("H2", "I.3. Situation géographique"),
    ("H2", "I.4. Vision, missions et objectifs de l’institution"),
    ("H2", "I.5. Structure organisationnelle"),
    ("H2", "I.6. Déroulement du stage"),
    ("H3", "I.6.1. Introduction"),
    ("H3", "I.6.2. Activités réalisées"),
    ("H3", "I.6.3. Etude de l’existant"),
    ("H4", "Critique de l’existant"),
    ("H4", "Solution proposée"),
    ("H3", "I.6.4. Corrélation du stage avec les Eléments Constitutifs des Unités d’Enseignement"),
    ("H1", "CHAPITRE II : CONCEPTS THEORIQUES ET METHODOLOGIE DE L’ETUDE"),
    ("H2", "II.1. Concepts théoriques"),
    ("H2", "II.2. Méthodologie de l’étude"),
    ("H1", "CHAPITRE III : PRESENTATION DES RESULTATS"),
    ("H1", "CONCLUSION GENERALE"),
    ("H1", "CRITIQUES, SUGGESTIONS ET RECOMMANDATIONS"),
]

doc = Document(sys.argv[1])
heads = [(p.style.name, p.text.strip()) for p in doc.paragraphs if p.style.name.startswith("Heading")]


def norm(s):
    s = s.strip().rstrip(".")
    s = re.sub(r"\s+", " ", s)
    s = s.replace("É", "E").replace("È", "E").replace("Ê", "E")
    s = s.replace("é", "e").replace("è", "e").replace("ê", "e")
    s = s.replace("'", "'").replace("’", "'")
    return s.lower()


print(f"{'CANEVAS':55s} | {'RAPPORT':55s} | OK")
print("-" * 125)
missing = []
NUM = re.compile(r"^(\d+|[ivx]+)\.(\d+\.?)*\s*", re.IGNORECASE)

for lvl, label in CANEVAS:
    want = norm(NUM.sub("", label))
    found = None
    for sname, text in heads:
        t = norm(NUM.sub("", text))
        if t.startswith(want[:32]) or want.startswith(t[:32]):
            found = text
            break
    ok = "OK" if found else "MANQUANT"
    if not found:
        missing.append(label)
    print(f"{label[:55]:55s} | {(found or '—')[:55]:55s} | {ok}")

print()
print(f"{len(CANEVAS) - len(missing)}/{len(CANEVAS)} sections conformes")
if missing:
    print("Manquantes :", missing)