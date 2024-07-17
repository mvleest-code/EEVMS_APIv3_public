import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class EagleEyeNetwork:
    def __init__(self):
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.base_url = os.getenv('BASE_URL')
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}"
        }
        self.account_id = ""
        
    def list_accounts(self):
        url = f"https://{self.base_url}/api/v3.0/accounts"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()

            print(f"Total Size: {data['totalSize']}")
            print("Results:")
            for result in data['results']:
                print(f"- ID: {result['id']}, Name: {result['name']}, Status: {result['status']}, Type: {result['type']}")
                self.account_id = result['id']
                self.account_name = result['name']
            return response.json()
        else:
            print("Failed to retrieve list of accounts")
            return print(json.dumps(response.json(), indent=4))
    
    def switch_account(self):
        url = "https://auth.eagleeyenetworks.com/api/v3.0/authorizationTokens"
        self.account_id = input("Enter the account id you want to switch to: ")
        payload = {
            "scopes": ["vms.all"],
            "type": "reseller",
            "targetType": "account",
            "targetId": f"{self.account_id}"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Switching account to: ID: {self.account_id}, Name: {self.account_name} ")
        if response.status_code == 201:
            data = response.json()
            print("Switched to account: results:")

            print(f"- Access_token: {data['accessToken']}")
            print(f"- BaseUrl: {data['httpsBaseUrl']['hostname']}")
            return response.json()
        else:
            print("Failed to switch account")
            return print(json.dumps(response.json(), indent=4))
        
if __name__ == "__main__":
    eagle_eye_network = EagleEyeNetwork()
    eagle_eye_network.list_accounts()
    eagle_eye_network.switch_account()
