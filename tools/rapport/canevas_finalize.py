# -*- coding: utf-8 -*-
"""Derniere passe de mise en coherence du rapport de stage (canevas du professeur).

Corrections appliquees :
  * numerotation des figures et des tableaux alignee sur la structure du rapport
    (Introduction, Chapitre I, Chapitre II, Chapitre III) ;
  * sous-sections technologiques 6.x renumerotees en II.1.5.x ;
  * renvois internes (Figure x, Tableau x) mis a jour ;
  * extraits de code de l'annexe A synchronises avec le code reel du projet
    fomi-stock-api (StockService.sortirFifo et DistributionService) ;
  * figures synchronisees avec les PNG regeneres dans memoire_assets ;
  * quelques coquilles et fragments de phrase corriges.
"""
import os
import re
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
API = os.path.join(HERE, "fomi-stock-api", "src", "main", "java", "bi", "fomi", "stock", "service")

doc = Document(DOC)

# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------
def set_para_text(p, text):
    """Remplace le texte d'un paragraphe en conservant le format du 1er run."""
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)


def replace_para_exact(old, new):
    matches = [p for p in doc.paragraphs if p.text.strip() == old]
    if len(matches) != 1:
        print(f"  [!] paragraphe exact trouve {len(matches)} fois : {old[:60]!r}")
        return False
    set_para_text(matches[0], new)
    return True


def replace_para_prefix(prefix, new):
    matches = [p for p in doc.paragraphs if p.text.strip().startswith(prefix)]
    if len(matches) != 1:
        print(f"  [!] prefixe trouve {len(matches)} fois : {prefix[:60]!r}")
        return False
    set_para_text(matches[0], new)
    return True


def fix_in_all(old, new):
    n = 0
    for p in doc.paragraphs:
        if old in p.text:
            set_para_text(p, p.text.replace(old, new))
            n += 1
    return n


def delete_para(p):
    p._element.getparent().remove(p._element)


def delete_between(start, end):
    el = start._element.getnext()
    while el is not None and el is not end._element:
        nxt = el.getnext()
        el.getparent().remove(el)
        el = nxt


def insert_after(anchor, template_el, text):
    new_el = deepcopy(template_el)
    anchor._element.addnext(new_el)
    p = Paragraph(new_el, anchor._parent)
    set_para_text(p, text)
    for r in p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    return p


# ---------------------------------------------------------------------------
# 1. Numerotation des figures et des tableaux
# ---------------------------------------------------------------------------
FIG = {
    "2.2": "I.1",
    "5.1": "III.1", "5.2": "III.2", "5.9": "III.3", "5.3": "III.4",
    "5.10": "III.5", "5.11": "III.6", "5.12": "III.7", "5.13": "III.8",
    "5.4": "III.9", "5.5": "III.10", "5.6": "III.11", "5.7": "III.12",
    "5.8": "III.13",
}
TAB = {
    "6.1": "II.1",
    "4.1": "III.1", "4.2": "III.2", "4.3": "III.3", "4.4": "III.4",
    "5.1": "III.5", "5.2": "III.6", "5.3": "III.7",
    "7.2": "III.8", "8.1": "III.9",
}

CAPTION = re.compile(r"\b(Figure|Tableau)\s+([0-9]+\.[0-9]+)\b")


def renumber(match):
    kind, code = match.group(1), match.group(2)
    mapping = FIG if kind == "Figure" else TAB
    if code not in mapping:
        return match.group(0)
    return f"{kind} {mapping[code]}"


changed = 0
for p in doc.paragraphs:
    new = CAPTION.sub(renumber, p.text)
    if new != p.text:
        set_para_text(p, new)
        changed += 1
print(f"OK numerotation : {changed} paragraphes mis a jour")

# ---------------------------------------------------------------------------
# 2. Sous-sections technologiques : 6.x -> II.1.5.x
# ---------------------------------------------------------------------------
TECH = {
    "6.1 Java 21 et Spring Boot 3.3.5": "II.1.5.1 Java 21 et Spring Boot 3.3.5",
    "6.2 PostgreSQL 16": "II.1.5.2 PostgreSQL 16",
    "6.3 Flyway — Gestion des migrations": "II.1.5.3 Flyway — Gestion des migrations",
    "6.4 Spring Security et JWT": "II.1.5.4 Spring Security et JWT",
    "6.5 Spring Data JPA et Hibernate": "II.1.5.5 Spring Data JPA et Hibernate",
    "6.6 Testcontainers et JUnit 5": "II.1.5.6 Testcontainers et JUnit 5",
    "6.7 SpringDoc OpenAPI — Documentation": "II.1.5.7 SpringDoc OpenAPI — Documentation",
    "6.8 Lombok": "II.1.5.8 Lombok",
}
for old, new in TECH.items():
    for p in doc.paragraphs:
        if p.text.strip() == old:
            set_para_text(p, new)
            for r in p.runs:
                r.bold = True
            break
