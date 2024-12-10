import unittest  # Import unittest module
import json
from backend import app  
from io import BytesIO
from PIL import Image
import base64
import time
import requests  

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Change to server url in future 
        self.server_url = "https://flask-app-358350046745.europe-central2.run.app/"
        self.test_user = {
            "email": "userabcd",
            "password": "testpassword123"
        }
        self.test_user1 = {
            "email": "user1asd",
            "password": "testpassword123"
        }

    def test_register(self):
        response = requests.post(f'{self.server_url}/register', json=self.test_user1)
        time.sleep(2)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.text)

    def test_login(self):
        # Register the user first
        requests.post(f'{self.server_url}/register', json=self.test_user)
        response = requests.post(f'{self.server_url}/login', json=self.test_user)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('access_token', data)

        # Test invalid login
        wrong_user = { "email": "wronguser@example.com", "password": "wrongpassword" }
        response = requests.post(f'{self.server_url}/login', json=wrong_user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid email or password', response.text)

    def test_upload_image(self):
        # Register and login
        requests.post(f'{self.server_url}/register', json=self.test_user)
        login_response = requests.post(f'{self.server_url}/login', json=self.test_user)
        token = login_response.json()['access_token']

        flower_image_path = '1355932.jpg'  
        with open(flower_image_path, 'rb') as img_file:
            img_byte_arr = img_file.read()

        
        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(f'{self.server_url}/upload-image', json={'image': encoded_image}, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)

    def test_get_all_plants(self):
        response = requests.get(f'{self.server_url}/plants')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('plants', data)

    def test_unauthorized_image_upload(self):
        image = Image.new('RGB', (100, 100), color='green')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

        response = requests.post(f'{self.server_url}/upload-image', json={'image': encoded_image})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', response.text)

if __name__ == '__main__':
    unittest.main()
