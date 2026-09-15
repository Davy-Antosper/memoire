import React from 'react';
import { Badge } from 'react-native-paper';
import { COLORS, STATUT_COLORS, ALERTE_NIVEAU_COLORS, MOUVEMENT_TYPE_COLORS } from '../theme';

const STATUS_LABELS = {
  PAYE: 'Payé',
  EN_ATTENTE_DE_VALIDATION: 'En attente',
  ACTIF: 'Actif',
  PARTIEL: 'Partiel',
  SERVI: 'Servi',
  REJETE: 'Rejeté',
  ANNULE: 'Annulé',
};

const NIVEAU_LABELS = {
  INFO: 'Info',
  WARNING: 'Alerte',
  CRITIQUE: 'Critique',
  HAUTE: 'Haute',
  MOYENNE: 'Moyenne',
  BASSE: 'Basse',
};

const TYPE_LABELS = {
  RECEPTION_FOMI: 'Réception',
  TRANSFERT: 'Transfert',
  DISTRIBUTION: 'Distribution',
};

export default function StatusBadge({ status, niveau, type, style }) {
  if (status) {
    const color = STATUT_COLORS[status] || COLORS.muted;
    const label = STATUS_LABELS[status] || status;
    return (
      <Badge
        style={[{ backgroundColor: color }, styles.badge, style]}
        textStyle={styles.badgeText}
      >
        {label}
      </Badge>
    );
  }

  if (niveau) {
    const color = ALERTE_NIVEAU_COLORS[niveau] || COLORS.muted;
    const label = NIVEAU_LABELS[niveau] || niveau;
    return (
      <Badge
        style={[{ backgroundColor: color }, styles.badge, style]}
        textStyle={styles.badgeText}
      >
        {label}
      </Badge>
    );
  }

  if (type) {
    const color = MOUVEMENT_TYPE_COLORS[type] || COLORS.muted;
    const label = TYPE_LABELS[type] || type;
    return (
      <Badge
        style={[{ backgroundColor: color }, styles.badge, style]}
        textStyle={styles.badgeText}
      >
        {label}
      </Badge>
    );
  }

  return null;
}

const styles = StyleSheet.create({
  badge: {
    alignSelf: 'flex-start',
  },
  badgeText: {
    color: COLORS.white,
    fontSize: 11,
  },
});
