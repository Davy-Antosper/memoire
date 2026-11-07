# -*- coding: utf-8 -*-
"""Corrections factuelles du rapport restructure (API Spring Boot reelle)."""
import os
from copy import deepcopy
from docx import Document
from docx.table import _Row
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")


def set_para_text(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)


def replace_para(prefix, new_text):
    matches = [p for p in doc.paragraphs if p.text.strip().startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"Prefixe trouve {len(matches)} fois : {prefix!r}")
    set_para_text(matches[0], new_text)
    print("OK para:", prefix[:55])


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


def rebuild_table(table, rows):
    if len(table.rows) < 2:
        raise RuntimeError("Table sans ligne de donnees")
    template = deepcopy(table.rows[1]._tr)
    for row in list(table.rows)[1:]:
        table._tbl.remove(row._tr)
    for data in rows:
        new_tr = deepcopy(template)
        table._tbl.append(new_tr)
        row = _Row(new_tr, table)
        if len(row.cells) != len(data):
            raise RuntimeError(f"Nombre de colonnes {len(row.cells)} != {len(data)}")
        for cell, val in zip(row.cells, data):
            set_cell(cell, val)
    print(f"OK table {len(rows)} lignes")


def delete_between(start_para, end_para):
    el = start_para._element.getnext()
    while el is not None and el is not end_para._element:
        nxt = el.getnext()
        el.getparent().remove(el)
        el = nxt


def insert_after(anchor, template_el, text):
    new_el = deepcopy(template_el)
    anchor._element.addnext(new_el)
    new_para = Paragraph(new_el, anchor._parent)
    set_para_text(new_para, text)
    return new_para


doc = Document(DOC)

# ---------------------------------------------------------------------------
# 1. Paragraphes factuels
# ---------------------------------------------------------------------------
replace_para(
    "Le projet compte 203 tests",
    "Le projet compte 207 tests automatisés (204 tests d'intégration et 3 tests unitaires), tous validés. "
    "La solution répond aux 25 besoins fonctionnels identifiés et intègre des mécanismes de sécurité avancés. "
    "Ce travail constitue une contribution significative à la modernisation de la gestion des stocks agricoles "
    "au Burundi et ouvre des perspectives d'évolution vers une plateforme numérique complète intégrant les "
    "clients web et mobile déjà développés, les notifications SMS et les paiements mobiles.",
)

replace_para(
    "PostgreSQL 16 a été sélectionné",
    "PostgreSQL 16 a été sélectionné comme SGBD pour sa robustesse éprouvée, sa conformité aux standards SQL "
    "et ses fonctionnalités avancées. Les énumérations nommées offrent un mécanisme natif pour garantir "
    "l'intégrité des données au niveau de la base. Le type JSONB permet de stocker des données structurées "
    "de manière flexible, notamment les détails des opérations dans la table audit_log. Les index B-tree et "
    "composites sur les colonnes fréquemment utilisées dans les clauses WHERE, JOIN et ORDER BY réduisent "
    "significativement le temps d'exécution des requêtes. Aucun index GIN n'est utilisé dans l'implémentation actuelle.",
)

replace_para(
    "Spring Security est le framework",
    "Spring Security est le framework de référence pour la sécurité des applications Spring. Dans le contexte "
    "de l'API FOMI, il est configuré en mode stateless, désactivant les sessions côté serveur. Le cycle JWT "
    "complet est implémenté : génération du token lors du login, validation à chaque requête via un filtre "
    "personnalisé, et rejet automatique des tokens expirés. Les règles d'autorisation sont déclarées dans la "
    "classe SecurityConfig, sous forme de règles par URL et par méthode HTTP ; le code n'utilise pas les "
    "annotations @PreAuthorize ou @Secured.",
)

replace_para(
    "Testcontainers lance une instance",
    "Testcontainers lance une instance PostgreSQL réelle en Docker pour les tests d'intégration, garantissant "
    "la fidélité des tests par rapport à la production. JUnit 5 fournit les annotations et les assertions. "
    "Les 207 tests se répartissent en 204 tests d'intégration (PostgreSQL) et 3 tests unitaires de configuration ; "
    "ils couvrent la sécurité RBAC, la concurrence (pessimistic locking) et les cas métier (FIFO, annulation, alertes).",
)

replace_para(
    "Vingt-six besoins fonctionnels",
    "Vingt-cinq besoins fonctionnels ont été identifiés à partir de l'analyse des exigences de FOMI, des "
    "entretiens avec les parties prenantes et de l'étude du contexte opérationnel. Ces besoins couvrent "
    "l'authentification et la sécurité, la gestion des données de référence, la gestion des stocks, la "
    "distribution et les tickets, le reporting et l'audit, ainsi que l'intégrité des données.",
)

replace_para(
    "Vingt-trois règles métier",
    "Vingt-deux règles métier ont été identifiées pour garantir l'intégrité des données et la cohérence des "
    "opérations dans le système. Ces règles encadrent les opérations de stock, la distribution aux agriculteurs, "
    "la validation des tickets et le fonctionnement du système d'alertes. Chaque règle est implémentée dans la "
    "couche Service du système et validée par des tests d'intégration correspondants.",
)

replace_para(
    "Couche Repository :",
    "Couche Repository : assure la communication avec la base de données via Spring Data JPA. Les repositories "
    "encapsulent les requêtes de persistance, incluant les requêtes JPQL personnalisées (@Query) pour les "
    "opérations complexes de recherche, d'agrégation et de reporting. Les specifications JPA sont utilisées pour "
    "la recherche multicritère dynamique, permettant de construire des requêtes variables sans concaténation de "
    "chaînes SQL. Le pessimistic locking (SELECT FOR UPDATE) est utilisé dans les repositories de stock pour "
    "garantir l'intégrité des données en présence de transactions concurrentes. Le système compte 16 repositories.",
)

replace_para(
    "Couche Sécurité (Security) :",
    "Couche Sécurité (Security) : intercepte chaque requête entrante via le filtre JwtAuthFilter pour vérifier "
    "l'authenticité du token JWT, extraire les informations de l'utilisateur (identifiant, rôle, périmètre "
    "géographique) et appliquer les règles RBAC définies dans SecurityConfig. Le filtrage de périmètre est "
    "assuré dans les services et les contrôleurs ; il n'existe pas d'aspect AOP dédié (SecurityScopeAspect). "
    "Le SecurityContext est configuré pour chaque requête et ne persiste pas entre les requêtes (stateless).",
)

replace_para(
    "Couche Service :",
    "Couche Service : contient la logique métier du système. C'est dans cette couche que sont implémentées les "
    "22 règles métier identifiées lors de l'analyse : l'algorithme FIFO dans StockService.sortirFifo(), le "
    "contrôle des quotas dans TicketService.creer(), le dédoublement des alertes dans AlerteService.creerSiAbsente(), "
    "l'annulation avec ajustement dans MouvementService.annuler(), et le calcul des statistiques dans StatsService. "
    "Les services sont responsables de la gestion des transactions (@Transactional), de la coordination entre les "
    "repositories et de l'appel à AuditLogService pour l'enregistrement des opérations critiques. Le package "
    "service compte 11 classes, dont 9 services métier et 2 utilitaires.",
)

replace_para(
    "Base de données (PostgreSQL 16) :",
    "Base de données (PostgreSQL 16) : couche de persistance, stockant les données dans des tables relationnelles "
    "avec des index optimisés pour les requêtes fréquentes. Les types enum nommés de PostgreSQL assurent "
    "l'intégrité des données au niveau de la base. Les index B-tree sont créés sur les colonnes fréquemment "
    "utilisées dans les clauses WHERE et JOIN (depot_id, engrais_type_id, statut, date_creation), et des index "
    "composites couvrent notamment la table audit_log. Aucun index GIN n'est utilisé sur la colonne details_json. "
    "Le schéma de la base de données est géré par Flyway avec 11 versions de migration numérotées.",
)

replace_para(
    "Le diagramme de séquence de la distribution FIFO",
    "Le diagramme de séquence de la distribution FIFO détaille le processus de distribution d'engrais à un "
    "agriculteur selon le principe First-In-First-Out. L'agent sélectionne un ticket actif via "
    "DistributionController.distribuer(), et le DistributionService orchestre l'opération. Le "
    "StockService.sortirFifo() identifie les lots à distribuer en les triant par date de réception à FOMI "
    "(dateReceptionFomi), après exclusion des lots périmés et vides. Les stocks sont décrémentés lot par lot "
    "dans stock_lot jusqu'à satisfaction de la quantité demandée. Chaque sortie de lot génère un mouvement de "
    "stock de type DISTRIBUTION et un log d'audit via AuditLogService.log(). Le ticket est mis à jour avec la "
    "quantité servie et le statut approprié (PARTIEL ou SERVI).",
)

