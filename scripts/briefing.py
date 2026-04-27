import os
import sys
import requests
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/zyp"))

SIDECAR_URL = "http://127.0.0.1:5000"

def speak(text):
    try:
        requests.post(f"{SIDECAR_URL}/speak", json={"text": text})
    except:
        print(text)

def briefing():
    now = datetime.now()
    greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 17 else "Good evening"
    
    speak(f"{greeting} Tejas. Here is your daily briefing.")

    # date
    date_str = now.strftime("%A, %B %d, %Y")
    speak(f"Today is {date_str}.")

    # weather
    try:
        from plugins.weather import run as weather_run
        w = weather_run({"city": "Godda"})
        if w.get("status") == "ok":
            speak(f"Weather in Godda: {w['description']}, {w['temp']} degrees Celsius.")
    except Exception as e:
        speak("Weather unavailable.")

    # calendar
    try:
        from plugins.calendar import run as cal_run
        events = cal_run({"action": "today"})
        if events.get("status") == "ok":
            speak(f"You have {len(events['events'])} event today.")
            for e in events["events"]:
                speak(e)
        else:
            speak("No events on your calendar today.")
    except:
        speak("Calendar unavailable.")

    # notes
    try:
        from plugins.notes import run as notes_run
        notes = notes_run({"action": "list"})
        if notes.get("status") == "ok":
            speak(f"You have {len(notes['notes'])} saved notes.")
        else:
            speak("No notes saved.")
    except:
        pass

    # top news
    try:
        from tools.search import web_search
        results = web_search("top news today India", max_results=2)
        if results:
            speak("Top news today:")
            for r in results[:2]:
                speak(r["title"])
    except:
        pass

    speak("That's your briefing. Have a productive day, Tejas.")

if __name__ == "__main__":
    briefing()
