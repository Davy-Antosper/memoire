-- Données de démonstration : lots, stocks, agriculteurs, tickets
INSERT INTO lot (numero_lot, engrais_type_id, quantite_initiale, date_fabrication, date_peremption, date_reception_fomi) VALUES
    ('LOT-UREE-2026-001', (SELECT id FROM engrais_type WHERE code = 'UREE'), 5000, '2026-01-15', '2027-01-15', '2026-02-01'),
    ('LOT-UREE-2026-002', (SELECT id FROM engrais_type WHERE code = 'UREE'), 3000, '2026-02-01', '2027-02-01', '2026-02-15'),
    ('LOT-NPK-2026-001',  (SELECT id FROM engrais_type WHERE code = 'NPK'),  2000, '2026-01-20', '2027-01-20', '2026-02-05');

-- Stocks provinciaux Gitega (1500 sacs urée) et Ngozi (0 - rupture)
INSERT INTO stock (depot_id, engrais_type_id, quantite_disponible) VALUES
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-P'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 1500),
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-P'), (SELECT id FROM engrais_type WHERE code = 'NPK'),  800),
    ((SELECT id FROM depot WHERE code = 'DEP-BUB-P'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 1200),
    ((SELECT id FROM depot WHERE code = 'DEP-NGO-P'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 0),
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-Z'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 400),
    ((SELECT id FROM depot WHERE code = 'DEP-MUT'),   (SELECT id FROM engrais_type WHERE code = 'UREE'), 80),
    ((SELECT id FROM depot WHERE code = 'DEP-MUS'),   (SELECT id FROM engrais_type WHERE code = 'UREE'), 40);

INSERT INTO stock_lot (depot_id, lot_id, quantite) VALUES
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-P'), (SELECT id FROM lot WHERE numero_lot = 'LOT-UREE-2026-001'), 1500),
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-P'), (SELECT id FROM lot WHERE numero_lot = 'LOT-NPK-2026-001'),  800),
    ((SELECT id FROM depot WHERE code = 'DEP-BUB-P'), (SELECT id FROM lot WHERE numero_lot = 'LOT-UREE-2026-001'), 1200),
    ((SELECT id FROM depot WHERE code = 'DEP-GIT-Z'), (SELECT id FROM lot WHERE numero_lot = 'LOT-UREE-2026-002'), 400),
    ((SELECT id FROM depot WHERE code = 'DEP-MUT'),   (SELECT id FROM lot WHERE numero_lot = 'LOT-UREE-2026-002'), 80),
    ((SELECT id FROM depot WHERE code = 'DEP-MUS'),   (SELECT id FROM lot WHERE numero_lot = 'LOT-UREE-2026-001'), 40);

-- Agriculteurs (échantillon)
INSERT INTO agriculteur (numero_identite, nom, prenom, telephone, colline_id) VALUES
    ('AGR-001', 'Ndayisaba',  'Jean',    '79000001', (SELECT id FROM colline WHERE code = 'GIT-C-MUT')),
    ('AGR-002', 'Niyonkuru',  'Marie',   '79000002', (SELECT id FROM colline WHERE code = 'GIT-C-MUT')),
    ('AGR-003', 'Havyarimana','Pierre',  '79000003', (SELECT id FROM colline WHERE code = 'GIT-C-BIS')),
    ('AGR-004', 'Nshimirimana','Alice',  '79000004', (SELECT id FROM colline WHERE code = 'BUB-O-MUS')),
    ('AGR-005', 'Bizimana',   'Emmanuel','79000005', (SELECT id FROM colline WHERE code = 'NGO-C-MWE'));

-- Tickets
INSERT INTO ticket (numero_ticket, agriculteur_id, engrais_type_id, quantite_commandee, quantite_servie, montant_paye, date_paiement, depot_retrait_id, statut) VALUES
    ('TKT-2026-1247', (SELECT id FROM agriculteur WHERE numero_identite = 'AGR-001'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 5, 3, 125000.00, '2026-01-10', (SELECT id FROM depot WHERE code = 'DEP-MUT'), 'PARTIEL'),
    ('TKT-2026-1248', (SELECT id FROM agriculteur WHERE numero_identite = 'AGR-002'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 3, 0,  75000.00,  '2026-01-15', (SELECT id FROM depot WHERE code = 'DEP-MUT'), 'EN_ATTENTE'),
    ('TKT-2026-1249', (SELECT id FROM agriculteur WHERE numero_identite = 'AGR-003'), (SELECT id FROM engrais_type WHERE code = 'NPK'),  2, 2,  60000.00,  '2026-01-20', (SELECT id FROM depot WHERE code = 'DEP-BIS'), 'SERVI'),
    ('TKT-2026-1250', (SELECT id FROM agriculteur WHERE numero_identite = 'AGR-004'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 4, 0,  100000.00, '2025-11-01', (SELECT id FROM depot WHERE code = 'DEP-MUS'), 'RECLAMATION'),
    ('TKT-2026-1251', (SELECT id FROM agriculteur WHERE numero_identite = 'AGR-005'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 6, 0,  150000.00, '2026-02-01', (SELECT id FROM depot WHERE code = 'DEP-MWE'), 'PAYE');

-- Alertes initiales
INSERT INTO alerte (depot_id, engrais_type_id, type, message, niveau) VALUES
    ((SELECT id FROM depot WHERE code = 'DEP-NGO-P'), (SELECT id FROM engrais_type WHERE code = 'UREE'), 'RUPTURE', 'Stock urée épuisé au dépôt provincial Ngozi', 'CRITICAL'),
    ((SELECT id FROM depot WHERE code = 'DEP-MUT'),   (SELECT id FROM engrais_type WHERE code = 'UREE'), 'DEMANDE_SUP_STOCK', 'Demande tickets non servis (3 sacs) proche du stock disponible (80 sacs)', 'INFO');
