# -*- coding: utf-8 -*-
"""Extrait les blocs PlantUML (@startuml ... @enduml) depuis le transcript JSONL."""
import json
import os
import re

TRANSCRIPT = r"C:\Users\user\.cursor\projects\c-Users-user-Desktop-memoire\agent-transcripts\6c375dff-b9b7-4644-850b-eb0580695f45\6c375dff-b9b7-4644-850b-eb0580695f45.jsonl"
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memoire_assets", "puml_src"))

BLOCK = re.compile(r"@startuml[^\n]*\n.*?@enduml", re.DOTALL)
TITLE = re.compile(r"title\s+(.+)")


def walk_strings(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)
    elif isinstance(obj, str):
        yield obj


blocks = []
seen = set()
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for lineno, line in enumerate(fh, 1):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for text in walk_strings(obj):
            if "@startuml" not in text:
                continue
            for m in BLOCK.finditer(text):
                src = m.group(0).strip()
                key = src
                if key in seen:
                    continue
                seen.add(key)
                blocks.append((lineno, src))

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

for i, (lineno, src) in enumerate(blocks, 1):
    title = TITLE.search(src)
    name = f"bloc{i:02d}_L{lineno}.puml"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(src + "\n")
    print(f"{name}: {len(src)} car | {title.group(1).strip() if title else '(sans titre)'}")
print(f"\n{len(blocks)} blocs extraits -> {OUT}")
