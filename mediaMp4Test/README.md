# mp4MediaTester
```
Index.html:
```
Very basic version on how to use the media/session for play video on EE APIv3<br>
<br>
```
Index.php
```
More complete version using input fields for access_token, MP4 URl to play the video.<br>
When "Load videos" button is pressed the script will use the access token to make a get request to /clientSettings to retrieve the baseUrl.<br> 
The baseUrl is needed to make the request to the 
MP4 media tester, using APIv3 to load: client settings, media session and play the video files

**ClientSettings**
```
<script>
const options = {
  method: 'GET',
  headers: {accept: 'application/json', authorization: 'Bearer <access_token>'}
};

fetch('https://api.eagleeyenetworks.com/api/v3.0/clientSettings', options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));
</script>
```
**Media/session:**
```
<script>
    var requestOptions = {
      method: 'GET',
      headers: {
        "Authorization" : "Bearer <YOUR ACCESS_TOKEN>"
      },
      credentials: 'include'
    };

    fetch("<YOUR BASE URL>/api/v3.0/media/session", requestOptions)
      .then(response => response.json() )
      .then( body => fetch(body.url, requestOptions) )
      .then( response => console.log("response status", response.status ) )
      .catch(error => console.log('error', error));
</script>
```
**Make sure to request them in the following order:**
1. get access token (via login, or in this script by user input field)
2. request client settings to obtain the baseUrl (api.c000.eagleeyenetworks, this should not be hardcoded as it changes per user api.cXXX.eagleeyenetworks,com)
3. use the baseUrl to make the request for the media/session (You need this in order to play the video)
4. make the request to play the MP4 url.
