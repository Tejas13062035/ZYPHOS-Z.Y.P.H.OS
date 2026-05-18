import requests

SIDECAR_URL = "http://127.0.0.1:5000"

def click(x, y):
    r = requests.post(f"{SIDECAR_URL}/click", json={"x": x, "y": y})
    return r.json()

def type_text(text):
    r = requests.post(f"{SIDECAR_URL}/type", json={"text": text})
    return r.json()

def screenshot():
    r = requests.get(f"{SIDECAR_URL}/screenshot")
    return r.json()

def scroll(x, y, amount=3):
    r = requests.post(f"{SIDECAR_URL}/scroll", json={"x": x, "y": y, "amount": amount})
    return r.json()

def drag(x1, y1, x2, y2, duration=0.5):
    r = requests.post(f"{SIDECAR_URL}/drag", json={"x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration": duration})
    return r.json()

def hotkey(keys: list):
    r = requests.post(f"{SIDECAR_URL}/hotkey", json={"keys": keys})
    return r.json()

def speak(text: str, voice: str = "en-GB-RyanNeural"):
    return speak_edge(text, voice)

def speak_edge(text: str, voice: str = "en-GB-RyanNeural"):
    import subprocess
    audio_wsl = "/tmp/zyp_tts.mp3"
    audio_win_wsl = "/mnt/c/zyphos_sidecar/zyp_tts.mp3"
    audio_win = r"C:\zyphos_sidecar\zyp_tts.mp3"
    
    # generate MP3
    subprocess.run([
        "edge-tts",
        "--text", text,
        "--voice", voice,
        "--write-media", audio_wsl
    ])
    
    # copy to Windows-accessible path
    import shutil
    shutil.copy(audio_wsl, audio_win_wsl)
    
    # play via sidecar
    r = requests.post(f"{SIDECAR_URL}/play", json={"path": audio_win})
    return r.json()
