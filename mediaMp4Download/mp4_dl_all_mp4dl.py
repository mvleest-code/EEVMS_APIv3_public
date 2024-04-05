import os
import requests
import json
import logging

TIMESTAMP_FORMAT0 = "%3A"
TIMESTAMP_FORMAT1 = "%2B"

# Define the folder path where you want to save the MP4 files
output_folder = "mp4dl"

# Ensure the output folder exists; create it if it doesn't
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load access token from the file
with open('access_response.json') as user_file:
    file_contents = json.load(user_file)
    access_token = file_contents["access_token"]
    token_type = file_contents["token_type"]
    deviceId = ""
    baseUrl = "api.cxxx.eagleeyenetworks.com"
    mediaUrl = "media.cxxx.eagleeyenetworks.com"
    unencoded_startTimestamp = "2023-10-23T00:00:00.000+00:00"
    unencoded_endTimestamp = "2023-10-23T23:59:00.000+00:00"
    startTimestamp = unencoded_startTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
    endTimestamp = unencoded_endTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
    
# Make a GET request to retrieve the session URL
session_url = f"https://{mediaUrl}/media/session"
headers = {
    "accept": "application/json",
    "authorization": "Bearer " + access_token
}
session_response = requests.get(session_url, headers=headers, cookies={'credentials': 'include'})
print("session_response", session_response)

session = requests.Session()
session.headers.update({"accept": "application/json", "authorization": "Bearer " + access_token})

def download_mp4(mp4_url, file_name):
    try:
        mp4_response = session.get(mp4_url)
        mp4_response.raise_for_status()
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "wb") as mp4_file:
            mp4_file.write(mp4_response.content)
        print(f"MP4 file saved as {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download MP4 file from {mp4_url}: {e}")


def download_all_mp4_urls(results):
    for result in results:
        mp4_url = result["mp4Url"]
        startTimestamp = result["startTimestamp"].replace("%3A", ":")
        endTimestamp = result["startTimestamp"].replace("%3A", ":")
        file_name = f"{deviceId}_{startTimestamp}_{endTimestamp}_output.mp4"
        download_mp4(mp4_url, file_name)

def main():
    url = f"https://{baseUrl}/api/v3.0/media?deviceId={deviceId}&type=main&mediaType=video&startTimestamp__gte={startTimestamp}&endTimestamp__lte={endTimestamp}&coalesce=true&include=mp4Url&pageSize=100"
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token
    }
    response = requests.get(url, headers=headers)
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
