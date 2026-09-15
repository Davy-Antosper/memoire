-- Provinces du Burundi (MVP demo)
INSERT INTO province (code, nom) VALUES
    ('GIT', 'Gitega'),
    ('BUB', 'Bubanza'),
    ('NGO', 'Ngozi');

-- Zones
INSERT INTO zone (code, nom, province_id) VALUES
    ('GIT-C', 'Gitega Centre', (SELECT id FROM province WHERE code = 'GIT')),
    ('GIT-N', 'Gitega Nord',   (SELECT id FROM province WHERE code = 'GIT')),
    ('BUB-O', 'Bubanza Ouest', (SELECT id FROM province WHERE code = 'BUB')),
    ('NGO-C', 'Ngozi Centre',  (SELECT id FROM province WHERE code = 'NGO'));

-- Collines
INSERT INTO colline (code, nom, zone_id) VALUES
    ('GIT-C-MUT', 'Mutaho',      (SELECT id FROM zone WHERE code = 'GIT-C')),
    ('GIT-C-BIS', 'Bisoro',      (SELECT id FROM zone WHERE code = 'GIT-C')),
    ('GIT-N-GIS', 'Gisozi',      (SELECT id FROM zone WHERE code = 'GIT-N')),
    ('BUB-O-MUS', 'Musigati',    (SELECT id FROM zone WHERE code = 'BUB-O')),
    ('BUB-O-RUG', 'Rugazi',      (SELECT id FROM zone WHERE code = 'BUB-O')),
    ('NGO-C-MWE', 'Mwendo',      (SELECT id FROM zone WHERE code = 'NGO-C'));

-- Types d'engrais
INSERT INTO engrais_type (code, nom, poids_sac_kg, prix_subventionne) VALUES
    ('UREE', 'Urée',           50.00, 25000.00),
    ('NPK',  'NPK 17-17-17',   50.00, 30000.00),
    ('DAP',  'DAP',            50.00, 35000.00);

-- Dépôts
INSERT INTO depot (code, nom, niveau, province_id, zone_id, colline_id, seuil_alerte_min) VALUES
    ('DEP-GIT-P', 'Dépôt Provincial Gitega',   'PROVINCE', (SELECT id FROM province WHERE code = 'GIT'), NULL, NULL, 500),
    ('DEP-BUB-P', 'Dépôt Provincial Bubanza',  'PROVINCE', (SELECT id FROM province WHERE code = 'BUB'), NULL, NULL, 300),
    ('DEP-NGO-P', 'Dépôt Provincial Ngozi',    'PROVINCE', (SELECT id FROM province WHERE code = 'NGO'), NULL, NULL, 200),
    ('DEP-GIT-Z', 'Dépôt Zone Gitega Centre',  'ZONE',     NULL, (SELECT id FROM zone WHERE code = 'GIT-C'), NULL, 200),
    ('DEP-BUB-Z', 'Dépôt Zone Bubanza Ouest',  'ZONE',     NULL, (SELECT id FROM zone WHERE code = 'BUB-O'), NULL, 150),
    ('DEP-MUT',   'Dépôt Colline Mutaho',      'COLLINE',  NULL, NULL, (SELECT id FROM colline WHERE code = 'GIT-C-MUT'), 50),
    ('DEP-BIS',   'Dépôt Colline Bisoro',      'COLLINE',  NULL, NULL, (SELECT id FROM colline WHERE code = 'GIT-C-BIS'), 50),
    ('DEP-MUS',   'Dépôt Colline Musigati',    'COLLINE',  NULL, NULL, (SELECT id FROM colline WHERE code = 'BUB-O-MUS'), 50),
    ('DEP-MWE',   'Dépôt Colline Mwendo',      'COLLINE',  NULL, NULL, (SELECT id FROM colline WHERE code = 'NGO-C-MWE'), 50);

-- Utilisateurs (mot de passe: password)
INSERT INTO utilisateur (username, password_hash, nom_complet, role, depot_id, zone_id, province_id) VALUES
    ('admin',         '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Administrateur FOMI',      'ADMIN',         NULL, NULL, NULL),
    ('agent.zone',    '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Agent Zone Gitega',        'AGENT_ZONE',    NULL, (SELECT id FROM zone WHERE code = 'GIT-C'), NULL),
    ('agent.colline', '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Agent Colline Mutaho',     'AGENT_COLLINE', (SELECT id FROM depot WHERE code = 'DEP-MUT'), NULL, NULL),
    ('superviseur',   '$2a$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Superviseur Ministère',    'SUPERVISEUR',   NULL, NULL, NULL);
