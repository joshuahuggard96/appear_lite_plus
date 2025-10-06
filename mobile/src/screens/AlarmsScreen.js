import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
  TouchableOpacity,
} from 'react-native';
import { fetchLatestAlarms } from '../services/apiService';
import { addAlarmListener } from '../services/socketService';

export default function AlarmsScreen() {
  const [alarms, setAlarms] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadAlarms();

    // Listen for real-time updates
    const removeListener = addAlarmListener((newAlarm) => {
      setAlarms(prev => [newAlarm, ...prev]);
    });

    return () => removeListener();
  }, []);

  const loadAlarms = async () => {
    try {
      const data = await fetchLatestAlarms(100);
      setAlarms(data);
    } catch (error) {
      console.error('Error loading alarms:', error);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const onRefresh = () => {
    setIsRefreshing(true);
    loadAlarms();
  };

  const getFilteredAlarms = () => {
    if (filter === 'all') return alarms;
    return alarms.filter(alarm => alarm.source === filter);
  };

  const renderAlarmItem = ({ item }) => (
    <View style={styles.alarmCard}>
      <View style={styles.alarmHeader}>
        <View style={[styles.sourceBadge, { backgroundColor: getSourceColor(item.source) }]}>
          <Text style={styles.sourceBadgeText}>{formatSourceName(item.source)}</Text>
        </View>
        <Text style={styles.alarmTime}>
          {formatDateTime(item.received_at)}
        </Text>
      </View>
      <Text style={styles.alarmMessage}>{item.message}</Text>
      {item.raw_data && item.raw_data !== item.message && (
        <Text style={styles.rawData}>Raw: {item.raw_data}</Text>
      )}
    </View>
  );

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.filterContainer}>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'all' && styles.filterButtonActive]}
          onPress={() => setFilter('all')}
        >
          <Text style={[styles.filterText, filter === 'all' && styles.filterTextActive]}>
            All
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'serial' && styles.filterButtonActive]}
          onPress={() => setFilter('serial')}
        >
          <Text style={[styles.filterText, filter === 'serial' && styles.filterTextActive]}>
            Serial
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'tap' && styles.filterButtonActive]}
          onPress={() => setFilter('tap')}
        >
          <Text style={[styles.filterText, filter === 'tap' && styles.filterTextActive]}>
            TAP
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'serial_ip' && styles.filterButtonActive]}
          onPress={() => setFilter('serial_ip')}
        >
          <Text style={[styles.filterText, filter === 'serial_ip' && styles.filterTextActive]}>
            Serial/IP
          </Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={getFilteredAlarms()}
        renderItem={renderAlarmItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <Text style={styles.emptyText}>No alarms found</Text>
        }
      />
    </View>
  );
}

const getSourceColor = (source) => {
  const colors = {
    serial: '#ff6b6b',
    tap: '#4ecdc4',
    serial_ip: '#ffe66d',
  };
  return colors[source] || '#999';
};

const formatSourceName = (source) => {
  const names = {
    serial: 'Serial',
    tap: 'TAP',
    serial_ip: 'Serial/IP',
  };
  return names[source] || source;
};

const formatDateTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  filterContainer: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  filterButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginHorizontal: 4,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  filterButtonActive: {
    backgroundColor: '#007AFF',
  },
  filterText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  filterTextActive: {
    color: '#fff',
  },
  listContent: {
    padding: 15,
  },
  alarmCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  alarmHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  sourceBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  sourceBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  alarmTime: {
    fontSize: 12,
    color: '#999',
  },
  alarmMessage: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
  },
  rawData: {
    fontSize: 12,
    color: '#999',
    fontStyle: 'italic',
  },
  emptyText: {
    textAlign: 'center',
    color: '#999',
    fontSize: 16,
    marginTop: 50,
  },
});
