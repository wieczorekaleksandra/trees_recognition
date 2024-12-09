import React, { useState, useEffect } from 'react';
import { View, FlatList, StyleSheet, ActivityIndicator, Alert, Image } from 'react-native';
import { Text, Button, Card, IconButton } from 'react-native-paper';
import { url } from './Constants';

export default function Main({ navigation }) {
  const [favoritePlants, setFavoritePlants] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchFavoritePlants = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${url}/plants`); 
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      if (data.plants) {
        setFavoritePlants(data.plants);
      } else {
        setFavoritePlants([]);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to fetch favorite plants.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFavoritePlants();
  }, []);

  const renderPlant = ({ item }) => (
    <Card style={styles.card}>
      <Card.Title
        title={item.scientific_name}
        left={(props) => <IconButton {...props} icon="leaf" />}
      />
      {item.image && (
        <Image
          source={{ uri: `data:image/jpeg;base64,${item.image}` }}
          style={styles.image}
          resizeMode="cover"
        />
      )}
    </Card>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>All of plants recognized by the app</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#4CAF50" />
      ) : favoritePlants.length > 0 ? (
        <FlatList
          data={favoritePlants}
          renderItem={renderPlant}
          keyExtractor={(item) => item.id.toString()}
        />
      ) : (
        <Text style={styles.emptyMessage}>You don't have any favorite plants yet.</Text>
      )}
      <Button
        mode="contained"
        style={styles.button}
        onPress={() => navigation.navigate('Camera')} // Navigate to Camera
      >
        Take a photo
      </Button>
      <Button
        mode="text"
        style={styles.link}
        onPress={() => navigation.navigate('Login')}
      >
        Log Out
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#E8F5E9',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 16,
  },
  card: {
    marginBottom: 12,
    padding: 8,
  },
  image: {
    width: '100%',
    height: 200,
    marginTop: 8,
    borderRadius: 8,
  },
  emptyMessage: {
    textAlign: 'center',
    fontSize: 16,
    color: '#555',
    marginVertical: 16,
  },
  button: {
    marginTop: 16,
  },
  link: {
    marginTop: 8,
  },
});
