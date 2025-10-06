# Appear Lite Plus

A Raspberry Pi-based alarm messaging system that receives alarms via Serial or TAP over IP and forwards them to a mobile application.

## Features

- **Multiple Input Sources**
  - Serial port monitoring (RS-232, USB Serial)
  - TAP (Telocator Alphanumeric Protocol) over IP

- **Web Admin Interface**
  - User authentication (default: admin/admin)
  - Real-time dashboard with alarm statistics
  - Alarm history viewer
  - Configuration management

- **Mobile App Integration**
  - RESTful API for alarm retrieval
  - WebSocket support for real-time notifications
  - Easy integration with future mobile apps

- **Modular & Extensible**
  - Plugin-based architecture
  - Easy to add new alarm sources
  - Configurable alarm processing rules

## System Requirements

- Raspberry Pi (3B+ or newer recommended)
- Python 3.7 or higher
- Network connectivity (for TAP over IP and mobile app communication)
- Serial port (optional, for serial alarm sources)

## Installation

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd appear_lite_plus

# Run setup script
chmod +x setup.sh
./setup.sh

# Copy and configure environment variables
cp .env.example .env
nano .env

# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from src.database.db import Database; db = Database()"

# Create .env file
cp .env.example .env

# Run the application
python run.py
```

## Configuration

Edit the `.env` file to configure the system:

```ini
# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Serial Configuration
SERIAL_ENABLED=true
SERIAL_PORT=/dev/ttyUSB0
SERIAL_BAUD_RATE=9600

# TAP over IP Configuration
TAP_ENABLED=true
TAP_PORT=18001
TAP_HOST=0.0.0.0
```

## Usage

### Starting the Server

```bash
python run.py
```

The web interface will be available at `http://localhost:5000`

Default login credentials:
- Username: `admin`
- Password: `admin`

### Web Admin Interface

- **Dashboard**: View system statistics and status
- **Alarms**: Browse alarm history
- **Settings**: Configure serial and TAP settings

### Mobile App Integration

The system provides API endpoints for mobile app integration:

- `GET /api/alarms/latest?limit=50` - Get recent alarms
- `GET /api/stats` - Get alarm statistics
- `POST /api/alarms/<id>/mark_sent` - Mark alarm as sent

WebSocket endpoint for real-time updates:
- `ws://localhost:5000/socket.io/?EIO=4&transport=websocket` (namespace: `/app`)

## Project Structure

```
appear_lite_plus/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── database/
│   │   └── db.py              # Database handler
│   ├── handlers/
│   │   ├── serial_handler.py  # Serial port monitoring
│   │   └── tap_handler.py     # TAP over IP handler
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── alarms.html
│       └── settings.html
├── data/                      # Database files (auto-created)
├── logs/                      # Log files (auto-created)
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
└── .env                       # Configuration (create from .env.example)
```

## Development

### Adding New Alarm Sources

Create a new handler in `src/handlers/`:

```python
class CustomHandler:
    def __init__(self, alarm_callback=None):
        self.alarm_callback = alarm_callback

    def start(self):
        # Start monitoring
        pass

    def _process_alarm(self, data):
        # Save to database and trigger callback
        alarm_id = db.save_alarm('custom', data)
        if self.alarm_callback:
            self.alarm_callback({'id': alarm_id, 'source': 'custom', 'message': data})
```

Register in `src/app.py`:
```python
custom_handler = CustomHandler(alarm_callback)
custom_handler.start()
```

## Troubleshooting

### Serial Port Issues

- Check port permissions: `sudo usermod -a -G dialout $USER` (logout/login required)
- Verify port exists: `ls -l /dev/ttyUSB*` or `ls -l /dev/ttyAMA*`
- Check port availability: `sudo dmesg | grep tty`

### TAP Connection Issues

- Verify firewall allows port 18001
- Check if port is already in use: `netstat -tuln | grep 18001`

## License

[Specify your license here]

## Support

For issues and questions, please create an issue on the GitHub repository.
