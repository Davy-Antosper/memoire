import React, { useState, useCallback } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Text, Card } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get } from '../api/client';
import StatCard from '../components/StatCard';
import LoadingScreen from '../components/LoadingScreen';
import { COLORS } from '../theme';

export default function DashboardScreen() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const [rupturesRes, stocksRes, tauxRes, alertesRes] = await Promise.all([
        get('/api/statistiques/ruptures').catch(() => ({ data: [] })),
        get('/api/statistiques/stocks-par-province').catch(() => ({ data: [] })),
        get('/api/statistiques/taux-service').catch(() => ({ data: {} })),
        get('/api/alertes', { params: { nonTraitees: true } }).catch(() => ({ data: { content: [] } })),
      ]);

      const stocksData = Array.isArray(stocksRes.data) ? stocksRes.data : [];
      const totalStocks = stocksData.reduce((sum, s) => sum + (s.quantiteDisponible || s.quantite || 0), 0);

      const tauxData = tauxRes.data;
      const taux = typeof tauxData === 'number' ? tauxData : (tauxData?.taux || tauxData?.pourcentage || 0);

      const alertesData = alertesRes.data;
      const alertesCount = Array.isArray(alertesData) ? alertesData.length : (alertesData?.content?.length || 0);

      setStats({
        totalStocks,
        tauxService: typeof taux === 'number' ? taux : 0,
        ruptures: Array.isArray(rupturesRes.data) ? rupturesRes.data.length : 0,
        alertes: alertesCount,
        stocksParProvince: stocksData,
      });
    } catch (e) {}
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchData();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  if (loading) return <LoadingScreen />;

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
    >
      <Text style={styles.title}>Tableau de bord</Text>

      <View style={styles.statsGrid}>
        <StatCard icon="package-variant" value={stats?.totalStocks || 0} label="Total stocks (t)" color={COLORS.primary} />
        <StatCard icon="chart-line" value={`${stats?.tauxService || 0}%`} label="Taux de service" color={COLORS.info} />
      </View>
      <View style={styles.statsGrid}>
        <StatCard icon="alert-circle" value={stats?.ruptures || 0} label="Ruptures" color={COLORS.error} />
        <StatCard icon="bell" value={stats?.alertes || 0} label="Alertes actives" color={COLORS.warning} />
      </View>

      {stats?.stocksParProvince?.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Stocks par province</Text>
            {stats.stocksParProvince.map((item, index) => (
              <View key={index} style={styles.provinceRow}>
                <MaterialCommunityIcons name="map-marker" size={16} color={COLORS.primary} />
                <Text style={styles.provinceName}>{item.province || item.nom || `Province ${index + 1}`}</Text>
                <Text style={styles.provinceValue}>{item.quantiteDisponible || item.quantite || 0} t</Text>
              </View>
            ))}
          </Card.Content>
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: 12,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 12,
    marginTop: 4,
  },
  statsGrid: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  card: {
    backgroundColor: COLORS.card,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  provinceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  provinceName: {
    flex: 1,
    marginLeft: 8,
    color: COLORS.text,
  },
  provinceValue: {
    fontWeight: 'bold',
    color: COLORS.primary,
  },
});
