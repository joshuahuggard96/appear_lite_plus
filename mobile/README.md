# Appear Lite Plus - Mobile App

Flutter mobile application for iOS and Android to receive real-time alarm notifications from the Appear Lite Plus server.

## Features

- **Real-time Notifications** - Receive alarms instantly via SocketIO
- **Alarm History** - View and filter all received alarms
- **Dashboard** - See statistics and recent activity
- **Multi-source Support** - Display alarms from Serial, TAP, and Serial/IP sources
- **Cross-platform** - Single codebase for both iOS and Android

## Prerequisites

- Flutter SDK 3.0.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio (for Android development)
- Xcode (for iOS development, Mac only)

## Installation

1. **Install Flutter**

   Follow the official Flutter installation guide:
   - [Flutter installation](https://docs.flutter.dev/get-started/install)

2. **Navigate to the mobile directory:**
   ```bash
   cd mobile
   ```

3. **Install dependencies:**
   ```bash
   flutter pub get
   ```

## Running the App

### Check Flutter setup
```bash
flutter doctor
```

### Run on Android
```bash
flutter run
```

### Run on iOS (Mac only)
```bash
flutter run
```

### Run on specific device
```bash
# List available devices
flutter devices

# Run on specific device
flutter run -d <device-id>
```

## First Time Setup

When you first open the app, you'll be prompted to enter your server URL:

1. Make sure your phone is on the same network as the Raspberry Pi server
2. Enter the server URL (e.g., `http://192.168.1.100:5000`)
3. Tap "Connect"

The app will test the connection and save the server URL if successful.

## Configuration

You can change the server URL at any time from the Settings screen.

## Project Structure

```
mobile/
├── lib/
│   ├── main.dart             # App entry point and navigation
│   ├── models/
│   │   └── alarm.dart        # Alarm data models
│   ├── services/
│   │   ├── api_service.dart      # REST API client
│   │   ├── socket_service.dart   # SocketIO client
│   │   └── app_state.dart        # App state management
│   ├── screens/
│   │   ├── setup_screen.dart     # Initial server setup
│   │   ├── home_screen.dart      # Dashboard with stats
│   │   ├── alarms_screen.dart    # Alarm history list
│   │   └── settings_screen.dart  # App settings
│   └── widgets/              # Reusable widgets (future use)
├── android/                  # Android-specific files
├── ios/                      # iOS-specific files
└── pubspec.yaml              # Dependencies
```

## Dependencies

- **provider** - State management
- **http** - REST API calls
- **socket_io_client** - Real-time WebSocket connection
- **shared_preferences** - Persistent storage
- **intl** - Date/time formatting

## API Integration

The app connects to the server's API endpoints:

- `GET /api/alarms/latest` - Fetch alarm history
- `GET /api/stats` - Get alarm statistics
- SocketIO `/app` namespace - Real-time alarm updates

## Screens

### Setup Screen
- Initial connection setup
- Server URL validation
- Connection testing

### Home Screen
- Statistics cards (total alarms, sent to app)
- Alarm source breakdown with color coding
- 5 most recent alarms with real-time updates

### Alarms Screen
- Full list of all alarms (up to 100)
- Filter by source (All, Serial, TAP, Serial/IP)
- Pull to refresh
- Real-time updates

### Settings Screen
- Change server URL
- View app version
- Disconnect from server

## Building for Production

### Android

1. **Generate release keystore:**
   ```bash
   keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   ```

2. **Create `android/key.properties`:**
   ```properties
   storePassword=<password>
   keyPassword=<password>
   keyAlias=upload
   storeFile=<path-to-keystore>
   ```

3. **Build APK:**
   ```bash
   flutter build apk --release
   ```

4. **Build App Bundle (for Play Store):**
   ```bash
   flutter build appbundle --release
   ```

### iOS

1. **Open Xcode:**
   ```bash
   open ios/Runner.xcworkspace
   ```

2. **Configure signing** in Xcode (requires Apple Developer account)

3. **Build:**
   ```bash
   flutter build ios --release
   ```

## Troubleshooting

### Cannot connect to server

1. Verify your phone and server are on the same network
2. Check the server URL is correct (include `http://` and port)
3. Make sure the server is running (`python run.py` in server directory)
4. Check firewall settings on the Raspberry Pi

### Real-time updates not working

1. Check SocketIO connection in app logs
2. Verify the server is running
3. Try disconnecting and reconnecting from Settings

### Build errors

```bash
# Clean build
flutter clean

# Get dependencies again
flutter pub get

# Rebuild
flutter run
```

### Android build issues

```bash
# Update Android licenses
flutter doctor --android-licenses
```

## Development

### Hot Reload
Press `r` in the terminal while app is running to hot reload changes.

### Hot Restart
Press `R` in the terminal to hot restart the app.

### Debug Mode
```bash
flutter run --debug
```

### Release Mode
```bash
flutter run --release
```

## Future Enhancements

- Push notifications (Firebase Cloud Messaging)
- Alarm acknowledgment
- Custom notification sounds
- Multiple server support
- Dark mode
- Alarm filtering and search
- Offline mode with local storage

## License

MIT