replace_para(
    "Le ticket de distribution suit un workflow",
    "Le ticket de distribution suit un workflow défini par une machine à états de dix états. Les états et "
    "transitions possibles sont les suivants :",
)
replace_para(
    "EN_ATTENTE_DE_VALIDATION → EXPIRE : le ticket n'a pas été validé dans un délai de 30 jours. Cette transition est déclenchée automatiquement par un cron job planifié.",
    "Autres états : PAYE, EN_ATTENTE et RECLAMATION complètent l'énumération StatutTicket ; ils correspondent "
    "à des situations héritées ou spécifiques et ne sont pas utilisés comme état initial par le service de création.",
)
replace_para(
    "ACTIF/PARTIEL → ANNULE : le ticket est annulé à la demande de l'agriculteur ou en cas d'irrégularité détectée. Les distributions déjà effectuées sont annulées en sens inverse (rétroaction sur stock).",
    "EXPIRE : la méthode TicketService.expirerTickets(saison) marque EXPIRE tous les tickets non servis de "
    "la saison, à l'exception de ceux déjà ANNULE, REJETE, EXPIRE ou SERVI ; elle existe dans le code mais "
    "n'est reliée à aucune tâche planifiée ni à aucun endpoint.",
)
replace_para(
    "ACTIF/PARTIEL → SERVI : la totalité de la quantité demandée a été distribuée. Le ticket est clôturé définitivement.",
    "ACTIF/PARTIEL → ANNULE : le ticket est annulé à la demande de l'agriculteur ou en cas d'irrégularité "
    "détectée. Les distributions déjà effectuées font l'objet d'un ajustement de stock.",
)
replace_para(
    "ACTIF → PARTIEL : une partie de la quantité demandée a été distribuée. Le ticket reste actif pour permettre la distribution du solde lors de la prochaine disponibilité du stock.",
    "ACTIF/PARTIEL → SERVI : la totalité de la quantité demandée a été distribuée. Le ticket est clôturé "
    "définitivement.",
)
replace_para(
    "EN_ATTENTE_DE_VALIDATION → REJETE : le responsable rejette le ticket avec un motif obligatoire. Les motifs les plus fréquents sont : superficie insuffisante, doublon détecté, données erronées, ou documents manquants.",
    "ACTIF → PARTIEL : une partie de la quantité demandée a été distribuée. Le ticket reste actif pour "
    "permettre la distribution du solde lors de la prochaine disponibilité du stock.",
)
replace_para(
    "EN_ATTENTE_DE_VALIDATION → ACTIF : le responsable valide le ticket après vérification de la conformité des informations. Le ticket est maintenant traitable par les agents de distribution.",
    "EN_ATTENTE_DE_VALIDATION → REJETE : le responsable rejette le ticket avec un motif obligatoire. Les "
    "motifs les plus fréquents sont : superficie insuffisante, doublon détecté, données erronées ou "
    "documents manquants.",
)
replace_para(
    "PAYE → EN_ATTENTE_DE_VALIDATION",
    "EN_ATTENTE_DE_VALIDATION → ACTIF : le responsable valide le ticket après vérification de la conformité "
    "des informations. Le ticket devient traitable par les agents de distribution.",
)
replace_para(
    "PAYE : état initial",
    "EN_ATTENTE_DE_VALIDATION : état initial à la création du ticket. Le ticket est enregistré avec les "
    "informations de l'agriculteur, le type d'engrais demandé et la quantité, puis soumis à la validation "
    "d'un responsable.",
)

replace_para(
    "L'algorithme FIFO (First-In",
    "L'algorithme FIFO (First-In, First-Out) est le cœur du mécanisme de distribution des engrais. Il garantit "
    "que les lots les plus anciens, c'est-à-dire ceux réceptionnés le plus tôt à FOMI, sont distribués en "
    "priorité. Le système exclut par ailleurs les lots dont la date de péremption est dépassée, afin de limiter "
    "les pertes. La teneur en nutriments des engrais diminuant avec le temps, une rotation rigoureuse des lots "
    "est indispensable.",
)
replace_para(
    "Étape 1 — Récupération",
    "Étape 1 — Récupération des lots disponibles : le StockLotRepository interroge la table stock_lot pour "
    "obtenir tous les lots du dépôt concerné pour le type d'engrais demandé, en appliquant deux filtres : le "
    "stock du lot doit être supérieur à zéro, et la date de péremption du lot ne doit pas être dépassée. Les "
    "lots expirés sont donc exclus de la distribution, même s'ils contiennent encore du stock.",
)
replace_para(
    "Étape 2 — Tri",
    "Étape 2 — Tri par date de réception FOMI croissante : les lots récupérés sont triés par dateReceptionFomi "
    "dans l'ordre croissant (requête "
    "findByDepotIdAndLotEngraisTypeIdAndQuantiteGreaterThanOrderByLotDateReceptionFomiAsc). Le lot réceptionné "
    "le plus anciennement est traité en premier. Le tri ne s'appuie pas sur la date de péremption.",
)
replace_para(
    "Étape 3 — Distribution",
    "Étape 3 — Distribution itérative : pour chaque lot dans l'ordre du tri, le système calcule la quantité à "
    "distribuer comme le minimum entre le stock disponible du lot et la quantité restante à satisfaire. Cette "
    "quantité est retirée du stock_lot ; le stock agrégé est décrémenté une seule fois à la fin de la boucle. "
    "La boucle se poursuit jusqu'à ce que la quantité totale demandée soit satisfaite ou qu'il n'y ait plus de "
    "lots disponibles.",
)
replace_para(
    "Étape 4 — Enregistrement",
    "Étape 4 — Enregistrement des mouvements : de retour dans DistributionService.distribuer(), chaque LotSortie "
    "produit un mouvement de type DISTRIBUTION dans la table mouvement, avec le lot, le dépôt source, le ticket "
    "et l'agent. Une distribution détaillée est également enregistrée dans la table distribution.",
)
replace_para(
    "Étape 5 — Mise à jour",
    "Étape 5 — Mise à jour du ticket : la quantité totale distribuée est ajoutée au champ quantite_servie du "
    "ticket. Le statut est recalculé par ticket.mettreAJourStatut() : SERVI si la totalité est satisfaite, "
    "PARTIEL si un solde subsiste.",
)

replace_para(
    "Le système implémente un contrôle",
    "Le système implémente un contrôle d'accès basé sur les rôles (RBAC) avec cinq rôles distincts, chacun "
    "disposant d'un ensemble défini de permissions. Des contrôles de périmètre géographique sont effectués dans "
    "les services et les contrôleurs pour restreindre l'accès aux données selon le niveau hiérarchique de "
    "l'utilisateur. Cette double restriction (rôle + périmètre) vise à garantir que chaque acteur n'accède "
    "qu'aux fonctionnalités et données relevant de sa compétence.",
)
replace_para(
    "L'authentification est basée sur les tokens JWT",
    "L'authentification est basée sur les tokens JWT (JSON Web Token) signés avec l'algorithme HMAC-SHA256. "
    "Le processus d'authentification se déroule comme suit : l'utilisateur envoie son nom d'utilisateur et son "
    "mot de passe via l'endpoint POST /api/auth/login ; l'AuthenticationManager vérifie les identifiants en "
    "comparant le hash BCrypt du mot de passe fourni avec celui stocké en base ; si les identifiants sont "
    "valides, un token JWT est généré contenant l'identifiant de l'utilisateur, son rôle, son périmètre "
    "géographique (depotId) et la date d'expiration (24 heures) ; le token est retourné au client.",
)

replace_para(
    "L'implémentation du mécanisme FIFO constitue",
    "L'implémentation du mécanisme FIFO constitue l'un des aspects les plus critiques et les plus complexes du "
    "système. La méthode principale StockService.sortirFifo() orchestre l'ensemble du processus de distribution "
    "en garantissant l'intégrité des données même en présence de transactions concurrentes.",
)
replace_para(
    "L'implémentation utilise le pessimistic locking (SELECT FOR UPDATE)",
    "L'implémentation utilise le pessimistic locking (SELECT FOR UPDATE) dans StockLotRepository pour garantir "
    "que deux agents ne puissent pas distribuer le même stock simultanément. Le verrou est posé sur les lignes "
    "stock_lot lors de la sélection des lots et maintenu jusqu'à la fin de la transaction. En cas de conflit, "
    "l'exception de verrouillage remonte au gestionnaire global d'exceptions, qui renvoie une erreur HTTP ; "
    "aucun mécanisme de retry automatique n'est implémenté.",
)
replace_para(
    "La méthode procède comme suit",
    "La méthode procède comme suit : Étape 1 — Récupération des lots disponibles via "
    "StockLotRepository.findByDepotIdAndLotEngraisTypeIdAndQuantiteGreaterThanOrderByLotDateReceptionFomiAsc(), "
    "filtrés pour exclure les lots périmés et les lots vides. Étape 2 — Tri par date de réception FOMI "
    "croissante. Étape 3 — Distribution itérative lot par lot en décrémentant les stock_lot. Étape 4 — "
    "Enregistrement des mouvements de type DISTRIBUTION. Étape 5 — Mise à jour du ticket (quantite_servie et statut).",
)

