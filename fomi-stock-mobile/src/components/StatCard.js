import React from 'react';
import { StyleSheet } from 'react-native';
import { Card, Text } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { COLORS } from '../theme';

export default function StatCard({ icon, value, label, color = COLORS.primary }) {
  return (
    <Card style={styles.card}>
      <Card.Content style={styles.content}>
        <MaterialCommunityIcons name={icon} size={28} color={color} />
        <Text style={[styles.value, { color }]}>{value}</Text>
        <Text style={styles.label}>{label}</Text>
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    flex: 1,
    margin: 4,
    backgroundColor: COLORS.card,
  },
  content: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  value: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 4,
  },
  label: {
    fontSize: 12,
    color: COLORS.muted,
    marginTop: 2,
    textAlign: 'center',
  },
});
