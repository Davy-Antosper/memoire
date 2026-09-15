-- Seed volumineux : 500 agriculteurs répartis sur les 6 collines + index telephone (futur SMS)

CREATE INDEX idx_agriculteur_telephone ON agriculteur(telephone);

INSERT INTO agriculteur (numero_identite, nom, prenom, telephone, colline_id)
SELECT 'AGR-' || LPAD((6 + gs)::text, 6, '0'),
       'Nom' || gs,
       'Prenom' || gs,
       '78' || LPAD(gs::text, 8, '0'),
       (SELECT id FROM colline ORDER BY id OFFSET (gs % 6) LIMIT 1)
FROM generate_series(1, 500) AS gs;
