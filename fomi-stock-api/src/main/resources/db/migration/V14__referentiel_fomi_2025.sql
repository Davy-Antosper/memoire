-- V14 : mise en conformité avec la réalité burundaise et la gamme FOMI 2026.
--
-- Sources :
--   * Loi organique n° 1/05 du 16 mars 2023 portant détermination et délimitation
--     des provinces, communes, zones, collines et/ou quartiers (5 provinces,
--     42 communes, 451 zones, 3 044 collines), appliquée après les élections de 2025.
--   * Communiqués de prix FOMI / RPA (saison 2026) : Imbura 31 000 BIF,
--     Totahaza 33 000 BIF (à confirmer), Bagara 28 000 BIF, dolomie 5 000 BIF/50 kg.
--   * Sacs de 25 kg (et non 50 kg).
--
-- La migration conserve les identifiants existants (dépôts, tickets, stocks) et
-- se contente de corriger les libellés, les rattachements et les prix.

-- ---------------------------------------------------------------------------
-- 1. Colonnes de traçabilité et de démonstration
-- ---------------------------------------------------------------------------
ALTER TABLE engrais_type ADD COLUMN IF NOT EXISTS prix_a_confirmer BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE ticket        ADD COLUMN IF NOT EXISTS motif_rejet VARCHAR(500);
ALTER TABLE ticket        ADD COLUMN IF NOT EXISTS est_demo BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE agriculteur   ADD COLUMN IF NOT EXISTS est_demo BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE depot        ADD COLUMN IF NOT EXISTS est_demo BOOLEAN NOT NULL DEFAULT FALSE;

-- ---------------------------------------------------------------------------
-- 2. Les 5 provinces issues de la loi de 2023
--    Les deux anciennes provinces BUB (Bubanza) et NGO (Ngozi) sont
--    respectivement remplacées par Bujumbura et Butanyerera sans perdre
--    les identifiants déjà référencés.
-- ---------------------------------------------------------------------------
UPDATE province SET code = 'BUJ', nom = 'Bujumbura'  WHERE code = 'BUB';
UPDATE province SET code = 'BUT', nom = 'Butanyerera' WHERE code = 'NGO';

INSERT INTO province (code, nom) VALUES
    ('BUH', 'Buhumuza'),
    ('BUR', 'Burunga')
ON CONFLICT (code) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 3. Les 42 communes officielles
--    On réutilise les 5 communes existantes puis on insère les 37 autres.
-- ---------------------------------------------------------------------------
UPDATE commune SET code = 'BUJ-CO-BUBANZA',   nom = 'Bubanza',     province_id = (SELECT id FROM province WHERE code = 'BUJ') WHERE code = 'BUB-CO-BUB';
UPDATE commune SET code = 'BUJ-CO-BUKINANYANA', nom = 'Bukinanyana', province_id = (SELECT id FROM province WHERE code = 'BUJ') WHERE code = 'BUB-CO-MUS';
UPDATE commune SET code = 'BUT-CO-NGOZI',     nom = 'Ngozi',       province_id = (SELECT id FROM province WHERE code = 'BUT') WHERE code = 'NGO-CO-NGO';

