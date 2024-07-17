from flask import Flask, request, render_template_string, make_response
import requests
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def logout():
    # Get the token from the browser cookie access_token
    token = request.cookies.get('access_token')
    if not token:
        return "No access token found in cookies", 400

    # Define the token, token_type_hint, and client credentials
    token_type_hint = "access_token"
    client_id = "" ## enter your client ID
    client_secret = "" ## enter your client secret

    # Create the Authorization header with client credentials
    authorization = f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"

    # Define the URL for the POST request
    url = f"https://auth.eagleeyenetworks.com/oauth2/revoke?token={token}&token_type_hint={token_type_hint}"

    # Define the headers with Content-Type and Authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }

    # Make the POST request
    response = requests.post(url, headers=headers)

    # Print the response
    print("url:", url)
    print(response.cookies)
    print("resonse text:",response.text)
    print("resonse content:",response.content)
    print("response headers:",response.headers)
    print("resonse status_code",response.status_code)

    # Define the HTML for the logout confirmation page
    logout_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Logged Out</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial, sans-serif;
            }
            h1 {
                font-size: 2em;
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>You have been logged out successfully.</h1>
    </body>
    </html>
    """
    response = make_response(render_template_string(logout_page))
    response.set_cookie('access_token', '', expires=0, path='/', domain='.exampledomain.com') ## change to your domain
    response.set_cookie('base_url', '', expires=0, path='/', domain='.exampledomain.com') ## change to your domain
    return response
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

