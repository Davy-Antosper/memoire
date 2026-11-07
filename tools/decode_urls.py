# -*- coding: utf-8 -*-
"""Decode les URLs PlantUML du transcript et les compare aux sources extraites."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from puml import decode  # noqa: E402

TRANSCRIPT = r"C:\Users\user\.cursor\projects\c-Users-user-Desktop-memoire\agent-transcripts\6c375dff-b9b7-4644-850b-eb0580695f45\6c375dff-b9b7-4644-850b-eb0580695f45.jsonl"
SRC = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memoire_assets", "puml_src"))

URL = re.compile(r"plantuml\.com/plantuml/(svg|png)/([A-Za-z0-9_-]{40,})")


def walk_strings(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)
    elif isinstance(obj, str):
        yield obj


sources = {}
for f in os.listdir(SRC):
    with open(os.path.join(SRC, f), encoding="utf-8") as fh:
        sources[f] = fh.read().strip()

found = {}
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for line in fh:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for text in walk_strings(obj):
            if "plantuml.com/plantuml" not in text:
                continue
            for fmt, enc in URL.findall(text):
                found.setdefault(enc, fmt)

print(f"{len(found)} URLs uniques\n")
for enc, fmt in found.items():
    try:
        src = decode(enc).strip()
    except Exception as exc:
        print(f"[{fmt}] ECHEC decode: {exc}")
        continue
    title = ""
    for ln in src.splitlines():
        if ln.strip().lower().startswith("title"):
            title = ln.strip()
            break
    match = [n for n, s in sources.items() if s == src]
    print(f"[{fmt}] len={len(src):5d} | {title[:60]:60s} | source={match[0] if match else '*** AUCUNE CORRESPONDANCE ***'}")
