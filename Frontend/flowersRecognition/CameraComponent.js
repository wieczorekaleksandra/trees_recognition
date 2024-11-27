import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Modal } from 'react-native';
import {url} from './Constants'
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function CameraComponent() {
  const {facing, setFacing} = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef(null);
  
  const [modalVisible, setModalVisible] = useState(false);
  const [flowerDict, setFlowerDict] = useState({});

  if (!permission) {
    return <View />;
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({base64:true});
      handleImageUpload(photo.base64)
    }
  };

  const handleImageUpload = async (base64Image) => {
    try {
      // Retrieve the JWT token from AsyncStorage
      const token = await AsyncStorage.getItem('accessToken');
      if (!token) {
        Alert.alert('Error', 'Please log in first');
        return;
      }

      // Send the image with the token in the headers
      const response = await fetch(`${url}/upload-image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Include the token in the header
        },
        body: JSON.stringify({ image: base64Image }),
      });

      if (response.ok) {
        const result = await response.json();
        // Extract confidence and name from response
        const recognized = result['recognized'][0];
        const confidence = recognized[0];
        const name = recognized[1];

        // Update flowerDict with the new entry
        const newFlowerDict = { ...flowerDict, [name]: confidence };
        setFlowerDict(newFlowerDict);
        setModalVisible(true);
      } else {
        console.error('Image upload failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };
  

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing={facing} ref={cameraRef}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity onPress={takePicture} style={styles.captureButton} />
        </View>
      </CameraView>
      
      <Modal
  animationType="slide"
  transparent={true}
  visible={modalVisible}
  onRequestClose={() => setModalVisible(false)}
>
  <View style={styles.modalContainer}>
    <View style={styles.modalContent}>
      <Text style={styles.modalTitle}>Response Data</Text>

      {/* Loop through flowerDict and display each flower with its confidence */}
      {Object.entries(flowerDict).map(([name, confidence], index) => (
        <View key={index} style={styles.resultItem}>
          <Text style={styles.resultText}>Flower: {name}</Text>
          <Text style={styles.resultText}>Confidence: {confidence}</Text>
        </View>
      ))}

      <Button title="Close" onPress={() => {setModalVisible(false)
        setFlowerDict({})
      }} />
    </View>
  </View>
</Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingBottom: 30,
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 50,
    backgroundColor: '#fff',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    width: 300,
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});
