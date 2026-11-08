-- V17 : FOMI-Totahaza est remplacé par l'urée, sans perdre les données liées.
--
-- Le ministère de l'Environnement, de l'Agriculture et de l'Élevage a demandé à
-- la FOMI de ne plus transformer l'urée en FOMI-Totahaza : la formulation
-- organo-minérale était contestée par les agriculteurs. Les communiqués de prix
-- publiés ensuite ne mentionnent plus que FOMI-Imbura, l'urée, FOMI-Bagara et
-- la dolomie ; le tarif agriculteur de l'urée est de 33 000 BIF par sac de
-- 25 kg, soit le même montant que celui qui était appliqué à Totahaza.
--
-- Le code technique TOTAHAZA est donc renommé UREE. Les identifiants, les
-- stocks, les lots, les tickets et les mouvements existants sont conservés :
-- seule l'étiquette du produit change.

-- 1. Le produit : TOTAHAZA devient UREE.
--    Le renommage n'est tenté que si la cible est libre, pour rester rejouable.
UPDATE engrais_type
SET code = 'UREE',
    nom = 'Urée (46 % N)',
    poids_sac_kg = 25.00,
    prix_subventionne = 33000.00,
    prix_a_confirmer = FALSE,
    actif = TRUE
WHERE code = 'TOTAHAZA'
  AND NOT EXISTS (SELECT 1 FROM engrais_type WHERE code = 'UREE');

-- 2. Les numéros de lot suivent, pour rester lisibles.
UPDATE lot
SET numero_lot = 'LOT-UREE-2026-001'
WHERE numero_lot = 'LOT-TOTAHAZA-2026-001'
  AND NOT EXISTS (SELECT 1 FROM lot WHERE numero_lot = 'LOT-UREE-2026-001');

-- 3. Les seuils et les tickets pointent déjà sur l'identifiant du produit :
--    aucune clé étrangère à réécrire.

-- Contrôle attendu : une ligne UREE, aucune ligne TOTAHAZA.
-- SELECT code, nom, poids_sac_kg, prix_subventionne FROM engrais_type ORDER BY code;