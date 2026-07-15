import requests
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "nasa"
TOOL_DESCRIPTION = "Access NASA data — apod, asteroids, earth, donki, image, eonet"
TOOL_ARGS = {"action": "str: apod/asteroids/earth/donki/image/eonet", "query": "str: search term for image action"}

def run(args=None):
    action = args.get("action", "apod") if args else "apod"
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")

    try:
        if action == "apod":
            r = requests.get("https://api.nasa.gov/planetary/apod",
                params={"api_key": api_key}, timeout=15)
            d = r.json()
            result = f"{d.get('title', '')}: {d.get('explanation', '')[:800]}..."
            return {"status": "ok", "result": result, "url": d.get("url", "")}

        elif action == "asteroids":
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            r = requests.get("https://api.nasa.gov/neo/rest/v1/feed",
                params={"start_date": today, "end_date": today, "api_key": api_key},
                timeout=15)
            d = r.json()
            neos = d.get("near_earth_objects", {}).get(today, [])
            count = len(neos)
            hazardous = [n for n in neos if n.get("is_potentially_hazardous_asteroid")]
            closest = min(neos, key=lambda x: float(
                x["close_approach_data"][0]["miss_distance"]["kilometers"]
            )) if neos else None
            result = (
                f"{count} asteroids passing Earth today. "
                f"{len(hazardous)} potentially hazardous. "
                f"Closest: {closest['name']} at "
                f"{float(closest['close_approach_data'][0]['miss_distance']['kilometers']):,.0f} km"
                if closest else f"{count} asteroids passing Earth today."
            )
            return {"status": "ok", "result": result}

        elif action == "earth":
            r = requests.get("https://api.nasa.gov/EPIC/api/natural",
                params={"api_key": api_key}, timeout=15)
            d = r.json()
            if d:
                photo = d[0]
                date = photo["date"].split(" ")[0].replace("-", "/")
                img = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{photo['image']}.png"
                result = f"Latest Earth photo from {photo['date']}: {photo['caption']}"
                return {"status": "ok", "result": result, "url": img}
            return {"error": "no earth photos available"}

        elif action == "donki":
            from datetime import datetime, timedelta
            end = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            r = requests.get("https://api.nasa.gov/DONKI/FLR",
                params={"startDate": start, "endDate": end, "api_key": api_key},
                timeout=15)
            d = r.json()
            if d:
                latest = d[-1]
                result = (
                    f"Latest solar flare: Class {latest.get('classType', 'unknown')} "
                    f"on {latest.get('beginTime', 'unknown')[:10]}. "
                    f"Peak time: {latest.get('peakTime', 'unknown')}"
                )
            else:
                result = "No solar flares in the last 7 days"
            return {"status": "ok", "result": result}

        elif action == "image":
            query = args.get("query", "galaxy") if args else "galaxy"
            r = requests.get("https://images-api.nasa.gov/search",
                params={"q": query, "media_type": "image", "page_size": 1},
                timeout=15)
            d = r.json()
            items = d.get("collection", {}).get("items", [])
            if items:
                item = items[0]
                data = item.get("data", [{}])[0]
                links = item.get("links", [{}])
                result = f"{data.get('title', '')}: {data.get('description', '')[:200]}..."
                url = links[0].get("href", "") if links else ""
                return {"status": "ok", "result": result, "url": url}
            return {"error": "no images found"}

        elif action == "eonet":
            r = requests.get("https://eonet.gsfc.nasa.gov/api/v3/events",
                params={"status": "open", "limit": 5},
                timeout=15)
            d = r.json()
            events = d.get("events", [])
            if events:
                lines = [f"- {e['title']} ({e['categories'][0]['title']})" for e in events]
                result = "Active natural events:\n" + "\n".join(lines)
            else:
                result = "No active natural events"
            return {"status": "ok", "result": result}

        else:
            return {"error": f"unknown action: {action}. Use: apod, asteroids, earth, donki, image, eonet"}

    except Exception as e:
        return
