import os
import sounddevice as sd
import numpy as np
import audioop
import requests
import io

access_token = ""
cameraId = ""

def clear_terminal():
    """
    Clear the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def record_audio(duration, fs=8000):
    """
    Record audio from the microphone.
    """
    print(f"Recording {duration} seconds of audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return recording

def encode_alaw(audio_data):
    """
    Encode audio data to A-law.
    """
    print("Encoding audio to A-law...")
    audio_bytes = audio_data.tobytes()
    alaw_data = audioop.lin2alaw(audio_bytes, 2)
    print("Encoding complete.")
    return alaw_data

def send_audio(encoded_audio, url, access_token):
    """
    Send encoded audio via HTTPS POST request using in-memory file.
    """
    print("Sending audio to server...")
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'multipart/form-data',
    }
    files = {
        'data': ('audio.alaw', io.BytesIO(encoded_audio), 'audio/x-alaw')
    }
    response = requests.post(url, headers=headers, files=files)
    print("sending complete.")
    print(response.text)

def main():
    # Clear the terminal
    clear_terminal()

    # Authenticate and set up
    url = f'https://media.c001.eagleeyenetworks.com:443/media/streams/audio/{cameraId}/alaw'
    
    # Record, encode, and send the audio
    audio_data = record_audio(duration=5)  # 5 seconds of audio
    encoded_audio = encode_alaw(audio_data)
    send_audio(encoded_audio, url, access_token)

if __name__ == "__main__":
    main()
