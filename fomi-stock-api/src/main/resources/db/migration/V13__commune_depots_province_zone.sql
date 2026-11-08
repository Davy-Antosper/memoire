-- V13 : référentiel géographique officiel Province -> Commune -> Zone -> Colline
-- et alignement des dépôts sur le modèle FOMI : PROVINCE (logistique) et ZONE (distribution).
-- Aucun dépôt communal ni de colline : la FOMI achemine les engrais jusqu'aux zones.

-- 1. Référentiel des communes (2e niveau administratif du Burundi)
CREATE TABLE commune (
    id          BIGSERIAL PRIMARY KEY,
    code        VARCHAR(30)  NOT NULL UNIQUE,
    nom         VARCHAR(100) NOT NULL,
    province_id BIGINT       NOT NULL REFERENCES province(id),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_commune_province ON commune(province_id);

INSERT INTO commune (code, nom, province_id) VALUES
    ('GIT-CO-GIT', 'Gitega',    (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-BUG', 'Bugendana', (SELECT id FROM province WHERE code = 'GIT')),
    ('BUB-CO-BUB', 'Bubanza',   (SELECT id FROM province WHERE code = 'BUB')),
    ('BUB-CO-MUS', 'Musigati',  (SELECT id FROM province WHERE code = 'BUB')),
    ('NGO-CO-NGO', 'Ngozi',     (SELECT id FROM province WHERE code = 'NGO'));

-- 2. La zone devient une subdivision de la commune
ALTER TABLE zone ADD COLUMN commune_id BIGINT REFERENCES commune(id);

UPDATE zone z
SET commune_id = CASE z.code
        WHEN 'GIT-C' THEN (SELECT id FROM commune WHERE code = 'GIT-CO-GIT')
        WHEN 'GIT-N' THEN (SELECT id FROM commune WHERE code = 'GIT-CO-BUG')
        WHEN 'BUB-O' THEN (SELECT id FROM commune WHERE code = 'BUB-CO-BUB')
        WHEN 'NGO-C' THEN (SELECT id FROM commune WHERE code = 'NGO-CO-NGO')
    END
WHERE z.commune_id IS NULL;

-- Filet de sécurité pour toute zone ajoutée hors des seeds
UPDATE zone z
SET commune_id = (SELECT c.id FROM commune c WHERE c.province_id = z.province_id ORDER BY c.id LIMIT 1)
WHERE z.commune_id IS NULL;

ALTER TABLE zone ALTER COLUMN commune_id SET NOT NULL;
CREATE INDEX idx_zone_commune ON zone(commune_id);
DROP INDEX IF EXISTS idx_zone_province;
ALTER TABLE zone DROP COLUMN province_id;

-- 3. Conversion des anciens dépôts de colline en dépôts de zone.
--    Les identifiants (6 à 9) sont conservés : les stocks, tickets et alertes de démonstration
--    qui les référencent restent valides.
ALTER TABLE depot DROP CONSTRAINT IF EXISTS chk_depot_niveau;

UPDATE depot d
SET niveau   = 'ZONE',
    zone_id  = c.zone_id,
    nom      = REPLACE(d.nom, 'Colline', 'Zone')
FROM colline c
WHERE d.colline_id = c.id
  AND d.niveau = 'COLLINE';

ALTER TABLE depot DROP COLUMN IF EXISTS colline_id;

-- 4. L'enum ne comporte plus que les deux niveaux FOMI
ALTER TYPE niveau_depot RENAME TO niveau_depot_old;
CREATE TYPE niveau_depot AS ENUM ('PROVINCE', 'ZONE');
ALTER TABLE depot ALTER COLUMN niveau TYPE niveau_depot USING niveau::text::niveau_depot;
DROP TYPE niveau_depot_old;

DROP INDEX IF EXISTS idx_depot_niveau;

ALTER TABLE depot ADD CONSTRAINT chk_depot_niveau CHECK (
    (niveau = 'PROVINCE' AND province_id IS NOT NULL AND zone_id IS NULL) OR
    (niveau = 'ZONE'     AND zone_id IS NOT NULL     AND province_id IS NULL)
);

CREATE INDEX idx_depot_niveau ON depot(niveau, province_id, zone_id);
