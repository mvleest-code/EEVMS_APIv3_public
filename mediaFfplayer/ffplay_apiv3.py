import os
import subprocess
import requests
import json

def clientsettings():
    camid = "ESN"
    with open('access_response.json') as user_file:
        file_contents = json.load(user_file)
        access_token = file_contents["access_token"]
        token_type = file_contents["token_type"]
        url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
        headers = {"accept": "application/json",
                    "authorization": token_type + access_token
                    }
        response = requests.get(url, headers=headers)
        httpsBaseURL = response.json()["httpsBaseUrl"]["hostname"]       
        return access_token, token_type, httpsBaseURL, camid

def getcamsettings():
        ## request cameras ##        
        access_token, token_type, httpsBaseURL, camid = clientsettings()
        url = "https://" + httpsBaseURL + "/api/v3.0/cameras/" + camid
        headers = {"accept": "application/json",
                    "authorization": token_type +  ' ' +access_token
                    }
        getcam = requests.get(url, headers=headers)
        print("Get camerasettings", getcam.status_code)
        print(httpsBaseURL)

def getfeeds():
        ## request cameras ##        
        access_token, token_type, httpsBaseURL, camid = clientsettings()
        url = "https://" + httpsBaseURL + "/api/v3.0/feeds?deviceId=" + camid + "&type=main&include=flvUrl&include=rtspUrl&include=rtspsUrl&include=hlsUrl&include=multipartUrl&include=webRtcUrl&pageSize=100"
        headers = {"accept": "application/json",
                    "authorization": token_type +  ' ' +access_token
                    }
        getfeeds = requests.get(url, headers=headers)
        data = json.loads(getfeeds.text)
        print("Loading Camera Feeds", getfeeds.status_code)
        flvUrl = data['results'][0]['flvUrl']
        rtspUrl = data["results"][0]["rtspUrl"]
        rtspsUrl = data["results"][0]["rtspsUrl"]
        hlsUrl = data["results"][0]["hlsUrl"]
        multipart = data["results"][0]["multipartUrl"]
        return flvUrl, rtspUrl, rtspsUrl, hlsUrl, multipart

def print_menu():
    # Display menu with streaming protocol options
    print("Select an option (enter the corresponding number):")
    print("1- Multipart preview")
    print("2- Multipart full")
    print("3 - RTSP Over TCP")
    print("4 - RTSP Over UDP")
    print("5 - RTSPS")
    print("6 - HLS")
    print("7 - FLV")
    print("0 - Exit")
    
def execute_command(choice, token, url):
    # Execute the appropriate FFplay command based on user's choice
    commands = [
        "ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"",
        "ffplay -headers \"Authorization: Bearer {1}\" -f h264 \"{0}&flavor=ffmpeg\"",
        "ffplay -rtsp_transport tcp \"{}&access_token={}\"",
        "ffplay -rtsp_transport udp \"{}&access_token={}\"",
        "ffplay \"{}&access_token={}\"",
        "ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"",
        "ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"",
    ]
    cmd = commands[choice - 1].format(url,token)
    subprocess.run(cmd, shell=True)

def main():
    access_token, token_type, httpsBaseURL, camid = clientsettings()
    flvUrl, rtspUrl, rtspsUrl, hlsUrl, multipart = getfeeds()
    # Main loop: display menu, take input, execute command or exit
    while True:
        print_menu()
        choice = int(input())
        if choice == 0:
            break
        elif choice == 1:
            token = access_token
            url = multipart
            execute_command(choice, token, url)
        elif choice == 2:
            token = access_token
            url = multipart
            execute_command(choice, token, url)
        elif choice == 3:
            token = access_token
            url = rtspUrl
            execute_command(choice, token, url)
        elif choice == 4:
            token = access_token
            url = rtspUrl
            execute_command(choice, token, url)
        elif choice == 5:
            token = access_token
            url = rtspsUrl
            execute_command(choice, token, url)
        elif choice == 6:
            token = access_token
            url = hlsUrl
            execute_command(choice, token, url)
        elif choice == 7:
            token = access_token
            url = flvUrl
            execute_command(choice, token, url)    
        else:
            print("Invalid input. Please enter a number between 0 and 7.")
if __name__ == "__main__":
    main()
