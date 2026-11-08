-- V18 : statut ARRIERE pour les tickets non servis reportés à la saison suivante.
--
-- À la clôture d'une saison, un ticket payé mais non entièrement servi était
-- auparavant marqué EXPIRE (« expiré »), ce qui laissait croire que le droit de
-- l'agriculteur était perdu. Or la pratique observée est tout autre : le
-- reliquat devient un arriéré, reporté et servi lors de la saison suivante, ou
-- remboursé sur décision du ministère.
--
-- Un nouveau statut ARRIERE distingue donc :
--   * EXPIRE  : la saison est clôturée et le ticket est clos sans suite ;
--   * ARRIERE : la saison est clôturée mais le reliquat reste dû à l'agriculteur.
--
-- PostgreSQL n'autorise pas le retrait d'une valeur d'énumération : on ajoute
-- simplement la nouvelle valeur, qui coexiste avec les précédentes.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_enum
        WHERE enumlabel = 'ARRIERE'
          AND enumtypid = 'statut_ticket'::regtype
    ) THEN
        ALTER TYPE statut_ticket ADD VALUE 'ARRIERE';
    END IF;
END $$;