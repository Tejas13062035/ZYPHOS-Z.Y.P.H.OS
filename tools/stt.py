import whisper
import requests
import time
import os

SIDECAR_URL = "http://127.0.0.1:5000"
AUDIO_PATH = "/mnt/c/zyphos_sidecar/audio.wav"
MODEL_SIZE = "base"

model = None

def load_model():
    global model
    if model is None:
        print("STT: loading Whisper model...")
        model = whisper.load_model(MODEL_SIZE)
        print("STT: model ready")
    return model

def record(duration=5):
    r = requests.post(f"{SIDECAR_URL}/record", json={"duration": duration})
    if r.json().get("status") != "recording":
        raise RuntimeError("Sidecar record failed")
    print(f"STT: recording for {duration}s...")
    time.sleep(duration + 1)

def transcribe():
    if not os.path.exists(AUDIO_PATH):
        raise FileNotFoundError(f"No audio file at {AUDIO_PATH}")
    m = load_model()
    print("STT: transcribing...")
    result = m.transcribe(AUDIO_PATH)
    text = result["text"].strip()
    print(f"STT: heard → {text}")
    return text

def listen(duration=5):
    record(duration)
    return transcribe()
