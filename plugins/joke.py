import requests

TOOL_NAME = "joke"
TOOL_DESCRIPTION = "Tell a random joke"
TOOL_ARGS = {"category": "str (optional): programming, misc, dark, pun"}

def run(args=None):
    category = args.get("category", "Programming") if args else "Programming"
    r = requests.get(f"https://v2.jokeapi.dev/joke/{category}?safe-mode")
    data = r.json()
    if data.get("type") == "single":
        text = data["joke"]
    else:
        text = f"{data['setup']} ... {data['delivery']}"
    return {"status": "ok", "joke": text, "result": text}
