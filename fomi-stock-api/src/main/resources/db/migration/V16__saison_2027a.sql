-- V16 : saison culturale courante 2027A.
--
-- Le ministère nomme une saison par l'année de sa récolte : « 2027 A » désigne
-- la saison A démarrée en septembre-octobre 2026. La valeur par défaut de
-- ticket.saison passe donc de 2026A à 2027A.
--
-- Aucune donnée historique n'est modifiée : seules les futures insertions qui
-- omettent la saison utilisent le nouveau défaut. Les tickets déjà enregistrés
-- conservent leur saison d'origine.

ALTER TABLE ticket ALTER COLUMN saison SET DEFAULT '2027A';