import React, { useState } from 'react';
import { View, FlatList, StyleSheet } from 'react-native';
import { Text, Button, Card, IconButton } from 'react-native-paper';

export default function PlantAdditionScreen({ navigation }) {
  // Mock data for available plants
  const [allPlants, setAllPlants] = useState([
    { id: '1', name: 'Monstera' },
    { id: '2', name: 'Fiddle Leaf Fig' },
    { id: '3', name: 'Snake Plant' },
    { id: '4', name: 'Pothos' },
    { id: '5', name: 'Peace Lily' },
    { id: '6', name: 'Spider Plant' },
  ]);

  const renderPlant = ({ item }) => (
    <Card style={styles.card}>
      <Card.Title
        title={item.name}
        left={(props) => <IconButton {...props} icon="leaf" />}
        right={(props) => (
          <IconButton
            {...props}
            icon="plus"
            onPress={() => alert(`${item.name} added to favorites!`)}
          />
        )}
      />
    </Card>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>All Available Plants</Text>
      <FlatList
        data={allPlants}
        renderItem={renderPlant}
        keyExtractor={(item) => item.id}
      />
      <Button
        mode="text"
        style={styles.link}
        onPress={() => navigation.goBack()} // Return to the Main screen
      >
        Back to Favorites
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#F1F8E9',
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
  link: {
    marginTop: 16,
  },
});
