import time
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zyp"))

from plugins.calendar import run as calendar_run
import requests

CHECK_INTERVAL = 300  # 5 minutes — finer granularity to catch both windows
REMINDER_WINDOWS = [30, 10]  # minutes before event to remind
LOG_FILE = os.path.expanduser("~/zyp/logs/reminder.log")
REMINDED_FILE = os.path.expanduser("~/zyp/state/reminded_events.txt")


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def speak(text):
    try:
        requests.post("http://127.0.0.1:5000/speak", json={"text": text}, timeout=5)
    except Exception:
        pass


def get_reminded():
    if not os.path.exists(REMINDED_FILE):
        return set()
    with open(REMINDED_FILE) as f:
        return set(line.strip() for line in f if line.strip())


def mark_reminded(event_id):
    with open(REMINDED_FILE, "a") as f:
        f.write(event_id + "\n")


def check_events():
    reminded = get_reminded()
    result = calendar_run({"action": "today"})

    if result.get("status") != "ok":
        return

    events = result.get("events", [])
    now = datetime.now()

    for event_str in events:
        try:
            time_part, title = event_str.split(":", 1)
            event_time = datetime.fromisoformat(time_part.strip())
            minutes_until = (event_time.replace(tzinfo=None) - now).total_seconds() / 60

            for window in REMINDER_WINDOWS:
                event_id = f"{time_part}_{title.strip()}_{window}min"
                if event_id in reminded:
                    continue

                lower_bound = window - (CHECK_INTERVAL / 60)
                if lower_bound <= minutes_until <= window:
                    msg = f"Reminder: {title.strip()} starts in {window} minutes."
                    log(msg)
                    speak(msg)
                    mark_reminded(event_id)
        except (ValueError, IndexError):
            continue


def main():
    log("Event reminder started — 30min and 10min windows")
    while True:
        try:
            check_events()
        except Exception as e:
            log(f"Error checking events: {e}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
