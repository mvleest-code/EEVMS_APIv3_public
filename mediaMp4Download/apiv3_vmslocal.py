import json, requests
from flask import Flask, request

app = Flask(__name__)

HOST_NAME = "127.0.0.1"
PORT = 3333
CLIENT_ID = ""
CLIENT_SECRET = ""
AUTH_URL = "https://auth.eagleeyenetworks.com"
BASE_URL = "https://api.eagleeyenetworks.com"

def make_request(method, url, headers=None, auth=None):
    response = requests.request(method, url, headers=headers, auth=auth)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Debug - Failed to make request. Response: {response.text}")  # Debug
        return None

def getTokens(code):
    url = f"{AUTH_URL}/oauth2/token?grant_type=authorization_code&scope=vms.all&code={code}&redirect_uri=http://{HOST_NAME}:{PORT}"
    oauthObject = make_request("POST", url, auth=(CLIENT_ID, CLIENT_SECRET))
    if oauthObject:
        accessToken = oauthObject.get('access_token', None)
        print(f"Debug - Access Token: {accessToken}")  # Debug
        return accessToken, oauthObject
    return None, None

def get_base_url(accessToken):
    url = f"{BASE_URL}/api/v3.0/clientSettings"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {accessToken}"
    }
    settings = make_request("GET", url, headers=headers)
    if settings:
        return settings.get('httpsBaseUrl', {}).get('hostname')
    return None

def get_user_details(accessToken):
    if not accessToken:
        print("Debug - Access Token is None")  # Debug
        return {}

    base_url = get_base_url(accessToken)
    if not base_url:
        print("Debug - Failed to get base URL")
        return {}
    
    url = f"https://{base_url}/api/v3.0/users/self"
    headers = {"accept": "application/json", "authorization": f"Bearer {accessToken}"}
    userDetails = make_request("GET", url, headers=headers)
    if not userDetails:
        print(f"Debug - Failed to get user details.")  # Debug
    return userDetails or {}

@app.route('/')
def index():
    code = request.args.get('code')
    if code:
        accessToken, oauthObject = getTokens(code)
        
        if accessToken is None:
            return "Failed to log in."
        
        userDetails = get_user_details(accessToken)
        userId = userDetails.get('id', 'unknown')
        
        with open('access_response.json', 'w') as f:
            json.dump(oauthObject, f)
            
        return f"You are logged in. Your user ID is {userId}."
    else:
        endpoint = f"{AUTH_URL}/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&scope=vms.all&redirect_uri=http://{HOST_NAME}:{PORT}"
        return f"<a href='{endpoint}'>Login with Eagle Eye Networks</a>"

if __name__ == '__main__':
    app.run(host=HOST_NAME, port=PORT)