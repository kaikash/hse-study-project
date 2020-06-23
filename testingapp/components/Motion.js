import React, { useState, useEffect } from "react";
import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { DeviceMotion } from "expo-sensors";

let gesture = [];

export default function Motion(props) {
  const [recording, setRecording] = useState(false);
  const size = recording ? 220 : 200;
  useEffect(() => {
    if (!recording) return;
    const contentFunc = async () => {
      await DeviceMotion.isAvailableAsync();
      DeviceMotion.addListener(({ acceleration, rotation }) => {
        gesture.push([
          Date.now(),
          acceleration.x,
          acceleration.y,
          acceleration.z,
          rotation.alpha,
          rotation.beta,
          rotation.gamma,
        ]);
      });
      DeviceMotion.setUpdateInterval(1);
    };
    contentFunc();
    return () => DeviceMotion.removeAllListeners();
  }, [recording]);
  return (
    <TouchableOpacity
      style={{
        width: size,
        height: size,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "red",
        borderRadius: size,
      }}
      onPressIn={() => {
        gesture = [];
        setRecording(true);
      }}
      onPressOut={() => {
        setRecording(false);
        props.onGesture([...gesture]);
      }}
    >
      <Text
        style={{
          fontWeight: "900",
          color: "white",
          fontSize: 18,
          textTransform: "uppercase",
        }}
      >
        {recording ? "Recording..." : "Record"}
      </Text>
    </TouchableOpacity>
  );
}

Motion.defaultProps = {
  onGesture: (gesture) => null,
};
