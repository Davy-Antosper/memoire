# -*- coding: utf-8 -*-
"""Mise à jour du rapport de stage pour le modèle métier strict FOMI.

Modèle retenu : Province -> Commune -> Zone -> Colline, avec deux niveaux de
dépôts uniquement (PROVINCE et ZONE). La colline reste le lieu de résidence
des agriculteurs, pas un niveau de stockage.

Cette passe est idempotente : elle peut être rejouée sans effet de bord.
"""
import os
import sys
from copy import deepcopy

from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(DOC)
modifs = 0
manquants = []


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------
def trace(label, n=1):
    global modifs
    if n:
        modifs += n
        print(f"  ok  {label}" + (f" ({n})" if n != 1 else ""))
    else:
        manquants.append(label)


def set_text(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)


def replace_para(old, new, label):
    """Remplace tout le texte d'un paragraphe identifié par son début."""
    hits = [p for p in doc.paragraphs if p.text.strip() == old]
    if not hits:
        hits = [p for p in doc.paragraphs if p.text.strip().startswith(old)]
    for p in hits:
        set_text(p, new)
    trace(label, len(hits))


def replace_in(old, new, label):
    """Remplace une sous-chaîne dans tous les paragraphes."""
    n = 0
    for p in doc.paragraphs:
        if old in p.text:
            set_text(p, p.text.replace(old, new))
            n += 1
    trace(label, n)


def replace_first_line(starts, new_line, label):
    n = 0
    for p in doc.paragraphs:
        if p.text.strip().startswith(starts):
            lines = p.text.split("\n")
            lines[0] = new_line
            set_text(p, "\n".join(lines))
            n += 1
    trace(label, n)


def set_cell(cell, text):
    p = cell.paragraphs[0]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)
    for extra in cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)


def find_table(*header_cells):
    for table in doc.tables:
        header = [c.text.strip() for c in table.rows[0].cells]
        if header[:len(header_cells)] == list(header_cells):
            return table
    return None


def insert_row_after(table, index, values):
    tr = deepcopy(table.rows[index]._tr)
    table.rows[index]._tr.addnext(tr)
    row = table.rows[index + 1]
    for cell, value in zip(row.cells, values):
        set_cell(cell, value)


def insert_paragraph_like(anchor, text):
    p = anchor.insert_paragraph_before()
    p.style = anchor.style
    run = p.add_run(text)
    if anchor.runs:
        src = anchor.runs[0]
        run.font.name = src.font.name
        run.font.size = src.font.size
    return p


# ---------------------------------------------------------------------------
# 1. Circuit de distribution : deux niveaux de dépôts
# ---------------------------------------------------------------------------
replace_para(
    "La distribution des engrais FOMI suit un circuit logistique et administratif hiérarchisé",
    "La distribution des engrais FOMI suit un circuit logistique et administratif hiérarchisé, "
    "depuis l’usine de Maramvya jusqu’aux agriculteurs bénéficiaires (Figure I.1). Ce circuit, "
    "restructuré en conformité avec l’organisation territoriale du pays (province, commune, zone, "
    "colline), s’appuie sur deux niveaux de dépôts fixes et permanents — le dépôt provincial et le "
    "dépôt de zone — complétés par une distribution finale organisée au niveau de chaque colline.",
    "circuit : deux niveaux de dépôts",
)

replace_first_line(
    "Niveau 1 : L'usine FOMI de Maramvya",
    "Site de production : l'usine FOMI de Maramvya (stockage central)",
    "usine = site de production",
)
replace_first_line(
    "Niveau 2 : Les dépôts provinciaux",
    "Niveau 1 : Le dépôt provincial — BPEAE (stockage régional)",
    "dépôt provincial = niveau 1",
)
replace_in(
    "assurent la répartition des stocks entre les différentes communes et zones de leur ressort",
    "assurent la répartition des stocks vers les communes, puis les zones de leur ressort",
    "répartition province -> communes -> zones",
)
replace_first_line(
    "Niveau 3 : Les dépôts de zone",
    "Niveau 2 : Le dépôt de zone (terminus logistique officiel de la FOMI)",
    "dépôt de zone = niveau 2",
)
replace_first_line(
    "Distribution finale : les points de distribution de colline",
    "Distribution finale : les collines (sans dépôt permanent)",
    "collines sans dépôt",
)
replace_in(
    "au point de distribution collinaire",
    "au point de service organisé dans sa colline",
    "retrait organisé dans la colline",
)

