import json
import requests
from urllib.parse import quote
from sys import exit

URL = "https://auth.eagleeyenetworks.com/oauth2/token"

def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def make_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if response:
            print(f"Status Code: {response.status_code}, Reason: {response.reason}")
        exit(1)

def main():
    access_data = read_json('access_response.json')
    client_data = read_json('clientidbase64.json')

    required_keys = ['access_token', 'refresh_token', 'scope', 'token_type', 'cc_base64']
    required_data = {key: access_data.get(key) if key in access_data else client_data.get(key) for key in required_keys}

    if not all(required_data.values()):
        print("Required data missing from JSON files")
        exit(1)

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

    print("Successfully updated access token.")
    print(f"URL: {URL}")
    print(f"Response: {new_access_data}")

if __name__ == "__main__":
    main()
