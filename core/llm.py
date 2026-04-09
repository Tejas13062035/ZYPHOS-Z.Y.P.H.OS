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

# --- Llama (main machine) ---
LLAMA_URL = "http://localhost:1234/v1/chat/completions"
LLAMA_MODEL = "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF"


def ask(prompt: str, system: str = "", max_tokens: int = 150) -> str:
    if BACKEND == "llama":
        url = LLAMA_URL
        model = LLAMA_MODEL
    else:
        url = PHI_URL
        model = PHI_MODEL

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        r = requests.post(url, json={
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.2
        }, timeout=180)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"
