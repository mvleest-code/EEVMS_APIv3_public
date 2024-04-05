import os
import requests
import json
import logging


# Constants
TIMESTAMP_FORMAT0 = "%3A"
TIMESTAMP_FORMAT1 = "%2B"
OUTPUT_FOLDER = "mp4dl"

# Load access token
try:
    with open('access_response.json') as user_file:
        access_token = json.load(user_file)["access_token"]
except (IOError, KeyError) as e:
    logging.error(f"Failed to load access token from 'access_response.json': {e}")
    exit(1)

# Headers
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {access_token}",
}

# Session
session = requests.Session()
session.headers.update(headers)

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Device ID and timestamps
deviceId = "100f9f79"
pageSize = 5000
unencoded_startTimestamp = "2023-11-27T00:00:00.000+00:00"
unencoded_endTimestamp = "2023-11-30T23:59:00.000+00:00"
startTimestamp = unencoded_startTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
endTimestamp = unencoded_endTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)

def make_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to make request to {url}: {e}")
        raise  # Re-raise the exception for better error handling
    return response

def get_session_response(base_url):
    session_url = f"https://{base_url}/api/v3.0/media/session"
    print("/media/session requested")
    return make_request(session_url)

def clientsettings():
    url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
    try:
        return make_request(url).json()["httpsBaseUrl"]["hostname"]
    except (json.JSONDecodeError, KeyError, requests.exceptions.RequestException) as e:
        logging.error(f"Failed to get client settings: {e}")
        raise

base_url = clientsettings()
#media_url = base_url.replace("api", "media")
media_url = clientsettings()

def download_image(url, file_name):
    try:
        print(f"Downloading image from {url}")
        response = session.get(url, stream=True)
        response.raise_for_status()
        file_path = os.path.join(OUTPUT_FOLDER, file_name)
        with open(file_path, "wb") as image_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    image_file.write(chunk)
        print(f"Image file saved as {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image from {url}: {e}")
        # Log the error and continue with the next iteration
        pass
    
def main():
    try:
        # Get the session response
        session_response = get_session_response(base_url)

        # Handle the session response if needed
        if session_response.status_code == 200:
            print("Session response received successfully.")
            # Process the session response as needed
        else:
            print("Failed to get session response.")
            print(session_response.status_code)

        # Continue with the rest of your main logic
        url = f"https://{base_url}/api/v3.0/media?deviceId={deviceId}&type=main&mediaType=video&startTimestamp__gte={startTimestamp}&endTimestamp__lte={endTimestamp}&pageSize={pageSize}"
        response = make_request(url)

        if response.status_code == 200:
            data = response.json()
            results = data["results"]

            for result in results:
                startTimestamp2 = result["startTimestamp"]
                endTimestamp2 = result["endTimestamp"]

                startTimestamp1 = startTimestamp2.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
                endTimestamp1 = endTimestamp2.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)

                start_url = f"https://{media_url}/api/v3.0/media/recordedImage.jpeg?deviceId={deviceId}&type=main&timestamp={startTimestamp1}"
                end_url = f"https://{media_url}/api/v3.0/media/recordedImage.jpeg?deviceId={deviceId}&type=main&timestamp={endTimestamp1}"

                download_image(start_url, f"{deviceId}_{startTimestamp2}_main_image.jpeg")
                #download_image(end_url, f"{deviceId}_{endTimestamp1}_image.jpeg")
        else:
            print("Failed to get images.")
            print(response.status_code)

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the main execution: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
