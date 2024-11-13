// App.js
import { StyleSheet, View } from 'react-native';
import CameraComponent from './CameraComponent.js';

export default function App() {
  return (
    <View style={styles.container}>
      <CameraComponent />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
});
