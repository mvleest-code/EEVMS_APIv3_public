import json
import requests
from urllib.parse import quote

import base64

URL = "https://auth.eagleeyenetworks.com/oauth2/token"


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
def get_required_data():
    required_data = {}
    required_keys = ['refresh_token', 'client_id', 'client_secret']

    for key in required_keys:
        required_data[key] = input(f"Enter the value for {key}: ")

    if not all(required_data.values()):
        raise ValueError("All required data was not provided")

    return required_data

def main():
    required_data = get_required_data()

    # Base64 encode the client_id and client_secret
    client_credentials = f"{required_data['client_id']}:{required_data['client_secret']}"
    cc_base64 = base64.b64encode(client_credentials.encode()).decode()

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {cc_base64}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": quote(required_data['refresh_token'])
    }

    new_access_data = make_request(URL, headers, data)
    print(json.dumps(new_access_data, indent=4))

if __name__ == "__main__":
    main()