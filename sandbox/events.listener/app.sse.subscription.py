import os
import json
import time
import logging
import requests
import datetime
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("events.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# API Authentication
AUTH_URL = "https://auth.eagleeyenetworks.com/oauth2/token"
CLIENT_ID = "" # add your client ID here
CLIENT_SECRET = "" # add your client secret here
REFRESH_TOKEN = input("Enter your refresh token: ")

# Token and API Configuration
access_token = None
token_expiry = None
BASE_URL = ""

# List of all event types
EVENT_TYPES = [
    "een.motionDetectionEvent.v1",
    "een.motionInRegionDetectionEvent.v1"
]

def get_access_token():
    """Fetch a new access token using the refresh token."""
    global access_token, token_expiry, BASE_URL

    logger.info("Requesting new access token...")
    
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    payload = {"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN}
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(AUTH_URL, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data.get("access_token")
        expires_in = int(token_data.get("expires_in", 3600)) - 300
        token_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

        # Update base URL
        if "httpsBaseUrl" in token_data and "hostname" in token_data["httpsBaseUrl"]:
            BASE_URL = f"https://{token_data['httpsBaseUrl']['hostname']}"
            logger.info(f"Updated base URL: {BASE_URL}")

        logger.info(f"Access token obtained, expires in {expires_in} seconds.")
        return True
    except Exception as e:
        logger.error(f"Failed to get access token: {str(e)}")
        return False


def refresh_token_if_needed():
    """Refresh the access token if it's expired."""
    global token_expiry
    if token_expiry is None or datetime.datetime.utcnow() >= token_expiry:
        return get_access_token()
    return True


def get_all_cameras():
    """Retrieve all camera IDs."""
    if not refresh_token_if_needed():
        return []

    logger.info("Fetching camera list...")
    url = f"{BASE_URL}/api/v3.0/cameras"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    params = {"pageSize": 100}

    camera_ids = []
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for cam in data.get("results", []):
            camera_ids.append(cam["id"])
            logger.info(f"Camera found: {cam['name']} (ID: {cam['id']})")

        return camera_ids
    except Exception as e:
        logger.error(f"Failed to get cameras: {str(e)}")
        return []


def create_sse_subscription(camera_ids):
    """Create an SSE subscription for all specified event types."""
    if not refresh_token_if_needed():
        return None

    url = f"{BASE_URL}/api/v3.0/eventSubscriptions"
    payload = json.dumps({
        "deliveryConfig": {"type": "serverSentEvents.v1"},
        "filters": [
            {"actors": [f"camera:{cam_id}" for cam_id in camera_ids],
             "types": [{"id": event} for event in EVENT_TYPES]}
        ]
    })
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        sse_data = response.json()
        
        if "deliveryConfig" not in sse_data:
            logger.error("Invalid SSE subscription response:")
            logger.error(json.dumps(sse_data, indent=2))
            return None

        sse_url = sse_data["deliveryConfig"]["sseUrl"]
        logger.info(f"SSE subscription created successfully: {sse_url}")
        return sse_url
    except Exception as e:
        logger.error(f"Failed to create SSE subscription: {str(e)}")
        return None


def listen_to_sse(sse_url):
    """Connect to the SSE stream and listen for events."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "text/event-stream",
        'Accept-Encoding': ''
    }

    while True:
        try:
            with requests.get(sse_url, headers=headers, stream=True, timeout=60) as response:
                if response.status_code == 200:
                    logger.info("Connected to SSE stream, waiting for events...")
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            logging.info(decoded_line)
                            print(decoded_line)
                else:
                    logger.error(f"Failed to connect to SSE stream: {response.status_code}")
                    logger.error(response.text)

        except Exception as e:
            logger.error(f"SSE Listener Error: {str(e)}")

        logger.info("Reconnecting in 5 seconds...")
        time.sleep(5)


def main():
    """Main function to set up and start SSE listener."""
    logger.info("Starting Eagle Eye SSE Listener")

    if not get_access_token():
        logger.error("Failed to authenticate. Exiting.")
        return

    camera_ids = get_all_cameras()
    if not camera_ids:
        logger.error("No cameras found. Exiting.")
        return

    sse_url = create_sse_subscription(camera_ids)
    if not sse_url:
        logger.error("Failed to create SSE subscription. Exiting.")
        return

    listen_to_sse(sse_url)


if __name__ == "__main__":
    main()