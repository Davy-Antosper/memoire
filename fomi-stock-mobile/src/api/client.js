import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_URL } from '../config';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  async (config) => {
    try {
      const userData = await AsyncStorage.getItem('fomi_user');
      if (userData) {
        const user = JSON.parse(userData);
        if (user.token) {
          config.headers.Authorization = `Bearer ${user.token}`;
        }
      }
    } catch (e) {}
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      try {
        await AsyncStorage.removeItem('fomi_user');
      } catch (e) {}
    }
    return Promise.reject(error);
  }
);

export const get = (url, config = {}) => apiClient.get(url, config);
export const post = (url, data, config = {}) => apiClient.post(url, data, config);
export const put = (url, data, config = {}) => apiClient.put(url, data, config);
export const patch = (url, data, config = {}) => apiClient.patch(url, data, config);
export const del = (url, config = {}) => apiClient.delete(url, config);

export default apiClient;
