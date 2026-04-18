import json
import os

PERSONALITY_FILE = os.path.expanduser("~/zyp/state/personality.json")

def load():
    if not os.path.exists(PERSONALITY_FILE):
        return {}
    with open(PERSONALITY_FILE) as f:
        return json.load(f)

def save(data: dict):
    with open(PERSONALITY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def remember(fact: str):
    data = load()
    parts = fact.split(" is ", 1)
    if len(parts) == 2:
        key = parts[0].strip()
        value = parts[1].strip()
    else:
        parts = fact.split(" ", 1)
        key = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else fact
    data[key] = value
    save(data)
    return f"Remembered: {key} = {value}"

def forget(key: str):
    data = load()
    if key in data:
        del data[key]
        save(data)
        return f"Forgot: {key}"
    return f"Not found: {key}"

def recall_all():
    data = load()
    if not data:
        return "No personality data stored."
    return "\n".join([f"{k}: {v}" for k, v in data.items()])
