import * as WebBrowser from 'expo-web-browser';
import * as React from 'react';
import { useState } from 'react'
import { Image, Platform, Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';

import { MonoText } from '../components/StyledText';
import Motion from "../components/Motion";

import exampleImage from '../assets/images/11.jpg'

export default function HomeScreen() {
  const [result, setResult] = useState(null)
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      { !result && <Motion onGesture={(gesture) => setResult(gesture)} /> }
      { result && <View style={{ alignItems: "center" }}>
        <Image
          style={{ width: 200, height: 200, marginBottom: 20 }}
          source={exampleImage}
        />
        <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 10 }}>I guess it's a circle!</Text>
        <Button title="Reset" color="red" onPress={() => setResult(null)} />
      </View> }
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};