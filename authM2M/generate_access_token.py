import json
import requests
from urllib.parse import quote
import os

URL = "https://auth.eagleeyenetworks.com/oauth2/token"

# Function to get the absolute file path
def get_filepath(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_directory, filename)

# Function to write JSON data to a file
def write_json(filename, data):
    with open(get_filepath(filename), 'w') as f:
        json.dump(data, f, indent=4)

# Function to make a POST request
def make_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if response:
            print(f"Status Code: {response.status_code}, Reason: {response.reason}")
        raise

# Function to get the required data from the user
## keep in mind that the clientId and clientSecret should be base64 encoded: clientId:clientSecret ##
def get_required_data():
    required_data = {}
    required_keys = ['refresh_token','cc_base64']

    for key in required_keys:
        required_data[key] = input(f"Enter the value for {key}: ")

    if not all(required_data.values()):
        raise ValueError("All required data was not provided")

    return required_data

def main():
    required_data = get_required_data()

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {required_data['cc_base64']}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": quote(required_data['refresh_token'])
    }

    new_access_data = make_request(URL, headers, data)
    write_json('access_response.json', new_access_data)
    print("New access token and refresh token written to access_response.json")

if __name__ == "__main__":
    main()
