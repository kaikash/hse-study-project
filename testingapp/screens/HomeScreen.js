import * as WebBrowser from 'expo-web-browser';
import * as React from 'react';
import { useState } from 'react'
import { Image, Platform, Button, StyleSheet, Text, TouchableOpacity, View, ActivityIndicator } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';

import { MonoText } from '../components/StyledText';
import Motion from "../components/Motion";

import exampleImage from '../assets/images/11.jpg'

import { train, predict, GestureData } from '../mobile_lib/index.js'
import { apiUrl } from '../config';

export default function HomeScreen() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  if (loading) return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <ActivityIndicator size="large" color="black" />
    </View>
  );
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      { !result && <Motion onGesture={async (gesture) => {
        setLoading(true)
        try {
          let gestureData = new GestureData(gesture)
          setResult(await predict(gestureData, apiUrl))
          setLoading(false)
        } catch (err) {
          console.warn(err)
          setLoading(false)
        }
      }} /> }
      { result && result.name && <View style={{ alignItems: "center" }}>
        <Image
          style={{ width: 200, height: 200, marginBottom: 20 }}
          source={{
            uri: result.image
          }}
        />
        <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 10 }}>I guess it's a {result.name}!</Text>
        <Button title="Reset" color="red" onPress={() => setResult(null)} />
      </View> }
      { result && !result.name && <View style={{ alignItems: "center" }}>
        <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 10, color: 'red' }}>Can't recognize gesture!</Text>
        <Button title="Reset" color="red" onPress={() => setResult(null)} />
      </View> }
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};