INSERT INTO commune (code, nom, province_id) VALUES
    -- Buhumuza (7)
    ('BUH-CO-BUTAGANZWA', 'Butaganzwa', (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-BUTIHINDA',  'Butihinda',  (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-CANKUZO',    'Cankuzo',    (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-GISAGARA',   'Gisagara',   (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-GISURU',     'Gisuru',     (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-MUYINGA',    'Muyinga',    (SELECT id FROM province WHERE code = 'BUH')),
    ('BUH-CO-RUYIGI',     'Ruyigi',     (SELECT id FROM province WHERE code = 'BUH')),
    -- Bujumbura (11)
    ('BUJ-CO-BUBANZA',    'Bubanza',    (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-BUKINANYANA','Bukinanyana',(SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-CIBITOKE',   'Cibitoke',   (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-ISARE',      'Isare',      (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-MPANDA',     'Mpanda',     (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-MUGERE',     'Mugere',     (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-MUGINA',     'Mugina',     (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-MUHUTA',     'Muhuta',     (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-MUKAZA',     'Mukaza',     (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-NTAHANGWA',  'Ntahangwa',  (SELECT id FROM province WHERE code = 'BUJ')),
    ('BUJ-CO-RWIBAGA',    'Rwibaga',    (SELECT id FROM province WHERE code = 'BUJ')),
    -- Burunga (7)
    ('BUR-CO-BURURI',     'Bururi',     (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-MAKAMBA',    'Makamba',    (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-MATANA',     'Matana',     (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-MUSONGATI',  'Musongati',  (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-NYANZA',     'Nyanza',     (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-RUMONGE',    'Rumonge',    (SELECT id FROM province WHERE code = 'BUR')),
    ('BUR-CO-RUTANA',     'Rutana',     (SELECT id FROM province WHERE code = 'BUR')),
    -- Butanyerera (8)
    ('BUT-CO-BUSONI',     'Busoni',     (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-KAYANZA',    'Kayanza',    (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-KIREMBA',    'Kiremba',    (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-KIRUNDO',    'Kirundo',    (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-MATONGO',    'Matongo',    (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-MUHANGA',    'Muhanga',    (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-NGOZI',      'Ngozi',      (SELECT id FROM province WHERE code = 'BUT')),
    ('BUT-CO-TANGARA',    'Tangara',    (SELECT id FROM province WHERE code = 'BUT')),
    -- Gitega (9) : Bugendana et Gitega sont recodées plus bas (UPDATE), elles
    -- ne doivent pas être insérées ici sous peine de doublon.
    ('GIT-CO-GISHUBI',    'Gishubi',    (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-KARUSI',     'Karusi',     (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-KIGANDA',    'Kiganda',    (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-MURAMVYA',   'Muramvya',   (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-MWARO',      'Mwaro',      (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-NYABIHANGA', 'Nyabihanga', (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-CO-SHOMBO',     'Shombo',     (SELECT id FROM province WHERE code = 'GIT'))
ON CONFLICT (code) DO NOTHING;

-- Les deux communes historiques Gitega et Bugendana sont recodées avec le
-- même schéma que les autres, sans changer leur identifiant.
UPDATE commune SET code = 'GIT-CO-GITEGA',  nom = 'Gitega',
       province_id = (SELECT id FROM province WHERE code = 'GIT') WHERE code = 'GIT-CO-GIT';
UPDATE commune SET code = 'GIT-CO-BUGENDANA', nom = 'Bugendana',
       province_id = (SELECT id FROM province WHERE code = 'GIT') WHERE code = 'GIT-CO-BUG';

-- ---------------------------------------------------------------------------
-- 4. Zones vérifiées (loi de 2023) pour les communes de démonstration
--    Gitega (12), Bugendana (7), Bubanza (8), Ngozi (12).
-- ---------------------------------------------------------------------------
-- 4.1 Réaffectation des 4 zones historiques
UPDATE zone SET code = 'GIT-Z-BUHEVYI', nom = 'Buhevyi',
       commune_id = (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')
WHERE code = 'GIT-C';

UPDATE zone SET code = 'GIT-Z-MUTAHO', nom = 'Mutaho',
       commune_id = (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')
WHERE code = 'GIT-N';

UPDATE zone SET code = 'BUJ-Z-MUSIGATI', nom = 'Musigati',
       commune_id = (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')
WHERE code = 'BUB-O';

UPDATE zone SET code = 'BUT-Z-MIVO', nom = 'Mivo',
       commune_id = (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')
WHERE code = 'NGO-C';

-- 4.2 Nouvelles zones (mêmes noms que dans la loi, sans invention)
INSERT INTO zone (code, nom, commune_id) VALUES
    -- Commune Gitega
    ('GIT-Z-BUHINDA',  'Buhinda',  (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-GIHETA',   'Giheta',   (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-ITABA',    'Itaba',    (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-KABANGA',  'Kabanga',  (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-KIRIBA',   'Kiriba',   (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MAKEBUKO', 'Makebuko', (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MARAMVYA', 'Maramvya', (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MARIZA',   'Mariza',   (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MUBUGA',   'Mubuga',   (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MUNGWA',   'Mungwa',   (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    ('GIT-Z-MURENDA',  'Murenda',  (SELECT id FROM commune WHERE code = 'GIT-CO-GITEGA')),
    -- Commune Bugendana
    ('GIT-Z-BITARE',   'Bitare',   (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    ('GIT-Z-BUGENDANA','Bugendana',(SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    ('GIT-Z-GITONGO',  'Gitongo',  (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    ('GIT-Z-MUGERA',   'Mugera',   (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    ('GIT-Z-MUTOYI',   'Mutoyi',   (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    ('GIT-Z-RWISABI',  'Rwisabi',  (SELECT id FROM commune WHERE code = 'GIT-CO-BUGENDANA')),
    -- Commune Bubanza
    ('BUJ-Z-BUBANZA',  'Bubanza',  (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-BUVYUKO',  'Buvyuko',  (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-KIVYUKA',  'Kivyuka',  (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-MITAKATAKA','Mitakataka',(SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-MURAMBA',  'Muramba',  (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-MUYEBE',   'Muyebe',   (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    ('BUJ-Z-NTAMBA',   'Ntamba',   (SELECT id FROM commune WHERE code = 'BUJ-CO-BUBANZA')),
    -- Commune Ngozi
    ('BUT-Z-BUHIGA',   'Buhiga',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-BUSIGA',   'Busiga',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-BUYE',     'Buye',     (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-GATSINDA', 'Gatsinda', (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-MAKABA',   'Makaba',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-MUBUGA',   'Mubuga',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-MUGOMERA', 'Mugomera', (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-MWUMBA',   'Mwumba',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-NGOZI',    'Ngozi',    (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-RUKECO',   'Rukeco',   (SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI')),
    ('BUT-Z-RWABIRIRO','Rwabiriro',(SELECT id FROM commune WHERE code = 'BUT-CO-NGOZI'))
ON CONFLICT (code) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 5. Collines / quartiers vérifiés
-- ---------------------------------------------------------------------------
UPDATE colline SET code = 'GIT-C-MUTAHO', nom = 'Mutaho',
       zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO') WHERE code = 'GIT-C-MUT';
UPDATE colline SET code = 'GIT-C-BITARE', nom = 'Bitare',
       zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE') WHERE code = 'GIT-C-BIS';
UPDATE colline SET code = 'GIT-C-GITONGO', nom = 'Gitongo',
       zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO') WHERE code = 'GIT-N-GIS';
UPDATE colline SET code = 'BUJ-C-MUSIGATI', nom = 'Musigati',
       zone_id = (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI') WHERE code = 'BUB-O-MUS';
UPDATE colline SET code = 'BUJ-C-BUHURIKA', nom = 'Buhurika',
       zone_id = (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI') WHERE code = 'BUB-O-RUG';
UPDATE colline SET code = 'BUT-C-MIVO', nom = 'Mivo',
       zone_id = (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO') WHERE code = 'NGO-C-MWE';

INSERT INTO colline (code, nom, zone_id) VALUES
    ('GIT-C-BUHORO',      'Buhoro',      (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')),
    ('GIT-C-KAGOMA',      'Kagoma',      (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')),
    ('GIT-C-KANYONGA',    'Kanyonga',    (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')),
    ('GIT-C-RUKOBE',      'Rukobe',      (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')),
    ('GIT-C-RUTEGAMA',    'Rutegama',    (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')),
    ('GIT-C-GIHAMAGARA',  'Gihamagara',  (SELECT id FROM zone WHERE code = 'GIT-Z-BUHINDA')),
    ('GIT-C-KIBOGOYE',    'Kibogoye',    (SELECT id FROM zone WHERE code = 'GIT-Z-BUHINDA')),
    ('GIT-C-KIRAMBI',     'Kirambi',     (SELECT id FROM zone WHERE code = 'GIT-Z-BUHINDA')),
    ('GIT-C-KIREMBA',     'Kiremba',     (SELECT id FROM zone WHERE code = 'GIT-Z-BUHINDA')),
    ('GIT-C-BIHORORO',    'Bihororo',    (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-GISURU',      'Gisuru',      (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-KIREMERA',    'Kiremera',    (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-KORANE',      'Korane',      (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-MUREMERA',    'Muremera',    (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-RUHANZA',     'Ruhanza',     (SELECT id FROM zone WHERE code = 'GIT-Z-GIHETA')),
    ('GIT-C-CARIRE',      'Carire',      (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')),
    ('GIT-C-GATERAMA',    'Gaterama',    (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')),
    ('GIT-C-KIBASI',      'Kibasi',      (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')),
    ('GIT-C-KIBUNGO',     'Kibungo',     (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')),
    ('GIT-C-RUNYERI',     'Runyeri',     (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')),
    ('GIT-C-BIGERA',      'Bigera',      (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO')),
    ('GIT-C-MUSHIKANWA',  'Mushikanwa',  (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO')),
    ('GIT-C-NYABISAKA',   'Nyabisaka',   (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO')),
    ('GIT-C-NYANGUNGU',   'Nyangungu',   (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO')),
    ('GIT-C-MASANGO',     'Masango',     (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO')),
    ('GIT-C-MURIRIMBO',   'Muririmbo',   (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO')),
    ('GIT-C-MUYANGE',     'Muyange',     (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO')),
    ('GIT-C-MUZENGA',     'Muzenga',     (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO')),
    ('GIT-C-NKONGWE',     'Nkongwe',     (SELECT id FROM zone WHERE code = 'GIT-Z-GITONGO')),
    ('BUJ-C-BUHORORO',    'Quartier Buhororo', (SELECT id FROM zone WHERE code = 'BUJ-Z-BUBANZA')),
    ('BUJ-C-GIKO',        'Quartier Giko',     (SELECT id FROM zone WHERE code = 'BUJ-Z-BUBANZA')),
    ('BUJ-C-MATONGE',     'Quartier Matonge',  (SELECT id FROM zone WHERE code = 'BUJ-Z-BUBANZA')),
    ('BUJ-C-RUVUMVU',     'Quartier Ruvumvu',  (SELECT id FROM zone WHERE code = 'BUJ-Z-BUBANZA')),
    ('BUJ-C-BUKINGA',     'Bukinga',     (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-DONDI',       'Dondi',       (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-KANAZI',      'Kanazi',      (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-KAYANGE',     'Kayange',     (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-MPISHI',      'Mpishi',      (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-MUGOMBARIMA', 'Mugombarima', (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-NYARUSANGE',  'Nyarusange',  (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')),
    ('BUJ-C-BUBENGA',     'Bubenga',     (SELECT id FROM zone WHERE code = 'BUJ-Z-MUYEBE')),
    ('BUJ-C-BUTAHA',      'Butaha',      (SELECT id FROM zone WHERE code = 'BUJ-Z-MUYEBE')),
    ('BUJ-C-MASARE',      'Masare',      (SELECT id FROM zone WHERE code = 'BUJ-Z-MUYEBE')),
    ('BUJ-C-MUGOMA',      'Mugoma',      (SELECT id FROM zone WHERE code = 'BUJ-Z-MUYEBE')),
    ('BUJ-C-RUVYIMVYA',   'Ruvyimvya',   (SELECT id FROM zone WHERE code = 'BUJ-Z-MUYEBE')),
    ('BUT-C-CIGUMIJE',    'Cigumije',    (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-GASEBEYI',    'Gasebeyi',    (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-GITWENZI',    'Gitwenzi',    (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-HINA',        'Hina',        (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-KAMBATI',     'Kambati',     (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-KIRURI',      'Kiruri',      (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-MIRANGO',     'Mirango',     (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-MWUNGERE',    'Mwungere',    (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')),
    ('BUT-C-BUSORO',      'Busoro',      (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-GAHWAZI',     'Gahwazi',     (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-GAKECERI',    'Gakeceri',    (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-KINYANA',     'Kinyana',     (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-MAKOMBE',     'Makombe',     (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-MASAMA',      'Masama',      (SELECT id FROM zone WHERE code = 'BUT-Z-BUHIGA')),
    ('BUT-C-CAMUGANI',    'Quartier Camugani', (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-GABIRO',      'Quartier Gabiro',   (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-GISAGARA',    'Quartier Gisagara', (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-KANYAMI',     'Quartier Kanyami',  (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-MUREMERA',    'Quartier Muremera', (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-RUBUYE',      'Quartier Rubuye',   (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-RUSUGUTI',    'Quartier Rusuguti', (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI')),
    ('BUT-C-SHIKIRO',     'Quartier Shikiro',  (SELECT id FROM zone WHERE code = 'BUT-Z-NGOZI'))
ON CONFLICT (code) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 6. Dépôts : seuls deux niveaux, libellés et rattachements corrigés
-- ---------------------------------------------------------------------------
UPDATE depot SET code = 'DEP-BUJ-P', nom = 'Dépôt logistique provincial Bujumbura',
       niveau = 'PROVINCE', province_id = (SELECT id FROM province WHERE code = 'BUJ'), zone_id = NULL
WHERE code = 'DEP-BUB-P';

UPDATE depot SET code = 'DEP-BUT-P', nom = 'Dépôt logistique provincial Butanyerera',
       niveau = 'PROVINCE', province_id = (SELECT id FROM province WHERE code = 'BUT'), zone_id = NULL
WHERE code = 'DEP-NGO-P';

UPDATE depot SET nom = 'Dépôt logistique provincial Gitega', niveau = 'PROVINCE',
       province_id = (SELECT id FROM province WHERE code = 'GIT'), zone_id = NULL
WHERE code = 'DEP-GIT-P';

UPDATE depot SET nom = 'Dépôt de distribution Buhevyi', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-BUHEVYI')
WHERE code = 'DEP-GIT-Z';

UPDATE depot SET code = 'DEP-BUJ-Z', nom = 'Dépôt de distribution Bubanza', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'BUJ-Z-BUBANZA')
WHERE code = 'DEP-BUB-Z';

UPDATE depot SET nom = 'Dépôt de distribution Mutaho', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-MUTAHO')
WHERE code = 'DEP-MUT';

UPDATE depot SET code = 'DEP-BIT', nom = 'Dépôt de distribution Bitare', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'GIT-Z-BITARE')
WHERE code = 'DEP-BIS';

UPDATE depot SET nom = 'Dépôt de distribution Musigati', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'BUJ-Z-MUSIGATI')
WHERE code = 'DEP-MUS';

UPDATE depot SET code = 'DEP-MIV', nom = 'Dépôt de distribution Mivo', niveau = 'ZONE',
       province_id = NULL, zone_id = (SELECT id FROM zone WHERE code = 'BUT-Z-MIVO')
WHERE code = 'DEP-MWE';

UPDATE depot SET est_demo = TRUE;

-- ---------------------------------------------------------------------------
-- 7. Gamme FOMI, conditionnement 25 kg et prix 2026
--    Les identifiants existants sont conservés pour ne pas casser les stocks,
--    lots, tickets et mouvements déjà enregistrés.
-- ---------------------------------------------------------------------------
UPDATE engrais_type
SET code = 'IMBURA',
    nom = 'FOMI-IMBURA (NPK 9-22-4 + 13CaO + 2MgO)',
    poids_sac_kg = 25.00,
    prix_subventionne = 31000.00,
    prix_a_confirmer = FALSE,
    actif = TRUE
WHERE code = 'UREE';

UPDATE engrais_type
SET code = 'TOTAHAZA',
    nom = 'FOMI-TOTAHAZA (NK 21-0-8 + 4CaO + 2MgO)',
    poids_sac_kg = 25.00,
    prix_subventionne = 33000.00,
    prix_a_confirmer = TRUE,
    actif = TRUE
WHERE code = 'NPK';

UPDATE engrais_type
SET code = 'BAGARA',
    nom = 'FOMI-BAGARA (NK 11-0-22 + 4CaO + 2MgO)',
    poids_sac_kg = 25.00,
    prix_subventionne = 28000.00,
    prix_a_confirmer = FALSE,
    actif = TRUE
WHERE code = 'DAP';

INSERT INTO engrais_type (code, nom, poids_sac_kg, prix_subventionne, prix_a_confirmer, actif) VALUES
    ('DOLOMIE', 'Dolomie / chaux agricole', 25.00, 2500.00, FALSE, TRUE)
ON CONFLICT (code) DO NOTHING;

-- Lots : seuls les numéros changent, les identifiants restent stables.
UPDATE lot SET numero_lot = 'LOT-IMBURA-2026-001'   WHERE numero_lot = 'LOT-UREE-2026-001';
UPDATE lot SET numero_lot = 'LOT-IMBURA-2026-002'   WHERE numero_lot = 'LOT-UREE-2026-002';
UPDATE lot SET numero_lot = 'LOT-TOTAHAZA-2026-001' WHERE numero_lot = 'LOT-NPK-2026-001';

INSERT INTO lot (numero_lot, engrais_type_id, quantite_initiale, date_fabrication, date_peremption, date_reception_fomi)
SELECT 'LOT-DOLOMIE-2026-001', id, 600, '2026-01-05', '2028-01-05', '2026-02-01'
FROM engrais_type WHERE code = 'DOLOMIE'
ON CONFLICT (numero_lot) DO NOTHING;

INSERT INTO stock (depot_id, engrais_type_id, quantite_disponible)
SELECT d.id, e.id, 120
FROM depot d, engrais_type e
WHERE d.code = 'DEP-GIT-P' AND e.code = 'DOLOMIE'
ON CONFLICT (depot_id, engrais_type_id) DO NOTHING;

INSERT INTO stock_lot (depot_id, lot_id, quantite)
SELECT d.id, l.id, 120
FROM depot d, lot l
WHERE d.code = 'DEP-GIT-P' AND l.numero_lot = 'LOT-DOLOMIE-2026-001'
ON CONFLICT (depot_id, lot_id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 8. Seuils par dépôt ET par produit (plus de seuil unique par dépôt)
-- ---------------------------------------------------------------------------
INSERT INTO seuil_alerte (depot_id, engrais_type_id, seuil_min, criticite)
SELECT d.id, e.id, v.seuil, v.criticite
FROM (VALUES
        ('DEP-GIT-P', 'IMBURA',   300, 'WARNING'),
        ('DEP-GIT-P', 'TOTAHAZA', 200, 'WARNING'),
        ('DEP-GIT-P', 'DOLOMIE',   50, 'INFO'),
        ('DEP-BUJ-P', 'IMBURA',   250, 'WARNING'),
        ('DEP-BUT-P', 'IMBURA',   150, 'CRITICAL'),
        ('DEP-GIT-Z', 'IMBURA',    80, 'WARNING'),
        ('DEP-MUT',   'IMBURA',    20, 'WARNING'),
        ('DEP-MUS',   'IMBURA',    20, 'WARNING')
     ) AS v(depot_code, engrais_code, seuil, criticite)
JOIN depot d ON d.code = v.depot_code
JOIN engrais_type e ON e.code = v.engrais_code
ON CONFLICT (depot_id, engrais_type_id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 9. Tickets de démonstration : produits, dépôts, montants et statuts
-- ---------------------------------------------------------------------------
UPDATE ticket SET engrais_type_id = (SELECT id FROM engrais_type WHERE code = 'IMBURA'),
       montant_paye = quantite_commandee * 31000.00
WHERE numero_ticket IN ('TKT-2026-1247', 'TKT-2026-1248', 'TKT-2026-1250', 'TKT-2026-1251');

UPDATE ticket SET engrais_type_id = (SELECT id FROM engrais_type WHERE code = 'TOTAHAZA'),
       montant_paye = quantite_commandee * 33000.00,
       depot_retrait_id = (SELECT id FROM depot WHERE code = 'DEP-BIT')
WHERE numero_ticket = 'TKT-2026-1249';

UPDATE ticket SET depot_retrait_id = (SELECT id FROM depot WHERE code = 'DEP-MIV')
WHERE numero_ticket = 'TKT-2026-1251';

-- La réclamation n'est plus un statut de ticket : elle devient une entité liée.
UPDATE ticket SET statut = 'PAYE'
WHERE numero_ticket = 'TKT-2026-1250';

UPDATE ticket SET est_demo = TRUE WHERE numero_ticket LIKE 'TKT-2026-%';

-- Purge des artefacts de test / d'e-mail (y compris leurs dépendances).
DELETE FROM distribution
WHERE ticket_id IN (SELECT id FROM ticket
                    WHERE numero_ticket LIKE 'TKT-E2E-%' OR numero_ticket = 'TKT-MAIL-DEMO-1');

DELETE FROM mouvement
WHERE ticket_id IN (SELECT id FROM ticket
                    WHERE numero_ticket LIKE 'TKT-E2E-%' OR numero_ticket = 'TKT-MAIL-DEMO-1');

DELETE FROM ticket
WHERE numero_ticket LIKE 'TKT-E2E-%' OR numero_ticket = 'TKT-MAIL-DEMO-1';

-- Message d'alerte encore rédigé avec l'ancien vocabulaire.
UPDATE alerte
SET message = 'Stock FOMI-IMBURA épuisé au dépôt logistique provincial Butanyerera'
WHERE type = 'RUPTURE'
  AND depot_id = (SELECT id FROM depot WHERE code = 'DEP-BUT-P');

UPDATE alerte
SET message = 'Demande non servie (3 sacs de 25 kg) proche du stock disponible (80 sacs) au dépôt de distribution Mutaho'
WHERE type = 'DEMANDE_SUP_STOCK'
  AND depot_id = (SELECT id FROM depot WHERE code = 'DEP-MUT');

-- ---------------------------------------------------------------------------
-- 10. Agriculteurs : suppression des « Nom1 Prenom1 »
--     500 lignes, 30 noms × 30 prénoms = 900 combinaisons possibles.
-- ---------------------------------------------------------------------------
WITH n AS (
    SELECT id, row_number() OVER (ORDER BY id) - 1 AS rn
    FROM agriculteur
    WHERE nom ~ '^Nom[0-9]+$'
), a AS (
    SELECT
        ARRAY['Niyonzima','Irakoze','Uwimana','Habonimana','Nahimana',
              'Ntahomvukiye','Niyibigira','Ndihokubwayo','Nduwimana','Ntakirutimana',
              'Mukeshimana','Nzeyimana','Ntirampeba','Nibigira','Kamariza',
              'Hakizimana','Ndayikengurukiye','Bukuru','Ndikumana','Manirakiza',
              'Sindayigaya','Nsabimana','Barakamfitiye','Niyongabo','Nkunzimana',
              'Ndayisenga','Bigirimana','Ruvubi','Havugimana','Ndabaneze'] AS noms,
        ARRAY['Espérance','Léonidas','Consolate','Aimé','Générose',
              'Théogène','Francine','Prosper','Claudine','Gervais',
              'Odette','Pascal','Adélaïde','Désiré','Béatrice',
              'Cyprien','Euphrasie','Eliakim','Pélagie','Épaphrodite',
              'Joselyne','Fabrice','Domitille','Samuel','Rose',
              'Dieudonné','Immaculée','Térence','Jeanne','Révérien'] AS prenoms
)
UPDATE agriculteur ag
SET nom = a.noms[1 + (n.rn % 30)],
    prenom = a.prenoms[1 + ((n.rn / 30) % 30)],
    est_demo = TRUE
FROM n, a
WHERE ag.id = n.id;

UPDATE agriculteur SET est_demo = TRUE WHERE est_demo = FALSE;

-- ---------------------------------------------------------------------------
-- 11. Réclamation : entité séparée du ticket
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reclamation (
    id                  BIGSERIAL PRIMARY KEY,
    ticket_id           BIGINT       NOT NULL REFERENCES ticket(id),
    motif               VARCHAR(200) NOT NULL,
    description         VARCHAR(1000),
    quantite_manquante  INTEGER      CHECK (quantite_manquante >= 0),
    statut              VARCHAR(20)  NOT NULL DEFAULT 'OUVERTE'
                        CHECK (statut IN ('OUVERTE', 'EN_INSTRUCTION', 'RESOLUE', 'REJETEE')),
    resolution          VARCHAR(1000),
    date_creation       TIMESTAMP    NOT NULL DEFAULT NOW(),
    date_resolution     TIMESTAMP,
    est_demo            BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_reclamation_ticket ON reclamation(ticket_id);
CREATE INDEX IF NOT EXISTS idx_reclamation_statut ON reclamation(statut);

INSERT INTO reclamation (ticket_id, motif, description, quantite_manquante, statut, date_creation, est_demo)
SELECT t.id,
       'Engrais payé non retiré',
       'Ticket payé le 01/11/2025, aucun sac retiré au dépôt. Réclamation de démonstration.',
       t.quantite_commandee - t.quantite_servie,
       'OUVERTE',
       '2025-11-05 09:00:00',
       TRUE
FROM ticket t
WHERE t.numero_ticket = 'TKT-2026-1250'
  AND NOT EXISTS (SELECT 1 FROM reclamation r WHERE r.ticket_id = t.id);
