class Alarm {
  final int id;
  final String source;
  final String message;
  final String? rawData;
  final DateTime receivedAt;
  final bool sentToApp;

  Alarm({
    required this.id,
    required this.source,
    required this.message,
    this.rawData,
    required this.receivedAt,
    this.sentToApp = false,
  });

  factory Alarm.fromJson(Map<String, dynamic> json) {
    return Alarm(
      id: json['id'],
      source: json['source'],
      message: json['message'],
      rawData: json['raw_data'],
      receivedAt: DateTime.parse(json['received_at']),
      sentToApp: json['sent_to_app'] == 1,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'source': source,
      'message': message,
      'raw_data': rawData,
      'received_at': receivedAt.toIso8601String(),
      'sent_to_app': sentToApp ? 1 : 0,
    };
  }
}

class AlarmStats {
  final int total;
  final int sentToApp;
  final Map<String, int> bySource;

  AlarmStats({
    required this.total,
    required this.sentToApp,
    required this.bySource,
  });

  factory AlarmStats.fromJson(Map<String, dynamic> json) {
    return AlarmStats(
      total: json['total'] ?? 0,
      sentToApp: json['sent_to_app'] ?? 0,
      bySource: Map<String, int>.from(json['by_source'] ?? {}),
    );
  }
}
