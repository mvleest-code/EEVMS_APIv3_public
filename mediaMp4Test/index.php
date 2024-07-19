<!DOCTYPE html>
<html>
<head>
    <title>EEN Media Player</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            text-align: center;
            color: #333;
        }
        .container {
            width: 60%;
            max-width: 800px;
            margin: 30px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h2 {
            color: #444;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
            text-align: center;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type='text'], input[type='button'] {
            padding: 10px;
            width: 100%;
            margin-right: 5px;
            border: 1px solid #ddd;
            font-weight: bold;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type='button'], input[type='buttonremove'] {
            padding: 10px;
            width: 100%;
            margin-right: 5px;
            border: 1px solid #ddd;
            font-weight: bold;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type='button'] {
            background-color: #878484;
            color: white;
            width: 25%;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type='buttonremove'] {
            background-color: #878484;
            color: white;
            width: 25%;
            border: none;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type='button']:hover {
            background-color: #5cb85c;
        }
        input[type='buttonremove']:hover {
            background-color: #f75e5e;
        }
        .video-container {
            margin-top: 20px;
            align-items: center;
        }
        video {
            max-width: 100%;
            align-items: center;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
        }
        .video-grid {
            display: grid;
            align-items: center;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        .alert {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>MP4 - Video Loader</h2>
        <br><br>
        <form id="videoForm">
            <div class="input-group">
                <label for="accessToken">Access Token:</label>
                <input type="text" id="accessToken" name="accessToken" placeholder="Enter Access Token">
            </div>
            <div id="urlInputs">
                <div class="input-group">
                    <label for="mp4Url1">MP4 URL:</label>
                    <input type="text" id="mp4Url1" name="mp4Url[]" placeholder="Enter MP4 URL">
                    <br><br>
                    <input type="button" value="Add more MP4 URL's" onclick="addUrlInput()">
                </div>
            </div>
            <input type="button" value="Load Videos" onclick="loadVideos()">
        </form>
        <div id="videoContainer" class="video-container"></div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        loadSavedData();
        document.getElementById('accessToken').addEventListener('input', saveData);
        document.querySelectorAll('input[name="mp4Url[]"]').forEach(input => {
            input.addEventListener('input', saveData);
        });
    });

    let urlCount = 1;

    function addUrlInput(url = '') {
        if (urlCount < 4) {
            urlCount++;
            let newInputHtml = `<div class="input-group" id="inputGroup${urlCount}">
                                    <label for="mp4Url${urlCount}">MP4 URL:</label>
                                    <input type="text" id="mp4Url${urlCount}" name="mp4Url[]" value="${url}">
                                    <input type="buttonremove" value="Remove MP4 URL" onclick="removeUrlInput(${urlCount})">
                                </div>`;
            let newInputGroup = document.createElement('div');
            newInputGroup.innerHTML = newInputHtml;
            document.getElementById('urlInputs').appendChild(newInputGroup.firstChild);
            document.getElementById(`mp4Url${urlCount}`).addEventListener('input', saveData);
        }
    }

    function removeUrlInput(index) {
        let element = document.getElementById(`inputGroup${index}`);
        if (element) {
            element.remove();
            urlCount--;
            saveData();
        }
    }

    function saveData() {
        const accessToken = document.getElementById('accessToken').value;
        localStorage.setItem('accessToken', accessToken);

        const urls = Array.from(document.querySelectorAll('input[name="mp4Url[]"]')).map(input => input.value);
        localStorage.setItem('mediaUrls', JSON.stringify(urls));
    }

    function loadSavedData() {
        const savedToken = localStorage.getItem('accessToken');
        if (savedToken) {
            document.getElementById('accessToken').value = savedToken;
        }

        const savedUrls = JSON.parse(localStorage.getItem('mediaUrls'));
        if (savedUrls && savedUrls.length > 0) {
            savedUrls.forEach((url, index) => {
                if (index === 0) {
                    document.getElementById('mp4Url1').value = url;
                } else {
                    addUrlInput(url);
                }
            });
        }
    }

    async function loadVideos() {
        const accessToken = document.getElementById('accessToken').value;
        const urls = document.querySelectorAll('input[name="mp4Url[]"]');
        let videoContainer = document.getElementById('videoContainer');
        videoContainer.innerHTML = ''; // Clear previous videos

        try {
            // Fetch client settings
            console.log('Making request: Fetch client settings');
            const settingsResponse = await fetch('https://api.eagleeyenetworks.com/api/v3.0/clientSettings', {
                method: 'GET',
                headers: {
                    accept: 'application/json',
                    authorization: 'Bearer ' + accessToken
                }
            });

            if (!settingsResponse.ok) {
                throw new Error('Not able to request client settings');
            }

            console.log('Received response: Fetch client settings');

            const settingsData = await settingsResponse.json();
            const baseUrl = settingsData.httpsBaseUrl.hostname;

            // Establish media session
            console.log('Making request: Establish media session');
            const sessionResponse = await fetch(`https://${baseUrl}/api/v3.0/media/session`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                },
                credentials: 'include'
            });

            if (!sessionResponse.ok) {
                throw new Error('Not able to set media/session');
            }

            console.log('Received response: Establish media session');

            const sessionData = await sessionResponse.json();
            const mediaSessionUrl = sessionData.url;

            // Prepare video grid
            let videoGrid = document.createElement('div');
            videoGrid.className = 'video-grid';

            // Load videos
            urls.forEach(url => {
                if (url.value === '') {
                    throw new Error('Please add an MP4 URL');
                }

                console.log(`Loading video: ${url.value}`);

                // Create video element
                let videoElement = document.createElement('video');
                videoElement.width = 320;
                videoElement.height = 240;
                videoElement.controls = true;
                videoElement.autoplay = true;

                // Create source element
                let sourceElement = document.createElement('source');
                sourceElement.src = url.value;
                sourceElement.type = 'video/mp4';

                // Append source to video
                videoElement.appendChild(sourceElement);
                // Append video to grid
                videoGrid.appendChild(videoElement);

                // Fetch the video to establish media session
                fetch(url.value, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + accessToken,
                        'accept': '*/*',
                        'cookie': document.cookie,
                        'referer': 'https://mp4.mvleest.app/',
                        'sec-fetch-dest': 'video',
                        'sec-fetch-mode': 'no-cors',
                        'sec-fetch-site': 'cross-site',
                    
                    },
                    credentials: 'include'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to load video');
                    }
                    console.log(`Video ${url.value} loaded successfully`);
                })
                .catch(error => {
                    console.error('Error loading video:', error);
                });
            });

            videoContainer.appendChild(videoGrid);
        } catch (error) {
            console.error('Error loading videos:', error);
            videoContainer.innerHTML = `<div class="alert">${error.message}</div>`;
        }
    }
    </script>
</body>
</html>
