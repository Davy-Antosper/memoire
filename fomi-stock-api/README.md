# fomi-stock-api

API REST de gestion des stocks d'engrais FOMI : réceptions, transferts, distributions FIFO, tickets agriculteurs, alertes de stock, statistiques et audit.

## Stack

- Java 21, Spring Boot 3.3, Spring Security + JWT, Spring Data JPA
- PostgreSQL 16, Flyway (migrations SQL)
- Testcontainers (tests d'intégration), JUnit 5, AssertJ, MockMvc
- OpenAPI (Swagger UI) via springdoc

## Prérequis

- JDK 21
- Maven 3.8+
- Docker (pour les tests d'intégration)
- PostgreSQL 16 en local (pour le mode dev)

## Installation et lancement

```bash
# 1. Base de données
sudo -u postgres psql -c "CREATE USER fomi WITH PASSWORD 'fomi123';"
sudo -u postgres psql -c "CREATE DATABASE fomi_stock OWNER fomi;"

# 2. Compiler
mvn clean package

# 3. Lancer (profil dev par défaut, port 8080)
mvn spring-boot:run
```

Le schéma et les données de démonstration (géographie, dépôts, 500 agriculteurs, tickets, alertes) sont créés automatiquement par Flyway au démarrage.

**Swagger UI** : http://localhost:8080/swagger-ui.html — **Spécification** : http://localhost:8080/api-docs

## Utilisateurs de démonstration

| Login          | Mot de passe | Rôle          | Périmètre                          |
|----------------|--------------|---------------|------------------------------------|
| `admin`        | `password`   | ADMIN         | Tout                               |
| `agent.zone`   | `password`   | AGENT_ZONE    | Zone Gitega Centre (id 1)          |
| `agent.colline`| `password`   | AGENT_COLLINE | Dépôt de zone DEP-MUT (id 6)       |
| `superviseur`  | `password`   | SUPERVISEUR   | Lecture statistiques               |
| `agent.fomi`   | `password`   | AGENT_LOGISTIQUE | Réceptions de lots FOMI         |

Connexion : `POST /api/auth/login` avec `{"username":"...","password":"..."}` → renvoie un `token` JWT à envoyer dans l'en-tête `Authorization: Bearer <token>` (expiration : 24 h).

## Tests

```bash
mvn test          # ou mvn verify
```

Les tests d'intégration démarrent un conteneur PostgreSQL éphémère via Testcontainers et couvrent l'ensemble des endpoints et des règles métier. Configuration requise : le fichier `src/test/resources/docker-java.properties` fixe la version d'API Docker (`api.version=1.44`) pour les moteurs Docker récents.

Sans Docker, la suite peut tourner contre une base PostgreSQL locale vide (le schéma et les seeds sont appliqués par Flyway) :

```bash
sudo -u postgres psql -c "CREATE DATABASE fomi_test OWNER fomi;"
mvn test -Dfomi.test.localdb=true
```

Les paramètres de connexion sont surchargeables avec `-Dfomi.test.db.url`, `-Dfomi.test.db.username` et `-Dfomi.test.db.password` (ou `FOMI_TEST_LOCALDB=true`).

## Règles métier principales

- **FIFO** : la distribution et le transfert consomment les lots dans l'ordre d'ancienneté de réception (`date_reception_fomi`), sauf si un `lotId` est forcé (contrôlé : type d'engrais et quantité disponibles).
- **Concurrence** : les lectures-écritures de stock (`stock_lot`, `stock`), du lot et du ticket sont protégées par des verrous pessimistes (`PESSIMISTIC_WRITE`) — deux distributions/réceptions simultanées ne peuvent pas survendre ni perdre de mise à jour.
- **Tickets** : un ticket `PAYE`/`EN_ATTENTE`/`PARTIEL` peut être servi tant qu'il reste une quantité ; un ticket `RECLAMATION`/`ANNULE` ou entièrement servi est refusé.
- **Idempotence** : la réception accepte une `idempotencyKey` ; une clé déjà utilisée renvoie 400.
- **Alertes** : générées automatiquement après réception/transfert/distribution — `RUPTURE` (stock 0), `STOCK_BAS` (sous le seuil du dépôt), `DEMANDE_SUP_STOCK` (demande non servie > stock) — et par la tâche planifiée quotidienne (06:00) pour les tickets impayés/servis partiellement depuis plus de 30 jours (`DELAI_DEPASSE`).
- **Périmètres** : `AGENT_COLLINE` ne distribue que sur son dépôt ; `AGENT_ZONE` que dans sa zone ; réception et transfert réservés à `ADMIN`.
- **Audit** : toute création de ticket/dépôt et tout mouvement/distribution/utilisateur est journalisé dans `audit_log`.
- **Notifications email** : chaque changement d'état d'un ticket (`TICKET_CREE`, `TICKET_VALIDE`, `TICKET_REJETE`, `TICKET_EXPIRE`) et chaque distribution envoie un email à l'agriculteur s'il possède une adresse. L'envoi est tracé (`EMAIL_SEND` / `EMAIL_FAILED`) et reste non bloquant : une panne SMTP ne fait pas échouer l'opération métier.

## Endpoints

### Authentification
| Méthode | URL | Rôles |
|---------|-----|-------|
| POST | `/api/auth/login` | public |

### Administration utilisateurs
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/utilisateurs` | ADMIN |
| GET | `/api/utilisateurs/{id}` | ADMIN |
| POST | `/api/utilisateurs` | ADMIN |
| PUT | `/api/utilisateurs/{id}` | ADMIN |

### Géographie et référentiel
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/provinces`, `/api/communes`, `/api/zones`, `/api/collines` | authentifié |
| GET | `/api/provinces/{id}/communes`, `/api/provinces/{id}/zones` | authentifié |
| GET | `/api/communes/{id}/zones`, `/api/zones/{id}/collines` | authentifié |
| GET | `/api/engrais-types` | authentifié |

Hiérarchie officielle : `Province → Commune → Zone → Colline`. La colline est le
lieu de résidence des agriculteurs ; seuls les dépôts `PROVINCE` (logistique) et
`ZONE` (distribution) existent.

### Agriculteurs
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/agriculteurs?page=0&size=50` | authentifié |
| GET | `/api/agriculteurs/{id}` | authentifié |
| GET | `/api/agriculteurs/recherche?telephone=...` | authentifié |
| POST | `/api/agriculteurs` | ADMIN, AGENT_ZONE, AGENT_COLLINE |
| PUT | `/api/agriculteurs/{id}` | ADMIN, AGENT_ZONE, AGENT_COLLINE |
| POST | `/api/agriculteurs/{id}/notifier` | ADMIN, AGENT_ZONE, AGENT_COLLINE |

### Tickets
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/tickets?depotId=&statut=` | authentifié |
| GET | `/api/tickets/{id}` | authentifié |
| POST | `/api/tickets` | ADMIN, AGENT_ZONE, AGENT_COLLINE |
| PUT | `/api/tickets/{id}` | ADMIN, AGENT_ZONE |
| PATCH | `/api/tickets/{id}/activer` | ADMIN, SUPERVISEUR |
| PATCH | `/api/tickets/{id}/rejeter` | ADMIN, SUPERVISEUR |
| POST | `/api/tickets/expirer?saison=...` | ADMIN, SUPERVISEUR |

### Dépôts
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/depots`, `/api/depots/{id}` | authentifié |
| GET | `/api/depots/{id}/stock` | authentifié |
| POST | `/api/depots` | ADMIN |
| PUT | `/api/depots/{id}` | ADMIN |

### Stocks
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/stocks?depotId=&engraisTypeId=` | authentifié |
| GET | `/api/stocks/disponibles` | authentifié |

### Mouvements
| Méthode | URL | Rôles |
|---------|-----|-------|
| POST | `/api/mouvements/reception` | ADMIN, AGENT_LOGISTIQUE |
| POST | `/api/mouvements/transfert` | ADMIN |
| POST | `/api/mouvements/{id}/annuler` | authentifié (règle ADMIN/SUPERVISEUR non appliquée) |
| GET | `/api/mouvements`, `/api/mouvements/lot/{lotId}` | authentifié |

### Distributions
| Méthode | URL | Rôles |
|---------|-----|-------|
| POST | `/api/distributions` | ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE |
| GET | `/api/distributions/ticket/{ticketId}` | authentifié |

### Alertes
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/alertes?nonTraitees=true` | ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE |
| GET | `/api/alertes/depot/{depotId}` | idem |
| PATCH | `/api/alertes/{id}/traiter` | ADMIN |

### Statistiques
| Méthode | URL | Rôles |
|---------|-----|-------|
| GET | `/api/statistiques/taux-service` | ADMIN, SUPERVISEUR |
| GET | `/api/statistiques/stocks-par-province` | ADMIN, SUPERVISEUR |
| GET | `/api/statistiques/ruptures` | ADMIN, SUPERVISEUR |

## Configuration

| Variable | Rôle | Défaut |
|----------|------|--------|
| `JWT_SECRET` | Clé de signature JWT (obligatoire en prod) | valeur de développement |
| `SPRING_PROFILES_ACTIVE` | Profil Spring (`dev` ou `prod`) | `dev` |
| `DB_URL` | URL JDBC PostgreSQL (profil `prod`) | `jdbc:postgresql://localhost:5432/fomi_stock` |
| `DB_USERNAME` | Utilisateur PostgreSQL (profil `prod`) | `fomi` |
| `DB_PASSWORD` | Mot de passe PostgreSQL (profil `prod`) | `fomi123` |
| `PORT` | Port HTTP (profil `prod`, défini par la plateforme) | `8080` |
| `FOMI_MAIL_ENABLED` | Active l'envoi réel des emails | `false` |
| `FOMI_MAIL_FROM` | Expéditeur des emails | `no-reply@fomi.bi` |
| `FOMI_MAIL_SUJET_PREFIX` | Préfixe des sujets | `[FOMI-Stock] ` |
| `MAIL_HOST` / `MAIL_PORT` | Serveur SMTP | `localhost` / `1025` |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | Identifiants SMTP | vide |
| `MAIL_SMTP_AUTH` / `MAIL_SMTP_STARTTLS` | Authentification et TLS SMTP | `false` |

### Notifications email

Les notifications sont **désactivées par défaut** : aucun email n'est envoyé tant que `FOMI_MAIL_ENABLED=true` n'est pas défini. Pour les tester localement, lancer un serveur SMTP de capture (Mailpit, MailHog ou `python -m smtpd -c DebuggingServer -n localhost:1025`) puis démarrer l'API :

```bash
FOMI_MAIL_ENABLED=true MAIL_HOST=localhost MAIL_PORT=1025 mvn spring-boot:run
```

Exemple d'envoi manuel :

```bash
curl -X POST http://localhost:8080/api/agriculteurs/1/notifier \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"sujet":"Engrais disponible","message":"Votre engrais est prêt au dépôt."}'
```

## Déploiement

Le dépôt contient un `Dockerfile` multi-étapes (image JRE 21, heap `-Xmx256m`) et un profil `prod` piloté par variables d'environnement. Il est prêt pour Railway, Render, Fly.io, ou toute plateforme compatible Docker.

```bash
# Construire l'image localement (optionnel)
docker build -t fomi-stock-api .
docker run -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e DB_URL=jdbc:postgresql://HOST:5432/fomi_stock \
  -e DB_USERNAME=fomi -e DB_PASSWORD=xxx \
  -e JWT_SECRET=uneCleDeSignatureLongueMin256Bits \
  fomi-stock-api
```

Flyway crée le schéma et les données de démonstration sur la base distante au premier démarrage. Mises à jour : pousser le code (déploiement automatique sur la plateforme) puis, en local, `git pull` + redémarrage du service.

## Structure

```
src/main/java/bi/fomi/stock/
├── controller/     # Endpoints REST
├── service/        # Logique métier (FIFO, alertes, audit, stats, sécurité)
├── repository/     # Accès données Spring Data JPA
├── dto/            # Requêtes / réponses
├── model/          # Entités JPA et enums
├── security/       # JWT, filtres, config
└── exception/      # Gestion d'erreurs centralisée
src/main/resources/db/migration/   # Schéma et seeds Flyway (V1 à V13)
src/test/java/bi/fomi/stock/       # tests d'intégration
```
