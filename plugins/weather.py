import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "weather"
TOOL_DESCRIPTION = "Get current weather for any city"
TOOL_ARGS = {"city": "city name e.g. Mumbai", "speak": "true/false to speak the result"}

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def run(args: dict) -> dict:
    city = args.get("city", "Mumbai")
    speak = args.get("speak", False)

    try:
        r = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }, timeout=10)
        data = r.json()

        if data.get("cod") != 200:
            return {"error": data.get("message", "city not found")}

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        summary = f"{city}: {desc}, {temp}°C, feels like {feels}°C, humidity {humidity}%, wind {wind} m/s"

        if speak:
            try:
                requests.post("http://127.0.0.1:5000/speak", json={"text": summary})
            except:
                pass

        return {
            "status": "ok",
            "city": city,
            "temp": temp,
            "feels_like": feels,
            "humidity": humidity,
            "description": desc,
            "wind": wind,
            "summary": summary
        }

    except Exception as e:
        return {"error": str(e)}
