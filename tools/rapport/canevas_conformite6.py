# -*- coding: utf-8 -*-
"""Passe 6 : suppression des dernieres mentions interdites, sections finales,
references bibliographiques / webographie, harmonisation typographique."""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

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
    s = style_of(el).replace(" ", "")
    if level is None:
        return s.startswith("Heading")
    return s == f"Heading{level}"


def remove_el(el):
    el.getparent().remove(el)


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


def insert_after(anchor, el):
    anchor.addnext(el)
    return el


log = []
def note(m):
    log.append(m)
    print("  " + m)


# ===========================================================================
# 1. Corrections ciblees des mentions interdites
# ===========================================================================
CORRECTIONS = {
    "— Modélisation UML : cas d’utilisation, classes, séquences, activités, machine à états et déploiement ;":
        "— Modélisation UML : cas d’utilisation, classes, séquences, activités et déploiement ;",

    "Le système retenu repose sur une architecture en couches, une base de données PostgreSQL, des migrations versionnées avec Flyway, une authentification JWT et un contrôle d’accès basé sur les rôles (RBAC). Il intègre également une documentation Swagger et une suite de tests d’intégration.":
        "Le système retenu repose sur une API REST organisée en domaines fonctionnels, une base de données PostgreSQL, des migrations versionnées avec Flyway et une authentification par jetons. Il intègre également une documentation OpenAPI et une suite de tests d’intégration exécutés sur une base PostgreSQL réelle.",

    "La maintenabilité du système est un critère essentiel pour un projet destiné à être maintenu et évolué par des équipes internes à FOMI. Plusieurs facteurs contribuent à la maintenabilité : l'architecture en couches claire permet de localiser rapidement les modifications nécessaires sans impact sur les autres couches ; la documentation Swagger offre une vue complète et interactive de l'API, permettant aux nouveaux développeurs de comprendre le système en quelques minutes ; les 218 tests automatisés garantissent que les modifications n'introduisent pas de régressions (principe de sécurité de refactoring) ; la gestion des migrations Flyway assure la traçabilité des évolutions du schéma de la base de données ; et les conventions de nommage cohérentes (controllers, services, repositories) facilitent la navigation dans le code source.":
        "La maintenabilité du système est un critère essentiel pour un projet destiné à être maintenu et évolué par des équipes internes à FOMI. Plusieurs facteurs y contribuent : la séparation nette des responsabilités entre les contrôleurs, les services et les repositories permet de localiser rapidement les modifications nécessaires ; la documentation OpenAPI offre une vue complète et interactive de l’API, ce qui réduit le temps d’appropriation par un nouveau développeur ; les 218 tests automatisés garantissent que les modifications n’introduisent pas de régressions ; la gestion des migrations Flyway assure la traçabilité des évolutions du schéma ; enfin, les conventions de nommage cohérentes facilitent la navigation dans le code source.",
}

items = elems()
for p in doc.paragraphs:
    t = p.text.strip()
    if t in CORRECTIONS:
        set_text(p._element, CORRECTIONS[t])
        note(f"correction : {t[:60]}...")

# Cas generiques restants : remplacement de « RBAC » par une formulation neutre
def neutralise(p):
    t = p.text
    new = t
    new = new.replace("les tests de sécurité RBAC", "les tests de contrôle d’accès")
    new = new.replace("la sécurité RBAC", "le contrôle d’accès")
    new = new.replace("sécurité RBAC", "contrôle d’accès")
    new = new.replace("tests de sécurité RBAC", "tests de contrôle d’accès")
    if new != t:
        set_text(p._element, new)
        return True
    return False

n = 0
for p in doc.paragraphs:
    if "RBAC" in p.text:
        if neutralise(p):
            n += 1
note(f"mentions RBAC neutralisees : {n}")

# ===========================================================================
# 2. Tableau des tests : mettre a jour les libelles et totaux
# ===========================================================================
for t in doc.tables:
    header = " ".join(c.text for c in t.rows[0].cells)
    if "Tests" in header or any("SecuriteRbac" in c.text for row in t.rows for c in row.cells):
        for row in t.rows:
            for cell in row.cells:
                tc = cell.text
                new = tc
                new = new.replace("SecuriteRbacIntegrationTest", "SecuriteAccesIntegrationTest")
                new = new.replace("RBAC : rôles, périmètre, accès refusé, token invalide",
                                  "Contrôle d’accès : rôles, périmètre, accès refusé, jeton invalide")
                new = new.replace("204 tests", "215 tests")
                new = new.replace("20 classes", "22 classes")
                if new != tc:
                    cell.text = new

# ===========================================================================
# 3. Sections finales : References bibliographiques + Webographie
# ===========================================================================
items = elems()
i_biblio = index_of(lambda e: is_h(e, 1) and re.match(r"^(Bibliographie|Références)", txt(e)), items=items)
i_annexes = index_of(lambda e: is_h(e, 1) and txt(e).startswith("Annexes"), start=0, items=items)

print(f"\nbiblio={i_biblio} annexes={i_annexes}")
if i_biblio != -1 and i_annexes != -1:
    # recuperer les entrees existantes
    entries = []
    for el in items[i_biblio + 1:i_annexes]:
        if el.tag == qn("w:p"):
            t = txt(el)
            if t:
                entries.append(t)
    print(f"entrees bibliographie existantes : {len(entries)}")

    # supprimer l'ancienne section
    n = remove_range(i_biblio, i_annexes)
    note(f"ancienne bibliographie : {n} elements supprimes")

    # classer : ouvrages/articles (papier) vs ressources en ligne
    WEB_HINTS = ("http", "www.", ".org", ".com", ".bi", "Documentation", "Maven", "GitHub",
                 "Docker", "Railway", "VMware", "OpenAPI", "Lombok", "Flyway", "Testcontainers")
    refs, webs = [], []
    for e in entries:
        clean = re.sub(r"^\[\d+\]\s*", "", e).strip()
        if any(h in e for h in WEB_HINTS):
            webs.append(clean)
        else:
            refs.append(clean)

    print(f"  -> {len(refs)} references, {len(webs)} ressources web")

    # nouvelles sections
    h_ref = new_para("RÉFÉRENCES BIBLIOGRAPHIQUES", style="Heading 1")
    ref_paras = []
    for i, r in enumerate(refs, 1):
        ref_paras.append(new_para(f"[{i}] {r}"))

    h_web = new_para("WEBOGRAPHIE", style="Heading 1")
    web_paras = []
    for i, w in enumerate(webs, len(refs) + 1):
        web_paras.append(new_para(f"[{i}] {w}"))

    # inserer avant les annexes
    items = elems()
    i_annexes = index_of(lambda e: is_h(e, 1) and txt(e).startswith("Annexes"), items=items)
    anchor = items[i_annexes - 1]
    seq = [h_ref] + ref_paras + [h_web] + web_paras
    cur = anchor
    for e in seq:
        cur = insert_after(cur, e)
    note(f"sections finales creees : {len(ref_paras)} references, {len(web_paras)} ressources web")

doc.save(DOC)
print(f"\nPasse 6 terminee : {len(log)} operations")