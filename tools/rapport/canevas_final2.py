# -*- coding: utf-8 -*-
"""Passe finale 2 : trou II.1.4, derniers blocs Source/URL, mentions RBAC residuelles."""
import os
import re

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

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


log = []
def note(m):
    log.append(m)
    print("  " + m)


# 1. II.1.5 Etat de l'art -> II.1.4
for el in elems():
    if el.tag == qn("w:p") and style_of(el) == "Heading3" and txt(el).startswith("II.1.5"):
        set_text(el, "II.1.4 État de l’art : systèmes de référence en Afrique de l’Est")
        note("II.1.5 -> II.1.4")

# 2. Blocs « Source : » / URL residuels
URL = re.compile(r"https?://")
for el in elems():
    if el.tag != qn("w:p"):
        continue
    t = txt(el)
    if t.startswith("Source") or (URL.search(t) and len(t) < 400 and not t.startswith("Le ")):
        el.getparent().remove(el)
        note(f"bloc source supprime : {t[:60]}")

# 3. Mentions RBAC dans les critiques et les tableaux
REPL = {
    "— La règle RBAC relative à l’annulation des mouvements est contournée par l’ordre des règles de sécurité, permettant à tout utilisateur authentifié de l’appeler.":
        "— L’ordre des règles de sécurité permet à tout utilisateur authentifié d’annuler un mouvement, alors que cette opération devrait être réservée aux profils habilités.",
    "— Cinq rôles RBAC (ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE) délimitant les permissions de chaque type d’utilisateur avec le principe du moindre privilège.":
        "— Cinq profils d’utilisateurs (ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE) délimitent les permissions de chaque type d’utilisateur selon le principe du moindre privilège.",
}
for p in doc.paragraphs:
    if p.text.strip() in REPL:
        set_text(p._element, REPL[p.text.strip()])
        note("critique reformulee")

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            c = cell.text
            new = c.replace("Sécurité de l’API et RBAC", "Sécurité de l’API et contrôle d’accès")
            new = new.replace("RBAC, JWT stateless, BCrypt, règles d'autorisation par URL",
                              "JWT stateless, BCrypt, autorisation par URL")
            new = new.replace("Rôles RBAC du système", "Profils utilisateurs du système")
            new = new.replace("Cinq rôles RBAC", "Cinq profils")
            new = new.replace("rôles RBAC", "profils utilisateurs")
            new = new.replace("RBAC", "contrôle d’accès")
            if new != c:
                cell.text = new
note("tableaux nettoyes")

doc.save(DOC)

# controle
d2 = Document(DOC)
print("\n=== VERIFICATION ===")
for f in ("architecture en couches", "layered", "machine à états", "RBAC", "https://"):
    hits = [p.text[:100] for p in d2.paragraphs if f in p.text]
    t_hits = [c.text[:60] for t in d2.tables for row in t.rows for c in row.cells if f in c.text]
    print(f"{f:24s} : {len(hits)} paragraphes, {len(t_hits)} cellules")
    for h in hits[:3]:
        print(f"      {h}")
    for h in t_hits[:2]:
        print(f"      [tab] {h}")