-- V15 : nettoyage du statut RECLAMATION côté données.
--
-- Le statut RECLAMATION disparaît de l'énumération Java : depuis V14, une
-- réclamation est une entité à part entière (table `reclamation`), liée au
-- ticket par `reclamation.ticket_id`.
--
-- Une valeur d'énumération PostgreSQL ne peut pas être retirée simplement
-- (aucun DROP VALUE n'existe). On se contente donc de garantir qu'aucune
-- ligne ne porte encore ce statut, afin qu'Hibernate ne tombe jamais sur une
-- valeur inconnue de l'énumération Java.
--
-- Migration idempotente : si aucune ligne ne porte RECLAMATION, elle ne fait rien.

-- Aucune quantité servie : le ticket repart en attente de traitement.
UPDATE ticket
SET statut = 'PAYE',
    updated_at = NOW()
WHERE statut = 'RECLAMATION'
  AND quantite_servie = 0;

-- Servi partiellement : le reliquat reste dû.
UPDATE ticket
SET statut = 'PARTIEL',
    updated_at = NOW()
WHERE statut = 'RECLAMATION'
  AND quantite_servie > 0
  AND quantite_servie < quantite_commandee;

-- Entièrement servi.
UPDATE ticket
SET statut = 'SERVI',
    updated_at = NOW()
WHERE statut = 'RECLAMATION'
  AND quantite_servie >= quantite_commandee;

-- Contrôle attendu après migration : 0 ligne.
-- SELECT count(*) FROM ticket WHERE statut = 'RECLAMATION';
