# Appear Lite Plus

Complete alarm messaging system for Raspberry Pi with iOS and Android mobile app support.

## Project Structure

This is a monorepo containing both the server and mobile applications:

```
appear_lite_plus/
├── server/          # Flask backend server (Python)
│   ├── src/        # Application source code
│   ├── data/       # SQLite database
│   └── README.md   # Server documentation
│
└── mobile/         # React Native mobile app (iOS/Android)
    └── README.md   # Mobile app documentation
```

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

## Quick Start

### Server Setup

1. Navigate to server directory:
   ```bash
   cd server
   ```

2. Run the setup script (Raspberry Pi/Linux):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually (Windows/Mac):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. Start the server:
   ```bash
   python run.py
   ```

4. Access the web interface at `http://localhost:5000`
   **Default login:** admin / admin

### Mobile App Setup

1. Navigate to mobile directory:
   ```bash
   cd mobile
   ```

2. Follow the [mobile README](mobile/README.md) for installation and setup

For detailed setup instructions, see the [server README](server/README.md) or [mobile README](mobile/README.md).

## Architecture

```
┌─────────────────┐
│  Alarm Sources  │
│  - Serial Port  │
│  - TAP over IP  │
│  - Serial/IP    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Server   │
│  (Raspberry Pi) │
│  - REST API     │
│  - SocketIO     │
│  - SQLite DB    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Mobile Apps   │
│  - iOS          │
│  - Android      │
└─────────────────┘
```

## API Overview

The server provides:
- **REST API** for alarm retrieval and management
- **SocketIO** for real-time push notifications
- **Web Admin** for configuration and monitoring

See [server README](server/README.md) for full API documentation.

## License

[Specify your license here]

## Support

For issues and questions, please create an issue on the GitHub repository.
