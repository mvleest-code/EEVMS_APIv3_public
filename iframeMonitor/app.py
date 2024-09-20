import requests
import os
from time import sleep
from flask import Flask, render_template, make_response
import threading


# Flask app initialization
app = Flask(__name__)

# In-memory variable to store the access token
access_token = None

# Function to request a new access token using refresh token
def refresh_access_token():
    global access_token  # Allow the function to modify the global variable
    url = "https://auth.eagleeyenetworks.com/oauth2/token"
    
    # Get refresh token and authorization header from environment
    refresh_token = ""
    auth_header = ""
    
    print(f"Refresh Token: {refresh_token}")
    print(f"Authorization Header: {auth_header}")

    payload = f'grant_type=refresh_token&refresh_token={refresh_token}'
    headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        print("Access Token refreshed:", access_token)
    else:
        print(f"Error fetching token: {response.status_code}")
        print(response.text)

# This function can be scheduled to run every 12 hours
def schedule_token_refresh():
    while True:
        refresh_access_token()
        # Wait for 12 hours before refreshing again
        sleep(12 * 3600)

# Flask route to serve the access token to the template
@app.route('/', methods=['GET'])
def index():
    # Check if access_token exists and is valid
    if access_token:
        # Create a response to render the template
        response = make_response(render_template('index.html'))
        # Set the access token as a cookie
        response.set_cookie('access_token', access_token)
        return response
    else:
        # Token is not available, trigger a refresh and try again
        refresh_access_token()
        if access_token:
            # Create response and set the access_token cookie
            response = make_response(render_template('index.html'))
            response.set_cookie('access_token', access_token)
            return response
        else:
            return "Access token is still not available after refresh."

# Start the token refreshing in a separate thread
def start_refresh_thread():
    # Refresh the token immediately to ensure it's available
    refresh_access_token()
    
    # Then start the periodic token refresh thread
    refresh_thread = threading.Thread(target=schedule_token_refresh)
    refresh_thread.daemon = True  # Daemonize thread to shut down with the program
    refresh_thread.start()

if __name__ == '__main__':
    # Start the token refresh thread
    start_refresh_thread()
    
    # Start the Flask app
    app.run(port=3339)