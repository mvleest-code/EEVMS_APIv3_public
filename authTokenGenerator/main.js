const express = require('express');
const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

const app = express();
const clientId = process.env.CLIENT_ID;
const clientSecret = process.env.CLIENT_SECRET;
const hostName = '127.0.0.1';
const port = 3333;
const stateStore = new Set();

const getTokens = async (code) => {
  const url = `https://auth.eagleeyenetworks.com/oauth2/token?grant_type=authorization_code&scope=vms.all&code=${code}&redirect_uri=http://${hostName}:${port}`;
  const response = await axios.post(url, {}, {
    auth: { username: clientId, password: clientSecret }
  });
  return response.data;
};

app.get('/', async (req, res) => {
  const code = req.query.code;
  const returnedState = req.query.state;

  if (!code) {
    const state = crypto.randomUUID();
    stateStore.add(state);
    const authUrl = `https://auth.eagleeyenetworks.com/oauth2/authorize?client_id=${clientId}&response_type=code&scope=vms.all&redirect_uri=http://${hostName}:${port}&state=${state}`;
    return res.redirect(authUrl);
  }

  if (!returnedState || !stateStore.has(returnedState)) {
    return res.status(403).send('Invalid OAuth state.');
  }

  stateStore.delete(returnedState);

  try {
    const tokens = await getTokens(code);
    const refreshToken = tokens.refresh_token;

    const page = `
    <html>
    <head>
      <title>Refresh Token</title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css">
    </head>
    <body>
      <div class="container" style="margin-top: 50px;">
        <div class="row">
          <div class="col-md-12 text-center">
            <h3>Refresh token</h3>
          </div>
        </div>
        
        <div class="row" style="margin-top: 20px;">
          <div class="col-md-12">
            <div style="display: flex; justify-content: center; align-items: center;">
              <input id="tokenInput" type="text" value="${refreshToken}" readonly class="form-control" style="width: 90%; max-width: 800px;">
              <svg onclick="copyToken()" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                   viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round"
                   stroke-linejoin="round" style="cursor: pointer; margin-left: 10px;" title="Copy">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div class="row" style="margin-top: 20px;">
          <div class="col-md-12 text-center">
            <button onclick="logout()" class="btn btn-danger">LOG OUT</button>
          </div>
        </div>
      </div>
      <script>
        function copyToken() {
          const input = document.getElementById('tokenInput');
          input.select();
          document.execCommand('copy');
          alert('Token copied!');
        }
      
        function logout() {
          window.location.href = "/";
        }
      </script>
    </body>
    </html>
    `;
    res.send(page);
  } catch (error) {
    console.error('OAuth error:', error.message);
    res.status(500).send('Authentication failed.');
  }
});

app.listen(port, () => {
  console.log(`Server running at http://${hostName}:${port}`);
});