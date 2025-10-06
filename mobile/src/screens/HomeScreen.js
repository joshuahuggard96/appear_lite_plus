import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  RefreshControl,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { fetchStats, fetchLatestAlarms } from '../services/apiService';
import { addAlarmListener } from '../services/socketService';

export default function HomeScreen() {
  const [stats, setStats] = useState(null);
  const [recentAlarms, setRecentAlarms] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    loadData();

    // Listen for real-time alarm updates
    const removeListener = addAlarmListener((newAlarm) => {
      setRecentAlarms(prev => [newAlarm, ...prev].slice(0, 5));
      // Update stats
      setStats(prev => ({
        ...prev,
        total: (prev?.total || 0) + 1
      }));
    });

    return () => removeListener();
  }, []);

  const loadData = async () => {
    try {
      const [statsData, alarmsData] = await Promise.all([
        fetchStats(),
        fetchLatestAlarms(5)
      ]);
      setStats(statsData);
      setRecentAlarms(alarmsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const onRefresh = () => {
    setIsRefreshing(true);
    loadData();
  };

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{stats?.total || 0}</Text>
          <Text style={styles.statLabel}>Total Alarms</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{stats?.sent_to_app || 0}</Text>
          <Text style={styles.statLabel}>Sent to App</Text>
        </View>
      </View>

      <View style={styles.sourcesContainer}>
        <Text style={styles.sectionTitle}>Alarm Sources</Text>
        {stats?.by_source && Object.entries(stats.by_source).map(([source, count]) => (
          <View key={source} style={styles.sourceRow}>
            <View style={[styles.sourceDot, { backgroundColor: getSourceColor(source) }]} />
            <Text style={styles.sourceName}>{formatSourceName(source)}</Text>
            <Text style={styles.sourceCount}>{count}</Text>
          </View>
        ))}
      </View>

      <View style={styles.recentContainer}>
        <Text style={styles.sectionTitle}>Recent Alarms</Text>
        {recentAlarms.length === 0 ? (
          <Text style={styles.emptyText}>No alarms yet</Text>
        ) : (
          recentAlarms.map((alarm) => (
            <View key={alarm.id} style={styles.alarmCard}>
              <View style={styles.alarmHeader}>
                <View style={[styles.sourceBadge, { backgroundColor: getSourceColor(alarm.source) }]}>
                  <Text style={styles.sourceBadgeText}>{formatSourceName(alarm.source)}</Text>
                </View>
                <Text style={styles.alarmTime}>
                  {formatTime(alarm.received_at)}
                </Text>
              </View>
              <Text style={styles.alarmMessage}>{alarm.message}</Text>
            </View>
          ))
        )}
      </View>
    </ScrollView>
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

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
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
  statsContainer: {
    flexDirection: 'row',
    padding: 15,
    gap: 15,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  sourcesContainer: {
    margin: 15,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  sourceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  sourceDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 10,
  },
  sourceName: {
    flex: 1,
    fontSize: 16,
    color: '#333',
  },
  sourceCount: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  recentContainer: {
    margin: 15,
    marginTop: 0,
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
  },
  emptyText: {
    textAlign: 'center',
    color: '#999',
    fontSize: 16,
    marginTop: 20,
  },
});
