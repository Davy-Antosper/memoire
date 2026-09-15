import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { COLORS } from '../theme';

export default function EmptyState({ icon = 'folder-open-outline', message = 'Aucune donnée' }) {
  return (
    <View style={styles.container}>
      <MaterialCommunityIcons name={icon} size={64} color={COLORS.border} />
      <Text style={styles.text}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  text: {
    marginTop: 12,
    fontSize: 16,
    color: COLORS.muted,
    textAlign: 'center',
  },
});
