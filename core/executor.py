from tools.vision import look
from tools.sidecar import click, type_text, screenshot, scroll, drag, hotkey

def execute_task(task: dict) -> dict:
    desc = task.get("description", "").lower()
    result = None

    if "click" in desc:
        parts = desc.split()
        try:
            x = int(parts[parts.index("click") + 1])
            y = int(parts[parts.index("click") + 2])
            result = click(x, y)
        except (ValueError, IndexError):
            result = {"error": "click requires x y coordinates"}

    elif "type" in desc:
        parts = desc.split("type ", 1)
        text = parts[1] if len(parts) > 1 else ""
        result = type_text(text)

    elif "screenshot" in desc:
        result = screenshot()
        result = {"status": "screenshot taken", "has_image": "image" in result}

    elif "search" in desc and ("chrome" in desc or "browser" in desc or "tab" in desc):
        import requests as req
        query = desc.replace("search", "").replace("chrome", "").replace("browser", "").replace("tab", "").replace("in", "").strip()
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        r = req.post("http://127.0.0.1:5000/open_url", json={"url": search_url})
        result = r.json()

    elif "open" in desc and ("chrome" in desc or "tab" in desc or "browser" in desc):
        import requests as req
        url = "https://google.com"
        r = req.post("http://127.0.0.1:5000/open_url", json={"url": url})
        result = r.json()

    elif "scroll" in desc:
        parts = desc.split()
        try:
            x = int(parts[parts.index("scroll") + 1])
            y = int(parts[parts.index("scroll") + 2])
            amount = int(parts[parts.index("scroll") + 3]) if len(parts) > parts.index("scroll") + 3 else 3
            result = scroll(x, y, amount)
        except (ValueError, IndexError):
            result = {"error": "scroll requires x y coordinates"}

    elif "drag" in desc:
        parts = desc.split()
        try:
            x1 = int(parts[parts.index("drag") + 1])
            y1 = int(parts[parts.index("drag") + 2])
            x2 = int(parts[parts.index("drag") + 3])
            y2 = int(parts[parts.index("drag") + 4])
            result = drag(x1, y1, x2, y2)
        except (ValueError, IndexError):
            result = {"error": "drag requires x1 y1 x2 y2 coordinates"}

    elif "hotkey" in desc:
        parts = desc.split()
        idx = parts.index("hotkey")
        keys = parts[idx + 1:]
        result = hotkey(keys) if keys else {"error": "hotkey requires at least one key"}

    elif "look" in desc:
        prompt = desc.replace("look", "").strip() or "What do you see on this screen?"
        result = look(prompt)

    elif "search" in desc:
        from tools.search import search_summary
        query = desc.split("search ", 1)[1] if "search " in desc else desc
        result = {"status": "ok", "result": search_summary(query)}

    elif desc.startswith("play "):
        from plugins.music import run as music_run
        query = desc[5:].strip()
        result = music_run({"action": "play", "query": query})

    elif "stop music" in desc or desc == "stop":
        from plugins.music import stop_music
        result = stop_music()

    elif "calendar" in desc or "schedule" in desc or "remind" in desc:
        from plugins.calendar import run as cal_run
        result = cal_run({"action": "today"})

    else:
        result = {"error": f"unknown task: {desc}"}

    task["status"] = "done"
    task["result"] = result
    return task