print("OK sous-sections II.1.5.x")

# ---------------------------------------------------------------------------
# 3. Renvois internes et formulations
# ---------------------------------------------------------------------------
replace_para_prefix(
    "Ce chapitre présente l'analyse détaillée des besoins",
    "Cette section présente l'analyse détaillée des besoins fonctionnels et non fonctionnels du système, "
    "les règles métier à implémenter et les cas d'utilisation identifiés lors de la phase d'analyse du "
    "projet. Cette analyse constitue la base contractuelle du développement, définissant précisément ce "
    "que le système doit faire et les contraintes auxquelles il doit se conformer. Les besoins ont été "
    "recueillis à travers des entretiens avec les responsables de FOMI et l'écoute des plaintes des "
    "agriculteurs.",
)
replace_para_prefix(
    "Ce chapitre présente la conception technique",
    "Cette section présente la conception technique du système, incluant l'architecture logicielle, le "
    "modèle de données, les diagrammes de séquence, la machine à états du ticket, l'algorithme FIFO et "
    "les mécanismes de sécurité. La conception a été réalisée en suivant les principes de l'ingénierie "
    "et en s'appuyant sur les patterns d'architecture d'entreprise.",
)
replace_para_prefix(
    "Ce chapitre présente les détails de l'implémentation",
    "Cette section présente les détails de l'implémentation du système, incluant la structure du projet, "
    "les algorithmes clés, le système d'alertes, le workflow de validation, le mécanisme d'annulation, "
    "les statistiques et l'audit trail. Chaque composant est décrit en détail avec les choix "
    "d'implémentation et les justifications techniques.",
)
replace_para_prefix(
    "Ce chapitre présente la stratégie de test",
    "Cette section présente la stratégie de test adoptée pour le projet, les différents types de tests "
    "implémentés, l'infrastructure de CI/CD et les résultats obtenus. La qualité des tests est un élément "
    "central du projet, garantissant la fiabilité du système et la confiance dans ses implémentations.",
)
replace_para_prefix(
    "Ce chapitre évalue le système",
    "Cette section évalue le système réalisé par rapport aux objectifs fixés, en termes de conformité au "
    "cahier des charges, de performance, de maintenabilité et de sécurité. L'évaluation est structurée de "
    "manière à couvrir l'ensemble des dimensions de qualité du système et à fournir un bilan objectif des "
    "réalisations et des limites du projet.",
)

# Coquilles
fix_in_all("à toute nos famille", "à toutes nos familles")
fix_in_all("Nous remercions nos famille", "Nous remercions nos familles")
fix_in_all("sa collaboration qui nous a été essentielles", "sa collaboration qui nous a été essentielle")
fix_in_all("ce Système d’approvisionnement engendrent",
           "ce système d’approvisionnement engendre")
fix_in_all("l’ecoute des plaintes des agriculteurs..",
           "l’écoute des plaintes des agriculteurs.")

# Le paragraphe d'historique se termine par un crochet parasite.
for p in doc.paragraphs:
    if p.text.strip().startswith("FOMI — Fertilisants Organo-Minéraux Industries — a été fondée") and p.text.rstrip().endswith("["):
        set_para_text(p, p.text.rstrip().rstrip("[").rstrip())

# Fragment de phrase « de paiement des bénéficiaires. » : on le supprime et on
# complète le paragraphe précédent.
fragment = [p for p in doc.paragraphs if p.text.strip() == "de paiement des bénéficiaires."]
if len(fragment) == 1:
    prev = fragment[0]._element.getprevious()
    # remonte au paragraphe précédent non vide
    while prev is not None and not "".join(t.text or "" for t in prev.iter()).strip():
        prev = prev.getprevious()
    if prev is not None:
        para = Paragraph(prev, fragment[0]._parent)
        set_para_text(para, para.text.rstrip() + " Ces décalages entraînent également des retards de "
                                              "paiement des bénéficiaires.")
    delete_para(fragment[0])
    print("OK fragment « de paiement des bénéficiaires » supprimé")

for p in doc.paragraphs:
    if p.text.startswith(" Ces difficultés financières"):
        set_para_text(p, p.text.lstrip())
        break

# ---------------------------------------------------------------------------
# 4. Annexe A : extraits de code réels du projet
# ---------------------------------------------------------------------------
def read_block(path, start_marker, stop_marker=None):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    start = next(i for i, l in enumerate(lines) if start_marker in l)
    if stop_marker is None:
        end = len(lines)
    else:
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith(stop_marker))
    return lines[start:end]


