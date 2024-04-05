import json
import requests
from flask import Flask, request, make_response, render_template_string, redirect

hostName = "127.0.0.1"
port = 3333

clientId = ""
clientSecret = ""

app = Flask(__name__)

def getTokens(code):
    url = f"https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code={code}&redirect_uri=http://{hostName}:{port}"
    try:
        response = requests.post(url, auth=(clientId, clientSecret))
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        return json.loads(response.text)
    except requests.RequestException as e:
        print(f"Error getting tokens: {e}")
        return None

@app.route('/')
def index():
    code = request.args.get('code')
    if code:
        oauthObject = getTokens(code)
        access_token = oauthObject.get('access_token', '')
        # Get the base URL
        base_url = get_base_url(access_token)
        response = make_response(render_template_string(HTML_TEMPLATE))
        response.set_cookie('access_token', access_token)
        response.set_cookie('base_url', base_url)
        return response
    else:
        endpoint = "https://auth.eagleeyenetworks.com/oauth2/authorize"
        requestAuthUrl = f"{endpoint}?client_id={clientId}&response_type=code&scope=vms.all&redirect_uri=http://{hostName}:{port}"
        return redirect(requestAuthUrl)

def get_base_url(access_token):
    url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        settings = json.loads(response.text)
        hostname = settings.get('httpsBaseUrl', {}).get('hostname')
        if hostname:
            return f"{hostname}"
    return None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Player</title>
    <link rel="shortcut icon" href="https://auth.eagleeyenetworks.com/images/favicon.ico">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.min.css">
    <script src="https://cdn.jsdelivr.net/npm/hls.js@1"></script>
    <style>
        body { margin: 40px; }
        .container { max-width: 600px; margin: auto; }
        .description { margin-bottom: 20px; }
        #video, #mjpeg { display: none; width: 100%; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video Player</h1>
        <p class="description">
            Copy the access token and use it to generate the video streams on developer.eagleeyenetworks.com.
        </p>
        <input type="text" id="accessToken" class="column column-90" value="{{ access_token }}" readonly />
        <button onclick="copyAccessToken()" class="column">COPY</button>
        
        <script>
        function copyAccessToken() {
            var accessTokenInput = document.getElementById('accessToken');
            if (accessTokenInput) {
                accessTokenInput.select();
                document.execCommand('copy');
            }
        }
        </script>
        <p class="description">
            Select the video format and enter the URL in the input field below. Supported formats are HLS, MP4, and MJPEG.
        </p>
        <select id="formatSelect">
            <option value="hls">HLS (LIVE)</option>
            <option value="mp4">MP4 (RECORDING)</option>
            <option value="mjpeg">MJPEG multipart</option>
        </select>
        <input type="text" id="videoUrl" class="column column-90" placeholder="Enter video URL here" />
        <button onclick="loadVideo()" class="column">PLAY</button>
        <video id="video" controls muted="muted"></video>
        <img id="mjpeg">
    </div>
    
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Try to fetch access token from cookie first
    var accessToken = getCookie('access_token');
    
    // Fallback to the value injected by Flask if the cookie is not set
    if (!accessToken) {
        accessToken = "{{ access_token }}"; // This line is server-side templating and will be evaluated by Flask
    }

    // Set the access token in the input field
    var accessTokenInput = document.getElementById('accessToken');
    if (accessToken && accessTokenInput) {
        accessTokenInput.value = accessToken;
    }
}, false);
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadVideo() {
        var format = document.getElementById('formatSelect').value;
        var videoSrc = document.getElementById('videoUrl').value;
        var video = document.getElementById('video');
        var mjpeg = document.getElementById('mjpeg');
        var accessToken = getCookie('access_token');
        
        video.style.display = 'none';
        mjpeg.style.display = 'none';

        if (format === 'hls') {
            video.style.display = 'block';
            if (Hls.isSupported()) {
                var hls = new Hls({
                    xhrSetup: function(xhr, url) {
                        xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
                    }
                });
                hls.loadSource(videoSrc);
                hls.attachMedia(video);
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = videoSrc;
            }
        } else if (format === 'mp4') {
            video.style.display = 'block';
            video.src = videoSrc;
            video.setAttribute('type', 'video/mp4');
        } else if (format === 'mjpeg') {
            mjpeg.style.display = 'block';
            mjpeg.src = videoSrc;
        } else {
            alert('Unsupported video format. Please select a valid format.');
        }
    }

    function getSessionAndPlay() {
        var requestOptions = {
            method: 'GET',
            headers: {
                "Authorization": "Bearer " + getCookie('access_token')
            },
            credentials: 'include'
        };

        fetch("https://" + getCookie('base_url') + "/api/v3.0/media/session", requestOptions)
            .then(response => response.json())
            .then(body => {
                console.log("Media session URL: ", body.url);
            })
            .catch(error => console.log('error', error));
    }
</script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host=hostName, port=port, debug=True)
