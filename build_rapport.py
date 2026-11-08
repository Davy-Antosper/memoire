# -*- coding: utf-8 -*-
"""Met à jour le rapport de stage FOMI (canevas du professeur).

Le rapport de référence est `Rapport_stage_FOMI_canevas.docx`, restructuré
selon le canevas du promoteur (voir l'historique dans `tools/rapport/`).

Trois passes idempotentes, dans cet ordre :

1. `update_docx_model.py` — modèle métier Province -> Commune -> Zone ->
   Colline, dépôts limités à PROVINCE et ZONE, compteurs de base ;
2. `update_docx_fomi_model.py` — alignement sur le code réel : gamme FOMI
   (Urée à la place de Totahaza, dolomie en sac de 25 kg), 18 tables,
   18 migrations, 68 endpoints, 232 tests, statut ARRIERE, réclamations
   dans les tableaux et l'annexe B ;
3. `update_docx_diagrams.py` — réinjection des figures PlantUML régénérées,
   proportions conservées.

Usage :
    python build_rapport.py            # met à jour le DOCX
    python build_rapport.py --pdf      # met à jour le DOCX puis le PDF
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["update_docx_model.py", "update_docx_fomi_model.py", "update_docx_diagrams.py"]

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

if "--pdf" in sys.argv:
    print("\n=== to_pdf.py ===")
    result = subprocess.run([sys.executable, os.path.join(HERE, "to_pdf.py")], cwd=HERE, env=env)
    sys.exit(result.returncode)
