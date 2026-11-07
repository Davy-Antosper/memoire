# -*- coding: utf-8 -*-
"""Passe 2 : architecture du systeme, fusion des sections du chapitre III,
insertion/remplacement des figures, suppression de l'architecture en couches."""
import os
import re
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
ASSETS = os.path.join(HERE, "memoire_assets")

doc = Document(DOC)
body = doc.element.body


def txt(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def style_of(el):
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        return ""
    ps = pPr.find(qn("w:pStyle"))
    return ps.get(qn("w:val")) if ps is not None else ""


def elems():
    sectPr = body.find(qn("w:sectPr"))
    return [c for c in body.iterchildren() if c is not sectPr]


def index_of(pred, start=0, items=None):
    items = items if items is not None else elems()
    for i in range(start, len(items)):
        if pred(items[i]):
            return i
    return -1


def is_h(el, level=None):
    if el.tag != qn("w:p"):
        return False
    s = style_of(el)
    if level is None:
        return s.startswith("Heading")
    return s.replace(" ", "") == f"Heading{level}"


def remove_range(a, b):
    items = elems()
    n = 0
    for el in items[a:b]:
        el.getparent().remove(el)
        n += 1
    return n


def set_text(el, new_text):
    runs = el.findall(".//" + qn("w:r"))
    if not runs:
        return False
    first = runs[0]
    for r in runs[1:]:
        r.getparent().remove(r)
    for t in first.findall(qn("w:t")):
        first.remove(t)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = new_text
    first.append(t)
    return True


def set_style(el, sid):
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        el.insert(0, pPr)
    ps = pPr.find(qn("w:pStyle"))
    if ps is None:
        ps = OxmlElement("w:pStyle")
        pPr.insert(0, ps)
    ps.set(qn("w:val"), sid)


def new_para(text="", style=None, bold=False, italic=False, size=None, align=None):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        if bold:
            r.bold = True
        if italic:
            r.italic = True
        if size:
            r.font.size = Pt(size)
    if style:
        p.style = doc.styles[style]
    if align is not None:
        p.alignment = align
    el = p._element
    body.remove(el)
    return el


def new_image(path, width_in=5.8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(path, width=Inches(width_in))
    el = p._element
    body.remove(el)
    return el


def insert_after(anchor, el):
    anchor.addnext(el)
    return el


def insert_seq_after(anchor, els):
    cur = anchor
    for e in els:
        cur = insert_after(cur, e)
    return cur


def page_break():
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)
    el = p._element
    body.remove(el)
    return el


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Sous-titres technologiques : II.1.5.x -> II.1.4.x (Heading 4)
# ===========================================================================
items = elems()
n = 0
for el in items:
    if el.tag != qn("w:p"):
        continue
    t = txt(el)
    m = re.match(r"^II\.1\.5\.(\d+)\s+(.+)$", t)
    if m and not is_h(el):
        set_text(el, f"II.1.4.{m.group(1)} {m.group(2)}")
        set_style(el, "Heading4")
        n += 1
note(f"sous-sections technologiques II.1.4.x : {n}")

# ===========================================================================
# 2. Introduction III.2 : retirer machine a etats / FIFO / securite
# ===========================================================================
items = elems()
i = index_of(lambda e: is_h(e, 2) and txt(e).startswith("III.2 Conception"), items=items)
if i != -1 and i + 1 < len(items):
    set_text(items[i + 1],
             "Cette section présente la conception du système : l'architecture d'ensemble, le modèle de "
             "données, les diagrammes de séquence des traitements critiques et la structure du projet. "
             "La conception s'appuie sur les besoins formalisés dans la section précédente et sur les "
             "contraintes techniques du contexte de déploiement.")
    note("introduction III.2 reecrite")

# ===========================================================================
# 3. Remplacement du bloc « architecture en couches » de III.2.1
# ===========================================================================
items = elems()
i_arch = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.2.1"), items=items)
i_model = index_of(lambda e: is_h(e, 3) and txt(e).startswith("III.2.2"), start=i_arch + 1, items=items)

if i_arch != -1 and i_model != -1:
    n = remove_range(i_arch, i_model)
    note(f"III.2.1 architecture en couches : {n} elements supprimes")

    h = new_para("III.2.1 L’architecture du système", style="Heading 3")
    intro = new_para(
        "L’architecture du système décrit l’organisation d’ensemble de la solution : les composants "
        "logiciels, leur rôle respectif et la manière dont ils communiquent. Le système FOMI-Stock "
        "adopte une architecture en trois tiers, dans laquelle les clients web et mobile consomment "
        "une API REST unique qui s’appuie sur une base de données relationnelle. Cette organisation "
        "centralise la logique métier et les données, ce qui garantit que tous les acteurs — "
        "administrateurs, superviseurs, agents de zone, agents de colline et agents logistiques — "
        "travaillent sur un même référentiel d’information.")

    img = new_image(os.path.join(ASSETS, "architecture.png"), 5.4)
    cap = new_para("Figure III.1 — Architecture du système FOMI-Stock", italic=True, size=9,
                   align=WD_ALIGN_PARAGRAPH.CENTER)

    p1 = new_para(
        "Les clients constituent le premier tiers. L’application web, développée avec React et Vite, "
        "est destinée aux utilisateurs du siège et des dépôts provinciaux ; elle est configurée comme "
        "une application web progressive (PWA). L’application mobile, développée avec Expo et React "
        "Native, cible les agents de terrain qui travaillent au niveau des zones et des collines. Les "
        "deux clients échangent avec l’API au format JSON, sur le protocole HTTPS, et ne détiennent "
        "aucune donnée métier : toute la logique est portée par le serveur.")
    p2 = new_para(
        "L’API REST, développée avec Java 21 et Spring Boot 3.3.5, constitue le deuxième tiers. Elle "
        "regroupe dix-sept contrôleurs exposant soixante-deux points d’entrée, répartis en quatre "
        "domaines fonctionnels : les référentiels (géographie, dépôts, types d’engrais, agriculteurs), "
        "les stocks et les lots (réceptions, transferts inter-dépôts, sorties, ajustements), les "
        "tickets et leur distribution (création, validation, distribution, annulation), et enfin les "
        "alertes, les statistiques et la piste d’audit. Chaque requête traverse le filtre "
        "d’authentification, qui vérifie le jeton et charge le profil de l’utilisateur, avant d’être "
        "traitée par le service métier compétent. Le service de notification complète l’ensemble en "
        "adressant les alertes par courrier électronique.")
    p3 = new_para(
        "La base de données PostgreSQL 16 forme le troisième tiers. Elle stocke seize tables "
        "relationnelles dont le schéma est versionné par douze migrations Flyway. Les contraintes "
        "d’intégrité — clés étrangères, énumérations nommées, contrôles de quantité et d’unicité — "
        "sont portées par la base elle-même, de sorte qu’aucune incohérence ne peut être enregistrée "
        "même en cas d’appel direct à l’API.")
    p4 = new_para(
        "Le choix d’une API unique plutôt que de composants spécialisés répond à trois contraintes du "
        "contexte. D’abord, la taille de l’organisation ne justifie pas une infrastructure distribuée : "
        "un serveur unique réduit les coûts d’exploitation et de maintenance. Ensuite, la cohérence des "
        "stocks exige des transactions strictes entre les mouvements, les distributions et les tickets ; "
        "une base relationnelle unique garantit cette cohérence. Enfin, l’ouverture de l’API permet "
        "d’ajouter sans refonte des clients supplémentaires, par exemple un portail public de suivi des "
        "tickets ou une passerelle de paiement mobile.")
    note("III.2.1 Architecture du systeme : figure + texte inseres")

    insert_seq_after(elems()[i_arch - 1], [h, intro, img, cap, p1, p2, p3, p4])
else:
    note("[!] bloc III.2.1 introuvable")

doc.save(DOC)
print(f"\nPasse 2 terminee : {len(log)} operations")