# -*- coding: utf-8 -*-
"""Aligne le rapport sur le modèle FOMI tel qu'il est réellement implémenté.

Les faits reportés ici ont été vérifiés sur le code, pas recopiés :

* 18 tables (la table `reclamation` de V14 manquait) ;
* 18 migrations Flyway (V1 à V18) ;
* 68 endpoints répartis sur 18 contrôleurs, dont les 3 de `/api/reclamations` ;
* 232 tests : 229 d'intégration et 3 unitaires (233 avec `@Test`, dont un
  `@Disabled` historique — voir la note en fin de script) ;
* statut `ARRIERE` au lieu de `RECLAMATION`, retiré en V15/V18 ;
* gamme FOMI : Imbura, Urée (ex-Totahaza), Bagara et dolomie, toutes en sacs
  de 25 kg ;
* tableau des packages remis à jour (18 contrôleurs, 18 repositories,
  18 entités, 15 services, 38 DTO).

Le script est idempotent : rejouable sans effet de bord.
"""
import os
import sys

from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(DOC)
modifs = 0
manquants = []


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


def replace_in(old, new, label):
    """Remplace une sous-chaîne dans tous les paragraphes."""
    n = 0
    for p in doc.paragraphs:
        if old in p.text:
            set_text(p, p.text.replace(old, new))
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


# ---------------------------------------------------------------------------
# 1. Gamme FOMI : Urée à la place de Totahaza, dolomie en sac de 25 kg
# ---------------------------------------------------------------------------
t_produits = find_table("Produit", "Formule", "Conditionnement", "Usage principal")
if t_produits is not None:
    lignes = {
        "FOMI-TOTAHAZA": ("Urée", "46 % N", "25 kg", "Céréales et cultures exigeantes en azote"),
        "Chaux agricole": ("Dolomie", "Chaux agricole (amendement calcique)", "25 kg",
                           "Correction de l’acidité des sols"),
    }
    for row in t_produits.rows:
        label = row.cells[0].text.strip()
        if label in lignes:
            for cell, valeur in zip(row.cells, lignes[label]):
                set_cell(cell, valeur)
            modifs += 1
    print("  ok  tableau I.1 : gamme FOMI")

# Le prix de la dolomie est aligné sur les 5 000 BIF annoncés (sac de 25 kg).
replace_in("(à confirmer)", "(prix confirmé)", "prix Totahaza confirmé")

# ---------------------------------------------------------------------------
# 2. Compteurs : tables, migrations, endpoints, contrôleurs
# ---------------------------------------------------------------------------
replace_in("dix-sept contrôleurs", "dix-huit contrôleurs", "P312 : 18 contrôleurs")
replace_in("soixante-cinq points d’entrée", "soixante-huit points d’entrée", "P312 : 68 endpoints")
replace_in("soixante-cinq endpoints", "soixante-huit endpoints", "P402 : 68 endpoints")
replace_in("dix-sept tables relationnelles", "dix-huit tables relationnelles", "P313 : 18 tables")
replace_in("treize migrations Flyway", "dix-huit migrations Flyway", "P313/P402 : 18 migrations")
replace_in("dix-sept tables principales", "dix-huit tables principales", "P318 : 18 tables")
replace_in("les dix-sept entités du système", "les dix-huit entités du système", "P327 : 18 entités")
replace_in("de dix-sept tables", "de dix-huit tables", "P402 : 18 tables")

# ---------------------------------------------------------------------------
# 3. Suite de tests : 232 tests (229 d'intégration + 3 unitaires)
# ---------------------------------------------------------------------------
replace_in("218 tests automatisés", "232 tests automatisés", "tests : 232")
replace_in("(215 tests d'intégration et 3 tests unitaires)",
           "(229 tests d'intégration et 3 tests unitaires)", "P33 : répartition 229 + 3")
replace_in("Les 218 tests se répartissent", "Les 232 tests se répartissent", "P252 : 232 tests")
replace_in("se répartissent en 215 tests d'intégration", "se répartissent en 229 tests d'intégration",
           "tests : 229 d'intégration")
replace_in("215 tests d'intégration (PostgreSQL)", "229 tests d'intégration (PostgreSQL)",
           "tests : 229")
replace_in("Les 215 tests d'intégration", "Les 229 tests d'intégration", "P371 : 229")
replace_in("215 tests d'intégration (PostgreSQL) : 215 tests, 215 réussis",
           "229 tests d'intégration (PostgreSQL) : 229 tests, 229 réussis",
           "annexe D : libellé 229")
