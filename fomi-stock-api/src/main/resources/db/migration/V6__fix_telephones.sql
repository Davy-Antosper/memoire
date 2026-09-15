-- Correction : les téléphones générés en V4 faisaient 9 chiffres (78 + 8 chiffres).
-- On les ramène à 8 chiffres (78 + 6 chiffres).
UPDATE agriculteur
SET telephone = '78' || LPAD(CAST(SUBSTRING(telephone, 3) AS BIGINT)::text, 6, '0')
WHERE telephone LIKE '78%';
