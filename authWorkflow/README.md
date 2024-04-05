# ee_apiv3_authentication_workflow

**Eagle Eye Network Video API Platform - Authentication Workflow**

 \
Initial request, redirecting to our **auth.eagleeyenetworks.com**:


```
https://auth.eagleeyenetworks.com/oauth2/authorize?client_id=<ADD_CLIENTID_HERE>&response_type=code&scope=vms.all&redirect_uri=http://127.0.0.1:3333
```


 \
Once redirected you login with your username and password:

                    

<img src=https://www.m-cloud.nl/images/authenticationexample.png>



When the authentication is completed you will be redirected back to [http://127.0.0.1:3333](http://127.0.0.1:3333/)  \



```
http://127.0.0.1:3333/?code=<ADD_CODE_HERE>
```


 \
The next step is to exchange the **CODE** for an **AccessToken**:


```
https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code=<ADD_CODE_HERE>&redirect_uri=http://127.0.0.1:3333
```


We need to add request headers to this request like this:


```
{'User-Agent': 'python-requests/2.28.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '0', 'Authorization': 'Basic <CLIENTID:CLIENTSECRET_BASE64ENCODED>'}
```

**Flask development server**

Putting all these steps together I have an example Python, Flask test script that creates a development web server for testing on localhost. I added prints to all the steps within the script so it will be clear what requests are made:

In order to run this you would need to install python3 and "pip install flask"


```
import json, requests, sys  
from flask import Flask, request

hostName            = "127.0.0.1"
port                = 3333
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
```


When you run the script you can click the link shown and open the webpage:


```
python3 apiv3_authentication_flow.py 

 * Serving Flask app 'apiv3_authentication_flow'
 * Debug mode: off
 * Running on http://127.0.0.1:3333
Press CTRL+C to quit
```
