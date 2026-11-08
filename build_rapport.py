# -*- coding: utf-8 -*-
"""Met à jour le rapport de stage FOMI (canevas du professeur).

Le rapport de référence est `Rapport_stage_FOMI_canevas.docx`, restructuré
selon le canevas du promoteur (voir l'historique dans `tools/rapport/`).

Cette commande applique uniquement la passe de cohérence métier
`update_docx_model.py` : modèle Province -> Commune -> Zone -> Colline,
dépôts limités à PROVINCE et ZONE, et compteurs à jour (17 tables,
13 migrations, 65 endpoints). La passe est idempotente.

Usage :
    python build_rapport.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["update_docx_model.py"]

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
print("Rapport mis à jour :", os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx"))
