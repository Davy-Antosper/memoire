import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Text, Card, Chip } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get } from '../api/client';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

const ACTION_COLORS = {
  CREATE: '#15803d',
  UPDATE: '#2563eb',
  DELETE: '#dc2626',
  LOGIN: '#7c3aed',
  LOGOUT: '#6b7280',
};

export default function AuditLogsScreen() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchLogs = async () => {
    try {
      const res = await get('/api/audit-logs', { params: { page: 0, size: 50 } });
      const data = res.data;
      setLogs(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchLogs();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchLogs();
    setRefreshing(false);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try { return new Date(dateStr).toLocaleString('fr-BI'); } catch { return dateStr; }
  };

  if (loading) return <LoadingScreen />;

  return (
    <FlatList
      data={logs}
      keyExtractor={(item) => String(item.id)}
      renderItem={({ item }) => (
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.header}>
              <Chip
                compact
                style={[styles.actionChip, { backgroundColor: (ACTION_COLORS[item.action] || COLORS.muted) + '20' }]}
                textStyle={{ color: ACTION_COLORS[item.action] || COLORS.muted, fontSize: 11 }}
              >
                {item.action}
              </Chip>
              <Text style={styles.entity}>{item.entityType} #{item.entityId || ''}</Text>
            </View>
            <View style={styles.details}>
              <MaterialCommunityIcons name="account" size={14} color={COLORS.muted} />
              <Text style={styles.user}>{item.username || item.utilisateurNom || 'Système'}</Text>
            </View>
            <Text style={styles.date}>{formatDate(item.dateAction)}</Text>
            {item.ipAddress && <Text style={styles.ip}>IP: {item.ipAddress}</Text>}
          </Card.Content>
        </Card>
      )}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
      ListEmptyComponent={<EmptyState icon="history" message="Aucun journal d'audit" />}
      contentContainerStyle={logs.length === 0 ? styles.emptyList : styles.list}
    />
  );
}

const styles = StyleSheet.create({
  list: { padding: 8 },
  emptyList: { flex: 1 },
  card: { marginBottom: 8, backgroundColor: COLORS.card },
  header: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 6 },
  actionChip: { height: 24 },
  entity: { color: COLORS.text, fontWeight: '500', flex: 1 },
  details: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  user: { color: COLORS.muted, fontSize: 13 },
  date: { color: COLORS.muted, fontSize: 12, marginTop: 4 },
  ip: { color: COLORS.muted, fontSize: 11, marginTop: 2 },
});
