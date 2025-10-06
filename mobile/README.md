# Appear Lite Plus - Mobile App

React Native mobile application for iOS and Android to receive real-time alarm notifications from the Appear Lite Plus server.

## Features

- **Real-time Notifications** - Receive alarms instantly via SocketIO
- **Alarm History** - View and filter all received alarms
- **Dashboard** - See statistics and recent activity
- **Multi-source Support** - Display alarms from Serial, TAP, and Serial/IP sources
- **Cross-platform** - Works on both iOS and Android

## Prerequisites

- Node.js 16+ and npm
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (Mac only) or Android Studio (for Android development)
- Expo Go app on your phone (for testing on physical device)

## Installation

1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the App

### Development Server

Start the Expo development server:

```bash
npm start
```

This will open the Expo DevTools in your browser.

### iOS Simulator (Mac only)

```bash
npm run ios
```

### Android Emulator

```bash
npm run android
```

### Physical Device

1. Install **Expo Go** from the App Store (iOS) or Play Store (Android)
2. Run `npm start`
3. Scan the QR code with your phone's camera (iOS) or Expo Go app (Android)

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
├── src/
│   ├── screens/          # App screens
│   │   ├── SetupScreen.js      # Initial server setup
│   │   ├── HomeScreen.js       # Dashboard with stats
│   │   ├── AlarmsScreen.js     # Alarm history list
│   │   └── SettingsScreen.js   # App settings
│   ├── services/         # API and socket services
│   │   ├── apiService.js       # REST API calls
│   │   └── socketService.js    # SocketIO connection
│   └── components/       # Reusable components (future use)
├── assets/               # Images and icons
├── App.js                # Main app entry point
├── app.json              # Expo configuration
└── package.json          # Dependencies
```

## API Integration

The app connects to the server's API endpoints:

- `GET /api/alarms/latest` - Fetch alarm history
- `GET /api/stats` - Get alarm statistics
- SocketIO `/app` namespace - Real-time alarm updates

## Screens

### Home Screen
- Statistics cards (total alarms, sent to app)
- Alarm source breakdown
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

## Troubleshooting

### Cannot connect to server

1. Verify your phone and server are on the same network
2. Check the server URL is correct (include `http://` and port)
3. Make sure the server is running (`python run.py` in server directory)
4. Check firewall settings on the Raspberry Pi

### Real-time updates not working

1. Check SocketIO connection in Settings
2. Verify the server is running
3. Try disconnecting and reconnecting from Settings

### App won't start

```bash
# Clear Expo cache
expo start -c

# Or reinstall dependencies
rm -rf node_modules
npm install
```

## Building for Production

### iOS

```bash
expo build:ios
```

You'll need an Apple Developer account ($99/year).

### Android

```bash
expo build:android
```

You can use a free Google Play Developer account.

## Future Enhancements

- Push notifications (when app is in background)
- Alarm acknowledgment
- Custom notification sounds
- Multiple server support
- Dark mode
- Alarm filtering and search

## License

MIT
