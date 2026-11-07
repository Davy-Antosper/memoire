# -*- coding: utf-8 -*-
"""1. Corrige la legende de la Figure III.2 (le diagramme d'activites
   represente le cycle de vie d'un ticket, pas un FIFO).
2. Supprime la Figure III.8 (diagramme de sequence FIFO) et son commentaire,
   conformement a la demande de suppression du detail FIFO."""
from docx import Document

DOC = r"Rapport_stage_FOMI_canevas.docx"


def rewrite(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)

# --- 1. legende Figure III.2 ---
fixed_caption = False
for p in doc.paragraphs:
    if p.text.strip().startswith("Figure III.2 — Diagramme d'activités — Distribution FIFO"):
        rewrite(p, "Figure III.2 — Diagramme d'activités : cycle de vie d'un ticket d'engrais")
        fixed_caption = True
        break

# --- 2. supprimer le bloc Figure III.8 (image + legende + paragraphe) ---
pars = doc.paragraphs
start = None
for i, p in enumerate(pars):
    if p.text.strip().startswith("Figure III.8 — Diagramme de séquence : Distribution FIFO"):
        start = i
        break

removed = 0
if start is not None:
    # supprimer la legende, le paragraphe de commentaire et l'image precedente
    to_remove = [pars[start]]
    # paragraphe suivant (commentaire) tant qu'il n'est pas un titre
    j = start + 1
    while j < len(pars) and not pars[j].style.name.startswith("Heading") and pars[j].text.strip():
        to_remove.append(pars[j])
        j += 1
    # image precedente
    k = start - 1
    if k >= 0 and "graphic" in pars[k]._p.xml:
        to_remove.append(pars[k])

    for p in to_remove:
        p._element.getparent().remove(p._element)
        removed += 1

doc.save(DOC)
print("legende III.2 corrigee :", fixed_caption, "| paragraphes supprimes :", removed)