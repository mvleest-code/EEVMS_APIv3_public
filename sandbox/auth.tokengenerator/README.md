## How to Use the Token Generator

The `app.tokengenerator.py` script is designed to generate secure tokens for authentication purposes. Follow the steps below to use the token generator:

1. **Install Dependencies**: Ensure you have all the necessary dependencies installed. You can install them using:
    ```bash
    pip install -r requirements.txt
    ```

2. **Add Client ID and Secret**: Before running the script, you need to add your client ID and secret. Open the `app.tokengenerator.py` file and add your credentials in the appropriate variables.

3. **Request Non-Rotating Refresh Token**: Ensure you request a non-rotating refresh token from your authentication provider. This will allow you to use the `refresh_token` permanently.

4. **Run the Script**: Execute the script to generate a token:
    ```bash
    python app.tokengenerator.py
    ```

5. **Token Output**: The generated token will be displayed in the console. You can use this token for your authentication needs.

6. **Configuration**: If needed, you can configure the script by modifying the settings in the script file to suit your requirements.

For more detailed information, refer to the comments within the script or the documentation provided.