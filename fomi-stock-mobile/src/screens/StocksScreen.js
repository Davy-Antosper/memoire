import React, { useState, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Text, Card, Chip } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { get } from '../api/client';
import LoadingScreen from '../components/LoadingScreen';
import EmptyState from '../components/EmptyState';
import { COLORS } from '../theme';

export default function StocksScreen() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [expandedDepot, setExpandedDepot] = useState(null);

  const fetchStocks = async () => {
    try {
      const res = await get('/api/stocks/disponibles');
      const data = res.data;
      setStocks(Array.isArray(data) ? data : data?.content || []);
    } catch (e) {
      try {
        const res = await get('/api/stocks');
        const data = res.data;
        setStocks(Array.isArray(data) ? data : data?.content || []);
      } catch (e2) {}
    }
    setLoading(false);
  };

  useFocusEffect(
    useCallback(() => {
      fetchStocks();
    }, [])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchStocks();
    setRefreshing(false);
  };

  // Group by depot
  const groupedStocks = {};
  stocks.forEach((s) => {
    const depot = s.depotNom || s.depot?.nom || s.depot || 'Inconnu';
    if (!groupedStocks[depot]) groupedStocks[depot] = [];
    groupedStocks[depot].push(s);
  });

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Stocks disponibles</Text>
      <FlatList
        data={Object.keys(groupedStocks)}
        keyExtractor={(item) => item}
        renderItem={({ item: depot }) => (
          <Card style={styles.depotCard}>
            <Card.Content>
              <View
                style={styles.depotHeader}
                onTouchEnd={() => setExpandedDepot(expandedDepot === depot ? null : depot)}
              >
                <MaterialCommunityIcons name="warehouse" size={20} color={COLORS.primary} />
                <Text style={styles.depotName}>{depot}</Text>
                <MaterialCommunityIcons
                  name={expandedDepot === depot ? 'chevron-up' : 'chevron-down'}
                  size={20}
                  color={COLORS.muted}
                />
              </View>

              {expandedDepot === depot && (
                <View style={styles.stockList}>
                  {groupedStocks[depot].map((stock, idx) => (
                    <View key={idx} style={styles.stockRow}>
                      <View style={styles.stockInfo}>
                        <Text style={styles.engraisName}>
                          {stock.engraisTypeNom || stock.engraisType?.nom || 'Type inconnu'}
                        </Text>
                        {stock.lotNumero && (
                          <Text style={styles.lotInfo}>Lot: {stock.lotNumero}</Text>
                        )}
                      </View>
                      <Chip compact style={styles.qtyChip} textStyle={styles.qtyText}>
                        {stock.quantiteDisponible || stock.quantite || 0} t
                      </Chip>
                    </View>
                  ))}
                </View>
              )}

              {expandedDepot !== depot && (
                <Text style={styles.stockCount}>
                  {groupedStocks[depot].length} type(s) d'engrais
                </Text>
              )}
            </Card.Content>
          </Card>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[COLORS.primary]} />}
        ListEmptyComponent={<EmptyState icon="package-variant" message="Aucun stock disponible" />}
        contentContainerStyle={Object.keys(groupedStocks).length === 0 ? styles.emptyList : styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  title: { fontSize: 20, fontWeight: 'bold', color: COLORS.text, padding: 12 },
  list: { padding: 8 },
  emptyList: { flex: 1 },
  depotCard: { marginBottom: 8, backgroundColor: COLORS.card },
  depotHeader: { flexDirection: 'row', alignItems: 'center', paddingVertical: 4 },
  depotName: { flex: 1, marginLeft: 8, fontSize: 16, fontWeight: '600', color: COLORS.text },
  stockCount: { color: COLORS.muted, fontSize: 13, marginTop: 4, marginLeft: 28 },
  stockList: { marginTop: 12 },
  stockRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8, borderTopWidth: 1, borderTopColor: COLORS.border },
  stockInfo: { flex: 1 },
  engraisName: { color: COLORS.text, fontWeight: '500' },
  lotInfo: { color: COLORS.muted, fontSize: 12, marginTop: 2 },
  qtyChip: { backgroundColor: COLORS.primary + '15' },
  qtyText: { color: COLORS.primary, fontWeight: 'bold' },
});