# ---------------------------------------------------------------------------
# 2. Compteurs : entités, tables, migrations, endpoints, tests
# ---------------------------------------------------------------------------
replace_in("soixante-deux points d’entrée", "soixante-cinq points d’entrée", "P312 : 65 endpoints")
replace_in("seize tables relationnelles", "dix-sept tables relationnelles", "P313 : 17 tables")
replace_in("douze migrations Flyway", "treize migrations Flyway", "P313 : 13 migrations")
replace_in("seize tables principales", "dix-sept tables principales", "P318 : 17 tables")
replace_in("les seize entités du système", "les dix-sept entités du système", "P327 : 17 entités")
replace_in("(province, zone, colline)", "(province, commune, zone, colline)", "P327 : hiérarchie")
replace_in("provinces, zones, collines, dépôts", "provinces, communes, zones, collines, dépôts",
           "P391 : référentiels")
replace_in("12 versions de migration", "13 versions de migration", "P246 : 13 versions")

replace_in("soixante-deux endpoints", "soixante-cinq endpoints", "P402 : 65 endpoints")
replace_in("de seize tables", "de dix-sept tables", "P402 : 17 tables")
replace_in("de douze migrations", "de treize migrations", "P402 : 13 migrations")
replace_in("deux cent sept tests", "deux cent dix-huit tests", "P402 : 218 tests")
replace_in("deux cent quatre tests d’intégration", "deux cent quinze tests d’intégration",
           "P402 : 215 tests d'intégration")

# ---------------------------------------------------------------------------
# 3. Tableaux : besoins, cas d'utilisation, modèle de données, enums, packages
# ---------------------------------------------------------------------------
t_besoins = find_table("ID", "Catégorie", "Description")
if t_besoins is not None:
    for row in t_besoins.rows:
        label = row.cells[0].text.strip()
        if label == "F3":
            set_cell(row.cells[2],
                     "Gestion des provinces/communes/zones/collines (hiérarchie administrative)")
            modifs += 1
        elif label == "F8" and "colline" in row.cells[2].text:
            set_cell(row.cells[2], "Transferts inter-dépôts (province, zone) avec vérification "
                                   "de disponibilité à la source")
            modifs += 1
    print("  ok  tableau des besoins")

t_uc = find_table("ID", "Cas d'utilisation", "Acteur", "Précondition", "Résultat")
if t_uc is not None:
    for row in t_uc.rows:
        label = row.cells[0].text.strip()
        if label == "UC-03" and "commune" not in row.cells[4].text:
            set_cell(row.cells[4], "CRUD provinces/communes/zones/collines")
            modifs += 1
        elif label == "UC-04" and "colline" in row.cells[4].text:
            set_cell(row.cells[4], "CRUD des dépôts (province, zone)")
            modifs += 1
    print("  ok  tableau des cas d'utilisation")

t_tables = find_table("Table", "Description", "Colonnes clés")
if t_tables is not None:
    labels = [r.cells[0].text.strip() for r in t_tables.rows]
    if "commune" not in labels:
        idx = labels.index("province") if "province" in labels else 1
        insert_row_after(t_tables, idx, [
            "commune",
            "Communes rattachées aux provinces",
            "id, code, nom, province_id, created_at",
        ])
        modifs += 1
    for row in t_tables.rows:
        label = row.cells[0].text.strip()
        if label == "zone" and "commune_id" not in row.cells[2].text:
            set_cell(row.cells[1], "Zones administratives rattachées aux communes")
            set_cell(row.cells[2], "id, code, nom, commune_id, created_at")
            modifs += 1
        elif label == "depot" and "colline_id" in row.cells[2].text:
            set_cell(row.cells[1], "Dépôts de stockage (province, zone)")
            set_cell(row.cells[2], "id, code, nom, niveau, province_id, zone_id, seuil_alerte_min, "
                                   "capacite_max, actif, created_at")
            modifs += 1
    print("  ok  tableau des tables")

