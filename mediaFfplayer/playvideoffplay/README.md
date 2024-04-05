# ee_apiv3_playvideoffplay

**Code sample - Play live feeds with FFPLAY**

This code sample will help you in testing the video streams using our /feed endpoint

First make sure you have FFMPEG installed (this contains the FFPLAY application): 



```
https://ffmpeg.org/download.html
```


Next step will be running the Python script:

When running this script make sure to add the **camId** and the **access_token:**


```
camid = "<ADD_CAMERA_ID_HERE>"
access_token = "<ADD_ACCESS_TOKEN_HERE>"
```


The **playvideowithffplay.py** code:

  <tr>
   <td>

```
import os
import subprocess
import requests
import json

Temp = True

camid = "<ADD_CAMERA_ID_HERE>"
access_token = "<ADD_ACCESS_TOKEN_HERE>"
token_type = "Bearer"
url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
headers = {"accept": "application/json",
           "authorization": token_type + access_token
           }
response = requests.get(url, headers=headers)
httpsBaseURL = response.json()["httpsBaseUrl"]["hostname"]

print ("Loading Camera Feeds", camid)

def get_session_response(base_url, access_token):
   session_url = f"https://{base_url}/api/v3.0/media/session"
   headers = {
       "accept": "application/json",
       "authorization": "Bearer " + access_token
   }

   try:
       session_response = requests.get(session_url, headers=headers, cookies={'credentials': 'include'})
       session_response.raise_for_status()
   except requests.exceptions.RequestException as e:
       logging.error(f"Failed to retrieve session URL: {e}")
       exit(1)

   # Print all cookies
   print(dict(session_response.cookies))

   return session_response

# retrieve the session response
session_response = get_session_response(httpsBaseURL, access_token)

session = requests.Session()
session.headers.update({"accept": "application/json", "authorization": "Bearer " + access_token})

def getfeeds():
       ## request cameras ##       
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
       multipartUrl = data["results"][0]["multipartUrl"]
       return flvUrl, rtspUrl, rtspsUrl, hlsUrl, multipartUrl

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
       #"ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"",
       "ffplay -headers \"Authorization: Bearer {1}\" -f mjpeg \"{0}\"", # 1 multipart preview
       "ffplay -headers \"Authorization: Bearer {1}\" -f h264 \"{0}\"", # 2 multipart full
       "ffplay -rtsp_transport tcp \"{}&access_token={}\"", # 3 rtsp over tcp
       "ffplay -rtsp_transport udp \"{}&access_token={}\"", # 4 rtsp over udp
       "ffplay \"{}&access_token={}\"", # 5 rtsps
       "ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"", # 6 hls
       "ffplay -headers \"Authorization: Bearer {1}\" \"{0}\"", # 7 flv
   ]
   cmd = commands[choice - 1].format(url,token)
   subprocess.run(cmd, shell=True)

def main():
   flvUrl, rtspUrl, rtspsUrl, hlsUrl, multipartUrl = getfeeds()
   # Main loop: display menu, take input, execute command or exit
   while True:
       print_menu()
       choice = int(input())
       if choice == 0:
           break
       elif choice == 1:
           token = access_token
           url = multipartUrl
           execute_command(choice, token, url)
       elif choice == 2:
           token = access_token
           url = multipartUrl
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
```


   </td>
  </tr>
