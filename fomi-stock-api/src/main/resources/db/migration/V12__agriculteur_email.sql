-- Notifications email des agriculteurs : adresse de contact
ALTER TABLE agriculteur ADD COLUMN IF NOT EXISTS email VARCHAR(150);

-- Un email ne peut être rattaché qu'à un seul agriculteur (les NULL restent autorisés)
CREATE UNIQUE INDEX IF NOT EXISTS idx_agriculteur_email
    ON agriculteur (LOWER(email))
    WHERE email IS NOT NULL;

-- Adresses de démonstration (domaine réservé, aucun envoi réel sans configuration SMTP)
UPDATE agriculteur SET email = 'jean.ndayisaba@example.bi' WHERE numero_identite = 'AGR-001';
UPDATE agriculteur SET email = 'marie.niyonkuru@example.bi' WHERE numero_identite = 'AGR-002';
UPDATE agriculteur SET email = 'pierre.havyarimana@example.bi' WHERE numero_identite = 'AGR-003';
UPDATE agriculteur SET email = 'alice.nshimirimana@example.bi' WHERE numero_identite = 'AGR-004';
UPDATE agriculteur SET email = 'emmanuel.bizimana@example.bi' WHERE numero_identite = 'AGR-005';
