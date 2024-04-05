# Loggin in using OAuth fovmslocal_2.pyllows 3 steps
# Step 1: redirect the user to auth.eagleeyenetworks.com
# Step 2: the user will login at EEN, login, and get redirected back to your application
# Step 3: Your application backend/server request the end user tokens.

# Flask is used to start an HTTP server to act as your application backend.
import json, requests, sys   
from flask import Flask, request

# Hostname and port for the HTTP server
hostName            = "127.0.0.1"
port                = 3333

# Enter your OAuth client credentials. For more info see developerv3.eagleeyenetworks.com
# To user the API your appliction needs its own client credentials.
clientId            = ""
clientSecret        = ""

# This method is executing step 3.
def getTokens(code):
    url = "https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code="+code+"&redirect_uri=http://"+hostName + ":" + str(port)
    response = requests.post(url, auth=(clientId, clientSecret))
    return response.text

app = Flask(__name__)

# If a user visits localhost:3333 this method will be called. This method is called in 2 cases:
# 1) For step 1, in this case a link is given to rediret the user to auth.eagleeyenetworks.com
# 2) Handling users that are redirected from auth.eagleeyenetworks.com
@app.route('/')
def index():
    # This is getting the ?code= querystring value from the HTTP request.
    code = request.args.get('code')

    if (code):
        # Execute Step 2, the user is redirected back to localhost:3333 because of the "&redirect_uri="
        # With the CODE this backend can request the actual access_token and refresh_token
        # For demo purposes the results are printed to the console, on production never show the refresh_token in the browser.
        oauthObject = getTokens(code)
        with open('access_response.json', 'w') as f:
            f.write(oauthObject)
        return "You are logged in"
    else:
        # Executing step 1, a link is generated to redirect the user to auth.eagleeyenetworks.com
        endpoint            = "https://auth.eagleeyenetworks.com/oauth2/authorize"
        requestAuthUrl      = endpoint+"?client_id="+clientId+"&response_type=code&scope=vms.all&redirect_uri=http://"+hostName + ":" + str(port)

        return "<a href='"+requestAuthUrl+"'>Login with Eagle Eye Networks</a>"

# Start the HTTP server
if __name__ == '__main__':
    app.run(host=hostName, port=port)
