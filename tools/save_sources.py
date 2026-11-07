# -*- coding: utf-8 -*-
"""Sauve les sources PlantUML reelles (decodees des URLs livrees) et rend PNG+SVG."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from puml import decode, fetch  # noqa: E402

TRANSCRIPT = r"C:\Users\user\.cursor\projects\c-Users-user-Desktop-memoire\agent-transcripts\6c375dff-b9b7-4644-850b-eb0580695f45\6c375dff-b9b7-4644-850b-eb0580695f45.jsonl"
ASSETS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memoire_assets"))
SRC = os.path.join(ASSETS, "puml_src")

URL = re.compile(r"plantuml\.com/plantuml/svg/([A-Za-z0-9_-]{40,})")

# titre PlantUML -> nom de fichier
NAMES = {
    "Diagramme de classes": "class_diagram",
    "Distribution d'engrais": "sequence_distribution",
    "Création et validation": "sequence_ticket",
    "Machine à états": "ticket_state_machine",
    "Diagramme de déploiement": "deployment_diagram",
    "Diagramme d'activités": "activity_diagram",
    "Cas d'utilisation": "use_case_diagram",
    "Modèle physique de données": "er_diagram",
}


def walk_strings(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)
    elif isinstance(obj, str):
        yield obj


encs = []
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for line in fh:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for text in walk_strings(obj):
            if "plantuml.com/plantuml/svg" not in text:
                continue
            for enc in URL.findall(text):
                if enc not in encs:
                    encs.append(enc)

os.makedirs(SRC, exist_ok=True)
saved = 0
for enc in encs:
    src = decode(enc).strip()
    if len(src) < 100:
        continue
    title = ""
    for ln in src.splitlines():
        if ln.strip().lower().startswith("title"):
            title = ln.strip()[5:].strip()
            break
    name = next((v for k, v in NAMES.items() if title.startswith(k)), None)
    if name is None:
        print(f"[skip] titre inconnu: {title[:50]}")
        continue
    with open(os.path.join(SRC, name + ".puml"), "w", encoding="utf-8") as fh:
        fh.write(src + "\n")
    print(f"[src] {name}.puml  ({len(src)} car)  <- {title[:55]}")
    saved += 1

print(f"\n{saved} sources sauvegardees dans {SRC}")