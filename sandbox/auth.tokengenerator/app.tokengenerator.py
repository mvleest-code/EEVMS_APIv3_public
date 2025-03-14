import json, requests
import urllib.parse
from flask import Flask, request, render_template_string

hostName = "127.0.0.1"
port = 3333
clientId = "" # Add your client ID here
clientSecret = "" # Add your client secret here

def getTokens(code):
    url = "https://auth.eagleeyenetworks.com/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "scope": "vms.all",
        "code": code,
        "redirect_uri": "http://" + hostName + ":" + str(port)
    }
    response = requests.post(url, auth=(clientId, clientSecret), data=data)
    return response.text

app = Flask(__name__)

# HTML template with JavaScript for the copy button functionality
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Eagle Eye Networks OAuth</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        .token-container {
            margin-top: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        .copy-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 4px;
        }
        .token-field {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <h1>Eagle Eye Networks OAuth</h1>
    {% if oauth_data %}
        <h2>Authentication Successful!</h2>
        <div class="token-container">
            <h3>Refresh Token:</h3>
            <textarea id="refresh_token" class="token-field" rows="3" readonly>{{ oauth_data.refresh_token }}</textarea>
            <button class="copy-button" onclick="copyToClipboard('refresh_token')">Copy Refresh Token</button>
            
            <h3>Complete Response:</h3>
            <pre id="complete_response">{{ full_response }}</pre>
            <button class="copy-button" onclick="copyToClipboard('complete_response')">Copy Full Response</button>
        </div>
    {% else %}
        <p>Please authenticate with Eagle Eye Networks to generate tokens.</p>
        <a href="{{ login_url }}" style="display: inline-block; background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login with Eagle Eye Networks</a>
    {% endif %}
    
    <script>
        function copyToClipboard(elementId) {
            const element = document.getElementById(elementId);
            element.select();
            document.execCommand('copy');
            alert('Copied to clipboard!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    code = request.args.get('code')
    if code:
        # User has authenticated, get tokens
        response_text = getTokens(code)
        oauth_data = json.loads(response_text)
        return render_template_string(
            html_template, 
            oauth_data=oauth_data, 
            full_response=json.dumps(oauth_data, indent=4),
            login_url=None
        )
    else:
        # User needs to authenticate
        url = "https://auth.eagleeyenetworks.com/oauth2/authorize"
        params = {
            "client_id": clientId,
            "response_type": "code",
            "scope": "vms.all",
            "redirect_uri": "http://" + hostName + ":" + str(port)
        }
        login_url = url + "?" + urllib.parse.urlencode(params)
        return render_template_string(html_template, oauth_data=None, full_response=None, login_url=login_url)

if __name__ == '__main__':
    print(f"Starting server at http://{hostName}:{port}")
    app.run(host=hostName, port=port, debug=True)