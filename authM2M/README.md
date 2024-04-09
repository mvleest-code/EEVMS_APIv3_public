## ee_apiv3_m2m_login

### genRefTokenCodeSample.py
Add `clientId`and `clientSecret`and run `genRefTokenCodeSample.py` it will follow the Eagle Eye Networks API v3 `authorization code` grant type to login and generate both `access_token` and `refresh_token`
When `Non-rotating refresh_token` is enabled, this script can be used to generate the permanent token to store service side instead of username/password.

### generate_access_token.py
Generate new `access_token`using the `refresh_token` grant type.