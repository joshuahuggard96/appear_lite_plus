import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { testConnection } from '../services/apiService';

export default function SetupScreen({ onSetupComplete }) {
  const [serverUrl, setServerUrl] = useState('http://192.168.1.100:5000');
  const [isLoading, setIsLoading] = useState(false);

  const handleConnect = async () => {
    if (!serverUrl) {
      Alert.alert('Error', 'Please enter a server URL');
      return;
    }

    setIsLoading(true);

    try {
      // Test connection
      const isConnected = await testConnection(serverUrl);

      if (!isConnected) {
        Alert.alert(
          'Connection Failed',
          'Could not connect to the server. Please check the URL and try again.'
        );
        setIsLoading(false);
        return;
      }

      // Save server URL
      await AsyncStorage.setItem('serverUrl', serverUrl);

      Alert.alert(
        'Success',
        'Connected to server successfully!',
        [{ text: 'OK', onPress: () => onSetupComplete(serverUrl) }]
      );
    } catch (error) {
      console.error('Setup error:', error);
      Alert.alert('Error', 'An error occurred during setup');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Appear Lite+</Text>
        <Text style={styles.subtitle}>Connect to your alarm server</Text>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Server URL</Text>
          <TextInput
            style={styles.input}
            value={serverUrl}
            onChangeText={setServerUrl}
            placeholder="http://192.168.1.100:5000"
            placeholderTextColor="#999"
            autoCapitalize="none"
            autoCorrect={false}
            keyboardType="url"
          />
          <Text style={styles.hint}>
            Enter the URL of your Appear Lite+ server
          </Text>
        </View>

        <TouchableOpacity
          style={[styles.button, isLoading && styles.buttonDisabled]}
          onPress={handleConnect}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Connect</Text>
          )}
        </TouchableOpacity>

        <Text style={styles.footer}>
          Make sure your device is on the same network as the server
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#007AFF',
  },
  subtitle: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 50,
    color: '#666',
  },
  inputContainer: {
    marginBottom: 30,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    fontSize: 16,
    color: '#333',
  },
  hint: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  footer: {
    fontSize: 14,
    textAlign: 'center',
    color: '#999',
  },
});
