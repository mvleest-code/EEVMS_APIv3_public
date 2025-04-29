# Eagle Eye Networks OAuth Node.JS

This sample Express application allows partners and internal developers to securely obtain a **refresh token** using the OAuth2 Authorization Code flow for the Eagle Eye Networks REST API.

This tool is specifically intended for use in cases where applications cannot handle a full OAuth flow directly (e.g. IoT devices, CLI tools). For full OAuth reference, see the [API documentation](https://developer.eagleeyenetworks.com/docs/getting-started).

---

## Requirements

- Node.JS v20.14.0 or higher
- Express
- Axios
- dotenv
- helmet

---

## Setup

1. Install dependencies:
   ```bash
   npm install express axios dotenv helmet
   ```

2. Create a `.env` file in the root with:
   ```env
   CLIENT_ID=your-client-id-here
   CLIENT_SECRET=your-client-secret-here
   ```

3. Clone or copy this repository and ensure the `main.js` file matches the security-hardened version.

---

## Running the Application

To start the server:
```bash
node main.js
```
The app will launch a local server at:  
➡️ `http://127.0.0.1:3333`

---

## Usage

1. Navigate to `http://127.0.0.1:3333` in your browser.
2. You will be redirected to the Eagle Eye Networks login page.
3. After login, you will be redirected back with a secure `code` and `state`.
4. The app validates the `state` (CSRF protection), exchanges the code for tokens.
5. The page will display your **refresh token** — copy and use it in your application.

---

## Security Features

- ✅ `.env`-based config (no hardcoded secrets)
- ✅ `helmet` middleware for HTTP header protection
- ✅ OAuth `state` parameter generation & validation
- ✅ CSP meta tag to prevent inline script/style injection
- ✅ Secure token display UI with manual copy + logout
- ✅ No access tokens are exposed
- ✅ No logging of sensitive token data

> ⚠️ **Note:** Partners must host this securely (preferably behind HTTPS and/or access-controlled).

---

## Support

If you encounter any issues or require further assistance, contact your technical partner manager or visit the [API documentation](https://developer.eagleeyenetworks.com/docs).
