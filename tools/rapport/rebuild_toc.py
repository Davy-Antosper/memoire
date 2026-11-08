# -*- coding: utf-8 -*-
"""Reconstruit le champ TOC (table des matieres) casse par la suppression
des hyperliens, puis marque le document pour mise a jour des champs."""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOC = r"Rapport_stage_FOMI_canevas.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = Document(DOC)

# 1. localiser le paragraphe contenant le champ TOC et tout le bloc toc
pars = doc.paragraphs
first_toc = None
for i, p in enumerate(pars):
    if "TOC \\o" in p.text:
        first_toc = i
        break

if first_toc is None:
    raise SystemExit("champ TOC introuvable")

# 2. supprimer tous les anciens paragraphes toc
for p in list(pars[first_toc:]):
    if p.style.name.startswith("toc") or "TOC \\o" in p.text:
        p._element.getparent().remove(p._element)
    elif p.style.name == "Heading 1":
        break

# 3. recreer un paragraphe unique portant le champ TOC
heading = doc.paragraphs[first_toc - 1]  # TABLE DES MATIÈRES
new_p = OxmlElement("w:p")

r1 = OxmlElement("w:r")
fc1 = OxmlElement("w:fldChar")
fc1.set(qn("w:fldCharType"), "begin")
r1.append(fc1)

r2 = OxmlElement("w:r")
it = OxmlElement("w:instrText")
it.set(qn("xml:space"), "preserve")
it.text = ' TOC \\o "1-3" \\h \\z \\u '
r2.append(it)

r3 = OxmlElement("w:r")
fc2 = OxmlElement("w:fldChar")
fc2.set(qn("w:fldCharType"), "separate")
r3.append(fc2)

r4 = OxmlElement("w:r")
t = OxmlElement("w:t")
t.text = "Mettez à jour le champ (F9) pour afficher la table des matières."
r4.append(t)

r5 = OxmlElement("w:r")
fc3 = OxmlElement("w:fldChar")
fc3.set(qn("w:fldCharType"), "end")
r5.append(fc3)

for r in (r1, r2, r3, r4, r5):
    new_p.append(r)

heading._p.addnext(new_p)

# 4. forcer la mise a jour des champs a l'ouverture
settings = doc.settings.element
if settings.find(qn("w:updateFields")) is None:
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

doc.save(DOC)
print("champ TOC reconstruit")