import io from 'socket.io-client';

let socket = null;
let alarmListeners = [];

export const initializeSocket = (serverUrl) => {
  if (socket) {
    socket.disconnect();
  }

  console.log('Connecting to server:', serverUrl);

  socket = io(serverUrl + '/app', {
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 10
  });

  socket.on('connect', () => {
    console.log('Connected to server');
    socket.emit('subscribe', { app: 'mobile' });
  });

  socket.on('connected', (data) => {
    console.log('Server acknowledged connection:', data);
  });

  socket.on('subscribed', (data) => {
    console.log('Subscribed:', data);
  });

  socket.on('new_alarm', (alarm) => {
    console.log('New alarm received:', alarm);
    notifyAlarmListeners(alarm);
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from server');
  });

  socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
  });

  return socket;
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const getSocket = () => socket;

export const addAlarmListener = (callback) => {
  alarmListeners.push(callback);
  return () => {
    alarmListeners = alarmListeners.filter(cb => cb !== callback);
  };
};

const notifyAlarmListeners = (alarm) => {
  alarmListeners.forEach(callback => callback(alarm));
};
