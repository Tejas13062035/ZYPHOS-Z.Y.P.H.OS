import requests

TOOL_NAME = "joke"
TOOL_DESCRIPTION = "Tell a random joke"
TOOL_ARGS = {"category": "str (optional): programming, misc, dark, pun"}

def run(args=None):
    category = args.get("category", "Any") if args else "Any"
    amount = args.get("count", 1) if args else 1
    r = requests.get(f"https://v2.jokeapi.dev/joke/{category}?amount={amount}")
    data = r.json()
    if amount == 1 or "joke" in data:
        if data.get("type") == "single":
            text = data["joke"]
        else:
            text = f"{data['setup']} ... {data['delivery']}"
    else:
        jokes = data.get("jokes", [])
        lines = []
        for j in jokes:
            if j.get("type") == "single":
                lines.append(j["joke"])
            else:
                lines.append(f"{j['setup']} ... {j['delivery']}")
        text = "\n".join(lines)
    return {"status": "ok", "joke": text, "result": text}
