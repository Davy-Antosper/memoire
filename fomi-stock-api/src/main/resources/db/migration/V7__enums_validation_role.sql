-- Lot A : validation des tickets par le SUPERVISEUR + rôle AGENT_LOGISTIQUE (FOMI)
-- Étend les enums PostgreSQL existants (ADD VALUE, idempotent via DO)

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'EN_ATTENTE_DE_VALIDATION' AND enumtypid = 'statut_ticket'::regtype) THEN
        ALTER TYPE statut_ticket ADD VALUE 'EN_ATTENTE_DE_VALIDATION' AFTER 'EN_ATTENTE';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'ACTIF' AND enumtypid = 'statut_ticket'::regtype) THEN
        ALTER TYPE statut_ticket ADD VALUE 'ACTIF' AFTER 'EN_ATTENTE_DE_VALIDATION';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'REJETE' AND enumtypid = 'statut_ticket'::regtype) THEN
        ALTER TYPE statut_ticket ADD VALUE 'REJETE';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'EXPIRE' AND enumtypid = 'statut_ticket'::regtype) THEN
        ALTER TYPE statut_ticket ADD VALUE 'EXPIRE';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'AGENT_LOGISTIQUE' AND enumtypid = 'role_utilisateur'::regtype) THEN
        ALTER TYPE role_utilisateur ADD VALUE 'AGENT_LOGISTIQUE';
    END IF;
END $$;
