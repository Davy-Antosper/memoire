import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Text, Card, Button, Chip } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get, patch } from '../api/client';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/StatusBadge';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS, ALERTE_NIVEAU_COLORS } from '../theme';

const FILTERS = [
  { key: 'ALL', label: 'Tous' },
  { key: 'UNREAD', label: 'Non traitées' },
  { key: 'READ', label: 'Traitées' },
];

export default function AlertesScreen() {
  const { canManageAlertes } = useAuth();
  const [alertes, setAlertes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState('ALL');

  const fetchAlertes = async () => {
    try {
      const params = filter === 'UNREAD' ? { nonTraitees: true } : {};
      const res = await get('/api/alertes', { params });
      const data = res.data;
      setAlertes(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchAlertes();
    }, [filter])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchAlertes();
    setRefreshing(false);
  };

  const handleTraiter = async (id) => {
    try {
      await patch(`/api/alertes/${id}/traiter`);
      setAlertes((prev) => prev.filter((a) => a.id !== id));
    } catch (e) {}
  };

  const getIconName = (type) => {
    if (type?.includes('RUPTURE') || type?.includes('STOCK')) return 'alert-circle';
    if (type?.includes('PEREMPTION')) return 'clock-alert';
    if (type?.includes('SEUIL')) return 'chart-line';
    return 'bell';
  };

  const getFilteredAlertes = () => {
    if (filter === 'UNREAD') return alertes.filter((a) => !a.traiter);
    if (filter === 'READ') return alertes.filter((a) => a.traiter);
    return alertes;
  };

  if (loading) return <LoadingScreen />;

  const filteredAlertes = getFilteredAlertes();

  return (
    <View style={styles.container}>
      <View style={styles.filterRow}>
        {FILTERS.map((f) => (
          <Chip
            key={f.key}
            selected={filter === f.key}
            onPress={() => setFilter(f.key)}
            style={[styles.chip, filter === f.key && styles.chipSelected]}
            textStyle={filter === f.key ? styles.chipTextSelected : {}}
          >
            {f.label}
          </Chip>
        ))}
      </View>

      <FlatList
        data={filteredAlertes}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.alertCard}>
            <Card.Content>
              <View style={styles.alertHeader}>
                <MaterialCommunityIcons
                  name={getIconName(item.type)}
                  size={24}
                  color={ALERTE_NIVEAU_COLORS[item.niveau] || COLORS.warning}
                />
                <View style={styles.alertInfo}>
                  <Text style={styles.alertDepot}>{item.depotNom || item.depot?.nom || 'Dépôt'}</Text>
                  <StatusBadge niveau={item.niveau} />
                </View>
              </View>
              <Text style={styles.alertMessage}>{item.message || item.description || 'Alerte'}</Text>
              {item.dateCreation && (
                <Text style={styles.alertDate}>
                  {new Date(item.dateCreation).toLocaleDateString('fr-BI')}
                </Text>
              )}
              {canManageAlertes && !item.traitee && (
                <Button
                  mode="outlined"
                  compact
                  onPress={() => handleTraiter(item.id)}
                  style={styles.traiterBtn}
                >
                  Traiter
                </Button>
              )}
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="bell-off" message="Aucune alerte" />}
        contentContainerStyle={filteredAlertes.length === 0 ? styles.emptyList : styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  filterRow: { flexDirection: 'row', paddingHorizontal: 8, paddingVertical: 8, gap: 6 },
  chip: { marginRight: 4 },
  chipSelected: { backgroundColor: COLORS.primary },
  chipTextSelected: { color: COLORS.white },
  list: { padding: 8 },
  emptyList: { flex: 1 },
  alertCard: { marginBottom: 8, backgroundColor: COLORS.card },
  alertHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  alertInfo: { flex: 1 },
  alertDepot: { fontWeight: '600', color: COLORS.text },
  alertMessage: { color: COLORS.muted, marginTop: 8, fontSize: 14 },
  alertDate: { color: COLORS.muted, fontSize: 12, marginTop: 4 },
  traiterBtn: { marginTop: 8, alignSelf: 'flex-start', borderColor: COLORS.primary },
});
