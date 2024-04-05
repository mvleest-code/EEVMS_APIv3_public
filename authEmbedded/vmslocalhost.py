import json, requests, sys
from flask import Flask, request

app = Flask(__name__)

hostName = "127.0.0.1"
port = 3333

clientId = ""
clientSecret = ""

def getTokens(code):
    url = "https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code=" + code + "&redirect_uri=http://" + hostName + ":" + str(port)
    response = requests.post(url, auth=(clientId, clientSecret))
    if response.status_code == 200:
        oauthObject = json.loads(response.text)
        accessToken = oauthObject.get('access_token', None)
        print(f"Debug - Access Token: {accessToken}")  # Debug
        if accessToken:
            return accessToken, oauthObject
    print(f"Debug - Failed to get Access Token. Response: {response.text}")  # Debug
    return None

def get_base_url(accessToken):
    url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {accessToken}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        settings = json.loads(response.text)
        hostname = settings.get('httpsBaseUrl', {}).get('hostname')
        if hostname:
            return f"{hostname}"
    return None

def get_user_details(accessToken):
    if not accessToken:
        print("Debug - Access Token is None")  # Debug
        return {}

    base_url = get_base_url(accessToken)
    if not base_url:
        print("Debug - Failed to get base URL")
        return {}
      
    url = f"https://{base_url}/api/v3.0/users/self"  # Make sure this URL is correct
    headers = {"accept": "application/json", "authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        userDetails = json.loads(response.text)
        return userDetails
    else:
        print(f"Debug - Failed to get user details. Response: {response.text}")  # Debug
        return {}

@app.route('/')
def index():
    code = request.args.get('code')
    if code:
        accessToken, oauthObject = getTokens(code)
        
        if accessToken is None:
            return "Failed to log in."
        
        userDetails = get_user_details(accessToken)
        userId = userDetails.get('id', 'unknown')
        
        with open(f'{userId}_access_response.json', 'w') as f:
            f.write(json.dumps(oauthObject))
            
        return f"You are logged in. Your user ID is {userId}."
    else:
        endpoint = "https://auth.eagleeyenetworks.com/oauth2/authorize"
        requestAuthUrl = endpoint + "?client_id=" + clientId + "&response_type=code&scope=vms.all&redirect_uri=http://" + hostName + ":" + str(port)
        return "<a href='" + requestAuthUrl + "'>Login with Eagle Eye Networks</a>"

if __name__ == '__main__':
    app.run(host=hostName, port=port)
