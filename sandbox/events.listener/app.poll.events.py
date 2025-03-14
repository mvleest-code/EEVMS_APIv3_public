import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from dotenv import load_dotenv
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

# Load environment variables from .env file if present
load_dotenv()

# Authentication Configuration
AUTH_URL = "https://auth.eagleeyenetworks.com/oauth2/token"
CLIENT_ID = "" # add your client ID here
CLIENT_SECRET = "" # add your client secret here
REFRESH_TOKEN = "" # add your refresh token here
BASE_URL = ""  # Default, will be updated from token response

# Token and camera state
access_token = None
token_expiry = None
cameras = {}
last_event_time = None

def format_time(dt):
    """Convert datetime to ISO format with +01:00 timezone offset"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    tz = timezone(timedelta(hours=1))
    dt_converted = dt.astimezone(tz)
    return dt_converted.isoformat(timespec='milliseconds')

def get_access_token():
    """Get an access token using the refresh token"""
    global access_token, token_expiry, BASE_URL
    
    logger.info("Getting new access token")

    # Correctly encode client credentials in Base64
    client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    encoded_credentials = base64.b64encode(client_credentials).decode("utf-8")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(AUTH_URL, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            # Set token expiry 5 minutes before actual expiry to be safe
            expires_in = int(token_data.get("expires_in", 3600)) - 300
            token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            # Update BASE_URL if provided in response
            if "httpsBaseUrl" in token_data and "hostname" in token_data["httpsBaseUrl"]:
                BASE_URL = f"https://{token_data['httpsBaseUrl']['hostname']}"
                logger.info(f"Updated base URL to {BASE_URL}")
            
            logger.info(f"Successfully obtained access token, expires in {expires_in} seconds")
            return True
        else:
            logger.error(f"Failed to get access token: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception during token acquisition: {str(e)}")
        return False

def refresh_token_if_needed():
    """Check if token needs refreshing and refresh if so"""
    global token_expiry
    
    if token_expiry is None or datetime.now() >= token_expiry:
        return get_access_token()
    return True

def get_all_cameras():
    """Retrieve all cameras for the account"""
    global cameras
    
    if not refresh_token_if_needed():
        return False
        
    logger.info("Retrieving cameras")
    url = f"{BASE_URL}/api/v3.0/cameras"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    params = {
        "pageSize": 100,
        "sort": "+name"
    }
    
    cameras_found = {}
    page_token = None
    
    try:
        while True:
            if page_token:
                params["pageToken"] = page_token
                
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to get cameras: {response.status_code} - {response.text}")
                return False
                
            data = response.json()
            results = data.get("results", [])
            
            for cam in results:
                cam_id = cam["id"]
                cam_name = cam["name"]
                cameras_found[cam_id] = cam_name
                logger.info(f"Found camera: {cam_name} (ID: {cam_id})")
                
            page_token = data.get("nextPageToken", "")
            if not page_token:
                break
                
        cameras = cameras_found
        logger.info(f"Retrieved {len(cameras)} cameras")
        return True
    except Exception as e:
        logger.error(f"Exception while retrieving cameras: {str(e)}")
        return False

def poll_events():
    """Poll for new person detection events"""
    global last_event_time
    
    if not refresh_token_if_needed():
        return
        
    # Initialize last_event_time if not set
    if last_event_time is None:
        last_event_time = datetime.now(timezone.utc) - timedelta(minutes=5)  # Start with events from last 5 minutes
    
    now = datetime.now(timezone.utc)
    
    logger.debug(f"Polling for events since {last_event_time}")
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    
    all_events = []
    
    # Check each camera for events
    for cam_id, cam_name in cameras.items():
        params = {
            "pageSize": 100,
            "startTimestamp__gte": format_time(last_event_time),
            "startTimestamp__lte": format_time(now),
            "actor": f"camera:{cam_id}",
            "type__in": "een.motionDetectionEvent.v1,een.motionInRegionDetectionEvent.v1",
            "include": [
            "data.een.motionRegion.v1",
            "data.een.objectDetection.v1",
            "data.een.croppedFrameImageUrl.v1",
            "data.een.fullFrameImageUrl.v1"
              ]
        }
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/v3.0/events",
                params=params, 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                events = data.get("results", [])
                
                # Add camera name to each event
                for event in events:
                    event["cameraName"] = cam_name
                    
                all_events.extend(events)
            else:
                logger.warning(f"Failed to get events for camera {cam_name}: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Exception while polling events for camera {cam_name}: {str(e)}")
    
    # Update last_event_time to now
    last_event_time = now
    
    # Process events (newest first)
    if all_events:
        all_events.sort(key=lambda e: e.get("startTimestamp") or e.get("createTimestamp") or "", reverse=True)
        
        logger.info(f"Found {len(all_events)} new events")
        
        for event in all_events:
            camera_name = event.get("cameraName", "Unknown Camera")
            timestamp = event.get("startTimestamp") or event.get("createTimestamp")
            confidence = event.get("confidence", "N/A")
            
            # Log each event summary
            logger.info(f"EVENT: Camera: {camera_name}, Time: {timestamp}, Confidence: {confidence}")

            # Log full JSON event data in log file
            logger.info(f"Full event data:\n{json.dumps(event, indent=2)}")

def main():
    """Main application loop"""
    logger.info("Starting Eagle Eye Network event monitor")
    
    # Get initial access token
    if not get_access_token():
        logger.error("Failed to get initial access token. Exiting.")
        return
    
    # Get cameras
    if not get_all_cameras():
        logger.error("Failed to retrieve cameras. Exiting.")
        return
    
    # Main polling loop
    try:
        while True:
            poll_events()
            # Sleep for 30 seconds before polling again
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()