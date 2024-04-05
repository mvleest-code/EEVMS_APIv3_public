import os
import requests
import json
import logging
from tqdm import tqdm

# Constants
TIMESTAMP_FORMAT0 = "%3A"
TIMESTAMP_FORMAT1 = "%2B"
OUTPUT_FOLDER = "mp4dl"

# Load access token
try:
    with open('access_response.json') as user_file:
        file_contents = json.load(user_file)
        access_token = file_contents["access_token"]
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
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Device ID and timestamps
deviceId = "1001e90f"
unencoded_startTimestamp = "2023-11-05T00:00:00.000+00:00"
unencoded_endTimestamp = "2023-11-07T23:59:00.000+00:00"
startTimestamp = unencoded_startTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
endTimestamp = unencoded_endTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)

def make_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to make request to {url}: {e}")
        exit(1)
    return response

def clientsettings():
    url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
    response = make_request(url)
    return response.json()["httpsBaseUrl"]["hostname"]

baseUrl = clientsettings()

def get_session_response(base_url):
    session_url = f"https://{base_url}/api/v3.0/media/session"
    return make_request(session_url)

session_response = get_session_response(baseUrl)

def download_mp4(mp4_url, file_name):
    try:
        mp4_response = session.get(mp4_url, stream=True)
        mp4_response.raise_for_status()
        file_path = os.path.join(OUTPUT_FOLDER, file_name)
        total_size = int(mp4_response.headers.get('content-length', 0))

        with open(file_path, "wb") as mp4_file, tqdm(
            desc=file_name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in mp4_response.iter_content(chunk_size=1024):
                mp4_file.write(data)
                progress_bar.update(len(data))
        print(f"MP4 file saved as {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download MP4 file from {mp4_url}: {e}")

def download_all_mp4_urls(results):
    for result in results:
        mp4_url = result["mp4Url"]
        startTimestamp = result["startTimestamp"].replace("%3A", ":")
        endTimestamp = result["endTimestamp"].replace("%3A", ":")
        file_name = f"{deviceId}_{startTimestamp}_{endTimestamp}_output.mp4"
        download_mp4(mp4_url, file_name)

def main():
    url = f"https://{baseUrl}/api/v3.0/media?deviceId={deviceId}&type=main&mediaType=video&startTimestamp__gte={startTimestamp}&endTimestamp__lte={endTimestamp}&coalesce=true&include=mp4Url&pageSize=100"
    response = make_request(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        results = data["results"]
        download_all_mp4_urls(results)
    else:
        print("Failed to get MP4 URLs from the API")
        print(response.status_code)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")