import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

let apiClient = null;

export const initializeApi = async () => {
  const serverUrl = await AsyncStorage.getItem('serverUrl');
  if (!serverUrl) {
    throw new Error('Server URL not configured');
  }

  apiClient = axios.create({
    baseURL: serverUrl,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return apiClient;
};

export const getApiClient = async () => {
  if (!apiClient) {
    await initializeApi();
  }
  return apiClient;
};

export const fetchLatestAlarms = async (limit = 50) => {
  try {
    const client = await getApiClient();
    const response = await client.get('/api/alarms/latest', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching alarms:', error);
    throw error;
  }
};

export const fetchStats = async () => {
  try {
    const client = await getApiClient();
    const response = await client.get('/api/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const markAlarmAsSent = async (alarmId) => {
  try {
    const client = await getApiClient();
    const response = await client.post(`/api/alarms/${alarmId}/mark_sent`);
    return response.data;
  } catch (error) {
    console.error('Error marking alarm as sent:', error);
    throw error;
  }
};

export const testConnection = async (serverUrl) => {
  try {
    const response = await axios.get(`${serverUrl}/api/stats`, {
      timeout: 5000
    });
    return response.status === 200;
  } catch (error) {
    console.error('Connection test failed:', error);
    return false;
  }
};