t_enums = find_table("Enum", "Valeurs", "Usage")
if t_enums is not None:
    for row in t_enums.rows:
        if row.cells[0].text.strip() == "NiveauDepot" and "COLLINE" in row.cells[1].text:
            set_cell(row.cells[1], "PROVINCE, ZONE")
            modifs += 1
    print("  ok  tableau des enums")

t_packages = find_table("Package", "Contenu", "Nombre de classes")
if t_packages is not None:
    for row in t_packages.rows:
        if row.cells[0].text.strip() == "repository" and "16" in row.cells[2].text:
            set_cell(row.cells[2], "17 interfaces")
            modifs += 1
        elif row.cells[0].text.strip() == "model/entity" and "16" in row.cells[2].text:
            set_cell(row.cells[2], "17 classes")
            modifs += 1
    print("  ok  tableau des packages")

# ---------------------------------------------------------------------------
# 4. Annexe B : endpoints manquants (communes, notifier, expirer)
# ---------------------------------------------------------------------------
t_endpoints = find_table("Méthode", "Endpoint", "Description", "Rôle")
if t_endpoints is not None:
    existants = [r.cells[1].text.strip() for r in t_endpoints.rows]

    def add_after(path_anchor, values):
        if values[1] in existants:
            return
        anchor = next(i for i, r in enumerate(t_endpoints.rows)
                      if r.cells[1].text.strip() == path_anchor)
        insert_row_after(t_endpoints, anchor, values)
        existants.insert(anchor + 1, values[1])

    add_after("/api/agriculteurs/{id}",
              ("POST", "/api/agriculteurs/{id}/notifier",
               "Notifier un agriculteur par email", "ADMIN, AGENT_ZONE, AGENT_COLLINE"))
    add_after("/api/provinces",
              ("GET", "/api/communes", "Liste des communes", "AUTH"))
    add_after("/api/provinces",
              ("GET", "/api/provinces/{id}/communes", "Communes d'une province", "AUTH"))
    add_after("/api/zones",
              ("GET", "/api/communes/{id}/zones", "Zones d'une commune", "AUTH"))
    add_after("/api/tickets/{id}/rejeter",
              ("POST", "/api/tickets/expirer",
               "Clôturer une saison et expirer les tickets non servis",
               "ADMIN, SUPERVISEUR"))
    print("  ok  annexe B : endpoints")

# ---------------------------------------------------------------------------
# 5. Annexe C : extrait de schéma aligné sur V13
# ---------------------------------------------------------------------------
replace_para("Extrait consolidé des migrations V1, V7 et V11 :",
             "Extrait consolidé des migrations V1, V7, V11, V12 et V13 :",
             "annexe C : versions")
replace_para("CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE', 'COLLINE');",
             "CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE');",
             "annexe C : enum niveau_depot")
replace_para("colline_id       BIGINT REFERENCES colline(id),",
             "-- V13 : colline_id supprimé (aucun dépôt de colline)",
             "annexe C : suppression colline_id")

anchor = next((p for p in doc.paragraphs if p.text.strip() == "CREATE TABLE depot ("), None)
if anchor is not None and not any(p.text.strip() == "CREATE TABLE commune (" for p in doc.paragraphs):
    for line in [
        "CREATE TABLE commune (",
        "    id          BIGSERIAL PRIMARY KEY,",
        "    code        VARCHAR(30)  NOT NULL UNIQUE,",
        "    nom         VARCHAR(100) NOT NULL,",
        "    province_id BIGINT       NOT NULL REFERENCES province(id),",
        "    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()",
        ");",
        "",
        "ALTER TABLE zone ADD COLUMN commune_id BIGINT REFERENCES commune(id);",
        "-- V13 : zone.commune_id devient NOT NULL ; zone.province_id est supprimé",
        "",
    ]:
        insert_paragraph_like(anchor, line)
        modifs += 1

# ---------------------------------------------------------------------------
# Sauvegarde
# ---------------------------------------------------------------------------
doc.save(DOC)

print()
print(f"Rapport mis à jour : {DOC}")
print(f"Modifications appliquées : {modifs}")
if manquants:
    print("Passages non trouvés (déjà corrigés ou reformulés) :")
    for m in manquants:
        print("  -", m)
