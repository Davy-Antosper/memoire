# -*- coding: utf-8 -*-
"""Mise à jour du rapport de stage pour le modèle métier strict FOMI.

Modèle retenu : Province -> Commune -> Zone -> Colline, avec deux niveaux de
stockage uniquement (PROVINCE et ZONE). La colline reste le lieu de résidence
des agriculteurs, pas un niveau de dépôt.

Cette passe est idempotente : elle peut être rejouée après build_rapport.py.
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
def set_para_text(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)


def replace_exact(old, new):
    global modifs
    matches = [p for p in doc.paragraphs if p.text.strip() == old]
    if not matches:
        manquants.append(old[:70])
        return False
    for p in matches:
        set_para_text(p, new)
        modifs += 1
    return True


def replace_in_paragraphs(old, new, expected=None):
    """Remplace une sous-chaîne dans tous les paragraphes qui la contiennent."""
    global modifs
    n = 0
    for p in doc.paragraphs:
        if old in p.text:
            set_para_text(p, p.text.replace(old, new))
            n += 1
    if n == 0:
        manquants.append(old[:70])
    modifs += n
    return n


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


def insert_row_after(table, index, values):
    """Insère une ligne après `index` en clonant son format."""
    tr = deepcopy(table.rows[index]._tr)
    table.rows[index]._tr.addnext(tr)
    row = table.rows[index + 1]
    for cell, value in zip(row.cells, values):
        set_cell(cell, value)


def find_table(header_first_cells):
    for table in doc.tables:
        header = [c.text.strip() for c in table.rows[0].cells]
        if header[:len(header_first_cells)] == header_first_cells:
            return table
    return None


def set_cell_if(table, row, col, expected_prefix, new):
    cell = table.rows[row].cells[col]
    if cell.text.strip().startswith(expected_prefix):
        set_cell(cell, new)
        return True
    return False


# ---------------------------------------------------------------------------
# 1. Texte : circuit de distribution et niveaux de stockage
# ---------------------------------------------------------------------------
replace_exact(
    "Le mécanisme de distribution repose sur un circuit hiérarchisé acheminant les produits "
    "depuis l'usine FOMI de Maramvya jusqu'aux agriculteurs bénéficiaires. Les engrais, d'abord "
    "stockés à l'usine, sont acheminés vers les dépôts provinciaux, puis vers les dépôts de zone "
    "et de colline, où les agriculteurs viennent retirer leurs engrais sur présentation de leurs "
    "tickets. Ce circuit implique de multiples acteurs et institutions, chacun jouant un rôle "
    "spécifique dans la chaîne de distribution.",
    "Le mécanisme de distribution repose sur un circuit hiérarchisé acheminant les produits depuis "
    "l'usine FOMI de Maramvya jusqu'aux agriculteurs bénéficiaires. Les engrais, d'abord stockés à "
    "l'usine, sont acheminés vers les dépôts provinciaux, puis vers les dépôts de zone, dernier "
    "niveau de stockage permanent maîtrisé par la FOMI. Les agriculteurs viennent ensuite retirer "
    "leurs engrais dans ces dépôts de zone sur présentation de leurs tickets. Ce circuit implique de "
    "multiples acteurs et institutions, chacun jouant un rôle spécifique dans la chaîne de "
    "distribution.",
)

replace_in_paragraphs("lors du retrait effectif des engrais au dépôt de colline",
                      "lors du retrait effectif des engrais au dépôt de zone")
replace_in_paragraphs("une architecture logistique articulée autour de quatre niveaux de stockage fixes",
                      "une architecture logistique articulée autour de deux niveaux de stockage fixes (province et zone)")
replace_in_paragraphs("au point de distribution collinaire",
                      "au point de service organisé dans sa colline")
replace_in_paragraphs("(provinces, zones et collines)",
                      "(provinces, communes, zones et collines)")
replace_in_paragraphs("jusqu’aux points de distribution collinaires",
                      "jusqu’aux dépôts de zone et aux collines desservies")

replace_exact(
    "La distribution des engrais FOMI suit un circuit logistique et administratif hiérarchisé, "
    "depuis l'usine de Maramvya jusqu'aux agriculteurs bénéficiaires. Ce circuit, restructuré en "
    "conformité avec l'organisation territoriale du pays, implique une chaîne d'approvisionnement "
    "en quatre niveaux de stockage fixes, complétée par un système de distribution finale au niveau "
    "de chaque colline.",
    "La distribution des engrais FOMI suit un circuit logistique et administratif hiérarchisé, "
    "depuis l'usine de Maramvya jusqu'aux agriculteurs bénéficiaires. Ce circuit, restructuré en "
    "conformité avec l'organisation territoriale du pays (province, commune, zone, colline), "
    "s'appuie sur deux niveaux de stockage fixes — le dépôt provincial et le dépôt de zone — "
    "complétés par la distribution finale aux agriculteurs dans les collines.",
)

replace_exact(
    "Niveau 4 : Les points de distribution de colline (Livraison éphémère)\n"
    "À ce stade, la logistique lourde s'arrête. Sous la coordination de l'administration locale et "
    "des comités collinaires, les engrais sont transférés depuis le dépôt de zone vers les collines "
    "de destination. Faute d'infrastructures de stockage permanentes, des sites communautaires "
    "éphémères (hangars, églises, écoles) sont réquisitionnés uniquement le jour de la distribution "
    "pour décharger temporairement les volumes (20 à 100 tonnes) et servir immédiatement les "
    "producteurs.",
    "Distribution finale : les collines (sans stockage permanent)\n"
    "À ce stade, la logistique lourde s'arrête : la FOMI ne gère plus de dépôt de colline. Sous la "
    "coordination de l'administration locale et des comités collinaires, les engrais sont acheminés "
    "depuis le dépôt de zone vers les collines de destination. Faute d'infrastructures de stockage "
    "permanentes, des sites communautaires éphémères (hangars, églises, écoles) sont réquisitionnés "
    "uniquement le jour de la distribution pour décharger temporairement les volumes et servir "
    "immédiatement les producteurs. Le système FOMI-Stock modélise la colline comme le lieu de "
    "résidence des agriculteurs, et non comme un niveau de stockage.",
)

replace_exact(
    "L'exploitant se présente au point de distribution collinaire muni de sa pièce d'identité et de "
    "son bon de commande numérique ou papier (ticket de distribution). Ce ticket nominatif, délivré "
    "après paiement, spécifie la nature de l'engrais organo-minéral, le quota exact autorisé calculé "
    "selon ses superficies, ainsi que la saison agricole concernée.",
    "L'exploitant se présente au point de service organisé dans sa colline, muni de sa pièce "
    "d'identité et de son bon de commande numérique ou papier (ticket de distribution). Ce ticket "
    "nominatif, délivré après paiement, spécifie la nature de l'engrais organo-minéral, le quota "
    "exact autorisé calculé selon ses superficies, ainsi que la saison agricole concernée.",
)

# ---------------------------------------------------------------------------
# 2. Compteurs : tables, entités, repositories, migrations, endpoints
# ---------------------------------------------------------------------------
replace_in_paragraphs("16 repositories", "17 repositories")
replace_in_paragraphs("16 entités métier", "17 entités métier")
replace_in_paragraphs("comprend 16 tables principales", "comprend 17 tables principales")
replace_in_paragraphs("géré par Flyway avec 12 versions de migration numérotées",
                      "géré par Flyway avec 13 versions de migration numérotées")
replace_in_paragraphs(
    "référentiels (types d'engrais, provinces, zones, collines, dépôts, lots, stocks)",
    "référentiels (types d'engrais, provinces, communes, zones, collines, dépôts, lots, stocks)",
)

replace_exact(
    "Les résultats obtenus sont les suivants : une API REST documentée exposant soixante-deux "
    "endpoints, couvrant les référentiels, les réceptions, les transferts, la distribution FIFO, les "
    "tickets et leur workflow, les alertes, les statistiques, les exports CSV, la piste d'audit et "
    "les notifications email des agriculteurs ; un modèle de données relationnel de seize tables "
    "géré par douze migrations Flyway ; un mécanisme de sécurité JWT avec cinq rôles et un hachage "
    "BCrypt ; un système d'alertes automatiques ; et une suite de deux cent dix-huit tests "
    "automatisés, dont deux cent quinze tests d'intégration sur PostgreSQL réel et trois tests "
    "unitaires.",
    "Les résultats obtenus sont les suivants : une API REST documentée exposant soixante-cinq "
    "endpoints, couvrant les référentiels géographiques (provinces, communes, zones, collines), les "
    "réceptions, les transferts, la distribution FIFO, les tickets et leur workflow, les alertes, "
    "les statistiques, les exports CSV, la piste d'audit et les notifications email des "
    "agriculteurs ; un modèle de données relationnel de dix-sept tables géré par treize migrations "
    "Flyway ; un mécanisme de sécurité JWT avec cinq rôles et un hachage BCrypt ; un système "
    "d'alertes automatiques ; et une suite de deux cent dix-huit tests automatisés, dont deux cent "
    "quinze tests d'intégration sur PostgreSQL réel et trois tests unitaires.",
)

# ---------------------------------------------------------------------------
# 3. Tableaux : besoins, cas d'utilisation, modèle de données, enums, RBAC
# ---------------------------------------------------------------------------
t_besoins = find_table(["ID", "Catégorie", "Description"])
if t_besoins is not None:
    if set_cell_if(t_besoins, 3, 2, "Gestion des provinces",
                   "Gestion des provinces, communes, zones et collines (hiérarchie administrative)"):
        modifs += 1
    if set_cell_if(t_besoins, 8, 2, "Transferts inter-dépôts",
                   "Transferts inter-dépôts (province, zone) avec vérification de disponibilité à la source"):
        modifs += 1

t_uc = find_table(["ID", "Cas d'utilisation", "Acteur"])
if t_uc is not None:
    if set_cell_if(t_uc, 3, 4, "CRUD provinces", "CRUD provinces/communes/zones/collines"):
        modifs += 1
    if set_cell_if(t_uc, 4, 4, "CRUD des dépôts", "CRUD des dépôts (province, zone)"):
        modifs += 1

t_tables = find_table(["Table", "Description", "Colonnes clés"])
if t_tables is not None:
    descriptions = [r.cells[0].text.strip() for r in t_tables.rows]
    if "commune" not in descriptions:
        insert_row_after(t_tables, 1, [
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
        if label == "depot" and "colline_id" in row.cells[2].text:
            set_cell(row.cells[1], "Dépôts de stockage (province, zone)")
            set_cell(row.cells[2], "id, code, nom, niveau, province_id, zone_id, seuil_alerte_min, "
                                   "capacite_max, actif, created_at")
            modifs += 1

t_enums = find_table(["Enum", "Valeurs", "Usage"])
if t_enums is not None:
    for row in t_enums.rows:
        if row.cells[0].text.strip() == "NiveauDepot" and "COLLINE" in row.cells[1].text:
            set_cell(row.cells[1], "PROVINCE, ZONE")
            modifs += 1

t_rbac = find_table(["Rôle", "Permissions principales", "Périmètre"])
if t_rbac is not None:
    for row in t_rbac.rows:
        if row.cells[0].text.strip() == "AGENT_COLLINE" and "colline" in row.cells[2].text:
            set_cell(row.cells[1], "Distribution et création de tickets au niveau des collines.")
            set_cell(row.cells[2], "Dépôt de sa zone")
            modifs += 1

# ---------------------------------------------------------------------------
# 4. Annexe B : nouveaux endpoints communes/zones
# ---------------------------------------------------------------------------
t_endpoints = find_table(["Méthode", "Endpoint", "Description", "Rôle"])
if t_endpoints is not None:
    endpoints = [r.cells[1].text.strip() for r in t_endpoints.rows]
    if "/api/communes" not in endpoints:
        anchor = next(i for i, r in enumerate(t_endpoints.rows)
                      if r.cells[1].text.strip() == "/api/provinces")
        for values in (
            ("GET", "/api/communes", "Liste des communes", "AUTH"),
            ("GET", "/api/provinces/{id}/communes", "Communes d'une province", "AUTH"),
            ("GET", "/api/communes/{id}/zones", "Zones d'une commune", "AUTH"),
        ):
            insert_row_after(t_endpoints, anchor, values)
            anchor += 1
            modifs += 1

# ---------------------------------------------------------------------------
# 5. Annexe C : extrait de schéma aligné sur V13
# ---------------------------------------------------------------------------
replace_exact("Extrait consolidé des migrations V1, V7, V11 et V12 :",
              "Extrait consolidé des migrations V1, V7, V11, V12 et V13 :")
replace_exact("CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE', 'COLLINE');",
              "CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE');")
replace_exact("colline_id       BIGINT REFERENCES colline(id),",
              "-- V13 : colline_id supprimé (aucun dépôt de colline)")
replace_exact("return depot.getColline() != null && depot.getColline().getZone() != null",
              "return depot.getZone() != null")
replace_exact("&& zoneId.equals(depot.getColline().getZone().getId());",
              "&& zoneId.equals(depot.getZone().getId());")

# Ajout de l'extrait commune/zone avant la table depot de l'annexe C.
anchor = next((p for p in doc.paragraphs if p.text.strip() == "CREATE TABLE depot ("), None)
if anchor is not None and not any(p.text.strip() == "CREATE TABLE commune ("
                                  for p in doc.paragraphs):
    block = [
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
    ]
    for line in block:
        p = anchor.insert_paragraph_before(line, style=anchor.style)
        modifs += 1

doc.save(DOC)

print(f"Rapport mis à jour : {DOC}")
print(f"Modifications appliquées : {modifs}")
if manquants:
    print("Passages non trouvés (déjà corrigés ou reformulés) :")
    for m in manquants:
        print("  -", m)
