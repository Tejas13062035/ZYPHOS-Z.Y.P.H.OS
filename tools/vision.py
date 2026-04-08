import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/zyp/.env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_screenshot(image_path: str, prompt: str = "What do you see on this screen?") -> str:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                    ]
                }
            ],
            "max_tokens": 500
        }
    )
    return response.json()["choices"][0]["message"]["content"].strip()

def look(prompt: str = "What do you see on this screen?") -> dict:
    from tools.sidecar import screenshot
    import tempfile

    result = screenshot()
    image_b64 = result.get("image", "")
    if not image_b64:
        return {"error": "no screenshot"}

    tmp_path = "/tmp/zyp_vision.png"
    with open(tmp_path, "wb") as f:
        f.write(base64.b64decode(image_b64))

    description = analyze_screenshot(tmp_path, prompt)
    return {"status": "ok", "description": description}
