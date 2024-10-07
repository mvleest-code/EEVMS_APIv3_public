# EEVMS API v3 Iframe "monitor"

## Setup

To set up the application, you need to provide the refresh token and the client credentials. These are required for authentication and authorization purposes.

### Environment Variables

You need to set the following environment variables:

- `REFRESH_TOKEN`: This is the token used to refresh the authentication session.
- `AUTH_HEADER`: This should be a base64 encoded string in the format `Basic clientid:clientsecret`.

### Example

```python
import os

# Get refresh token and authorization header from environment
refresh_token = os.getenv("REFRESH_TOKEN", "")
auth_header = os.getenv("AUTH_HEADER", "")  # should be: 'Basic clientid:clientsecret' as base64 encoded
```

Make sure to replace `clientid` and `clientsecret` with your actual client ID and client secret, then base64 encode the string `clientid:clientsecret`.

## Running the Application

Once you have set the environment variables, you can run the application using your preferred method. The application will use the provided credentials to authenticate and monitor the EEVMS API v3.

## Features

- Displays the "all cameras" layout of a specified account within an iframe.
- Requires a refresh token and client credentials (client ID and secret) for authentication.
- Automatically refreshes the token in the background, ensuring continuous operation without user interaction.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines before submitting a pull request.

## Contact

For any questions or issues, please open an issue on GitHub.

## Usage

After setting up the environment variables, the application will load the iframe and start monitoring the "all cameras" layout. No further user interaction is required once the application is running.