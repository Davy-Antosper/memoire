# -*- coding: utf-8 -*-
"""Telecharge les PNG des diagrammes PlantUML DIRECTEMENT depuis le serveur
(endpoint /png), sans passer par une conversion SVG -> PNG.

Le facteur d'echelle est injecte au rendu pour obtenir des images nettes
dans Word (>= 300 dpi effectifs), sans modifier les sources .puml.
"""
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from puml import url_for  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "memoire_assets"))
SRC = os.path.join(ASSETS, "puml_src")

SCALE = int(os.environ.get("PUML_SCALE", "2"))
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

    # injecter l'echelle juste avant @enduml, si absente
    if "scale " not in src.lower():
        src = src.replace("@enduml", "scale %d\n@enduml" % SCALE)

    out = os.path.join(ASSETS, stem + ".png")
    url = url_for(src, "png")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as resp:
            blob = resp.read()
        if blob[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("ce n'est pas un PNG (erreur PlantUML)")
        with open(out, "wb") as fh:
            fh.write(blob)
        from PIL import Image
        import io
        w, h = Image.open(io.BytesIO(blob)).size
        print("OK  %-24s %4dx%-5d %8.1f Ko" % (stem + ".png", w, h, len(blob) / 1024))
        ok.append(stem)
        time.sleep(0.7)
    except Exception as exc:
        print("KO  %-24s %s" % (stem + ".png", exc))
        ko.append(stem)

print("\n%d PNG telecharges" % len(ok) + (", echecs : %s" % ko if ko else ""))
sys.exit(1 if ko else 0)
