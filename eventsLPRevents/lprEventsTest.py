import requests
import json
import logging
from datetime import datetime

access_token = ""
base_url = ""

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')
print ("Eagle Eye Networks - License Plate Recognition - Events Endpoint")
base_url = f"https://{base_url}/api/v3.0/lprEvents"
params = {
    "timestamp__gte": "20240409143000.000",
    "timestamp__lte": "20240422141500.000",
    "pageSize": "100",
    "include": "data.een.lprDetection.v1",
    "pageToken": None
}

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {access_token}"
}

output_file = open("output.log", "w")

event_count = 0
plate_set = set()
entry_count = 0
exit_count = 0

while True:
    # Log the request URL
    logging.debug(f"Request URL: {base_url} with parameters: {params}")

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    output_file.write(json.dumps(data, indent=4))
    output_file.write("\n")
    nextPageToken = data.get("nextPageToken")
    if nextPageToken is not None:  # Check if nextPageToken is None explicitly
        params["pageToken"] = nextPageToken
        for event in data.get("results", []):
            if "id" in event:
                event_count += 1
                print(f"Events fetched: {event_count}", end='\r')
                for data_item in event.get("data", []):
                    if data_item.get("type") == "een.lprDetection.v1":
                        plate = data_item.get("plate", None)
                        if plate:
                            plate_set.add(plate)
                        direction = data_item.get("direction", None)
                        if direction == "entry":
                            entry_count += 1
                        elif direction == "exit":
                            exit_count += 1
    else:
        break

print(f"Total events fetched: {event_count}")
print(f"Total different plates: {len(plate_set)}")
print(f"Total entry events: {entry_count}")
print(f"Total exit events: {exit_count}")

output_file.close()