import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, Pressable } from 'react-native';
import React, { useState } from 'react';

export default function App() {
  const [input, setInput] = useState('');

  // IMPORTANT: include http://
  // const server = 'http://192.168.1.199:5001';
  const server = 'http://192.168.1.122:5001';

  const onSubmit = async () => {
    setInput('');
    try {
      const response = await fetch(`${server}/receiveInput`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
      });

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log('Error sending input:', error);
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.textInput}
        placeholder="Enter input:"
        keyboardType='phone-pad' // show only the numbers for ease of input
        value={input}
        onChangeText={setInput}
      />

      <Pressable style={styles.pressablePostButton} onPress={onSubmit}>
        <Text>Post!</Text>
      </Pressable>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#B76E79',
  },
  textInput: {
    width: '80%',
    height: 40,
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    color: '#ffffff',
  },
  pressablePostButton: {
    backgroundColor: '#ffee00cc',
    padding: 10,
    borderRadius: 5,
  },
});
