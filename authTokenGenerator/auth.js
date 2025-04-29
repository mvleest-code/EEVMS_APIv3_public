const axios = require('axios');
const readline = require('readline');
const querystring = require('querystring');
require('dotenv').config();

const URL = 'https://auth.eagleeyenetworks.com/oauth2/token';

// Helper to read refresh_token from CLI
const ask = (question) => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  return new Promise(resolve => rl.question(question, answer => {
    rl.close();
    resolve(answer.trim());
  }));
};

// Base64 encode client_id:client_secret
const encodeClientCredentials = (clientId, clientSecret) => {
  return Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
};

// Make POST request
const makeRequest = async (url, headers, data) => {
  try {
    const response = await axios.post(url, querystring.stringify(data), { headers });
    return response.data;
  } catch (error) {
    console.error(`Error: ${error.message}`);
    if (error.response) {
      console.error(`Status: ${error.response.status}, Reason: ${error.response.statusText}`);
    }
    throw error;
  }
};

const main = async () => {
  const client_id = process.env.CLIENT_ID;
  const client_secret = process.env.CLIENT_SECRET;

  if (!client_id || !client_secret) {
    console.error('Missing CLIENT_ID or CLIENT_SECRET in .env');
    process.exit(1);
  }

  const refresh_token = await ask('Enter the value for refresh_token: ');
  if (!refresh_token) {
    console.error('Missing refresh_token input.');
    process.exit(1);
  }

  const encodedCredentials = encodeClientCredentials(client_id, client_secret);

  const headers = {
    'Accept': 'application/json',
    'Authorization': `Basic ${encodedCredentials}`,
    'Content-Type': 'application/x-www-form-urlencoded'
  };

  const data = {
    grant_type: 'refresh_token',
    refresh_token
  };

  const response = await makeRequest(URL, headers, data);
  console.log(JSON.stringify(response, null, 2));
};

main();