replace_para(
    "Le mécanisme de dédoublement",
    "Le mécanisme de dédoublement est essentiel pour éviter la multiplication d'alertes identiques. La méthode "
    "AlerteService.creerSiAbsente() vérifie l'existence d'une alerte non traitée de même type, même dépôt et "
    "même type d'engrais avant d'en créer une nouvelle. Si une alerte similaire existe déjà, aucune nouvelle "
    "alerte n'est créée.",
)
replace_para(
    "Deux cron jobs planifiés",
    "Deux tâches planifiées via l'annotation @Scheduled complètent la détection en temps réel : la première "
    "s'exécute à 06h00 chaque jour pour vérifier les tickets non servis dont la date de paiement dépasse "
    "7 jours (alertes DELAI_DEPASSE) ; la seconde s'exécute à 06h30 pour identifier les dépôts actifs sans "
    "aucun mouvement de stock depuis 7 jours (alertes INACTIVITE). Les alertes de rupture, de stock bas, de "
    "péremption et de demande supérieure au stock sont, elles, générées par AlerteService.verifierDepot() "
    "après chaque mouvement de stock.",
)

replace_para(
    "Le workflow de validation des tickets",
    "Le workflow de validation des tickets implémente un processus en deux étapes avec vérifications "
    "automatiques à la création. Lors de la création du ticket (TicketService.creer()), le système vérifie "
    "plusieurs règles métier : le quota de superficie (R2 : la quantité demandée ne doit pas dépasser "
    "superficie × 150 kg/ha), le cumul des tickets de la même saison, l'unicité par saison et type d'engrais "
    "(R6), ainsi que l'existence de l'agriculteur, du type d'engrais et du dépôt de retrait. La disponibilité "
    "du stock n'est pas contrôlée à la création ; elle est vérifiée au moment de la distribution.",
)
replace_para(
    "Lors de la validation par le responsable (TicketService",
    "Lors de la validation par le responsable (TicketService.activer()), le système vérifie que le ticket est "
    "bien en EN_ATTENTE_DE_VALIDATION puis le passe à ACTIF. Aucune re-vérification du stock ou des quotas n'est "
    "effectuée à cette étape. Le responsable peut également rejeter le ticket via TicketService.rejeter() avec "
    "un motif ; le statut passe à REJETE. Une fois le ticket ACTIF, il peut être traité par un agent lors de la "
    "distribution via DistributionService.distribuer().",
)

replace_para(
    "Le mécanisme d'annulation des mouvements est une fonctionnalité critique",
    "Le mécanisme d'annulation des mouvements est une fonctionnalité critique pour la correction des erreurs et "
    "la gestion des litiges. Deux types d'annulation sont supportés, implémentés dans MouvementService.annuler() : "
    "l'annulation d'un transfert et celle d'une distribution.",
)
replace_para(
    "Annulation d'une distribution : lorsqu'un mouvement de type SORTIE (distribution) est annulé",
    "Annulation d'une distribution : lorsqu'un mouvement de type DISTRIBUTION est annulé, le système décrémente "
    "la quantite_servie du ticket associé, met à jour son statut et supprime l'enregistrement de distribution "
    "correspondant. En revanche, le stock du dépôt n'est pas réincrémenté, ce qui peut créer un écart entre le "
    "stock physique et le stock logique. Un mouvement de type AJUSTEMENT est créé avec une référence vers le "
    "mouvement annulé.",
)
replace_para(
    "Annulation d'un transfert : lorsqu'un mouvement de type TRANSFERT est annulé",
    "Annulation d'un transfert : lorsqu'un mouvement de type TRANSFERT est annulé, le stock est restauré au "
    "dépôt source (incrémenté) et retiré du dépôt destination (décrémenté). Cette opération atomique garantit "
    "la cohérence des stocks entre les deux dépôts. Un mouvement de type AJUSTEMENT est créé avec la référence "
    "du transfert original.",
)
replace_para(
    "Dans les deux cas, des vérifications",
    "Dans les deux cas, des vérifications sont effectuées avant l'annulation : le mouvement ne doit pas déjà "
    "être annulé (R7 : anti-double annulation), une réception FOMI ou un ajustement ne peut pas être annulé, "
    "et un log d'audit est généré pour tracer l'opération de correction. L'annulation d'un transfert vérifie "
    "également la disponibilité du stock au dépôt destination.",
)

replace_para(
    "Stocks par province",
    "Stocks par province : agrégation des stocks de tous les dépôts d'une province, ventilée par type d'engrais. "
    "Les données sont présentées sous forme de tableau avec les colonnes province, type d'engrais, stock_total "
    "et statut (OK/BAS/CRITIQUE). Cette vue permet d'identifier rapidement les provinces sous-approvisionnées "
    "nécessitant un transfert de stock.",
)
replace_para(
    "Mouvements par agent",
    "Mouvements par agent : historique des opérations effectuées par chaque agent, avec comptage par type de "
    "mouvement (RECEPTION_FOMI, TRANSFERT, DISTRIBUTION, AJUSTEMENT). Utile pour le suivi de productivité, la "
    "détection d'anomalies et la préparation des audits internes.",
)

replace_para(
    "Le mécanisme d'audit trail est implémenté via la classe AuditLogService",
    "Le mécanisme d'audit trail est implémenté via la classe AuditLogService, appelée explicitement dans les "
    "services lors des opérations critiques (création, validation, distribution, annulation, réception, "
    "transfert). Il n'existe pas d'aspect AOP automatique de type AuditLogAspect ni d'annotation @Auditable : "
    "l'appel à AuditLogService.log() est donc manuel et doit être maintenu par les développeurs.",
)
replace_para(
    "Les logs d'audit sont stockés dans la table audit_log",
    "Les logs d'audit sont stockés dans la table audit_log avec des index optimisés pour les requêtes de "
    "consultation courantes : un index sur entity_type + entity_id pour les recherches par entité, un index "
    "sur utilisateur_id pour les recherches par agent et un index sur created_at pour le tri chronologique. "
    "L'endpoint de consultation (AuditLogController) offre une pagination plafonnée à 200 éléments par page et "
    "des filtres par action, type d'entité, identifiant d'entité et utilisateur. Il ne propose pas de filtre "
    "par plage de dates. La colonne details_json est de type JSONB, mais aucun index GIN n'y est associé.",
)

replace_para(
    "La stratégie de test du projet",
    "La stratégie de test du projet repose principalement sur des tests d'intégration. Les 204 tests "
    "d'intégration sont exécutés avec une instance PostgreSQL réelle lancée via Testcontainers et vérifient le "
    "comportement de l'API de bout en bout, de la couche HTTP à la base de données. Ils sont complétés par "
    "3 tests unitaires de configuration. Le projet ne comporte donc pas de pyramide de tests classique "
    "majoritairement unitaire.",
)
replace_para(
    "Les tests d'intégration, constituant le sommet de la pyramide",
    "Les tests d'intégration sont exécutés avec une instance PostgreSQL réelle lancée via Testcontainers. Ils "
    "vérifient le fonctionnement correct de l'ensemble du système, de la couche API à la base de données, en "
    "incluant les transactions, les contraintes d'intégrité référentielle et les index de performance. "
    "L'utilisation de Testcontainers garantit que les tests s'exécutent dans un environnement identique à la "
    "production, éliminant les bugs liés aux différences comportementales entre une base en mémoire et PostgreSQL.",
)

replace_para(
    "La suite de tests complète compte 203",
    "La suite de tests complète compte 207 tests automatisés, tous en succès (207/207). La couverture de code "
    "n'a pas été mesurée avec un outil dédié ; elle n'est donc pas chiffrée dans ce rapport. Les tests couvrent "
    "l'ensemble des besoins fonctionnels critiques (F1-F25), des règles métier (R1-R22) et des cas d'utilisation "
    "(UC-01 à UC-26).",
)
replace_para(
    "Le temps d'exécution total de la suite de tests",
    "Le temps d'exécution total de la suite est d'environ 3 minutes, dont une part importante correspond au "
    "démarrage de l'instance Docker PostgreSQL utilisée par Testcontainers. Les 204 tests d'intégration "
    "représentent l'essentiel de la durée, les 3 tests unitaires étant quasi instantanés.",
)

replace_para(
    "Le tableau ci-dessous présente la conformité",
    "Le tableau ci-dessous présente la conformité du système réalisé par rapport aux 25 besoins fonctionnels "
    "du cahier des charges. Chaque besoin a été implémenté dans les couches appropriées du système et validé "
    "par des tests d'intégration spécifiques.",
)
replace_para(
    "L'analyse de conformité révèle",
    "L'analyse de conformité révèle un taux d'implémentation de 100 % pour l'ensemble des 25 besoins "
    "fonctionnels. Chaque besoin a été implémenté et validé par des tests d'intégration correspondants, "
    "garantissant non seulement la présence du code mais aussi son fonctionnement correct dans les conditions "
    "réelles d'utilisation.",
)

