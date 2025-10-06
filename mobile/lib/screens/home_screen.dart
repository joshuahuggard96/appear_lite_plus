import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/app_state.dart';
import '../models/alarm.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  Color _getSourceColor(String source) {
    switch (source) {
      case 'serial':
        return const Color(0xFFFF6B6B);
      case 'tap':
        return const Color(0xFF4ECDC4);
      case 'serial_ip':
        return const Color(0xFFFFE66D);
      default:
        return Colors.grey;
    }
  }

  String _formatSourceName(String source) {
    switch (source) {
      case 'serial':
        return 'Serial';
      case 'tap':
        return 'TAP';
      case 'serial_ip':
        return 'Serial/IP';
      default:
        return source;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Consumer<AppState>(
        builder: (context, appState, child) {
          if (appState.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          final stats = appState.stats;
          final recentAlarms = appState.alarms.take(5).toList();

          return RefreshIndicator(
            onRefresh: () => appState.loadData(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Stats Cards
                Row(
                  children: [
                    Expanded(
                      child: _StatCard(
                        title: 'Total Alarms',
                        value: stats?.total.toString() ?? '0',
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: _StatCard(
                        title: 'Sent to App',
                        value: stats?.sentToApp.toString() ?? '0',
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Alarm Sources
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Alarm Sources',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 12),
                        if (stats?.bySource.isEmpty ?? true)
                          const Text(
                            'No sources yet',
                            style: TextStyle(color: Colors.grey),
                          )
                        else
                          ...stats!.bySource.entries.map(
                            (entry) => Padding(
                              padding: const EdgeInsets.symmetric(vertical: 8),
                              child: Row(
                                children: [
                                  Container(
                                    width: 12,
                                    height: 12,
                                    decoration: BoxDecoration(
                                      color: _getSourceColor(entry.key),
                                      shape: BoxShape.circle,
                                    ),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      _formatSourceName(entry.key),
                                      style: const TextStyle(fontSize: 16),
                                    ),
                                  ),
                                  Text(
                                    entry.value.toString(),
                                    style: const TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.w600,
                                      color: Colors.grey,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                // Recent Alarms
                const Text(
                  'Recent Alarms',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                if (recentAlarms.isEmpty)
                  const Center(
                    child: Padding(
                      padding: EdgeInsets.all(20),
                      child: Text(
                        'No alarms yet',
                        style: TextStyle(color: Colors.grey),
                      ),
                    ),
                  )
                else
                  ...recentAlarms.map(
                    (alarm) => _AlarmCard(
                      alarm: alarm,
                      getSourceColor: _getSourceColor,
                      formatSourceName: _formatSourceName,
                    ),
                  ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;

  const _StatCard({
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Text(
              value,
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              title,
              style: const TextStyle(
                fontSize: 14,
                color: Colors.grey,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

class _AlarmCard extends StatelessWidget {
  final Alarm alarm;
  final Color Function(String) getSourceColor;
  final String Function(String) formatSourceName;

  const _AlarmCard({
    required this.alarm,
    required this.getSourceColor,
    required this.formatSourceName,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: getSourceColor(alarm.source),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    formatSourceName(alarm.source),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Text(
                  DateFormat.jm().format(alarm.receivedAt),
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              alarm.message,
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
