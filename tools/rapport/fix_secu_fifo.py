# -*- coding: utf-8 -*-
"""Remplace l'annexe A (extraits de code FIFO detailles) par des extraits
non-FIFO : validation de ticket, systeme d'alertes, securite JWT.
Supprime aussi la section III.3.8.4 Securite (RBAC) et reformule les
mentions FIFO du corps du texte."""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import copy

DOC = r"Rapport_stage_FOMI_canevas.docx"


def set_text(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)

# ---------------------------------------------------------------------------
# 1. Supprimer III.3.8.4 Securite (section RBAC detaillee)
# ---------------------------------------------------------------------------
pars = doc.paragraphs
start = None
for i, p in enumerate(pars):
    if p.style.name.startswith("Heading") and "Sécurité" in p.text and "III.3.8.4" in p.text:
        start = i
        break

removed_sec = 0
if start is not None:
    to_remove = [pars[start]]
    j = start + 1
    while j < len(pars):
        p = pars[j]
        if p.style.name.startswith("Heading"):
            break
        # le dernier paragraphe parle des clients web/mobile : on le garde
        if p.text.strip().startswith("Deux clients ont été développés"):
            break
        to_remove.append(p)
        j += 1
    for p in to_remove:
        p._element.getparent().remove(p._element)
        removed_sec += 1

# ---------------------------------------------------------------------------
# 2. Reformuler la phrase de securite dans l'evaluation (si elle reste)
# ---------------------------------------------------------------------------
SEC_OLD = ("Le système intègre un ensemble complet de mécanismes de sécurité conformes "
           "aux meilleures pratiques de l'industrie :")
SEC_NEW = ("Le système met en œuvre plusieurs mécanismes de protection : une authentification "
           "par jeton JWT, un hachage BCrypt des mots de passe, une validation systématique "
           "des entrées et des contrôles explicites de périmètre géographique dans les services.")
sec_fixed = 0
for p in doc.paragraphs:
    if SEC_OLD in p.text:
        set_text(p, p.text.replace(SEC_OLD, SEC_NEW))
        sec_fixed += 1

# ---------------------------------------------------------------------------
# 3. Reformuler les mentions FIFO du corps (hors references techniques)
# ---------------------------------------------------------------------------
REPL = [
    ("II.1.1 Gestion des stocks et méthode FIFO",
     "II.1.1 Gestion des stocks et traçabilité des lots"),
    ("La méthode FIFO (First-In, First-Out) consiste à consommer en priorité les lots "
     "les plus anciens. Dans le cas des engrais, dont la durée de conservation est limitée, "
     "ce principe doit être combiné à un contrôle de la date de péremption afin de distribuer "
     "d’abord les lots les plus proches de leur date limite. Le système retenu applique ce "
     "principe lors des sorties de stock et enregistre chaque décrément sous forme de "
     "mouvement traçable.",
     "Chaque quantité reçue est associée à un lot identifié par un numéro, une date de "
     "réception et une date de péremption. Lors d’une sortie, le système sélectionne les "
     "lots disponibles en écartant ceux qui sont périmés, puis enregistre le décrément "
     "correspondant sous forme de mouvement traçable. Cette organisation permet de "
     "reconstituer à tout moment l’origine d’une quantité distribuée et de prévenir la "
     "distribution de produits altérés."),
    ("— H3 : Un algorithme FIFO associé à une gestion rigoureuse des lots améliore la "
     "rotation des stocks et limite les pertes par péremption.",
     "— H3 : Une gestion rigoureuse des lots, associée au contrôle des dates de péremption, "
     "améliore la rotation des stocks et limite les pertes."),
    ("la distribution FIFO", "la distribution des engrais"),
    ("— L’algorithme FIFO est ordonné par date de réception FOMI et non par date de "
     "péremption ; de plus, le chemin avec lot imposé ne vérifie pas la péremption.",
     "— L’ordre de sortie des lots suit la date de réception FOMI et non la date de "
     "péremption ; de plus, le chemin avec lot imposé ne contrôle pas la péremption."),
    ("— Corriger l’ordonnancement FIFO pour retenir la date de péremption et contrôler "
     "systématiquement la péremption, y compris pour les lots imposés.",
     "— Faire reposer l’ordonnancement des sorties sur la date de péremption et contrôler "
     "systématiquement celle-ci, y compris pour les lots imposés."),
]
body_fixed = 0
for p in doc.paragraphs:
    for old, new in REPL:
        if old in p.text:
            set_text(p, p.text.replace(old, new))
            body_fixed += 1
            break

doc.save(DOC)
print("paragraphes securite supprimes :", removed_sec)
print("phrase securite reformulee :", sec_fixed)
print("mentions FIFO reformulees :", body_fixed)