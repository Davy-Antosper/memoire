# Guide des diagrammes — Système FOMI-Stock

Ce document explique **chaque diagramme** du mémoire : ce qu'il montre, comment le lire,
ce qu'il faut dire à l'oral pour l'expliquer, et les points de vigilance.

Toutes les informations proviennent du **code réel** de `fomi-stock-api` (entités, services,
`SecurityConfig`, migrations SQL), pas du cahier des charges initial.

**Fichiers sources** : `memoire_assets/*.svg` (8 diagrammes, générés avec PlantUML, thème `materia-outline`).

---

## Table des matières

| # | Diagramme | Fichier | Type UML |
|---|---|---|---|
| 1 | [Diagramme de classes](#1-diagramme-de-classes) | `class_diagram.svg` | Structure |
| 2 | [Entité-Relation (modèle physique)](#2-diagramme-entité-relation) | `er_diagram.svg` | Données |
| 3 | [Circuit de distribution des engrais](#3-circuit-de-distribution-des-engrais) | `distribution_circuit.svg` | Flux métier |
| 4 | [Séquence — Création et validation d'un ticket](#4-séquence--création-et-validation-dun-ticket) | `sequence_ticket.svg` | Comportement |
| 5 | [Architecture du système](#5-architecture-du-système) | `architecture.svg` | Structure |
| 6 | [Cas d'utilisation](#6-diagramme-de-cas-dutilisation) | `use_case_diagram.svg` | Besoins |
| 7 | [Diagramme d'activités](#7-diagramme-dactivités) | `activity_diagram.svg` | Comportement |
| 8 | [Diagramme de déploiement](#8-diagramme-de-déploiement) | `deployment_diagram.svg` | Infrastructure |
| — | [Matrice RBAC exacte](#annexe-a--matrice-rbac-réelle) | — | Sécurité |
| — | [Incohérences connues](#annexe-b--incohérences-et-points-de-vigilance) | — | — |

---

## 1. Diagramme de classes

**Fichier** : `class_diagram.svg` — **Type** : diagramme de structure (UML).

### Objectif

Montrer les **17 entités métier** du système et leurs relations, avec leurs attributs
principaux et leurs méthodes métier.

### Comment le lire

- Chaque **boîte** = une entité JPA (`@Entity`), donc une table en base.
- Les **compartiments** vont du général au particulier : nom de la classe, puis attributs.
- Les **flèches** portent une **multiplicité** aux deux extrémités (`1`, `0..*`, `0..1`).
- Les **couleurs** regroupent les entités par domaine : localisation (vert), acteurs (jaune),
  stock (bleu), distribution (rose).

### Contenu (extrait du code réel)

| Domaine | Entités |
|---|---|
| Localisation | `Province`, `Commune`, `Zone`, `Colline` |
| Acteurs | `Agriculteur`, `Utilisateur` |
| Stock | `EngraisType`, `Lot`, `Depot`, `Stock`, `StockLot` |
| Distribution | `Ticket`, `Mouvement`, `Distribution` |
| Pilotage | `Alerte`, `SeuilAlerte`, `AuditLog` |

**Relations clés** :

- `Province 1 — 0..* Commune`, `Commune 1 — 0..* Zone`, `Zone 1 — 0..* Colline` : découpage
  administratif du Burundi (`Province → Commune → Zone → Colline`).
- `Colline 1 — 0..* Agriculteur` : chaque agriculteur est rattaché à une colline (lieu de
  résidence).
- `Province 0..1 — 0..* Depot` et `Zone 0..1 — 0..* Depot` : un dépôt est soit provincial,
  soit de zone — la colline n'est jamais un niveau de stockage.
- `Agriculteur 1 — 0..* Ticket` : un agriculteur demande des tickets.
- `Ticket 1 — 0..* Distribution` : un ticket peut être servi en plusieurs fois (distributions partielles).
- `Lot 1 — 0..* Distribution` : chaque distribution sort d'un lot précis (traçabilité).
- `Mouvement 1 — 0..1 Distribution` : une distribution référence **exactement un** mouvement.
- `Utilisateur 0..1 — 0..* Depot/Zone/Province` : périmètre d'action d'un agent.

### À dire à l'oral

> « Ce diagramme présente le modèle objet du système. Trois remarques importantes.
> D'abord, `Distribution` est une entité à part de `Ticket` : c'est ce qui permet les
> **distributions partielles** et le suivi FIFO lot par lot. Ensuite, `StockLot` est la
> table qui rend le FIFO possible : elle stocke la quantité **par lot et par dépôt**, ce qui
> permet de savoir quel lot sortir en premier. Enfin, `Mouvement` porte une clé
> `idempotencyKey` unique, qui est notre garde-fou contre les doubles enregistrements. »

### Points de vigilance

- `Utilisateur` implémente `UserDetails` de Spring Security, mais le diagramme ne montre que
  les champs métier — c'est volontaire pour la lisibilité.
- `ANNULE` et `RECLAMATION` : `Mouvement.annule` est un **booléen**, pas un statut. Ne pas confondre.

---

## 2. Diagramme Entité-Relation

**Fichier** : `er_diagram.svg` — **Type** : modèle physique de données (notation patte d'oie).

### Objectif

Montrer la **structure exacte de la base PostgreSQL** : les 17 tables, leurs colonnes avec
types SQL, clés primaires (`PK`), clés étrangères (`FK`) et contraintes d'unicité.

### Comment le lire

C'est la différence essentielle avec le diagramme de classes :

| Diagramme de classes | Diagramme ER |
|---|---|
| Niveau **objet** (Java) | Niveau **table** (PostgreSQL) |
| Montre les types Java (`Long`, `String`) | Montre les types SQL (`BIGSERIAL`, `VARCHAR(50)`) |
| Montre les méthodes | Montre les contraintes (`UNIQUE`, `CHECK`) |

**Notation patte d'oie** :

```
||--o{   =  un vers plusieurs (0 ou plus)
||--||   =  un vers un exactement un
```

### Contenu (extrait du code réel)

**17 tables** : `province`, `commune`, `zone`, `colline`, `depot`, `engrais_type`, `lot`, `stock`,
`stock_lot`, `agriculteur`, `ticket`, `utilisateur`, `mouvement`, `distribution`, `alerte`,
`seuil_alerte`, `audit_log`.

**Modèle géographique et dépôts** :

- `commune.province_id` et `zone.commune_id` portent la hiérarchie administrative.
- `depot.niveau` ne prend que deux valeurs (`PROVINCE`, `ZONE`) ; `depot` référence
  `province_id` et/ou `zone_id`, et **plus aucune colonne `colline_id`**.
- `agriculteur.colline_id` reste présent : la colline est le lieu de résidence des
  agriculteurs, pas un niveau de stockage.

**Contraintes remarquables** :

- `UNIQUE (depot_id, engrais_type_id)` sur `stock` : une seule ligne de stock par couple dépôt/engrais.
- `UNIQUE (depot_id, lot_id)` sur `stock_lot` : un seul enregistrement par lot et par dépôt.
- `UNIQUE` sur `distribution.reference_mouvement_id` : c'est ce qui force la relation **1:1**.
- `CHECK (quantite_servie <= quantite_commandee)` sur `ticket` : la base elle-même interdit de servir plus que demandé.
- `CHECK (quantite_disponible >= 0)` sur `stock` : stock négatif impossible.
- `details_json` en **JSONB** dans `audit_log` (et non `TEXT`).
- **6 énumérations PostgreSQL natives** : `niveau_depot`, `statut_ticket`, `role_utilisateur`,
  `type_mouvement`, `type_alerte`, `niveau_alerte`.

### À dire à l'oral

> « Ce diagramme montre le modèle physique, c'est-à-dire le schéma tel qu'il existe dans
> PostgreSQL. L'important est la **défense en profondeur** : les règles métier sont protégées
> à trois niveaux — le contrôleur valide les entrées, le service applique la logique, et la
> base ajoute les contraintes `CHECK` et `UNIQUE`. Même un bug applicatif ne peut donc pas
> créer un stock négatif ou une quantité servie supérieure à la quantité commandée. »

### Points de vigilance

- Ce diagramme reflète l'état **après toutes les migrations** (`V1` à `V13`), c'est-à-dire
  l'état réel de production. Le fichier `V1__schema.sql` seul est incomplet
  (pas d'`email` sur `agriculteur`, pas de `seuil_alerte`, enums plus courts).
- Les enums ont évolué : `V1` déclarait 4 rôles, le code en compte **5** ; `V1` déclarait
  6 statuts de ticket, le code en compte **10**. C'est `V7__enums_validation_role.sql` qui a complété.

---

## 3. Circuit de distribution des engrais

**Fichier** : `distribution_circuit.svg` — **Type** : diagramme de flux (vue métier).

### Objectif

Montrer le chemin physique des engrais, de l'usine de Maramvya jusqu'à l'agriculteur, en
distinguant clairement les **deux niveaux de dépôts** du modèle FOMI et la distribution finale.

### Comment le lire

- Les **rectangles** représentent les étapes logistiques, de haut en bas.
- Le **site de production** (usine) n'est pas un dépôt de distribution : c'est le point de
  départ des livraisons.
- Le **niveau 1** est le dépôt provincial (BPEAE), le **niveau 2** le dépôt de zone.
- La **colline** n'héberge aucun dépôt permanent : elle accueille un point de service
  temporaire le jour de la distribution.
- La note rappelle la hiérarchie administrative : `Province → Commune → Zone → Colline`.

### Règles structurantes

| Élément | Rôle | Stockage |
|---|---|---|
| Usine FOMI (Maramvya) | Production et stockage central | Oui (site de production) |
| Dépôt provincial (BPEAE) | Répartition vers les communes et leurs zones | Oui — niveau `PROVINCE` |
| Dépôt de zone | Dernier point de stockage fixe de la FOMI | Oui — niveau `ZONE` |
| Colline | Point de service temporaire, lieu de résidence | Non |
| Agriculteur | Bénéficiaire final | Non |

### À dire à l'oral

> « Le circuit comporte deux niveaux de dépôts, pas trois. L'usine produit et stocke, mais elle
> n'est pas un dépôt de distribution. Le dépôt provincial alimente les communes, puis les zones ;
> le dépôt de zone est le dernier stockage fixe. Ensuite, la distribution se fait dans les
> collines, sans magasin permanent : c'est un point de service organisé le jour du retrait. »

### Points de vigilance

- La colline reste un niveau **administratif** (rattachement des agriculteurs et des tickets),
  pas un niveau de **stockage** : le modèle ne connaît que `PROVINCE` et `ZONE`.
- Le détail technique de la sortie FIFO (verrou pessimiste, lots périmés) est décrit dans la
  partie conception du rapport, pas dans ce schéma de flux.

---

## 4. Séquence — Création et validation d'un ticket

**Fichier** : `sequence_ticket.svg` — **Type** : diagramme de séquence (UML).
**Source** : `TicketService.creer()`, `activer()` et `rejeter()`.

### Objectif

Montrer le parcours d'un ticket, de sa création jusqu'à sa validation, en insistant sur les
**règles métier** appliquées.

### Comment le lire

Deux parties séparées par un trait : **Création** (agent colline → système) et
**Validation** (agent zone → système). Les règles métier sont regroupées dans une **note**,
plutôt que dispersées en cadres imbriqués — choix de lisibilité.

### Les règles métier appliquées (réelles)

| Règle | Contenu | Où dans le code |
|---|---|---|
| **R22 — plafond** | `quantité ≤ superficie × 150 kg/ha` | `TicketService.creer()` |
| **R22 — cumul** | Somme des tickets actifs de la saison + nouvelle quantité ≤ plafond | idem |
| **R6 — unicité** | Un seul ticket par agriculteur + saison + type d'engrais | idem |
| **Unicité numéro** | `numeroTicket` non déjà utilisé | idem |

**Statut initial** : `EN_ATTENTE_DE_VALIDATION` — et c'est important : ce n'est **pas** `PAYE`,
même si l'entité déclare `PAYE` par défaut. Le service force la valeur.

### À dire à l'oral

> « Ce diagramme montre l'application des règles métier. La règle R22 est la plus
> intéressante : le plafond d'engrais n'est pas un chiffre fixe, il est **calculé** à partir
> de la superficie déclarée de l'agriculteur, à raison de 150 kg par hectare. Et ce n'est pas
> contrôlé ticket par ticket, mais en **cumul** sur toute la saison : c'est ce qui empêche un
> agriculteur de contourner le quota en créant plusieurs tickets. La règle R6 interdit en plus
> deux tickets pour la même saison et le même engrais. »

### Points de vigilance

- **Le diagramme indique « agent zone valide »** — or `SecurityConfig` réserve en réalité
  `PATCH .../activer` et `.../rejeter` aux rôles **`ADMIN` et `SUPERVISEUR`**. Voir
  [Annexe B](#annexe-b--incohérences-et-points-de-vigilance).
- Après validation, un email part automatiquement (`TICKET_VALIDE`).

---

## 5. Architecture du système

**Fichier** : `architecture.svg` — **Type** : diagramme de composants (architecture 3 tiers).

### Objectif

Montrer l'organisation d'ensemble : les clients, l'API REST, la base de données et le service
de notification.

### Comment le lire

- **Clients** : application web React/Vite (PWA) et application mobile Expo/React Native.
- **API REST** : Spring Boot 3.3.5 / Java 21, organisée en quatre domaines — référentiels,
  stocks et lots, tickets et distribution, alertes/statistiques/audit.
- **Données** : PostgreSQL 16, **17 tables**, schéma versionné par **13 migrations** Flyway.
- **Service externe** : notification email (SMTP), appelée de façon non bloquante.

### À dire à l'oral

> « L'architecture est en trois tiers : les clients web et mobile consomment une API REST
> unique, qui centralise les règles métier et parle à PostgreSQL. Les référentiels
> géographiques suivent la hiérarchie réelle du Burundi — province, commune, zone, colline —
> et seuls les dépôts provinciaux et de zone stockent des engrais. »

### Points de vigilance

- L'application mobile est **prévue** dans l'architecture, mais le dépôt livré contient
  principalement l'application web ; le diagramme de déploiement le signale.
- Les notifications email sont volontairement **non bloquantes** : une panne SMTP ne fait pas
  échouer une distribution.

---

## 6. Diagramme de cas d'utilisation

**Fichier** : `use_case_diagram.svg` — **Type** : diagramme de cas d'utilisation (UML).

### Objectif

Montrer **qui** (acteurs) peut faire **quoi** (cas d'utilisation) dans le système. C'est le
diagramme des besoins fonctionnels, vu de l'extérieur.

### Comment le lire

- Les **bonhommes-bâtons** = acteurs (rôles ou utilisateurs externes).
- Les **ellipses** = cas d'utilisation (une action métier complète, pas une méthode technique).
- Le **cadre rectangulaire** = frontière du système.
- Les flèches en **pointillés `«include»`** = un cas en inclut toujours un autre.

### Les 5 rôles réels du système

| Rôle | Description |
|---|---|
| `ADMIN` | Administrateur : gère utilisateurs, engrais, dépôts, seuils |
| `SUPERVISEUR` | Supervise : statistiques, audit, clôture de saison, distribution |
| `AGENT_ZONE` | Agent de zone : crée et modifie les tickets, distribue |
| `AGENT_COLLINE` | Agent de colline : crée les tickets, distribue sur son dépôt |
| `AGENT_LOGISTIQUE` | Gère la réception des lots |

**Plus un acteur externe** : l'**Agriculteur**, qui n'a **pas de compte**. Il consulte son
ticket via `GET /api/public/tickets/{numero}`, sans authentification.

### À dire à l'oral

> « Deux points différencient ce diagramme d'un diagramme classique.
> **Premièrement**, l'agriculteur n'est pas un utilisateur authentifié : il n'a ni compte ni
> mot de passe. Il consulte son ticket par son numéro, via un point d'entrée public — c'est
> une contrainte forte du cahier des charges, car beaucoup d'agriculteurs n'ont pas de
> smartphone. **Deuxièmement**, le système compte 5 rôles, dont un rôle purement logistique
> qui gère la réception des lots chez FOMI. »

### Points de vigilance

- **Attention** : ce diagramme représente l'**intention fonctionnelle**, et les associations
  acteur ↔ cas sont **simplifiées**. La vérité exacte est dans `SecurityConfig` —
  voir [Annexe A](#annexe-a--matrice-rbac-réelle). En cas de contradiction, **c'est l'annexe A qui fait foi**.
- L'authentification est un cas transversal : elle est incluse par les autres fonctionnalités
  plutôt que reliée à chaque acteur par une flèche (choix de lisibilité).

---

## 7. Diagramme d'activités

**Fichier** : `activity_diagram.svg` — **Type** : diagramme d'activités (UML), en couloirs.
**Source** : `TicketService`, `DistributionService`, `AlerteService`.

### Objectif

Montrer le **cycle de vie complet** d'un ticket, du premier contact de l'agriculteur jusqu'à
la clôture de la saison, en indiquant **qui** fait chaque étape.

### Comment le lire

- Les **colonnes** = les couloirs (*swimlanes*) : Agriculteur, Agent colline, Système, Agent zone.
- On suit le flux de **haut en bas** ; changer de couloir = changer d'acteur.
- Les **losanges** = décisions (embranchements).
- Le **rond plein** = début ; le **rond cerclé** = fin.

### Étapes du flux

1. **Agriculteur** : se rend au point de distribution de sa colline et demande un ticket.
2. **Agent colline** : enregistre et crée la demande.
3. **Système** : vérifie les règles R22 (plafond et cumul) et R6 (unicité).
4. **Décision** : si non conforme → refus. Si conforme → enregistrement en `EN_ATTENTE_DE_VALIDATION`.
5. **Agent zone** : examine la demande.
6. **Décision** : validée → `ACTIF` ; refusée → `REJETE`.
7. **Distribution** : sortie FIFO des lots, mise à jour du stock, enregistrement du mouvement.
8. **Décision** : tout servi → `SERVI` ; sinon → `PARTIEL` (et attente d'un nouveau retrait).
9. **Clôture de saison** : les tickets non entièrement servis passent à `EXPIRE`.

### À dire à l'oral

> « L'intérêt des couloirs est de montrer **la séparation des responsabilités**. L'agriculteur
> ne fait que demander ; l'agent de colline enregistre ; l'agent de zone valide ; le système
> exécute les règles et le FIFO. On voit aussi que le parcours n'est pas linéaire : un ticket
> peut rester `PARTIEL` plusieurs semaines, jusqu'à ce que l'agriculteur revienne chercher le
> reste — et s'il ne revient pas avant la clôture, le ticket expire. »

### Points de vigilance

- Ce diagramme **mélange deux niveaux** : le parcours métier (visible par les acteurs) et des
  détails techniques (`mouvement`, FIFO). C'est un choix assumé pour la complétude ; une
  variante plus courte est possible si l'encadrant préfère.

---

## 8. Diagramme de déploiement

**Fichier** : `deployment_diagram.svg` — **Type** : diagramme de déploiement (UML).
**Source** : `Dockerfile`, `application-dev.yml`, `application-prod.yml`, `ci.yml`.

### Objectif

Montrer **où tourne quoi** : les machines, conteneurs et services, et comment ils communiquent.

### Comment le lire

- Les **nœuds 3D** = machines physiques ou virtuelles (poste client, serveur, CI).
- Les **cylindres** = bases de données.
- Le **nuage** = service externe.
- Les **flèches** = protocoles de communication (HTTPS, JDBC, SMTP).

### Contenu (réel)

| Composant | Détail | Source |
|---|---|---|
| Frontend | React + Vite, port 5173 en dev | `fomi-stock-web` |
| Mobile | Expo / React Native (prévu) | `fomi-stock-mobile` |
| API | Spring Boot 3.3.5, Java 21, port 8080 | `application.yml` |
| Conteneur | `maven:3.9-eclipse-temurin-21` (build) → `eclipse-temurin:21-jre` (run) | `Dockerfile` |
| Base | PostgreSQL 16, `fomi_stock` | `application-dev.yml` |
| Migrations | Flyway, `classpath:db/migration` | `application-prod.yml` |
| SMTP | Mailpit en local, port 1025 | `application.yml` |
| CI | GitHub Actions, `ubuntu-24.04`, JDK 21, `mvn -B verify` | `ci.yml` |

**En production**, la base est configurée par variables d'environnement
(`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`), et le port par `PORT`. Le fuseau horaire est forcé à
`Africa/Bujumbura` — important pour un système burundais.

### À dire à l'oral

> « Le déploiement est **conteneurisé** : le `Dockerfile` est multi-étapes, ce qui est une
> bonne pratique — l'image finale ne contient que le JRE et le `.jar`, pas Maven ni le code
> source, donc elle est plus légère et plus sûre. En production, aucun identifiant n'est écrit
> dans le code : la base est configurée par variables d'environnement. Enfin, Flyway applique
> les migrations **automatiquement au démarrage**, et Hibernate est en mode `validate`
> seulement — c'est Flyway qui fait foi sur le schéma, pas Hibernate. »

### Points de vigilance

- **Aucune configuration de déploiement cloud** n'a été trouvée dans le dépôt (pas de
  `railway.json`, `fly.toml`, etc.). Le diagramme reste donc générique côté hébergeur.
- Le fuseau `Africa/Bujumbura` (UTC+2) est défini **trois fois** : `Dockerfile`, Hibernate
  (`application-prod.yml`), et l'OS. C'est volontaire, mais à connaître.

---

## Annexe A — Matrice RBAC réelle

⚠️ **C'est la source de vérité** : extraite de `SecurityConfig.java`, ligne par ligne. En cas de
contradiction avec le diagramme de cas d'utilisation, **cette table gagne**.

### Points d'entrée publics (sans authentification)

| Endpoint | Détail |
|---|---|
| `POST /api/auth/login` | Connexion |
| `GET /actuator/health` | Sonde de santé |
| `/api-docs/**`, `/swagger-ui/**` | Documentation Swagger |
| `/api/public/**` | Consultation d'un ticket par numéro |

### Endpoints protégés

| Endpoint | Rôles autorisés |
|---|---|
| `GET /api/statistiques/**` | `ADMIN`, `SUPERVISEUR` |
| `GET /api/alertes/**` | `ADMIN`, `SUPERVISEUR`, `AGENT_ZONE`, `AGENT_COLLINE` |
| Autres `/api/alertes/**` (traiter) | `ADMIN` |
| `/api/utilisateurs/**` | `ADMIN` |
| `GET /api/audit-logs/**` | `ADMIN` |
| `POST /api/mouvements/reception` | `ADMIN`, `AGENT_LOGISTIQUE` |
| `POST /api/mouvements/transfert` | `ADMIN` |
| Autres `/api/mouvements/**` | tout utilisateur authentifié |
| `POST /api/mouvements/*/annuler` | `ADMIN`, `SUPERVISEUR` |
| `PUT /api/tickets/**` | `ADMIN`, `AGENT_ZONE` |
| `PATCH /api/tickets/*/activer` | **`ADMIN`, `SUPERVISEUR`** |
| `PATCH /api/tickets/*/rejeter` | **`ADMIN`, `SUPERVISEUR`** |
| `POST /api/tickets` | `ADMIN`, `AGENT_ZONE`, `AGENT_COLLINE` |
| `POST /api/tickets/expirer` | `ADMIN`, `SUPERVISEUR` |
| `POST /api/distributions` | `ADMIN`, `SUPERVISEUR`, `AGENT_ZONE`, `AGENT_COLLINE` |
| `POST /api/lots/**` | `ADMIN`, `AGENT_LOGISTIQUE` |
| `GET /api/lots/**` | `ADMIN`, `AGENT_ZONE`, `AGENT_COLLINE`, `SUPERVISEUR`, `AGENT_LOGISTIQUE` |
| `GET /api/export/**` | `ADMIN`, `SUPERVISEUR`, `AGENT_ZONE`, `AGENT_LOGISTIQUE` |
| `POST`/`PUT` `/api/depots/**` | `ADMIN` |
| `POST`/`PUT` `/api/agriculteurs/**` | `ADMIN`, `AGENT_ZONE`, `AGENT_COLLINE` |
| `GET /api/engrais-types/**` | authentifié |
| `POST`/`PUT`/`DELETE` `/api/engrais-types/**` | `ADMIN` |
| `GET /api/seuils-alerte/**` | authentifié |
| `POST`/`PUT`/`DELETE` `/api/seuils-alerte/**` | `ADMIN` |

### Règles métier sur les rôles (dans `DistributionService`)

- `AGENT_COLLINE` : ne peut distribuer que **sur son propre dépôt**.
- `AGENT_ZONE` : ne peut distribuer que **dans sa zone**.
- Ces contrôles sont **en plus** du RBAC : un agent ne peut pas distribuer sur un dépôt hors
  de son périmètre même s'il a le rôle autorisé.

---

## Annexe B — Incohérences et points de vigilance

Points relevés en comparant les diagrammes, `SecurityConfig`, le code et les migrations.
**À connaître avant la soutenance** : mieux vaut les maîtriser que se les voir signaler.

### 1. Validation des tickets : diagramme vs RBAC

- **Le diagramme de cas d'utilisation** associe la validation au rôle `AGENT_ZONE`.
- **`SecurityConfig`** réserve `activer` et `rejeter` à **`ADMIN` et `SUPERVISEUR`**.
- **Le texte du rapport** peut encore citer un agent provincial dans les scripts historiques
  de `tools/rapport/` (`canevas_fixfacts.py`).
- ➜ **Décision à prendre** : soit corriger le diagramme, soit assumer le diagramme comme
  intention fonctionnelle et s'appuyer sur l'annexe A. Il ne faut **pas** laisser les deux se
  contredire dans le même document.

### 2. Transfert de stock

- **Le diagramme** suggère que l'agent logistique transfère du stock.
- **`SecurityConfig`** réserve `POST /api/mouvements/transfert` à **`ADMIN` seul**.
- ➜ La réception, en revanche, est bien partagée `ADMIN` / `AGENT_LOGISTIQUE`.

### 3. Statuts jamais atteints

- `ANNULE` et `RECLAMATION` figurent dans `StatutTicket` mais **aucun code ne les assigne**.
- `PAYE` et `EN_ATTENTE` sont acceptés par `DistributionService` comme statuts distribuables,
  mais seul `PAYE` est la valeur par défaut de l'entité — reliquat historique.
- ➜ Si ces statuts apparaissent dans d'autres figures du mémoire, ils sont inexacts.

### 4. Compteurs (valeurs divergentes selon les fichiers)

| Donnée | Valeur **réelle** (code) | Remarque |
|---|---|---|
| Tests (`@Test`) | **218** | le rapport indique 218 (dont 215 d'intégration) |
| Repositories | **17** | `CommuneRepository` inclus |
| Migrations | **13** (`V1`→`V13`) | `V13__commune_depots_province_zone.sql` incluse |
| Tables | **17** | table `commune` incluse |
| Contrôleurs | **17** | inchangé |
| Endpoints | **65** mappings | `GeoController` expose communes et zones par commune |

➜ **Le rapport, les diagrammes et ce guide sont désormais alignés.** Les anciens scripts de
`tools/rapport/` et `generate_docx.py` peuvent encore afficher 207 tests, 16 tables, 12
migrations ou 62 endpoints : **ne pas les rejouer** sur le rapport final, ils sont conservés
pour l'historique.

### 5. Fichiers obsolètes dans le dépôt

`test_syntax.py` et `test_parse.py` sont d'**anciennes copies** de `generate_memoire.py`,
figées à 203 tests / 15 repositories / 11 migrations. Si quelqu'un les exécute, ils écrasent
les diagrammes à jour par des versions périmées. ➜ À supprimer ou à neutraliser.

### 6. Bugs relevés dans `AlerteService`

- **Nom de variable trompeur** : `LocalDateTime ilYADixSeptJours = LocalDateTime.now().minusDays(7);`
  — la variable dit « 17 jours » mais la valeur est **7 jours**.
- **Doublons possibles d'alertes `INACTIVITE`** : quand `engraisType` est `null`, la
  vérification d'unicité (`existe`) est court-circuitée à `false`, donc une **nouvelle alerte
  est créée à chaque exécution** du planificateur.
  ➜ Ces deux points sont dans le **code**, pas dans les diagrammes, mais un jury attentif peut
  les poser en question.

### 7. Tâches planifiées (réelles)

| Heure | Méthode | Rôle |
|---|---|---|
| 06h00 | `scheduledDelais()` | Alerte `DELAI_DEPASSE` pour les tickets non servis depuis **30 jours** |
| 06h30 | `scheduledInactivite()` | Alerte `INACTIVITE` pour les dépôts sans mouvement depuis **7 jours** |

➜ Le diagramme de déploiement ne montre pas ces tâches ; si tu veux les intégrer, il faut
indiquer que l'API exécute elle-même ces jobs (pas de serveur de tâches externe).

---

## Annexe C — Régénérer les diagrammes

Les sources PlantUML **sont versionnées** dans `memoire_assets/puml_src/`. Chaque fichier
`.puml` produit le PNG et le SVG du même nom dans `memoire_assets/`.

1. Modifier la source concernée dans `memoire_assets/puml_src/`.
2. Régénérer les images (Java 21 + `plantuml.jar` ; Graphviz est optionnel, PlantUML bascule
   sur son moteur interne s'il est absent) :

```powershell
java -jar plantuml.jar -tpng -o memoire_assets memoire_assets\puml_src\*.puml
java -jar plantuml.jar -tsvg -o memoire_assets memoire_assets\puml_src\*.puml
```

3. Réinjecter les PNG dans le rapport en conservant les proportions :

```powershell
python update_docx_diagrams.py
```

Le script `update_docx_diagrams.py` remplace les huit figures, plafonne la largeur à 15 cm et
la hauteur à 20 cm, puis enregistre `Rapport_stage_FOMI_canevas.docx`.

**Thème** : chaque source déclare son thème (`!theme vibrant`, `!theme toy`, ou styles
`skinparam`). Conserver le thème existant d'un fichier pour ne pas casser l'homogénéité du
mémoire ; la police commune est `Segoe UI` et le rendu PNG utilise `skinparam dpi 150`.

**Insertion dans Word** : `Insertion` → `Images` → `Cet appareil` → sélectionner le `.svg`.
Word 2016+ gère nativement le SVG.

---

## Récapitulatif pour la soutenance

| Si on te demande… | Réponds… |
|---|---|
| Le cœur technique du système | La séquence de distribution FIFO avec verrou pessimiste |
| Comment tu garantis l'intégrité | Triple protection : contrôleur, service, contraintes SQL |
| Comment tu évites la double distribution | `SELECT ... FOR UPDATE` + clé d'idempotence |
| Pourquoi FIFO par date de réception | Choix métier : écouler le stock le plus ancien en dépôt |
| Comment l'agriculteur suit sa commande | Endpoint public, sans compte, par numéro de ticket |
| Pourquoi les distributions partielles | `Distribution` séparée de `Ticket`, statut `PARTIEL` |
| Ce que tu améliorerais | Corriger les doublons d'alertes, ajouter les statuts `ANNULE`/`RECLAMATION` |
