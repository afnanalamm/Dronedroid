import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import React, { useEffect, useState, useRef } from 'react';
import { Accelerometer } from 'expo-sensors';
import io from 'socket.io-client'; // Import after install

const server = 'http://192.168.1.122:5001'; // Your server IP:port
const updateInterval = 200; // ms between emits (e.g., ~3.3 Hz)

export default function App() {
  const [accel, setAccel] = useState({ x: 0, y: 0 });
  const latestAccel = useRef({ x: 0, y: 0 });
  const socketRef = useRef(null);

  useEffect(() => {
    // Connect to WebSocket
    socketRef.current = io(server, {
      transports: ['websocket'], // Force WebSocket (safer, avoids polling fallback)
      reconnection: true, // Auto-reconnect on drops
      reconnectionAttempts: 5,
      timeout: 20000,
    });

    socketRef.current.on('connect', () => {
      console.log('Connected to WebSocket');
    });

    socketRef.current.on('connect_error', (err) => {
      console.log('Connection error:', err.message);
    });

    // Accelerometer setup: Listen frequently for fresh data
    Accelerometer.setUpdateInterval(50); // 20 Hz for responsive capture
    const subscription = Accelerometer.addListener(({ x, y }) => {
      latestAccel.current = { x: Math.round(x * 100) / 100, y: Math.round(y * 100) / 100 }; // Round to 2 decimals
      setAccel({ x, y }); // For UI only
    });

    // Periodic emit: Send latest data every 300ms
    const interval = setInterval(() => {
      if (socketRef.current && socketRef.current.connected) {
        socketRef.current.emit('accel', latestAccel.current);
      }
    }, updateInterval);

    return () => {
      subscription.remove();
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
      clearInterval(interval);
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text>X: {accel.x.toFixed(2)}</Text>
      <Text>Y: {accel.y.toFixed(2)}</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#d0c900ff',
  },
});