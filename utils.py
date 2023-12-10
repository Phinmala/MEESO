import requests
import pygame
import keyboard
import time
import os

def text_to_speech(text, voice="fable", model="tts-1"):
    api_key = os.environ.get('OPENAI_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "input": text,
        "voice": voice,
        "speed": 1.15
    }
    response = requests.post("https://api.openai.com/v1/audio/speech", json=data, headers=headers)
    
    if response.status_code == 200:
        audio_folder = "audio"
        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)

        audio_file = os.path.join(audio_folder, f"output_{int(time.time())}.mp3")
        with open(audio_file, "wb") as file:
            file.write(response.content)
        return audio_file
    else:
        print("[ERROR] Error in TTS:", response.status_code, response.text)
        return None

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    print("\n>> Audio is playing. Press the spacebar to interrupt.\n")

    while pygame.mixer.music.get_busy():
        if keyboard.is_pressed('space'):
            pygame.mixer.music.stop()
            print(">> Audio playback interrupted.\n")
            break
        pygame.time.Clock().tick(10)

    # Ensure the mixer is unloaded before deleting the file
    pygame.mixer.music.unload()
    pygame.mixer.quit()

    # Wait a moment to ensure the file is released
    time.sleep(1)

    # Delete the audio file after playing or interrupting
    try:
        os.remove(file_path)
    except PermissionError:
        print(f"[ERROR] Unable to delete the file: {file_path}. It may still be in use.")