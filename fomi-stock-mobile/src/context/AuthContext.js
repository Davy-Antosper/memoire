import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { post } from '../api/client';

const AuthContext = createContext(null);

const STORAGE_KEY = 'fomi_user';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const restoreSession = async () => {
      try {
        const userData = await AsyncStorage.getItem(STORAGE_KEY);
        if (userData) {
          setUser(JSON.parse(userData));
        }
      } catch (e) {}
      setLoading(false);
    };
    restoreSession();
  }, []);

  const login = useCallback(async (username, password) => {
    const response = await post('/api/auth/login', { username, password });
    const data = response.data;
    const userData = {
      token: data.token,
      username: data.username,
      nomComplet: data.nomComplet,
      role: data.role,
    };
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(userData));
    setUser(userData);
    return userData;
  }, []);

  const logout = useCallback(async () => {
    await AsyncStorage.removeItem(STORAGE_KEY);
    setUser(null);
  }, []);

  const isAdmin = user?.role === 'ADMIN';
  const isSuperviseur = user?.role === 'SUPERVISEUR';
  const isAgentLogistique = user?.role === 'AGENT_LOGISTIQUE';
  const isAgentCommercial = user?.role === 'AGENT_COMMERCIAL';
  const isCaissier = user?.role === 'CAISSIER';

  const canCreateTicket = isAdmin || isSuperviseur || isAgentCommercial;
  const canDistribute = isAdmin || isAgentLogistique;
  const canActivateTicket = isAdmin || isSuperviseur;
  const canManageUsers = isAdmin;
  const canViewAuditLogs = isAdmin;
  const canManageAlertes = isAdmin;
  const canCreateMouvement = isAdmin || isAgentLogistique;

  const value = {
    user,
    loading,
    login,
    logout,
    isAdmin,
    isSuperviseur,
    isAgentLogistique,
    isAgentCommercial,
    isCaissier,
    canCreateTicket,
    canDistribute,
    canActivateTicket,
    canManageUsers,
    canViewAuditLogs,
    canManageAlertes,
    canCreateMouvement,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
