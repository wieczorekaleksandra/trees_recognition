import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import Login from './Login';
import Register from './Register';
import Main from './Main';
import CameraComponent from './CameraComponent'
import PlantAdditionScreen from './PlantAdditionScreen'; // Import the screen

const Stack = createStackNavigator();

const greenTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#4CAF50',
  },
};

export default function App() {
  return (
    <PaperProvider theme={greenTheme}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
          <Stack.Screen name="Login" component={Login} />
          <Stack.Screen name="Register" component={Register} />
          <Stack.Screen name="Main" component={Main} />
          <Stack.Screen name="Plant Addition" component={PlantAdditionScreen} />
          <Stack.Screen name="Camera" component={CameraComponent} />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
