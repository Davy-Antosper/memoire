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

export default function AgriculteursScreen() {
  const { canCreateTicket } = useAuth();
  const [agriculteurs, setAgriculteurs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');
  const [createModal, setCreateModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [newAgri, setNewAgri] = useState({
    numeroIdentite: '', nom: '', prenom: '', telephone: '', collineId: '',
  });

  const fetchAgriculteurs = async (query) => {
    try {
      let res;
      if (query) {
        res = await get('/api/agriculteurs/recherche', { params: { telephone: query } });
      } else {
        res = await get('/api/agriculteurs', { params: { page: 0, size: 100 } });
      }
      const data = res.data;
      setAgriculteurs(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchAgriculteurs();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchAgriculteurs(search);
    setRefreshing(false);
  };

  const handleSearch = async () => {
    setLoading(true);
    await fetchAgriculteurs(search.trim() || undefined);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    try {
      await post('/api/agriculteurs', {
        numeroIdentite: newAgri.numeroIdentite,
        nom: newAgri.nom,
        prenom: newAgri.prenom,
        telephone: newAgri.telephone,
        collineId: parseInt(newAgri.collineId) || null,
      });
      setCreateModal(false);
      setNewAgri({ numeroIdentite: '', nom: '', prenom: '', telephone: '', collineId: '' });
      fetchAgriculteurs();
    } catch (e) {}
    setActionLoading(false);
  };

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.container}>
      <View style={styles.searchRow}>
        <TextInput
          placeholder="Rechercher par téléphone..."
          value={search}
          onChangeText={setSearch}
          mode="outlined"
          dense
          style={styles.searchInput}
          right={<TextInput.Icon icon="magnify" onPress={handleSearch} />}
        />
      </View>

      <FlatList
        data={agriculteurs}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Content style={styles.cardContent}>
              <MaterialCommunityIcons name="account" size={32} color={COLORS.primary} />
              <View style={styles.cardInfo}>
                <Text style={styles.name}>{item.prenom} {item.nom}</Text>
                <Text style={styles.phone}>{item.telephone}</Text>
                {item.collineNom && <Text style={styles.colline}>Colline: {item.collineNom}</Text>}
                {item.cooperativeNom && (
                  <Text style={styles.coop}>Coopérative: {item.cooperativeNom}</Text>
                )}
              </View>
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="account-group" message="Aucun agriculteur trouvé" />}
        contentContainerStyle={agriculteurs.length === 0 ? styles.emptyList : styles.list}
      />

      {canCreateTicket && (
        <FAB icon="plus" style={styles.fab} onPress={() => setCreateModal(true)} color={COLORS.white} />
      )}

      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouvel agriculteur</Text>
                <IconButton icon="close" onPress={() => setCreateModal(false)} />
              </View>
              <TextInput label="Numéro d'identité" value={newAgri.numeroIdentite} onChangeText={(v) => setNewAgri({ ...newAgri, numeroIdentite: v })} mode="outlined" style={styles.input} />
              <TextInput label="Nom" value={newAgri.nom} onChangeText={(v) => setNewAgri({ ...newAgri, nom: v })} mode="outlined" style={styles.input} />
              <TextInput label="Prénom" value={newAgri.prenom} onChangeText={(v) => setNewAgri({ ...newAgri, prenom: v })} mode="outlined" style={styles.input} />
              <TextInput label="Téléphone" value={newAgri.telephone} onChangeText={(v) => setNewAgri({ ...newAgri, telephone: v })} mode="outlined" keyboardType="phone-pad" style={styles.input} />
              <TextInput label="ID Colline" value={newAgri.collineId} onChangeText={(v) => setNewAgri({ ...newAgri, collineId: v })} mode="outlined" keyboardType="numeric" style={styles.input} />
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
  cardContent: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  cardInfo: { flex: 1 },
  name: { fontSize: 16, fontWeight: '600', color: COLORS.text },
  phone: { color: COLORS.muted, marginTop: 2 },
  colline: { color: COLORS.muted, fontSize: 12, marginTop: 2 },
  coop: { color: COLORS.primary, fontSize: 12, marginTop: 2 },
  fab: { position: 'absolute', right: 16, bottom: 16, backgroundColor: COLORS.primary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  input: { marginBottom: 12 },
  actionBtn: { marginTop: 8 },
});
