import os
import requests
import json
import time

start_script_time = time.time()  # Measure the start time of the script

TIMESTAMP_FORMAT0 = "%3A"
TIMESTAMP_FORMAT1 = "%2B"

access_token = ""
token_type = "Bearer"
actorId = "camera:XXXXXX"
baseUrl = "api.cXXX.eagleeyenetworks.com"
event_types = [
    "een.deviceCloudStatusUpdateEvent.v1",
    "een.motionDetectionEvent.v1",
    "een.lprPlateReadEvent.v1",
    "een.tamperDetectionEvent.v1",
    "een.objectIntrusionEvent.v1",
    "een.objectLineCrossEvent.v1",
    "een.loiterDetectionEvent.v1"
]

pageSize = "pageSize=50000"
date = "2024-01-20"
unencoded_startTimestamp = f"{date}T00:00:00.000+00:00"
unencoded_endTimestamp = f"{date}T23:59:59.000+00:00"
startTimestamp = unencoded_startTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
endTimestamp = unencoded_endTimestamp.replace(":", TIMESTAMP_FORMAT0).replace("+", TIMESTAMP_FORMAT1)
print(unencoded_startTimestamp, "to", unencoded_endTimestamp)

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {access_token}"
}

for event_type in event_types:
    typeIn = event_type
    url = f"https://{baseUrl}/api/v3.0/events?{pageSize}&startTimestamp__gte={startTimestamp}&endTimestamp__lte={endTimestamp}&actor={actorId}&type__in={typeIn}"

    request_times = []  # List to store request times

    for i in range(10):
        start_time = time.time()  # Initialize start_time before calculating request time
        response = requests.get(url, headers=headers)
        end_time = time.time()
        request_time = end_time - start_time
        request_times.append(request_time)  # Add request time to the list

        response_json = json.loads(response.text)
        #print response status code to see if all the requests come through
        #print(response.status_code)
        total_size = response_json.get("totalSize")

        # Get the current subfolder path
        current_folder = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(current_folder, f"output_{event_type}.txt")

        with open(output_file_path, "w") as file:
            file.write(json.dumps(response_json, indent=4))

    # Calculate average, lowest, and highest request times
    average_request_time = sum(request_times) / len(request_times)
    lowest_request_time = min(request_times)
    highest_request_time = max(request_times)

    print(f"Event type: {event_type}")
    print(f"Average request time: {average_request_time} seconds")
    print(f"Lowest request time: {lowest_request_time} seconds")
    print(f"Highest request time: {highest_request_time} seconds")
    print(f"Total number of events: {total_size}")

end_script_time = time.time()  # Measure the end time of the script
total_script_time = end_script_time - start_script_time  # Calculate the total script time
print(f"Total script time: {total_script_time} seconds")