replace_para(
    "Pagination :",
    "Pagination : les endpoints de liste (tickets, agriculteurs, mouvements, audit) utilisent une pagination "
    "côté serveur via Spring Data. Les contrôleurs plafonnent la taille de page à 200 éléments. Certains "
    "référentiels (types d'engrais, provinces, zones, collines, dépôts, lots, stocks) renvoient l'ensemble "
    "des éléments sans pagination.",
)
replace_para(
    "Index de base de données",
    "Index de base de données : des index B-tree ont été créés sur les clés étrangères et les colonnes de "
    "filtrage fréquentes : lot_id, depot_source_id, depot_dest_id, ticket_id, statut, date_mouvement, "
    "utilisateur_id. Des index composites couvrent (depot_retrait_id, statut) pour les tickets, "
    "(lot_id, date_mouvement) pour les mouvements, (entity_type, entity_id) et (utilisateur_id, created_at) "
    "pour l'audit, ainsi que (depot_id, traitee) pour les alertes. La contrainte UNIQUE "
    "(depot_id, engrais_type_id) de la table stock joue également le rôle d'index composite. Aucun index GIN "
    "n'a été créé sur details_json.",
)
replace_para(
    "Requêtes JPQL optimisées",
    "Requêtes JPQL optimisées : les agrégations des tableaux de bord sont effectuées côté serveur SQL "
    "(SUM, COUNT, GROUP BY) plutôt qu'en mémoire Java, réduisant la consommation de mémoire et le temps de "
    "traitement. Le service de statistiques ne recourt toutefois pas systématiquement à JOIN FETCH ni à DISTINCT.",
)
replace_para(
    "La maintenabilité du système est un critère",
    "La maintenabilité du système est un critère essentiel pour un projet destiné à être maintenu et évolué par "
    "des équipes internes à FOMI. Plusieurs facteurs contribuent à la maintenabilité : l'architecture en couches "
    "claire permet de localiser rapidement les modifications nécessaires sans impact sur les autres couches ; la "
    "documentation Swagger offre une vue complète et interactive de l'API, permettant aux nouveaux développeurs "
    "de comprendre le système en quelques minutes ; les 207 tests automatisés garantissent que les modifications "
    "n'introduisent pas de régressions (principe de sécurité de refactoring) ; la gestion des migrations Flyway "
    "assure la traçabilité des évolutions du schéma de la base de données ; et les conventions de nommage "
    "cohérentes (controllers, services, repositories) facilitent la navigation dans le code source.",
)

replace_para(
    "— Filtrage périmètre géographique",
    "— Contrôles de périmètre géographique dans les services et contrôleurs : un agent de colline ne peut accéder "
    "qu'aux données de son dépôt et un agent de zone uniquement aux dépôts de sa zone. Il n'existe pas d'aspect "
    "AOP dédié (SecurityScopeAspect) ; ces contrôles sont explicites dans le code.",
)
replace_para(
    "— Headers de sécurité HTTP",
    "— Les en-têtes de sécurité HTTP (Content-Security-Policy, X-Content-Type-Options, X-Frame-Options) ne sont "
    "pas configurés explicitement dans l'API actuelle ; leur ajout constitue une recommandation.",
)

replace_para(
    "1. Créer une Un Systeme",
    "1. Créer un système centralisé pour la gestion des stocks d'engrais de la société FOMI, offrant une "
    "interface standardisée pour toutes les opérations de gestion de stock (réception FOMI, transfert, "
    "distribution, ajustement). Ce système doit être documenté, testé et sécurisé, prêt à être consommé par un "
    "client web ou mobile.",
)
replace_para(
    "Le mécanisme de distribution repose sur un circuit hiérarchisé",
    "Le mécanisme de distribution repose sur un circuit hiérarchisé acheminant les produits depuis l'usine FOMI "
    "de Maramvya jusqu'aux agriculteurs bénéficiaires. Les engrais, d'abord stockés à l'usine, sont acheminés "
    "vers les dépôts provinciaux, puis vers les dépôts de zone et de colline, où les agriculteurs viennent "
    "retirer leurs engrais sur présentation de leurs tickets. Ce circuit implique de multiples acteurs et "
    "institutions, chacun jouant un rôle spécifique dans la chaîne de distribution.",
)

# ---------------------------------------------------------------------------
# 2. Hierarchie introduction : 1.1 a 1.4 en Heading 3
# ---------------------------------------------------------------------------
for title in [
    "1.1 Le contexte géographique et économique du Burundi",
    "1.2 La fertilité des sols et l’usage des engrais",
    "1.3 Le Programme National de Subvention des Engrais (PNSEB)",
    "1.4 La réforme administrative de 2023",
]:
    found = [p for p in doc.paragraphs if p.text.strip() == title]
    if len(found) != 1:
        raise RuntimeError(f"Titre intro trouve {len(found)} fois : {title}")
    found[0].style = doc.styles["Heading 3"]
    print("OK heading:", title)

# ---------------------------------------------------------------------------
# 3. Tableaux
# ---------------------------------------------------------------------------
tables = doc.tables

# Table 5 : comparatif technologique
tables[5].rows[3].cells[2].text = "Enums nommés, JSONB, index B-tree et composites, performance, open source, ACID"
tables[5].rows[5].cells[2].text = "RBAC, JWT stateless, BCrypt, règles d'autorisation par URL"

# Table 6 : besoins fonctionnels (25)
besoins = [
    ("F1", "Authentification", "Authentification JWT avec contrôle d'accès par rôle"),
    ("F2", "Données référence", "Gestion des types d'engrais (CRUD) avec composition et seuils d'alerte"),
    ("F3", "Données référence", "Gestion des provinces/zones/collines (hiérarchie administrative)"),
    ("F4", "Données référence", "Gestion des dépôts (CRUD, liaison hiérarchique, capacité de stockage)"),
    ("F5", "Gestion agriculteurs", "CRUD des agriculteurs avec identifiant unique, superficie, colline"),
    ("F6", "Tickets", "Création et suivi des tickets de distribution avec workflow"),
    ("F7", "Stocks", "Réception FOMI (entrées de stock)"),
    ("F8", "Stocks", "Transferts inter-dépôts (province, zone, colline) avec vérification de disponibilité à la source"),
    ("F9", "Distribution", "Distribution aux agriculteurs selon l'algorithme FIFO"),
    ("F10", "Stocks", "Gestion des lots (dates de fabrication et de péremption)"),
    ("F11", "Stocks", "Suivi des stocks par dépôt, type d'engrais et lot"),
    ("F12", "Alertes", "Système d'alertes automatiques (rupture, stock bas, retard, péremption, inactivité)"),
    ("F13", "Mouvements", "Annulation de mouvements (transfert avec rétroaction stock, distribution avec mise à jour du ticket)"),
    ("F14", "Tickets", "Validation et rejet des tickets (workflow multi-états avec motifs)"),
    ("F15", "Reporting", "Tableaux de bord analytiques (taux de service, stocks régionaux)"),
    ("F16", "Reporting", "Export de données au format CSV (tickets et mouvements)"),
    ("F17", "Audit", "Piste d'audit avec détails JSON"),
    ("F18", "Alertes", "Configuration des seuils d'alerte par dépôt et type d'engrais"),
    ("F19", "Transparence", "Consultation publique des tickets (sans authentification)"),
    ("F20", "Recherche", "Recherche multicritère sur les agriculteurs et les lots avec pagination côté serveur"),
    ("F21", "Reporting", "Extraction des volumes non servis par colline"),
    ("F22", "Reporting", "Calcul du taux de service par province et par zone"),
    ("F23", "Reporting", "Journalisation des mouvements par agent"),
    ("F24", "Sécurité", "Gestion des comptes utilisateurs et des rôles (CRUD par admin)"),
    ("F25", "Intégrité", "Cohérence des stocks et des tickets (contraintes SQL, transactions, anti-double annulation)"),
]
rebuild_table(tables[6], besoins)

