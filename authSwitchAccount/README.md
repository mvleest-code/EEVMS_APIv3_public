# EagleEyeNetwork API

This is a code sample for interacting with the EagleEyeNetwork API. It can be used to generate access tokens on behalf of the end-user account.

**Use case:**  
A reseller needs to manage bridges or cameras within one of the end-user accounts. The reseller does not have direct access to these devices. To gain access, they need to generate an access token on behalf of the end-user. With this new access token, the reseller has access to all devices within the end-user account.
  
## Installation

To use this library, you need to have Python installed. You can install the required dependencies by running the following command:

```shell
pip install requests python-dotenv
```

## Usage

1. Import the required modules:

```python
import requests
import json
from dotenv import load_dotenv
import os
```

1. Load the environment variables from a `.env` file:

```python
load_dotenv()
```

1. `.env`contains:

```shell
ACCESS_TOKEN=''
BASE_URL='api.cXXX.eagleeyenetworks.com'
```

1. Create an instance of the `EagleEyeNetwork` class:

```python
class EagleEyeNetwork:
    def __init__(self):
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.base_url = os.environ.get('BASE_URL')
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}"
        }
        self.account_id = ""
```

1. List accounts:

```python
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
```

1. Generating an access_token on behalf of the end-user account:

```python
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
```

1. Run the code:

```python
if __name__ == "__main__":
    eagle_eye_network = EagleEyeNetwork()
    eagle_eye_network.list_accounts()
    eagle_eye_network.switch_account()
```
