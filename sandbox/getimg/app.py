import requests
import json
import os
import logging
from datetime import datetime, timezone

# Configuration - set these variables
ACCESS_TOKEN = ""
BASE_URL = "https://api.c013.eagleeyenetworks.com/api/v3.0"
DEVICE_ID = ""

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def format_timestamp(dt):
    """Format datetime to ISO 8601 with exactly 3 decimal places for milliseconds"""
    # Format with 3 decimal places for milliseconds
    formatted = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"
    return formatted

def get_media_list():
    """Get recordings from today for the specified device"""
    logger.debug(f"Getting list of today's recordings for device {DEVICE_ID}")
    
    # Today's start in ISO 8601 with proper formatting
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_timestamp = format_timestamp(today_start)
    
    # Current time with proper formatting
    end_timestamp = format_timestamp(datetime.now(timezone.utc))
    
    endpoint = f"{BASE_URL}/media"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "deviceId": DEVICE_ID,
        "type": "main",
        "mediaType": "video",
        "startTimestamp__gte": start_timestamp,
        "endTimestamp__lte": end_timestamp,
        "coalesce": "true"
    }
    
    logger.debug(f"API call: GET {endpoint} with params: {params}")
    response = requests.get(endpoint, headers=headers, params=params)
    
    logger.debug(f"Status code: {response.status_code}")
    logger.debug(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        media_data = response.json()
        results = media_data.get('results', [])
        logger.debug(f"Found {len(results)} recordings")
        return results
    else:
        logger.error(f"Failed to get recordings: {response.text}")
        return []

def download_image(timestamp, stream_type="main"):
    """Download image at specified timestamp"""
    logger.debug(f"Downloading image: device={DEVICE_ID}, time={timestamp}")
    
    endpoint = f"{BASE_URL}/media/recordedImage.jpeg"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "image/jpeg"
    }
    
    params = {
        "deviceId": DEVICE_ID,
        "type": stream_type,
        "timestamp__gte": timestamp
    }
    
    logger.debug(f"API call: GET {endpoint} with params: {params}")
    response = requests.get(endpoint, headers=headers, params=params)
    
    logger.debug(f"Status code: {response.status_code}")
    logger.debug(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        # Get timestamp from header or use original
        resp_timestamp = response.headers.get('X-Een-Timestamp', timestamp)
        
        # Format for filename
        try:
            if 'Z' in resp_timestamp:
                resp_timestamp = resp_timestamp.replace('Z', '+00:00')
            timestamp_obj = datetime.fromisoformat(resp_timestamp)
            filename = timestamp_obj.strftime("%Y%m%d_%H%M%S") + ".jpg"
        except (ValueError, TypeError):
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_unknown.jpg"
            logger.warning(f"Could not parse timestamp {resp_timestamp}")
        
        # Ensure img directory exists
        os.makedirs("img", exist_ok=True)
        
        # Save image
        image_path = os.path.join("img", filename)
        with open(image_path, "wb") as f:
            f.write(response.content)
        
        logger.debug(f"Image saved to {image_path}")
        return image_path
    else:
        logger.error(f"Failed to download image: {response.text}")
        return None

def main():
    logger.info(f"Starting recording image downloader for device {DEVICE_ID}")
    
    # Get today's recordings
    recordings = get_media_list()
    
    if not recordings:
        logger.warning("No recordings found for today")
        return
    
    # Download image from each recording's start time
    for recording in recordings:
        start_timestamp = recording.get("startTimestamp")
        stream_type = recording.get("type", "main")
        
        if start_timestamp:
            logger.info(f"Processing recording with start={start_timestamp}")
            download_image(start_timestamp, stream_type)
        else:
            logger.warning(f"Skipping recording with missing timestamp: {recording}")
    
    logger.info("All recordings processed")

if __name__ == "__main__":
    main()