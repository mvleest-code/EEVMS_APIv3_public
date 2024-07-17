#!/usr/local/bin/python3

import json
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from flask import Flask, request
from threading import Thread, Event

#### please note this is an example script and should not be used in production ####
#### If you are using this script in production, please make sure to use a secure method to store the client secret and client id ###
#### This script is for educational purposes only ####
#### not recommended for production use, please use a production server like wsgi ####

load_dotenv()

# Constants
HOST_NAME = "127.0.0.1"
PORT = 3333
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
AUTH_URL = "https://auth.eagleeyenetworks.com"
BASE_URL = "https://api.eagleeyenetworks.com"

# Flask app for handling redirect
app = Flask(__name__)
auth_code_received = Event()

# Utility Functions
def make_request(method, url, headers=None, auth=None):
    response = requests.request(method, url, headers=headers, auth=auth)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

# OAuth and User Details Handling
def get_tokens(code):
    url = f"{AUTH_URL}/oauth2/token?grant_type=authorization_code&scope=vms.all&code={code}&redirect_uri=http://{HOST_NAME}:{PORT}"
    return make_request("POST", url, auth=(CLIENT_ID, CLIENT_SECRET))

def get_base_url(accessToken):
    url = f"{BASE_URL}/api/v3.0/clientSettings"
    headers = {"accept": "application/json", "authorization": f"Bearer {accessToken}"}
    settings = make_request("GET", url, headers=headers)
    return settings.get('httpsBaseUrl', {}).get('hostname') if settings else None

def get_user_details(accessToken, base_url):
    url = f"https://{base_url}/api/v3.0/users/self"
    headers = {"accept": "application/json", "authorization": f"Bearer {accessToken}"}
    return make_request("GET", url, headers=headers)

# Selenium for automated login
def automate_login():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    auth_url = f"{AUTH_URL}/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&scope=vms.all&redirect_uri=http://{HOST_NAME}:{PORT}"
    driver.get(auth_url)

    try:
        # Wait for the email input to be present
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "authentication--input__email")))
        print("Email input found")
        email_input.send_keys(USERNAME)
        
        # Wait for the next button to be clickable and click it
        next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        print("Next button found and clickable")
        next_button.click()

        # Wait for the new URL where the password is entered
        WebDriverWait(driver, 20).until(EC.url_contains("id.eagleeyenetworks.com/login"))

        # Wait for the password input to be present
        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "authentication--input__password")))
        print("Password input found")
        password_input.send_keys(PASSWORD)
        
        # Wait for the submit button to be clickable and click it
        submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "next")))
        print("Submit button found and clickable")
        submit_button.click()

        # Allow some time for the login to process
        time.sleep(5)

        # Wait until the authorization code is in the URL
        WebDriverWait(driver, 30).until(EC.url_contains("code="))
        code = driver.current_url.split("code=")[1]
        return code
    except Exception as e:
        print(f"Error during login: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page Source: {driver.page_source}")
        return None
    finally:
        driver.quit()

@app.route('/')
def handle_redirect():
    code = request.args.get('code')
    if code:
        global oauth_object
        oauth_object = get_tokens(code)
        auth_code_received.set()
        return "Authorization successful. You can close this window."
    else:
        return "Failed to obtain authorization code."

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return "Server shutting down..."

def run_flask():
    app.run(host=HOST_NAME, port=PORT)

def main():
    if not CLIENT_ID or not CLIENT_SECRET or not USERNAME or not PASSWORD:
        print("Missing environment variables. Please check your .env file.")
        return
    
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    code = automate_login()
    if not code:
        print("Failed to obtain authorization code. Check logs for details.")
        auth_code_received.set()
        return

    auth_code_received.wait()
    if oauth_object:
        accessToken = oauth_object.get('access_token')
        base_url = get_base_url(accessToken)
        userDetails = get_user_details(accessToken, base_url) if base_url else None
        userId = userDetails.get('email', 'unknown') if userDetails else 'unknown'
        refresh_token = oauth_object.get('refresh_token', 'unknown')
        access_token = oauth_object.get('access_token', 'unknown')

        # Print results to terminal
        print(f"User ID: {userId}")
        print(f"OAuth Object: {json.dumps(oauth_object, indent=2)}")
    else:
        print("Failed to obtain authorization token. Check logs for details.")
    
    # Shut down Flask server
    requests.post(f"http://{HOST_NAME}:{PORT}/shutdown")
    flask_thread.join()

if __name__ == '__main__':
    main()
