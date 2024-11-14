import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

export default function CameraComponent() {
  const {facing, setFacing} = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef(null);

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
      const response = await fetch('http://192.168.8.103:5000/upload-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: base64Image }),
      });
      if (response.ok) {
        const result = await response.json();
        console.log('Image uploaded successfully:', result);
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
    <CameraView style={styles.camera} facing={facing} ref={cameraRef}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          onPress={takePicture}
          style={styles.captureButton}
        />
      </View>
    </CameraView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
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
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 50,
    backgroundColor: '#fff',
  },
});
