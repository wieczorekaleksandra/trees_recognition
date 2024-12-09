import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Modal, Image, Alert } from 'react-native';
import { url } from './Constants'; // Ensure the correct API URL
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function CameraComponent() {
  const {facing, setFacing} = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef(null);

  const [modalVisible, setModalVisible] = useState(false);
  const [flowerDict, setFlowerDict] = useState([]); // Ensuring flowerDict is an array

  if (!permission) {
    return <View />;
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({ base64: true });
      handleImageUpload(photo.base64);
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

          const recognized = result["results"]; 
          const newFlowerDict = recognized.map((item) => ({
            name: item["plant_name"],       // Flower name (at index 1)
            image: item["image_base64"],      // Base64 image data (at index 2)
          }));
          console.log(recognized)
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
            <Text style={styles.modalTitle}>Recognized Plants</Text>

            {/* Loop through flowerDict and display each plant with its confidence and image */}
            {flowerDict.map((flower, index) => (
              <View key={index} style={styles.resultItem}>
                <Text style={styles.resultText}>Flower: {flower.name}</Text>
                {flower.image ? (
                  <Image
                    source={{ uri: `data:image/jpeg;base64,${flower.image}` }}
                    style={styles.resultImage}
                  />
                ) : null}
              </View>
            ))}

            <Button
              title="Close"
              onPress={() => {
                setModalVisible(false);
                setFlowerDict([]); // Reset flowerDict when closing modal
              }}
            />
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
  resultItem: {
    marginBottom: 10,
    alignItems: 'center',
  },
  resultText: {
    fontSize: 14,
    marginBottom: 5,
  },
  resultImage: {
    width: 100,
    height: 100,
    marginTop: 10,
    borderRadius: 10,
  },
});