# Table 7 : regles metier (22)
regles = [
    ("R1", "Intégrité stock", "Le stock d'un dépôt ne peut pas devenir négatif (contrainte CHECK quantite_disponible >= 0)."),
    ("R2", "Quota distribution", "La quantité d'un ticket ne peut excéder la superficie × 150 kg/ha pour le type d'engrais demandé."),
    ("R3", "Seuil alerte", "Une alerte est levée lorsque le stock disponible est inférieur au seuil configuré pour un dépôt et un type d'engrais."),
    ("R4", "Péremption", "Les lots dont la date de péremption est dépassée sont exclus de la distribution FIFO ; le chemin avec lot imposé doit encore être corrigé."),
    ("R5", "Capacité dépôt", "La somme des stocks ne doit pas dépasser la capacité maximale du dépôt."),
    ("R6", "Unicité ticket", "Impossible de créer deux tickets pour la même saison, le même type d'engrais et le même agriculteur."),
    ("R7", "Annulation", "Un mouvement déjà annulé ne peut pas faire l'objet d'une seconde annulation."),
    ("R8", "Rétroaction", "L'annulation d'un transfert restaure le stock au dépôt source et le retire du dépôt destination ; l'annulation d'une distribution met à jour le ticket et crée un ajustement."),
    ("R9", "Transfert", "Tout transfert inter-dépôts valide d'abord la disponibilité réelle des lots dans le dépôt source."),
    ("R10", "Validation ticket", "Un ticket peut être validé ou rejeté avec un motif obligatoire."),
    ("R11", "FIFO", "L'allocation des engrais suit un algorithme FIFO basé sur la date de réception FOMI, après exclusion des lots périmés."),
    ("R12", "Capacité max", "La capacité maximale du dépôt est vérifiée lors d'une réception."),
    ("R13", "Audit", "Chaque opération critique génère un log d'audit via AuditLogService."),
    ("R14", "Rôle admin", "Seul le profil ADMIN dispose des droits CRUD pour gérer les comptes utilisateurs et configurer les seuils d'alerte."),
    ("R15", "Périmètre", "Un utilisateur AGENT_ZONE est limité aux données et mouvements des dépôts de sa zone."),
    ("R16", "Export", "L'extraction CSV des tickets est plafonnée à 100 000 lignes ; l'export des mouvements n'est pas plafonné."),
    ("R17", "Inactivité", "Une alerte est générée si un dépôt actif n'enregistre aucun mouvement durant 7 jours consécutifs."),
    ("R18", "Recherche", "Les endpoints de recherche multicritère doivent implémenter une pagination côté serveur."),
    ("R19", "JWT", "Un token expiré (24 h) est rejeté automatiquement avec le code 401."),
    ("R20", "Ticket expiré", "Un ticket non servi peut être marqué EXPIRE via TicketService.expirerTickets(), sans planification automatique."),
    ("R21", "Quota saison", "Le contrôle des droits aux engrais subventionnés est réinitialisé et cloisonné par saison agricole."),
    ("R22", "BCrypt", "Les mots de passe sont hashés avec BCrypt (cost 10)."),
]
rebuild_table(tables[7], regles)

# Table 8 : cas d'utilisation, corrections ciblees
t = tables[8]
t.rows[4].cells[4].text = "CRUD des dépôts (province, zone, colline)"
t.rows[6].cells[4].text = "Génération d'un ticket en état EN_ATTENTE_DE_VALIDATION"
t.rows[8].cells[4].text = "Mise à jour des stocks du dépôt récepteur"
t.rows[9].cells[2].text = "ADMIN"
t.rows[10].cells[2].text = "AGENT_ZONE / AGENT_COLLINE"
t.rows[12].cells[2].text = "UTILISATEUR AUTHENTIFIÉ"
t.rows[12].cells[4].text = "Annulation + ajustement"
t.rows[16].cells[2].text = "ADMIN / SUPERVISEUR / AGENT"

# Table 10 : modele de donnees (16 tables)
tables_data = [
    ("province", "Provinces du Burundi", "id, code, nom, created_at"),
    ("zone", "Zones administratives rattachées aux provinces", "id, code, nom, province_id, created_at"),
    ("colline", "Collines rattachées aux zones", "id, code, nom, zone_id, created_at"),
    ("depot", "Dépôts de stockage (province, zone, colline)", "id, code, nom, niveau, province_id, zone_id, colline_id, seuil_alerte_min, capacite_max, actif"),
    ("engrais_type", "Types d'engrais et prix subventionné", "id, code, nom, poids_sac_kg, prix_subventionne, actif"),
    ("lot", "Lots d'engrais avec dates de fabrication et de péremption", "id, numero_lot, engrais_type_id, quantite_initiale, date_fabrication, date_peremption, date_reception_fomi"),
    ("stock", "Stock agrégé par dépôt et type d'engrais", "id, depot_id, engrais_type_id, quantite_disponible, updated_at"),
    ("stock_lot", "Stock détaillé par dépôt et lot", "id, depot_id, lot_id, quantite, updated_at"),
    ("agriculteur", "Agriculteurs bénéficiaires", "id, numero_identite, nom, prenom, telephone, colline_id, est_cooperative, superficie_ha"),
    ("ticket", "Tickets de distribution", "id, numero_ticket, agriculteur_id, engrais_type_id, quantite_commandee, quantite_servie, montant_paye, date_paiement, depot_retrait_id, statut, saison"),
    ("utilisateur", "Utilisateurs et rôles", "id, username, password_hash, nom_complet, role, depot_id, zone_id, province_id, actif"),
    ("mouvement", "Historique des mouvements de stock", "id, type, lot_id, engrais_type_id, depot_source_id, depot_dest_id, quantite, agent_id, ticket_id, date_mouvement, annule"),
    ("distribution", "Détail des distributions effectuées", "id, ticket_id, lot_id, depot_id, quantite, agent_id, date_distribution, reference_mouvement_id"),
    ("alerte", "Alertes automatiques", "id, depot_id, engrais_type_id, type, message, niveau, traitee, created_at"),
    ("audit_log", "Piste d'audit", "id, utilisateur_id, action, entity_type, entity_id, ip_address, details_json, created_at"),
    ("seuil_alerte", "Seuils d'alerte par dépôt et type d'engrais", "id, depot_id, engrais_type_id, seuil_min, criticite"),
]
rebuild_table(tables[10], tables_data)

