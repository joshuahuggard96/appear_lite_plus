import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/app_state.dart';
import '../models/alarm.dart';

class AlarmsScreen extends StatefulWidget {
  const AlarmsScreen({super.key});

  @override
  State<AlarmsScreen> createState() => _AlarmsScreenState();
}

class _AlarmsScreenState extends State<AlarmsScreen> {
  String _selectedFilter = 'all';

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
        title: const Text('Alarms'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Consumer<AppState>(
        builder: (context, appState, child) {
          final alarms = appState.getFilteredAlarms(_selectedFilter);

          return Column(
            children: [
              // Filter Buttons
              Container(
                padding: const EdgeInsets.all(16),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  border: Border(
                    bottom: BorderSide(color: Colors.grey, width: 0.5),
                  ),
                ),
                child: Row(
                  children: [
                    _FilterButton(
                      label: 'All',
                      isSelected: _selectedFilter == 'all',
                      onTap: () => setState(() => _selectedFilter = 'all'),
                    ),
                    const SizedBox(width: 8),
                    _FilterButton(
                      label: 'Serial',
                      isSelected: _selectedFilter == 'serial',
                      onTap: () => setState(() => _selectedFilter = 'serial'),
                    ),
                    const SizedBox(width: 8),
                    _FilterButton(
                      label: 'TAP',
                      isSelected: _selectedFilter == 'tap',
                      onTap: () => setState(() => _selectedFilter = 'tap'),
                    ),
                    const SizedBox(width: 8),
                    _FilterButton(
                      label: 'Serial/IP',
                      isSelected: _selectedFilter == 'serial_ip',
                      onTap: () => setState(() => _selectedFilter = 'serial_ip'),
                    ),
                  ],
                ),
              ),

              // Alarms List
              Expanded(
                child: RefreshIndicator(
                  onRefresh: () => appState.loadData(),
                  child: alarms.isEmpty
                      ? const Center(
                          child: Text(
                            'No alarms found',
                            style: TextStyle(
                              fontSize: 16,
                              color: Colors.grey,
                            ),
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.all(16),
                          itemCount: alarms.length,
                          itemBuilder: (context, index) {
                            final alarm = alarms[index];
                            return _AlarmCard(
                              alarm: alarm,
                              getSourceColor: _getSourceColor,
                              formatSourceName: _formatSourceName,
                            );
                          },
                        ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _FilterButton extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _FilterButton({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? Colors.blue : Colors.grey[200],
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: isSelected ? Colors.white : Colors.grey[700],
            ),
            textAlign: TextAlign.center,
          ),
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
      elevation: 2,
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
                  DateFormat('yyyy-MM-dd HH:mm:ss').format(alarm.receivedAt),
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
            if (alarm.rawData != null && alarm.rawData != alarm.message) ...[
              const SizedBox(height: 8),
              Text(
                'Raw: ${alarm.rawData}',
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                  fontStyle: FontStyle.italic,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