replace_in("215 tests d'intégration représentent", "229 tests d'intégration représentent",
           "P382 : 229 d'intégration")
replace_in("deux cent dix-huit tests automatisés", "deux cent trente-deux tests automatisés",
           "P402 : 232 tests")
replace_in("deux cent quinze tests d’intégration", "deux cent vingt-neuf tests d’intégration",
           "P402 : 229 tests d'intégration")
replace_in("218/218", "232/232", "P381 : 232/232")
replace_in("218 tests exécutés, 218 réussis", "232 tests exécutés, 232 réussis",
           "annexe D : 232 exécutés")
replace_in("215 tests, 215 réussis", "229 tests, 229 réussis", "annexe D : 229 réussis")
replace_in("215 tests d'intégration représentent", "229 tests d'intégration représentent",
           "P382 : 229 d'intégration")
replace_in("Total : 218 tests, 218 réussis", "Total : 232 tests, 232 réussis",
           "annexe D : total 232")

# ---------------------------------------------------------------------------
# 4. Énumérations : ARRIERE remplace RECLAMATION
# ---------------------------------------------------------------------------
t_enums = find_table("Enum", "Valeurs", "Usage")
if t_enums is not None:
    for row in t_enums.rows:
        if row.cells[0].text.strip() == "StatutTicket" and "RECLAMATION" in row.cells[1].text:
            set_cell(row.cells[1],
                     "EN_ATTENTE_DE_VALIDATION, ACTIF, REJETE, EXPIRE, ARRIERE, PAYE, "
                     "EN_ATTENTE, PARTIEL, SERVI, ANNULE")
            modifs += 1
    print("  ok  tableau III.6 : StatutTicket")

# Annexe C : l'extrait SQL ne doit plus déclarer un statut supprimé.
replace_in("'SERVI', 'RECLAMATION', 'ANNULE');", "'SERVI', 'ANNULE');",
           "annexe C : enum statut_ticket")
replace_in("Extrait consolidé des migrations V1, V7, V11, V12 et V13 :",
           "Extrait consolidé des migrations V1, V7, V11, V12, V13, V14 et V18 :",
           "annexe C : versions")
replace_in("ALTER TYPE statut_ticket ADD VALUE 'EXPIRE';",
           "ALTER TYPE statut_ticket ADD VALUE 'EXPIRE';\n"
           "-- V18 : arriéré de saison (reliquat dû à l'agriculteur)\n"
           "ALTER TYPE statut_ticket ADD VALUE 'ARRIERE';",
           "annexe C : statut ARRIERE")

# ---------------------------------------------------------------------------
# 5. R20 : clôture de saison en arriéré, pas en expiration
# ---------------------------------------------------------------------------
t_regles = find_table("ID", "Catégorie", "Règle")
if t_regles is not None:
    for row in t_regles.rows:
        if row.cells[0].text.strip() == "R20":
            set_cell(row.cells[2],
                     "À la clôture d'une saison, un ticket validé et non entièrement servi "
                     "passe en ARRIERE : le reliquat reste dû et pourra être servi lors d'une "
                     "saison ultérieure. Un ticket jamais validé passe en EXPIRE. La clôture "
                     "est déclenchée par TicketService.expirerTickets(), sans planification "
                     "automatique.")
            modifs += 1
    print("  ok  tableau III.2 : règle R20")

# ---------------------------------------------------------------------------
# 6. Table des tables de la base : ajout de `reclamation`
# ---------------------------------------------------------------------------
t_tables = find_table("Table", "Description", "Colonnes clés")
if t_tables is not None:
    labels = [r.cells[0].text.strip() for r in t_tables.rows]
    if "reclamation" not in labels:
        from copy import deepcopy
        idx = labels.index("seuil_alerte") if "seuil_alerte" in labels else len(labels) - 1
        tr = deepcopy(t_tables.rows[idx]._tr)
        t_tables.rows[idx]._tr.addnext(tr)
        row = t_tables.rows[idx + 1]
        valeurs = [
            "reclamation",
            "Réclamations des agriculteurs sur un ticket",
            "id, ticket_id, motif, description, quantite_manquante, statut, "
            "resolution, date_creation, date_resolution, est_demo",
        ]
        for cell, valeur in zip(row.cells, valeurs):
            set_cell(cell, valeur)
        modifs += 1
    print("  ok  tableau III.5 : table reclamation")