# Table 11 : enums
enums = [
    ("NiveauDepot", "PROVINCE, ZONE, COLLINE", "Classement des dépôts par niveau hiérarchique"),
    ("StatutTicket", "EN_ATTENTE_DE_VALIDATION, ACTIF, REJETE, EXPIRE, PAYE, EN_ATTENTE, PARTIEL, SERVI, RECLAMATION, ANNULE", "Workflow des tickets de distribution"),
    ("TypeMouvement", "RECEPTION_FOMI, TRANSFERT, DISTRIBUTION, AJUSTEMENT", "Classification des mouvements de stock"),
    ("TypeAlerte", "RUPTURE, STOCK_BAS, DELAI_DEPASSE, DEMANDE_SUP_STOCK, PEREMPTION, INACTIVITE", "Types d'alertes automatiques"),
    ("NiveauAlerte", "INFO, WARNING, CRITICAL", "Sévérité des alertes"),
    ("RoleUtilisateur", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE", "Rôles RBAC du système"),
]
rebuild_table(tables[11], enums)

# Table 12 : colonnes cles
colonnes = [
    ("utilisateur", "username / password_hash", "VARCHAR(50) / VARCHAR(255)", "username UNIQUE NOT NULL ; hash BCrypt"),
    ("utilisateur", "nom_complet", "VARCHAR(150)", "NOT NULL"),
    ("utilisateur", "role", "role_utilisateur (enum PG)", "NOT NULL"),
    ("utilisateur", "depot_id / zone_id / province_id", "BIGINT FK", "NULL (ancrage géographique)"),
    ("utilisateur", "actif", "BOOLEAN", "DEFAULT TRUE ; soft delete via supprime"),
    ("depot", "code", "VARCHAR(30)", "UNIQUE, NOT NULL"),
    ("depot", "niveau", "niveau_depot (enum PG)", "NOT NULL"),
    ("depot", "seuil_alerte_min", "INTEGER", "DEFAULT 100, NOT NULL"),
    ("depot", "capacite_max", "INTEGER", "NULL (V11)"),
    ("ticket", "numero_ticket", "VARCHAR(50)", "UNIQUE, NOT NULL"),
    ("ticket", "statut", "statut_ticket (enum PG)", "NOT NULL DEFAULT 'PAYE'"),
    ("ticket", "quantite_commandee / quantite_servie", "INTEGER", "NOT NULL / DEFAULT 0"),
    ("ticket", "agriculteur_id / depot_retrait_id", "BIGINT FK", "NOT NULL"),
    ("ticket", "montant_paye", "DECIMAL(12,2)", "NOT NULL"),
    ("ticket", "saison / superficie_ha", "VARCHAR(10) / DECIMAL(8,2)", "DEFAULT '2026A' / NULL"),
    ("lot", "numero_lot", "VARCHAR(50)", "UNIQUE, NOT NULL"),
    ("lot", "quantite_initiale", "INTEGER", "NOT NULL"),
    ("lot", "date_fabrication / date_peremption", "DATE", "NULL"),
    ("lot", "date_reception_fomi", "TIMESTAMP", "NOT NULL DEFAULT NOW() (base FIFO)"),
    ("mouvement", "type", "type_mouvement (enum PG)", "NOT NULL"),
    ("mouvement", "idempotency_key", "VARCHAR(64)", "UNIQUE (nullable)"),
    ("mouvement", "annule / motif_annulation / annule_par_id / reference_annulation_id", "BOOLEAN / VARCHAR(500) / BIGINT FK / BIGINT FK", "V11 (annulation)"),
    ("stock / stock_lot", "depot_id / engrais_type_id / lot_id", "BIGINT FK", "UNIQUE (depot_id, engrais_type_id) et (depot_id, lot_id)"),
    ("audit_log", "action / entity_type / entity_id", "VARCHAR / VARCHAR / BIGINT", "NOT NULL / NOT NULL / NULL"),
    ("audit_log", "details_json", "JSONB", "Sans index GIN"),
    ("alerte", "depot_id / type / engrais_type_id", "BIGINT FK", "engrais_type_id NOT NULL (à assouplir pour INACTIVITE)"),
    ("alerte", "niveau", "niveau_alerte (enum PG)", "NOT NULL DEFAULT 'WARNING'"),
]
rebuild_table(tables[12], colonnes)

# Table 13 : roles
t = tables[13]
t.rows[2].cells[1].text = "Validation/rejet tickets, alertes, statistiques, consultation des exports."
t.rows[3].cells[1].text = "Distribution, création tickets, consultation."
t.rows[4].cells[1].text = "Distribution et création tickets."
t.rows[5].cells[1].text = "Réception livraisons, gestion des lots."
t.rows[5].cells[2].text = "Dépôts de niveau province"

# Table 14 : packages
t = tables[14]
t.rows[3].cells[2].text = "16 interfaces"
t.rows[7].cells[2].text = "4 classes"
t.rows[8].cells[2].text = "1 classe"

# Table 15 : alertes
t = tables[15]
t.rows[3].cells[2].text = "Ticket non servi dont la date de paiement dépasse 7 jours"
t.rows[3].cells[3].text = "Cron 06h00 quotidien"
t.rows[4].cells[1].text = "WARNING"
t.rows[4].cells[2].text = "Demande non servie > stock disponible"
t.rows[4].cells[3].text = "À chaque mouvement de stock (verifierDepot)"
t.rows[5].cells[1].text = "CRITICAL"
t.rows[5].cells[2].text = "Lot déjà périmé avec stock > 0"
t.rows[5].cells[3].text = "À chaque mouvement de stock (verifierDepot)"
t.rows[6].cells[1].text = "WARNING"
t.rows[6].cells[2].text = "Aucun mouvement sur un dépôt actif pendant 7 jours"
t.rows[6].cells[3].text = "Cron 06h30 quotidien"
t.rows[1].cells[3].text = "À chaque mouvement de stock"
t.rows[2].cells[3].text = "À chaque mouvement de stock"

# Table 16 : champs audit
t = tables[16]
t.rows[1].cells[2].text = "Type d'opération : TICKET_CREATE, TICKET_ACTIVATE, DISTRIBUTION_CREATE, MOUVEMENT_CANCEL, etc."
t.rows[2].cells[2].text = "Type d'entité concernée : Ticket, Agriculteur, Lot, Mouvement, etc."
t.rows[5].cells[2].text = "Adresse IP de la requête (RemoteAddr)"
t.rows[7].cells[2].text = "Horodatage de l'opération"

# Table 17 : tests d'integration (20 classes, 204 tests)
tests = [
    ("ValidationTicketIntegrationTest", "27 tests", "Workflow complet : création, activation, rejet, unicité, quota"),
    ("SecuriteRbacIntegrationTest", "18 tests", "RBAC : rôles, périmètre, accès refusé, token invalide"),
    ("DistributionIntegrationTest", "17 tests", "Distribution, contrôle du restant, mise à jour du ticket"),
    ("AuthIntegrationTest", "17 tests", "Authentification, JWT, comptes désactivés"),
    ("AgriculteurIntegrationTest", "15 tests", "CRUD, recherche, téléphone unique"),
    ("TicketIntegrationTest", "14 tests", "CRUD tickets, filtres, pagination"),
    ("DepotIntegrationTest", "14 tests", "CRUD dépôts, contraintes de niveau, stocks"),
    ("MouvementIntegrationTest", "14 tests", "Réception, transfert, annulation, ajustement"),
    ("UtilisateurIntegrationTest", "11 tests", "CRUD utilisateurs, rôles, soft delete"),
    ("ApiIntegrationTest", "9 tests", "Endpoints transverses et gestion des erreurs"),
    ("AlerteIntegrationTest", "8 tests", "Déclenchement, dédoublement, traitement"),
    ("GeoIntegrationTest", "7 tests", "Provinces, zones, collines"),
    ("StockIntegrationTest", "6 tests", "Consultation, disponibilité, seuils"),
    ("LotIntegrationTest", "6 tests", "Création, recherche, péremption"),
    ("DistributionFifoIntegrationTest", "5 tests", "FIFO multi-lots, partiel, complet"),
    ("AuditLogIntegrationTest", "4 tests", "Enregistrement, consultation, filtres, pagination"),
    ("StatsIntegrationTest", "4 tests", "Taux de service, stocks par province, ruptures"),
    ("GlobalExceptionHandlerIntegrationTest", "4 tests", "Réponses d'erreur uniformes"),
    ("AlerteDelaiIntegrationTest", "3 tests", "Alertes de délai dépassé"),
    ("StockConcurrenceIntegrationTest", "1 test", "Pessimistic locking, accès concurrent"),
    ("Total", "204 tests", "20 classes de tests d'intégration PostgreSQL"),
]
rebuild_table(tables[17], tests)

# Table 18 : conformite (25 besoins)
conformite = [
    ("F1", "Authentification JWT", "Implémenté", "SecurityConfig, AuthController"),
    ("F2", "Types d'engrais CRUD", "Implémenté", "EngraisTypeController"),
    ("F3", "Géographie hiérarchique", "Implémenté", "GeoController"),
    ("F4", "Dépôts CRUD", "Implémenté", "DepotController, DepotService"),
    ("F5", "Agriculteurs CRUD", "Implémenté", "AgriculteurController"),
    ("F6", "Tickets distribution", "Implémenté", "TicketController, TicketService"),
    ("F7", "Réception FOMI", "Implémenté", "MouvementService.reception()"),
    ("F8", "Transferts inter-dépôts", "Implémenté", "MouvementService.transfert()"),
    ("F9", "Distribution FIFO", "Implémenté", "DistributionService.distribuer()"),
    ("F10", "Gestion des lots", "Implémenté", "LotController"),
    ("F11", "Suivi stocks", "Implémenté", "StockController, StockService"),
    ("F12", "Alertes automatiques", "Implémenté", "AlerteService, @Scheduled"),
    ("F13", "Annulation mouvements", "Implémenté", "MouvementService.annuler()"),
    ("F14", "Validation tickets", "Implémenté", "TicketService.activer(), rejeter()"),
    ("F15", "Statistiques", "Implémenté", "StatsController, StatsService"),
    ("F16", "Export CSV", "Implémenté", "ExportController"),
    ("F17", "Audit trail", "Implémenté", "AuditLogService, AuditLogController"),
    ("F18", "Seuils alerte", "Implémenté", "SeuilAlerteController"),
    ("F19", "Consultation publique", "Implémenté", "PublicTicketController"),
    ("F20", "Recherche multicritère", "Implémenté", "AgriculteurController.recherche(), LotController.recherche()"),
    ("F21", "Tickets non servis", "Implémenté", "StatsController (/tickets-non-servis-par-colline)"),
    ("F22", "Taux service", "Implémenté", "StatsController (/taux-service, /taux-service-par-province)"),
    ("F23", "Mouvements par agent", "Implémenté", "StatsController (/mouvements-par-agent/{agentId})"),
    ("F24", "Gestion utilisateurs", "Implémenté", "UtilisateurController, UtilisateurService"),
    ("F25", "Intégrité", "Implémenté", "Contraintes SQL, @Transactional, MouvementService.annuler()"),
]
rebuild_table(tables[18], conformite)

# Table 19 : annexe B, 60 endpoints
endpoints = [
    ("GET", "/api/agriculteurs", "Liste paginée des agriculteurs", "AUTH"),
    ("GET", "/api/agriculteurs/{id}", "Détail d'un agriculteur", "AUTH"),
    ("GET", "/api/agriculteurs/recherche", "Recherche d'agriculteurs par critères", "AUTH"),
    ("POST", "/api/agriculteurs", "Créer un agriculteur", "ADMIN, AGENT_ZONE, AGENT_COLLINE"),
    ("PUT", "/api/agriculteurs/{id}", "Modifier un agriculteur", "ADMIN, AGENT_ZONE, AGENT_COLLINE"),
    ("GET", "/api/alertes", "Liste des alertes", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE"),
    ("GET", "/api/alertes/depot/{depotId}", "Alertes d'un dépôt", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE"),
    ("PATCH", "/api/alertes/{id}/traiter", "Marquer une alerte comme traitée", "ADMIN"),
    ("GET", "/api/audit-logs", "Consulter la piste d'audit (pagination max 200)", "ADMIN"),
    ("POST", "/api/auth/login", "Authentification et génération du JWT", "PUBLIC"),
    ("GET", "/api/depots", "Liste des dépôts", "AUTH"),
    ("GET", "/api/depots/{id}", "Détail d'un dépôt", "AUTH"),
    ("POST", "/api/depots", "Créer un dépôt", "ADMIN"),
    ("PUT", "/api/depots/{id}", "Modifier un dépôt", "ADMIN"),
    ("GET", "/api/depots/{id}/stock", "Stocks d'un dépôt", "AUTH"),
    ("POST", "/api/distributions", "Distribuer des engrais (FIFO)", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE"),
    ("GET", "/api/distributions/ticket/{ticketId}", "Distributions d'un ticket", "AUTH"),
    ("GET", "/api/engrais-types", "Liste des types d'engrais", "AUTH"),
    ("GET", "/api/engrais-types/{id}", "Détail d'un type d'engrais", "AUTH"),
    ("POST", "/api/engrais-types", "Créer un type d'engrais", "ADMIN"),
    ("PUT", "/api/engrais-types/{id}", "Modifier un type d'engrais", "ADMIN"),
    ("DELETE", "/api/engrais-types/{id}", "Supprimer un type d'engrais", "ADMIN"),
    ("GET", "/api/export/tickets.csv", "Export CSV des tickets", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_LOGISTIQUE"),
    ("GET", "/api/export/mouvements.csv", "Export CSV des mouvements", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_LOGISTIQUE"),
    ("GET", "/api/provinces", "Liste des provinces", "AUTH"),
    ("GET", "/api/zones", "Liste des zones", "AUTH"),
    ("GET", "/api/provinces/{id}/zones", "Zones d'une province", "AUTH"),
    ("GET", "/api/collines", "Liste des collines", "AUTH"),
    ("GET", "/api/zones/{id}/collines", "Collines d'une zone", "AUTH"),
    ("GET", "/api/lots", "Liste des lots", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE"),
    ("GET", "/api/lots/recherche", "Recherche d'un lot par numéro", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE"),
    ("POST", "/api/lots", "Créer un lot", "ADMIN, AGENT_LOGISTIQUE"),
    ("POST", "/api/mouvements/reception", "Réception FOMI", "ADMIN, AGENT_LOGISTIQUE"),
    ("POST", "/api/mouvements/transfert", "Transfert inter-dépôts", "ADMIN"),
    ("POST", "/api/mouvements/{id}/annuler", "Annuler un mouvement", "AUTH (règle ADMIN/SUPERVISEUR non appliquée)"),
    ("GET", "/api/mouvements", "Liste paginée des mouvements", "AUTH"),
    ("GET", "/api/mouvements/lot/{lotId}", "Mouvements d'un lot", "AUTH"),
    ("GET", "/api/public/tickets/{numero}", "Suivi public d'un ticket", "PUBLIC"),
    ("GET", "/api/seuils-alerte", "Liste des seuils d'alerte", "AUTH"),
    ("POST", "/api/seuils-alerte", "Créer un seuil d'alerte", "ADMIN"),
    ("PUT", "/api/seuils-alerte/{id}", "Modifier un seuil d'alerte", "ADMIN"),
    ("DELETE", "/api/seuils-alerte/{id}", "Supprimer un seuil d'alerte", "ADMIN"),
    ("GET", "/api/statistiques/taux-service", "Taux de service", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/statistiques/stocks-par-province", "Stocks par province", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/statistiques/ruptures", "Ruptures en cours", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/statistiques/tickets-non-servis-par-colline", "Tickets non servis par colline", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/statistiques/taux-service-par-province", "Taux de service par province", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/statistiques/mouvements-par-agent/{agentId}", "Mouvements d'un agent", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/stocks", "Liste des stocks", "AUTH"),
    ("GET", "/api/stocks/disponibles", "Stocks disponibles pour un type d'engrais", "AUTH"),
    ("GET", "/api/tickets", "Liste paginée des tickets", "AUTH"),
    ("GET", "/api/tickets/{id}", "Détail d'un ticket", "AUTH"),
    ("POST", "/api/tickets", "Créer un ticket", "ADMIN, AGENT_ZONE, AGENT_COLLINE"),
    ("PUT", "/api/tickets/{id}", "Modifier un ticket", "ADMIN, AGENT_ZONE"),
    ("PATCH", "/api/tickets/{id}/activer", "Activer un ticket", "ADMIN, SUPERVISEUR"),
    ("PATCH", "/api/tickets/{id}/rejeter", "Rejeter un ticket", "ADMIN, SUPERVISEUR"),
    ("GET", "/api/utilisateurs", "Liste des utilisateurs", "ADMIN"),
    ("GET", "/api/utilisateurs/{id}", "Détail d'un utilisateur", "ADMIN"),
    ("POST", "/api/utilisateurs", "Créer un utilisateur", "ADMIN"),
    ("PUT", "/api/utilisateurs/{id}", "Modifier un utilisateur", "ADMIN"),
]
if len(endpoints) != 60:
    raise RuntimeError(f"Annexe B : {len(endpoints)} endpoints au lieu de 60")
rebuild_table(tables[19], endpoints)

# ---------------------------------------------------------------------------
# 4. Annexe A : extraits de code reels
# ---------------------------------------------------------------------------
p_a1 = [p for p in doc.paragraphs if p.text.strip().startswith("A.1 StockService.java")][0]
p_a2 = [p for p in doc.paragraphs if p.text.strip().startswith("A.2 DistributionService.java")][0]
p_b = [p for p in doc.paragraphs if p.text.strip().startswith("Annexe B : Liste des endpoints")][0]
code_template = deepcopy(p_a1._element.getnext())
title_template = deepcopy(p_a2._element)
delete_between(p_a1, p_b)

code_a1 = [
    "// Distribution FIFO par date de reception FOMI (tri croissant)",
    "@Transactional",
    "public List<LotSortie> sortirFifo(Depot depot, EngraisType engraisType,",
    "        int quantite, Long lotIdForce) {",
    "    List<StockLot> lots;",
    "    if (lotIdForce != null) {",
    "        StockLot forced = stockLotRepository",
    "                .findByDepotIdAndLotId(depot.getId(), lotIdForce)",
    "                .orElseThrow(() -> new BusinessException(\"Lot absent\"));",
    "        lots = List.of(forced);",
    "    } else {",
    "        lots = stockLotRepository",
    "                .findByDepotIdAndLotEngraisTypeIdAndQuantiteGreaterThanOrderByLotDateReceptionFomiAsc(",
    "                        depot.getId(), engraisType.getId(), 0);",
    "        lots = lots.stream()",
    "                .filter(sl -> sl.getLot().getDatePeremption() == null",
    "                        || !sl.getLot().getDatePeremption().isBefore(LocalDate.now()))",
    "                .collect(Collectors.toList());",
    "    }",
    "    int restant = quantite;",
    "    List<LotSortie> sorties = new ArrayList<>();",
    "    for (StockLot stockLot : lots) {",
    "        if (restant <= 0) break;",
    "        int pris = Math.min(stockLot.getQuantite(), restant);",
    "        stockLot.setQuantite(stockLot.getQuantite() - pris);",
    "        restant -= pris;",
    "        sorties.add(new LotSortie(stockLot.getLot(), pris));",
    "    }",
    "    if (restant > 0) {",
    "        throw new BusinessException(\"Stock insuffisant\");",
    "    }",
    "    Stock stock = getOrCreate(depot, engraisType);",
    "    stock.setQuantiteDisponible(stock.getQuantiteDisponible() - quantite);",
    "    stockRepository.save(stock);",
    "    return sorties;",
    "}",
]
anchor = p_a1
for line in code_a1:
    anchor = insert_after(anchor, code_template, line)

anchor = insert_after(anchor, title_template, "A.2 DistributionService.java — Méthode distribuer()")
code_a2 = [
    "@Service @RequiredArgsConstructor",
    "public class DistributionService {",
    "    private final TicketRepository ticketRepository;",
    "    private final DepotRepository depotRepository;",
    "    private final MouvementRepository mouvementRepository;",
    "    private final DistributionRepository distributionRepository;",
    "    private final StockService stockService;",
    "    private final AlerteService alerteService;",
    "    private final AuditLogService auditLogService;",
    "",
    "    @Transactional",
    "    public List<DistributionResponse> distribuer(DistributionRequest req, Utilisateur agent) {",
    "        Ticket ticket = ticketRepository.findByIdForUpdate(req.ticketId())",
    "                .orElseThrow(() -> new ResourceNotFoundException(\"Ticket introuvable\"));",
    "        Depot depot = depotRepository.findById(req.depotId())",
    "                .orElseThrow(() -> new ResourceNotFoundException(\"Dépôt introuvable\"));",
    "        verifierPerimetreAgent(agent, depot);",
    "        if (!List.of(StatutTicket.ACTIF, StatutTicket.PAYE,",
    "                StatutTicket.EN_ATTENTE, StatutTicket.PARTIEL)",
    "                .contains(ticket.getStatut())) {",
    "            throw new BusinessException(\"Distribution impossible\");",
    "        }",
    "        int restant = ticket.getQuantiteCommandee() - ticket.getQuantiteServie();",
    "        if (restant < req.quantite()) {",
    "            throw new BusinessException(\"Quantité supérieure au restant du ticket\");",
    "        }",
    "        List<LotSortie> sorties = stockService.sortirFifo(",
    "                depot, ticket.getEngraisType(), req.quantite(), req.lotId());",
    "        List<DistributionResponse> reponses = new ArrayList<>();",
    "        for (LotSortie sortie : sorties) {",
    "            Mouvement mouvement = Mouvement.builder()",
    "                    .type(TypeMouvement.DISTRIBUTION)",
    "                    .lot(sortie.lot())",
    "                    .engraisType(ticket.getEngraisType())",
    "                    .depotSource(depot)",
    "                    .quantite(sortie.quantite())",
    "                    .agent(agent)",
    "                    .ticket(ticket)",
    "                    .dateMouvement(LocalDateTime.now())",
    "                    .build();",
    "            mouvementRepository.save(mouvement);",
    "            // Distribution enregistree avec referenceMouvement",
    "        }",
    "        ticket.setQuantiteServie(ticket.getQuantiteServie() + req.quantite());",
    "        ticket.mettreAJourStatut();",
    "        ticketRepository.save(ticket);",
    "        alerteService.verifierDepot(depot, ticket.getEngraisType());",
    "        auditLogService.log(\"DISTRIBUTION_CREATE\", \"Ticket\", ticket.getId(), \"...\");",
    "        return reponses;",
    "    }",
    "}",
]
for line in code_a2:
    anchor = insert_after(anchor, code_template, line)
print("OK Annexe A")

# ---------------------------------------------------------------------------
# 5. Annexe C : schema SQL reel
# ---------------------------------------------------------------------------
p_c = [p for p in doc.paragraphs if p.text.strip().startswith("V1__init_schema.sql")][0]
p_d = [p for p in doc.paragraphs if p.text.strip().startswith("Annexe D : Résultats des tests")][0]
sql_template = deepcopy(p_c._element)
delete_between(p_c, p_d)
set_para_text(p_c, "Extrait consolidé des migrations V1, V7 et V11 :")

sql_lines = [
    "CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE', 'COLLINE');",
    "CREATE TYPE statut_ticket AS ENUM ('PAYE', 'EN_ATTENTE', 'PARTIEL',",
    "    'SERVI', 'RECLAMATION', 'ANNULE');",
    "ALTER TYPE statut_ticket ADD VALUE 'EN_ATTENTE_DE_VALIDATION' AFTER 'EN_ATTENTE';",
    "ALTER TYPE statut_ticket ADD VALUE 'ACTIF' AFTER 'EN_ATTENTE_DE_VALIDATION';",
    "ALTER TYPE statut_ticket ADD VALUE 'REJETE';",
    "ALTER TYPE statut_ticket ADD VALUE 'EXPIRE';",
    "CREATE TYPE role_utilisateur AS ENUM ('ADMIN', 'AGENT_ZONE',",
    "    'AGENT_COLLINE', 'SUPERVISEUR');",
    "ALTER TYPE role_utilisateur ADD VALUE 'AGENT_LOGISTIQUE';",
    "CREATE TYPE type_mouvement AS ENUM ('RECEPTION_FOMI', 'TRANSFERT',",
    "    'DISTRIBUTION', 'AJUSTEMENT');",
    "CREATE TYPE type_alerte AS ENUM ('STOCK_BAS', 'RUPTURE',",
    "    'DELAI_DEPASSE', 'DEMANDE_SUP_STOCK');",
    "ALTER TYPE type_alerte ADD VALUE 'PEREMPTION';",
    "ALTER TYPE type_alerte ADD VALUE 'INACTIVITE';",
    "CREATE TYPE niveau_alerte AS ENUM ('INFO', 'WARNING', 'CRITICAL');",
    "",
    "CREATE TABLE depot (",
    "    id               BIGSERIAL PRIMARY KEY,",
    "    code             VARCHAR(30)   NOT NULL UNIQUE,",
    "    nom              VARCHAR(150)  NOT NULL,",
    "    niveau           niveau_depot  NOT NULL,",
    "    province_id      BIGINT REFERENCES province(id),",
    "    zone_id          BIGINT REFERENCES zone(id),",
    "    colline_id       BIGINT REFERENCES colline(id),",
    "    seuil_alerte_min INTEGER NOT NULL DEFAULT 100,",
    "    capacite_max     INTEGER,",
    "    actif            BOOLEAN NOT NULL DEFAULT TRUE,",
    "    created_at       TIMESTAMP NOT NULL DEFAULT NOW()",
    ");",
    "",
    "CREATE TABLE stock (",
    "    id                  BIGSERIAL PRIMARY KEY,",
    "    depot_id            BIGINT NOT NULL REFERENCES depot(id),",
    "    engrais_type_id     BIGINT NOT NULL REFERENCES engrais_type(id),",
    "    quantite_disponible INTEGER NOT NULL DEFAULT 0 CHECK (quantite_disponible >= 0),",
    "    updated_at          TIMESTAMP NOT NULL DEFAULT NOW(),",
    "    UNIQUE (depot_id, engrais_type_id)",
    ");",
    "",
    "CREATE TABLE ticket (",
    "    id                 BIGSERIAL PRIMARY KEY,",
    "    numero_ticket      VARCHAR(50) NOT NULL UNIQUE,",
    "    agriculteur_id     BIGINT NOT NULL REFERENCES agriculteur(id),",
    "    engrais_type_id    BIGINT NOT NULL REFERENCES engrais_type(id),",
    "    quantite_commandee INTEGER NOT NULL CHECK (quantite_commandee > 0),",
    "    quantite_servie    INTEGER NOT NULL DEFAULT 0 CHECK (quantite_servie >= 0),",
    "    montant_paye       DECIMAL(12,2) NOT NULL,",
    "    date_paiement      DATE NOT NULL,",
    "    depot_retrait_id   BIGINT NOT NULL REFERENCES depot(id),",
    "    statut             statut_ticket NOT NULL DEFAULT 'PAYE',",
    "    saison             VARCHAR(10) NOT NULL DEFAULT '2026A',",
    "    superficie_ha      DECIMAL(8,2),",
    "    date_creation      TIMESTAMP NOT NULL DEFAULT NOW()",
    ");",
    "",
    "CREATE INDEX idx_ticket_statut ON ticket(statut);",
    "CREATE INDEX idx_ticket_depot_retrait ON ticket(depot_retrait_id, statut);",
    "",
    "CREATE TABLE mouvement (",
    "    id               BIGSERIAL PRIMARY KEY,",
    "    type             type_mouvement NOT NULL,",
    "    lot_id           BIGINT NOT NULL REFERENCES lot(id),",
    "    engrais_type_id  BIGINT NOT NULL REFERENCES engrais_type(id),",
    "    depot_source_id  BIGINT REFERENCES depot(id),",
    "    depot_dest_id    BIGINT REFERENCES depot(id),",
    "    quantite         INTEGER NOT NULL CHECK (quantite > 0),",
    "    agent_id         BIGINT NOT NULL REFERENCES utilisateur(id),",
    "    ticket_id        BIGINT REFERENCES ticket(id),",
    "    date_mouvement   TIMESTAMP NOT NULL DEFAULT NOW(),",
    "    idempotency_key  VARCHAR(64) UNIQUE,",
    "    annule           BOOLEAN NOT NULL DEFAULT FALSE,",
    "    motif_annulation VARCHAR(500),",
    "    annule_par_id    BIGINT REFERENCES utilisateur(id),",
    "    reference_annulation_id BIGINT REFERENCES mouvement(id)",
    ");",
]
anchor = p_c
for line in sql_lines:
    anchor = insert_after(anchor, sql_template, line)
print("OK Annexe C")

# ---------------------------------------------------------------------------
# 6. Annexe D : resultats des tests
# ---------------------------------------------------------------------------
replace_para(
    "Résultats globaux : 203 tests",
    "Résultats globaux : 207 tests exécutés, 207 réussis, 0 échoué, 0 ignoré.",
)
replace_para(
    "Temps d'exécution total : 2 min 47 s",
    "Temps d'exécution total : environ 3 minutes (dont démarrage de l'instance PostgreSQL Testcontainers).",
)
replace_para(
    "Couverture de code estimée : 85 %",
    "Couverture de code : non mesurée par un outil dédié.",
)

p_label = [p for p in doc.paragraphs if p.text.strip().startswith("Détail par catégorie")][0]
bullets = []
el = p_label._element.getnext()
while el is not None:
    if el.tag.endswith("}p"):
        p = Paragraph(el, p_label._parent)
        if p.style.name == "List Bullet":
            bullets.append(p)
    el = el.getnext()
if not bullets:
    raise RuntimeError("Aucune puce trouvee apres Detail par categorie")
bullet_template = deepcopy(bullets[0]._element)
for p in bullets:
    p._element.getparent().remove(p._element)
anchor = p_label
for line in [
    "Tests d'intégration (PostgreSQL via Testcontainers) : 204 tests, 204 réussis",
    "Tests unitaires (DatabaseUrlConfigTest) : 3 tests, 3 réussis",
    "Total : 207 tests, 207 réussis",
]:
    anchor = insert_after(anchor, bullet_template, line)
print("OK Annexe D")

# ---------------------------------------------------------------------------
doc.save(DOC)
print("DOCUMENT ENREGISTRE :", DOC)
