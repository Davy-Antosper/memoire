import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Modal, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, Card, TextInput, Button, FAB, IconButton } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get, post } from '../api/client';
import { useAuth } from '../context/AuthContext';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

export default function LotsScreen() {
  const { isAdmin, isAgentLogistique } = useAuth();
  const canCreate = isAdmin || isAgentLogistique;
  const [lots, setLots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');
  const [createModal, setCreateModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [form, setForm] = useState({ numero: '', engraisTypeId: '', quantiteInitiale: '', dateFabrication: '', datePeremption: '' });

  const fetchLots = async (query) => {
    try {
      let res;
      if (query) {
        res = await get('/api/lots/recherche', { params: { numero: query } });
      } else {
        res = await get('/api/lots');
      }
      const data = res.data;
      setLots(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchLots();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchLots(search);
    setRefreshing(false);
  };

  const handleSearch = async () => {
    setLoading(true);
    await fetchLots(search.trim() || undefined);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    try {
      await post('/api/lots', {
        numero: form.numero,
        engraisTypeId: parseInt(form.engraisTypeId) || null,
        quantiteInitiale: parseFloat(form.quantiteInitiale) || 0,
        dateFabrication: form.dateFabrication || null,
        datePeremption: form.datePeremption || null,
      });
      setCreateModal(false);
      setForm({ numero: '', engraisTypeId: '', quantiteInitiale: '', dateFabrication: '', datePeremption: '' });
      fetchLots();
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
      <View style={styles.searchRow}>
        <TextInput
          placeholder="Rechercher par numéro..."
          value={search}
          onChangeText={setSearch}
          mode="outlined"
          dense
          style={styles.searchInput}
          right={<TextInput.Icon icon="magnify" onPress={handleSearch} />}
        />
      </View>

      <FlatList
        data={lots}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Content>
              <View style={styles.header}>
                <MaterialCommunityIcons name="package-variant" size={20} color={COLORS.primary} />
                <Text style={styles.numero}>{item.numero}</Text>
              </View>
              <Text style={styles.engrais}>{item.engraisTypeNom || item.engraisType?.nom || 'Type inconnu'}</Text>
              <View style={styles.details}>
                <Text style={styles.detail}>Qté initiale: {item.quantiteInitiale} t</Text>
                <Text style={styles.detail}>Fab: {formatDate(item.dateFabrication)}</Text>
              </View>
              <Text style={styles.peremption}>Expire: {formatDate(item.datePeremption)}</Text>
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="package-variant" message="Aucun lot trouvé" />}
        contentContainerStyle={lots.length === 0 ? styles.emptyList : styles.list}
      />

      {canCreate && (
        <FAB icon="plus" style={styles.fab} onPress={() => setCreateModal(true)} color={COLORS.white} />
      )}

      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouveau lot</Text>
                <IconButton icon="close" onPress={() => setCreateModal(false)} />
              </View>
              <TextInput label="Numéro du lot" value={form.numero} onChangeText={(v) => setForm({ ...form, numero: v })} mode="outlined" style={styles.input} />
              <TextInput label="ID Type d'engrais" value={form.engraisTypeId} onChangeText={(v) => setForm({ ...form, engraisTypeId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Quantité initiale (t)" value={form.quantiteInitiale} onChangeText={(v) => setForm({ ...form, quantiteInitiale: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Date fabrication (AAAA-MM-JJ)" value={form.dateFabrication} onChangeText={(v) => setForm({ ...form, dateFabrication: v })} mode="outlined" style={styles.input} />
              <TextInput label="Date peremption (AAAA-MM-JJ)" value={form.datePeremption} onChangeText={(v) => setForm({ ...form, datePeremption: v })} mode="outlined" style={styles.input} />
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
  searchRow: { padding: 8 },
  searchInput: { backgroundColor: COLORS.card },
  list: { padding: 8 },
  emptyList: { flex: 1 },
  card: { marginBottom: 8, backgroundColor: COLORS.card },
  header: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  numero: { fontSize: 16, fontWeight: 'bold', color: COLORS.text },
  engrais: { color: COLORS.primary, marginTop: 4 },
  details: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 6 },
  detail: { color: COLORS.muted, fontSize: 13 },
  peremption: { color: COLORS.muted, fontSize: 12, marginTop: 4 },
  fab: { position: 'absolute', right: 16, bottom: 16, backgroundColor: COLORS.primary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  input: { marginBottom: 12 },
  actionBtn: { marginTop: 8 },
});
