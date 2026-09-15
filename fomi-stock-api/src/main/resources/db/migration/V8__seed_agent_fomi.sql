-- Utilisateur de démonstration : agent logistique FOMI (mot de passe "password")
INSERT INTO utilisateur (username, password_hash, nom_complet, role)
SELECT 'agent.fomi', '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG', 'Agent logistique FOMI', 'AGENT_LOGISTIQUE'
WHERE NOT EXISTS (SELECT 1 FROM utilisateur WHERE username = 'agent.fomi');