def stock_service_block():
    path = os.path.join(API, "StockService.java")
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    start = next(i for i, l in enumerate(lines) if "public List<LotSortie> sortirFifo" in l)
    if start > 0 and lines[start - 1].strip() == "@Transactional":
        start -= 1
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "    }")
    return lines[start:end + 1]


def distribution_service_block():
    path = os.path.join(API, "DistributionService.java")
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("public class DistributionService"))
    while lines and lines[-1].strip() == "":
        lines.pop()
    return lines[start:]


p_a1 = next(p for p in doc.paragraphs if p.text.strip().startswith("A.1 StockService.java"))
p_a2 = next(p for p in doc.paragraphs if p.text.strip().startswith("A.2 DistributionService.java"))
p_b = next(p for p in doc.paragraphs if p.text.strip().startswith("Annexe B : Liste des endpoints"))

code_template = deepcopy(p_a1._element.getnext())
delete_between(p_a1, p_b)
set_para_text(p_a1, "A.1 StockService.java — Méthode sortirFifo()")
set_para_text(p_a2, "A.2 DistributionService.java — Classe et méthode distribuer()")

anchor = p_a1
for line in ["// Distribution FIFO par date de réception FOMI (tri croissant)"] + stock_service_block():
    anchor = insert_after(anchor, code_template, line)

# Le titre A.2 a été supprimé avec le bloc : on le recrée juste après le code A.1.
anchor = insert_after(anchor, code_template, "")
anchor.runs[0].text = ""
title_el = deepcopy(p_a2._element)
anchor._element.addnext(title_el)
p_a2 = Paragraph(title_el, anchor._parent)
set_para_text(p_a2, "A.2 DistributionService.java — Classe et méthode distribuer()")

anchor = p_a2
for line in ["// Service de distribution : FIFO, mouvements, distributions et audit"] + distribution_service_block():
    anchor = insert_after(anchor, code_template, line)

print("OK annexe A synchronisée avec fomi-stock-api")

# ---------------------------------------------------------------------------
# 5. Figures : image manquante + synchronisation avec memoire_assets
# ---------------------------------------------------------------------------
ASSETS = os.path.join(HERE, "memoire_assets")
FIGURES = [
    ("Circuit de distribution", "distribution_circuit.png"),
    ("Architecture globale", "architecture.png"),
    ("Architecture en couches", "layered_architecture.png"),
    ("Diagramme de classes", "class_diagram.png"),
    ("Entité-Relation", "er_diagram.png"),
    ("Diagramme de déploiement", "deployment_diagram.png"),
    ("cas d'utilisation", "use_case_diagram.png"),
    ("d'activités", "activity_diagram.png"),
    ("Dictionnaire de données", "data_dictionary_summary.png"),
    ("Création et validation de ticket", "sequence_ticket.png"),
    ("Machine à états", "ticket_state_machine.png"),
    ("Organigramme de l'algorithme FIFO", "fifo_flowchart.png"),
    ("Matrice RBAC", "rbac_matrix.png"),
    ("Distribution FIFO", "sequence_distribution.png"),
]


def next_text(el):
    el = el.getnext()
    while el is not None:
        txt = "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()
        if txt:
            return txt
        el = el.getnext()
    return ""


# 5.1 Restaure l'image du circuit de distribution (perdue a la restructuration).
p_caption = next(p for p in doc.paragraphs if p.text.strip().startswith("Figure I.1"))
prev_el = p_caption._element.getprevious()
if prev_el is not None and not prev_el.findall(".//" + qn("w:drawing")):
    p_img = Paragraph(prev_el, p_caption._parent)
    if not p_img.text.strip():
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(
            os.path.join(ASSETS, "distribution_circuit.png"), width=Inches(5.8))
        print("OK Figure I.1 : image du circuit insérée")

# 5.2 Remplace chaque image par le PNG regenere correspondant.
synced = 0
for p in doc.paragraphs:
    blips = list(p._element.iter(qn("a:blip")))
    if not blips:
        continue
    caption = next_text(p._element)
    if not caption.startswith("Figure"):
        continue
    for needle, filename in FIGURES:
        path = os.path.join(ASSETS, filename)
        if needle.lower() in caption.lower() and os.path.exists(path):
            with open(path, "rb") as fh:
                blob = fh.read()
            for blip in blips:
                r_id = blip.get(qn("r:embed"))
                doc.part.related_parts[r_id]._blob = blob
            synced += 1
            break
print(f"OK figures synchronisées : {synced}")

# ---------------------------------------------------------------------------
# 6. Enregistrement
# ---------------------------------------------------------------------------
doc.save(DOC)
print("DOCUMENT FINAL ENREGISTRÉ :", DOC)
