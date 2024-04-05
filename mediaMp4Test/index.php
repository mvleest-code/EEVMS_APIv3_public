<!DOCTYPE html>
<html>
<head>
    <title>EEN Media Player</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif; // Updated font-family to Roboto
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
        input[type='text'], input[type='buttonremove'] {
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
        <code align="left" style="border: 1px solid #ddd; background-color: #f5f5f5; display: inline-block; padding: 10px;">
            <p style="color: grey; font-size: 14px;">
                This MP4 video loader will load up to 4 MP4 videos from the Eagle Eye Cloud VMS.<br>
                The videos will be loaded in a grid layout.<br>
                In the background, the loader will fetch the client settings and establish a media session.<br> 
                The media session will be used to load the videos.<br>
                The loader will also save the access token and MP4 URL's in local storage.<br>
                <br>
                <a href="https://github.com/mvleest-code/mp4MediaTester" target="_blank"><strong>MP4 Media Tester on Github</strong><br></a>
            </p>
        </code>
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

            let videoGrid = document.createElement('div');
            videoGrid.className = 'video-grid';

            // Load videos
            urls.forEach(url => {
                if (url.value === '') {
                    throw new Error('Please add an MP4 URL');
                }

                console.log(`Loading video: ${url.value}`);
                let videoHtml = `<video width="320" height="240" controls autoplay>
                                    <source src="${url.value}" />
                                 </video>`;
                videoGrid.insertAdjacentHTML('beforeend', videoHtml);
            });

            videoContainer.appendChild(videoGrid);
        } catch (error) {
            videoContainer.innerHTML = `<div class="alert">${error.message}</div>`;
        }
    }
    </script>
</body>
</html>
