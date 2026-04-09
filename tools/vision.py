import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/zyp/.env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VISION_BACKEND = os.environ.get("ZYPHOS_VISION_BACKEND", "groq").lower()

# --- Groq (current machine) ---
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- LLaVA (main machine, local) ---
LLAVA_URL = "http://localhost:1234/v1/chat/completions"
LLAVA_MODEL = "llava-v1.5-7b"


def analyze_screenshot(image_path: str, prompt: str = "What do you see on this screen?") -> str:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    if VISION_BACKEND == "llava":
        # Local LLaVA via LM Studio on main machine
        response = requests.post(
            LLAVA_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": LLAVA_MODEL,
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
    else:
        # Groq (current machine)
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
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
    result = screenshot()
    image_b64 = result.get("image", "")
    if not image_b64:
        return {"error": "no screenshot"}
    tmp_path = "/tmp/zyp_vision.png"
    with open(tmp_path, "wb") as f:
        f.write(base64.b64decode(image_b64))
    description = analyze_screenshot(tmp_path, prompt)
    return {"status": "ok", "description": description}
