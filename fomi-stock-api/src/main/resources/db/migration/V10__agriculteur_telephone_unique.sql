-- Règle R14 : un agriculteur ne peut être enregistré qu'une seule fois avec un numéro de téléphone unique.
-- Les téléphones des seeds sont uniques (V3: 79xxxxxx, V4/V6: 78xxxxxx) ; les valeurs NULL restent autorisées.

CREATE UNIQUE INDEX uniq_agriculteur_telephone ON agriculteur(telephone);
