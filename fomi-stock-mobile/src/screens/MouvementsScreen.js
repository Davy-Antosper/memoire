import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Modal, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, Card, TextInput, Button, FAB, IconButton, SegmentedButtons } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get, post } from '../api/client';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/StatusBadge';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

export default function MouvementsScreen() {
  const { canCreateMouvement } = useAuth();
  const [mouvements, setMouvements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [createModal, setCreateModal] = useState(false);
  const [mouvementType, setMouvementType] = useState('RECEPTION_FOMI');
  const [actionLoading, setActionLoading] = useState(false);
  const [form, setForm] = useState({ lotId: '', depotDestId: '', depotSourceId: '', quantite: '' });

  const fetchMouvements = async () => {
    try {
      const res = await get('/api/mouvements', { params: { page: 0, size: 50 } });
      const data = res.data;
      setMouvements(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchMouvements();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchMouvements();
    setRefreshing(false);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    try {
      const payload = {
        lotId: parseInt(form.lotId) || null,
        quantite: parseFloat(form.quantite) || 0,
      };
      let url;
      if (mouvementType === 'RECEPTION_FOMI') {
        payload.depotDestId = parseInt(form.depotDestId) || null;
        url = '/api/mouvements/reception';
      } else {
        payload.depotSourceId = parseInt(form.depotSourceId) || null;
        payload.depotDestId = parseInt(form.depotDestId) || null;
        url = '/api/mouvements/transfert';
      }
      await post(url, payload);
      setCreateModal(false);
      setForm({ lotId: '', depotDestId: '', depotSourceId: '', quantite: '' });
      fetchMouvements();
    } catch (e) {}
    setActionLoading(false);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try { return new Date(dateStr).toLocaleDateString('fr-BI'); } catch { return dateStr; }
  };

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.container}>
      <FlatList
        data={mouvements}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Content>
              <View style={styles.header}>
                <StatusBadge type={item.type} />
                <Text style={styles.date}>{formatDate(item.dateMouvement)}</Text>
              </View>
              <View style={styles.details}>
                <Text style={styles.detail}>Lot: {item.lotNumero || item.lotId}</Text>
                <Text style={styles.qty}>{item.quantite} t</Text>
              </View>
              <View style={styles.route}>
                {item.depotSource && (
                  <Text style={styles.depot}>{item.depotSourceNom || item.depotSource?.nom || 'Source'}</Text>
                )}
                {item.type === 'TRANSFERT' && (
                  <MaterialCommunityIcons name="arrow-right" size={16} color={COLORS.muted} />
                )}
                <Text style={styles.depot}>{item.depotDestNom || item.depotDest?.nom || 'Destination'}</Text>
              </View>
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="swap-horizontal" message="Aucun mouvement" />}
        contentContainerStyle={mouvements.length === 0 ? styles.emptyList : styles.list}
      />

      {canCreateMouvement && (
        <FAB icon="plus" style={styles.fab} onPress={() => setCreateModal(true)} color={COLORS.white} />
      )}

      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouveau mouvement</Text>
                <IconButton icon="close" onPress={() => setCreateModal(false)} />
              </View>

              <SegmentedButtons
                value={mouvementType}
                onValueChange={setMouvementType}
                buttons={[
                  { value: 'RECEPTION_FOMI', label: 'Réception' },
                  { value: 'TRANSFERT', label: 'Transfert' },
                ]}
                style={styles.segmented}
              />

              <TextInput label="ID Lot" value={form.lotId} onChangeText={(v) => setForm({ ...form, lotId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              {mouvementType === 'RECEPTION_FOMI' ? (
                <TextInput label="ID Dépôt destination" value={form.depotDestId} onChangeText={(v) => setForm({ ...form, depotDestId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              ) : (
                <>
                  <TextInput label="ID Dépôt source" value={form.depotSourceId} onChangeText={(v) => setForm({ ...form, depotSourceId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
                  <TextInput label="ID Dépôt destination" value={form.depotDestId} onChangeText={(v) => setForm({ ...form, depotDestId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
                </>
              )}
              <TextInput label="Quantité (tonnes)" value={form.quantite} onChangeText={(v) => setForm({ ...form, quantite: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <Button mode="contained" buttonColor={COLORS.primary} onPress={handleCreate} loading={actionLoading} style={styles.actionBtn}>Créer</Button>
            </ScrollView>
          </KeyboardAvoidingView>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  list: { padding: 8 },
  emptyList: { flex: 1 },
  card: { marginBottom: 8, backgroundColor: COLORS.card },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  date: { color: COLORS.muted, fontSize: 12 },
  details: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 8 },
  detail: { color: COLORS.muted },
  qty: { fontWeight: 'bold', color: COLORS.primary },
  route: { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 6 },
  depot: { color: COLORS.text, fontSize: 13 },
  fab: { position: 'absolute', right: 16, bottom: 16, backgroundColor: COLORS.primary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  segmented: { marginBottom: 12 },
  input: { marginBottom: 12 },
  actionBtn: { marginTop: 8 },
});
