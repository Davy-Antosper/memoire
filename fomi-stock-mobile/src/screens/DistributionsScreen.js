import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Modal, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, Card, TextInput, Button, IconButton } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get, post } from '../api/client';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

export default function DistributionsScreen() {
  const [distributions, setDistributions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [createModal, setCreateModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [form, setForm] = useState({ ticketId: '', depotId: '', lotId: '', quantite: '', commentaire: '' });

  const fetchDistributions = async () => {
    try {
      const res = await get('/api/distributions', { params: { page: 0, size: 50 } });
      const data = res.data;
      setDistributions(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchDistributions();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchDistributions();
    setRefreshing(false);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    setResult(null);
    try {
      const payload = {
        ticketId: parseInt(form.ticketId) || null,
        depotId: parseInt(form.depotId) || null,
        quantite: parseFloat(form.quantite) || 0,
        commentaire: form.commentaire || null,
      };
      if (form.lotId) payload.lotId = parseInt(form.lotId);
      const res = await post('/api/distributions', payload);
      setResult({ success: true, data: res.data });
      setForm({ ticketId: '', depotId: '', lotId: '', quantite: '', commentaire: '' });
      fetchDistributions();
    } catch (e) {
      setResult({ success: false, message: e.response?.data?.message || 'Erreur' });
    }
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
        data={distributions}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Content>
              <View style={styles.header}>
                <MaterialCommunityIcons name="truck-delivery" size={20} color={COLORS.primary} />
                <Text style={styles.ticketNum}>Ticket #{item.ticketNumero || item.ticketId}</Text>
              </View>
              <View style={styles.details}>
                <Text style={styles.detail}>Dépôt: {item.depotNom || item.depotId}</Text>
                <Text style={styles.detail}>Qté: {item.quantiteDistribuee || item.quantite} t</Text>
                <Text style={styles.date}>{formatDate(item.dateDistribution)}</Text>
              </View>
              {item.commentaire && <Text style={styles.comment}>{item.commentaire}</Text>}
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="truck-delivery" message="Aucune distribution" />}
        contentContainerStyle={distributions.length === 0 ? styles.emptyList : styles.list}
      />

      <Button mode="contained" buttonColor={COLORS.primary} style={styles.createBtn} onPress={() => setCreateModal(true)}>
        Nouvelle distribution
      </Button>

      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouvelle distribution</Text>
                <IconButton icon="close" onPress={() => { setCreateModal(false); setResult(null); }} />
              </View>
              <TextInput label="ID Ticket" value={form.ticketId} onChangeText={(v) => setForm({ ...form, ticketId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="ID Dépôt" value={form.depotId} onChangeText={(v) => setForm({ ...form, depotId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="ID Lot (optionnel)" value={form.lotId} onChangeText={(v) => setForm({ ...form, lotId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Quantité (tonnes)" value={form.quantite} onChangeText={(v) => setForm({ ...form, quantite: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Commentaire" value={form.commentaire} onChangeText={(v) => setForm({ ...form, commentaire: v })} mode="outlined" multiline style={styles.input} />

              {result && (
                <Card style={[styles.resultCard, result.success ? styles.resultSuccess : styles.resultError]}>
                  <Card.Content>
                    <Text style={result.success ? styles.resultTextSuccess : styles.resultTextError}>
                      {result.success ? 'Distribution créée avec succès' : result.message}
                    </Text>
                  </Card.Content>
                </Card>
              )}

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
  header: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 6 },
  ticketNum: { fontWeight: '600', color: COLORS.text },
  details: { flexDirection: 'row', justifyContent: 'space-between', flexWrap: 'wrap', gap: 4 },
  detail: { color: COLORS.muted, fontSize: 13 },
  date: { color: COLORS.muted, fontSize: 12 },
  comment: { color: COLORS.muted, fontSize: 12, marginTop: 4, fontStyle: 'italic' },
  createBtn: { margin: 12 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  input: { marginBottom: 12 },
  actionBtn: { marginTop: 8 },
  resultCard: { marginBottom: 12 },
  resultSuccess: { backgroundColor: '#dcfce7' },
  resultError: { backgroundColor: '#fee2e2' },
  resultTextSuccess: { color: '#166534' },
  resultTextError: { color: '#991b1b' },
});
