import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/alarm.dart';

class ApiService {
  String? _baseUrl;

  void setBaseUrl(String url) {
    _baseUrl = url;
  }

  String? get baseUrl => _baseUrl;

  Future<bool> testConnection(String url) async {
    try {
      final response = await http
          .get(Uri.parse('$url/api/stats'))
          .timeout(const Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      print('Connection test failed: $e');
      return false;
    }
  }

  Future<List<Alarm>> fetchLatestAlarms({int limit = 50}) async {
    if (_baseUrl == null) {
      throw Exception('Base URL not set');
    }

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/alarms/latest?limit=$limit'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => Alarm.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load alarms');
      }
    } catch (e) {
      print('Error fetching alarms: $e');
      rethrow;
    }
  }

  Future<AlarmStats> fetchStats() async {
    if (_baseUrl == null) {
      throw Exception('Base URL not set');
    }

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/stats'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return AlarmStats.fromJson(data);
      } else {
        throw Exception('Failed to load stats');
      }
    } catch (e) {
      print('Error fetching stats: $e');
      rethrow;
    }
  }

  Future<void> markAlarmAsSent(int alarmId) async {
    if (_baseUrl == null) {
      throw Exception('Base URL not set');
    }

    try {
      await http.post(
        Uri.parse('$_baseUrl/api/alarms/$alarmId/mark_sent'),
      );
    } catch (e) {
      print('Error marking alarm as sent: $e');
      rethrow;
    }
  }
}
