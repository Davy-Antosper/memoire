# -*- coding: utf-8 -*-
"""Rend tous les diagrammes PlantUML (memoire_assets/puml_src/*.puml) en PNG et SVG."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from puml import fetch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "memoire_assets"))
SRC = os.path.join(ASSETS, "puml_src")

only = sys.argv[1:] or None
ok, ko = [], []

for name in sorted(os.listdir(SRC)):
    if not name.endswith(".puml"):
        continue
    stem = name[:-5]
    if only and stem not in only:
        continue
    with open(os.path.join(SRC, name), encoding="utf-8") as fh:
        src = fh.read()
    for fmt, ext in (("png", "png"), ("svg", "svg")):
        out = os.path.join(ASSETS, f"{stem}.{ext}")
        try:
            size, url = fetch(src, out, fmt)
            if size < 500:
                raise ValueError(f"reponse trop petite ({size} o) — erreur PlantUML probable")
            print(f"OK  {stem}.{ext:3s} {size:>7d} o")
            time.sleep(0.6)
        except Exception as exc:
            print(f"KO  {stem}.{ext:3s} : {exc}")
            ko.append(f"{stem}.{ext}")
            continue
    ok.append(stem)

print(f"\n{len(ok)} diagrammes rendus" + (f", {len(ko)} echecs : {ko}" if ko else ""))
sys.exit(1 if ko else 0)