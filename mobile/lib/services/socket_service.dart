import 'package:socket_io_client/socket_io_client.dart' as IO;
import '../models/alarm.dart';

class SocketService {
  IO.Socket? _socket;
  final List<Function(Alarm)> _alarmListeners = [];

  void connect(String serverUrl) {
    disconnect();

    print('Connecting to socket: $serverUrl');

    _socket = IO.io(
      '$serverUrl/app',
      IO.OptionBuilder()
          .setTransports(['websocket'])
          .enableReconnection()
          .setReconnectionDelay(1000)
          .setReconnectionAttempts(10)
          .build(),
    );

    _socket?.on('connect', (_) {
      print('Socket connected');
      _socket?.emit('subscribe', {'app': 'mobile'});
    });

    _socket?.on('connected', (data) {
      print('Server acknowledged connection: $data');
    });

    _socket?.on('subscribed', (data) {
      print('Subscribed: $data');
    });

    _socket?.on('new_alarm', (data) {
      print('New alarm received: $data');
      try {
        final alarm = Alarm.fromJson(data);
        _notifyAlarmListeners(alarm);
      } catch (e) {
        print('Error parsing alarm: $e');
      }
    });

    _socket?.on('disconnect', (_) {
      print('Socket disconnected');
    });

    _socket?.on('connect_error', (error) {
      print('Connection error: $error');
    });

    _socket?.connect();
  }

  void disconnect() {
    _socket?.disconnect();
    _socket?.dispose();
    _socket = null;
  }

  void addAlarmListener(Function(Alarm) listener) {
    _alarmListeners.add(listener);
  }

  void removeAlarmListener(Function(Alarm) listener) {
    _alarmListeners.remove(listener);
  }

  void _notifyAlarmListeners(Alarm alarm) {
    for (var listener in _alarmListeners) {
      listener(alarm);
    }
  }

  bool get isConnected => _socket?.connected ?? false;
}
