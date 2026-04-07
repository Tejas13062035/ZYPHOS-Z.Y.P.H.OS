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
