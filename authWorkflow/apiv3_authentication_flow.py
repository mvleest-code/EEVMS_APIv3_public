import json, requests, sys  
from flask import Flask, request


hostName            = "127.0.0.1" #redirect uri for local host
port                = 3333 #port for the localhost uri
clientId            = "<ADD_CLIENT_ID_HERE>"
clientSecret        = "<ADD_CLIENT_SECRET_HERE>"

def getTokens(code):
    url = "https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code="+code+"&redirect_uri=http://"+hostName + ":" + str(port)
    response = requests.post(url, auth=(clientId, clientSecret))
    print("the second request",url)
    print(response.request.headers,response,response.status_code)
    return response.text
app = Flask(__name__)

@app.route('/')
def index():
    code = request.args.get('code')
    if (code):
        oauthObject = getTokens(code)
        print(oauthObject)
        return f"You are logged in oauthObject: {oauthObject}"
    else:
        endpoint            = "https://auth.eagleeyenetworks.com/oauth2/authorize"
        requestAuthUrl      = endpoint+"?client_id="+clientId+"&response_type=code&scope=vms.all&redirect_uri=http://"+hostName + ":" + str(port)
        print("the first request", requestAuthUrl)
        return "<a href='"+requestAuthUrl+"'>Login with Eagle Eye Networks</a>"

if __name__ == '__main__':
    app.run(host=hostName, port=port)
