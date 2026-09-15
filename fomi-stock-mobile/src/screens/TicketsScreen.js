import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Modal, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, Card, Button, TextInput, Chip, FAB, IconButton, Portal } from 'react-native-paper';
import { useFocusEffect } from '@react-navigation/native';
import { get, post, patch } from '../api/client';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/StatusBadge';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

const STATUTS = [
  { key: 'TOUS', label: 'Tous' },
  { key: 'PAYE', label: 'Payé' },
  { key: 'EN_ATTENTE_DE_VALIDATION', label: 'En attente' },
  { key: 'ACTIF', label: 'Actif' },
  { key: 'PARTIEL', label: 'Partiel' },
  { key: 'SERVI', label: 'Servi' },
  { key: 'REJETE', label: 'Rejeté' },
];

export default function TicketsScreen({ navigation }) {
  const { user, canCreateTicket, canActivateTicket } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState('TOUS');
  const [detailModal, setDetailModal] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [createModal, setCreateModal] = useState(false);
  const [rejectModal, setRejectModal] = useState(false);
  const [rejectMotif, setRejectMotif] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  const [newTicket, setNewTicket] = useState({
    agriculteurId: '',
    engraisTypeId: '',
    quantiteCommandee: '',
    montantPaye: '',
    depotRetraitId: '',
    saison: '',
  });

  const fetchTickets = async () => {
    try {
      const res = await get('/api/tickets', { params: { page: 0, size: 100 } });
      const data = res.data;
      setTickets(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchTickets();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchTickets();
    setRefreshing(false);
  };

  const filteredTickets = filter === 'TOUS'
    ? tickets
    : tickets.filter((t) => t.statut === filter);

  const openDetail = async (ticket) => {
    try {
      const res = await get(`/api/tickets/${ticket.id}`);
      setSelectedTicket(res.data);
    } catch (e) {
      setSelectedTicket(ticket);
    }
    setDetailModal(true);
  };

  const handleActivate = async (id) => {
    setActionLoading(true);
    try {
      await patch(`/api/tickets/${id}/activer`);
      setDetailModal(false);
      fetchTickets();
    } catch (e) {}
    setActionLoading(false);
  };

  const handleReject = async (id) => {
    setActionLoading(true);
    try {
      await patch(`/api/tickets/${id}/rejeter`, { motif: rejectMotif });
      setRejectModal(false);
      setDetailModal(false);
      setRejectMotif('');
      fetchTickets();
    } catch (e) {}
    setActionLoading(false);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    try {
      await post('/api/tickets', {
        agriculteurId: parseInt(newTicket.agriculteurId) || null,
        engraisTypeId: parseInt(newTicket.engraisTypeId) || null,
        quantiteCommandee: parseFloat(newTicket.quantiteCommandee) || 0,
        montantPaye: parseFloat(newTicket.montantPaye) || 0,
        depotRetraitId: parseInt(newTicket.depotRetraitId) || null,
        saison: newTicket.saison || null,
      });
      setCreateModal(false);
      setNewTicket({ agriculteurId: '', engraisTypeId: '', quantiteCommandee: '', montantPaye: '', depotRetraitId: '', saison: '' });
      fetchTickets();
    } catch (e) {}
    setActionLoading(false);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try {
      return new Date(dateStr).toLocaleDateString('fr-BI');
    } catch {
      return dateStr;
    }
  };

  const renderTicket = ({ item }) => (
    <Card style={styles.ticketCard} onPress={() => openDetail(item)}>
      <Card.Content>
        <View style={styles.ticketHeader}>
          <Text style={styles.ticketNumero}>#{item.numero}</Text>
          <StatusBadge status={item.statut} />
        </View>
        <Text style={styles.ticketInfo}>
          {item.agriculteurNom || item.agriculteur?.nom || 'Agriculteur'} - {item.engraisTypeNom || item.engraisType?.nom || 'N/A'}
        </Text>
        <View style={styles.ticketFooter}>
          <Text style={styles.ticketQty}>Qté: {item.quantiteCommandee}</Text>
          <Text style={styles.ticketDate}>{formatDate(item.dateCreation)}</Text>
        </View>
      </Card.Content>
    </Card>
  );

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.container}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterRow}>
        {STATUTS.map((s) => (
          <Chip
            key={s.key}
            selected={filter === s.key}
            onPress={() => setFilter(s.key)}
            style={[styles.chip, filter === s.key && styles.chipSelected]}
            textStyle={filter === s.key ? styles.chipTextSelected : {}}
          >
            {s.label}
          </Chip>
        ))}
      </ScrollView>

      <FlatList
        data={filteredTickets}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderTicket}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="ticket" message="Aucun ticket" />}
        contentContainerStyle={filteredTickets.length === 0 ? styles.emptyList : styles.list}
      />

      {canCreateTicket && (
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={() => setCreateModal(true)}
          color={COLORS.white}
        />
      )}

      {/* Detail Modal */}
      <Modal visible={detailModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Ticket #{selectedTicket?.numero}</Text>
                <IconButton icon="close" onPress={() => setDetailModal(false)} />
              </View>

              {selectedTicket && (
                <>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Statut</Text>
                    <StatusBadge status={selectedTicket.statut} />
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Agriculteur</Text>
                    <Text style={styles.detailValue}>{selectedTicket.agriculteurNom || selectedTicket.agriculteur?.nom || '-'}</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Engrais</Text>
                    <Text style={styles.detailValue}>{selectedTicket.engraisTypeNom || selectedTicket.engraisType?.nom || '-'}</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Quantité</Text>
                    <Text style={styles.detailValue}>{selectedTicket.quantiteCommandee}</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Montant payé</Text>
                    <Text style={styles.detailValue}>{selectedTicket.montantPaye} BIF</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Dépôt retrait</Text>
                    <Text style={styles.detailValue}>{selectedTicket.depotRetraitNom || selectedTicket.depotRetrait?.nom || '-'}</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Saison</Text>
                    <Text style={styles.detailValue}>{selectedTicket.saison || '-'}</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Date création</Text>
                    <Text style={styles.detailValue}>{formatDate(selectedTicket.dateCreation)}</Text>
                  </View>

                  {selectedTicket.distributions && selectedTicket.distributions.length > 0 && (
                    <View style={styles.section}>
                      <Text style={styles.sectionTitle}>Distributions</Text>
                      {selectedTicket.distributions.map((d, i) => (
                        <Card key={i} style={styles.distCard}>
                          <Card.Content>
                            <Text>{d.quantiteDistribuee} t - {formatDate(d.dateDistribution)}</Text>
                          </Card.Content>
                        </Card>
                      ))}
                    </View>
                  )}

                  {canActivateTicket && (selectedTicket.statut === 'PAYE' || selectedTicket.statut === 'EN_ATTENTE_DE_VALIDATION') && (
                    <View style={styles.actions}>
                      <Button
                        mode="contained"
                        buttonColor={COLORS.primary}
                        onPress={() => handleActivate(selectedTicket.id)}
                        loading={actionLoading}
                        style={styles.actionBtn}
                      >
                        Activer
                      </Button>
                      <Button
                        mode="outlined"
                        textColor={COLORS.error}
                        onPress={() => setRejectModal(true)}
                        style={styles.actionBtn}
                      >
                        Rejeter
                      </Button>
                    </View>
                  )}
                </>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Reject Modal */}
      <Modal visible={rejectModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Rejeter le ticket</Text>
            <TextInput
              label="Motif du rejet"
              value={rejectMotif}
              onChangeText={setRejectMotif}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
            />
            <View style={styles.actions}>
              <Button mode="outlined" onPress={() => setRejectModal(false)} style={styles.actionBtn}>Annuler</Button>
              <Button mode="contained" buttonColor={COLORS.error} onPress={() => handleReject(selectedTicket?.id)} loading={actionLoading} style={styles.actionBtn}>Confirmer</Button>
            </View>
          </View>
        </View>
      </Modal>

      {/* Create Modal */}
      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouveau ticket</Text>
                <IconButton icon="close" onPress={() => setCreateModal(false)} />
              </View>
              <TextInput label="ID Agriculteur" value={newTicket.agriculteurId} onChangeText={(v) => setNewTicket({ ...newTicket, agriculteurId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="ID Type d'engrais" value={newTicket.engraisTypeId} onChangeText={(v) => setNewTicket({ ...newTicket, engraisTypeId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Quantité commandée" value={newTicket.quantiteCommandee} onChangeText={(v) => setNewTicket({ ...newTicket, quantiteCommandee: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Montant payé (BIF)" value={newTicket.montantPaye} onChangeText={(v) => setNewTicket({ ...newTicket, montantPaye: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="ID Dépôt retrait" value={newTicket.depotRetraitId} onChangeText={(v) => setNewTicket({ ...newTicket, depotRetraitId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
              <TextInput label="Saison" value={newTicket.saison} onChangeText={(v) => setNewTicket({ ...newTicket, saison: v })} mode="outlined" style={styles.input} />
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
  filterRow: { paddingHorizontal: 8, paddingVertical: 8, maxHeight: 52 },
  chip: { marginRight: 6 },
  chipSelected: { backgroundColor: COLORS.primary },
  chipTextSelected: { color: COLORS.white },
  list: { padding: 8 },
  emptyList: { flex: 1 },
  ticketCard: { marginBottom: 8, backgroundColor: COLORS.card },
  ticketHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  ticketNumero: { fontSize: 16, fontWeight: 'bold', color: COLORS.text },
  ticketInfo: { color: COLORS.muted, marginTop: 4 },
  ticketFooter: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 6 },
  ticketQty: { color: COLORS.primary, fontWeight: '600' },
  ticketDate: { color: COLORS.muted, fontSize: 12 },
  fab: { position: 'absolute', right: 16, bottom: 16, backgroundColor: COLORS.primary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  detailRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: COLORS.border },
  detailLabel: { color: COLORS.muted, fontSize: 14 },
  detailValue: { color: COLORS.text, fontWeight: '500' },
  section: { marginTop: 16 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', marginBottom: 8 },
  distCard: { marginBottom: 6, backgroundColor: COLORS.background },
  actions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 16, gap: 8 },
  actionBtn: { flex: 1 },
  input: { marginBottom: 12 },
});
