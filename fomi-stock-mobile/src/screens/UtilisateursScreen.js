import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Modal, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, Card, TextInput, Button, FAB, IconButton } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get, post } from '../api/client';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

const ROLE_COLORS = {
  ADMIN: '#dc2626',
  SUPERVISEUR: '#2563eb',
  AGENT_LOGISTIQUE: '#15803d',
  AGENT_COMMERCIAL: '#d97706',
  CAISSIER: '#7c3aed',
};

export default function UtilisateursScreen() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [createModal, setCreateModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [form, setForm] = useState({ username: '', password: '', nomComplet: '', role: 'AGENT_COMMERCIAL' });

  const fetchUsers = async () => {
    try {
      const res = await get('/api/utilisateurs');
      const data = res.data;
      setUsers(data.content || data || []);
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchUsers();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchUsers();
    setRefreshing(false);
  };

  const handleCreate = async () => {
    setActionLoading(true);
    try {
      await post('/api/utilisateurs', {
        username: form.username,
        password: form.password,
        nomComplet: form.nomComplet,
        role: form.role,
      });
      setCreateModal(false);
      setForm({ username: '', password: '', nomComplet: '', role: 'AGENT_COMMERCIAL' });
      fetchUsers();
    } catch (e) {}
    setActionLoading(false);
  };

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.container}>
      <FlatList
        data={users}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Content style={styles.cardContent}>
              <MaterialCommunityIcons name="account" size={32} color={COLORS.primary} />
              <View style={styles.cardInfo}>
                <Text style={styles.name}>{item.nomComplet || item.username}</Text>
                <Text style={styles.username}>@{item.username}</Text>
              </View>
              <View style={[styles.roleBadge, { backgroundColor: (ROLE_COLORS[item.role] || COLORS.muted) + '20' }]}>
                <Text style={[styles.roleText, { color: ROLE_COLORS[item.role] || COLORS.muted }]}>
                  {item.role}
                </Text>
              </View>
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="account-group" message="Aucun utilisateur" />}
        contentContainerStyle={users.length === 0 ? styles.emptyList : styles.list}
      />

      <FAB icon="plus" style={styles.fab} onPress={() => setCreateModal(true)} color={COLORS.white} />

      <Modal visible={createModal} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalContent}>
            <ScrollView>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>Nouvel utilisateur</Text>
                <IconButton icon="close" onPress={() => setCreateModal(false)} />
              </View>
              <TextInput label="Nom d'utilisateur" value={form.username} onChangeText={(v) => setForm({ ...form, username: v })} mode="outlined" style={styles.input} />
              <TextInput label="Mot de passe" value={form.password} onChangeText={(v) => setForm({ ...form, password: v })} mode="outlined" secureTextEntry style={styles.input} />
              <TextInput label="Nom complet" value={form.nomComplet} onChangeText={(v) => setForm({ ...form, nomComplet: v })} mode="outlined" style={styles.input} />
              <TextInput label="Rôle" value={form.role} onChangeText={(v) => setForm({ ...form, role: v })} mode="outlined" style={styles.input} />
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
  cardContent: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  cardInfo: { flex: 1 },
  name: { fontWeight: '600', color: COLORS.text },
  username: { color: COLORS.muted, fontSize: 13 },
  roleBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12 },
  roleText: { fontSize: 11, fontWeight: '600' },
  fab: { position: 'absolute', right: 16, bottom: 16, backgroundColor: COLORS.primary },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modalContent: { backgroundColor: COLORS.card, borderTopLeftRadius: 16, borderTopRightRadius: 16, padding: 16, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  input: { marginBottom: 12 },
  actionBtn: { marginTop: 8 },
});
