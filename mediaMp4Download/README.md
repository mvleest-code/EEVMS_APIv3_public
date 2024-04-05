# apiv3_mp4_dl.py
Added new version, only access token and esn are needed for this one<br>
<br>
<br>
# APIv3_mp4_downloader
Eagle Eye Networks API v3 MP4 Downloader<br>
<br>
For this script I use access_response.json which contains access_token.<br>
Add deviceId = camera esn<br>
add baseUrl = get it from the client settings endpoint<br>
add mediaUrl = same as baseUrl but replace "api" for "media"<be>
<br>
<br>
```
with open('access_response.json') as user_file:
    file_contents = json.load(user_file)
    access_token = file_contents["access_token"]
    token_type = file_contents["token_type"]
    deviceId = ""
    baseUrl = "api.cxxx.eagleeyenetworks.com"
    mediaUrl = "media.cxxx.eagleeyenetworks.com"
    unencoded_startTimestamp = "2023-10-23T00:00:00.000+00:00"
    unencoded_endTimestamp = "2023-10-23T23:59:00.000+00:00"
```
<br>
