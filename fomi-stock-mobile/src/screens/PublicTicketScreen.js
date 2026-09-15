import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, TextInput, Button } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { get } from '../api/client';
import StatusBadge from '../components/StatusBadge';
import LoadingScreen from '../components/LoadingScreen';
import { COLORS } from '../theme';

export default function PublicTicketScreen() {
  const [numero, setNumero] = useState('');
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!numero.trim()) return;
    setLoading(true);
    setError('');
    setTicket(null);
    try {
      const res = await get(`/api/public/tickets/${numero.trim()}`);
      setTicket(res.data);
    } catch (e) {
      setError(e.response?.data?.message || 'Ticket non trouvé');
    }
    setLoading(false);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try { return new Date(dateStr).toLocaleDateString('fr-BI'); } catch { return dateStr; }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <MaterialCommunityIcons name="ticket-confirmation" size={48} color={COLORS.primary} />
        <Text style={styles.title}>Suivi de commande</Text>
        <Text style={styles.subtitle}>Entrez votre numéro de ticket</Text>
      </View>

      <Card style={styles.searchCard}>
        <Card.Content>
          <TextInput
            label="Numéro de ticket"
            value={numero}
            onChangeText={setNumero}
            mode="outlined"
            placeholder="Ex: 12345"
            right={<TextInput.Icon icon="magnify" onPress={handleSearch} />}
          />
        </Card.Content>
      </Card>

      {loading && <LoadingScreen message="Recherche..." />}

      {error ? (
        <Card style={[styles.card, styles.errorCard]}>
          <Card.Content style={styles.errorContent}>
            <MaterialCommunityIcons name="alert-circle" size={32} color={COLORS.error} />
            <Text style={styles.errorText}>{error}</Text>
          </Card.Content>
        </Card>
      ) : null}

      {ticket && (
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.ticketHeader}>
              <Text style={styles.ticketNumero}>Ticket #{ticket.numero}</Text>
              <StatusBadge status={ticket.statut} />
            </View>

            <View style={styles.row}>
              <Text style={styles.label}>Engrais</Text>
              <Text style={styles.value}>{ticket.engraisTypeNom || ticket.engraisType?.nom || '-'}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Quantité commandée</Text>
              <Text style={styles.value}>{ticket.quantiteCommandee} t</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Quantité servie</Text>
              <Text style={styles.value}>{ticket.quantiteServie || 0} t</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Montant payé</Text>
              <Text style={styles.value}>{ticket.montantPaye} BIF</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Dépôt retrait</Text>
              <Text style={styles.value}>{ticket.depotRetraitNom || ticket.depotRetrait?.nom || '-'}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Date</Text>
              <Text style={styles.value}>{formatDate(ticket.dateCreation)}</Text>
            </View>
          </Card.Content>
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  content: { padding: 16 },
  header: { alignItems: 'center', marginBottom: 24, marginTop: 16 },
  title: { fontSize: 24, fontWeight: 'bold', color: COLORS.primary, marginTop: 8 },
  subtitle: { fontSize: 14, color: COLORS.muted, marginTop: 4 },
  searchCard: { backgroundColor: COLORS.card, marginBottom: 16 },
  card: { backgroundColor: COLORS.card, marginBottom: 12 },
  ticketHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  ticketNumero: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  row: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: COLORS.border },
  label: { color: COLORS.muted },
  value: { color: COLORS.text, fontWeight: '500' },
  errorCard: { backgroundColor: '#fee2e2' },
  errorContent: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  errorText: { color: COLORS.error, flex: 1 },
});
