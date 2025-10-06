# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Appear Lite Plus is a Raspberry Pi-based alarm messaging system that receives alarms from multiple sources (Serial, TAP over IP) and forwards them to mobile applications. It features a web-based admin interface for configuration and monitoring.

## Technology Stack

- **Backend**: Python 3.7+ with Flask
- **Real-time Communication**: Flask-SocketIO
- **Database**: SQLite3
- **Web UI**: Bootstrap 5 with Jinja2 templates
- **Serial Communication**: pyserial
- **Authentication**: Flask-Login with bcrypt

## Project Structure

```
src/
├── app.py                 # Main Flask application, routes, and SocketIO events
├── database/
│   └── db.py             # Database abstraction layer (SQLite)
├── handlers/
│   ├── serial_handler.py # Serial port monitoring in background thread
│   └── tap_handler.py    # TAP over IP server (TCP socket server)
└── templates/            # Jinja2 HTML templates
    ├── base.html         # Base template with navigation
    ├── login.html        # Login page
    ├── dashboard.html    # Main dashboard with stats
    ├── alarms.html       # Alarm history table
    └── settings.html     # Configuration interface
```

## Common Commands

### Setup and Installation
```bash
# First time setup
chmod +x setup.sh
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "from src.database.db import Database; db = Database()"
```

### Running the Application
```bash
# Development
python run.py

# Production (with systemd recommended)
# See setup.sh for environment setup
```

### Database Operations
```bash
# Initialize database (auto-creates tables and default admin user)
python -c "from src.database.db import Database; db = Database()"

# Database location: data/appear.db
```

## Key Architecture Patterns

### Handler System
The application uses a modular handler pattern for alarm sources:
- Each handler runs in its own background thread
- Handlers register a callback function to notify the app of new alarms
- Alarms are saved to database and broadcast via SocketIO
- Handlers can be started/stopped via settings interface

### Alarm Flow
1. Handler receives data (serial or TAP)
2. Data is parsed and saved to database (src/database/db.py)
3. Callback triggers app notification
4. Alarm is broadcast to connected mobile apps via SocketIO (namespace: `/app`)
5. Web admin can view alarm history

### Adding New Alarm Sources
1. Create new handler in `src/handlers/`
2. Implement `start()`, `stop()`, and `is_running()` methods
3. Use background threading for continuous monitoring
4. Call `alarm_callback()` when alarm received
5. Register handler in `src/app.py` `start_handlers()` function
6. Add configuration settings to database

### Database Schema
- **users**: Admin authentication (default: admin/admin)
- **settings**: Key-value configuration store
- **alarms**: Alarm history with source, message, timestamps
- **alarm_rules**: Future feature for alarm processing rules

### SocketIO Namespaces
- `/app`: Mobile app real-time alarm notifications
  - Events: `connect`, `disconnect`, `subscribe`, `new_alarm`

### API Endpoints for Mobile Apps
- `GET /api/alarms/latest?limit=50` - Recent alarms
- `GET /api/stats` - Alarm statistics
- `POST /api/alarms/<id>/mark_sent` - Mark alarm as delivered

### Configuration
All runtime settings stored in database `settings` table, configurable via web interface. Environment variables in `.env` for server-level config only (ports, debug mode).

### Serial Port Handler (src/handlers/serial_handler.py)
- Runs in daemon thread
- Automatic reconnection on serial errors
- Configurable port and baud rate
- Line-based reading (waits for newline)

### TAP Handler (src/handlers/tap_handler.py)
- TCP server accepting multiple concurrent clients
- TAP protocol: ESC EOT (\x1b\x04) message delimiter
- Sends ACK (\x06) after each message
- Each client handled in separate thread

## Development Notes

- All handlers must be thread-safe
- Database connections are per-query (SQLite threading limitation)
- SocketIO uses eventlet for async support
- Web templates use Bootstrap 5 for responsive UI
- Login required decorator protects admin routes
- Session-based authentication (change SECRET_KEY in production)

## Raspberry Pi Specific

- Serial ports typically: `/dev/ttyUSB0`, `/dev/ttyAMA0`
- User must be in `dialout` group for serial access: `sudo usermod -a -G dialout $USER`
- Systemd service recommended for auto-start
- Consider watchdog for production reliability
