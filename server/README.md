# Appear Lite Plus - Server

Flask-based server for handling alarm messaging from multiple input sources.

## Features

- **Serial Port Monitoring** - Monitor RS-232/USB serial connections
- **TAP over IP** - Telocator Alphanumeric Protocol server
- **Serial over IP** - TCP socket server for serial data
- **Web Admin Interface** - Configure settings and view alarm history
- **Real-time Notifications** - SocketIO integration for mobile apps
- **SQLite Database** - Store alarms and configuration

## Installation

### Raspberry Pi / Linux

```bash
cd server
chmod +x setup.sh
./setup.sh
```

### Windows / Manual Setup

```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` to configure:
   - Flask host/port
   - Serial port settings
   - TAP server settings
   - Serial over IP settings

## Running

```bash
python run.py
```

Access the web interface at `http://localhost:5000`

**Default credentials:** admin / admin

## API Endpoints

### GET /api/alarms/latest
Get recent alarms for mobile app
- Query params: `limit` (default: 50)

### POST /api/alarms/<alarm_id>/mark_sent
Mark alarm as sent to app

### GET /api/stats
Get alarm statistics

## SocketIO Events

Connect to `/app` namespace for real-time alarm updates:

```javascript
socket.on('new_alarm', (data) => {
  // Handle new alarm
});
```

## Testing

Send test alarms using the test script:

```bash
python test_alarm.py
```

## Project Structure

```
server/
├── src/
│   ├── app.py              # Main Flask application
│   ├── database/
│   │   └── db.py          # Database operations
│   ├── handlers/          # Alarm input handlers
│   │   ├── serial_handler.py
│   │   ├── tap_handler.py
│   │   └── serial_ip_handler.py
│   └── templates/         # HTML templates
├── data/                  # SQLite database
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── test_alarm.py         # Testing script
```
