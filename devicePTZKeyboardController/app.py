import requests
from pynput import keyboard
import threading
import time
import json
import os

# Eagle Eye Networks API version 3 PTZ Keyboard Control.
# This script will allow you to control a PTZ camera using the keyboard.

# Global control variables
current_direction = None
control_thread_running = False
control_thread = None

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# Clear the screen at the start of the program.
clear_screen()
print("PTZ Keyboard Control, checking for cameras...")
# Request the client settings, this will return the base URL.
def clientsettings():
    with open('access_response.json') as user_file:
        file_contents = json.load(user_file)
        access_token = file_contents["access_token"]
        token_type = file_contents["token_type"]
        url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
        headers = {"accept": "application/json",
                    "authorization": token_type + access_token}
        response = requests.get(url, headers=headers)
        vmshostname = response.json()["httpsBaseUrl"]["hostname"]
        return access_token, token_type, vmshostname

# Request the cameras, and check for PTZ capabilities.
def fetch_cameras(token_type, access_token, vmshostname):
    url = f"https://{vmshostname}/api/v3.0/cameras?include=capabilities&pageSize=100"
    headers = {"accept": "application/json",
                "authorization": f"{token_type} {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cameras = response.json().get("results", [])
        ptz_cameras = [cam for cam in cameras if cam["capabilities"]["ptz"]["capable"] and 
                        cam["capabilities"]["ptz"]["panTilt"] and 
                        cam["capabilities"]["ptz"]["zoom"] and 
                        cam["capabilities"]["ptz"]["directionMove"]]
        return ptz_cameras
    else:
        print(f"Error fetching cameras: {response.json()}")
        return []

# Select a camera from the list of PTZ-capable cameras.
def select_camera(cameras):
    clear_screen()
    print("Select a camera for PTZ control:")
    for i, cam in enumerate(cameras, start=1):
        print(f"{i}. {cam['name']}")
    choice = int(input("Enter the number of the camera: ")) - 1
    clear_screen()
    print("PTZ Keyboard Control")
    print("Control the camera with arrow keys for direction, Page Up for zoom in, and Page Down for zoom out.")
    return cameras[choice]["id"]

# Control the camera with the selected direction.
def control_camera(camid, token_type, access_token, vmshostname):
    global current_direction, control_thread_running
    control_thread_running = True
    while control_thread_running:
        if current_direction:
            url = f"https://{vmshostname}/api/v3.0/cameras/{camid}/ptz/position"
            payload = {
                "direction": [current_direction],
                "moveType": "direction",
                "stepSize": "medium"
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": token_type + ' ' + access_token
            }
            clear_screen()
            print("PTZ Keyboard Control")
            print("Control the camera with arrow keys for direction, Page Up for zoom in, and Page Down for zoom out.")
            response = requests.put(url, json=payload, headers=headers)
            print(f"Moved camera successfully: {response.status_code}")
        time.sleep(0.1)

# Key press event handler
def on_press(key):
    global current_direction, control_thread, control_thread_running
    key_id = getattr(key, 'name', getattr(key, 'char', None))
    if key_id in ['left', 'right', 'up', 'down', 'page_up', 'page_down']:
        current_direction = key_id

# Key release event handler 
def on_release(key):
    global current_direction
    key_id = getattr(key, 'name', getattr(key, 'char', None))
    if key_id == current_direction:
        current_direction = None

# Main function
def main():
    access_token, token_type, vmshostname = clientsettings()
    ptz_cameras = fetch_cameras(token_type, access_token, vmshostname)
    if ptz_cameras:
        selected_cam_id = select_camera(ptz_cameras)
        control_thread = threading.Thread(target=control_camera, args=(selected_cam_id, token_type, access_token, vmshostname))
        control_thread.start()
        with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as _listener:
            _listener.join()
        control_thread_running = False
        control_thread.join()
    else:
        print("No PTZ-capable cameras found.")

if __name__ == "__main__":
    main()
