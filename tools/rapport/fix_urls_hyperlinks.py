# -*- coding: utf-8 -*-
"""Supprime les hyperliens (w:hyperlink) et les runs contenant des URLs brutes
dans le corps du rapport, hors sections bibliographie/webographie."""
import re
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
URL_RE = re.compile(r'https?://\S+')


def in_refs_or_webo():
    """Retourne les elements a preserver (refs + webographie + annexes)."""
    doc = Document(DOC)
    keep = set()
    active = False
    for p in doc.paragraphs:
        if p.style.name == "Heading 1" and (
            "RÉFÉRENCES" in p.text.upper() or "WEBOGRAPHIE" in p.text.upper()
            or "ANNEXE" in p.text.upper()
        ):
            active = True
        keep.add(id(p._element))
    return keep


doc = Document(DOC)

# reperer la zone a nettoyer : depuis le debut jusqu'au titre REFERENCES
stop = None
for i, p in enumerate(doc.paragraphs):
    if p.style.name == "Heading 1" and "RÉFÉRENCES" in p.text.upper():
        stop = i
        break
if stop is None:
    stop = len(doc.paragraphs)

removed_links = 0
removed_runs = 0
cleaned_pars = 0

for p in doc.paragraphs[:stop]:
    changed = False

    # 1. supprimer les elements w:hyperlink
    for h in p._element.findall(W + "hyperlink"):
        p._element.remove(h)
        removed_links += 1
        changed = True

    # 2. supprimer les runs contenant encore une URL brute
    for r in list(p._element.findall(W + "r")):
        txt = "".join(t.text or "" for t in r.findall(W + "t"))
        if URL_RE.search(txt):
            p._element.remove(r)
            removed_runs += 1
            changed = True

    # 3. nettoyer les espaces doubles et ponctuation orpheline
    if changed:
        txt = p.text
        txt = re.sub(r'\s{2,}', ' ', txt).strip()
        txt = re.sub(r'\.\s*\.', '.', txt)
        if txt and not txt.endswith((".", ":", "!", "?")):
            txt += "."
        runs = p._element.findall(W + "r")
        if runs:
            t_el = runs[0].find(W + "t")
            if t_el is None:
                t_el = runs[0].makeelement(W + "t", {})
                runs[0].append(t_el)
            t_el.text = txt
            for extra in runs[1:]:
                for t2 in extra.findall(W + "t"):
                    t2.text = ""
        cleaned_pars += 1

doc.save(DOC)
print("hyperliens supprimes :", removed_links)
print("runs URL supprimes :", removed_runs)
print("paragraphes nettoyes :", cleaned_pars)