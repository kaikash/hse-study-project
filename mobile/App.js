import React from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native';
import { Accelerometer, DeviceMotion } from 'expo-sensors';
import { ScreenOrientation } from 'expo';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';


// export default function App() {
  // return (
  //   <View style={styles.container}>
  //     <Text>Open up App.js to start working on your app!</Text>
  //   </View>
  // );
// }

let buffer = [];
let gestures = [];
let session = Date.now();
let resultFilename = `${FileSystem.cacheDirectory}gestures_${session}.json`;
let start = Date.now();

export default class App extends React.Component {

  state = {
    data: {}
  }

  async componentDidMount () {
    await ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.PORTRAIT_UP);
    await DeviceMotion.isAvailableAsync();
    DeviceMotion.setUpdateInterval(1);
    DeviceMotion.addListener((data) => {
      if (this.state.record)
        buffer.push([
          Date.now()-start,
          data.acceleration.x,
          data.acceleration.y,
          data.acceleration.z,
          data.rotation.alpha,
          data.rotation.beta,
          data.rotation.gamma,
          data.rotationRate.alpha,
          data.rotationRate.beta,
          data.rotationRate.gamma,
          data.orientation
        ]);
    });

  }

  render () {
    return (
      <View style={styles.container}>
        <View
          onTouchStart={() => {
            start = Date.now()
            this.setState({ record: true })
          }}
          onTouchEnd={async () => {
            this.setState({ record: false })
            gestures.push(buffer.concat())
            buffer = []
            await FileSystem.writeAsStringAsync(resultFilename, JSON.stringify(gestures))
          }}
          style={{
            width: this.state.record ? 300 : 250,
            height: this.state.record ? 300 : 250,
            backgroundColor: 'red',
            borderRadius: this.state.record ? 300 : 250
          }}>
        </View>
        { gestures.length > 0 && <Button title="Share" onPress={() => {
          Sharing.shareAsync(resultFilename)
        }} /> }
        { gestures.length > 0 && <Button title="Reset" color="red" onPress={() => {
          try {
            buffer = [];
            gestures = [];
            session = Date.now();
            resultFilename = `${FileSystem.cacheDirectory}gestures_${session}.json`;
            this.setState({ record: false })
          } catch (err) {
            console.warn(err)
          }
        }} /> }
        {/* <Text>{JSON.stringify(this.state.data, undefined, 2)}</Text> */}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
