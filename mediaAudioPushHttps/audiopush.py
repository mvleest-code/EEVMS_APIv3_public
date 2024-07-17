import requests

access_token = ""
cameraId = ""
print("sending audio to server...")
url = f'https://media.c001.eagleeyenetworks.com:443/media/streams/audio/{cameraId}/alaw'
headers = {
    'accept': '*/*',
    'Content-Type': 'multipart/form-data',
    'authorization': 'Bearer ' + access_token
    }
# select filed to be send:
files = {
    'data': ('rubberdukky.raw', open('rubberdukky.raw', 'rb'), 'audio/wav')
}
# making the actual request:
response = requests.post(url, headers=headers, files=files)
print ("audio sent successfully",response.status_code)