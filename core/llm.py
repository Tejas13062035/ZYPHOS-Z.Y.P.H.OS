import os
import requests

# -----------------------------------------------------------
# BACKEND SWITCH
# Set ZYPHOS_BACKEND=llama in your shell or .env to use
# Llama 3.1 8B on the main machine.
# Default: phi (current machine, LM Studio)
# -----------------------------------------------------------
BACKEND = os.environ.get("ZYPHOS_BACKEND", "phi").lower()

# --- Phi (current machine) ---
PHI_URL = "http://localhost:1234/v1/chat/completions"
PHI_MODEL = "phi-3.5-mini-instruct"

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
OLLAMA_MODEL = "gemma3:4b"

PROFILE_FILE = os.path.expanduser("~/zyp/state/user_profile.txt")
PERSONALITY_FILE = os.path.expanduser("~/zyp/state/personality.json")

def load_profile():
    lines = []
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE) as f:
            lines.append(f.read().strip())
    if os.path.exists(PERSONALITY_FILE):
        import json
        with open(PERSONALITY_FILE) as f:
            data = json.load(f)
        for k, v in data.items():
            lines.append(f"{k}: {v}")
    return "\n".join(lines)

def ask(prompt: str, system: str = "", max_tokens: int = 150) -> str:
    profile = load_profile()
    full_system = f"USER PROFILE:\n{profile}\n\n{system}" if profile else system
    messages = []
    if full_system:
        messages.append({"role": "system", "content": full_system})
    messages.append({"role": "user", "content": prompt})
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.2
        }, timeout=120)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"

def ask_groq(prompt: str, system: str = "", max_tokens: int = 150) -> str:
    try:
        import os
        from groq import Groq
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/zyp/.env"))
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"