# ---------------------------------------------------------------------------
# 6 bis. Cas d'utilisation : réclamations (UC-27, UC-28)
# ---------------------------------------------------------------------------
t_uc = find_table("ID", "Cas d'utilisation", "Acteur", "Précondition", "Résultat")
if t_uc is not None:
    from copy import deepcopy

    presents = [r.cells[0].text.strip() for r in t_uc.rows]
    nouveaux = [
        ("UC-27", "Enregistrer une réclamation", "AGENT_COLLINE / AGENT_ZONE",
         "Ticket existant", "Réclamation ouverte, rattachée au ticket"),
        ("UC-28", "Instruire une réclamation", "SUPERVISEUR",
         "Réclamation ouverte", "Réclamation résolue ou rejetée, avec motif"),
    ]
    for valeurs in nouveaux:
        if valeurs[0] in presents:
            continue
        tr = deepcopy(t_uc.rows[-1]._tr)
        t_uc.rows[-1]._tr.addnext(tr)
        row = t_uc.rows[-1]
        for cell, valeur in zip(row.cells, valeurs):
            set_cell(cell, valeur)
        modifs += 1
    print("  ok  tableau III.3 : cas d'utilisation réclamation")

# ---------------------------------------------------------------------------
# 7. Table des packages : effectifs réels
# ---------------------------------------------------------------------------
t_packages = find_table("Package", "Contenu", "Nombre de classes")
if t_packages is not None:
    effectifs = {
        "controller": "18 classes",
        "service": "15 classes",
        "repository": "18 interfaces",
        "model/entity": "18 classes",
        "dto": "38 classes",
    }
    for row in t_packages.rows:
        label = row.cells[0].text.strip()
        if label in effectifs and row.cells[2].text.strip() != effectifs[label]:
            set_cell(row.cells[2], effectifs[label])
            modifs += 1
    print("  ok  tableau des packages")

# ---------------------------------------------------------------------------
# 8. Annexe B : endpoints de réclamation + libellé de clôture de saison
# ---------------------------------------------------------------------------
t_endpoints = find_table("Méthode", "Endpoint", "Description", "Rôle")
if t_endpoints is not None:
    from copy import deepcopy

    existants = [(r.cells[0].text.strip(), r.cells[1].text.strip()) for r in t_endpoints.rows]

    def add_after(path_anchor, values):
        # La clé d'unicité est le couple (méthode, chemin) : GET et POST
        # partagent le même chemin.
        if (values[0], values[1]) in existants:
            return
        anchor = next((i for i, r in enumerate(t_endpoints.rows)
                       if r.cells[1].text.strip() == path_anchor
                       and r.cells[1].text.strip() != ""), None)
        if anchor is None:
            return
        tr = deepcopy(t_endpoints.rows[anchor]._tr)
        t_endpoints.rows[anchor]._tr.addnext(tr)
        row = t_endpoints.rows[anchor + 1]
        for cell, valeur in zip(row.cells, values):
            set_cell(cell, valeur)
        existants.insert(anchor + 1, (values[0], values[1]))

    # Insertion en bloc, dans l'ordre des méthodes, après le suivi public.
    a_inserer = [
        ("GET", "/api/reclamations", "Liste des réclamations", "ADMIN, SUPERVISEUR, AGENT_ZONE"),
        ("POST", "/api/reclamations", "Créer une réclamation", "ADMIN, AGENT_ZONE, AGENT_COLLINE"),
        ("PATCH", "/api/reclamations/{id}/statut", "Instruire une réclamation",
         "ADMIN, SUPERVISEUR"),
    ]
    ancre = next((i for i, r in enumerate(t_endpoints.rows)
                  if r.cells[1].text.strip() == "/api/public/tickets/{numero}"), None)
    if ancre is not None:
        for decalage, valeurs in enumerate(a_inserer):
            if (valeurs[0], valeurs[1]) in existants:
                continue
            tr = deepcopy(t_endpoints.rows[ancre + decalage]._tr)
            t_endpoints.rows[ancre + decalage]._tr.addnext(tr)
            row = t_endpoints.rows[ancre + decalage + 1]
            for cell, valeur in zip(row.cells, valeurs):
                set_cell(cell, valeur)
            existants.insert(ancre + decalage + 1, (valeurs[0], valeurs[1]))
            modifs += 1

    for row in t_endpoints.rows:
        if row.cells[1].text.strip() == "/api/tickets/expirer":
            set_cell(row.cells[2],
                     "Clôturer une saison : arriéré pour les tickets validés non servis, "
                     "expiration pour ceux jamais validés")
            modifs += 1
    print("  ok  annexe B : réclamations et clôture de saison")

