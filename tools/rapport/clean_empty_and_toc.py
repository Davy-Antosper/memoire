# -*- coding: utf-8 -*-
"""Supprime les paragraphes vides consecutifs (max 1) dans le corps,
puis reconstruit le champ TOC pour effacer les entrees dupliquees."""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)

# --------------------------------------------------------------------------
# 1. reduire les suites de paragraphes vides a un seul
# --------------------------------------------------------------------------
removed = 0
prev_empty = False
for p in list(doc.paragraphs):
    empty = (not p.text.strip() and not p._p.findall(".//" + qn("w:drawing"))
             and not p._p.findall(".//" + qn("w:pict")))
    if empty and prev_empty:
        p._element.getparent().remove(p._element)
        removed += 1
        continue
    prev_empty = empty

# --------------------------------------------------------------------------
# 2. reconstruire le champ TOC (supprime les doublons issus des fusions)
# --------------------------------------------------------------------------
pars = doc.paragraphs
found = any("TOC \\o" in p._p.xml for p in pars)

if not found:
    raise SystemExit("champ TOC introuvable")

# supprimer tous les paragraphes toc existants
for p in list(doc.paragraphs):
    if p.style.name.startswith("toc") or "TOC \\o" in p._p.xml:
        p._element.getparent().remove(p._element)

# reinserer apres le titre TABLE DES MATIÈRES
heading = None
for p in doc.paragraphs:
    if p.text.strip() == "TABLE DES MATIÈRES":
        heading = p
        break

new_p = OxmlElement("w:p")


def run_with(el):
    r = OxmlElement("w:r")
    r.append(el)
    return r


fc1 = OxmlElement("w:fldChar")
fc1.set(qn("w:fldCharType"), "begin")
it = OxmlElement("w:instrText")
it.set(qn("xml:space"), "preserve")
it.text = ' TOC \\o "1-3" \\h \\z \\u '
fc2 = OxmlElement("w:fldChar")
fc2.set(qn("w:fldCharType"), "separate")
t = OxmlElement("w:t")
t.text = "Table des matières — appuyez sur F9 pour mettre à jour."
fc3 = OxmlElement("w:fldChar")
fc3.set(qn("w:fldCharType"), "end")

for el in (fc1, it, fc2, t, fc3):
    new_p.append(run_with(el))

heading._p.addnext(new_p)

# forcer la mise a jour des champs
settings = doc.settings.element
if settings.find(qn("w:updateFields")) is None:
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

doc.save(DOC)
print("paragraphes vides supprimes :", removed, "| TOC reconstruit")