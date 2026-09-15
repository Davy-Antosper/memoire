-- Lot A : réinitialise les mots de passe des comptes de démonstration sur "password"
-- (les hashes en base ne correspondaient plus au seed pour certains environnements)
UPDATE utilisateur
SET password_hash = '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG'
WHERE username IN ('admin', 'superviseur', 'agent.zone', 'agent.colline', 'agent.fomi');
