import requests
from plugins.weather import run as weather_run
from plugins.news import run as news_run
from plugins.calendar import run as calendar_run

TOOL_NAME = "briefing"
TOOL_DESCRIPTION = "gives a spoken morning briefing combining weather, today's calendar, and top news"
TOOL_ARGS = {"city": "str (default Mumbai)", "topic": "str (news topic, default technology)"}


def _speak(text: str):
    try:
        requests.post("http://127.0.0.1:5000/speak", json={"text": text}, timeout=5)
    except Exception:
        pass


def run(args: dict) -> dict:
    city = args.get("city", "Mumbai")
    topic = args.get("topic", "technology")

    parts = []

    # Weather
    try:
        w = weather_run({"city": city, "speak": False})
        if w.get("status") == "ok":
            parts.append(f"Weather in {city}: {w['description']}, {w['temp']} degrees, feels like {w['feels_like']}.")
        else:
            parts.append("Weather data unavailable.")
    except Exception as e:
        parts.append(f"Weather check failed: {e}")

    # Calendar — today's events
    try:
        c = calendar_run({"action": "today"})
        if c.get("status") == "ok":
            events = c.get("events", [])
            if events:
                parts.append(f"You have {len(events)} event(s) today: " + "; ".join(events))
            else:
                parts.append("No events on your calendar today.")
        else:
            parts.append("No events on your calendar today.")
    except Exception as e:
        parts.append(f"Calendar check failed: {e}")

    # News — top headlines
    try:
        n = news_run({"topic": topic})
        if n.get("status") == "ok":
            parts.append(f"Top {topic} news: {n['result']}")
        else:
            parts.append("News unavailable.")
    except Exception as e:
        parts.append(f"News check failed: {e}")

    full_briefing = "\n\n".join(parts)
    _speak(" ".join(parts).replace("\n", " "))

    return {"status": "ok", "result": full_briefing}
