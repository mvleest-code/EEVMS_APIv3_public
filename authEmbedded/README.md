# apiv3_embedded_login

```
vmslocalhost.py:
```
flask webserver that should run server side, add your clientId and secret.<br>
<br>
Default redirect URI is set to HTTP://127.0.0.1:3333/ and it will save the oautheObject to: <br>
```
{userId}_access_response.json
```
This file will contain:
```
{
    "access_token": "",
    "refresh_token": "",
    "scope": "vms.all",
    "token_type": "Bearer",
    "expires_i
    n": 604799
}
```

When you start this server it will start at: HTTP://127.0.0.1:3333.<br>
It will redirect you to https://auth.eagleeyenetworks.com.<br>
<br>
IMPORTANT: NEVER SHARE THE REFRESH TOKEN, THIS SHOULD BE SECURELY STORED SERVER-SIDE<br>

```
generate_new_token.py
```
Script to refresh the *access_token* using the *refresh_token* this can be scheduled:<br>
<br>
*WINDOWS BATCH FILE*
```
:loop
C:\path\to\python.exe C:\path\to\your_script.py
timeout /t 39600 /nobreak
goto loop
```
Save this as a .bat file and then you can use Task Scheduler to run this batch file at startup or logon.<br>
<br>
*LINUX/MACOS CRON JOB*<br>
You can use the cron utility to schedule tasks. To edit your cron jobs, open the terminal and run:<br>
```
crontab -e
```
Add a line like the following to schedule your Python script:<br>
```
0 */11 * * * /path/to/python3 /path/to/generate_new_token.py
```
This will run your Python script at minute 0 every 11 hours.<br>
<br>
*Using a Shell Script*<br>
You can create a simple shell script to run your Python script every 11 hours:<br>

```
#!/bin/bash

while true; do
    /path/to/python3 /path/to/your_script.py
    sleep 39600
done
```
Make this script executable by running chmod +x your_script.sh and then you can either run this manually or use something like cron or systemd to start this script at boot.<br>
<br>
*Python time.sleep*<br>
You can also make the Python script itself responsible for the timing, though this is generally less advisable since it would require the Python interpreter to be running continuously.<br>
<br>
Here's how you could do it:<br>
```
import time
from your_script import main_function  # Assuming you have a main_function in your_script.py

while True:
    main_function()
    time.sleep(11 * 60 * 60)  # Sleeps for 11 hours
```
How to encode the clientId and secret:<br>
```
encode_cc_base64.py
```
Add your clientId and Secret to the script, the response can then be copied into:<br>
```
clientidbase64.json
```