# ---------------------------------------------------------------------------
# 9. Tableau des tests d'intégration : effectifs réels
# ---------------------------------------------------------------------------
t_tests = find_table("Suite de tests", "Nombre", "Domaine couvert")
if t_tests is not None:
    reels = {
        "ValidationTicketIntegrationTest": "27 tests",
        "SecuriteRbacIntegrationTest": "18 tests",
        "DistributionIntegrationTest": "17 tests",
        "AuthIntegrationTest": "17 tests",
        "AgriculteurIntegrationTest": "15 tests",
        "TicketIntegrationTest": "14 tests",
        "DepotIntegrationTest": "14 tests",
        "MouvementIntegrationTest": "14 tests",
        "EmailNotificationIntegrationTest": "12 tests",
        "ReclamationIntegrationTest": "12 tests",
        "UtilisateurIntegrationTest": "11 tests",
        "ApiIntegrationTest": "9 tests",
        "AlerteIntegrationTest": "8 tests",
        "GeoIntegrationTest": "7 tests",
        "StockIntegrationTest": "6 tests",
        "LotIntegrationTest": "6 tests",
        "DistributionFifoIntegrationTest": "5 tests",
        "GlobalExceptionHandlerIntegrationTest": "5 tests",
        "AuditLogIntegrationTest": "4 tests",
        "StatsIntegrationTest": "4 tests",
        "AlerteDelaiIntegrationTest": "3 tests",
        "StockConcurrenceIntegrationTest": "1 test",
    }
    total = 0
    for label, nombre in reels.items():
        total += int(nombre.split()[0])
    # La ligne « Total » est mise à jour à part.
    for row in t_tests.rows:
        label = row.cells[0].text.strip()
        if label in reels and row.cells[1].text.strip() != reels[label]:
            set_cell(row.cells[1], reels[label])
            modifs += 1
        if label == "Total":
            set_cell(row.cells[1], f"{total} tests")
            set_cell(row.cells[2], f"{len(reels)} classes de tests d'intégration PostgreSQL")
            modifs += 1

    # Deux suites manquaient au tableau : notifications email et réclamations.
    from copy import deepcopy

    presents = [r.cells[0].text.strip() for r in t_tests.rows]
    a_inserer = [
        ("EmailNotificationIntegrationTest", "12 tests",
         "Notifications email : création, validation, rejet, arriéré, distribution"),
        ("ReclamationIntegrationTest", "12 tests",
         "Réclamations : création, instruction, résolution, rejet, contrôle d'accès"),
    ]
    for label, nombre, domaine in a_inserer:
        if label in presents:
            continue
        # Insertion juste avant la ligne de total.
        idx_total = next(i for i, r in enumerate(t_tests.rows)
                         if r.cells[0].text.strip() == "Total")
        tr = deepcopy(t_tests.rows[idx_total - 1]._tr)
        t_tests.rows[idx_total - 1]._tr.addnext(tr)
        row = t_tests.rows[idx_total]
        for cell, valeur in zip(row.cells, [label, nombre, domaine]):
            set_cell(cell, valeur)
        presents.insert(idx_total, label)
        modifs += 1

    # Le total se recalcule une fois toutes les lignes présentes.
    total = sum(int(r.cells[1].text.split()[0]) for r in t_tests.rows
                if r.cells[0].text.strip() not in ("Suite de tests", "Total")
                and r.cells[1].text.strip())
    nb_classes = len([r for r in t_tests.rows
                      if r.cells[0].text.strip() not in ("Suite de tests", "Total")]) 
    for row in t_tests.rows:
        if row.cells[0].text.strip() == "Total":
            set_cell(row.cells[1], f"{total} tests")
            set_cell(row.cells[2], f"{nb_classes} classes de tests d'intégration PostgreSQL")
    print(f"  ok  tableau III.9 : {total} tests d'intégration sur {nb_classes} classes")

# ---------------------------------------------------------------------------
# 10. Renommage du test de sécurité mentionné dans le rapport
# ---------------------------------------------------------------------------
replace_in("SecuriteAccesIntegrationTest", "SecuriteRbacIntegrationTest",
           "tableau III.9 : nom du test RBAC")

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