-- Lot B : conformité au cahier des charges
-- saison culturale, capacité max dépôts, seuils par type engrais, soft delete, annulation mouvements, péremption alerte

-- 1. Ticket : saison culturale + superficie certifiée (R6, R22) + soft delete (F27)
ALTER TABLE ticket ADD COLUMN saison VARCHAR(10) NOT NULL DEFAULT '2026A';
ALTER TABLE ticket ADD COLUMN superficie_ha DECIMAL(8, 2);
ALTER TABLE ticket ADD COLUMN supprime BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE ticket ADD COLUMN deleted_at TIMESTAMP;
CREATE INDEX idx_ticket_saison ON ticket(saison);

-- 2. Depot : capacité maximale (R12)
ALTER TABLE depot ADD COLUMN capacite_max INTEGER;
ALTER TABLE depot ADD COLUMN supprime BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE depot ADD COLUMN deleted_at TIMESTAMP;

-- 3. Seuils d'alerte par type d'engrais et niveau de dépôt (R3)
CREATE TABLE seuil_alerte (
    id              BIGSERIAL PRIMARY KEY,
    depot_id        BIGINT NOT NULL REFERENCES depot(id),
    engrais_type_id BIGINT NOT NULL REFERENCES engrais_type(id),
    seuil_min       INTEGER NOT NULL CHECK (seuil_min > 0),
    criticite       VARCHAR(20) NOT NULL DEFAULT 'WARNING',
    UNIQUE (depot_id, engrais_type_id)
);
CREATE INDEX idx_seuil_alerte_depot ON seuil_alerte(depot_id, engrais_type_id);

-- 4. Agriculteur : soft delete (F27) + superficie certifiée
ALTER TABLE agriculteur ADD COLUMN supprime BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE agriculteur ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE agriculteur ADD COLUMN superficie_ha DECIMAL(8, 2);

-- 5. Utilisateur : soft delete (F27)
ALTER TABLE utilisateur ADD COLUMN supprime BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE utilisateur ADD COLUMN deleted_at TIMESTAMP;

-- 6. Mouvement : colonnes pour annulation (UC-12/R8)
ALTER TABLE mouvement ADD COLUMN annule BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE mouvement ADD COLUMN motif_annulation VARCHAR(500);
ALTER TABLE mouvement ADD COLUMN annule_par_id BIGINT REFERENCES utilisateur(id);
ALTER TABLE mouvement ADD COLUMN reference_annulation_id BIGINT REFERENCES mouvement(id);

-- 7. TypeAlerte : ajouter PEREMPTION et INACTIVITE
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'PEREMPTION' AND enumtypid = 'type_alerte'::regtype) THEN
        ALTER TYPE type_alerte ADD VALUE 'PEREMPTION';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'INACTIVITE' AND enumtypid = 'type_alerte'::regtype) THEN
        ALTER TYPE type_alerte ADD VALUE 'INACTIVITE';
    END IF;
END $$;
