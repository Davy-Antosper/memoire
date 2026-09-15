-- FOMI Stock API - Schema initial
-- Province -> Zone -> Colline

CREATE TABLE province (
    id          BIGSERIAL PRIMARY KEY,
    code        VARCHAR(10)  NOT NULL UNIQUE,
    nom         VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE zone (
    id          BIGSERIAL PRIMARY KEY,
    code        VARCHAR(20)  NOT NULL UNIQUE,
    nom         VARCHAR(100) NOT NULL,
    province_id BIGINT       NOT NULL REFERENCES province(id),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_zone_province ON zone(province_id);

CREATE TABLE colline (
    id          BIGSERIAL PRIMARY KEY,
    code        VARCHAR(30)  NOT NULL UNIQUE,
    nom         VARCHAR(100) NOT NULL,
    zone_id     BIGINT       NOT NULL REFERENCES zone(id),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_colline_zone ON colline(zone_id);

CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE', 'COLLINE');

CREATE TABLE depot (
    id               BIGSERIAL PRIMARY KEY,
    code             VARCHAR(30)   NOT NULL UNIQUE,
    nom              VARCHAR(150)  NOT NULL,
    niveau           niveau_depot  NOT NULL,
    province_id      BIGINT        REFERENCES province(id),
    zone_id          BIGINT        REFERENCES zone(id),
    colline_id       BIGINT        REFERENCES colline(id),
    seuil_alerte_min INTEGER       NOT NULL DEFAULT 100,
    actif            BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMP     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_depot_niveau CHECK (
        (niveau = 'PROVINCE' AND province_id IS NOT NULL AND zone_id IS NULL AND colline_id IS NULL) OR
        (niveau = 'ZONE'     AND zone_id IS NOT NULL     AND colline_id IS NULL) OR
        (niveau = 'COLLINE'  AND colline_id IS NOT NULL)
    )
);

CREATE INDEX idx_depot_niveau ON depot(niveau, province_id, zone_id, colline_id);

CREATE TABLE engrais_type (
    id                 BIGSERIAL PRIMARY KEY,
    code               VARCHAR(20)   NOT NULL UNIQUE,
    nom                VARCHAR(100)  NOT NULL,
    poids_sac_kg       DECIMAL(8, 2) NOT NULL DEFAULT 50.00,
    prix_subventionne  DECIMAL(12, 2) NOT NULL,
    actif              BOOLEAN       NOT NULL DEFAULT TRUE
);

CREATE TABLE lot (
    id                  BIGSERIAL PRIMARY KEY,
    numero_lot          VARCHAR(50) NOT NULL UNIQUE,
    engrais_type_id     BIGINT      NOT NULL REFERENCES engrais_type(id),
    quantite_initiale   INTEGER     NOT NULL CHECK (quantite_initiale > 0),
    date_fabrication    DATE,
    date_peremption     DATE,
    date_reception_fomi TIMESTAMP   NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lot_engrais ON lot(engrais_type_id);

CREATE TABLE stock (
    id                   BIGSERIAL PRIMARY KEY,
    depot_id             BIGINT    NOT NULL REFERENCES depot(id),
    engrais_type_id      BIGINT    NOT NULL REFERENCES engrais_type(id),
    quantite_disponible  INTEGER   NOT NULL DEFAULT 0 CHECK (quantite_disponible >= 0),
    updated_at           TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (depot_id, engrais_type_id)
);

CREATE TABLE stock_lot (
    id          BIGSERIAL PRIMARY KEY,
    depot_id    BIGINT    NOT NULL REFERENCES depot(id),
    lot_id      BIGINT    NOT NULL REFERENCES lot(id),
    quantite    INTEGER   NOT NULL DEFAULT 0 CHECK (quantite >= 0),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (depot_id, lot_id)
);

CREATE TABLE agriculteur (
    id               BIGSERIAL PRIMARY KEY,
    numero_identite  VARCHAR(30) NOT NULL UNIQUE,
    nom              VARCHAR(100) NOT NULL,
    prenom           VARCHAR(100) NOT NULL,
    telephone        VARCHAR(20),
    colline_id       BIGINT      NOT NULL REFERENCES colline(id),
    est_cooperative  BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_agriculteur_colline ON agriculteur(colline_id);

CREATE TYPE statut_ticket AS ENUM (
    'PAYE', 'EN_ATTENTE', 'PARTIEL', 'SERVI', 'RECLAMATION', 'ANNULE'
);

CREATE TABLE ticket (
    id                  BIGSERIAL PRIMARY KEY,
    numero_ticket       VARCHAR(50)    NOT NULL UNIQUE,
    agriculteur_id      BIGINT         NOT NULL REFERENCES agriculteur(id),
    engrais_type_id     BIGINT         NOT NULL REFERENCES engrais_type(id),
    quantite_commandee  INTEGER        NOT NULL CHECK (quantite_commandee > 0),
    quantite_servie     INTEGER        NOT NULL DEFAULT 0 CHECK (quantite_servie >= 0),
    montant_paye        DECIMAL(12, 2) NOT NULL,
    date_paiement       DATE           NOT NULL,
    depot_retrait_id    BIGINT         NOT NULL REFERENCES depot(id),
    statut              statut_ticket  NOT NULL DEFAULT 'PAYE',
    date_creation       TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP      NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_ticket_quantite CHECK (quantite_servie <= quantite_commandee)
);

CREATE INDEX idx_ticket_statut ON ticket(statut);
CREATE INDEX idx_ticket_agriculteur ON ticket(agriculteur_id);
CREATE INDEX idx_ticket_depot_retrait ON ticket(depot_retrait_id, statut);

CREATE TYPE role_utilisateur AS ENUM (
    'ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'
);

CREATE TABLE utilisateur (
    id            BIGSERIAL PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nom_complet   VARCHAR(150) NOT NULL,
    role          role_utilisateur NOT NULL,
    depot_id      BIGINT       REFERENCES depot(id),
    zone_id       BIGINT       REFERENCES zone(id),
    province_id   BIGINT       REFERENCES province(id),
    actif         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TYPE type_mouvement AS ENUM (
    'RECEPTION_FOMI', 'TRANSFERT', 'DISTRIBUTION', 'AJUSTEMENT'
);

CREATE TABLE mouvement (
    id               BIGSERIAL PRIMARY KEY,
    type             type_mouvement NOT NULL,
    lot_id           BIGINT         NOT NULL REFERENCES lot(id),
    engrais_type_id  BIGINT         NOT NULL REFERENCES engrais_type(id),
    depot_source_id  BIGINT         REFERENCES depot(id),
    depot_dest_id    BIGINT         REFERENCES depot(id),
    quantite         INTEGER        NOT NULL CHECK (quantite > 0),
    agent_id         BIGINT         NOT NULL REFERENCES utilisateur(id),
    ticket_id        BIGINT         REFERENCES ticket(id),
    commentaire      VARCHAR(500),
    date_mouvement   TIMESTAMP      NOT NULL DEFAULT NOW(),
    idempotency_key  VARCHAR(64)    UNIQUE
);

CREATE INDEX idx_mouvement_lot ON mouvement(lot_id, date_mouvement);
CREATE INDEX idx_mouvement_source ON mouvement(depot_source_id);
CREATE INDEX idx_mouvement_dest ON mouvement(depot_dest_id);
CREATE INDEX idx_mouvement_ticket ON mouvement(ticket_id);

CREATE TABLE distribution (
    id                     BIGSERIAL PRIMARY KEY,
    ticket_id              BIGINT    NOT NULL REFERENCES ticket(id),
    lot_id                 BIGINT    NOT NULL REFERENCES lot(id),
    depot_id               BIGINT    NOT NULL REFERENCES depot(id),
    quantite               INTEGER   NOT NULL CHECK (quantite > 0),
    agent_id               BIGINT    NOT NULL REFERENCES utilisateur(id),
    date_distribution      TIMESTAMP NOT NULL DEFAULT NOW(),
    reference_mouvement_id BIGINT    NOT NULL UNIQUE REFERENCES mouvement(id)
);

CREATE INDEX idx_distribution_ticket ON distribution(ticket_id);

CREATE TYPE type_alerte AS ENUM (
    'STOCK_BAS', 'RUPTURE', 'DELAI_DEPASSE', 'DEMANDE_SUP_STOCK'
);

CREATE TYPE niveau_alerte AS ENUM ('INFO', 'WARNING', 'CRITICAL');

CREATE TABLE alerte (
    id              BIGSERIAL PRIMARY KEY,
    depot_id        BIGINT        NOT NULL REFERENCES depot(id),
    engrais_type_id BIGINT        NOT NULL REFERENCES engrais_type(id),
    type            type_alerte   NOT NULL,
    message         VARCHAR(500)  NOT NULL,
    niveau          niveau_alerte NOT NULL DEFAULT 'WARNING',
    traitee         BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alerte_depot ON alerte(depot_id, traitee);

CREATE TABLE audit_log (
    id              BIGSERIAL PRIMARY KEY,
    utilisateur_id  BIGINT        REFERENCES utilisateur(id),
    action          VARCHAR(100)  NOT NULL,
    entity_type     VARCHAR(50)   NOT NULL,
    entity_id       BIGINT,
    ip_address      VARCHAR(45),
    details_json    JSONB,
    created_at      TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(utilisateur_id, created_at);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
