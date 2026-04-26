import time
import threading
import requests

TOOL_NAME = "timer"
TOOL_DESCRIPTION = "Set a timer or reminder. Speaks when time is up."
TOOL_ARGS = {"minutes": "number of minutes", "message": "reminder message"}

SIDECAR_URL = "http://127.0.0.1:5000"

def _ring(message: str):
    try:
        requests.post(f"{SIDECAR_URL}/speak", json={"text": message})
    except:
        print(f"TIMER: {message}")

def run(args: dict) -> dict:
    minutes = float(args.get("minutes", 1))
    seconds = float(args.get("seconds", 0))
    message = args.get("message", f"Timer done! {minutes} minutes are up.")
    
    total_seconds = minutes * 60 + seconds

    def countdown():
        time.sleep(total_seconds)
        _ring(message)

    t = threading.Thread(target=countdown, daemon=True)
    t.start()

    return {
        "status": "timer set",
        "minutes": minutes,
        "message": message
    }
