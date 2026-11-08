# -*- coding: utf-8 -*-
"""Deplace les figures du diagramme de cas d'utilisation et du diagramme
d'activites dans la section III.1.3 Cas d'utilisation (elles etaient
placees sous III.1.4 Besoins non fonctionnels, ce qui contredisait
le titre de la section)."""
from docx import Document
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"

doc = Document(DOC)
pars = doc.paragraphs

# reperer les index
i_cas = None          # Heading III.1.3
i_bnf = None          # Heading III.1.4
for i, p in enumerate(pars):
    if p.style.name == "Heading 3" and p.text.strip().startswith("III.1.3"):
        i_cas = i
    if p.style.name == "Heading 3" and p.text.strip().startswith("III.1.4"):
        i_bnf = i

if i_cas is None or i_bnf is None:
    raise SystemExit("sections III.1.3 / III.1.4 introuvables")

# le bloc a deplacer : du 1er paragraphe de figure jusqu'a la fin de III.1.4
# on identifie les 6 paragraphes (intro use case, image, legende, intro activites,
# image, legende) qui se trouvent APRES le tableau des besoins non fonctionnels
bloc = []
for i in range(i_bnf + 1, len(pars)):
    p = pars[i]
    if p.style.name.startswith("Heading"):
        break
    t = p.text.strip()
    if ("diagramme de cas d'utilisation" in t
            or "diagramme d'activités" in t
            or "Figure III.1" in t
            or "Figure III.2" in t
            or "graphic" in p._p.xml):
        bloc.append(p)

if len(bloc) < 5:
    raise SystemExit("bloc de figures introuvable (trouve %d)" % len(bloc))

# retirer du document
for p in bloc:
    p._element.getparent().remove(p._element)

# reinserer juste apres le tableau des cas d'utilisation (avant III.1.4)
anchor = None
for p in doc.paragraphs:
    if p.style.name == "Heading 3" and p.text.strip().startswith("III.1.4"):
        anchor = p._p
        break

# inserer apres les paragraphes vides qui precedent III.1.4 : on prend
# l'element precedent le titre
prev = anchor.getprevious()
for p in bloc:
    prev.addnext(p._element)
    prev = p._element

doc.save(DOC)
print("paragraphes deplaces :", len(bloc))