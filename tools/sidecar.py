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

def speak(text: str):
    r = requests.post(f"{SIDECAR_URL}/speak", json={"text": text})
    return r.json()
