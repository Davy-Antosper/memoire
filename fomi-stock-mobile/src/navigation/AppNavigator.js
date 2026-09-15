import React from 'react';
import { View, StyleSheet, TouchableOpacity, Modal, ScrollView, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { COLORS } from '../theme';

import LoginScreen from '../screens/LoginScreen';
import PublicTicketScreen from '../screens/PublicTicketScreen';
import DashboardScreen from '../screens/DashboardScreen';
import TicketsScreen from '../screens/TicketsScreen';
import StocksScreen from '../screens/StocksScreen';
import AlertesScreen from '../screens/AlertesScreen';
import ParametresScreen from '../screens/ParametresScreen';
import AgriculteursScreen from '../screens/AgriculteursScreen';
import DistributionsScreen from '../screens/DistributionsScreen';
import MouvementsScreen from '../screens/MouvementsScreen';
import LotsScreen from '../screens/LotsScreen';
import UtilisateursScreen from '../screens/UtilisateursScreen';
import AuditLogsScreen from '../screens/AuditLogsScreen';
import LoadingScreen from '../components/LoadingScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const screenOptions = {
  headerStyle: { backgroundColor: COLORS.primary },
  headerTintColor: COLORS.white,
  headerTitleStyle: { fontWeight: '600' },
};

function MoreMenuScreen({ navigation }) {
  const { canManageUsers, canViewAuditLogs } = useAuth();

  const menuItems = [
    { icon: 'account-group', label: 'Agriculteurs', screen: 'Agriculteurs' },
    { icon: 'truck-delivery', label: 'Distributions', screen: 'Distributions' },
    { icon: 'swap-horizontal', label: 'Mouvements', screen: 'Mouvements' },
    { icon: 'package-variant', label: 'Lots', screen: 'Lots' },
  ];

  if (canManageUsers) {
    menuItems.push({ icon: 'account-cog', label: 'Utilisateurs', screen: 'Utilisateurs' });
  }
  if (canViewAuditLogs) {
    menuItems.push({ icon: 'history', label: 'Audit Logs', screen: 'AuditLogs' });
  }

  return (
    <ScrollView style={styles.menuContainer}>
      {menuItems.map((item) => (
        <TouchableOpacity
          key={item.screen}
          style={styles.menuItem}
          onPress={() => navigation.navigate(item.screen)}
        >
          <MaterialCommunityIcons name={item.icon} size={24} color={COLORS.primary} />
          <Text style={styles.menuLabel}>{item.label}</Text>
          <MaterialCommunityIcons name="chevron-right" size={20} color={COLORS.muted} />
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerStyle: { backgroundColor: COLORS.primary },
        headerTintColor: COLORS.white,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.muted,
        tabBarIcon: ({ color, size }) => {
          let iconName;
          switch (route.name) {
            case 'Dashboard': iconName = 'view-dashboard'; break;
            case 'Tickets': iconName = 'ticket'; break;
            case 'Stocks': iconName = 'package-variant'; break;
            case 'Alertes': iconName = 'bell'; break;
            case 'More': iconName = 'dots-horizontal'; break;
            default: iconName = 'circle';
          }
          return <MaterialCommunityIcons name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} options={{ title: 'Accueil' }} />
      <Tab.Screen name="Tickets" component={TicketsScreen} options={{ title: 'Tickets' }} />
      <Tab.Screen name="Stocks" component={StocksScreen} options={{ title: 'Stocks' }} />
      <Tab.Screen name="Alertes" component={AlertesScreen} options={{ title: 'Alertes' }} />
      <Tab.Screen name="More" component={MoreMenuScreen} options={{ title: 'Plus' }} />
    </Tab.Navigator>
  );
}

function AuthStack() {
  return (
    <Stack.Navigator screenOptions={screenOptions}>
      <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
      <Stack.Screen name="PublicTicket" component={PublicTicketScreen} options={{ title: 'Suivi de commande' }} />
    </Stack.Navigator>
  );
}

function MainStack() {
  return (
    <Stack.Navigator screenOptions={screenOptions}>
      <Stack.Screen name="MainTabs" component={MainTabs} options={{ headerShown: false }} />
      <Stack.Screen name="Agriculteurs" component={AgriculteursScreen} options={{ title: 'Agriculteurs' }} />
      <Stack.Screen name="Distributions" component={DistributionsScreen} options={{ title: 'Distributions' }} />
      <Stack.Screen name="Mouvements" component={MouvementsScreen} options={{ title: 'Mouvements' }} />
      <Stack.Screen name="Lots" component={LotsScreen} options={{ title: 'Lots' }} />
      <Stack.Screen name="Utilisateurs" component={UtilisateursScreen} options={{ title: 'Utilisateurs' }} />
      <Stack.Screen name="AuditLogs" component={AuditLogsScreen} options={{ title: 'Journal d\'audit' }} />
      <Stack.Screen name="Parametres" component={ParametresScreen} options={{ title: 'Paramètres' }} />
      <Stack.Screen name="PublicTicket" component={PublicTicketScreen} options={{ title: 'Suivi de commande' }} />
    </Stack.Navigator>
  );
}

export default function AppNavigator() {
  const { user, loading } = useAuth();

  if (loading) return <LoadingScreen />;

  return (
    <NavigationContainer>
      {user ? <MainStack /> : <AuthStack />}
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  menuContainer: { flex: 1, backgroundColor: COLORS.background },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: COLORS.card,
    marginBottom: 1,
  },
  menuLabel: { flex: 1, marginLeft: 12, fontSize: 16, color: COLORS.text },
});
