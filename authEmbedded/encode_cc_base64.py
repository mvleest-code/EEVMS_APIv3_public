import base64
client_id = ""
client_secret = ""
auth_string = f"{client_id}:{client_secret}"

encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
print(f"Encoded: {encoded_auth_string}")
