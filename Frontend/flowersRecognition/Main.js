import React, { useState } from 'react';
import { View, FlatList, StyleSheet } from 'react-native';
import { Text, Button, Card, IconButton } from 'react-native-paper';

export default function Main({ navigation }) {
  const [favoritePlants, setFavoritePlants] = useState([
    { id: '1', name: 'Monstera' },
    { id: '2', name: 'Fiddle Leaf Fig' },
    { id: '3', name: 'Snake Plant' },
    { id: '4', name: 'Pothos' },
  ]);

  const renderPlant = ({ item }) => (
    <Card style={styles.card}>
      <Card.Title
        title={item.name}
        left={(props) => <IconButton {...props} icon="leaf" />}
      />
    </Card>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Favorite Plants</Text>
      {favoritePlants.length > 0 ? (
        <FlatList
          data={favoritePlants}
          renderItem={renderPlant}
          keyExtractor={(item) => item.id}
        />
      ) : (
        <Text style={styles.emptyMessage}>You don't have any favorite plants yet.</Text>
      )}
      <Button
        mode="contained"
        style={styles.button}
        onPress={() => navigation.navigate("Plant Addition")} // Navigate to PlantAdditionScreen
      >
        Add a Plant
      </Button>
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
