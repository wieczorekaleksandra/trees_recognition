import requests


url = "http://127.0.0.1:5000/plants"

try:
    response = requests.get(url)

    if response.status_code == 200:
        print("Request was successful!")
        print("Response Data:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print("Error message:", response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
