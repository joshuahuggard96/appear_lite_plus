import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/alarm.dart';
import 'api_service.dart';
import 'socket_service.dart';

class AppState extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final SocketService _socketService = SocketService();

  String? _serverUrl;
  List<Alarm> _alarms = [];
  AlarmStats? _stats;
  bool _isLoading = false;

  String? get serverUrl => _serverUrl;
  List<Alarm> get alarms => _alarms;
  AlarmStats? get stats => _stats;
  bool get isLoading => _isLoading;
  bool get isConnected => _serverUrl != null;

  ApiService get apiService => _apiService;
  SocketService get socketService => _socketService;

  Future<void> initialize() async {
    final prefs = await SharedPreferences.getInstance();
    _serverUrl = prefs.getString('serverUrl');

    if (_serverUrl != null) {
      _apiService.setBaseUrl(_serverUrl!);
      _socketService.connect(_serverUrl!);
      _setupSocketListener();
      await loadData();
    }

    notifyListeners();
  }

  Future<bool> setServerUrl(String url) async {
    // Test connection
    final isValid = await _apiService.testConnection(url);

    if (!isValid) {
      return false;
    }

    // Save URL
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('serverUrl', url);

    _serverUrl = url;
    _apiService.setBaseUrl(url);
    _socketService.connect(url);
    _setupSocketListener();

    await loadData();
    notifyListeners();

    return true;
  }

  Future<void> disconnect() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('serverUrl');

    _serverUrl = null;
    _alarms = [];
    _stats = null;
    _socketService.disconnect();

    notifyListeners();
  }

  Future<void> loadData() async {
    if (_serverUrl == null) return;

    _isLoading = true;
    notifyListeners();

    try {
      final results = await Future.wait([
        _apiService.fetchLatestAlarms(limit: 100),
        _apiService.fetchStats(),
      ]);

      _alarms = results[0] as List<Alarm>;
      _stats = results[1] as AlarmStats;
    } catch (e) {
      print('Error loading data: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _setupSocketListener() {
    _socketService.addAlarmListener((alarm) {
      _alarms.insert(0, alarm);

      // Update stats
      if (_stats != null) {
        _stats = AlarmStats(
          total: _stats!.total + 1,
          sentToApp: _stats!.sentToApp,
          bySource: {
            ..._stats!.bySource,
            alarm.source: (_stats!.bySource[alarm.source] ?? 0) + 1,
          },
        );
      }

      notifyListeners();
    });
  }

  List<Alarm> getFilteredAlarms(String filter) {
    if (filter == 'all') return _alarms;
    return _alarms.where((alarm) => alarm.source == filter).toList();
  }
}
