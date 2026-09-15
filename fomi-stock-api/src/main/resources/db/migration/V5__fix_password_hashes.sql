-- Correction : les hashes bcrypt du seed V2 étaient invalides.
-- On réinitialise le mot de passe de tous les utilisateurs de démo sur "password".
UPDATE utilisateur
SET password_hash = '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG'
WHERE username IN ('admin', 'agent.zone', 'agent.colline', 'superviseur');
