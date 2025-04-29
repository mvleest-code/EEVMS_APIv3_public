# Eagle Eye Networks OAuth Node.JS

This sample Express application allows partners and developers to securely obtain a **refresh token** using the OAuth2 Authorization Code flow for the Eagle Eye Networks REST API.

This tool is useful when applications can't handle a full OAuth flow (e.g., IoT devices, CLI tools). For full OAuth reference, see the [API documentation](https://developer.eagleeyenetworks.com/docs/getting-started).

---

## Requirements

- Node.js v20.14.0 or higher
- express
- axios
- dotenv

---

## Setup

1. Install dependencies:
   ```bash
   npm install express axios dotenv
   ```

2. Create a `.env` file:
   ```env
   CLIENT_ID=your-client-id-here
   CLIENT_SECRET=your-client-secret-here
   ```

3. Clone or copy this repository and make sure the `main.js` and `auth.js` files are present.

---

## Running the Application

Start the server:
```bash
node main.js
```
Local server will run at:  
➡️ `http://127.0.0.1:3333`

---

## Usage

1. Open `http://127.0.0.1:3333` in your browser.
2. You will be redirected to the Eagle Eye Networks login page.
3. After login, a secure `code` and `state` are returned.
4. The app validates the `state` and exchanges the `code` for tokens.
5. The page displays your **refresh token**. Copy it for your application.

---

## How It Works

### `main.js`

- Starts an Express server on `127.0.0.1:3333`.
- Redirects user to the Eagle Eye OAuth login if no code is present.
- Generates and validates a `state` parameter (CSRF protection).
- Exchanges the authorization `code` for a **refresh token**.
- Displays the refresh token on a Bootstrap-styled HTML page with copy and logout functionality.

### `auth.js`

- CLI tool to **refresh access tokens** using a **refresh token**.
- Reads client ID/secret from `.env`.
- Prompts the user for a refresh token via command line.
- Encodes client credentials and makes a secure POST request to the OAuth token endpoint.
- Prints the new access token to the console.

---

## Security Features

- ✅ `.env` file for secrets (no hardcoded credentials)
- ✅ OAuth `state` parameter handling (anti-CSRF)
- ✅ Secure display and manual copy of refresh tokens
- ✅ No access tokens logged or exposed
- ✅ Manual logout option

> ⚠️ **Important:** Deploy behind HTTPS or use access controls to protect the local server.

---

## Support

If you encounter any issues, contact your technical partner manager or check the [API documentation](https://developer.eagleeyenetworks.com/docs).

