## Media cookie example  ##

How to use the Media Session to be able to use the /media /feeds url's.

Without the requesting this Media Session it's not possible to access any video from API v3

## The logic: ##
1. Use the access token to make the request to https://api.c***.eagleeyenetworks.com/api/v3.0/media/session
   This will set the browser Media Cookie.
2. When Step one is successfull, you should be able to load any of the /media /feed URL's.
   An example is the following multipartUrl of the preview stream:
   https://media.c***.eagleeyenetworks.com:443/media/streams/preview/multipart?esn=1002931e&stream_session=df8b1c36-3c9c-440c-88ed-d6cf562717f4

## notes: ##
Always make sure to use the correct baseUrl api.c***.eagleeyenetworks.com this can be obtained from the authentication response or by making a GET request to : https://api.eagleeyenetworks.com/api/v3.0/clientSettings

## Common errors ##
Using the Eagle Eye Networks APIv3 should always be done from a CORS whitelisted domain. 
When you are in doubt or if you are having issues with the iFrame please check the console for error reporting.
CORS error = As already mentioned, the domain is not whitelisted, this will litterly say CORS error in the console log.

If you open the index.html file from your browser this will always return a CORS error, within this repository I added a Python Flask server that serves the html file on: http://127.0.0.1:3333 this localhost domain has been whitelisted for local testing/development.