import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import React, { useEffect, useState } from 'react';
import { Accelerometer } from 'expo-sensors';

// Different server addresses for different setup locations

const server = 'http://192.168.1.122:5001'; // PC on home wifi
// const server = 'http://192.168.1.122:5001'; // RPi on home wifi
// const server = 'http://10.30.12.63:5001'; // RPi on school wifi


export default function App() {
  const updateInterval =300; // sensor update interval in milliseconds
  

  const [accel, setAccel] = useState({ x: 0, y: 0 });

  useEffect(() => {
    Accelerometer.setUpdateInterval(updateInterval);

    const subscription = Accelerometer.addListener(({ x, y }) => {
      setAccel({ x, y });
    });

    const interval = setInterval(() => {
      fetch(`${server}/receiveInput`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(accel),
      }).catch(err => console.log(err));
    }, updateInterval);

    return () => {
      subscription.remove();
      clearInterval(interval);
    };
  }, [accel]);

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
