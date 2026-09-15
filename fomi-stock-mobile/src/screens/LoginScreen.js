import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { TextInput, Button, Text, Card } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { COLORS } from '../theme';

export default function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [secureEntry, setSecureEntry] = useState(true);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setError('Veuillez remplir tous les champs');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await login(username.trim(), password);
    } catch (e) {
      const msg = e.response?.data?.message || e.message || 'Erreur de connexion';
      setError(msg);
    }
    setLoading(false);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.header}>
          <MaterialCommunityIcons name="seed" size={64} color={COLORS.primary} />
          <Text style={styles.title}>FOMI Stock</Text>
          <Text style={styles.subtitle}>Gestion des stocks d'engrais</Text>
        </View>

        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Nom d'utilisateur"
              value={username}
              onChangeText={setUsername}
              mode="outlined"
              left={<TextInput.Icon icon="account" />}
              style={styles.input}
              autoCapitalize="none"
            />
            <TextInput
              label="Mot de passe"
              value={password}
              onChangeText={setPassword}
              mode="outlined"
              secureTextEntry={secureEntry}
              left={<TextInput.Icon icon="lock" />}
              right={
                <TextInput.Icon
                  icon={secureEntry ? 'eye-off' : 'eye'}
                  onPress={() => setSecureEntry(!secureEntry)}
                />
              }
              style={styles.input}
            />

            {error ? (
              <Text style={styles.error}>{error}</Text>
            ) : null}

            <Button
              mode="contained"
              onPress={handleLogin}
              loading={loading}
              disabled={loading}
              buttonColor={COLORS.primary}
              style={styles.button}
              contentStyle={styles.buttonContent}
            >
              Se connecter
            </Button>
          </Card.Content>
        </Card>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scroll: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 24,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginTop: 8,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.muted,
    marginTop: 4,
  },
  card: {
    backgroundColor: COLORS.card,
  },
  input: {
    marginBottom: 12,
  },
  error: {
    color: COLORS.error,
    marginBottom: 12,
    textAlign: 'center',
  },
  button: {
    marginTop: 8,
    borderRadius: 8,
  },
  buttonContent: {
    paddingVertical: 6,
  },
});
