import { useState } from "react";
import { Ionicons } from "@expo/vector-icons";
import * as WebBrowser from "expo-web-browser";
import * as React from "react";
import { Image, StyleSheet, Text, View, Picker, Button, ActivityIndicator } from "react-native";
import { RectButton, ScrollView } from "react-native-gesture-handler";
import Motion from "../components/Motion";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { train, predict, retrain, GestureData } from '../mobile_lib/index.js'
import { apiUrl } from '../config';

import exampleImage from '../assets/images/12.jpg'

export default function TrainScreen() {
  const classes = [
    { label: "Shake", value: "shake" },
    { label: "Circle", value: "circle" },
    { label: "Square", value: "square" },
    { label: "Triangle", value: "triangle" },
  ];
  const [selectedClass, setSelectedClass] = useState("circle");
  const [gesture, setGesture] = useState([]);
  const [result, setResult] = useState(false);
  const [loading, setLoading] = useState(false)

  const submitGesture = async () => {
    setLoading(true)
    try {
      let gestureData = new GestureData(gesture)
      let res = await train(selectedClass, gestureData, apiUrl)
      setResult(res)
      setLoading(false)
    } catch (err) {
      console.warn(err)
      setLoading(false)
    }
  }
  if (loading) return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <ActivityIndicator size="large" color="black" />
    </View>
  );
  return (
    <View style={{ alignItems: "center", flex: 1 }}>
      <Text style={{ padding: 20, fontWeight: "bold", fontSize: 20 }}>
        Select class:
      </Text>
      <View style={{ width: "100%" }}>
        <Picker
          selectedValue={selectedClass}
          disabled={!!result}
          onValueChange={(itemValue, itemIndex) => {
            let value = itemValue;
            // if (itemValue == "_add_new") {
            //   let value = prompt("Enter class name:");
            //   setClasses([...classes, { label: value, value }]);
            // }
            // console.warn(value)
            setSelectedClass(value);
          }}
        >
          {/* <Picker.Item label="Shake" value="shake" />
          <Picker.Item label="Circle" value="circle" />
          <Picker.Item label="Square" value="square" /> */}
          {classes.map((x) => (
            <Picker.Item label={x.label} value={x.value} key={x.value} />
          ))}
          {/* <Picker.Item label="Add new" value="_add_new" /> */}
        </Picker>
      </View>
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        { !result && <Motion onGesture={(gesture) => setGesture(gesture)} /> }
        { result && <View style={{ alignItems: "center" }}>
          <Image
            style={{ width: 200, height: 200, marginBottom: 20 }}
            source={{
              uri: result.image
            }}
          />
        </View> }
      </View>
      <View
        style={{
          flexDirection: "row",
          padding: 20,
          opacity: gesture ? 1 : 0,
        }}
      >
        <View style={{ flex: 1 }}>
          <Button title="Reset" color="red" onPress={() => {
            setGesture(null)
            setResult(null)
          }} />
        </View>
        <Button title="Submit" disabled={!!result} onPress={() => submitGesture()} />
        <View style={{ flex: 1 }}>
          <Button
            title="Share"
            onPress={async () => {
              let resultFilename = `${
                FileSystem.cacheDirectory
              }gesture_${selectedClass}_${Date.now()}.json`;
              await FileSystem.writeAsStringAsync(
                resultFilename,
                JSON.stringify([gesture])
              );
              await Sharing.shareAsync(resultFilename);
            }}
          />
        </View>
      </View>
      <View style={{
          flexDirection: "row",
          paddingBottom: 20
        }}>
        <Button title="Retrain model" color="orange" onPress={async () => {
          setLoading(true)
          try {
            await retrain(apiUrl)
            setLoading(false)
          } catch (err) {
            console.warn(err)
            setLoading(false)
          }
        }} />
      </View>
    </View>
  );
}
