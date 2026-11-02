# -*- coding: utf-8 -*-
"""Construit le rapport de stage FOMI au format du canevas du professeur.

Etapes :
    1. canevas_restructure.py : restructuration du mémoire selon le canevas ;
    2. canevas_fixfacts.py    : mise à jour des faits techniques (API réelle) ;
    3. canevas_finalize.py    : numérotation, renvois internes, annexes de code.

Usage :
    python build_rapport.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["canevas_restructure.py", "canevas_fixfacts.py", "canevas_finalize.py"]

env = dict(os.environ)
env.setdefault("PYTHONIOENCODING", "utf-8")

for step in STEPS:
    path = os.path.join(HERE, step)
    print(f"\n=== {step} ===")
    result = subprocess.run([sys.executable, path], cwd=HERE, env=env)
    if result.returncode != 0:
        print(f"\nECHEC de {step} (code {result.returncode})")
        sys.exit(result.returncode)

print("\n=== TERMINE ===")
print("Rapport généré :", os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx"))
