import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Card, Button, Divider } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { useNavigation } from '@react-navigation/native';
import { COLORS } from '../theme';

export default function ParametresScreen() {
  const { user, logout } = useAuth();
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.userRow}>
            <MaterialCommunityIcons name="account-circle" size={48} color={COLORS.primary} />
            <View style={styles.userInfo}>
              <Text style={styles.userName}>{user?.nomComplet || user?.username}</Text>
              <Text style={styles.userRole}>{user?.role || 'Utilisateur'}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Actions</Text>

          <Button
            mode="text"
            icon="ticket"
            onPress={() => navigation.navigate('PublicTicket')}
            contentStyle={styles.menuItem}
          >
            Suivi de commande publique
          </Button>

          <Divider />

          <Button
            mode="text"
            icon="logout"
            textColor={COLORS.error}
            onPress={logout}
            contentStyle={styles.menuItem}
          >
            Déconnexion
          </Button>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>À propos</Text>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Application</Text>
            <Text style={styles.aboutValue}>FOMI Stock Mobile</Text>
          </View>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
        </Card.Content>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background, padding: 12 },
  card: { backgroundColor: COLORS.card, marginBottom: 12 },
  userRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  userInfo: { flex: 1 },
  userName: { fontSize: 18, fontWeight: 'bold', color: COLORS.text },
  userRole: { color: COLORS.muted, marginTop: 2 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: COLORS.text, marginBottom: 8 },
  menuItem: { justifyContent: 'flex-start', paddingVertical: 4 },
  aboutRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 6 },
  aboutLabel: { color: COLORS.muted },
  aboutValue: { color: COLORS.text, fontWeight: '500' },
});
